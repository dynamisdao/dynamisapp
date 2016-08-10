import "contracts/owned.sol";


contract ResolverType is owned {
    address public origin;
    address public current;

    mapping (address => address) public history;

    event Updated(address indexed _old, address indexed _new);

    function update(address _where) public onlyowner returns (bool);
}


contract Resolver is ResolverType {
    function update(address _where) public onlyowner returns (bool) {
        if (_where == 0x0) throw;
        if (history[_where] != 0x0) throw;
        Updated(current, _where);
        history[current] = _where;
        current = _where;

        return true;
    }
}
