import "contracts/owned.sol";


contract NotaryType is owned {
    struct Record {
        uint createdAt;
        address createdBy;
        string value;
    }

    Record[] public records;

    event Notarized(address indexed createdBy, uint recordIdx);

    function notorize(string value) public returns (uint);
    function lookup(uint idx) constant returns (uint createdAt, address createdBy, string value);
    function numRecords() constant returns (uint);
}


contract Notary is NotaryType {
    function notorize(string value) public returns (uint) {
        records.push(Record(now, msg.sender, value));
        Notarized(msg.sender, records.length - 1);
        return records.length - 1;
    }

    function lookup(uint idx) constant returns (uint createdAt, address createdBy, string value) {
        var record = records[idx];
        createdBy = record.createdBy;
        createdAt = record.createdAt;
        value = record.value;

        return (createdAt, createdBy, value);
    }

    function numRecords() constant returns (uint) {
        return records.length;
    }
}
