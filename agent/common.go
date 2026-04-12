package main

import (
	"context"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"net"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
	"time"

	"github.com/Ullaakut/nmap/v3"
)

type CryptoRules struct {
	AssetType           string
	AlgorithmProperties AlgoProperties
	ProtocolProperties  ProtoProperties
}

type AlgoProperties struct {
	Primitive     string
	Algorithm     string
	Modes         []string
	KeyLengths    []int
	Curves        []string
	HashFunctions []string
	Paddings      []string
	Deprecated    bool
}

type ProtoProperties struct {
	ProtocolType string
	Versions     []string
	Deprecated   bool
}

type CryptoHit struct {
	Algorithm       string
	Primitive       string
	Parameters      map[string]interface{}
	Confidence      string
	DetectionSource []string
	Deprecated      bool
}

var cryptoRules = initCryptoRules()
var cryptoLibPatterns = []string{
	"libcrypto",
	"libssl",
	"mbedtls",
	"wolfssl",
	"boringssl",
	"libgcrypt",
	"libsodium",
	"nettle",
}

func initCryptoRules() map[string]CryptoRules {
	rules := make(map[string]CryptoRules)

	rules["AES"] = CryptoRules{
		AssetType: "algorithm",
		AlgorithmProperties: AlgoProperties{
			Primitive:  "block-cipher",
			Algorithm:  "AES",
			Modes:      []string{"ECB", "CBC", "CTR", "GCM", "CCM", "XTS"},
			KeyLengths: []int{128, 192, 256},
		},
	}

	rules["3DES"] = CryptoRules{
		AssetType: "algorithm",
		AlgorithmProperties: AlgoProperties{
			Primitive:  "block-cipher",
			Algorithm:  "3DES",
			KeyLengths: []int{112, 168},
		},
	}

	rules["DES"] = CryptoRules{
		AssetType: "algorithm",
		AlgorithmProperties: AlgoProperties{
			Primitive:  "block-cipher",
			Algorithm:  "DES",
			KeyLengths: []int{56},
			Deprecated: true,
		},
	}

	rules["SHA-256"] = CryptoRules{
		AssetType: "algorithm",
		AlgorithmProperties: AlgoProperties{
			Primitive: "hash-function",
			Algorithm: "SHA-256",
		},
	}

	rules["SHA-512"] = CryptoRules{
		AssetType: "algorithm",
		AlgorithmProperties: AlgoProperties{
			Primitive: "hash-function",
			Algorithm: "SHA-512",
		},
	}

	rules["MD5"] = CryptoRules{
		AssetType: "algorithm",
		AlgorithmProperties: AlgoProperties{
			Primitive:  "hash-function",
			Algorithm:  "MD5",
			Deprecated: true,
		},
	}

	rules["RSA"] = CryptoRules{
		AssetType: "algorithm",
		AlgorithmProperties: AlgoProperties{
			Primitive:  "public-key-encryption",
			Algorithm:  "RSA",
			KeyLengths: []int{1024, 2048, 3072, 4096},
		},
	}

	rules["ECDSA"] = CryptoRules{
		AssetType: "algorithm",
		AlgorithmProperties: AlgoProperties{
			Primitive:     "digital-signature",
			Algorithm:     "ECDSA",
			Curves:        []string{"P-256", "P-384", "P-521", "secp256k1"},
			HashFunctions: []string{"SHA-256", "SHA-384", "SHA-512"},
		},
	}

	rules["TLS"] = CryptoRules{
		AssetType: "protocol",
		ProtocolProperties: ProtoProperties{
			ProtocolType: "tls",
			Versions:     []string{"1.0", "1.1", "1.2", "1.3"},
		},
	}

	return rules
}

func detectOS() string {
	if runtime.GOOS == "windows" {
		return "windows"
	}
	return "unix"
}

func runCmd(cmd string, args ...string) string {
	osType := detectOS()
	var out []byte
	var err error

	if osType == "windows" {
		out, err = exec.Command("cmd", "/C", cmd).CombinedOutput()
	} else {
		out, err = exec.Command(cmd, args...).CombinedOutput()
	}

	if err != nil {
		return ""
	}
	return string(out)
}

func getCryptoDeps(binary string) string {
	osType := detectOS()
	var out string

	if osType == "unix" {
		out = runCmd("ldd", binary)
	} else {
		out = runCmd(fmt.Sprintf("dumpbin /imports \"%s\"", binary))
	}

	deps := make(map[string]bool)
	for _, line := range strings.Split(out, "\n") {
		for _, lib := range cryptoLibPatterns {
			if strings.Contains(strings.ToLower(line), strings.ToLower(lib)) {
				deps[lib] = true
			}
		}
	}

	if len(deps) == 0 {
		return "none"
	}

	result := make([]string, 0, len(deps))
	for dep := range deps {
		result = append(result, dep)
	}
	return strings.Join(result, ",")
}

func detectCrypto(binary string) []CryptoHit {
	osType := detectOS()
	var stringsOut, symbolsOut, depsOut string

	if osType == "unix" {
		stringsOut = strings.ToLower(runCmd("strings", binary))
		symbolsOut = strings.ToLower(runCmd("nm", "-D", binary))
		depsOut = strings.ToLower(runCmd("ldd", binary))
	} else {
		stringsOut = strings.ToLower(runCmd(fmt.Sprintf("strings \"%s\"", binary)))
		symbolsOut = strings.ToLower(runCmd(fmt.Sprintf("dumpbin /symbols \"%s\"", binary)))
		depsOut = strings.ToLower(runCmd(fmt.Sprintf("dumpbin /imports \"%s\"", binary)))
	}

	var results []CryptoHit

	for name, meta := range cryptoRules {
		algo := meta.AlgorithmProperties
		proto := meta.ProtocolProperties

		lowerName := strings.ToLower(name)
		if !strings.Contains(stringsOut, lowerName) && !strings.Contains(symbolsOut, lowerName) {
			continue
		}

		hit := CryptoHit{
			Algorithm:       algo.Algorithm,
			Primitive:       algo.Primitive,
			Parameters:      make(map[string]interface{}),
			Confidence:      "low",
			DetectionSource: []string{},
			Deprecated:      algo.Deprecated,
		}

		if hit.Primitive == "" {
			hit.Primitive = proto.ProtocolType
		}
		if hit.Algorithm == "" {
			hit.Algorithm = name
		}

		for _, size := range algo.KeyLengths {
			if strings.Contains(stringsOut, fmt.Sprintf("%d", size)) {
				hit.Parameters["keyLength"] = size
				hit.Confidence = "medium"
				hit.DetectionSource = append(hit.DetectionSource, "string")
				break
			}
		}

		for _, mode := range algo.Modes {
			if strings.Contains(stringsOut, strings.ToLower(mode)) {
				hit.Parameters["mode"] = mode
				hit.DetectionSource = append(hit.DetectionSource, "string")
				break
			}
		}

		if strings.Contains(depsOut, "libcrypto") || strings.Contains(depsOut, "libssl") {
			hit.DetectionSource = append(hit.DetectionSource, "crypto-library")
			hit.Confidence = "medium"
		}

		results = append(results, hit)
	}

	return results
}

var libDirs []string
var libExts []string

func initLibraryDirs() {
	osType := detectOS()
	if osType == "unix" {
		libDirs = []string{
			"/lib",
			"/lib64",
			"/usr/lib",
			"/usr/lib64",
			"/usr/local/lib",
		}
		libExts = []string{".so", ".a", ".la"}
	} else {
		systemRoot := os.Getenv("SystemRoot")
		if systemRoot == "" {
			systemRoot = "C:\\Windows"
		}
		libDirs = []string{
			filepath.Join(systemRoot, "System32"),
			filepath.Join(systemRoot, "SysWOW64"),
		}
		libExts = []string{".dll", ".lib"}
	}
}

func isLibrary(path string) bool {
	osType := detectOS()
	if osType == "windows" {
		lowerPath := strings.ToLower(path)
		for _, ext := range libExts {
			if strings.HasSuffix(lowerPath, ext) {
				return true
			}
		}
		return false
	}

	for _, ext := range libExts {
		if strings.HasSuffix(path, ext) {
			return true
		}
	}
	return false
}

func findLibraries() []string {
	if len(libDirs) == 0 {
		initLibraryDirs()
	}

	libs := make(map[string]bool)

	for _, dir := range libDirs {
		info, err := os.Stat(dir)
		if err != nil || !info.IsDir() {
			continue
		}

		filepath.Walk(dir, func(path string, info os.FileInfo, err error) error {
			if err != nil {
				return nil
			}
			if !info.IsDir() && isLibrary(path) {
				realPath, err := filepath.EvalSymlinks(path)
				if err == nil {
					libs[realPath] = true
				} else {
					libs[path] = true
				}
			}
			return nil
		})
	}

	result := make([]string, 0, len(libs))
	for lib := range libs {
		result = append(result, lib)
	}
	return result
}

func isExecutable(path string) bool {
	osType := detectOS()
	info, err := os.Stat(path)
	if err != nil {
		return false
	}

	if osType == "windows" {
		return !info.IsDir() && strings.HasSuffix(strings.ToLower(path), ".exe")
	}

	return !info.IsDir() && (info.Mode()&0111 != 0)
}

func listBinaries() []string {
	binaries := make(map[string]bool)
	pathEnv := os.Getenv("PATH")

	for _, dir := range strings.Split(pathEnv, string(os.PathListSeparator)) {
		info, err := os.Stat(dir)
		if err != nil || !info.IsDir() {
			continue
		}

		entries, err := os.ReadDir(dir)
		if err != nil {
			continue
		}

		for _, entry := range entries {
			fullPath := filepath.Join(dir, entry.Name())
			if isExecutable(fullPath) {
				binaries[fullPath] = true
			}
		}
	}

	result := make([]string, 0, len(binaries))
	for bin := range binaries {
		result = append(result, bin)
	}

	return result
}

// Network discovery types and functions
type ScanData struct {
	IP              string
	MACAddress      string
	Vendor          string
	OS              string
	Port            uint16
	Protocol        string
	Service         string
	ApplicationType string
	Product         string
	Version         string
}

var appLookup = map[uint16]string{
	22:   "Secure Shell (Admin Access)",
	80:   "Web Server (Insecure)",
	443:  "Web Server (Secure)",
	445:  "Windows File Share (SMB)",
	3306: "MySQL Database",
	3389: "Remote Desktop (RDP)",
	5432: "PostgreSQL Database",
	8000: "Development Web Server",
	8080: "HTTP Proxy/Alternative",
	554:  "RTSP Video Stream (IP Camera)",
	1883: "MQTT (IoT Broker)",
}

func getAppCategory(port uint16) string {
	if cat, ok := appLookup[port]; ok {
		return cat
	}
	return "Unknown / Other"
}

func scanNetworkNmap(networkRange string) {
	fmt.Printf("Scanning %s...\n", networkRange)

	// Try to use nmap if available
	scanner, err := nmap.NewScanner(context.Background(),
		nmap.WithTargets(networkRange),
		nmap.WithServiceInfo(),
		nmap.WithOSDetection(),
		nmap.WithTimingTemplate(nmap.TimingAggressive),
	)

	if err != nil {
		fmt.Printf("Note: nmap not available (%v), using basic network scanning\n", err)
		scanNetworkBasic(networkRange)
		return
	}

	result, warnings, err := scanner.Run()
	if err != nil {
		fmt.Printf("Error running nmap scan: %v, falling back to basic scan\n", err)
		scanNetworkBasic(networkRange)
		return
	}

	if warnings != nil {
		fmt.Printf("Warnings: %v\n", warnings)
	}

	scanResults := make(map[string]interface{})
	var csvData []ScanData

	for _, host := range result.Hosts {
		if len(host.Addresses) == 0 {
			continue
		}

		hostIP := host.Addresses[0].Addr
		macAddress := "Unknown"
		vendorName := "Unknown Vendor"

		// Get MAC and Vendor
		for _, addr := range host.Addresses {
			if addr.AddrType == "mac" {
				macAddress = addr.Addr
				vendorName = addr.Vendor
				break
			}
		}

		// Get OS Name
		osName := "Unknown"
		if len(host.OS.Matches) > 0 {
			osName = host.OS.Matches[0].Name
		}

		hostInfo := map[string]interface{}{
			"hostname":    host.Hostnames,
			"state":       host.Status.State,
			"mac_address": macAddress,
			"vendor":      vendorName,
			"os":          osName,
			"protocols":   make(map[string][]interface{}),
		}

		protocols := make(map[string][]interface{})

		for _, port := range host.Ports {
			appType := getAppCategory(port.ID)

			portInfo := map[string]interface{}{
				"port":             port.ID,
				"service":          port.Service.Name,
				"application_type": appType,
				"product":          port.Service.Product,
				"version":          port.Service.Version,
			}

			proto := string(port.Protocol)
			protocols[proto] = append(protocols[proto], portInfo)

			csvData = append(csvData, ScanData{
				IP:              hostIP,
				MACAddress:      macAddress,
				Vendor:          vendorName,
				OS:              osName,
				Port:            port.ID,
				Protocol:        proto,
				Service:         port.Service.Name,
				ApplicationType: appType,
				Product:         port.Service.Product,
				Version:         port.Service.Version,
			})
		}

		hostInfo["protocols"] = protocols
		scanResults[hostIP] = hostInfo
	}

	// Save JSON
	jsonFile, err := os.Create("scan_results.json")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error creating JSON file: %v\n", err)
		return
	}
	defer jsonFile.Close()

	encoder := json.NewEncoder(jsonFile)
	encoder.SetIndent("", "    ")
	encoder.Encode(scanResults)
	fmt.Println("JSON results saved to: scan_results.json")

	// Save CSV
	csvFile, err := os.Create("DISCOVERY_results.csv")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error creating CSV file: %v\n", err)
		return
	}
	defer csvFile.Close()

	writer := csv.NewWriter(csvFile)
	defer writer.Flush()

	writer.Write([]string{
		"IP", "MAC Address", "Vendor", "OS", "Port", "Protocol",
		"Service", "Application Type", "Product", "Version",
	})

	for _, data := range csvData {
		writer.Write([]string{
			data.IP,
			data.MACAddress,
			data.Vendor,
			data.OS,
			fmt.Sprintf("%d", data.Port),
			data.Protocol,
			data.Service,
			data.ApplicationType,
			data.Product,
			data.Version,
		})
	}

	fmt.Printf("Scan complete. Data for %d hosts saved to: DISCOVERY_results.csv\n", len(result.Hosts))
}

func scanNetworkBasic(networkRange string) {
	fmt.Println("Starting basic network scan (without nmap)...")

	// For basic scanning, we'll scan common ports on the given host
	commonPorts := []uint16{22, 80, 443, 445, 3306, 3389, 5432, 8000, 8080, 554, 1883}

	var csvData []ScanData
	scanResults := make(map[string]interface{})

	// Parse the network range - it could be an IP or IP/CIDR
	hostIP := strings.Split(networkRange, "/")[0]

	fmt.Printf("Scanning host: %s\n", hostIP)

	hostInfo := map[string]interface{}{
		"hostname":    []string{},
		"state":       "up",
		"mac_address": "Unknown",
		"vendor":      "Unknown",
		"os":          "Unknown",
		"open_ports":  []map[string]interface{}{},
	}

	openPorts := []map[string]interface{}{}

	for _, port := range commonPorts {
		address := fmt.Sprintf("%s:%d", hostIP, port)
		// Handle IPv6 addresses
		if strings.Contains(hostIP, ":") && !strings.HasPrefix(hostIP, "[") {
			address = fmt.Sprintf("[%s]:%d", hostIP, port)
		}
		conn, err := net.DialTimeout("tcp", address, 1*time.Second)
		if err == nil {
			conn.Close()
			appType := getAppCategory(port)
			portInfo := map[string]interface{}{
				"port":             port,
				"service":          "",
				"application_type": appType,
			}
			openPorts = append(openPorts, portInfo)

			csvData = append(csvData, ScanData{
				IP:              hostIP,
				MACAddress:      "Unknown",
				Vendor:          "Unknown",
				OS:              "Unknown",
				Port:            port,
				Protocol:        "tcp",
				Service:         "",
				ApplicationType: appType,
				Product:         "Unknown",
				Version:         "Unknown",
			})
			fmt.Printf("  [+] Port %d OPEN (%s)\n", port, appType)
		}
	}

	hostInfo["open_ports"] = openPorts
	scanResults[hostIP] = hostInfo

	// Save results
	jsonFile, err := os.Create("scan_results.json")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error creating JSON file: %v\n", err)
		return
	}
	defer jsonFile.Close()

	encoder := json.NewEncoder(jsonFile)
	encoder.SetIndent("", "    ")
	encoder.Encode(scanResults)
	fmt.Println("JSON results saved to: scan_results.json")

	// Save CSV
	csvFile, err := os.Create("DISCOVERY_results.csv")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error creating CSV file: %v\n", err)
		return
	}
	defer csvFile.Close()

	writer := csv.NewWriter(csvFile)
	defer writer.Flush()

	writer.Write([]string{
		"IP", "MAC Address", "Vendor", "OS", "Port", "Protocol",
		"Service", "Application Type", "Product", "Version",
	})

	for _, data := range csvData {
		writer.Write([]string{
			data.IP,
			data.MACAddress,
			data.Vendor,
			data.OS,
			fmt.Sprintf("%d", data.Port),
			data.Protocol,
			data.Service,
			data.ApplicationType,
			data.Product,
			data.Version,
		})
	}

	fmt.Printf("Basic scan complete. Found %d open ports. Results saved.\n", len(csvData))
}
