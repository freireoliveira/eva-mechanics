# Evolutionary Vector Architecture

Tendo em mente todo o repertório da mecânica evolutiva desenvolvido desde Darwin, EVA tenta modelar, a cada rodada, ramificações por fissão binária de organismos simples sujeitos a mutações, seleção e deriva gênica.

Cada rodada é, estatisticamente, única, posto que a composição da sequência inicial é determinada estocasticamente, bem como as forças evolutivas atuantes.

A seleção no estilo 'hard selection' define, a cada geração, uma subsequência deletéria, em que todos os organismos que a possuem são eliminados da árvore da vida.

Novos eventos ainda devem ser implementados.

Requisitos
------------
### Python
Python 3.x

### Pacotes
−　Numpy: http://www.numpy.org/<br>
−　ETE Toolkit: http://etetoolkit.org/<br>

Uso
-----

### Exemplos

```shell
$ python3 run.py --gentime 2
```

```shell
$ python3 run.py -g 6
```

**gentime* refere-se ao tempo de geração, isto é, o tempo para a fissão binária de todos os indivíduos da geração atual acontecer. Por padrão, *gentime* é de 4 segundos.
