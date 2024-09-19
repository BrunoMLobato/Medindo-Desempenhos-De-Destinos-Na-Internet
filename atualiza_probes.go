//a funcionalidade desse código é atualizar, organizar e formatar os dados das "probes" com informações sobre países, continente, hops, destino e RTT.

package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math"
	"math/rand"
	"net/http"
	"os"
	"sync"
	"time"
)

// Estrutura para armazenar dados de cada entrada JSON
type ProbeEntry struct {
	PrbID       int     `json:"prb_id"`
	Timestamp   int64   `json:"timestamp"`
	Hops        int     `json:"hops"`
	Destination string  `json:"destination"`
	Country     string  `json:"country,omitempty"`
	Continent   string  `json:"continent,omitempty"`
	RTTDestino  float64 `json:"rtt_destino,omitempty"`
}

// Estrutura da entrada do JSON original
type OriginalData struct {
	PrbID     int   `json:"prb_id"`
	Timestamp int64 `json:"timestamp"`
	Result    []struct {
		Hop    int `json:"hop"`
		Result []struct {
			RTT float64 `json:"rtt,omitempty"`
		} `json:"result"`
	} `json:"result"`
	DstName string `json:"dst_name"`
}

// Estrutura para resposta da API do Atlas
type ProbeAPIResponse struct {
	CountryCode   string `json:"country_code"`
	ContinentCode string `json:"continent_code"`
}

// Mapa para associar países a continentes
var countryToContinent = map[string]string{
	"BR": "América do Sul",   // Brasil
	"AR": "América do Sul",   // Argentina
	"CL": "América do Sul",   // Chile
	"CA": "América do Norte", // Canadá
	"US": "América do Norte", // Estados Unidos
	"MX": "América do Norte", // México
	"PT": "Europa",           // Portugal
	"ES": "Europa",           // Espanha
	"GB": "Europa",           // Inglaterra (Reino Unido)
}

// Função que busca o país e continente da probe com retry e backoff exponencial
func getProbeLocation(prbID int) (string, string, error) {
	url := fmt.Sprintf("https://atlas.ripe.net/api/v2/probes/%d/", prbID)

	// Número máximo de tentativas
	maxRetries := 5

	for attempt := 0; attempt < maxRetries; attempt++ {
		resp, err := http.Get(url)
		if err != nil {
			return "Unknown", "Unknown", err
		}
		defer resp.Body.Close()

		// Verifica o status da resposta
		if resp.StatusCode == http.StatusOK {
			var apiResponse ProbeAPIResponse
			if err := json.NewDecoder(resp.Body).Decode(&apiResponse); err != nil {
				return "Unknown", "Unknown", err
			}

			country := apiResponse.CountryCode
			if country == "" {
				country = "Unknown"
			}

			continent, exists := countryToContinent[country]
			if !exists {
				continent = "Unknown"
			}

			return country, continent, nil
		} else if resp.StatusCode == 429 {
			// Implementa backoff exponencial para erro 429
			sleepDuration := time.Duration(math.Pow(2, float64(attempt))) * time.Second
			jitter := time.Duration(rand.Intn(1000)) * time.Millisecond // Jitter para evitar requisições ao mesmo tempo
			time.Sleep(sleepDuration + jitter)
			fmt.Printf("Tentativa %d falhou com status 429. Esperando %v antes de tentar novamente.\n", attempt+1, sleepDuration+jitter)
		} else {
			return "Unknown", "Unknown", fmt.Errorf("erro ao buscar a probe %d: status %d", prbID, resp.StatusCode)
		}
	}
	return "Unknown", "Unknown", fmt.Errorf("excedido número máximo de tentativas para a probe %d", prbID)
}

// Função que calcula o RTT médio do último hop
func calculateRTT(results []struct {
	Hop    int `json:"hop"`
	Result []struct {
		RTT float64 `json:"rtt,omitempty"`
	} `json:"result"`
}) float64 {
	if len(results) == 0 {
		return 0.0
	}

	// Pegar o último hop
	lastHopResults := results[len(results)-1].Result
	if len(lastHopResults) == 0 {
		return 0.0
	}

	// Soma os valores de RTT do último hop
	totalRTT := 0.0
	count := 0
	for _, r := range lastHopResults {
		if r.RTT > 0 {
			totalRTT += r.RTT
			count++
		}
	}

	if count == 0 {
		return 0.0
	}

	return totalRTT / float64(count)
}

// Função que atualiza o JSON com as localizações, hops, rtt e destino, usando goroutines e WaitGroup para controle de concorrência
func updateJSONWithLocation(entries []OriginalData) []ProbeEntry {
	var wg sync.WaitGroup
	mutex := &sync.Mutex{}

	// Slice para armazenar os resultados atualizados
	updatedEntries := make([]ProbeEntry, len(entries))

	for i := range entries {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()

			// Calcular o número de hops
			hops := len(entries[i].Result)

			// Extrair o destino
			destination := entries[i].DstName
			if destination == "" {
				destination = "Unknown"
			}

			// Calcular o RTT médio do último hop
			rttDestino := calculateRTT(entries[i].Result)

			// Obter país e continente com base no prb_id
			country, continent, err := getProbeLocation(entries[i].PrbID)
			if err != nil {
				fmt.Printf("Erro ao buscar a probe %d: %v\n", entries[i].PrbID, err)
			}

			// Atualizar a entrada
			mutex.Lock()
			updatedEntries[i] = ProbeEntry{
				PrbID:       entries[i].PrbID,
				Timestamp:   entries[i].Timestamp,
				Hops:        hops,
				Destination: destination,
				Country:     country,
				Continent:   continent,
				RTTDestino:  rttDestino,
			}
			mutex.Unlock()
		}(i)
	}
	wg.Wait()

	return updatedEntries
}

func main() {
	// Carregar o arquivo JSON
	file, err := os.Open("twitch.json")
	if err != nil {
		fmt.Printf("Erro ao abrir o arquivo: %v\n", err)
		return
	}
	defer file.Close()

	byteValue, _ := ioutil.ReadAll(file)

	// Analisar o JSON de entrada
	var entries []OriginalData
	if err := json.Unmarshal(byteValue, &entries); err != nil {
		fmt.Printf("Erro ao decodificar JSON: %v\n", err)
		return
	}

	// Atualizar o JSON com país, continente, hops, destino e RTT
	updatedEntries := updateJSONWithLocation(entries)

	// Salvar o JSON atualizado
	updatedData, err := json.MarshalIndent(updatedEntries, "", "  ")
	if err != nil {
		fmt.Printf("Erro ao converter para JSON: %v\n", err)
		return
	}

	err = ioutil.WriteFile("twitch_probes.json", updatedData, 0644)
	if err != nil {
		fmt.Printf("Erro ao salvar o arquivo atualizado: %v\n", err)
		return
	}

	fmt.Println("Arquivo JSON atualizado com sucesso!")
}
