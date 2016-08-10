contract owned {
    address public owner;

    function owned() {
        owner = msg.sender;
    }

    modifier onlyowner { if (msg.sender != owner) throw; }

    event OwnershipTransfer(address indexed _old, address indexed _new);

    function transferOwner(address _who) {
        OwnershipTransfer(owner, _who);
        owner = _who;
    }
}
