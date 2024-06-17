class ListNode {
  val: number;
  next: ListNode | null;

  constructor(val?: number, next?: ListNode | null) {
    this.val = val === undefined ? 0 : val;
    this.next = next === undefined ? null : next;
  }

  printNode() {
    let current: ListNode | null = this;
    while (current.next !== null) {
      console.log(current?.val);
      current = current.next;
    }
  }
}

function addTwoNumbers(
  l1: ListNode | null,
  l2: ListNode | null,
  out: ListNode | null = null,
  carry:number = 0,
): ListNode | null {
  const result: ListNode = out === null ? new ListNode() : out;
  if (l1 === null && l2 === null && !carry) return null;
  const sum = (l1?.val ?? 0) + (l2?.val ?? 0) +carry;
  carry = 0;
  if (sum >= 10) {
    carry = 1;
    result.val = sum - 10;
  } else {
    
    result.val = sum;
  }
  result.next = addTwoNumbers(
    l1?.next ?? null,
    l2?.next ?? null,
    result.next ?? null,
    carry
  );

  return result;
}

const b = addTwoNumbers(
  new ListNode(2, new ListNode(4, new ListNode(8))),
  new ListNode(5, new ListNode(6, new ListNode(4)))
);

console.log(b)

// b?.printNode();
