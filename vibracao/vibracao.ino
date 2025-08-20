#include <Arduino.h>

const int motorPin = 9;

const int padrao1[] = {50, 150, 50, 700, 50, 150, 50, 1000};
const int padrao2[] = {125, 75, 125, 275, 200, 275, 125, 75};
const int padrao3[] = {0, 50, 100, 50, 100, 50, 100, 50};
const int padrao4[] = {0, 500, 250, 500, 250, 500};
const int padrao5[] = {0, 1000, 0, 2000, 0, 100, 300, 590};

const int* padroesFixos[] = {padrao1, padrao2, padrao3, padrao4, padrao5};
const int tamanhosFixos[] = {
  sizeof(padrao1)/sizeof(padrao1[0]),
  sizeof(padrao2)/sizeof(padrao2[0]),
  sizeof(padrao3)/sizeof(padrao3[0]),
  sizeof(padrao4)/sizeof(padrao4[0]),
  sizeof(padrao5)/sizeof(padrao5[0])
};

int* padroes[20] = {nullptr};  // Máximo 20 padrões personalizados
int tamanhos[20] = {0}; //tam de cada padrao
int qtdPadroes = 0; //qtd de padroes personalizados

void vibracao(int duracao) {
  digitalWrite(motorPin, HIGH);
  delay(duracao);
  digitalWrite(motorPin, LOW);
  delay(100);
}

void tocarPadrao(const int padrao[], int tamanho) {
  for (int i = 0; i < tamanho; i++) {
    vibracao(padrao[i]);
  }
}

void setup() {
  pinMode(motorPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');

    // Adicionar novo padrão
    if (comando.startsWith("@")) {
      if (qtdPadroes < 20) {
        String dados = comando.substring(1);//remove o @
        int valores[50]; //vetor para armazenar os numeros convertidos
        int n = 0; //contador de quantos numeros foram convertidos

        while (dados.length() > 0 && n < 50) {
          int idx = dados.indexOf(','); //procurando a posicao  da  prox virgula 
          if (idx == -1) idx = dados.length();//se nao tem mais nada, converte pra int
          valores[n++] = dados.substring(0, idx).toInt();
          dados = dados.substring(idx + 1); //remove o numero ja processado da string
        }

        padroes[qtdPadroes] = new int[n]; //aloca vetor dinamico
        for (int i = 0; i < n; i++) {
          padroes[qtdPadroes][i] = valores[i]; //copia os valores do vetor temp para o novo vetor, padroes[i] é um ponteiro pro vetor
        }
        tamanhos[qtdPadroes] = n; //pega o tamanho do vetor atual
        qtdPadroes++; //incrementa mais 1 na quantidade total de padroes criados
      }
    }

    // Excluir padrão personalizado
    else if (comando.startsWith("#")) {
      int idx = comando.substring(1).toInt() - 6;
      if (idx >= 0 && idx < qtdPadroes && padroes[idx]) {
        delete[] padroes[idx];
        padroes[idx] = nullptr;
        tamanhos[idx] = 0;
      }
    }

    // Tocar padrão
    else {
      int idx = comando.toInt();
      if (idx >= 1 && idx <= 5) {
        tocarPadrao(padroesFixos[idx - 1], tamanhosFixos[idx - 1]);
      } else if (idx >= 6 && idx <= qtdPadroes + 5) {
        int i = idx - 6;
        if (padroes[i]) {
          tocarPadrao(padroes[i], tamanhos[i]);
        }
      }
    }
  }
}
