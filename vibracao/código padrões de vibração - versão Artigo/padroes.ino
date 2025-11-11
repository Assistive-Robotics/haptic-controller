#include <Arduino.h>

// Estrutura para um passo de vibração, composta pelo atuador (motor)
// e a duração da vibração em milissegundos.
struct PassoVibracao {
  int atuador;  // Qual motor vibrar (índice de 0 a 5). -1 para pausa.
  int duracao;  // Duração em milissegundos
};

// --- Configuração do Hardware ---
// Os atuadores (motores) estão mapeados para os índices de 0 a 5.
const int motorPins[] = { 4, 5, 6, 7, 9, 10}; // Pinos digitais conectados aos drivers dos motores
const int numMotores = 6;                     // Número total de motores

// --- Padrões Fixos ---

// Observação: Os índices dos atuadores (0-5) correspondem à ordem dos pinos acima.
const PassoVibracao padrao1[] = {
  {0, 60}, {-1, 20}, // Atuador 0
  {1, 80}, {-1, 20}, // Atuador 1
  {2, 100}, {-1, 20}, // Atuador 2
  {3, 100}, {-1, 20}, // Atuador 3
  {4, 100}, {-1, 20}, // Atuador 4
  {5, 200}            // Atuador 5
};
const PassoVibracao padrao2[] = {
  {5, 60},
  {4, 80}, {-1, 20},
  {3, 100}, {-1, 20},
  {2, 100}, {-1, 20},
  {1, 100}, {-1, 20},
  {0, 200}, {-1, 20}
};
const PassoVibracao padrao3[] = {
  {0, 270}, {5, 270}, {-1, 150}, {0, 270}, {5, 270}
};
const PassoVibracao padrao4[] = {
  {0, 270}, {5, 270}, {-1, 50}, {1, 270},{4, 270}, {-1, 50},{0, 240},{5, 270}, {-1, 50},{1, 270}, {4, 270}
};
const PassoVibracao padrao5[] = {
  {0, 520}
};
const PassoVibracao padrao6[] = {
  {5, 270},{5, 270}
};

// --- Gerenciamento dos Padrões ---
const PassoVibracao* padroesFixos[] = {padrao1, padrao2, padrao3, padrao4, padrao5, padrao6};
const int tamanhosFixos[] = {
  sizeof(padrao1) / sizeof(padrao1[0]), sizeof(padrao2) / sizeof(padrao2[0]),
  sizeof(padrao3) / sizeof(padrao3[0]), sizeof(padrao4) / sizeof(padrao4[0]),
  sizeof(padrao5) / sizeof(padrao5[0]), sizeof(padrao6) / sizeof(padrao6[0])
};

// Padrões criados dinamicamente (personalizados)
PassoVibracao* padroesPersonalizados[20] = {NULL};
int tamanhosPersonalizados[20] = {0};
int qtdPadroesPersonalizados = 0;

// --- Funções de Controle ---

// Toca um único passo de vibração (liga, espera, desliga)
void tocarPasso(PassoVibracao passo) {
  if (passo.atuador >= 0 && passo.atuador < numMotores) {
    digitalWrite(motorPins[passo.atuador], HIGH); // Liga o motor
  }
  delay(passo.duracao); // Espera o tempo de vibração/pausa
  if (passo.atuador >= 0 && passo.atuador < numMotores) {
    digitalWrite(motorPins[passo.atuador], LOW);  // Desliga o motor
  }
}

// Toca uma sequência inteira de passos
void tocarPadrao(const PassoVibracao padrao[], int tamanho) {
  for (int i = 0; i < tamanho; i++) {
    tocarPasso(padrao[i]);
  }
}

// --- Funções Principais do Arduino ---
void setup() {
  // Configura todos os pinos dos motores como saída e os desliga
  for (int i = 0; i < numMotores; i++) {
    pinMode(motorPins[i], OUTPUT);
    digitalWrite(motorPins[i], LOW);
  }
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();
    
    Serial.println("Recebi o comando: " + comando); 

    // Comando para CRIAR um novo padrão (prefixo '@')
    if (comando.startsWith("@")) {
      if (qtdPadroesPersonalizados < 20) {
        String dados = comando.substring(1);
        int valores[100]; 
        int n = 0; // Contador de valores lidos

        // Parseia a string "atuador,duracao,atuador,duracao,..."
        while (dados.length() > 0 && n < 100) {
          int idx = dados.indexOf(',');
          if (idx == -1) idx = dados.length();
          valores[n++] = dados.substring(0, idx).toInt();
          dados = (idx + 1 >= dados.length()) ? "" : dados.substring(idx + 1);
        }
        
        int numPassos = n / 2; // Cada passo tem 2 valores (atuador e duração)
        
        // Aloca memória para o novo padrão personalizado
        padroesPersonalizados[qtdPadroesPersonalizados] = new PassoVibracao[numPassos];
        
        // Preenche a estrutura PassoVibracao
        for (int i = 0; i < numPassos; i++) {
          padroesPersonalizados[qtdPadroesPersonalizados][i].atuador = valores[i * 2];
          padroesPersonalizados[qtdPadroesPersonalizados][i].duracao = valores[i * 2 + 1];
        }
        
        tamanhosPersonalizados[qtdPadroesPersonalizados] = numPassos;
        qtdPadroesPersonalizados++;
        Serial.println("Novo padrao personalizado criado.");
      }
    } 
    // Comando para EXCLUIR um padrão (prefixo '#')
    else if (comando.startsWith("#")) {
      // O primeiro padrão personalizado é o 7, então subtraímos 7 da ID do comando
      int idComando = comando.substring(1).toInt();
      int idx = idComando - 7; 
      
      if (idx >= 0 && idx < qtdPadroesPersonalizados && padroesPersonalizados[idx] != NULL) {
        delete[] padroesPersonalizados[idx]; // Libera a memória alocada
        padroesPersonalizados[idx] = NULL;
        Serial.println("Padrao " + String(idComando) + " excluido.");
      }
    } 
    // Comando para TOCAR um padrão (número inteiro)
    else {
      int idx = comando.toInt();
      
      // Toca padrões fixos (1 a 6)
      if (idx >= 1 && idx <= 6) {
        Serial.println("Tocando padrao fixo " + String(idx));
        tocarPadrao(padroesFixos[idx - 1], tamanhosFixos[idx - 1]);
      } 
      // Toca padrões personalizados (a partir do 7)
      else if (idx > 6) {
        int i = idx - 7;
        if (i < qtdPadroesPersonalizados && padroesPersonalizados[i] != NULL) {
          Serial.println("Tocando padrao personalizado " + String(idx));
          tocarPadrao(padroesPersonalizados[i], tamanhosPersonalizados[i]);
        }
      }
    }
  }
}
