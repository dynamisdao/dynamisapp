import "contracts/owned.sol";


contract ClaimType is owned {
    address public policy;
    address public pool;

    enum Status {
        Created,    // => (Open, Rejected)
        Open,       // => (Closed, Terminated)
        Closed,     // => ()
        Rejected,   // => ()
        Terminated  // => ()
    }

    uint public createdAt;

    Status public status;

    modifier onlypool { if (msg.sender != pool) throw; }
    modifier onlypolicy { if (msg.sender != policy) throw; }
    modifier onlystatus(Status _status) { if (status != _status) throw; }

    event Opened(address indexed _who, uint _claimId);
    event Extended(address indexed _who, uint _claimId);
    event Closed(address indexed _who, uint _claimId);

    function extend(string _evidenceURI) public onlyowner returns (bool);
    function close() public onlyowner returns (bool);
    function triggerPayment() public returns (bool);

    /*
     *  Administrative API
     */
    function authorizeOpen(uint claimId,
                           bool isAuthorized,
                           string _reasonURI) public onlypool onlystatus(Status.Created) returns (bool);

    function authorizeExtension(uint claimId,
                                bool isAuthorized,
                                string _reasonURI) public onlypool onlystatus(Status.Open) returns (bool);

    function terminate(uint claimId,
                       string _reasonURI) public onlypool onlystatus(Status.Open) returns (bool);
}
