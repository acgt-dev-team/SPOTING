package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

const version = "1.0.0"

func printUsage() {
	fmt.Println("CBOM Scanner Agent v" + version)
	fmt.Println("\nUsage: cbom-agent <command> [options]")
	fmt.Println("\nCommands:")
	fmt.Println("  binaries-used      Scan running binaries for crypto usage")
	fmt.Println("  binaries-disk      Scan disk binaries for crypto libraries")
	fmt.Println("  libraries          Analyze system libraries for crypto")
	fmt.Println("  kernel-modules     Scan Linux kernel modules (Linux only)")
	fmt.Println("  cert-keys          Analyze certificates and private keys")
	fmt.Println("  exec-scripts       Scan executable scripts for crypto")
	fmt.Println("  web-apps           Scan web application files")
	fmt.Println("  network-apps       Analyze network applications")
	fmt.Println("  network-protocol   SSL/TLS protocol scanner")
	fmt.Println("  discovery          Network discovery with nmap")
	fmt.Println("  read-cert          Read and analyze a certificate/key file")
	fmt.Println("  all                Run all applicable scans")
	fmt.Println("  version            Show version information")
	fmt.Println("  help               Show this help message")
	fmt.Println("\nExamples:")
	fmt.Println("  cbom-agent binaries-used")
	fmt.Println("  cbom-agent cert-keys /etc/ssl")
	fmt.Println("  cbom-agent read-cert certificate.pem")
	fmt.Println("  cbom-agent all")
}

func main() {
	// Check if running interactively (double-clicked)
	if len(os.Args) < 2 {

	startServer()

	return
}

	command := os.Args[1]
	args := os.Args[2:]

	switch command {
	case "binaries-used":
		runBinariesUsed(args)
	case "binaries-disk":
		runBinariesDisk(args)
	case "libraries":
		runLibraries(args)
	case "kernel-modules":
		runKernelModules(args)
	case "cert-keys":
		runCertKeys(args)
	case "exec-scripts":
		runExecScripts(args)
	case "web-apps":
		runWebApps(args)
	case "network-apps":
		runNetworkApps(args)
	case "network-protocol":
		runNetworkProtocol(args)
	case "discovery":
		runDiscovery(args)
	case "read-cert":
		runReadCert(args)
	case "all":
		runAllScans(args)
	case "version":
		fmt.Println("CBOM Scanner Agent v" + version)
	case "help", "--help", "-h":
		printUsage()
	default:
		fmt.Fprintf(os.Stderr, "Unknown command: %s\n\n", command)
		printUsage()
		os.Exit(1)
	}
}

func runAllScans(args []string) {
	fmt.Println("=== Running All CBOM Scans ===")
	fmt.Println()
	fmt.Println("[1/9] Scanning running binaries...")
	runBinariesUsed([]string{})

	fmt.Println("\n[2/9] Scanning disk binaries...")
	runBinariesDisk([]string{})

	fmt.Println("\n[3/9] Scanning libraries...")
	runLibraries([]string{})

	fmt.Println("\n[4/9] Scanning kernel modules...")
	runKernelModules([]string{})

	fmt.Println("\n[5/9] Scanning certificates and keys...")
	runCertKeys([]string{})

	fmt.Println("\n[6/9] Scanning executable scripts...")
	runExecScripts([]string{})

	fmt.Println("\n[7/9] Scanning web applications...")
	runWebApps([]string{})

	fmt.Println("\n[8/9] Scanning network applications...")
	runNetworkApps([]string{})

	fmt.Println("\n[9/9] Network discovery...")
	// Only run if network range is provided
	if len(args) > 0 {
		runDiscovery(args)
	} else {
		fmt.Println("  Skipped: Network discovery requires network range argument")
	}

	fmt.Println("\n=== All Scans Complete ===")
}

func runInteractiveMode() {
	reader := bufio.NewReader(os.Stdin)

	for {
		fmt.Println("\n" + strings.Repeat("=", 60))
		fmt.Println("CBOM Scanner Agent v" + version + " - Interactive Mode")
		fmt.Println(strings.Repeat("=", 60))
		fmt.Println("\nAvailable Commands:")
		fmt.Println("  1.  binaries-used      - Scan running binaries")
		fmt.Println("  2.  binaries-disk      - Scan disk binaries")
		fmt.Println("  3.  libraries          - Analyze system libraries")
		fmt.Println("  4.  kernel-modules     - Scan kernel modules (Linux)")
		fmt.Println("  5.  cert-keys          - Analyze certificates/keys")
		fmt.Println("  6.  exec-scripts       - Scan executable scripts")
		fmt.Println("  7.  web-apps           - Scan web applications")
		fmt.Println("  8.  network-apps       - Analyze network apps")
		fmt.Println("  9.  network-protocol   - SSL/TLS scanner")
		fmt.Println("  10. discovery          - Network discovery")
		fmt.Println("  11. read-cert          - Read certificate file")
		fmt.Println("  12. all                - Run all scans")
		fmt.Println("  0.  exit               - Exit program")
		fmt.Println("\nEnter command number or name (or type 'help' for more info):")
		fmt.Print("> ")

		input, err := reader.ReadString('\n')
		if err != nil {
			fmt.Println("Error reading input:", err)
			continue
		}

		input = strings.TrimSpace(input)
		if input == "" {
			continue
		}

		// Handle exit
		if input == "0" || input == "exit" || input == "quit" || input == "q" {
			fmt.Println("\nExiting CBOM Scanner Agent. Goodbye!")
			break
		}

		// Handle help
		if input == "help" || input == "-h" || input == "--help" {
			printUsage()
			fmt.Println("\nPress Enter to continue...")
			reader.ReadString('\n')
			continue
		}

		// Map numbers to commands
		var command string
		switch input {
		case "1":
			command = "binaries-used"
		case "2":
			command = "binaries-disk"
		case "3":
			command = "libraries"
		case "4":
			command = "kernel-modules"
		case "5":
			command = "cert-keys"
		case "6":
			command = "exec-scripts"
		case "7":
			command = "web-apps"
		case "8":
			command = "network-apps"
		case "9":
			command = "network-protocol"
		case "10":
			command = "discovery"
		case "11":
			command = "read-cert"
		case "12":
			command = "all"
		default:
			command = input
		}

		// Execute command
		fmt.Println("\n" + strings.Repeat("-", 60))
		fmt.Printf("Running: %s\n", command)
		fmt.Println(strings.Repeat("-", 60))

		switch command {
		case "binaries-used":
			runBinariesUsed([]string{})
		case "binaries-disk":
			runBinariesDisk([]string{})
		case "libraries":
			runLibraries([]string{})
		case "kernel-modules":
			runKernelModules([]string{})
		case "cert-keys":
			fmt.Print("Enter path to scan (or press Enter for current directory): ")
			path, _ := reader.ReadString('\n')
			path = strings.TrimSpace(path)
			if path == "" {
				path = "."
			}
			runCertKeys([]string{path})
		case "exec-scripts":
			runExecScripts([]string{})
		case "web-apps":
			fmt.Print("Enter path to scan (or press Enter for current directory): ")
			path, _ := reader.ReadString('\n')
			path = strings.TrimSpace(path)
			if path == "" {
				path = "."
			}
			runWebApps([]string{path})
		case "network-apps":
			runNetworkApps([]string{})
		case "network-protocol":
			fmt.Print("Enter domain to scan (e.g., example.com): ")
			domain, _ := reader.ReadString('\n')
			domain = strings.TrimSpace(domain)
			if domain != "" {
				runNetworkProtocol([]string{domain})
			} else {
				fmt.Println("Error: Domain required")
			}
		case "discovery":
			fmt.Print("Enter network range (e.g., 192.168.1.0/24): ")
			network, _ := reader.ReadString('\n')
			network = strings.TrimSpace(network)
			if network != "" {
				runDiscovery([]string{network})
			} else {
				fmt.Println("Error: Network range required")
			}
		case "read-cert":
			fmt.Print("Enter certificate file path: ")
			certPath, _ := reader.ReadString('\n')
			certPath = strings.TrimSpace(certPath)
			if certPath != "" {
				runReadCert([]string{certPath})
			} else {
				fmt.Println("Error: Certificate file path required")
			}
		case "all":
			runAllScans([]string{})
		default:
			fmt.Printf("Unknown command: %s\n", command)
			fmt.Println("Type 'help' to see available commands")
		}

		fmt.Println("\n" + strings.Repeat("-", 60))
		fmt.Println("Press Enter to continue...")
		reader.ReadString('\n')
	}
}
