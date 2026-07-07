# Esercizio 3 – Interfacce

---

### Descrizione
Questo esercizio illustra l'uso delle **interfacce** in Java per definire contratti comportamentali comuni tra oggetti logicamente distanti.

Il programma:
- Definisce l'interfaccia `Measurable` con i metodi `getArea()` e `getPerimeter()`.
- Implementa `Measurable` in classi diverse come `Circle` e `Smartphone`.
- Utilizza un `ArrayList<Measurable>` per memorizzare e processare oggetti diversi che condividono lo stesso contratto.
- Dimostra come le interfacce permettano di accomunare oggetti che non appartengono alla stessa gerarchia di ereditarietà.

### Obiettivo didattico
- Comprendere la differenza tra ereditarietà (`extends`) e implementazione di interfacce (`implements`).
- Apprendere come definire capacità comuni tra oggetti diversi.
- Utilizzare le interfacce come tipi di dato per il polimorfismo.

### Esempio di Output
```text
L'area dell'oggetto Circle equivale a: 1256.6370614359173
Il perimetro dell'oggetto Circle equivale a: 125.66370614359172
L'area dell'oggetto Smartphone equivale a: 435.0
Il perimetro dell'oggetto Smartphone equivale a: 89.0
```

