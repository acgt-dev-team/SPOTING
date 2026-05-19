package main

import (
	"encoding/json"
	"net/http"
)

type ScanResponse struct {
	Message      string                   `json:"message"`
	HasilImbasan []map[string]interface{} `json:"hasil_imbasan"`
}

func imbasHandler(w http.ResponseWriter, r *http.Request) {

	result := []map[string]interface{}{
		{
			"cbom_data": map[string]interface{}{
				"path":      "C:/test.pem",
				"file_type": "certificate",
				"algorithm": "RSA",
				"key_size":  "2048",
				"issuer":    "Test CA",
				"subject":   "localhost",
			},
		},
	}

	response := ScanResponse{
		Message:      "Imbasan berjaya",
		HasilImbasan: result,
	}

	w.Header().Set("Content-Type", "application/json")

	json.NewEncoder(w).Encode(response)
}

func startServer() {

	http.HandleFunc("/imbas", imbasHandler)

	println("Agent running on :9001")

	http.ListenAndServe(":9001", nil)
}