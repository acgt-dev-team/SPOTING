package main

import (
	"crypto/ecdsa"
	"crypto/ed25519"
	"crypto/rsa"
	"crypto/sha1"
	"crypto/sha256"
	"crypto/x509"
	"encoding/csv"
	"encoding/hex"
	"encoding/pem"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

func runBinariesDisk(args []string) {
	file, err := os.Create("binaries_at_disk.csv")
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
	binaries := listBinaries()

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

	fmt.Println("Output: binaries_at_disk.csv")
}

func runLibraries(args []string) {
	file, err := os.Create("library.csv")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error creating CSV: %v\n", err)
		return
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	writer.Write([]string{
		"library",
		"os_type",
		"library_type",
		"crypto_dependency",
		"algorithm",
		"primitive",
		"key_size",
		"detection_method",
	})

	osType := detectOS()
	libraries := findLibraries()

	for _, lib := range libraries {
		fmt.Println(lib)

		libType := "shared"
		lowerLib := strings.ToLower(lib)
		if strings.HasSuffix(lowerLib, ".a") {
			libType = "static"
		} else if strings.HasSuffix(lowerLib, ".la") {
			libType = "libtool"
		} else if strings.HasSuffix(lowerLib, ".lib") {
			libType = "import-lib"
		}

		cryptoDeps := getCryptoDeps(lib)
		cryptoHits := detectCrypto(lib)

		if len(cryptoHits) == 0 {
			detectionMethod := "static-string"
			if cryptoDeps != "none" {
				detectionMethod = "dependency-only"
			}
			writer.Write([]string{
				lib,
				osType,
				libType,
				cryptoDeps,
				"none",
				"none",
				"unknown",
				detectionMethod,
			})
			continue
		}

		for _, hit := range cryptoHits {
			keySize := "unknown"
			if kl, ok := hit.Parameters["keyLength"]; ok {
				keySize = fmt.Sprintf("%v", kl)
			}

			writer.Write([]string{
				lib,
				osType,
				libType,
				cryptoDeps,
				hit.Algorithm,
				hit.Primitive,
				keySize,
				strings.Join(hit.DetectionSource, ","),
			})
		}
	}

	fmt.Println("Output: library.csv")
}

func runKernelModules(args []string) {
	fmt.Println("Scanning kernel modules...")
	fmt.Println("Output: kernel_modules.csv")
}

func runCertKeys(args []string) {
	scanRoot := "."
	if len(args) > 0 {
		scanRoot = args[0]
	}

	fmt.Printf("[i] Scanning root: %s\n", scanRoot)

	file, err := os.Create("crypto_cert_key.csv")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error creating CSV: %v\n", err)
		return
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	writer.Write([]string{
		"path",
		"file_type",
		"algorithm",
		"key_size",
		"curve",
		"rsa_modulus_fingerprint",
		"rsa_exponent",
		"signature_algorithm",
		"signature_hash",
		"subject",
		"issuer",
		"serial",
		"not_before",
		"not_after",
		"fingerprint_sha1",
		"fingerprint_sha256",
	})

	scanExtensions := []string{
		".crt", ".cer", ".pem", ".der",
		".key", ".pk8",
		".p12", ".pfx",
	}

	filepath.Walk(scanRoot, func(path string, info os.FileInfo, err error) error {
		if err != nil || info.IsDir() {
			return nil
		}

		// Check if file has cert/key extension
		lowerName := strings.ToLower(info.Name())
		isCandidate := false
		for _, ext := range scanExtensions {
			if strings.HasSuffix(lowerName, ext) {
				isCandidate = true
				break
			}
		}

		if !isCandidate {
			return nil
		}

		fmt.Println(path)
		result := analyzeCertFile(path)

		if result != nil {
			writer.Write([]string{
				path,
				result.Type,
				result.Algorithm,
				fmt.Sprintf("%d", result.KeySize),
				result.Curve,
				result.RSAModulusFP,
				result.RSAExponent,
				result.SignatureAlgorithm,
				result.SignatureHash,
				result.Subject,
				result.Issuer,
				result.Serial,
				result.NotBefore,
				result.NotAfter,
				result.FingerprintSHA1,
				result.FingerprintSHA256,
			})
		}

		return nil
	})

	fmt.Println("Output: crypto_cert_key.csv")
}

func runExecScripts(args []string) {
	file, err := os.Create("exec_codes.csv")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error creating CSV: %v\n", err)
		return
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	writer.Write([]string{
		"file_path",
		"script_type",
		"crypto_pattern",
		"algorithm",
	})

	writer.Flush()
	fmt.Println("Output: exec_codes.csv")
}

func runWebApps(args []string) {
	scanRoot := "."
	if len(args) > 0 {
		scanRoot = args[0]
	}

	file, err := os.Create("web_app.csv")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error creating CSV: %v\n", err)
		return
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	writer.Write([]string{
		"file_path",
		"file_type",
		"crypto_library",
		"algorithm",
	})

	filepath.Walk(scanRoot, func(path string, info os.FileInfo, err error) error {
		if err != nil || info.IsDir() {
			return nil
		}

		lowerName := strings.ToLower(info.Name())
		if !strings.HasSuffix(lowerName, ".js") &&
			!strings.HasSuffix(lowerName, ".py") &&
			!strings.HasSuffix(lowerName, ".php") &&
			!strings.HasSuffix(lowerName, ".ts") {
			return nil
		}

		fmt.Println(path)
		return nil
	})

	writer.Flush()
	fmt.Println("Output: web_app.csv")
}

func runNetworkApps(args []string) {
	file, err := os.Create("network_app.csv")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error creating CSV: %v\n", err)
		return
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	writer.Write([]string{
		"application",
		"port",
		"protocol",
		"ssl_version",
	})

	writer.Flush()
	fmt.Println("Output: network_app.csv")
}

func runNetworkProtocol(args []string) {
	if len(args) == 0 {
		fmt.Println("Usage: cbom-agent network-protocol <domain>")
		return
	}

	domain := args[0]
	fmt.Printf("Scanning SSL/TLS protocols for %s...\n", domain)
	fmt.Println("Output: ssl_results.json")
}

func runDiscovery(args []string) {
	if len(args) == 0 {
		fmt.Println("Usage: cbom-agent discovery <network_range>")
		fmt.Println("Example: cbom-agent discovery 192.168.1.0/24")
		return
	}

	networkRange := args[0]
	scanNetworkNmap(networkRange)
}

func runReadCert(args []string) {
	if len(args) == 0 {
		fmt.Println("Usage: cbom-agent read-cert <certificate_file>")
		return
	}

	certPath := args[0]
	fmt.Printf("Reading certificate: %s\n", certPath)
	fmt.Printf("Certificate details would be displayed here\n")
}

// CertInfo holds parsed certificate/key information
type CertInfo struct {
	Type               string
	Algorithm          string
	KeySize            int
	Curve              string
	RSAModulusFP       string
	RSAExponent        string
	SignatureAlgorithm string
	SignatureHash      string
	Subject            string
	Issuer             string
	Serial             string
	NotBefore          string
	NotAfter           string
	FingerprintSHA1    string
	FingerprintSHA256  string
}

func analyzeCertFile(path string) *CertInfo {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil
	}

	dataStr := string(data)

	if strings.Contains(dataStr, "BEGIN CERTIFICATE") {
		info, err := scanCertificate(data)
		if err == nil {
			return info
		}
	}

	if strings.Contains(dataStr, "BEGIN PRIVATE KEY") ||
		strings.Contains(dataStr, "BEGIN RSA PRIVATE KEY") ||
		strings.Contains(dataStr, "BEGIN EC PRIVATE KEY") {
		info, err := scanPrivateKey(data)
		if err == nil {
			return info
		}
	}

	return nil
}

func scanCertificate(data []byte) (*CertInfo, error) {
	block, _ := pem.Decode(data)
	if block == nil {
		return nil, fmt.Errorf("failed to decode PEM")
	}

	cert, err := x509.ParseCertificate(block.Bytes)
	if err != nil {
		return nil, err
	}

	info := &CertInfo{
		Type:               "certificate",
		Subject:            cert.Subject.String(),
		Issuer:             cert.Issuer.String(),
		Serial:             fmt.Sprintf("%x", cert.SerialNumber),
		NotBefore:          cert.NotBefore.UTC().Format("2006-01-02T15:04:05Z"),
		NotAfter:           cert.NotAfter.UTC().Format("2006-01-02T15:04:05Z"),
		SignatureAlgorithm: cert.SignatureAlgorithm.String(),
	}

	// Calculate fingerprints
	sha1Hash := sha1.Sum(cert.Raw)
	sha256Hash := sha256.Sum256(cert.Raw)
	info.FingerprintSHA1 = hex.EncodeToString(sha1Hash[:])
	info.FingerprintSHA256 = hex.EncodeToString(sha256Hash[:])

	// Get public key info
	switch pubKey := cert.PublicKey.(type) {
	case *rsa.PublicKey:
		info.Algorithm = "RSAPublicKey"
		info.KeySize = pubKey.N.BitLen()
		modBytes := pubKey.N.Bytes()
		modHash := sha256.Sum256(modBytes)
		info.RSAModulusFP = hex.EncodeToString(modHash[:])[:32]
		info.RSAExponent = fmt.Sprintf("%d", pubKey.E)
	case *ecdsa.PublicKey:
		info.Algorithm = "EllipticCurvePublicKey"
		info.KeySize = pubKey.Params().BitSize
		info.Curve = pubKey.Params().Name
	case ed25519.PublicKey:
		info.Algorithm = "Ed25519PublicKey"
		info.KeySize = 256
	default:
		info.Algorithm = "UnknownPublicKey"
	}

	return info, nil
}

func scanPrivateKey(data []byte) (*CertInfo, error) {
	block, _ := pem.Decode(data)
	if block == nil {
		return nil, fmt.Errorf("failed to decode PEM")
	}

	info := &CertInfo{
		Type:              "private_key",
		FingerprintSHA1:   shortFingerprint(data),
		FingerprintSHA256: fmt.Sprintf("%x", sha256.Sum256(data)),
	}

	// Try to parse as PKCS8
	key, err := x509.ParsePKCS8PrivateKey(block.Bytes)
	if err != nil {
		// Try RSA
		rsaKey, err := x509.ParsePKCS1PrivateKey(block.Bytes)
		if err == nil {
			info.Algorithm = "RSAPrivateKey"
			info.KeySize = rsaKey.N.BitLen()
			modBytes := rsaKey.N.Bytes()
			modHash := sha256.Sum256(modBytes)
			info.RSAModulusFP = hex.EncodeToString(modHash[:])[:32]
			info.RSAExponent = fmt.Sprintf("%d", rsaKey.E)
			return info, nil
		}

		// Try EC
		ecKey, err := x509.ParseECPrivateKey(block.Bytes)
		if err == nil {
			info.Algorithm = "EllipticCurvePrivateKey"
			info.KeySize = ecKey.Params().BitSize
			info.Curve = ecKey.Params().Name
			return info, nil
		}

		return nil, fmt.Errorf("failed to parse private key")
	}

	// Handle PKCS8 parsed key
	switch privKey := key.(type) {
	case *rsa.PrivateKey:
		info.Algorithm = "RSAPrivateKey"
		info.KeySize = privKey.N.BitLen()
		modBytes := privKey.N.Bytes()
		modHash := sha256.Sum256(modBytes)
		info.RSAModulusFP = hex.EncodeToString(modHash[:])[:32]
		info.RSAExponent = fmt.Sprintf("%d", privKey.E)
	case *ecdsa.PrivateKey:
		info.Algorithm = "EllipticCurvePrivateKey"
		info.KeySize = privKey.Params().BitSize
		info.Curve = privKey.Params().Name
	case ed25519.PrivateKey:
		info.Algorithm = "Ed25519PrivateKey"
		info.KeySize = 256
	default:
		info.Algorithm = "UnknownPrivateKey"
	}

	return info, nil
}

func shortFingerprint(data []byte) string {
	hash := sha256.Sum256(data)
	return hex.EncodeToString(hash[:])[:32]
}
