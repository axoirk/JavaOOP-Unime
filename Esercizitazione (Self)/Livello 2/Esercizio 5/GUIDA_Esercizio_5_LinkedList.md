# Guida completa - Esercizio 5: Linked List da zero

Questa guida ti accompagna dalle basi fino a una implementazione completa della lista concatenata, con esempi pratici e metodi tipici.

---

## 1) Cos'e una Linked List

Una **Linked List** (lista concatenata) e una struttura dati composta da nodi collegati tra loro.

Ogni nodo contiene:
1. un **dato** (`data`)
2. un **riferimento al nodo successivo** (`link` o `next`)

Differenza con array:
- Array: elementi contigui in memoria, dimensione fissa.
- Linked List: elementi sparsi in memoria, dimensione dinamica.

---

## 2) Il concetto di nodo (`ListNode`)

Nell'esercizio devi usare una classe interna privata:

```java
private class ListNode {
    String data;
    ListNode link;
}
```

Significato:
- `data`: valore salvato nel nodo
- `link`: puntatore al nodo successivo
- se `link == null`, sei arrivato all'ultimo nodo

---

## 3) Il ruolo di `head`

`head` e il riferimento al **primo nodo** della lista.

- Se `head == null`, la lista e vuota.
- Se `head != null`, da `head` puoi raggiungere tutti gli altri nodi seguendo i `link`.

Esempio visuale:

```text
head
  |
  v
[A|*] -> [B|*] -> [C|null]
```

---

## 4) Struttura base della classe `StringLinkedList`

```java
public class StringLinkedList {

    private class ListNode {
        String data;
        ListNode link;
    }

    private ListNode head; // testa della lista
    private int size;      // opzionale ma molto utile
}
```

---

## 5) Costruttore del nodo (consigliato)

Per creare nodi in modo pulito, usa un costruttore:

```java
private class ListNode {
    String data;
    ListNode link;

    ListNode(String data, ListNode link) {
        this.data = data;
        this.link = link;
    }
}
```

---

## 6) Metodo richiesto: aggiungere in cima (`addFirst`)

Il testo dell'esercizio richiede aggiunta in testa.

Logica:
1. Crea nuovo nodo.
2. Il nuovo nodo punta all'attuale `head`.
3. Aggiorna `head` col nuovo nodo.

```java
public void addFirst(String value) {
    ListNode newNode = new ListNode(value, head);
    head = newNode;
    size++;
}
```

Esempio:
- Lista iniziale: `head -> [B] -> [C]`
- `addFirst("A")`
- Risultato: `head -> [A] -> [B] -> [C]`

---

## 7) Metodo `hasNext` (correzione concettuale)

Nel tuo file c'e:

```java
public boolean hasNext(ListNode head) {
    return head != null && head.link != null;
}
```

Funziona, ma:
- il parametro chiamato `head` puo confondere (sembra la testa reale della lista)
- spesso `hasNext` ha senso su un nodo corrente (`current`)

Versione piu chiara:

```java
private boolean hasNext(ListNode current) {
    return current != null && current.link != null;
}
```

---

## 8) Metodi fondamentali da implementare

Anche se l'esercizio chiede solo l'aggiunta in testa, questi metodi ti servono per padroneggiare la struttura.

## 8.1 `isEmpty`

```java
public boolean isEmpty() {
    return head == null;
}
```

## 8.2 `size`

```java
public int size() {
    return size;
}
```

## 8.3 `addLast`

```java
public void addLast(String value) {
    ListNode newNode = new ListNode(value, null);

    if (head == null) {
        head = newNode;
        size++;
        return;
    }

    ListNode current = head;
    while (current.link != null) {
        current = current.link;
    }
    current.link = newNode;
    size++;
}
```

## 8.4 `contains`

```java
public boolean contains(String value) {
    ListNode current = head;
    while (current != null) {
        if (current.data.equals(value)) {
            return true;
        }
        current = current.link;
    }
    return false;
}
```

## 8.5 `removeFirst`

```java
public String removeFirst() {
    if (head == null) {
        throw new IllegalStateException("Lista vuota");
    }

    String removed = head.data;
    head = head.link;
    size--;
    return removed;
}
```

## 8.6 `remove(value)` (prima occorrenza)

```java
public boolean remove(String value) {
    if (head == null) return false;

    if (head.data.equals(value)) {
        head = head.link;
        size--;
        return true;
    }

    ListNode prev = head;
    ListNode current = head.link;

    while (current != null) {
        if (current.data.equals(value)) {
            prev.link = current.link;
            size--;
            return true;
        }
        prev = current;
        current = current.link;
    }
    return false;
}
```

---

## 9) Metodo `toString` utile per debug

```java
@Override
public String toString() {
    StringBuilder sb = new StringBuilder("[");
    ListNode current = head;

    while (current != null) {
        sb.append(current.data);
        if (current.link != null) sb.append(", ");
        current = current.link;
    }

    sb.append("]");
    return sb.toString();
}
```

---

## 10) Esempio completo di uso in `Main`

```java
public class Main {
    public static void main(String[] args) {
        StringLinkedList list = new StringLinkedList();

        list.addFirst("Pane");
        list.addFirst("Latte");
        list.addLast("Uova");

        System.out.println(list);                // [Latte, Pane, Uova]
        System.out.println(list.contains("Pane"));// true
        System.out.println(list.removeFirst());   // Latte
        System.out.println(list);                 // [Pane, Uova]
    }
}
```

---

## 11) Versione generica (`LinkedList<T>`)

Quando diciamo "metodi generici", spesso intendiamo che la lista deve funzionare con qualunque tipo (`String`, `Integer`, `Studente`, ...).

Struttura:

```java
public class LinkedList<T> {

    private class Node {
        T data;
        Node next;

        Node(T data, Node next) {
            this.data = data;
            this.next = next;
        }
    }

    private Node head;
    private int size;

    public void addFirst(T value) {
        head = new Node(value, head);
        size++;
    }

    public boolean contains(T value) {
        Node current = head;
        while (current != null) {
            if ((value == null && current.data == null) ||
                (value != null && value.equals(current.data))) {
                return true;
            }
            current = current.next;
        }
        return false;
    }
}
```

Perche e importante:
- riusi la stessa logica con qualsiasi tipo
- impari i **Generics** di Java (`<T>`)

---

## 12) Errori comuni da evitare

1. **Dimenticare di aggiornare `head`** in `addFirst` o `removeFirst`.
2. **Perdere il resto della lista** quando modifichi i link.
3. Usare `==` tra stringhe invece di `.equals(...)`.
4. Non gestire il caso lista vuota.
5. Dimenticare `size++` / `size--`.

---

## 13) Complessita (Big-O) dei metodi principali

| Metodo | Complessita |
|---|---|
| `addFirst` | `O(1)` |
| `removeFirst` | `O(1)` |
| `addLast` (senza tail) | `O(n)` |
| `contains` | `O(n)` |
| `remove(value)` | `O(n)` |

Se aggiungi un riferimento `tail`, `addLast` puo diventare `O(1)`.

---

## 14) Mini checklist per completare l'esercizio 5

1. Crea `head` in `StringLinkedList`.
2. Completa `ListNode` (campi + costruttore).
3. Implementa `addFirst`.
4. Aggiungi almeno `isEmpty`, `size`, `toString`.
5. Testa da `Main` con piu inserimenti.
6. Verifica casi limite: lista vuota, un solo nodo, piu nodi.

---

## 15) Implementazione minima consigliata (pronta)

```java
public class StringLinkedList {

    private class ListNode {
        String data;
        ListNode link;

        ListNode(String data, ListNode link) {
            this.data = data;
            this.link = link;
        }
    }

    private ListNode head;
    private int size;

    public void addFirst(String value) {
        head = new ListNode(value, head);
        size++;
    }

    public boolean isEmpty() {
        return head == null;
    }

    public int size() {
        return size;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("[");
        ListNode current = head;
        while (current != null) {
            sb.append(current.data);
            if (current.link != null) sb.append(", ");
            current = current.link;
        }
        sb.append("]");
        return sb.toString();
    }
}
```

Con questa base hai gia una lista concatenata funzionante e pronta da estendere con gli altri metodi.
