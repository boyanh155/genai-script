var ListNode = /** @class */ (function () {
    function ListNode(val, next) {
        this.val = val === undefined ? 0 : val;
        this.next = next === undefined ? null : next;
    }
    ListNode.prototype.printNode = function () {
        var current = this;
        while (current.next !== null) {
            console.log(current === null || current === void 0 ? void 0 : current.val);
            current = current.next;
        }
    };
    return ListNode;
}());
function addTwoNumbers(l1, l2, out, carry) {
    var _a, _b, _c, _d, _e;
    if (out === void 0) { out = null; }
    if (carry === void 0) { carry = 0; }
    var result = out === null ? new ListNode() : out;
    if (l1 === null && l2 === null && !carry)
        return null;
    var sum = ((_a = l1 === null || l1 === void 0 ? void 0 : l1.val) !== null && _a !== void 0 ? _a : 0) + ((_b = l2 === null || l2 === void 0 ? void 0 : l2.val) !== null && _b !== void 0 ? _b : 0) + carry;
    carry = 0;
    if (sum >= 10) {
        carry = 1;
        result.val = sum - 10;
    }
    else {
        result.val = sum;
    }
    result.next = addTwoNumbers((_c = l1 === null || l1 === void 0 ? void 0 : l1.next) !== null && _c !== void 0 ? _c : null, (_d = l2 === null || l2 === void 0 ? void 0 : l2.next) !== null && _d !== void 0 ? _d : null, (_e = result.next) !== null && _e !== void 0 ? _e : null, carry);
    return result;
}
var b = addTwoNumbers(new ListNode(2, new ListNode(4, new ListNode(8))), new ListNode(5, new ListNode(6, new ListNode(4))));
console.log(b);
// b?.printNode();
