# Esercizio 4 – Ordinamento e Interfaccia Comparable / Sorting and Comparable Interface

---

## 🇮🇹 Italiano

### Descrizione
Questo esercizio mostra come implementare l'ordinamento personalizzato di oggetti utilizzando l'interfaccia standard di Java `Comparable`.

Il programma:
- Definisce la classe `Pellicola` (Film) che implementa `Comparable<Pellicola>`.
- Sovrascrive il metodo `compareTo()` per stabilire un criterio di ordinamento naturale (in questo caso, basato sull'anno di uscita).
- Utilizza `Collections.sort()` per ordinare una lista di oggetti `Pellicola`.
- Stampa la lista prima e dopo l'ordinamento.

### Obiettivo didattico
- Imparare a utilizzare le interfacce di sistema di Java.
- Comprendere la logica del metodo `compareTo()`.
- Gestire l'ordinamento di collezioni di oggetti complessi.

### Esempio di Output
```text
Pellicole PRIMA DEL SORTING:

Titolo: Inception, Regista: Christopher Nolan, Anno: 2010
Titolo: Pulp Fiction, Regista: Quentin Tarantino, Anno: 1994
Titolo: Il Padrino, Regista: Francis Ford Coppola, Anno: 1972
Titolo: Interstellar, Regista: Christopher Nolan, Anno: 2014
Titolo: La Città Incantata, Regista: Hayao Miyazaki, Anno: 2001

Pellicole DOPO DEL SORTING:

Titolo: Il Padrino, Regista: Francis Ford Coppola, Anno: 1972
Titolo: Pulp Fiction, Regista: Quentin Tarantino, Anno: 1994
Titolo: La Città Incantata, Regista: Hayao Miyazaki, Anno: 2001
Titolo: Inception, Regista: Christopher Nolan, Anno: 2010
Titolo: Interstellar, Regista: Christopher Nolan, Anno: 2014
```

---

## 🇬🇧 English

### Description
This exercise demonstrates how to implement custom object sorting using Java's standard `Comparable` interface.

The program:
- Defines the `Pellicola` (Film) class which implements `Comparable<Pellicola>`.
- Overrides the `compareTo()` method to establish a natural sorting criterion (in this case, based on the release year).
- Uses `Collections.sort()` to sort a list of `Pellicola` objects.
- Prints the list before and after sorting.

### Learning Objective
- Learn how to use standard Java system interfaces.
- Understand the logic of the `compareTo()` method.
- Handle sorting for collections of complex objects.

### Output Example
```text
Pellicole PRIMA DEL SORTING:

Titolo: Inception, Regista: Christopher Nolan, Anno: 2010
Titolo: Pulp Fiction, Regista: Quentin Tarantino, Anno: 1994
Titolo: Il Padrino, Regista: Francis Ford Coppola, Anno: 1972
Titolo: Interstellar, Regista: Christopher Nolan, Anno: 2014
Titolo: La Città Incantata, Regista: Hayao Miyazaki, Anno: 2001

Pellicole DOPO DEL SORTING:

Titolo: Il Padrino, Regista: Francis Ford Coppola, Anno: 1972
Titolo: Pulp Fiction, Regista: Quentin Tarantino, Anno: 1994
Titolo: La Città Incantata, Regista: Hayao Miyazaki, Anno: 2001
Titolo: Inception, Regista: Christopher Nolan, Anno: 2010
Titolo: Interstellar, Regista: Christopher Nolan, Anno: 2014
```
