import "contracts/owned.sol";


contract PolicyType is owned {
    address public pool;

    modifier onlypool { if (msg.sender != pool) throw; }

    enum Status {
        Active,    // => (Closed, Claiming, Terminated, Retired)
        Closed,    // => ()
        Claiming,  // => (Closed, Active, Terminated, Retired)
        Retired,   // => ()
        Terminated // => ()
    }

    Status public status;

    struct Config {
        uint premiumPaymentAmount;
        uint premiumPaymentFrequency;
    }

    // Stores configuration information about the policy
    Config public config;

    struct Meta {
        uint createdAt;
        uint lastPaymentAt;
        uint nextPaymentAt;
    }

    // Stores metadata about the policy
    Meta public meta;

    event PremiumPayment(address indexed _who, uint _amount);

    // Should send money to the pool.
    function payPremium() public returns (bool);

    function terminate(string _reasonURI) public returns (bool);

    // Deploys a new Claim contract.
    function openClaim(string _evidenceURI) public onlyowner returns (bool);

    // Array of claims
    mapping (uint => address) public claims;
    uint public numClaims;

    // If a claim is currently active, this should be non-zero.
    uint public activeClaimId;

}
