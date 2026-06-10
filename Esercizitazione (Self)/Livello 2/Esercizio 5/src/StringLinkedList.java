/**
 * Implementazione didattica di lista concatenata semplice di stringhe.
 * Introduce nodi collegati e inserimento in testa/coda.
 */
public class StringLinkedList {

    /**
     * Nodo interno: contiene dato e riferimento al nodo successivo.
     */
    private class ListNode {
        String data;
        ListNode link;

        ListNode(String data) {
            this.data = data;
            this.link = null;
        }
    }

    private ListNode head;

    /**
     * Controlla se il nodo corrente punta a un nodo successivo.
     */
    public static boolean hasNext(ListNode node) {
        return node != null && node.link != null;
    }

    public void addTail(String data) {
        ListNode newNode = new ListNode(data);
        if (head == null) {
            head = newNode;
        } else {
            // Scorre fino all'ultimo nodo disponibile.
            while (hasNext(head)) {
                if(!hasNext(head)) {
                    head.link = newNode;
                    break;
                }
                head = head.link;
            }
        }
    }

    public void addHead(String data) {
        ListNode newNode = new ListNode(data);
        if (head == null) {
            head = newNode;
        } else {
           // Inserimento in testa: il nuovo nodo punta alla vecchia head.
           ListNode current = head;
           head = newNode;
           head.link = current;
        }
    }

}
