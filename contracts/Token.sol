import {ERC20} from "contracts/ERC20.sol";
import {SafeMath} from "contracts/SafeMath.sol";
import {owned} from "contracts/owned.sol";


contract Token is ERC20, SafeMath {
    uint public totalSupply;
    mapping (address => uint) public balanceOf;
    mapping (address => mapping (address => uint)) public allowance;

    function Token(uint initialSupply) {
        totalSupply = initialSupply;
        balanceOf[msg.sender] = initialSupply;
    }

    function transfer(address to, uint value) returns (bool ok) {
        if (balanceOf[msg.sender] >= value) {
            balanceOf[msg.sender] = safeSub(balanceOf[msg.sender], value);
            balanceOf[to] = safeAdd(balanceOf[to], value);
            Transfer(msg.sender, to, value);
            return true;
        } else {
            return false;
        }
    }

    function transferFrom(address from, address to, uint value) returns (bool ok) {
        if (balanceOf[from] >= value && allowance[from][to] >= value) {
            balanceOf[from] = safeSub(balanceOf[from], value);
            allowance[from][to] = safeSub(allowance[from][to], value);
            balanceOf[to] = safeAdd(balanceOf[to], value);
            Transfer(from, to, value);
            return true;
        } else {
            return false;
        }
    }

    function approve(address spender, uint value) returns (bool ok) {
        allowance[msg.sender][spender] = value;
        return true;
    }
}


contract MintableToken is Token, owned {
    mapping (address => bool) public minters;

    modifier onlyminter { if (!minters[msg.sender]) throw; }

    event Mint(address indexed minter, uint value);

    function MintableToken(uint initialSupply) Token(initialSupply) {
        minters[msg.sender] = true;
    }

    function addMinter(address who) public onlyowner {
        minters[msg.sender] = true;
    }

    function removeMinter(address who) public onlyowner {
        minters[msg.sender] = false;
    }

    function mint(uint value) public onlyminter returns (bool ok) {
        balanceOf[msg.sender] = safeAdd(balanceOf[msg.sender], value);
        totalSupply = safeAdd(totalSupply, value);
        Mint(msg.sender, value);
        return true;
    }
}
