## Nivel de possiveis combinacoes.
* Classe A = Minusculo
* Classe B = Numerico.
* Classe C = Maiusculo, Minusculo e Numero.

## Tamanho e Unidade das frases.
* Tamanho = Se nao for fornecido o tamanho da frase, logo sera 20 caracteres.
* Unidades = Se nao for fornecido a unidade da frase, logo sera 1 combinacao.

## Como usar, exemplo:
```
import Raney

Password = Raney.criar(0, classe="C")
print(" Sua senha: " + Password)
```
``` Sua senha: vPgZYy7g4MNFiuyhb2m3 ```

## Segundo exemplo:
```
import Raney

Password = Raney.criar(0, classe="C", tamanho=40, unidades=1)
print(" Sua senha: " + Password)
```
``` Seu senha: vPgZYy7g4MNFiuyhb2m3VuEHPqbedzIidW5QoXPc ```

## Terceiro exemplo:
```
import Raney

Password = Raney.criar(0, classe="B", tamanho=40, unidades=1)
print(" Sua senha: " + Password)
```
``` Seu senha: 7953534152702352984373528086301837196322 ```

# Saiba mais:
* Discord: https://discord.gg/CHsnjZB3Ec