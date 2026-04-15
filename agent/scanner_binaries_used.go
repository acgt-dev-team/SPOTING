package main

import (
	"bytes"
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/shirou/gopsutil/v3/process"
)

func runBinariesUsed(args []string) {
	file, err := os.Create("binaries_used.csv")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error creating CSV: %v\n", err)
		return
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	writer.Write([]string{
		"binary",
		"os_type",
		"language",
		"modules/libraries",
		"third party libraries",
		"primitive",
		"algorithm",
		"crypto_library",
		"key_length",
		"parameters",
	})

	osType := detectOS()
	binaries := listRunningBinaries()

	for _, binary := range binaries {
		fmt.Println(binary)
		language := guessLanguage(binary)
		thirdParty, system, _ := classifyLibraries(binary)
		libs := getCryptoDeps(binary)

		if libs == "none" {
			continue
		}

		hits := detectCrypto(binary)
		if len(hits) == 0 {
			writer.Write([]string{
				binary,
				osType,
				"unknown",
				"unknown",
				"unknown",
				"unknown",
				"unknown",
				libs,
				"unknown",
				"none",
			})
			continue
		}

		for _, hit := range hits {
			keyLen := "unknown"
			if kl, ok := hit.Parameters["keyLength"]; ok {
				keyLen = fmt.Sprintf("%v", kl)
				delete(hit.Parameters, "keyLength")
			}

			params := []string{}
			for k, v := range hit.Parameters {
				params = append(params, fmt.Sprintf("%s=%v", k, v))
			}
			paramStr := strings.Join(params, "; ")
			if paramStr == "" {
				paramStr = "none"
			}

			writer.Write([]string{
				binary,
				osType,
				language,
				fmt.Sprintf("%v", system),
				fmt.Sprintf("%v", thirdParty),
				hit.Primitive,
				hit.Algorithm,
				libs,
				keyLen,
				paramStr,
			})
		}
	}

	fmt.Println("Output: binaries_used.csv")
}

func listRunningBinaries() []string {
	binaries := make(map[string]bool)
	osType := detectOS()

	if osType == "unix" {
		procs, err := process.Processes()
		if err == nil {
			for _, proc := range procs {
				exe, err := proc.Exe()
				if err == nil && exe != "" {
					if info, err := os.Stat(exe); err == nil && !info.IsDir() {
						binaries[exe] = true
					}
				}
			}
		}
	} else {
		out := runCmd("tasklist", "/FO", "CSV", "/NH")
		for _, line := range strings.Split(out, "\n") {
			if strings.TrimSpace(line) == "" {
				continue
			}
			// Parse CSV format: "process_name.exe","PID"
			parts := strings.Split(line, ",")
			if len(parts) >= 1 {
				processName := strings.Trim(parts[0], "\"")
				binaries[processName] = true
			}
		}
	}

	result := make([]string, 0, len(binaries))
	for bin := range binaries {
		result = append(result, bin)
	}

	fmt.Printf("%d binaries detected\n", len(result))
	return result
}

func checkBinaryState(filePath string) string {
	absPath, err := filepath.Abs(filePath)
	if err != nil {
		return "Error getting absolute path"
	}

	if _, err := os.Stat(absPath); os.IsNotExist(err) {
		return "File does not exist on disk"
	}

	procs, err := process.Processes()
	if err == nil {
		for _, proc := range procs {
			exe, err := proc.Exe()
			if err == nil && exe == absPath {
				return fmt.Sprintf("STATE: IN USE (Running as PID %d)", proc.Pid)
			}
		}
	}

	return "STATE: AT REST (Static on disk)"
}

func guessLanguage(binaryPath string) string {
	signatures := map[string][]string{
		"Go":     {"go.runtime", "runtime.gopanic"},
		"Rust":   {"rustc/", "rust_panic"},
		"Python": {"py_runmain", "PyZipFile", "_PYI"},
		"C++":    {"GLIBCXX", "std::"},
		"Java":   {"JNI_CreateJavaVM", "java/lang/Object"},
	}

	output := runCmd("strings", binaryPath)

	for lang, sigs := range signatures {
		for _, sig := range sigs {
			if strings.Contains(output, sig) {
				return lang
			}
		}
	}

	return "C"
}

func classifyLibraries(binaryPath string) ([]string, []string, error) {
	f, err := os.Open(binaryPath)
	if err != nil {
		return nil, nil, err
	}
	defer f.Close()

	magic := make([]byte, 4)
	_, err = f.Read(magic)
	if err != nil || !bytes.Equal(magic, []byte{0x7f, 'E', 'L', 'F'}) {
		return []string{}, []string{}, nil
	}

	out := runCmd("ldd", binaryPath)
	if out == "" {
		return []string{}, []string{}, fmt.Errorf("ldd failed")
	}

	systemLibs := []string{}
	thirdPartyLibs := []string{}
	systemPaths := []string{"/lib", "/usr/lib", "/lib64"}

	for _, line := range strings.Split(out, "\n") {
		if !strings.Contains(line, "=>") {
			continue
		}

		parts := strings.Split(line, "=>")
		if len(parts) < 2 {
			continue
		}

		libPath := strings.TrimSpace(strings.Split(parts[1], "(")[0])
		if libPath == "" || libPath == "not found" {
			continue
		}

		isSystem := false
		for _, sp := range systemPaths {
			if strings.HasPrefix(libPath, sp) {
				isSystem = true
				break
			}
		}

		if strings.HasPrefix(libPath, "/usr/local/lib") {
			isSystem = false
		}

		if isSystem {
			systemLibs = append(systemLibs, libPath)
		} else {
			thirdPartyLibs = append(thirdPartyLibs, libPath)
		}
	}

	return thirdPartyLibs, systemLibs, nil
}
