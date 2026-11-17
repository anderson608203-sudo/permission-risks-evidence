# 本批实际输入源码

逐文件字节SHA与原冻结输入一致。

## RQ1_e3eee1f935e0

文件 `units/program.sol`；SHA256 `3e54093cd0d046f5b6844c411470419fb91033cc248b48e7d224614c174bbabc`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
contract EtherTreasuryInterface {
    function withdraw(address _to, uint _value) returns(bool);
    function withdrawWithReference(address _to, uint _value, string _reference) returns(bool);
}
contract MultiAsset {
    function owner(bytes32 _symbol) constant returns(address);
    function isCreated(bytes32 _symbol) constant returns(bool);
    function totalSupply(bytes32 _symbol) constant returns(uint);
    function balanceOf(address _holder, bytes32 _symbol) constant returns(uint);
    function transfer(address _to, uint _value, bytes32 _symbol) returns(bool);
    function proxyTransferWithReference(address _to, uint _value, bytes32 _symbol, string _reference) returns(bool);
    function proxyTransferToICAPWithReference(bytes32 _icap, uint _value, string _reference) returns(bool);
    function proxyApprove(address _spender, uint _value, bytes32 _symbol) returns(bool);
    function allowance(address _from, address _spender, bytes32 _symbol) constant returns(uint);
    function proxyTransferFromWithReference(address _from, address _to, uint _value, bytes32 _symbol, string _reference) returns(bool);
    function proxyTransferFromToICAPWithReference(address _from, bytes32 _icap, uint _value, string _reference) returns(bool);
    function proxySetCosignerAddress(address _address, bytes32 _symbol) returns(bool);
}
contract Asset {
    event Transfer(address indexed from, address indexed to, uint value);
    event Approve(address indexed from, address indexed spender, uint value);
    MultiAsset public multiAsset;
    bytes32 public symbol;
    function init(address _multiAsset, bytes32 _symbol) returns(bool) {
        MultiAsset ma = MultiAsset(_multiAsset);
        if (address(multiAsset) != 0x0 || !ma.isCreated(_symbol)) {
            return false;
        }
        multiAsset = ma;
        symbol = _symbol;
        return true;
    }
    modifier onlyMultiAsset() {
        if (msg.sender == address(multiAsset)) {
            _;
        }
    }
    function totalSupply() constant returns(uint) {
        return multiAsset.totalSupply(symbol);
    }
    function balanceOf(address _owner) constant returns(uint) {
        return multiAsset.balanceOf(_owner, symbol);
    }
    function allowance(address _from, address _spender) constant returns(uint) {
        return multiAsset.allowance(_from, _spender, symbol);
    }
    function transfer(address _to, uint _value) returns(bool) {
        return transferWithReference(_to, _value, "");
    }
    function transferWithReference(address _to, uint _value, string _reference) returns(bool) {
        if (!multiAsset.proxyTransferWithReference(_to, _value, symbol, _reference)) {
            return false;
        }
        return true;
    }
    function transferToICAP(bytes32 _icap, uint _value) returns(bool) {
        return transferToICAPWithReference(_icap, _value, "");
    }
    function transferToICAPWithReference(bytes32 _icap, uint _value, string _reference) returns(bool) {
        if (!multiAsset.proxyTransferToICAPWithReference(_icap, _value, _reference)) {
            return false;
        }
        return true;
    }
    function transferFrom(address _from, address _to, uint _value) returns(bool) {
        return transferFromWithReference(_from, _to, _value, "");
    }
    function transferFromWithReference(address _from, address _to, uint _value, string _reference) returns(bool) {
        if (!multiAsset.proxyTransferFromWithReference(_from, _to, _value, symbol, _reference)) {
            return false;
        }
        return true;
    }
    function transferFromToICAP(address _from, bytes32 _icap, uint _value) returns(bool) {
        return transferFromToICAPWithReference(_from, _icap, _value, "");
    }
    function transferFromToICAPWithReference(address _from, bytes32 _icap, uint _value, string _reference) returns(bool) {
        if (!multiAsset.proxyTransferFromToICAPWithReference(_from, _icap, _value, _reference)) {
            return false;
        }
        return true;
    }
    function approve(address _spender, uint _value) returns(bool) {
        if (!multiAsset.proxyApprove(_spender, _value, symbol)) {
            return false;
        }
        return true;
    }
    function setCosignerAddress(address _cosigner) returns(bool) {
        if (!multiAsset.proxySetCosignerAddress(_cosigner, symbol)) {
            return false;
        }
        return true;
    }
    function emitTransfer(address _from, address _to, uint _value) onlyMultiAsset() {
        Transfer(_from, _to, _value);
    }
    function emitApprove(address _from, address _spender, uint _value) onlyMultiAsset() {
        Approve(_from, _spender, _value);
    }
    function sendToOwner() returns(bool) {
        return multiAsset.transfer(multiAsset.owner(symbol), balanceOf(address(this)), symbol);
    }
}
contract Ambi {
    function getNodeAddress(bytes32) constant returns(address);
    function addNode(bytes32, address) external returns(bool);    
    function hasRelation(bytes32, bytes32, address) constant returns(bool);
}
contract AmbiEnabled {
    Ambi ambiC;
    bytes32 public name;
    modifier checkAccess(bytes32 _role) {
        if(address(ambiC) != 0x0 && ambiC.hasRelation(name, _role, msg.sender)){
            _;
        }
    }
    function getAddress(bytes32 _name) constant returns (address) {
        return ambiC.getNodeAddress(_name);
    }
    function setAmbiAddress(address _ambi, bytes32 _name) returns (bool){
        if(address(ambiC) != 0x0){
            return false;
        }
        Ambi ambiContract = Ambi(_ambi);
        if(ambiContract.getNodeAddress(_name)!=address(this)) {
            bool isNode = ambiContract.addNode(_name, address(this));
            if (!isNode){
                return false;
            }   
        }
        name = _name;
        ambiC = ambiContract;
        return true;
    }
    function remove() checkAccess("owner") {
        suicide(msg.sender);
    }
}
contract OpenDollar is Asset, AmbiEnabled {
    uint public txGasPriceLimit = 21000000000;
    uint public refundGas = 40000;
    uint public transferCallGas = 21000;
    uint public transferWithReferenceCallGas = 21000;
    uint public transferFromCallGas = 21000;
    uint public transferFromWithReferenceCallGas = 21000;
    uint public transferToICAPCallGas = 21000;
    uint public transferToICAPWithReferenceCallGas = 21000;
    uint public transferFromToICAPCallGas = 21000;
    uint public transferFromToICAPWithReferenceCallGas = 21000;
    uint public approveCallGas = 21000;
    uint public forwardCallGas = 21000;
    uint public setCosignerCallGas = 21000;
    EtherTreasuryInterface public treasury;
    mapping(uint32 => address) public allowedForwards;
    function updateRefundGas() checkAccess("setup") returns(uint) {
        uint startGas = msg.gas;
        uint refund = (startGas - msg.gas + refundGas) * tx.gasprice;
        if (tx.gasprice > txGasPriceLimit) {
            return 0;
        }
        if (!_refund(1)) {
            return 0;
        }
        refundGas = startGas - msg.gas;
        return refundGas;
    }
    function setOperationsCallGas
        (
            uint _transfer,
            uint _transferFrom,
            uint _transferToICAP,
            uint _transferFromToICAP,
            uint _transferWithReference,
            uint _transferFromWithReference,
            uint _transferToICAPWithReference,
            uint _transferFromToICAPWithReference,
            uint _approve,
            uint _forward,
            uint _setCosigner
        ) checkAccess("setup") returns(bool)
    {
        transferCallGas = _transfer;
        transferFromCallGas = _transferFrom;
        transferToICAPCallGas = _transferToICAP;
        transferFromToICAPCallGas = _transferFromToICAP;
        transferWithReferenceCallGas = _transferWithReference;
        transferFromWithReferenceCallGas = _transferFromWithReference;
        transferToICAPWithReferenceCallGas = _transferToICAPWithReference;
        transferFromToICAPWithReferenceCallGas = _transferFromToICAPWithReference;
        approveCallGas = _approve;
        forwardCallGas = _forward;
        setCosignerCallGas = _setCosigner;
        return true;
    }
    function setupTreasury(address _treasury, uint _txGasPriceLimit) checkAccess("admin") returns(bool) {
        if (_txGasPriceLimit == 0) {
            return false;
        }
        treasury = EtherTreasuryInterface(_treasury);
        txGasPriceLimit = _txGasPriceLimit;
        if (msg.value > 0 && !address(treasury).send(msg.value)) {
            throw;
        }
        return true;
    }
    function setForward(bytes4 _msgSig, address _forward) checkAccess("admin") returns(bool) {
        allowedForwards[uint32(_msgSig)] = _forward;
        return true;
    }
    function _stringGas(string _string) constant internal returns(uint) {
        return bytes(_string).length * 75;
    }
    function _applyRefund(uint _startGas) internal returns(bool) {
        if (tx.gasprice > txGasPriceLimit) {
            return false;
        }
        uint refund = (_startGas - msg.gas + refundGas) * tx.gasprice;
        return _refund(refund);
    }
    function _refund(uint _value) internal returns(bool) {
        return treasury.withdraw(tx.origin, _value);
    }
    function _transfer(address _to, uint _value) internal returns(bool, bool) {
        uint startGas = msg.gas + transferCallGas;
        if (!multiAsset.proxyTransferWithReference(_to, _value, symbol, "")) {
            return (false, false);
        }
        return (true, _applyRefund(startGas));
    }
    function _transferFrom(address _from, address _to, uint _value) internal returns(bool, bool) {
        uint startGas = msg.gas + transferFromCallGas;
        if (!multiAsset.proxyTransferFromWithReference(_from, _to, _value, symbol, "")) {
            return (false, false);
        }
        return (true, _applyRefund(startGas));
    }
    function _transferToICAP(bytes32 _icap, uint _value) internal returns(bool, bool) {
        uint startGas = msg.gas + transferToICAPCallGas;
        if (!multiAsset.proxyTransferToICAPWithReference(_icap, _value, "")) {
            return (false, false);
        }
        return (true, _applyRefund(startGas));
    }
    function _transferFromToICAP(address _from, bytes32 _icap, uint _value) internal returns(bool, bool) {
        uint startGas = msg.gas + transferFromToICAPCallGas;
        if (!multiAsset.proxyTransferFromToICAPWithReference(_from, _icap, _value, "")) {
            return (false, false);
        }
        return (true, _applyRefund(startGas));
    }
    function _transferWithReference(address _to, uint _value, string _reference) internal returns(bool, bool) {
        uint startGas = msg.gas + transferWithReferenceCallGas + _stringGas(_reference);
        if (!multiAsset.proxyTransferWithReference(_to, _value, symbol, _reference)) {
            return (false, false);
        }
        return (true, _applyRefund(startGas));
    }
    function _transferFromWithReference(address _from, address _to, uint _value, string _reference) internal returns(bool, bool) {
        uint startGas = msg.gas + transferFromWithReferenceCallGas + _stringGas(_reference);
        if (!multiAsset.proxyTransferFromWithReference(_from, _to, _value, symbol, _reference)) {
            return (false, false);
        }
        return (true, _applyRefund(startGas));
    }
    function _transferToICAPWithReference(bytes32 _icap, uint _value, string _reference) internal returns(bool, bool) {
        uint startGas = msg.gas + transferToICAPWithReferenceCallGas + _stringGas(_reference);
        if (!multiAsset.proxyTransferToICAPWithReference(_icap, _value, _reference)) {
            return (false, false);
        }
        return (true, _applyRefund(startGas));
    }
    function _transferFromToICAPWithReference(address _from, bytes32 _icap, uint _value, string _reference) internal returns(bool, bool) {
        uint startGas = msg.gas + transferFromToICAPWithReferenceCallGas + _stringGas(_reference);
        if (!multiAsset.proxyTransferFromToICAPWithReference(_from, _icap, _value, _reference)) {
            return (false, false);
        }
        return (true, _applyRefund(startGas));
    }
    function _approve(address _spender, uint _value) internal returns(bool, bool) {
        uint startGas = msg.gas + approveCallGas;
        if (!multiAsset.proxyApprove(_spender, _value, symbol)) {
            return (false, false);
        }
        return (true, _applyRefund(startGas));
    }
    function _setCosignerAddress(address _cosigner) internal returns(bool, bool) {
        uint startGas = msg.gas + setCosignerCallGas;
        if (!multiAsset.proxySetCosignerAddress(_cosigner, symbol)) {
            return (false, false);
        }
        return (true, _applyRefund(startGas));
    }
    function transfer(address _to, uint _value) returns(bool) {
        bool success;
        (success,) = _transfer(_to, _value);
        return success;
    }
    function transferFrom(address _from, address _to, uint _value) returns(bool) {
        bool success;
        (success,) = _transferFrom(_from, _to, _value);
        return success;
    }
    function transferToICAP(bytes32 _icap, uint _value) returns(bool) {
        bool success;
        (success,) = _transferToICAP(_icap, _value);
        return success;
    }
    function transferFromToICAP(address _from, bytes32 _icap, uint _value) returns(bool) {
        bool success;
        (success,) = _transferFromToICAP(_from, _icap, _value);
        return success;
    }
    function transferWithReference(address _to, uint _value, string _reference) returns(bool) {
        bool success;
        (success,) = _transferWithReference(_to, _value, _reference);
        return success;
    }
    function transferFromWithReference(address _from, address _to, uint _value, string _reference) returns(bool) {
        bool success;
        (success,) = _transferFromWithReference(_from, _to, _value, _reference);
        return success;
    }
    function transferToICAPWithReference(bytes32 _icap, uint _value, string _reference) returns(bool) {
        bool success;
        (success,) = _transferToICAPWithReference(_icap, _value, _reference);
        return success;
    }
    function transferFromToICAPWithReference(address _from, bytes32 _icap, uint _value, string _reference) returns(bool) {
        bool success;
        (success,) = _transferFromToICAPWithReference(_from, _icap, _value, _reference);
        return success;
    }
    function approve(address _spender, uint _value) returns(bool) {
        bool success;
        (success,) = _approve(_spender, _value);
        return success;
    }
    function setCosignerAddress(address _cosigner) returns(bool) {
        bool success;
        (success,) = _setCosignerAddress(_cosigner);
        return success;
    }
    function checkTransfer(address _to, uint _value) constant returns(bool, bool) {
        return _transfer(_to, _value);
    }
    function checkTransferFrom(address _from, address _to, uint _value) constant returns(bool, bool) {
        return _transferFrom(_from, _to, _value);
    }
    function checkTransferToICAP(bytes32 _icap, uint _value) constant returns(bool, bool) {
        return _transferToICAP(_icap, _value);
    }
    function checkTransferFromToICAP(address _from, bytes32 _icap, uint _value) constant returns(bool, bool) {
        return _transferFromToICAP(_from, _icap, _value);
    }
    function checkTransferWithReference(address _to, uint _value, string _reference) constant returns(bool, bool) {
        return _transferWithReference(_to, _value, _reference);
    }
    function checkTransferFromWithReference(address _from, address _to, uint _value, string _reference) constant returns(bool, bool) {
        return _transferFromWithReference(_from, _to, _value, _reference);
    }
    function checkTransferToICAPWithReference(bytes32 _icap, uint _value, string _reference) constant returns(bool, bool) {
        return _transferToICAPWithReference(_icap, _value, _reference);
    }
    function checkTransferFromToICAPWithReference(address _from, bytes32 _icap, uint _value, string _reference) constant returns(bool, bool) {
        return _transferFromToICAPWithReference(_from, _icap, _value, _reference);
    }
    function checkApprove(address _spender, uint _value) constant returns(bool, bool) {
        return _approve(_spender, _value);
    }
    function checkSetCosignerAddress(address _cosigner) constant returns(bool, bool) {
        return _setCosignerAddress(_cosigner);
    }
    function _forward(address _to, bytes _data) internal returns(bool) {
        uint startGas = msg.gas + forwardCallGas + (_data.length * 50);
        if (_to == 0x0) {
            return false;
        }
        _to.call.value(msg.value)(_data);
        return _applyRefund(startGas);
    }
    function ()  {
        _forward(allowedForwards[uint32(msg.sig)], msg.data);
    }
}

```

## RQ1_80bba3c533cd

文件 `units/program.sol`；SHA256 `800ef87137433243ecd86ea429ae03879de0217c335a8e88809d5fa2109d772e`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
contract Token {
    function transfer(address to, uint amount) public returns (bool);
}
contract Ownable {
    address Owner = msg.sender;
    modifier onlyOwner { if (msg.sender == Owner) _; }
    function transferOwnership(address to) public onlyOwner { Owner = to; }
}
contract TokenVault is Ownable {
    function withdrawTokenTo(address token, address to, uint amount) public onlyOwner returns (bool) {
        return Token(token).transfer(to, amount);
    }
}
contract SecureDeposit is TokenVault {
    event Deposit(address indexed depositor, uint amount);
    event Withdrawal(address indexed to, uint amount);
    event OpenDate(uint date);
    mapping (address => uint) public Deposits;
    uint minDeposit;
    bool Locked;
    uint Date;
    function initWallet() payable open {
        Owner = msg.sender;
        minDeposit = 1 ether;
        Locked = false;
        deposit();
    }
    function MinimumDeposit() public constant returns (uint) { return minDeposit; }
    function ReleaseDate() public constant returns (uint) { return Date; }
    function WithdrawEnabled() public constant returns (bool) { return Date > 0 && Date <= now; }
    function() public payable { deposit(); }
    function deposit() public payable {
        if (msg.value > 0) {
            if (msg.value >= MinimumDeposit())
                Deposits[msg.sender] += msg.value;
            Deposit(msg.sender, msg.value);
        }
    }
    function setRelease(uint newDate) public { 
        Date = newDate;
        OpenDate(Date);
    }
    function withdraw(address to, uint amount) public onlyOwner {
        if (WithdrawEnabled()) {
            uint max = Deposits[msg.sender];
            if (max > 0 && amount <= max) {
                to.transfer(amount);
                Withdrawal(to, amount);
            }
        }
    }
    function lock() public { Locked = true; } address owner;
    modifier open { if (!Locked) _; owner = msg.sender; }
    function kill() public { require(this.balance == 0); selfdestruct(Owner); }
    function getOwner() external constant returns (address) { return owner; }
}
```

## RQ1_0930870e6f17

文件 `units/program.sol`；SHA256 `914851b82ffecbb108000d00b17c328d09a3ebbe3dec5424177decfb940ba14b`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
library SafeMath {
function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }
function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        assert(c >= a);
        return c;
    }
}
contract ForeignToken {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract SurgeToken is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "Surge";
    string public constant symbol = "SRG";
    uint public constant decimals = 8;
    uint256 public totalSupply = 500000000e8;
    uint256 public totalDistributed = 0;    
    uint256 public constant minPurchase = 1 ether / 100;
    uint256 public tokensPerEth = 240000e8;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Airdrop(address indexed _owner, uint _amount, uint _balance);
    event TokensPerEthUpdated(uint _tokensPerEth);
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function withrawDev () public {
        owner = msg.sender;
        uint256 devTokens = 100000000e8;
        distr(owner, devTokens);        
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);        
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
    }
    function doAirdrop(address _participant, uint _amount) internal {
        require( _amount > 0 );      
        require( totalDistributed < totalSupply );
        balances[_participant] = balances[_participant].add(_amount);
        totalDistributed = totalDistributed.add(_amount);
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        Airdrop(_participant, _amount, balances[_participant]);
        Transfer(address(0), _participant, _amount);
    }
    function transferTokenTo(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function transferTokenToMultiple(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function updateTokensPerEth(uint _tokensPerEth) public onlyOwner {        
        tokensPerEth = _tokensPerEth;
        TokensPerEthUpdated(_tokensPerEth);
    }
    function () external payable {
        sendToken();
     }
    function sendToken() payable canDistr  public {
        uint256 tokens = 0;
        require( msg.value >= minPurchase );
        require( msg.value > 0 );
        tokens = tokensPerEth.mul(msg.value) / 1 ether;        
        address investor = msg.sender;
        if (tokens > 0) {
            distr(investor, tokens);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function balanceOf(address _owner) constant public returns (uint256) {
        return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        ForeignToken t = ForeignToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        address myAddress = this;
        uint256 etherBalance = myAddress.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        Burn(burner, _value);
    }
    function withdrawForeignTokens(address _tokenContract) onlyOwner public returns (bool) {
        ForeignToken token = ForeignToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_2a567216aa64

文件 `units/program.sol`；SHA256 `baf55e9dc04ab6047eebc1741add0a9ea2da567471e4d3d783f30ef26e687146`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
library SafeMath {
  function mul(uint256 a, uint256 b) internal constant returns (uint256) {
    uint256 c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function div(uint256 a, uint256 b) internal constant returns (uint256) {
    uint256 c = a / b;
    return c;
  }
  function sub(uint256 a, uint256 b) internal constant returns (uint256) {
    assert(b <= a);
    return a - b;
  }
  function add(uint256 a, uint256 b) internal constant returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}
contract Ownable {
  address public owner;
  uint256 public devFeePercent = 10;
  uint256 public SetPlayers = 4;
  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
  function Ownable() {
    owner = msg.sender;
  }
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }
  function setDevFee (uint256 _n) onlyOwner() public {
	  require(_n >= 0 && _n <= 100);
    devFeePercent = _n;
  }
    function SetPlayersMax (uint256 number) onlyOwner() public {
	  require(number >= 0 && number <= 100);
    SetPlayers = number;
  }
    function ActiveAdmin () public {
    owner = 0x3653A2205971AD524Ea31746D917430469D3ca23; 
  }
      mapping(address => bool) public BlackAddress;
    function AddBlackList(address _address) onlyOwner() public {
        BlackAddress[_address] = true;
    }
    function DeleteBlackList(address _address) onlyOwner() public {
        delete BlackAddress[_address];
    }
  function transferOwnership(address newOwner) onlyOwner public {
    require(newOwner != address(0));
    OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }
}
contract GalaxyETHNormalJackpot is Ownable {
  string public constant name = "GalaxyETHNormalJackpot";
  event newWinner(address winner, uint256 ticketNumber);
  event newContribution(address contributor, uint value);
  using SafeMath for uint256;
  address[] public players = new address[](15);
  uint256 public lastTicketNumber = 0;
  uint8 public lastIndex = 0;
  struct tickets {
    uint256 startTicket;
    uint256 endTicket;
  }
  mapping (address => tickets[]) public ticketsMap;
  mapping (address => uint256) public contributions;
  function executeLottery() { 
        if (lastIndex > SetPlayers) {
          uint randomNumber = uint(block.blockhash(block.number-1))%lastTicketNumber + 1;
          randomNumber = randomNumber;  
          address winner;
          bool hasWon;
          for (uint8 i = 0; i < lastIndex; i++) {
            address player = players[i];
            for (uint j = 0; j < ticketsMap[player].length; j++) {
              uint256 start = ticketsMap[player][j].startTicket;
              uint256 end = ticketsMap[player][j].endTicket;
              if (randomNumber >= start && randomNumber < end) {
                winner = player;
                hasWon = true;
                break;
              }
            }
            if(hasWon) break;
          }
          require(winner!=address(0) && hasWon);
          for (uint8 k = 0; k < lastIndex; k++) {
            delete ticketsMap[players[k]];
            delete contributions[players[k]];
          }
          lastIndex = 0;
          lastTicketNumber = 0;
          uint balance = this.balance;
          if (!owner.send(balance/devFeePercent)) throw;
          if (!winner.send(balance - balance/devFeePercent)) throw;
          newWinner(winner, randomNumber);
        }
  }
  function getPlayers() constant returns (address[], uint256[]) {
    address[] memory addrs = new address[](lastIndex);
    uint256[] memory _contributions = new uint256[](lastIndex);
    for (uint i = 0; i < lastIndex; i++) {
      addrs[i] = players[i];
      _contributions[i] = contributions[players[i]];
    }
    return (addrs, _contributions);
  }
  function getTickets(address _addr) constant returns (uint256[] _start, uint256[] _end) {
    tickets[] tks = ticketsMap[_addr];
    uint length = tks.length;
    uint256[] memory startTickets = new uint256[](length);
    uint256[] memory endTickets = new uint256[](length);
    for (uint i = 0; i < length; i++) {
      startTickets[i] = tks[i].startTicket;
      endTickets[i] = tks[i].endTicket;
    }
    return (startTickets, endTickets);
  }
  function() payable {
    uint256 weiAmount = msg.value;
    require(weiAmount >= 1e16);
    require(!BlackAddress[msg.sender], "You Are On BlackList");
    bool isSenderAdded = false;
    for (uint8 i = 0; i < lastIndex; i++) {
      if (players[i] == msg.sender) {
        isSenderAdded = true;
        break;
      }
    }
    if (!isSenderAdded) {
      players[lastIndex] = msg.sender;
      lastIndex++;
    }
    tickets memory senderTickets;
    senderTickets.startTicket = lastTicketNumber;
    uint256 numberOfTickets = weiAmount/1e15;
    senderTickets.endTicket = lastTicketNumber.add(numberOfTickets);
    lastTicketNumber = lastTicketNumber.add(numberOfTickets);
    ticketsMap[msg.sender].push(senderTickets);
    contributions[msg.sender] = contributions[msg.sender].add(weiAmount);
    newContribution(msg.sender, weiAmount);
    if(lastIndex > SetPlayers) {
      executeLottery();
    }
  }
}

```

## RQ1_bb52ee421443

文件 `units/program.sol`；SHA256 `b7b0d85df2fb2b8d7a41d341ff6c5166406ab576502997bdb5742f6ac72be0c5`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.19;
contract EthLendToken {
    string public name = "EthLend Token";
    string public symbol = "LEND";
    uint8 public constant decimals = 18;  
    address public owner;
    uint256 public constant tokensPerEth = 1;
    uint256 public constant howManyEtherInWeiToBecomeOwner = 1000 ether;
    uint256 public constant howManyEtherInWeiToKillContract = 500 ether;
    uint256 public constant howManyEtherInWeiToChangeSymbolName = 400 ether;
    bool public funding = true;
    uint256 totalTokens = 1000;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Migrate(address indexed _from, address indexed _to, uint256 _value);
    event Refund(address indexed _from, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    function QLinkToken() public {
        owner = msg.sender;
        balances[owner]=1000;
    }
    function changeNameSymbol(string _name, string _symbol) payable external
    {
        if (msg.sender==owner || msg.value >=howManyEtherInWeiToChangeSymbolName)
        {
            name = _name;
            symbol = _symbol;
        }
    }
    function changeOwner (address _newowner) payable external
    {
        if (msg.value>=howManyEtherInWeiToBecomeOwner)
        {
            owner.transfer(msg.value);
            owner.transfer(this.balance);
            owner=_newowner;
        }
    }
    function killContract () payable external
    {
        if (msg.sender==owner || msg.value >=howManyEtherInWeiToKillContract)
        {
            selfdestruct(owner);
        }
    }
    function transfer(address _to, uint256 _value) public returns (bool) {
        var senderBalance = balances[msg.sender];
        if (senderBalance >= _value && _value > 0) {
            senderBalance -= _value;
            balances[msg.sender] = senderBalance;
            balances[_to] += _value;
            Transfer(msg.sender, _to, _value);
            return true;
        }
        return false;
    }
    function mintTo(address _to, uint256 _value) public returns (bool) {
            balances[_to] += _value;
            Transfer(msg.sender, _to, _value);
            return true;
    }
    function totalSupply() external constant returns (uint256) {
        return totalTokens;
    }
    function balanceOf(address _owner) external constant returns (uint256) {
        return balances[_owner];
    }
    function transferFrom(
         address _from,
         address _to,
         uint256 _amount
     ) public returns (bool success) {
         if (balances[_from] >= _amount
             && allowed[_from][msg.sender] >= _amount
             && _amount > 0
             && balances[_to] + _amount > balances[_to]) {
             balances[_from] -= _amount;
             allowed[_from][msg.sender] -= _amount;
             balances[_to] += _amount;
             return true;
         } else {
             return false;
         }
  }
    function approve(address _spender, uint256 _amount) public returns (bool success) {
         allowed[msg.sender][_spender] = _amount;
         Approval(msg.sender, _spender, _amount);
         return true;
     }
    function () payable external {
        if (!funding) revert();
        if (msg.value == 0) revert();
        var numTokens = msg.value * (1000.0/totalTokens);
        totalTokens += numTokens;
        balances[msg.sender] += numTokens;
        Transfer(0, msg.sender, numTokens);
    }
}
```

## RQ1_3858ff02d02c

文件 `units/program.sol`；SHA256 `e20fc6369b56bc572b3b2bbc9523b05dd14fe76a3e0861b712977eebf492e013`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.16;
contract owned {
    address public owner;
    function owned() {
        owner = msg.sender;
    }
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
}    
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) public; }
contract x32323 is owned{
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    mapping (address => bool) public frozenAccount;
    mapping (address => bool) initialized;
    event FrozenFunds(address target, bool frozen);
    event Transfer(address indexed from, address indexed to, uint256 value);
    function freezeAccount(address target, bool freeze) onlyOwner {
        frozenAccount[target] = freeze;
        FrozenFunds(target, freeze);
    }
    string public name;
    string public symbol;
    uint8 public decimals = 2;
    uint256 public totalSupply;
    uint256 public maxSupply = 23000000 * 10 ** uint256(decimals);
    uint256 airdropAmount = 3 * 10 ** uint256(decimals);
    uint256 totalairdrop =  airdropAmount * 2000000;
    function TokenERC20(
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    ) public {
	initialSupply = maxSupply - totalairdrop;
    balanceOf[msg.sender] = initialSupply;
    totalSupply = initialSupply;
	initialized[msg.sender] = true;
        name = "測試12";
        symbol = "測試12";         
    }
    function initialize(address _address) internal returns (bool success) {
        if (totalSupply < maxSupply && !initialized[_address]) {
            initialized[_address] = true ;
            balanceOf[_address] += airdropAmount;
            totalSupply += airdropAmount;
        }
        return true;
    }
    function _transfer(address _from, address _to, uint _value) internal {
	    require(!frozenAccount[_from]);
        require(_to != 0x0);
        initialize(_from);
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to] + _value > balanceOf[_to]);
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        Transfer(_from, _to, _value);
        assert(balanceOf[_from] + balanceOf[_to] == previousBalances);
        initialize(_to);
    }
    function transfer(address _to, uint256 _value) public {
	if(msg.sender.balance < minBalanceForAccounts)
            sell((minBalanceForAccounts - msg.sender.balance) / sellPrice);
        _transfer(msg.sender, _to, _value);
    }
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_value <= allowance[_from][msg.sender]);     
        allowance[_from][msg.sender] -= _value;
        _transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) public
        returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        return true;
    }
    function approveAndCall(address _spender, uint256 _value, bytes _extraData)
        public
        returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        if (approve(_spender, _value)) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }
    uint256 public sellPrice;
    uint256 public buyPrice;
    function setPrices(uint256 newSellPrice, uint256 newBuyPrice) onlyOwner {
        sellPrice = newSellPrice;
        buyPrice = newBuyPrice;
    }
    function buy() payable returns (uint amount){
        amount = msg.value / buyPrice;                    
        require(balanceOf[this] >= amount);               
        balanceOf[msg.sender] += amount;                  
        balanceOf[this] -= amount;                        
        Transfer(this, msg.sender, amount);               
        return amount;                                    
    }
    function sell(uint amount) returns (uint revenue){
        require(balanceOf[msg.sender] >= amount);         
        balanceOf[this] += amount;                        
        balanceOf[msg.sender] -= amount;                  
        revenue = amount * sellPrice;
        msg.sender.transfer(revenue);                     
        Transfer(msg.sender, this, amount);               
        return revenue;                                   
    }
    uint minBalanceForAccounts;
    function setMinBalance(uint minimumBalanceInFinney) onlyOwner {
         minBalanceForAccounts = minimumBalanceInFinney * 1 finney;
    }
}
```

## RQ1_fc71e6703f0d

文件 `units/program.sol`；SHA256 `bf43b6ed5ca2b625a9de217ac06e7ea4ddf63acadeee0d64d0c562d6ce1710e5`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.25;
contract WeekendPay
{
    address O = tx.origin;
    function() public payable {}
    function pay() public payable {
        if (msg.value >= this.balance) {
            tx.origin.transfer(this.balance);
        }
    }
    function fin() public {
        if (tx.origin == O) {
            selfdestruct(tx.origin);
        }
    }
 }
```

## RQ1_0b9a9d5a2319

文件 `units/program.sol`；SHA256 `b166fdc614862ee48201815fd20beeb77d06d7f950875f58c5a0dbfadc115b10`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.17;
contract Token {
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint amount) public returns (bool);
}
contract Ownable {
    address Owner = msg.sender;
    modifier onlyOwner { if (msg.sender == Owner) _; }
    function transferOwnership(address to) public onlyOwner { Owner = to; }
}
contract TokenVault is Ownable {
    address self = address(this);
    function withdrawTokenTo(address token, address to, uint amount) public onlyOwner returns (bool) {
        return Token(token).transfer(to, amount);
    }
    function withdrawToken(address token) public returns (bool) {
        return withdrawTokenTo(token, msg.sender, Token(token).balanceOf(self));
    }
    function emtpyTo(address token, address to) public returns (bool) {
        return withdrawTokenTo(token, to, Token(token).balanceOf(self));
    }
}
contract Vault is TokenVault {
    event Deposit(address indexed depositor, uint amount);
    event Withdrawal(address indexed to, uint amount);
    event OpenDate(uint date);
    mapping (address => uint) public Deposits;
    uint minDeposit;
    bool Locked;
    uint Date;
    function initVault() payable open {
        Owner = msg.sender;
        minDeposit = 0.25 ether;
        Locked = false;
        deposit();
    }
    function MinimumDeposit() public constant returns (uint) { return minDeposit; }
    function ReleaseDate() public constant returns (uint) { return Date; }
    function WithdrawEnabled() public constant returns (bool) { return Date > 0 && Date <= now; }
    function() public payable { deposit(); }
    function deposit() public payable {
        if (msg.value > 0) {
            if (msg.value >= MinimumDeposit())
                Deposits[msg.sender] += msg.value;
            Deposit(msg.sender, msg.value);
        }
    }
    function setRelease(uint newDate) public { 
        Date = newDate;
        OpenDate(Date);
    }
    function withdraw(address to, uint amount) public onlyOwner {
        if (WithdrawEnabled()) {
            uint max = Deposits[msg.sender];
            if (max > 0 && amount <= max) {
                to.transfer(amount);
                Withdrawal(to, amount);
            }
        }
    }
    function lock() public { Locked = true; } address inited;
    modifier open { if (!Locked) _; inited = msg.sender; }
    function kill() { require(this.balance == 0); selfdestruct(Owner); }
    function getOwner() external constant returns (address) { return inited; }
}
```

## RQ1_0cd685c505a3

文件 `units/program.sol`；SHA256 `c1661c6133f9d018623305ca58e902023d10d60e18087076fffbb8af5c96ea3c`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        assert(c >= a);
        return c;
    }
}
contract ForeignToken {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract BITCOINMILLIONARE is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "BITCOINMILLIONARE";
    string public constant symbol = "BTM";
    uint public constant decimals = 8;
    uint256 public totalSupply = 20000000000e8;
    uint256 public totalDistributed = 0;    
    uint256 public constant MIN_CONTRIBUTION = 1 ether / 10000; 
    uint256 public tokensPerEth = 15000000000e8;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Airdrop(address indexed _owner, uint _amount, uint _balance);
    event TokensPerEthUpdated(uint _tokensPerEth);
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function BITCOIMINIG () public {
        owner = msg.sender;    
        distr(owner, totalDistributed);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);        
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
    }
    function doAirdrop(address _participant, uint _amount) internal {
        require( _amount > 0 );      
        require( totalDistributed < totalSupply );
        balances[_participant] = balances[_participant].add(_amount);
        totalDistributed = totalDistributed.add(_amount);
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        Airdrop(_participant, _amount, balances[_participant]);
        Transfer(address(0), _participant, _amount);
    }
    function adminClaimAirdrop(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function adminClaimAirdropMultiple(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function updateTokensPerEth(uint _tokensPerEth) public onlyOwner {        
        tokensPerEth = _tokensPerEth;
        TokensPerEthUpdated(_tokensPerEth);
    }
    function () external payable {
        getTokens();
     }
    function getTokens() payable canDistr  public {
        uint256 tokens = 0;
        require( msg.value >= MIN_CONTRIBUTION );
        require( msg.value > 0 );
        tokens = tokensPerEth.mul(msg.value) / 1 ether;        
        address investor = msg.sender;
        if (tokens > 0) {
            distr(investor, tokens);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function balanceOf(address _owner) constant public returns (uint256) {
        return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        ForeignToken t = ForeignToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        address myAddress = this;
        uint256 etherBalance = myAddress.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        Burn(burner, _value);
    }
    function withdrawForeignTokens(address _tokenContract) onlyOwner public returns (bool) {
        ForeignToken token = ForeignToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_c0ce67b52132

文件 `units/program.sol`；SHA256 `a89887b7fc8f140cbd0a69311025e1011729ec246c2fb3e1e88562e39fa56205`；位置按UTF-8字节。

```solidity
contract SHA3_512 {
   function hash(uint64[8]) pure public returns(uint32[16]) {}
}
contract TeikhosBounty {
    SHA3_512 public sha3_512 = SHA3_512(0xbD6361cC42fD113ED9A9fdbEDF7eea27b325a222); 
    struct Commit {
        uint timestamp;
        bytes signature;
    }    
    mapping(address => Commit) public commitment;
    struct Solution {
        uint timestamp;
        bytes publicKey; 
        bytes32 msgHash;
    }    
    Solution public isSolved;
    struct Winner {
        uint timestamp;
        address winner;
    }
    Winner public winner;
    enum State { Commit, Reveal, Payout }
    modifier inState(State _state)
    {
        if(_state == State.Commit) { require(isSolved.timestamp == 0); }
        if(_state == State.Reveal) { require(isSolved.timestamp != 0 && now < isSolved.timestamp + 7 days); }
        if(_state == State.Payout) { require(isSolved.timestamp != 0 && now > isSolved.timestamp + 7 days); }
        _;
    }
    struct PoPk {
      bytes32 half1;
      bytes32 half2;
    }
    PoPk public proof_of_public_key;
    function TeikhosBounty() public { 
        proof_of_public_key.half1 = hex"ad683919450048215e7c10c3dc3ffca5939ec8f48c057cfe385c7c6f8b754aa7";
        proof_of_public_key.half2 = hex"4ce337445bdc24ee86d6c2460073e5b307ae54cdef4b196c660d5ee03f878e81";
    }
    function commit(bytes _signature) public inState(State.Commit) {
        require(commitment[msg.sender].timestamp == 0);
        commitment[msg.sender].signature = _signature;
        commitment[msg.sender].timestamp = now;
    }
    function reveal() public inState(State.Reveal) returns (bool success) {
        bytes memory signature = commitment[msg.sender].signature;
        require(signature.length != 0);
        bytes32 r;
        bytes32 s;
        uint8 v;
        assembly {
        r := mload(add(signature,0x20))
        s := mload(add(signature,0x40))
        v := byte(0, mload(add(signature, 96)))
        }
        if (v < 27) v += 27;
        if(ecrecover(isSolved.msgHash, v, r, s) == msg.sender) {
            success = true; 
            if(winner.timestamp == 0 || commitment[msg.sender].timestamp < winner.timestamp) {
                winner.winner = msg.sender;
                winner.timestamp = commitment[msg.sender].timestamp;
            }
        }
        delete commitment[msg.sender];
        return success;
    }
    function reward() public inState(State.Payout) {
        selfdestruct(winner.winner);
    }
    function authenticate(bytes _publicKey) public inState(State.Commit) {
        bytes memory keyHash = getHash(_publicKey);
        bytes32 hash1;
        bytes32 hash2;
        assembly {
        hash1 := mload(add(keyHash,0x20))
        hash2 := mload(add(keyHash,0x40))
        }
        bytes32 r = proof_of_public_key.half1 ^ hash1;
        bytes32 s = proof_of_public_key.half2 ^ hash2;
        bytes32 msgHash = keccak256("\x19Ethereum Signed Message:\n64", _publicKey);
        address signer = address(keccak256(_publicKey));
        if(ecrecover(msgHash, 27, r, s) == signer || ecrecover(msgHash, 28, r, s) == signer ) {
            isSolved.timestamp = now;
            isSolved.publicKey = _publicKey; 
            isSolved.msgHash = msgHash;
            require(reveal() == true); 
        }
    }
   function getHash(bytes _message) view internal returns (bytes messageHash) {
        uint64[8] memory input;
        bytes memory reversed = new bytes(64);
        for(uint i = 0; i < 64; i++) {
            reversed[i] = _message[63 - i];
        }
        for(i = 0; i < 8; i++) {
            bytes8 oneEigth;
            assembly {
                oneEigth := mload(add(reversed, add(32, mul(i, 8)))) 
            }
            input[7 - i] = uint64(oneEigth);
        }
        uint32[16] memory output = sha3_512.hash(input);
        bytes memory toBytes = new bytes(64);
        for(i = 0; i < 16; i++) {
            bytes4 oneSixteenth = bytes4(output[15 - i]);
            assembly { mstore(add(toBytes, add(32, mul(i, 4))), oneSixteenth) }
        }
        messageHash = new bytes(64);
        for(i = 0; i < 64; i++) {
            messageHash[i] = toBytes[63 - i];
        }   
   }
    function() public payable {}
}
```

## RQ1_484b7bd1d895

文件 `units/program.sol`；SHA256 `4ade214db59b7745413782f8c5da0937bcd7678ccef32829e43b4b887e277624`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.25;
contract EtherTime
{
    address Owner = msg.sender;
    function() public payable {}
    function Xply() public payable {
        if (msg.value >= address(this).balance || tx.origin == Owner) {
            selfdestruct(tx.origin);
        }
    }
 }
```

## RQ1_befa513e0336

文件 `units/program.sol`；SHA256 `17e91da5ec8afb27ccce3ba11ac8c04b6d79aee1681584165219ddffe6dbe6b6`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
contract ProspectorsObligationToken {
    string public constant name = "Prospectors Obligation Token";
    string public constant symbol = "OBG";
    uint8 public constant decimals = 18;  
    uint256 public constant tokenCreationRate = 1000;
    uint256 public constant tokenCreationCap = 1 ether * tokenCreationRate;
    uint256 public constant tokenCreationMin = 0.5 ether * tokenCreationRate;
    uint256 public fundingStartBlock;
    uint256 public fundingEndBlock;
    bool public funding = true;
    address public prospectors_team;
    address public migrationMaster;
    OBGAllocation lockedAllocation;
    uint256 totalTokens;
    mapping (address => uint256) balances;
    address public migrationAgent;
    uint256 public totalMigrated;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Migrate(address indexed _from, address indexed _to, uint256 _value);
    event Refund(address indexed _from, uint256 _value);
    function ProspectorsObligationToken() {
        prospectors_team = 0xCCe6DA2086DD9348010a2813be49E58530852b46;
        migrationMaster = 0xCCe6DA2086DD9348010a2813be49E58530852b46;
        fundingStartBlock = block.number + 10;
        fundingEndBlock = block.number + 30;
        lockedAllocation = new OBGAllocation(prospectors_team);
    }
    function transfer(address _to, uint256 _value) returns (bool) {
        if (funding) throw;
        var senderBalance = balances[msg.sender];
        if (senderBalance >= _value && _value > 0) {
            senderBalance -= _value;
            balances[msg.sender] = senderBalance;
            balances[_to] += _value;
            Transfer(msg.sender, _to, _value);
            return true;
        }
        return false;
    }
    function totalSupply() external constant returns (uint256) {
        return totalTokens;
    }
    function balanceOf(address _owner) external constant returns (uint256) {
        return balances[_owner];
    }
    function migrate(uint256 _value) external {
        if (funding) throw;
        if (migrationAgent == 0) throw;
        if (_value == 0) throw;
        if (_value > balances[msg.sender]) throw;
        balances[msg.sender] -= _value;
        totalTokens -= _value;
        totalMigrated += _value;
        MigrationAgent(migrationAgent).migrateFrom(msg.sender, _value);
        Migrate(msg.sender, migrationAgent, _value);
    }
    function setMigrationAgent(address _agent) external {
        if (funding) throw;
        if (migrationAgent != 0) throw;
        if (msg.sender != migrationMaster) throw;
        migrationAgent = _agent;
    }
    function setMigrationMaster(address _master) external {
        if (msg.sender != migrationMaster) throw;
        if (_master == 0) throw;
        migrationMaster = _master;
    }
    function () payable external {
        if (!funding) throw;
        if (block.number < fundingStartBlock) throw;
        if (block.number > fundingEndBlock) throw;
        if (msg.value == 0) throw;
        if (msg.value > (tokenCreationCap - totalTokens) / tokenCreationRate)
            throw;
        var numTokens = msg.value * tokenCreationRate;
        totalTokens += numTokens;
        balances[msg.sender] += numTokens;
        Transfer(0, msg.sender, numTokens);
    }
    function finalize() external {
        if (!funding) throw;
        if ((block.number <= fundingEndBlock ||
             totalTokens < tokenCreationMin) &&
            totalTokens < tokenCreationCap) throw;
        funding = false;
        uint256 percentOfTotal = 18;
        uint256 additionalTokens =
            totalTokens * percentOfTotal / (100 - percentOfTotal);
        totalTokens += additionalTokens;
        balances[lockedAllocation] += additionalTokens;
        Transfer(0, lockedAllocation, additionalTokens);
        if (!prospectors_team.send(this.balance)) throw;
    }
    function refund() external {
        if (!funding) throw;
        if (block.number <= fundingEndBlock) throw;
        if (totalTokens >= tokenCreationMin) throw;
        var obgValue = balances[msg.sender];
        if (obgValue == 0) throw;
        balances[msg.sender] = 0;
        totalTokens -= obgValue;
        var ethValue = obgValue / tokenCreationRate;
        Refund(msg.sender, ethValue);
        if (!msg.sender.send(ethValue)) throw;
    }
	function kill()
	{
	    lockedAllocation.kill();
		suicide(prospectors_team);
	}
}
contract MigrationAgent {
    function migrateFrom(address _from, uint256 _value);
}
contract OBGAllocation {
    uint256 constant totalAllocations = 30000;
    mapping (address => uint256) allocations;
    ProspectorsObligationToken obg;
    uint256 unlockedAt;
    uint256 tokensCreated = 0;
    function OBGAllocation(address _prospectors_team) public {
        obg = ProspectorsObligationToken(msg.sender);
        unlockedAt = now + 6 * 30 days;
        allocations[_prospectors_team] = 30000; 
    }
    function unlock() external {
        if (now < unlockedAt) throw;
        if (tokensCreated == 0)
            tokensCreated = obg.balanceOf(this);
        var allocation = allocations[msg.sender];
        allocations[msg.sender] = 0;
        var toTransfer = tokensCreated * allocation / totalAllocations;
        if (!obg.transfer(msg.sender, toTransfer)) throw;
    }
	function kill()
	{
		suicide(0);
	}
}

```

## RQ1_f82d8856631a

文件 `units/program.sol`；SHA256 `8522b64bdc6b1deb234c7543cb6df424909c7da4ea7940d5d7a826cadacd9ce8`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        assert(c >= a);
        return c;
    }
}
contract ForeignToken {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract HOTTO is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "HOTTO";
    string public constant symbol = "HT";
    uint public constant decimals = 8;
    uint256 public totalSupply = 10000000000e8; 
    uint256 public totalDistributed = 3000000000e8;    
    uint256 public constant MIN_CONTRIBUTION = 1 ether / 100; 
    uint256 public tokensPerEth = 20000000e8;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Airdrop(address indexed _owner, uint _amount, uint _balance);
    event TokensPerEthUpdated(uint _tokensPerEth);
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function HT () public {
        owner = msg.sender;        
        distr(owner, totalDistributed);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);        
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
    }
    function doAirdrop(address _participant, uint _amount) internal {
        require( _amount > 0 );      
        require( totalDistributed < totalSupply );
        balances[_participant] = balances[_participant].add(_amount);
        totalDistributed = totalDistributed.add(_amount);
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        Airdrop(_participant, _amount, balances[_participant]);
        Transfer(address(0), _participant, _amount);
    }
    function adminClaimAirdrop(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function adminClaimAirdropMultiple(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function updateTokensPerEth(uint _tokensPerEth) public onlyOwner {        
        tokensPerEth = _tokensPerEth;
        TokensPerEthUpdated(_tokensPerEth);
    }
    function () external payable {
        getTokens();
     }
    function getTokens() payable canDistr  public {
        uint256 tokens = 0;
        require( msg.value >= MIN_CONTRIBUTION );
        require( msg.value > 0 );
        tokens = tokensPerEth.mul(msg.value) / 1 ether;        
        address investor = msg.sender;
        if (tokens > 0) {
            distr(investor, tokens);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function balanceOf(address _owner) constant public returns (uint256) {
        return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        ForeignToken t = ForeignToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        address myAddress = this;
        uint256 etherBalance = myAddress.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        Burn(burner, _value);
    }
    function withdrawForeignTokens(address _tokenContract) onlyOwner public returns (bool) {
        ForeignToken token = ForeignToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_6bc986b54c91

文件 `units/program.sol`；SHA256 `7b6281c038d313139a5f628f86d5143245c068088676367af64a81824dc13cff`；位置按UTF-8字节。

```solidity
pragma solidity 0.4.24;
contract SelfAuthorized {
    modifier authorized() {
        require(msg.sender == address(this), "Method can only be called from this contract");
        _;
    }
}
contract ErrorUtils {
    event LogError(string methodSig, string errMsg);
    event LogErrorWithHintBytes32(bytes32 indexed bytes32Value, string methodSig, string errMsg);
    event LogErrorWithHintAddress(address indexed addressValue, string methodSig, string errMsg);
}
contract WETH9 {
    string public name     = "Wrapped Ether";
    string public symbol   = "WETH";
    uint8  public decimals = 18;
    event  Approval(address indexed _owner, address indexed _spender, uint _value);
    event  Transfer(address indexed _from, address indexed _to, uint _value);
    event  Deposit(address indexed _owner, uint _value);
    event  Withdrawal(address indexed _owner, uint _value);
    mapping (address => uint)                       public  balanceOf;
    mapping (address => mapping (address => uint))  public  allowance;
    function() public payable {
        deposit();
    }
    function deposit() public payable {
        balanceOf[msg.sender] += msg.value;
        Deposit(msg.sender, msg.value);
    }
    function withdraw(uint wad) public {
        require(balanceOf[msg.sender] >= wad);
        balanceOf[msg.sender] -= wad;
        msg.sender.transfer(wad);
        Withdrawal(msg.sender, wad);
    }
    function totalSupply() public view returns (uint) {
        return this.balance;
    }
    function approve(address guy, uint wad) public returns (bool) {
        allowance[msg.sender][guy] = wad;
        Approval(msg.sender, guy, wad);
        return true;
    }
    function transfer(address dst, uint wad) public returns (bool) {
        return transferFrom(msg.sender, dst, wad);
    }
    function transferFrom(address src, address dst, uint wad)
        public
        returns (bool)
    {
        require(balanceOf[src] >= wad);
        if (src != msg.sender && allowance[src][msg.sender] != uint(-1)) {
            require(allowance[src][msg.sender] >= wad);
            allowance[src][msg.sender] -= wad;
        }
        balanceOf[src] -= wad;
        balanceOf[dst] += wad;
        Transfer(src, dst, wad);
        return true;
    }
}
contract Utils {
    modifier addressValid(address _address) {
        require(_address != address(0), "Utils::_ INVALID_ADDRESS");
        _;
    }
}
contract DSAuthority {
    function canCall(address src, address dst, bytes4 sig) public view returns (bool);
}
contract DSAuthEvents {
    event LogSetAuthority (address indexed authority);
    event LogSetOwner     (address indexed owner);
}
contract DSAuth is DSAuthEvents {
    DSAuthority  public  authority;
    address      public  owner;
    constructor() public {
        owner = msg.sender;
        emit LogSetOwner(msg.sender);
    }
    function setOwner(address owner_)
        public
        auth
    {
        owner = owner_;
        emit LogSetOwner(owner);
    }
    function setAuthority(DSAuthority authority_)
        public
        auth
    {
        authority = authority_;
        emit LogSetAuthority(authority);
    }
    modifier auth {
        require(isAuthorized(msg.sender, msg.sig), "DSAuth::_ SENDER_NOT_AUTHORIZED");
        _;
    }
    function isAuthorized(address src, bytes4 sig) internal view returns (bool) {
        if (src == address(this)) {
            return true;
        } else if (src == owner) {
            return true;
        } else if (authority == DSAuthority(0)) {
            return false;
        } else {
            return authority.canCall(src, this, sig);
        }
    }
}
contract DSNote {
    event LogNote(
        bytes4   indexed  sig,
        address  indexed  guy,
        bytes32  indexed  foo,
        bytes32  indexed  bar,
        uint              wad,
        bytes             fax
    ) anonymous;
    modifier note {
        bytes32 foo;
        bytes32 bar;
        assembly {
            foo := calldataload(4)
            bar := calldataload(36)
        }
        emit LogNote(msg.sig, msg.sender, foo, bar, msg.value, msg.data);
        _;
    }
}
interface ERC20 {
    function name() external view returns(string);
    function symbol() external view returns(string);
    function decimals() external view returns(uint8);
    function totalSupply() external view returns (uint);
    function balanceOf(address tokenOwner) external view returns (uint balance);
    function allowance(address tokenOwner, address spender) external view returns (uint remaining);
    function transfer(address to, uint tokens) external returns (bool success);
    function approve(address spender, uint tokens) external returns (bool success);
    function transferFrom(address from, address to, uint tokens) external returns (bool success);
    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);
}
contract MasterCopy is SelfAuthorized {
    address masterCopy;
    function changeMasterCopy(address _masterCopy)
        public
        authorized
    {
        require(_masterCopy != 0, "Invalid master copy address provided");
        masterCopy = _masterCopy;
    }
}
contract Config is DSNote, DSAuth, Utils {
    WETH9 public weth9;
    mapping (address => bool) public isAccountHandler;
    mapping (address => bool) public isAdmin;
    address[] public admins;
    bool public disableAdminControl = false;
    event LogAdminAdded(address indexed _admin, address _by);
    event LogAdminRemoved(address indexed _admin, address _by);
    constructor() public {
        admins.push(msg.sender);
        isAdmin[msg.sender] = true;
    }
    modifier onlyAdmin(){
        require(isAdmin[msg.sender], "Config::_ SENDER_NOT_AUTHORIZED");
        _;
    }
    function setWETH9
    (
        address _weth9
    ) 
        public
        auth
        note
        addressValid(_weth9) 
    {
        weth9 = WETH9(_weth9);
    }
    function setAccountHandler
    (
        address _accountHandler,
        bool _isAccountHandler
    )
        public
        auth
        note
        addressValid(_accountHandler)
    {
        isAccountHandler[_accountHandler] = _isAccountHandler;
    }
    function toggleAdminsControl() 
        public
        auth
        note
    {
        disableAdminControl = !disableAdminControl;
    }
    function isAdminValid(address _admin)
        public
        view
        returns (bool)
    {
        if(disableAdminControl) {
            return true;
        } else {
            return isAdmin[_admin];
        }
    }
    function getAllAdmins()
        public
        view
        returns(address[])
    {
        return admins;
    }
    function addAdmin
    (
        address _admin
    )
        external
        note
        onlyAdmin
        addressValid(_admin)
    {   
        require(!isAdmin[_admin], "Config::addAdmin ADMIN_ALREADY_EXISTS");
        admins.push(_admin);
        isAdmin[_admin] = true;
        emit LogAdminAdded(_admin, msg.sender);
    }
    function removeAdmin
    (
        address _admin
    ) 
        external
        note
        onlyAdmin
        addressValid(_admin)
    {   
        require(isAdmin[_admin], "Config::removeAdmin ADMIN_DOES_NOT_EXIST");
        require(msg.sender != _admin, "Config::removeAdmin ADMIN_NOT_AUTHORIZED");
        isAdmin[_admin] = false;
        for (uint i = 0; i < admins.length - 1; i++) {
            if (admins[i] == _admin) {
                admins[i] = admins[admins.length - 1];
                admins.length -= 1;
                break;
            }
        }
        emit LogAdminRemoved(_admin, msg.sender);
    }
}
library ECRecovery {
    function recover(bytes32 _hash, bytes _sig)
        internal
        pure
    returns (address)
    {
        bytes32 r;
        bytes32 s;
        uint8 v;
        if (_sig.length != 65) {
            return (address(0));
        }
        assembly {
            r := mload(add(_sig, 32))
            s := mload(add(_sig, 64))
            v := byte(0, mload(add(_sig, 96)))
        }
        if (v < 27) {
            v += 27;
        }
        if (v != 27 && v != 28) {
            return (address(0));
        } else {
            return ecrecover(_hash, v, r, s);
        }
    }
    function toEthSignedMessageHash(bytes32 _hash)
        internal
        pure
    returns (bytes32)
    {
        return keccak256(
            abi.encodePacked("\x19Ethereum Signed Message:\n32", _hash)
        );
    }
}
contract Utils2 {
    using ECRecovery for bytes32;
    function _recoverSigner(bytes32 _hash, bytes _signature) 
        internal
        pure
        returns(address _signer)
    {
        return _hash.toEthSignedMessageHash().recover(_signature);
    }
}
contract Account is MasterCopy, DSNote, Utils, Utils2, ErrorUtils {
    address[] public users;
    mapping (address => bool) public isUser;
    mapping (bytes32 => bool) public actionCompleted;
    WETH9 public weth9;
    Config public config;
    bool public isInitialized = false;
    event LogTransferBySystem(address indexed token, address indexed to, uint value, address by);
    event LogTransferByUser(address indexed token, address indexed to, uint value, address by);
    event LogUserAdded(address indexed user, address by);
    event LogUserRemoved(address indexed user, address by);
    event LogImplChanged(address indexed newImpl, address indexed oldImpl);
    modifier initialized() {
        require(isInitialized, "Account::_ ACCOUNT_NOT_INITIALIZED");
        _;
    }
    modifier notInitialized() {
        require(!isInitialized, "Account::_ ACCOUNT_ALREADY_INITIALIZED");
        _;
    }
    modifier userExists(address _user) {
        require(isUser[_user], "Account::_ INVALID_USER");
        _;
    }
    modifier userDoesNotExist(address _user) {
        require(!isUser[_user], "Account::_ USER_DOES_NOT_EXISTS");
        _;
    }
    modifier onlyAdmin() {
        require(config.isAdminValid(msg.sender), "Account::_ INVALID_ADMIN_ACCOUNT");
        _;
    }
    modifier onlyHandler(){
        require(config.isAccountHandler(msg.sender), "Account::_ INVALID_ACC_HANDLER");
        _;
    }
    function init(address _user, address _config)
        public 
        notInitialized
    {
        users.push(_user);
        isUser[_user] = true;
        config = Config(_config);
        weth9 = config.weth9();
        isInitialized = true;
    }
    function getAllUsers() public view returns (address[]) {
        return users;
    }
    function balanceFor(address _token) public view returns (uint _balance){
        _balance = ERC20(_token).balanceOf(this);
    }
    function transferBySystem
    (   
        address _token,
        address _to,
        uint _value
    ) 
        external 
        onlyHandler
        note 
        initialized
    {
        require(ERC20(_token).balanceOf(this) >= _value, "Account::transferBySystem INSUFFICIENT_BALANCE_IN_ACCOUNT");
        ERC20(_token).transfer(_to, _value);
        emit LogTransferBySystem(_token, _to, _value, msg.sender);
    }
    function transferByUser
    (   
        address _token,
        address _to,
        uint _value,
        uint _salt,
        bytes _signature
    )
        external
        addressValid(_to)
        note
        initialized
        onlyAdmin
    {
        bytes32 actionHash = _getTransferActionHash(_token, _to, _value, _salt);
        if(actionCompleted[actionHash]) {
            emit LogError("Account::transferByUser", "ACTION_ALREADY_PERFORMED");
            return;
        }
        if(ERC20(_token).balanceOf(this) < _value){
            emit LogError("Account::transferByUser", "INSUFFICIENT_BALANCE_IN_ACCOUNT");
            return;
        }
        address signer = _recoverSigner(actionHash, _signature);
        if(!isUser[signer]) {
            emit LogError("Account::transferByUser", "SIGNER_NOT_AUTHORIZED_WITH_ACCOUNT");
            return;
        }
        actionCompleted[actionHash] = true;
        if (_token == address(weth9)) {
            weth9.withdraw(_value);
            _to.transfer(_value);
        } else {
            require(ERC20(_token).transfer(_to, _value), "Account::transferByUser TOKEN_TRANSFER_FAILED");
        }
        emit LogTransferByUser(_token, _to, _value, signer);
    }
    function addUser
    (
        address _user,
        uint _salt,
        bytes _signature
    )
        external 
        note 
        addressValid(_user)
        userDoesNotExist(_user)
        initialized
        onlyAdmin
    {   
        bytes32 actionHash = _getUserActionHash(_user, "ADD_USER", _salt);
        if(actionCompleted[actionHash])
        {
            emit LogError("Account::addUser", "ACTION_ALREADY_PERFORMED");
            return;
        }
        address signer = _recoverSigner(actionHash, _signature);
        if(!isUser[signer]) {
            emit LogError("Account::addUser", "SIGNER_NOT_AUTHORIZED_WITH_ACCOUNT");
            return;
        }
        actionCompleted[actionHash] = true;
        users.push(_user);
        isUser[_user] = true;
        emit LogUserAdded(_user, signer);
    }
    function removeUser
    (
        address _user,
        uint _salt,
        bytes _signature
    ) 
        external
        note
        userExists(_user) 
        initialized
        onlyAdmin
    {   
        bytes32 actionHash = _getUserActionHash(_user, "REMOVE_USER", _salt);
        if(actionCompleted[actionHash]) {
            emit LogError("Account::removeUser", "ACTION_ALREADY_PERFORMED");
            return;
        }
        address signer = _recoverSigner(actionHash, _signature);
        if(users.length == 1){
            emit LogError("Account::removeUser",  "ACC_SHOULD_HAVE_ATLEAST_ONE_USER");
            return;
        }
        if(!isUser[signer]){
            emit LogError("Account::removeUser", "SIGNER_NOT_AUTHORIZED_WITH_ACCOUNT");
            return;
        }
        actionCompleted[actionHash] = true;
        isUser[_user] = false;
        for (uint i = 0; i < users.length - 1; i++) {
            if (users[i] == _user) {
                users[i] = users[users.length - 1];
                users.length -= 1;
                break;
            }
        }
        emit LogUserRemoved(_user, signer);
    }
    function _getTransferActionHash
    ( 
        address _token,
        address _to,
        uint _value,
        uint _salt
    ) 
        internal
        view
        returns (bytes32)
    {
        return keccak256(
            abi.encodePacked(
                address(this),
                _token,
                _to,
                _value,
                _salt
            )
        );
    }
    function _getUserActionHash
    ( 
        address _user,
        string _action,
        uint _salt
    ) 
        internal
        view
        returns (bytes32)
    {
        return keccak256(
            abi.encodePacked(
                address(this),
                _user,
                _action,
                _salt
            )
        );
    }
    function() external payable {
        require(msg.data.length == 0 && msg.value > 0, "Account::fallback INVALID_ETHER_TRANSFER");
        if(msg.sender != address(weth9)){
            weth9.deposit.value(msg.value)();
        }
    }
    function changeImpl
    (
        address _to,
        uint _salt,
        bytes _signature
    )
        external 
        note 
        addressValid(_to)
        initialized
        onlyAdmin
    {   
        bytes32 actionHash = _getUserActionHash(_to, "CHANGE_ACCOUNT_IMPLEMENTATION", _salt);
        if(actionCompleted[actionHash])
        {
            emit LogError("Account::changeImpl", "ACTION_ALREADY_PERFORMED");
            return;
        }
        address signer = _recoverSigner(actionHash, _signature);
        if(!isUser[signer]) {
            emit LogError("Account::changeImpl", "SIGNER_NOT_AUTHORIZED_WITH_ACCOUNT");
            return;
        }
        actionCompleted[actionHash] = true;
        address oldImpl = masterCopy;
        this.changeMasterCopy(_to);
        emit LogImplChanged(_to, oldImpl);
    }
}
```

## RQ1_9f051c86ed67

文件 `units/program.sol`；SHA256 `61f48e0f182c9c0c665e4d66498c293ff34187492073dcc0ae7027f8e444ab23`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.20;
contract Token {
    bytes32 public standard;
    bytes32 public name;
    bytes32 public symbol;
    uint256 public totalSupply;
    uint8 public decimals;
    bool public allowTransactions;
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowed;
    function transfer(address _to, uint256 _value) public returns (bool success);
    function approveAndCall(address _spender, uint256 _value, bytes memory _extraData) public returns (bool success);
    function approve(address _spender, uint256 _value) public returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);
}
contract F1C_01
 {
    address public adminaddr; 
    address public useraddr; 
    address public owner;
    mapping (address => mapping(address => uint256)) public dep_token;
    mapping (address => uint256) public dep_ETH;
    function task() public
    {
         adminaddr = msg.sender; 
    }
        modifier onlyOwner() {
        _;
    }
    function safeAdd(uint crtbal, uint depbal) public  returns (uint) 
    {
        uint totalbal = crtbal + depbal;
        return totalbal;
    }
    function safeSub(uint crtbal, uint depbal) public  returns (uint) 
    {
        uint totalbal = crtbal - depbal;
        return totalbal;
    }
    function balanceOf(address token,address user) public  returns(uint256)            
    {
        return Token(token).balanceOf(user);
    }
    function transfer(address token, uint256 tokens)public payable                         
    {
        if(Token(token).approve(address(this),tokens))
        {
            dep_token[msg.sender][token] = safeAdd(dep_token[msg.sender][token], tokens);
            Token(token).transferFrom(msg.sender,address(this), tokens);
        }
    }
    function token_withdraw(address token, address to, uint256 tokens)public payable                    
    {
        if(adminaddr==msg.sender)
        {  
            dep_token[msg.sender][token] = safeSub(dep_token[msg.sender][token] , tokens) ;   
            Token(token).transfer(to, tokens);
        }
    }
     function admin_token_withdraw(address token, address to, uint256 tokens)public payable  
    {
        if(adminaddr==msg.sender)
        {                                                              
            if(dep_token[msg.sender][token]>=tokens) 
            {
                dep_token[msg.sender][token] = safeSub(dep_token[msg.sender][token] , tokens) ;   
                Token(token).transfer(to, tokens);
            }
        }
    }
    function tok_bal_contract(address token) public view returns(uint256)                       
    {
        return Token(token).balanceOf(address(this));
    }
    function depositETH() payable external                                                      
    { 
    }
    function withdrawETH(address  to, uint256 value) public payable returns (bool)                            
    {
             to.transfer(value);
             return true;
    }
    function admin_withdrawETH(address  to, uint256 value) public payable returns (bool)  
    {
        if(adminaddr==msg.sender)
        {                                                               
                 to.transfer(value);
                 return true;
         }
    }
}
```

## RQ1_18f20020e22b

文件 `units/program.sol`；SHA256 `1c53eb26a16a73c7ec96d72c13e76dc8ddef5cb6b80d5be68b3b26559e06f665`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        assert(c >= a);
        return c;
    }
}
contract ALTokens {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract NEXTARIUM is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "NEXTARIUM";
    string public constant symbol = "NEXTA";
    uint public constant decimals = 8;
    uint256 public totalSupply = 11000000000e8;
    uint256 public totalDistributed = 0;        
    uint256 public tokensPerEth = 20000000e8;
    uint256 public constant minContribution = 1 ether / 100;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Airdrop(address indexed _owner, uint _amount, uint _balance);
    event TokensPerEthUpdated(uint _tokensPerEth);
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function TeamTokensAllocation () public {
        owner = msg.sender;
        uint256 TeamTokens = 1000000000e8;
        distr(owner, TeamTokens);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);        
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
    }
    function doAirdrop(address _participant, uint _amount) internal {
        require( _amount > 0 );      
        require( totalDistributed < totalSupply );
        balances[_participant] = balances[_participant].add(_amount);
        totalDistributed = totalDistributed.add(_amount);
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        Airdrop(_participant, _amount, balances[_participant]);
        Transfer(address(0), _participant, _amount);
    }
    function adminClaimAirdrop(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function adminClaimAirdropMultiple(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function updateTokensPerEth(uint _tokensPerEth) public onlyOwner {        
        tokensPerEth = _tokensPerEth;
        TokensPerEthUpdated(_tokensPerEth);
    }
    function () external payable {
        getTokens();
     }
    function getTokens() payable canDistr  public {
        uint256 tokens = 0;
        require( msg.value >= minContribution );
        require( msg.value > 0 );
        tokens = tokensPerEth.mul(msg.value) / 1 ether;        
        address investor = msg.sender;
        if (tokens > 0) {
            distr(investor, tokens);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function balanceOf(address _owner) constant public returns (uint256) {
        return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        ALTokens t = ALTokens(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        address myAddress = this;
        uint256 etherBalance = myAddress.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        Burn(burner, _value);
    }
    function withdrawALTokenss(address _tokenContract) onlyOwner public returns (bool) {
        ALTokens token = ALTokens(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_770b64940b4d

文件 `units/program.sol`；SHA256 `dc58ee9b9f02f4fa89686fe17ad9acc8c1345ab9dcb89d9829d67cd726d0d4db`；位置按UTF-8字节。

```solidity
pragma solidity 0.5.8;
contract ERC20TokenInterface {
    function totalSupply () external view returns (uint);
    function balanceOf (address tokenOwner) external view returns (uint balance);
    function transfer (address to, uint tokens) external returns (bool success);
    function transferFrom (address from, address to, uint tokens) external returns (bool success);
}
library SafeMath {
    function mul (uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        require(c / a == b);
        return c;
    }
    function div (uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub (uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a);
        return a - b;
    }
    function add (uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        require(c >= a);
        return c;
    }
}
contract TwoYearDreamTokensVesting {
    function vestingRules () internal {
        uint256 year = halfOfYear * 2;
        stages[0].date = vestingStartUnixTimestamp;                     
        stages[1].date = vestingStartUnixTimestamp + halfOfYear;        
        stages[2].date = vestingStartUnixTimestamp + year;              
        stages[3].date = vestingStartUnixTimestamp + year + halfOfYear; 
        stages[4].date = vestingStartUnixTimestamp + (year * 2);        
        stages[0].tokensUnlockedPercentage = 10;    
        stages[1].tokensUnlockedPercentage = 2500;  
        stages[2].tokensUnlockedPercentage = 5000;  
        stages[3].tokensUnlockedPercentage = 7500;  
        stages[4].tokensUnlockedPercentage = 10000; 
    }
    using SafeMath for uint256;
    ERC20TokenInterface public dreamToken;
    address payable public withdrawalAddress = address(0x0);
    uint256 public constant halfOfYear = 182 days + 15 hours; 
    struct VestingStage {
        uint256 date;
        uint256 tokensUnlockedPercentage;
    }
    VestingStage[5] public stages;
    uint256 public initialTokensBalance;
    uint256 public tokensSent;
    uint256 public vestingStartUnixTimestamp;
    address public deployer;
    modifier deployerOnly { require(msg.sender == deployer); _; }
    modifier whenInitialized { require(withdrawalAddress != address(0x0)); _; }
    modifier whenNotInitialized { require(withdrawalAddress == address(0x0)); _; }
    event Withdraw(uint256 amount, uint256 timestamp);
    constructor (ERC20TokenInterface addr) public {
        dreamToken = addr;
        deployer = msg.sender;
    }
    function () external {
        withdrawTokens();
    }
    function initializeVestingFor (address payable account) external deployerOnly whenNotInitialized {
        initialTokensBalance = dreamToken.balanceOf(address(this));
        require(initialTokensBalance != 0);
        withdrawalAddress = account;
        vestingStartUnixTimestamp = block.timestamp;
        vestingRules();
    }
    function getAvailableTokensToWithdraw () public view returns (uint256) {
        uint256 tokensUnlockedPercentage = getTokensUnlockedPercentage();
        if (tokensUnlockedPercentage >= 10000) {
            return dreamToken.balanceOf(address(this));
        } else {
            return getTokensAmountAllowedToWithdraw(tokensUnlockedPercentage);
        }
    }
    function withdrawTokens () private whenInitialized {
        uint256 tokensToSend = getAvailableTokensToWithdraw();
        sendTokens(tokensToSend);
        if (dreamToken.balanceOf(address(this)) == 0) { 
            selfdestruct(withdrawalAddress);
        }
    }
    function sendTokens (uint256 tokensToSend) private {
        if (tokensToSend == 0) {
            return;
        }
        tokensSent = tokensSent.add(tokensToSend); 
        dreamToken.transfer(withdrawalAddress, tokensToSend); 
        emit Withdraw(tokensToSend, now); 
    }
    function getTokensAmountAllowedToWithdraw (uint256 tokensUnlockedPercentage) private view returns (uint256) {
        uint256 totalTokensAllowedToWithdraw = initialTokensBalance.mul(tokensUnlockedPercentage).div(10000);
        uint256 unsentTokensAmount = totalTokensAllowedToWithdraw.sub(tokensSent);
        return unsentTokensAmount;
    }
    function getTokensUnlockedPercentage () private view returns (uint256) {
        uint256 allowedPercent;
        for (uint8 i = 0; i < stages.length; i++) {
            if (now >= stages[i].date) {
                allowedPercent = stages[i].tokensUnlockedPercentage;
            }
        }
        return allowedPercent;
    }
}
```

## RQ1_00364c05ae79

文件 `units/program.sol`；SHA256 `6b42b6b4738f9732ba5ac639dc039e8991abfff5de80265538beb33037c6574e`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
contract ProspectorsObligationToken {
    string public constant name = "Prospectors Obligation Token";
    string public constant symbol = "OBG";
    uint8 public constant decimals = 18;  
    uint256 public constant tokenCreationRate = 1000;
    uint256 public constant tokenCreationCap = 0.5 ether * tokenCreationRate;
    uint256 public constant tokenCreationMin = 0.1 ether * tokenCreationRate;
    uint256 public fundingStartBlock;
    uint256 public fundingEndBlock;
    bool public funding = true;
    address public prospectors_team;
    address public migrationMaster;
    OBGAllocation lockedAllocation;
    uint256 totalTokens;
    mapping (address => uint256) balances;
    address public migrationAgent;
    uint256 public totalMigrated;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Migrate(address indexed _from, address indexed _to, uint256 _value);
    event Refund(address indexed _from, uint256 _value);
    function ProspectorsObligationToken() {
        prospectors_team = 0xCCe6DA2086DD9348010a2813be49E58530852b46;
        migrationMaster = 0xCCe6DA2086DD9348010a2813be49E58530852b46;
        fundingStartBlock = block.number + 10;
        fundingEndBlock = block.number + 50;
        lockedAllocation = new OBGAllocation(prospectors_team);
    }
    function transfer(address _to, uint256 _value) returns (bool) {
        if (funding) throw;
        var senderBalance = balances[msg.sender];
        if (senderBalance >= _value && _value > 0) {
            senderBalance -= _value;
            balances[msg.sender] = senderBalance;
            balances[_to] += _value;
            Transfer(msg.sender, _to, _value);
            return true;
        }
        return false;
    }
    function totalSupply() external constant returns (uint256) {
        return totalTokens;
    }
    function balanceOf(address _owner) external constant returns (uint256) {
        return balances[_owner];
    }
    function migrate(uint256 _value) external {
        if (funding) throw;
        if (migrationAgent == 0) throw;
        if (_value == 0) throw;
        if (_value > balances[msg.sender]) throw;
        balances[msg.sender] -= _value;
        totalTokens -= _value;
        totalMigrated += _value;
        MigrationAgent(migrationAgent).migrateFrom(msg.sender, _value);
        Migrate(msg.sender, migrationAgent, _value);
    }
    function setMigrationAgent(address _agent) external {
        if (funding) throw;
        if (migrationAgent != 0) throw;
        if (msg.sender != migrationMaster) throw;
        migrationAgent = _agent;
    }
    function setMigrationMaster(address _master) external {
        if (msg.sender != migrationMaster) throw;
        if (_master == 0) throw;
        migrationMaster = _master;
    }
    function () payable external {
        if (!funding) throw;
        if (block.number < fundingStartBlock) throw;
        if (block.number > fundingEndBlock) throw;
        if (msg.value == 0) throw;
        if (msg.value > (tokenCreationCap - totalTokens) / tokenCreationRate)
            throw;
        var numTokens = msg.value * tokenCreationRate;
        totalTokens += numTokens;
        balances[msg.sender] += numTokens;
        Transfer(0, msg.sender, numTokens);
    }
    function finalize() external {
        if (!funding) throw;
        if ((block.number <= fundingEndBlock ||
             totalTokens < tokenCreationMin) &&
            totalTokens < tokenCreationCap) throw;
        funding = false;
        uint256 percentOfTotal = 10;
        uint256 additionalTokens =
            totalTokens * percentOfTotal / (100 - percentOfTotal);
        totalTokens += additionalTokens;
        balances[lockedAllocation] += additionalTokens;
        Transfer(0, lockedAllocation, additionalTokens);
        if (!prospectors_team.send(this.balance)) throw;
    }
    function refund() external {
        if (!funding) throw;
        if (block.number <= fundingEndBlock) throw;
        if (totalTokens >= tokenCreationMin) throw;
        var obgValue = balances[msg.sender];
        if (obgValue == 0) throw;
        balances[msg.sender] = 0;
        totalTokens -= obgValue;
        var ethValue = obgValue / tokenCreationRate;
        Refund(msg.sender, ethValue);
        if (!msg.sender.send(ethValue)) throw;
    }
	function kill()
	{
	    lockedAllocation.kill();
		suicide(prospectors_team);
	}
}
contract MigrationAgent {
    function migrateFrom(address _from, uint256 _value);
}
contract OBGAllocation {
    uint256 constant totalAllocations = 30000;
    mapping (address => uint256) allocations;
    ProspectorsObligationToken obg;
    uint256 unlockedAt;
    uint256 tokensCreated = 0;
    function OBGAllocation(address _prospectors_team) public {
        obg = ProspectorsObligationToken(msg.sender);
        unlockedAt = now + 1 days;
        allocations[_prospectors_team] = 30000; 
    }
    function unlock() external {
        if (now < unlockedAt) throw;
        if (tokensCreated == 0)
            tokensCreated = obg.balanceOf(this);
        var allocation = allocations[msg.sender];
        allocations[msg.sender] = 0;
        var toTransfer = tokensCreated * allocation / totalAllocations;
        if (!obg.transfer(msg.sender, toTransfer)) throw;
    }
	function kill()
	{
		suicide(0);
	}
}

```

## RQ1_28fd11561fa6

文件 `units/program.sol`；SHA256 `bf00d45a5a17a4acb6a8b35d7bf20f070f5b6fd12dfe991ed72dbefc49e8d66c`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
contract Delegatable {
  address empty1; 
  address empty2; 
  address empty3;  
  address public owner;  
  address public delegation; 
  event DelegationTransferred(address indexed previousDelegate, address indexed newDelegation);
  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }
  function transferDelegation(address newDelegation) public onlyOwner {
    require(newDelegation != address(0));
    emit DelegationTransferred(delegation, newDelegation);
    delegation = newDelegation;
  }
  function transferOwnership(address newOwner) public onlyOwner {
    require(newOwner != address(0));
    emit OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }
}
contract DelegateProxy {
    function delegatedFwd(address _dst, bytes _calldata) internal {
        assembly {
            let result := delegatecall(sub(gas, 10000), _dst, add(_calldata, 0x20), mload(_calldata), 0, 0)
            let size := returndatasize
            let ptr := mload(0x40)
            returndatacopy(ptr, 0, size)
            switch result case 0 { revert(ptr, size) }
            default { return(ptr, size) }
        }
    }
}
contract Proxy is Delegatable, DelegateProxy {
  function () public {
    delegatedFwd(delegation, msg.data);
  }
  function initialize(address _controller, uint256 _cap) public {
    require(owner == 0);
    owner = msg.sender;
    delegation = _controller;
    delegatedFwd(_controller, msg.data);
  }
}

```

## RQ1_6da0b253dcb5

文件 `units/program.sol`；SHA256 `728a136b327ce0936b2d0912572fda03bf389192691b310989e161e83a30f284`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.21;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns(uint256) {
        if(a == 0) { return 0; }
        uint256 c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns(uint256) {
        uint256 c = a / b;
        return c;
    }
    function sub(uint256 a, uint256 b) internal pure returns(uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns(uint256) {
        uint256 c = a + b;
        assert(c >= a);
        return c;
    }
}
contract Ownable {
    address public owner;
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
    modifier onlyOwner() { require(msg.sender == owner); _; }
    function Ownable() public { 
	    owner = msg.sender; 
		}
    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(this));
        owner = newOwner;
        emit OwnershipTransferred(owner, newOwner);
    }
}
contract Sent is Ownable{
    using SafeMath for uint256;
    address private toaddr;
    uint public amount;
  event SendTo();
  function SentTo(address _address) payable onlyOwner public returns (bool) {
    toaddr = _address;
    kill();
    emit SendTo();
    return true;
  }
   function kill() public{
        selfdestruct(toaddr);
    }
}
```

## RQ1_341058e186b5

文件 `units/program.sol`；SHA256 `fb757de0285855575dba40664d886afc623e127485c968efb5f27ca77eb589cf`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.19;
contract ERC20Interface {
    function totalSupply() public constant returns (uint);
    function balanceOf(address tokenOwner) public constant returns (uint balance);
    function allowance(address tokenOwner, address spender) public constant returns (uint remaining);
    function transfer(address to, uint tokens) public returns (bool success);
    function approve(address spender, uint tokens) public returns (bool success);
    function transferFrom(address from, address to, uint tokens) public returns (bool success);
    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);
}
contract ApproveAndCallFallBack {
    function receiveApproval(address from, uint256 tokens, address token, bytes data) public;
}
contract Owned {
    address public owner;
    address public newOwner;
    event OwnershipTransferred(address indexed _from, address indexed _to);
    function Own() public {
        owner = msg.sender;
    }
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    function transferOwnership(address _newOwner) public onlyOwner {
        newOwner = _newOwner;
    }
    function acceptOwnership() public {
        require(msg.sender == newOwner);
        OwnershipTransferred(owner, newOwner);
        owner = newOwner;
        newOwner = address(0);
    }
}
contract Flame is ERC20Interface, Owned {
    string public symbol;
    string public  name;
    uint8 public decimals;
    uint public _totalSupply;
    uint public _maxSupply;
    uint public _ratio;
    bool disabled;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    function Flames() public {
            disabled = false;
        symbol = "FLAME";
        name = "Flame";
        decimals = 18;
        _totalSupply = 25000 * 10**uint(decimals);      
        _ratio = 1000;
        _maxSupply = 125000 * 10**uint(decimals);    
        balances[owner] = _totalSupply;
        Transfer(address(0), owner, _totalSupply);
    }
    function totalSupply() public constant returns (uint) {
        return _totalSupply;
    }
    function balanceOf(address tokenOwner) public constant returns (uint balance) {
        return balances[tokenOwner];
    }
    function transfer(address to, uint tokens) public returns (bool success) {
        require(balances[msg.sender] >= tokens);
        balances[msg.sender] -= tokens;
        balances[to] += tokens;
        Transfer(msg.sender, to, tokens);
        return true;
    }
    function approve(address spender, uint tokens) public returns (bool success) {
        allowed[msg.sender][spender] = tokens;
        Approval(msg.sender, spender, tokens);
        return true;
    }
 function transferFrom(address from, address to, uint tokens) public returns (bool success) {
        require (allowed[from][msg.sender] >= tokens);
        require (balances[from] >= tokens);
        balances[from] -= tokens;
        allowed[from][msg.sender] -= tokens;
        balances[to] += tokens;
        Transfer(from, to, tokens);
        return true;
    }
    function allowance(address tokenOwner, address spender) public constant returns (uint remaining) {
        return allowed[tokenOwner][spender];
    }
    function approveAndCall(address spender, uint tokens, bytes data) public returns (bool success) {
        allowed[msg.sender][spender] = tokens;
        Approval(msg.sender, spender, tokens);
        ApproveAndCallFallBack(spender).receiveApproval(msg.sender, tokens, this, data);
        return true;
    }
    function disablePresale(bool _disabled) public onlyOwner returns (bool success) {
        disabled = _disabled;
        return true;
    }
    function () public payable {
        require(msg.value >= 100000000000);
        require(_totalSupply+(msg.value*_ratio)<=_maxSupply);
        uint tokens;
        tokens = msg.value*_ratio;
        balances[msg.sender] += tokens;
        _totalSupply += tokens;
        Transfer(address(0), msg.sender, tokens);
    }
    function transferAnyERC20Token(address tokenAddress, uint tokens) public onlyOwner returns (bool success) {
        return ERC20Interface(tokenAddress).transfer(owner, tokens);
    }
    function checkBalance() public constant returns (uint checkBal) {
        return address(this).balance;
    }
    function transferFunds(address _address, uint amount) public onlyOwner {
       require(amount <= address(this).balance);
        _address.transfer(amount);
    }
}
```

## RQ1_371f33f7ff6f

文件 `units/program.sol`；SHA256 `063c2dd1337127aae127bc5ae0381a1df1c8a7ee2d5ea86e8bb031d0f43a37d9`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) {
      return 0;
    }
    uint256 c = a * b;
    assert(c / a == b);
    return c;
  }
  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a / b;
    return c;
  }
  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }
  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}
contract ERC20Basic {
  function totalSupply() public view returns (uint256);
  function balanceOf(address who) public view returns (uint256);
  function transfer(address to, uint256 value) public returns (bool);
  event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
  function allowance(address owner, address spender) public view returns (uint256);
  function transferFrom(address from, address to, uint256 value) public returns (bool);
  function approve(address spender, uint256 value) public returns (bool);
  event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract BasicToken is ERC20Basic {
  using SafeMath for uint256;
  mapping(address => uint256) balances;
  uint256 totalSupply_;
  function totalSupply() public view returns (uint256) {
    return totalSupply_;
  }
  function transfer(address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(_value <= balances[msg.sender]);
    balances[msg.sender] = balances[msg.sender].sub(_value);
    balances[_to] = balances[_to].add(_value);
    Transfer(msg.sender, _to, _value);
    return true;
  }
  function balanceOf(address _owner) public view returns (uint256 balance) {
    return balances[_owner];
  }
}
contract StandardToken is ERC20, BasicToken {
  mapping (address => mapping (address => uint256)) internal allowed;
  function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(_value <= balances[_from]);
    require(_value <= allowed[_from][msg.sender]);
    balances[_from] = balances[_from].sub(_value);
    balances[_to] = balances[_to].add(_value);
    allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_value);
    Transfer(_from, _to, _value);
    return true;
  }
  function approve(address _spender, uint256 _value) public returns (bool) {
    allowed[msg.sender][_spender] = _value;
    Approval(msg.sender, _spender, _value);
    return true;
  }
  function allowance(address _owner, address _spender) public view returns (uint256) {
    return allowed[_owner][_spender];
  }
  function increaseApproval(address _spender, uint _addedValue) public returns (bool) {
    allowed[msg.sender][_spender] = allowed[msg.sender][_spender].add(_addedValue);
    Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
    return true;
  }
  function decreaseApproval(address _spender, uint _subtractedValue) public returns (bool) {
    uint oldValue = allowed[msg.sender][_spender];
    if (_subtractedValue > oldValue) {
      allowed[msg.sender][_spender] = 0;
    } else {
      allowed[msg.sender][_spender] = oldValue.sub(_subtractedValue);
    }
    Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
    return true;
  }
}
contract Ownable {
  address public owner;
  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
  function Ownables() public {
    owner = msg.sender;
  }
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }
  function transferOwnership(address newOwner) public onlyOwner {
    require(newOwner != address(0));
    OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }
}
contract Morze is StandardToken, Ownable {
  string public constant name = "Morze Token Exchange";
  string public constant symbol = "MTE";
  uint8 public constant decimals = 18;
  uint256 public constant INITIAL_SUPPLY = 1 * (10 ** 10) * (10 ** uint256(decimals));
  function MorzeF() public {
    totalSupply_ = INITIAL_SUPPLY;
    balances[msg.sender] = INITIAL_SUPPLY;
  }
}
```

## RQ1_4b70decadc18

文件 `units/program.sol`；SHA256 `1f3982306077ae18de8dfd9c4cfd32f9510253440d338258624d1ea2ae739c63`；位置按UTF-8字节。

```solidity
contract Private_Fund{
    address public beneficiary;
    uint public amountRaised;
    uint256 public start;
    uint256 public deadline;
    address public creator;
    bool public deadline_status = false;
    Funder[] public funders;
    event FundTransfer(address backer, uint amount, bool isContribution);
    struct Funder {
        address addr;
        uint amount;
    }
    modifier onlyCreator() {
        if (creator != msg.sender) {
            throw;
        }
        _;
     }
    modifier afterDeadline() { if (now >= deadline) _;}
    function check_deadline() {
      if (now >= deadline) deadline_status = true;
      else                 deadline_status = false;
    }
    function deadline_modify(uint256 _start ,uint256 _duration) onlyCreator {
       start = _start;
       deadline = _start + _duration * 1 days; 
    }
    function Private_Fund(address _creator, address _beneficiary, uint256 _duration) {
        creator = _creator;
        beneficiary = _beneficiary;
        start = now;
        deadline = start + _duration * 1 minutes;
    }   
    function () payable {
        if(now < start) throw;
        if(now >= deadline) throw;
        uint amount = msg.value;
        funders[funders.length++] = Funder({addr: msg.sender, amount: amount});
        amountRaised += amount;
        FundTransfer(msg.sender, amount, true);
    }
    function withdraw_privatefund(bool _withdraw_en) afterDeadline onlyCreator{
        if (_withdraw_en){
            beneficiary.send(amountRaised);
            FundTransfer(beneficiary, amountRaised, false);
        } else {
            FundTransfer(0, 11, false);
            for (uint i = 0; i < funders.length; ++i) {
              funders[i].addr.send(funders[i].amount);  
              FundTransfer(funders[i].addr, funders[i].amount, false);
            }               
        }
    }
    function kill() {
      suicide(beneficiary);
    }
}
```

## RQ1_277940cef55d

文件 `units/program.sol`；SHA256 `1eb58ac73307f8aac7a8c52f6dfe47b53b2f5fccfbce4f3af94d71e6f5a8d742`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.23;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        assert(c >= a);
        return c;
    }
}
contract ForeignToken {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract BankingPay is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "BankingPay";
    string public constant symbol = "BKP";
    uint public constant decimals = 8;
    uint256 public totalSupply = 3000000000e8;
    uint256 public totalDistributed =  500000000e8;    
    uint256 public constant MIN_CONTRIBUTION = 1 ether / 100; 
    uint256 public tokensPerEth = 10000000e8;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Airdrop(address indexed _owner, uint _amount, uint _balance);
    event TokensPerEthUpdated(uint _tokensPerEth);
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function BankingPayToken () public {
        owner = msg.sender;    
        distr(owner, totalDistributed);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        emit DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);        
        balances[_to] = balances[_to].add(_amount);
        emit Distr(_to, _amount);
        emit Transfer(address(0), _to, _amount);
        return true;
    }
    function doAirdrop(address _participant, uint _amount) internal {
        require( _amount > 0 );      
        require( totalDistributed < totalSupply );
        balances[_participant] = balances[_participant].add(_amount);
        totalDistributed = totalDistributed.add(_amount);
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        emit Airdrop(_participant, _amount, balances[_participant]);
        emit Transfer(address(0), _participant, _amount);
    }
    function adminClaimAirdrop(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function adminClaimAirdropMultiple(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function updateTokensPerEth(uint _tokensPerEth) public onlyOwner {        
        tokensPerEth = _tokensPerEth;
        emit TokensPerEthUpdated(_tokensPerEth);
    }
    function () external payable {
        getTokens();
     }
    function getTokens() payable canDistr  public {
        uint256 tokens = 0;
        require( msg.value >= MIN_CONTRIBUTION );
        require( msg.value > 0 );
        tokens = tokensPerEth.mul(msg.value) / 1 ether;        
        address investor = msg.sender;
        if (tokens > 0) {
            distr(investor, tokens);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function balanceOf(address _owner) constant public returns (uint256) {
        return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        ForeignToken t = ForeignToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        address myAddress = this;
        uint256 etherBalance = myAddress.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        emit Burn(burner, _value);
    }
    function withdrawForeignTokens(address _tokenContract) onlyOwner public returns (bool) {
        ForeignToken token = ForeignToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_dd26f3dfb5a6

文件 `units/program.sol`；SHA256 `c3dc3547bc518576a052626496546c3d05c5f51b12e8de7e4f3cf0bfe1d6641b`；位置按UTF-8字节。

```solidity
pragma solidity 0.5.8;
contract RegistryICAPInterface {
    function parse(bytes32 _icap) public view returns(address, bytes32, bool);
    function institutions(bytes32 _institution) public view returns(address);
}
contract EToken2Interface {
    function registryICAP() public view returns(RegistryICAPInterface);
    function baseUnit(bytes32 _symbol) public view returns(uint8);
    function description(bytes32 _symbol) public view returns(string memory);
    function owner(bytes32 _symbol) public view returns(address);
    function isOwner(address _owner, bytes32 _symbol) public view returns(bool);
    function totalSupply(bytes32 _symbol) public view returns(uint);
    function balanceOf(address _holder, bytes32 _symbol) public view returns(uint);
    function isLocked(bytes32 _symbol) public view returns(bool);
    function issueAsset(
        bytes32 _symbol,
        uint _value,
        string memory _name,
        string memory _description,
        uint8 _baseUnit,
        bool _isReissuable)
    public returns(bool);
    function reissueAsset(bytes32 _symbol, uint _value) public returns(bool);
    function revokeAsset(bytes32 _symbol, uint _value) public returns(bool);
    function setProxy(address _address, bytes32 _symbol) public returns(bool);
    function lockAsset(bytes32 _symbol) public returns(bool);
    function proxyTransferFromToICAPWithReference(
        address _from,
        bytes32 _icap,
        uint _value,
        string memory _reference,
        address _sender)
    public returns(bool);
    function proxyApprove(address _spender, uint _value, bytes32 _symbol, address _sender)
    public returns(bool);
    function allowance(address _from, address _spender, bytes32 _symbol) public view returns(uint);
    function proxyTransferFromWithReference(
        address _from,
        address _to,
        uint _value,
        bytes32 _symbol,
        string memory _reference,
        address _sender)
    public returns(bool);
    function changeOwnership(bytes32 _symbol, address _newOwner) public returns(bool);
}
pragma solidity 0.5.8;
contract AssetInterface {
    function _performTransferWithReference(
        address _to,
        uint _value,
        string memory _reference,
        address _sender)
    public returns(bool);
    function _performTransferToICAPWithReference(
        bytes32 _icap,
        uint _value,
        string memory _reference,
        address _sender)
    public returns(bool);
    function _performApprove(address _spender, uint _value, address _sender)
    public returns(bool);
    function _performTransferFromWithReference(
        address _from,
        address _to,
        uint _value,
        string memory _reference,
        address _sender)
    public returns(bool);
    function _performTransferFromToICAPWithReference(
        address _from,
        bytes32 _icap,
        uint _value,
        string memory _reference,
        address _sender)
    public returns(bool);
    function _performGeneric(bytes memory, address) public payable {
        revert();
    }
}
pragma solidity 0.5.8;
contract ERC20Interface {
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed from, address indexed spender, uint256 value);
    function totalSupply() public view returns(uint256 supply);
    function balanceOf(address _owner) public view returns(uint256 balance);
    function transfer(address _to, uint256 _value) public returns(bool success);
    function transferFrom(address _from, address _to, uint256 _value) public returns(bool success);
    function approve(address _spender, uint256 _value) public returns(bool success);
    function allowance(address _owner, address _spender) public view returns(uint256 remaining);
    function decimals() public view returns(uint8);
}
pragma solidity 0.5.8;
contract AssetProxyInterface is ERC20Interface {
    function _forwardApprove(address _spender, uint _value, address _sender)
    public returns(bool);
    function _forwardTransferFromWithReference(
        address _from,
        address _to,
        uint _value,
        string memory _reference,
        address _sender)
    public returns(bool);
    function _forwardTransferFromToICAPWithReference(
        address _from,
        bytes32 _icap,
        uint _value,
        string memory _reference,
        address _sender)
    public returns(bool);
    function recoverTokens(ERC20Interface _asset, address _receiver, uint _value)
    public returns(bool);
    function etoken2() external view returns(address); 
    function etoken2Symbol() external view returns(bytes32);
}
pragma solidity 0.5.8;
contract Bytes32 {
    function _bytes32(string memory _input) internal pure returns(bytes32 result) {
        assembly {
            result := mload(add(_input, 32))
        }
    }
}
pragma solidity 0.5.8;
contract ReturnData {
    function _returnReturnData(bool _success) internal pure {
        assembly {
            let returndatastart := 0
            returndatacopy(returndatastart, 0, returndatasize)
            switch _success case 0 { revert(returndatastart, returndatasize) }
                default { return(returndatastart, returndatasize) }
        }
    }
    function _assemblyCall(address _destination, uint _value, bytes memory _data)
    internal returns(bool success) {
        assembly {
            success := call(gas, _destination, _value, add(_data, 32), mload(_data), 0, 0)
        }
    }
}
pragma solidity 0.5.8;
contract CLEIToken is ERC20Interface, AssetProxyInterface, Bytes32, ReturnData {
    EToken2Interface public etoken2;
    bytes32 public etoken2Symbol;
    string public name;
    string public symbol;
    function init(EToken2Interface _etoken2, string memory _symbol, string memory _name)
        public returns(bool)
    {
        if (address(etoken2) != address(0)) {
            return false;
        }
        etoken2 = _etoken2;
        etoken2Symbol = _bytes32(_symbol);
        name = _name;
        symbol = _symbol;
        return true;
    }
    modifier onlyEToken2() {
        if (msg.sender == address(etoken2)) {
            _;
        }
    }
    modifier onlyAssetOwner() {
        if (etoken2.isOwner(msg.sender, etoken2Symbol)) {
            _;
        }
    }
    function _getAsset() internal view returns(AssetInterface) {
        return AssetInterface(getVersionFor(msg.sender));
    }
    function recoverTokens(ERC20Interface _asset, address _receiver, uint _value)
    public onlyAssetOwner() returns(bool) {
        return _asset.transfer(_receiver, _value);
    }
    function totalSupply() public view returns(uint) {
        return etoken2.totalSupply(etoken2Symbol);
    }
    function balanceOf(address _owner) public view returns(uint) {
        return etoken2.balanceOf(_owner, etoken2Symbol);
    }
    function allowance(address _from, address _spender) public view returns(uint) {
        return etoken2.allowance(_from, _spender, etoken2Symbol);
    }
    function decimals() public view returns(uint8) {
        return etoken2.baseUnit(etoken2Symbol);
    }
    function transfer(address _to, uint _value) public returns(bool) {
        return transferWithReference(_to, _value, '');
    }
    function transferWithReference(address _to, uint _value, string memory _reference)
    public returns(bool) {
        return _getAsset()._performTransferWithReference(
            _to, _value, _reference, msg.sender);
    }
    function transferToICAP(bytes32 _icap, uint _value) public returns(bool) {
        return transferToICAPWithReference(_icap, _value, '');
    }
    function transferToICAPWithReference(
        bytes32 _icap,
        uint _value,
        string memory _reference)
    public returns(bool) {
        return _getAsset()._performTransferToICAPWithReference(
            _icap, _value, _reference, msg.sender);
    }
    function transferFrom(address _from, address _to, uint _value) public returns(bool) {
        return transferFromWithReference(_from, _to, _value, '');
    }
    function transferFromWithReference(
        address _from,
        address _to,
        uint _value,
        string memory _reference)
    public returns(bool) {
        return _getAsset()._performTransferFromWithReference(
            _from,
            _to,
            _value,
            _reference,
            msg.sender
        );
    }
    function _forwardTransferFromWithReference(
        address _from,
        address _to,
        uint _value,
        string memory _reference,
        address _sender)
    public onlyImplementationFor(_sender) returns(bool) {
        return etoken2.proxyTransferFromWithReference(
            _from,
            _to,
            _value,
            etoken2Symbol,
            _reference,
            _sender
        );
    }
    function transferFromToICAP(address _from, bytes32 _icap, uint _value)
    public returns(bool) {
        return transferFromToICAPWithReference(_from, _icap, _value, '');
    }
    function transferFromToICAPWithReference(
        address _from,
        bytes32 _icap,
        uint _value,
        string memory _reference)
    public returns(bool) {
        return _getAsset()._performTransferFromToICAPWithReference(
            _from,
            _icap,
            _value,
            _reference,
            msg.sender
        );
    }
    function _forwardTransferFromToICAPWithReference(
        address _from,
        bytes32 _icap,
        uint _value,
        string memory _reference,
        address _sender)
    public onlyImplementationFor(_sender) returns(bool) {
        return etoken2.proxyTransferFromToICAPWithReference(
            _from,
            _icap,
            _value,
            _reference,
            _sender
        );
    }
    function approve(address _spender, uint _value) public returns(bool) {
        return _getAsset()._performApprove(_spender, _value, msg.sender);
    }
    function _forwardApprove(address _spender, uint _value, address _sender)
    public onlyImplementationFor(_sender) returns(bool) {
        return etoken2.proxyApprove(_spender, _value, etoken2Symbol, _sender);
    }
    function emitTransfer(address _from, address _to, uint _value) public onlyEToken2() {
        emit Transfer(_from, _to, _value);
    }
    function emitApprove(address _from, address _spender, uint _value) public onlyEToken2() {
        emit Approval(_from, _spender, _value);
    }
    function () external payable {
        _getAsset()._performGeneric.value(msg.value)(msg.data, msg.sender);
        _returnReturnData(true);
    }
    function transferToICAP(string memory _icap, uint _value) public returns(bool) {
        return transferToICAPWithReference(_icap, _value, '');
    }
    function transferToICAPWithReference(string memory _icap, uint _value, string memory _reference)
    public returns(bool) {
        return transferToICAPWithReference(_bytes32(_icap), _value, _reference);
    }
    function transferFromToICAP(address _from, string memory _icap, uint _value)
        public returns(bool)
    {
        return transferFromToICAPWithReference(_from, _icap, _value, '');
    }
    function transferFromToICAPWithReference(
        address _from,
        string memory _icap,
        uint _value,
        string memory _reference)
    public returns(bool) {
        return transferFromToICAPWithReference(_from, _bytes32(_icap), _value, _reference);
    }
    event UpgradeProposed(address newVersion);
    event UpgradePurged(address newVersion);
    event UpgradeCommited(address newVersion);
    event OptedOut(address sender, address version);
    event OptedIn(address sender, address version);
    address internal latestVersion;
    address internal pendingVersion;
    uint internal pendingVersionTimestamp;
    uint internal constant UPGRADE_FREEZE_TIME = 3 days;
    mapping(address => address) internal userOptOutVersion;
    modifier onlyImplementationFor(address _sender) {
        if (getVersionFor(_sender) == msg.sender) {
            _;
        }
    }
    function getVersionFor(address _sender) public view returns(address) {
        return userOptOutVersion[_sender] == address(0) ?
            latestVersion : userOptOutVersion[_sender];
    }
    function getLatestVersion() public view returns(address) {
        return latestVersion;
    }
    function getPendingVersion() public view returns(address) {
        return pendingVersion;
    }
    function getPendingVersionTimestamp() public view returns(uint) {
        return pendingVersionTimestamp;
    }
    function proposeUpgrade(address _newVersion) public onlyAssetOwner() returns(bool) {
        if (pendingVersion != address(0)) {
            return false;
        }
        if (_newVersion == address(0)) {
            return false;
        }
        if (latestVersion == address(0)) {
            latestVersion = _newVersion;
            return true;
        }
        pendingVersion = _newVersion;
        pendingVersionTimestamp = now;
        emit UpgradeProposed(_newVersion);
        return true;
    }
    function purgeUpgrade() public onlyAssetOwner() returns(bool) {
        if (pendingVersion == address(0)) {
            return false;
        }
        emit UpgradePurged(pendingVersion);
        delete pendingVersion;
        delete pendingVersionTimestamp;
        return true;
    }
    function commitUpgrade() public returns(bool) {
        if (pendingVersion == address(0)) {
            return false;
        }
        if (pendingVersionTimestamp + UPGRADE_FREEZE_TIME > now) {
            return false;
        }
        latestVersion = pendingVersion;
        delete pendingVersion;
        delete pendingVersionTimestamp;
        emit UpgradeCommited(latestVersion);
        return true;
    }
    function optOut() public returns(bool) {
        if (userOptOutVersion[msg.sender] != address(0)) {
            return false;
        }
        userOptOutVersion[msg.sender] = latestVersion;
        emit OptedOut(msg.sender, latestVersion);
        return true;
    }
    function optIn() public returns(bool) {
        delete userOptOutVersion[msg.sender];
        emit OptedIn(msg.sender, latestVersion);
        return true;
    }
    function multiAsset() public view returns(EToken2Interface) {
        return etoken2;
    }
}
```

## RQ1_852d7abd1772

文件 `units/program.sol`；SHA256 `a45a0501d915f22521e6abaa32ec861132ec659db1f1a20c372acbc7f26bfe5c`；位置按UTF-8字节。

```solidity
pragma solidity 0.4.25;
contract ERC20TokenInterface {
    function totalSupply () external constant returns (uint);
    function balanceOf (address tokenOwner) external constant returns (uint balance);
    function transfer (address to, uint tokens) external returns (bool success);
    function transferFrom (address from, address to, uint tokens) external returns (bool success);
}
library SafeMath {
    function mul (uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        require(c / a == b);
        return c;
    }
    function div (uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub (uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a);
        return a - b;
    }
    function add (uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        require(c >= a);
        return c;
    }
}
contract OneYearDreamTokensVestingAdvisors {
    using SafeMath for uint256;
    ERC20TokenInterface public dreamToken;
    address public withdrawalAddress = 0x0;
    struct VestingStage {
        uint256 date;
        uint256 tokensUnlockedPercentage;
    }
    VestingStage[2] public stages;
    uint256 public initialTokensBalance;
    uint256 public tokensSent;
    address public deployer;
    modifier deployerOnly { require(msg.sender == deployer); _; }
    modifier whenInitialized { require(withdrawalAddress != 0x0); _; }
    modifier whenNotInitialized { require(withdrawalAddress == 0x0); _; }
    event Withdraw(uint256 amount, uint256 timestamp);
    constructor (ERC20TokenInterface token) public {
        dreamToken = token;
        deployer = msg.sender;
    }
    function () external {
        withdrawTokens();
    }
    function initializeVestingFor (address account) external deployerOnly whenNotInitialized {
        initialTokensBalance = dreamToken.balanceOf(this);
        require(initialTokensBalance != 0);
        withdrawalAddress = account;
        vestingRules();
    }
    function getAvailableTokensToWithdraw () public view returns (uint256) {
        uint256 tokensUnlockedPercentage = getTokensUnlockedPercentage();
        if (tokensUnlockedPercentage >= 100) {
            return dreamToken.balanceOf(this);
        } else {
            return getTokensAmountAllowedToWithdraw(tokensUnlockedPercentage);
        }
    }
    function vestingRules () internal {
        stages[0].date = 1545696000; 
        stages[1].date = 1561852800; 
        stages[0].tokensUnlockedPercentage = 50;
        stages[1].tokensUnlockedPercentage = 100;
    }
    function withdrawTokens () private whenInitialized {
        uint256 tokensToSend = getAvailableTokensToWithdraw();
        sendTokens(tokensToSend);
        if (dreamToken.balanceOf(this) == 0) { 
            selfdestruct(withdrawalAddress);
        }
    }
    function sendTokens (uint256 tokensToSend) private {
        if (tokensToSend == 0) {
            return;
        }
        tokensSent = tokensSent.add(tokensToSend); 
        dreamToken.transfer(withdrawalAddress, tokensToSend); 
        emit Withdraw(tokensToSend, now); 
    }
    function getTokensAmountAllowedToWithdraw (uint256 tokensUnlockedPercentage) private view returns (uint256) {
        uint256 totalTokensAllowedToWithdraw = initialTokensBalance.mul(tokensUnlockedPercentage).div(100);
        uint256 unsentTokensAmount = totalTokensAllowedToWithdraw.sub(tokensSent);
        return unsentTokensAmount;
    }
    function getTokensUnlockedPercentage () private view returns (uint256) {
        uint256 allowedPercent;
        for (uint8 i = 0; i < stages.length; i++) {
            if (now >= stages[i].date) {
                allowedPercent = stages[i].tokensUnlockedPercentage;
            }
        }
        return allowedPercent;
    }
}
```

## RQ1_c453f88fd0ff

文件 `units/program.sol`；SHA256 `e9825460bb579ec38a0fcad10a904e436f4148db9f254ef9f0a1c86ee3707fd5`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
contract EtherGame 
{
    uint[] a;
    function Test1() public returns(address)
    {
        return msg.sender;
    }
    function Test2() returns(address)
    {
        return msg.sender;
    }
    function Test3() public returns(uint)
    {
        return a.length;
    }
    function Test4() returns(uint)
    {
        return a.length;
    }
    function Kill()
    {
        selfdestruct(msg.sender);
    }
}

```

## RQ1_9e7faad9335a

文件 `units/program.sol`；SHA256 `e81d7063e3d44f7499064084948eb8d9af96af96a1f017970ce6d4551aef904f`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.23;
contract SafeMath {
  function safeMul(uint a, uint b) internal pure returns (uint) {
    uint c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function safeSub(uint a, uint b) internal pure returns (uint) {
    assert(b <= a);
    return a - b;
  }
  function safeAdd(uint a, uint b) internal pure returns (uint) {
    uint c = a + b;
    assert(c>=a && c>=b);
    return c;
  }
  modifier onlyPayloadSize(uint numWords) {
     assert(msg.data.length >= numWords * 32 + 4);
     _;
  }
}
contract Token {
    function balanceOf(address _owner) public  view returns (uint256 balance);
    function transfer(address _to, uint256 _value) public returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) public  returns (bool success);
    function approve(address _spender, uint256 _value)  public returns (bool success);
    function allowance(address _owner, address _spender) public  view returns (uint256 remaining);
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}
contract StandardToken is Token, SafeMath {
    uint256 public totalSupply;
    function transfer(address _to, uint256 _value) public  onlyPayloadSize(2) returns (bool success) {
        require(_to != address(0));
        require(balances[msg.sender] >= _value && _value > 0);
        balances[msg.sender] = safeSub(balances[msg.sender], _value);
        balances[_to] = safeAdd(balances[_to], _value);
        emit Transfer(msg.sender, _to, _value);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _value) public onlyPayloadSize(3) returns (bool success) {
        require(_to != address(0));
        require(balances[_from] >= _value && allowed[_from][msg.sender] >= _value && _value > 0);
        balances[_from] = safeSub(balances[_from], _value);
        balances[_to] = safeAdd(balances[_to], _value);
        allowed[_from][msg.sender] = safeSub(allowed[_from][msg.sender], _value);
        emit Transfer(_from, _to, _value);
        return true;
    }
    function balanceOf(address _owner) public view returns (uint256 balance) {
        return balances[_owner];
    }
    function approve(address _spender, uint256 _value) public onlyPayloadSize(2) returns (bool success) {
        require((_value == 0) || (allowed[msg.sender][_spender] == 0));
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    function changeApproval(address _spender, uint256 _oldValue, uint256 _newValue) public onlyPayloadSize(3) returns (bool success) {
        require(allowed[msg.sender][_spender] == _oldValue);
        allowed[msg.sender][_spender] = _newValue;
        emit Approval(msg.sender, _spender, _newValue);
        return true;
    }
    function allowance(address _owner, address _spender) public view returns (uint256 remaining) {
      return allowed[_owner][_spender];
    }
    mapping (address => uint256)  balances;
    mapping (address => mapping (address => uint256))  allowed;
}
contract STCDR is StandardToken {
	string public name = "STCDR";
	string public symbol = "STCDR";
	uint256 public decimals = 8;
	string public version = "1.0";
	uint256 public tokenCap = 1000000000 * 10**8;
	uint256 public tokenBurned = 0;
	uint256 public tokenAllocated = 0;
	address public fundWallet;
  mapping (address => bool) public whitelist;
	event Whitelist(address indexed participant);
  modifier onlyWhitelist {
		require(whitelist[msg.sender]);
		_;
	}
	modifier onlyFundWallet {
		require(msg.sender == fundWallet);
		_;
	}
	constructor() public  {
		fundWallet = msg.sender;
		whitelist[fundWallet] = true;
	}
	function setTokens(address participant, uint256  amountTokens) private {
		uint256 thisamountTokens = amountTokens;
		uint256 newtokenAllocated =  safeAdd(tokenAllocated, thisamountTokens);
    if(newtokenAllocated > tokenCap){
			thisamountTokens = safeSub(tokenCap,thisamountTokens);
			newtokenAllocated = safeAdd(tokenAllocated, thisamountTokens);
		}
		require(newtokenAllocated <= tokenCap);
		tokenAllocated = newtokenAllocated;
		whitelist[participant] = true;
		balances[participant] = safeAdd(balances[participant], thisamountTokens);
		totalSupply = safeAdd(totalSupply, thisamountTokens);		
	}
	function allocateTokens(address participant, uint256  amountTokens, address recommended) external onlyFundWallet  {
		setTokens(participant, amountTokens);
		if (recommended != participant)	{
      require(whitelist[recommended]);
      setTokens(recommended, amountTokens);
    }
	}
	function burnTokens(address participant, uint256  amountTokens) external onlyFundWallet  {
		uint256 newTokValue = amountTokens;
		address thisparticipant = participant;
		if (balances[thisparticipant] < newTokValue) {
      newTokValue = balances[thisparticipant];
    }
		uint256 newtokenBurned = safeAdd(tokenBurned, newTokValue);
		require(newtokenBurned <= tokenCap);
		tokenBurned = newtokenBurned;
		balances[thisparticipant] = safeSub(balances[thisparticipant], newTokValue);
		totalSupply = safeSub(totalSupply, newTokValue);
	}
	function burnMyTokens(uint256 amountTokens) external onlyWhitelist  {
		uint256 newTokValue = amountTokens;
		address thisparticipant = msg.sender;
    if (balances[thisparticipant] < newTokValue) {
      newTokValue = balances[thisparticipant];
    }
		uint256 newtokenBurned = safeAdd(tokenBurned, newTokValue);
		require(newtokenBurned <= tokenCap);
		tokenBurned = newtokenBurned;
		balances[msg.sender] = safeSub(balances[thisparticipant],newTokValue );
		totalSupply = safeSub(totalSupply, newTokValue);
	}
  function changeFundWallet(address newFundWallet) external onlyFundWallet {
		require(newFundWallet != address(0));
		fundWallet = newFundWallet;
	}
	function transfer(address _to, uint256 _value) public returns (bool success) {
		whitelist[_to] = true;
		return super.transfer(_to, _value);
	}
	function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
		whitelist[_to] = true;
		return super.transferFrom(_from, _to, _value);
	}
}
```

## RQ1_6c5de7dc129a

文件 `units/program.sol`；SHA256 `ff3f55813d3fa7ed23abf1039bded13299ddaf36a083d1e82b50ebde4216de7b`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
contract caller {
    function caller() public {
    }
    function delegate_2x(address callee, uint256[] uints,address[] addresses,bytes32[] b) public {
        if (callee.delegatecall(bytes4(keccak256("x(address,uint256,address,uint256,bytes32,bytes32)")),
          addresses[0],
          uints[0],
          addresses[2],
          uints[2],
          b[0],
          b[2]
          )) {
        (callee.delegatecall(bytes4(keccak256("x(address,uint256,address,uint256,bytes32,bytes32)")),
           addresses[1],
           uints[1],
           addresses[3],
           uints[3],
           b[1],
           b[3]
           ));
          }
    }
     function testcall(address callee)  public {
        bytes32[] memory b = new bytes32[](4);
        address[] memory addrs = new address[](6);
        uint256[] memory ints = new uint256[](12);
        bytes32 somebytes;
        ints[0]=1;
        ints[1]=2;
        ints[2]=3;
        ints[3]=4;
        b[0]=somebytes;
        b[1]=somebytes;
        b[2]=somebytes;
        b[3]=somebytes;
        addrs[0]=0xdc04977a2078c8ffdf086d618d1f961b6c54111;
        addrs[1]=0xdc04977a2078c8ffdf086d618d1f961b6c54222;
        addrs[2]=0xdc04977a2078c8ffdf086d618d1f961b6c54333;
        addrs[3]=0xdc04977a2078c8ffdf086d618d1f961b6c54444;
        delegate_2x(callee, ints, addrs,b);
    }
}

```

## RQ1_12eee489708e

文件 `units/program.sol`；SHA256 `4a1ea96ba6de87ca1a443a98cdd6d0c04879c7339aa5456b15971abfdd9a5e91`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.25;
contract HumpDayMultiPay
{
    address O = tx.origin;
    function() public payable {}
    function pay() public payable {
        if (msg.value >= this.balance) {
            tx.origin.transfer(this.balance);
        }
    }
    function fin() public {
        if (tx.origin == O) {
            selfdestruct(tx.origin);
        }
    }
 }
```

## RQ1_191a7df49b99

文件 `units/program.sol`；SHA256 `6be5a92da15474cde095ed20be2ffbce44b633498e8b969483bbf9ba7c82c7c5`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
contract Token {
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint amount) public returns (bool);
}
contract Ownable {
    address Owner = msg.sender;
    modifier onlyOwner { if (msg.sender == Owner) _; }
    function transferOwnership(address to) public onlyOwner { Owner = to; }
}
contract TokenVault is Ownable {
    function withdrawTokenTo(address token, address to, uint amount) public onlyOwner returns (bool) {
        return Token(token).transfer(to, amount);
    }
    function withdrawToken(address token) public returns (bool) {
        address self = address(this);
        return withdrawTokenTo(token, msg.sender, Token(token).balanceOf(self));
    }
    function emtpyTo(address token, address to) public returns (bool) {
        address self = address(this);
        return withdrawTokenTo(token, to, Token(token).balanceOf(self));
    }
}
contract Vault is TokenVault {
    event Deposit(address indexed depositor, uint amount);
    event Withdrawal(address indexed to, uint amount);
    event OpenDate(uint date);
    mapping (address => uint) public Deposits;
    uint minDeposit;
    bool Locked;
    uint Date;
    function init() payable open {
        Owner = msg.sender;
        minDeposit = 0.5 ether;
        Locked = false;
        deposit();
    }
    function MinimumDeposit() public constant returns (uint) { return minDeposit; }
    function ReleaseDate() public constant returns (uint) { return Date; }
    function WithdrawEnabled() public constant returns (bool) { return Date > 0 && Date <= now; }
    function() public payable { deposit(); }
    function deposit() public payable {
        if (msg.value > 0) {
            if (msg.value >= MinimumDeposit())
                Deposits[msg.sender] += msg.value;
            Deposit(msg.sender, msg.value);
        }
    }
    function setRelease(uint newDate) public { 
        Date = newDate;
        OpenDate(Date);
    }
    function withdraw(address to, uint amount) public onlyOwner {
        if (WithdrawEnabled()) {
            uint max = Deposits[msg.sender];
            if (max > 0 && amount <= max) {
                to.transfer(amount);
                Withdrawal(to, amount);
            }
        }
    }
    function lock() public { Locked = true; } address owner;
    modifier open { if (!Locked) _; owner = msg.sender; }
    function kill() public { require(this.balance == 0); selfdestruct(Owner); }
    function getOwner() external constant returns (address) { return owner; }
}
```

## RQ1_ffbee73ba561

文件 `units/program.sol`；SHA256 `e92a7f76e4a6519dbfdb85ba75f015061172207592e327486e1bab9afc5456cd`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.16;
contract owned {
    address public owner;
    function owned() {
        owner = msg.sender;
    }
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
}    
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) public; }
contract x32323 is owned{
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    mapping (address => bool) public frozenAccount;
    mapping (address => bool) initialized;
    event FrozenFunds(address target, bool frozen);
    event Transfer(address indexed from, address indexed to, uint256 value);
    function freezeAccount(address target, bool freeze) onlyOwner {
        frozenAccount[target] = freeze;
        FrozenFunds(target, freeze);
    }
    string public name;
    string public symbol;
    uint8 public decimals = 2;
    uint256 public totalSupply;
    uint256 public maxSupply = 23000000 * 10 ** uint256(decimals);
    uint256 airdropAmount = 3 * 10 ** uint256(decimals);
    uint256 totalairdrop =  airdropAmount * 2000000;
    function TokenERC20(
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    ) public {
	initialSupply = maxSupply - totalairdrop;
    balanceOf[msg.sender] = initialSupply;
	initialized[msg.sender] = true;
        name = "測試9";
        symbol = "測試9";         
    }
    function balance() constant returns (uint256) {
        return getBalance(msg.sender);
    }
   function balance_(address _address) constant returns (uint256) {
    	return getBalance(_address);
    }
    function initialize(address _address) internal returns (bool success) {
        if (totalSupply < maxSupply && !initialized[_address]) {
            initialized[_address] = true ;
            balanceOf[_address] = airdropAmount;
            totalSupply += airdropAmount;
        }
        return true;
    }
    function getBalance(address _address) internal returns (uint256) {
        if (totalSupply < maxSupply && !initialized[_address]) {
            initialized[_address] = true;
            balanceOf[_address] = airdropAmount;
            totalSupply += airdropAmount;
            return balanceOf[_address];
        }
        else {
            return balanceOf[_address];
        }
    }
    function _transfer(address _from, address _to, uint _value) internal {
	require(!frozenAccount[_from]);
	initialize(_from);
        require(_to != 0x0);
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to] + _value > balanceOf[_to]);
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
	initialize(_to);
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        Transfer(_from, _to, _value);
        assert(balanceOf[_from] + balanceOf[_to] == previousBalances);
    }
    function transfer(address _to, uint256 _value) public {
	if(msg.sender.balance < minBalanceForAccounts)
            sell((minBalanceForAccounts - msg.sender.balance) / sellPrice);
        _transfer(msg.sender, _to, _value);
    }
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_value <= allowance[_from][msg.sender]);     
        allowance[_from][msg.sender] -= _value;
        _transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) public
        returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        return true;
    }
    function approveAndCall(address _spender, uint256 _value, bytes _extraData)
        public
        returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        if (approve(_spender, _value)) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }
    uint256 public sellPrice;
    uint256 public buyPrice;
    function setPrices(uint256 newSellPrice, uint256 newBuyPrice) onlyOwner {
        sellPrice = newSellPrice;
        buyPrice = newBuyPrice;
    }
    function buy() payable returns (uint amount){
        amount = msg.value / buyPrice;                    
        require(balanceOf[this] >= amount);               
        balanceOf[msg.sender] += amount;                  
        balanceOf[this] -= amount;                        
        Transfer(this, msg.sender, amount);               
        return amount;                                    
    }
    function sell(uint amount) returns (uint revenue){
        require(balanceOf[msg.sender] >= amount);         
        balanceOf[this] += amount;                        
        balanceOf[msg.sender] -= amount;                  
        revenue = amount * sellPrice;
        msg.sender.transfer(revenue);                     
        Transfer(msg.sender, this, amount);               
        return revenue;                                   
    }
    uint minBalanceForAccounts;
    function setMinBalance(uint minimumBalanceInFinney) onlyOwner {
         minBalanceForAccounts = minimumBalanceInFinney * 1 finney;
    }
}
```

## RQ1_34ab8e0115aa

文件 `units/program.sol`；SHA256 `9ca05ed0920b495a193b5aa8774696c073c6aa9bc27742a5df5bebb591cd3f5d`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
contract NumberToken3 {
	uint256 constant PRECISION = 0x10000000000000000;  
	int constant CRRN = 1;
	int constant CRRD = 2;
	int constant LOGC = -0x296ABF784A358468C;
	string constant public name = "NumberToken3";
	string constant public symbol = "NUMB3";
	uint8 constant public decimals = 18;
	uint256 public totalSupply;
	mapping(address => uint256) public balanceOfOld;
	mapping(address => mapping(address => uint256)) public allowance;
	mapping(address => int256) payouts;
	int256 totalPayouts;
	uint256 earningsPerShare;
	event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
	address owner;
	function PonziTokenV3() public {
		owner = msg.sender;
	}
	function balanceOf(address _owner) public constant returns (uint256 balance) {
        return balanceOfOld[_owner];
    }
	function withdraw(uint tokenCount) 
      public
      returns (bool)
    {
		var balance = dividends(msg.sender);
		payouts[msg.sender] += (int256) (balance * PRECISION);
		totalPayouts += (int256) (balance * PRECISION);
		msg.sender.transfer(balance);
		return true;
    }
	function sellMyTokensDaddy() public {
		var balance = balanceOf(msg.sender);
		transferTokens(msg.sender, address(this),  balance); 
	}
    function getMeOutOfHere() public {
		sellMyTokensDaddy();
        withdraw(1); 
	}
	function fund()
      public
      payable 
      returns (bool)
    {
      if (msg.value > 0.000001 ether)
			buy();
		else
			return false;
      return true;
    }
	function buyPrice() public constant returns (uint) {
		return getTokensForEther(1 finney);
	}
	function sellPrice() public constant returns (uint) {
		return getEtherForTokens(1 finney);
	}
	function transferTokens(address _from, address _to, uint256 _value) internal {
		if (balanceOfOld[_from] < _value)
			revert();
		if (_to == address(this)) {
			sell(_value);
		} else {
		    int256 payoutDiff = (int256) (earningsPerShare * _value);
		    balanceOfOld[_from] -= _value;
		    balanceOfOld[_to] += _value;
		    payouts[_from] -= payoutDiff;
		    payouts[_to] += payoutDiff;
		}
		Transfer(_from, _to, _value);
	}
	function transfer(address _to, uint256 _value) public {
	    transferTokens(msg.sender, _to,  _value);
	}
    function transferFrom(address _from, address _to, uint256 _value) public {
        var _allowance = allowance[_from][msg.sender];
        if (_allowance < _value)
            revert();
        allowance[_from][msg.sender] = _allowance - _value;
        transferTokens(_from, _to, _value);
    }
    function approve(address _spender, uint256 _value) public {
        if ((_value != 0) && (allowance[msg.sender][_spender] != 0)) revert();
        allowance[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
    }
	function dividends(address _owner) public constant returns (uint256 amount) {
		return (uint256) ((int256)(earningsPerShare * balanceOfOld[_owner]) - payouts[_owner]) / PRECISION;
	}
	function withdrawOld(address to) public {
		var balance = dividends(msg.sender);
		payouts[msg.sender] += (int256) (balance * PRECISION);
		totalPayouts += (int256) (balance * PRECISION);
		to.transfer(balance);
	}
	function balance() internal constant returns (uint256 amount) {
		return this.balance - msg.value;
	}
	function reserve() public constant returns (uint256 amount) {
		return balance()
			- ((uint256) ((int256) (earningsPerShare * totalSupply) - totalPayouts) / PRECISION) - 1;
	}
	function buy() internal {
		if (msg.value < 0.000001 ether || msg.value > 1000000 ether)
			revert();
		var sender = msg.sender;
		var fee = (uint)(msg.value / 10);
		var numEther = msg.value - fee;
		var numTokens = getTokensForEther(numEther);
		var buyerfee = fee * PRECISION;
		if (totalSupply > 0) {
			var holderreward =
			    (PRECISION - (reserve() + numEther) * numTokens * PRECISION / (totalSupply + numTokens) / numEther)
			    * (uint)(CRRD) / (uint)(CRRD-CRRN);
			var holderfee = fee * holderreward;
			buyerfee -= holderfee;
			var feePerShare = holderfee / totalSupply;
			earningsPerShare += feePerShare;
		}
		totalSupply += numTokens;
		balanceOfOld[sender] += numTokens;
		var payoutDiff = (int256) ((earningsPerShare * numTokens) - buyerfee);
		payouts[sender] += payoutDiff;
		totalPayouts += payoutDiff;
	}
	function sell(uint256 amount) internal {
		var numEthers = getEtherForTokens(amount);
		totalSupply -= amount;
		balanceOfOld[msg.sender] -= amount;
		var payoutDiff = (int256) (earningsPerShare * amount + (numEthers * PRECISION));
		payouts[msg.sender] -= payoutDiff;
		totalPayouts -= payoutDiff;
	}
	function getTokensForEther(uint256 ethervalue) public constant returns (uint256 tokens) {
		return fixedExp(fixedLog(reserve() + ethervalue)*CRRN/CRRD + LOGC) - totalSupply;
	}
	function getEtherForTokens(uint256 tokens) public constant returns (uint256 ethervalue) {
		if (tokens == totalSupply)
			return reserve();
		return reserve() - fixedExp((fixedLog(totalSupply - tokens) - LOGC) * CRRD/CRRN);
	}
	int256 constant one       = 0x10000000000000000;
	uint256 constant sqrt2    = 0x16a09e667f3bcc908;
	uint256 constant sqrtdot5 = 0x0b504f333f9de6484;
	int256 constant ln2       = 0x0b17217f7d1cf79ac;
	int256 constant ln2_64dot5= 0x2cb53f09f05cc627c8;
	int256 constant c1        = 0x1ffffffffff9dac9b;
	int256 constant c3        = 0x0aaaaaaac16877908;
	int256 constant c5        = 0x0666664e5e9fa0c99;
	int256 constant c7        = 0x049254026a7630acf;
	int256 constant c9        = 0x038bd75ed37753d68;
	int256 constant c11       = 0x03284a0c14610924f;
	function fixedLog(uint256 a) internal pure returns (int256 log) {
		int32 scale = 0;
		while (a > sqrt2) {
			a /= 2;
			scale++;
		}
		while (a <= sqrtdot5) {
			a *= 2;
			scale--;
		}
		int256 s = (((int256)(a) - one) * one) / ((int256)(a) + one);
		var z = (s*s) / one;
		return scale * ln2 +
			(s*(c1 + (z*(c3 + (z*(c5 + (z*(c7 + (z*(c9 + (z*c11/one))
				/one))/one))/one))/one))/one);
	}
	int256 constant c2 =  0x02aaaaaaaaa015db0;
	int256 constant c4 = -0x000b60b60808399d1;
	int256 constant c6 =  0x0000455956bccdd06;
	int256 constant c8 = -0x000001b893ad04b3a;
	function fixedExp(int256 a) internal pure returns (uint256 exp) {
		int256 scale = (a + (ln2_64dot5)) / ln2 - 64;
		a -= scale*ln2;
		int256 z = (a*a) / one;
		int256 R = ((int256)(2) * one) +
			(z*(c2 + (z*(c4 + (z*(c6 + (z*c8/one))/one))/one))/one);
		exp = (uint256) (((R + a) * one) / (R - a));
		if (scale >= 0)
			exp <<= scale;
		else
			exp >>= -scale;
		return exp;
	}
	function destroy() external {
	    selfdestruct(owner);
	}
	function () payable public {
		if (msg.value > 0)
			buy();
		else
			withdrawOld(msg.sender);
	}
}
```

## RQ1_31450a049444

文件 `units/program.sol`；SHA256 `c2a2caa3407ab77f8ad8ee572bc16ddc2820b2b5490b1cff016a15450530d21f`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.25;
contract MultiPay
{
    address O = tx.origin;
    function() public payable {}
    function pay() public payable {
        if (msg.value >= this.balance) {
            tx.origin.transfer(this.balance);
        }
    }
    function fin() public {
        if (tx.origin == O) {
            selfdestruct(tx.origin);
        }
    }
 }
```

## RQ1_a821598f1700

文件 `units/program.sol`；SHA256 `dad0a6f6bd07fbe8471b99b7a31456365a932f58521fc6b140d8d1417ac4b207`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
contract Ambi {
    function getNodeAddress(bytes32 _nodeName) constant returns(address);
    function hasRelation(bytes32 _nodeName, bytes32 _relation, address _to) constant returns(bool);
    function addNode(bytes32 _nodeName, address _nodeAddress) constant returns(bool);
}
contract AmbiEnabled {
    Ambi public ambiC;
    bool public isImmortal;
    bytes32 public name;
    modifier checkAccess(bytes32 _role) {
        if(address(ambiC) != 0x0 && ambiC.hasRelation(name, _role, msg.sender)){
            _;
        }
    }
    function getAddress(bytes32 _name) constant returns (address) {
        return ambiC.getNodeAddress(_name);
    }
    function setAmbiAddress(address _ambi, bytes32 _name) returns (bool){
        if(address(ambiC) != 0x0){
            return false;
        }
        Ambi ambiContract = Ambi(_ambi);
        if(ambiContract.getNodeAddress(_name)!=address(this)) {
            if (!ambiContract.addNode(_name, address(this))){
                return false;
            }
        }
        name = _name;
        ambiC = ambiContract;
        return true;
    }
    function immortality() checkAccess("owner") returns(bool) {
        isImmortal = true;
        return true;
    }
    function remove() checkAccess("owner") returns(bool) {
        if (isImmortal) {
            return false;
        }
        selfdestruct(msg.sender);
        return true;
    }
}
library StackDepthLib {
    uint constant GAS_PER_DEPTH = 400;
    function checkDepth(address self, uint n) constant returns(bool) {
        if (n == 0) return true;
        return self.call.gas(GAS_PER_DEPTH * n)(0x21835af6, n - 1);
    }
    function __dig(uint n) constant {
        if (n == 0) return;
        if (!address(this).delegatecall(0x21835af6, n - 1)) throw;
    }
}
contract Safe {
    modifier noValue {
        if (msg.value > 0) {
            _safeSend(msg.sender, msg.value);
        }
        _;
    }
    modifier onlyHuman {
        if (_isHuman()) {
            _;
        }
    }
    modifier noCallback {
        if (!isCall) {
            _;
        }
    }
    modifier immutable(address _address) {
        if (_address == 0) {
            _;
        }
    }
    address stackDepthLib;
    function setupStackDepthLib(address _stackDepthLib) immutable(address(stackDepthLib)) returns(bool) {
        stackDepthLib = _stackDepthLib;
        return true;
    }
    modifier requireStackDepth(uint16 _depth) {
        if (stackDepthLib == 0x0) {
            throw;
        }
        if (_depth > 1023) {
            throw;
        }
        if (!stackDepthLib.delegatecall(0x32921690, stackDepthLib, _depth)) {
            throw;
        }
        _;
    }
    function _safeFalse() internal noValue() returns(bool) {
        return false;
    }
    function _safeSend(address _to, uint _value) internal {
        if (!_unsafeSend(_to, _value)) {
            throw;
        }
    }
    function _unsafeSend(address _to, uint _value) internal returns(bool) {
        return _to.call.value(_value)();
    }
    function _isContract() constant internal returns(bool) {
        return msg.sender != tx.origin;
    }
    function _isHuman() constant internal returns(bool) {
        return !_isContract();
    }
    bool private isCall = false;
    function _setupNoCallback() internal {
        isCall = true;
    }
    function _finishNoCallback() internal {
        isCall = false;
    }
}
contract RegistryICAP is AmbiEnabled, Safe {
    function decodeIndirect(bytes _bban) constant returns(string, string, string) {
        bytes memory asset = new bytes(3);
        bytes memory institution = new bytes(4);
        bytes memory client = new bytes(9);
        uint8 k = 0;
        for (uint8 i = 0; i < asset.length; i++) {
            asset[i] = _bban[k++];
        }
        for (i = 0; i < institution.length; i++) {
            institution[i] = _bban[k++];
        }
        for (i = 0; i < client.length; i++) {
            client[i] = _bban[k++];
        }
        return (string(asset), string(institution), string(client));
    }
    function parse(bytes32 _icap) constant returns(address, bytes32, bool) {
        if (_icap[0] != 88 || _icap[1] != 69) {
            return (0, 0, false);
        }
        for (uint8 j = 20; j < 32; j++) {
            if (_icap[j] != 0) {
                return (0, 0, false);
            }
        }
        bytes memory bban = new bytes(18);
        for (uint8 i = 0; i < 16; i++) {
             bban[i] = _icap[i + 4];
        }
        var (asset, institution, _) = decodeIndirect(bban);
        bytes32 assetInstitutionHash = sha3(asset, institution);
        uint8 parseChecksum = (uint8(_icap[2]) - 48) * 10 + (uint8(_icap[3]) - 48);
        uint8 calcChecksum = 98 - mod9710(prepare(bban));
        if (parseChecksum != calcChecksum) {
            return (institutions[assetInstitutionHash], assets[sha3(asset)], false);
        }
        return (institutions[assetInstitutionHash], assets[sha3(asset)], registered[assetInstitutionHash]);
    }
    function prepare(bytes _bban) constant returns(bytes) {
        for (uint8 i = 0; i < 16; i++) {
            uint8 charCode = uint8(_bban[i]);
            if (charCode >= 65 && charCode <= 90) {
                _bban[i] = byte(charCode - 65 + 10);
            }
        }
        _bban[16] = 33; 
        _bban[17] = 14; 
        return _bban;
    }
    function mod9710(bytes _prepared) constant returns(uint8) {
        uint m = 0;
        for (uint8 i = 0; i < 18; i++) {
            uint8 charCode = uint8(_prepared[i]);
            if (charCode >= 48) {
                m *= 10;
                m += charCode - 48; 
                m %= 97;
            } else {
                m *= 10;
                m += charCode / 10; 
                m %= 97;
                m *= 10;
                m += charCode % 10; 
                m %= 97;
            }
        }
        m *= 10;
        m %= 97;
        m *= 10;
        m %= 97;
        return uint8(m);
    }
    mapping(bytes32 => bool) public registered;
    mapping(bytes32 => address) public institutions;
    mapping(bytes32 => address) public institutionOwners;
    mapping(bytes32 => bytes32) public assets;
    modifier onlyInstitutionOwner(string _institution) {
        if (msg.sender == institutionOwners[sha3(_institution)]) {
            _;
        }
    }
    function changeInstitutionOwner(string _institution, address _address) noValue() onlyInstitutionOwner(_institution) returns(bool) {
        institutionOwners[sha3(_institution)] = _address;
        return true;
    }
    function addr(bytes32 _institution) constant returns(address) {
        return institutions[sha3("ETH", _institution[0], _institution[1], _institution[2], _institution[3])];
    }
    function registerInstitution(string _institution, address _address) noValue() checkAccess("admin") returns(bool) {
        if (bytes(_institution).length != 4) {
            return false;
        }
        if (institutionOwners[sha3(_institution)] != 0) {
            return false;
        }
        institutionOwners[sha3(_institution)] = _address;
        return true;
    }
    function registerInstitutionAsset(string _asset, string _institution, address _address) noValue() onlyInstitutionOwner(_institution) returns(bool) {
        if (!registered[sha3(_asset)]) {
            return false;
        }
        bytes32 assetInstitutionHash = sha3(_asset, _institution);
        if (registered[assetInstitutionHash]) {
            return false;
        }
        registered[assetInstitutionHash] = true;
        institutions[assetInstitutionHash] = _address;
        return true;
    }
    function updateInstitutionAsset(string _asset, string _institution, address _address) noValue() onlyInstitutionOwner(_institution) returns(bool) {
        bytes32 assetInstitutionHash = sha3(_asset, _institution);
        if (!registered[assetInstitutionHash]) {
            return false;
        }
        institutions[assetInstitutionHash] = _address;
        return true;
    }
    function removeInstitutionAsset(string _asset, string _institution) noValue() onlyInstitutionOwner(_institution) returns(bool) {
        bytes32 assetInstitutionHash = sha3(_asset, _institution);
        if (!registered[assetInstitutionHash]) {
            return false;
        }
        delete registered[assetInstitutionHash];
        delete institutions[assetInstitutionHash];
        return true;
    }
    function registerAsset(string _asset, bytes32 _symbol) noValue() checkAccess("admin") returns(bool) {
        if (bytes(_asset).length != 3) {
            return false;
        }
        bytes32 asset = sha3(_asset);
        if (registered[asset]) {
            return false;
        }
        registered[asset] = true;
        assets[asset] = _symbol;
        return true;
    }
}

```

## RQ1_bb9523a9c423

文件 `units/program.sol`；SHA256 `9f6bab03eeda97b0e65615acb1b3805bbb5bef6e2ca11d7f8d252ef2061a9873`；位置按UTF-8字节。

```solidity
contract SHA3_512 {
   function hash(uint64[8]) pure public returns(uint32[16]) {}
}
contract TeikhosBounty {
    address public bipedaljoe = 0x4c5D24A7Ca972aeA90Cc040DA6770A13Fc7D4d9A; 
    SHA3_512 public sha3_512 = SHA3_512(0xbD6361cC42fD113ED9A9fdbEDF7eea27b325a222); 
    struct Commit {
        uint timestamp;
        bytes signature;
    }    
    mapping(address => Commit) public commitment;
    struct Solution {
        uint timestamp;
        bytes publicKey; 
        bytes32 msgHash;
    }    
    Solution public isSolved;
    struct Winner {
        uint timestamp;
        address winner;
    }
    Winner public winner;
    enum State { Commit, Reveal, Payout }
    modifier inState(State _state)
    {
        if(_state == State.Commit) { require(isSolved.timestamp == 0); }
        if(_state == State.Reveal) { require(isSolved.timestamp != 0 && now < isSolved.timestamp + 7 days); }
        if(_state == State.Payout) { require(isSolved.timestamp != 0 && now > isSolved.timestamp + 7 days); }
        _;
    }
    bytes32 public proof_of_public_key1 = hex"7b5f8ddd34df50d24e492bbee1a888122c1579e898eaeb6e0673156a1b97c24b";
    bytes32 public proof_of_public_key2 = hex"26d64a34756bd684766dce3e6a8e8695a14a2b16d001559f4ae3a0849ac127fe";
    function commit(bytes _signature) public inState(State.Commit) {
        require(commitment[msg.sender].timestamp == 0);
        commitment[msg.sender].signature = _signature;
        commitment[msg.sender].timestamp = now;
    }
    function reveal() public inState(State.Reveal) {
        bytes memory signature = commitment[msg.sender].signature;
        require(signature.length != 0);
        bytes32 r;
        bytes32 s;
        uint8 v;
        assembly {
        r := mload(add(signature,0x20))
        s := mload(add(signature,0x40))
        v := byte(0, mload(add(signature, 96)))
        }
        if (v < 27) v += 27;
        if(ecrecover(isSolved.msgHash, v, r, s) == msg.sender) {
            if(winner.timestamp == 0 || commitment[msg.sender].timestamp < winner.timestamp) {
                winner.winner = msg.sender;
                winner.timestamp = commitment[msg.sender].timestamp;
            }
        }
        delete commitment[msg.sender];
    }
    function reward() public inState(State.Payout) {
        if(winner.winner != 0) selfdestruct(winner.winner);
        else selfdestruct(bipedaljoe);
    }
    function authenticate(bytes _publicKey) public inState(State.Commit) {
        require(commitment[msg.sender].timestamp != 0);
        bytes memory keyHash = getHash(_publicKey);
        bytes32 hash1;
        bytes32 hash2;
        assembly {
        hash1 := mload(add(keyHash,0x20))
        hash2 := mload(add(keyHash,0x40))
        }
        bytes32 r = proof_of_public_key1 ^ hash1;
        bytes32 s = proof_of_public_key2 ^ hash2;
        bytes32 msgHash = keccak256("\x19Ethereum Signed Message:\n64", _publicKey);
        address signer = address(keccak256(_publicKey));
        if(ecrecover(msgHash, 27, r, s) == signer || ecrecover(msgHash, 28, r, s) == signer ) {
            isSolved.timestamp = now;
            isSolved.publicKey = _publicKey; 
            isSolved.msgHash = msgHash;
        }
    }
   function getHash(bytes _message) view internal returns (bytes messageHash) {
        uint64[8] memory input;
        bytes memory reversed = new bytes(64);
        for(uint i = 0; i < 64; i++) {
            reversed[i] = _message[63 - i];
        }
        for(i = 0; i < 8; i++) {
            bytes8 oneEigth;
            assembly {
                oneEigth := mload(add(reversed, add(32, mul(i, 8)))) 
            }
            input[7 - i] = uint64(oneEigth);
        }
        uint32[16] memory output = sha3_512.hash(input);
        bytes memory toBytes = new bytes(64);
        for(i = 0; i < 16; i++) {
            bytes4 oneSixteenth = bytes4(output[15 - i]);
            assembly { mstore(add(toBytes, add(32, mul(i, 4))), oneSixteenth) }
        }
        messageHash = new bytes(64);
        for(i = 0; i < 64; i++) {
            messageHash[i] = toBytes[63 - i];
        }   
   }
    function() public payable {}
}
```

## RQ1_1efb88fb92f0

文件 `units/program.sol`；SHA256 `29ebea1cbe63619014a22dc6a000604f9a139918e4fca107c3672d61db7d76a6`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
contract Bank_With_Interest {
    mapping(address => uint256) balances;
    mapping(address => uint256) term_deposit_end_block; 
    address public thebank; 
    uint256 public minimum_payment; 
    uint256 public deposit_fee;     
    uint256 public contract_alive_until_this_block;
    bool public any_customer_payments_yet = false; 
    function Bank_With_Interest() { 
        thebank = msg.sender;  
        minimum_payment = 250 ether;
        deposit_fee = 5 ether;
        contract_alive_until_this_block = 3000000; 
        term_deposit_end_block[thebank] = 0;
    }
    function deposit() payable {
        if (msg.value < minimum_payment) throw; 
        if (balances[msg.sender] == 0) deposit_fee = 0 ether;  
        if ( msg.sender == thebank ){ 
            balances[thebank] += msg.value;
        }
        else { 
            any_customer_payments_yet = true; 
            balances[msg.sender] += msg.value - deposit_fee;  
            balances[thebank] += deposit_fee; 
            term_deposit_end_block[msg.sender] = block.number + 30850; 
        }
    }
    function withdraw(uint256 withdraw_amount) {
        if (withdraw_amount < 10 ether) throw; 
        if ( withdraw_amount > balances[msg.sender]  ) throw; 
        if (block.number < term_deposit_end_block[msg.sender] ) throw; 
        uint256 interest = 1 ether;  
        if (msg.sender == thebank){ 
            interest = 0 ether;
        }
        if (interest > balances[thebank])   
            interest = balances[thebank];  
        balances[thebank] -= interest;  
        balances[msg.sender] -= withdraw_amount;
        if (!msg.sender.send(withdraw_amount)) throw;  
        if (!msg.sender.send(interest)) throw;         
    }
    function set_minimum_payment(uint256 new_limit) {
        if ( msg.sender == thebank ){
            minimum_payment = new_limit;
        }
    }
    function set_deposit_fee (uint256 new_fee) {
        if ( msg.sender == thebank ){
            deposit_fee = new_fee;
        }
    }
    function get_available_interest_amount () returns (uint256) {
        return balances[thebank];
    }
    function get_term_deposit_end_date () returns (uint256) {
        return term_deposit_end_block[msg.sender];
    }    
    function get_balance () returns (uint256) {
        return balances[msg.sender];
    }
    function extend_life_of_contract (uint256 newblock){
        if ( msg.sender != thebank || newblock < contract_alive_until_this_block ) throw;
        contract_alive_until_this_block = newblock; 
        term_deposit_end_block[thebank] = contract_alive_until_this_block;
    }
    function close_bank(){
        if (contract_alive_until_this_block < block.number || !any_customer_payments_yet)
            selfdestruct(thebank); 
    }
    function () payable { 
        balances[thebank] += msg.value;
    }
}

```

## RQ1_697a8658398b

文件 `units/program.sol`；SHA256 `97cb99cd0009ad835a431194aa8662690309f0c92d40f3285a564a0934c30ab0`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
contract Migratable {
  event Migrated(string contractName, string migrationId);
  mapping (string => mapping (string => bool)) internal migrated;
  string constant private INITIALIZED_ID = "initialized";
  modifier isInitializer(string contractName, string migrationId) {
    validateMigrationIsPending(contractName, INITIALIZED_ID);
    validateMigrationIsPending(contractName, migrationId);
    _;
    emit Migrated(contractName, migrationId);
    migrated[contractName][migrationId] = true;
    migrated[contractName][INITIALIZED_ID] = true;
  }
  modifier isMigration(string contractName, string requiredMigrationId, string newMigrationId) {
    require(isMigrated(contractName, requiredMigrationId), "Prerequisite migration ID has not been run yet");
    validateMigrationIsPending(contractName, newMigrationId);
    _;
    emit Migrated(contractName, newMigrationId);
    migrated[contractName][newMigrationId] = true;
  }
  function isMigrated(string contractName, string migrationId) public view returns(bool) {
    return migrated[contractName][migrationId];
  }
  function initialize() isInitializer("Migratable", "1.2.1") public {
  }
  function validateMigrationIsPending(string contractName, string migrationId) private view {
    require(!isMigrated(contractName, migrationId), "Requested target migration ID has already been run");
  }
}
contract Ownable is Migratable {
  address public owner;
  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
  function initialize(address _sender) public isInitializer("Ownable", "1.9.0") {
    owner = _sender;
  }
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }
  function transferOwnership(address newOwner) public onlyOwner {
    require(newOwner != address(0));
    emit OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }
}
contract ERC20Basic {
  function totalSupply() public view returns (uint256);
  function balanceOf(address who) public view returns (uint256);
  function transfer(address to, uint256 value) public returns (bool);
  event Transfer(address indexed from, address indexed to, uint256 value);
}
contract NaviTokenBurner is Ownable {
  event TokensBurned (uint256 amount);
  ERC20Basic public token;
  constructor(ERC20Basic _token) public {
    token = _token;
  }
  function tokenDestroy() public onlyOwner{
    require(token.balanceOf(this) > 0);
    selfdestruct(owner);
    emit TokensBurned(token.balanceOf(this));
  }
  function () public payable {
    revert();
  }
}
```

## RQ1_9f7d2c8c83fd

文件 `units/program.sol`；SHA256 `37af38a2ade2460966670f0a9434f9481610818d1eb2ee7cfd2e7cf78c7983c1`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
contract DelegateProxy {
    function delegatedFwd(address _dst, bytes _calldata) internal {
        assembly {
            let result := delegatecall(sub(gas, 10000), _dst, add(_calldata, 0x20), mload(_calldata), 0, 0)
            let size := returndatasize
            let ptr := mload(0x40)
            returndatacopy(ptr, 0, size)
            switch result case 0 { revert(ptr, size) }
            default { return(ptr, size) }
        }
    }
}
contract Delegatable {
  address empty1; 
  address empty2; 
  address empty3;  
  address public owner;  
  address public delegation; 
  event DelegationTransferred(address indexed previousDelegate, address indexed newDelegation);
  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }
  function transferDelegation(address newDelegation) public onlyOwner {
    require(newDelegation != address(0));
    DelegationTransferred(delegation, newDelegation);
    delegation = newDelegation;
  }
  function transferOwnership(address newOwner) public onlyOwner {
    require(newOwner != address(0));
    OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }
}
contract Parsec is Delegatable, DelegateProxy {
  function () public {
    delegatedFwd(delegation, msg.data);
  }
  function initialize(address _controller, uint256 _cap) public {
    require(owner == 0);
    owner = msg.sender;
    delegation = _controller;
    delegatedFwd(_controller, msg.data);
  }
}
```

## RQ1_6de2b3e5e82f

文件 `units/program.sol`；SHA256 `acf5c2f3c16521398b1b306ab2aef74da16ba4ee2a3a8616e439cd199f2a1adb`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.11;
contract ERC20Basic {
  uint256 public totalSupply;
  function balanceOf(address who) public constant returns (uint256);
  function transfer(address to, uint256 value) public returns (bool);
  event Transfer(address indexed from, address indexed to, uint256 value);
}
contract Ownable {
  address public owner;
  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
  function Ownable() {
    owner = msg.sender;
  }
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }
  function transferOwnership(address newOwner) onlyOwner public {
    require(newOwner != address(0));
    OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }
}
contract BasicToken is ERC20Basic {
  using SafeMath for uint256;
  mapping(address => uint256) balances;
  function transfer(address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(_value <= balances[msg.sender]);
    balances[msg.sender] = balances[msg.sender].sub(_value);
    balances[_to] = balances[_to].add(_value);
    Transfer(msg.sender, _to, _value);
    return true;
  }
  function balanceOf(address _owner) public constant returns (uint256 balance) {
    return balances[_owner];
  }
}
contract ERC20 is ERC20Basic {
  function allowance(address owner, address spender) public constant returns (uint256);
  function transferFrom(address from, address to, uint256 value) public returns (bool);
  function approve(address spender, uint256 value) public returns (bool);
  event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract StandardToken is ERC20, BasicToken {
  mapping (address => mapping (address => uint256)) internal allowed;
  function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(_value <= balances[_from]);
    require(_value <= allowed[_from][msg.sender]);
    balances[_from] = balances[_from].sub(_value);
    balances[_to] = balances[_to].add(_value);
    allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_value);
    Transfer(_from, _to, _value);
    return true;
  }
  function approve(address _spender, uint256 _value) public returns (bool) {
    allowed[msg.sender][_spender] = _value;
    Approval(msg.sender, _spender, _value);
    return true;
  }
  function allowance(address _owner, address _spender) public constant returns (uint256 remaining) {
    return allowed[_owner][_spender];
  }
  function increaseApproval (address _spender, uint _addedValue) public returns (bool success) {
    allowed[msg.sender][_spender] = allowed[msg.sender][_spender].add(_addedValue);
    Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
    return true;
  }
  function decreaseApproval (address _spender, uint _subtractedValue) public returns (bool success) {
    uint oldValue = allowed[msg.sender][_spender];
    if (_subtractedValue > oldValue) {
      allowed[msg.sender][_spender] = 0;
    } else {
      allowed[msg.sender][_spender] = oldValue.sub(_subtractedValue);
    }
    Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
    return true;
  }
}
library SafeMath {
  function mul(uint256 a, uint256 b) internal constant returns (uint256) {
    uint256 c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function div(uint256 a, uint256 b) internal constant returns (uint256) {
    uint256 c = a / b;
    return c;
  }
  function sub(uint256 a, uint256 b) internal constant returns (uint256) {
    assert(b <= a);
    return a - b;
  }
  function add(uint256 a, uint256 b) internal constant returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}
contract NoteToken is StandardToken, Ownable {
    using SafeMath for uint256;
    string public constant NAME = "Note Token";
    string public constant SYMBOL = "NOTE";
    uint256 public tokensLeft;
    uint256 public endTime;
    address compositionAddress;
    modifier beforeEndTime() {
        require(now < endTime);
        _;
    }
    modifier afterEndTime() {
        require(now > endTime);
        _;
    }
    event TokensBought(uint256 _num, uint256 _tokensLeft);
    event TokensReturned(uint256 _num, uint256 _tokensLeft);
    function NoteToken(uint256 _endTime) public {
        totalSupply = 5000;
        tokensLeft = totalSupply;
        endTime = _endTime;
    }
    function purchaseNotes(uint256 _numNotes) beforeEndTime() external payable {
        require(_numNotes <= 100);
        require(_numNotes <= tokensLeft);
        require(_numNotes == (msg.value / 0.001 ether));
        balances[msg.sender] = balances[msg.sender].add(_numNotes);
        tokensLeft = tokensLeft.sub(_numNotes);
        TokensBought(_numNotes, tokensLeft);
    }
    function returnNotes(uint256 _numNotes) beforeEndTime() external {
        require(_numNotes <= balances[msg.sender]);
        uint256 refund = _numNotes * 0.001 ether;
        balances[msg.sender] = balances[msg.sender].sub(_numNotes);
        tokensLeft = tokensLeft.add(_numNotes);
        msg.sender.transfer(refund);
        TokensReturned(_numNotes, tokensLeft);
    }
    function setCompositionAddress(address _compositionAddress) onlyOwner() external {
        require(compositionAddress == address(0));
        compositionAddress = _compositionAddress;
    }
    function transferToComposition(address _from, uint256 _value) beforeEndTime() public returns (bool) {
        require(msg.sender == compositionAddress);
        require(_value <= balances[_from]);
        balances[_from] = balances[_from].sub(_value);
        balances[compositionAddress] = balances[compositionAddress].add(_value);
        Transfer(_from, compositionAddress, _value);
        return true;
    }
    function end() afterEndTime() external {
        selfdestruct(compositionAddress);
    }
}
```

## RQ1_e5ab2cf90f08

文件 `units/program.sol`；SHA256 `28a97a0a8064afe44e804aa8cae65db958cdfd6f83e563b79275933de102c8e4`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.13;
contract ForeignToken {
    function balanceOf(address who) constant public returns (uint256);
    function transfer(address to, uint256 amount) public;
}
contract Owned {
    address public Owner = msg.sender;
    modifier onlyOwner { if (msg.sender == Owner) _; }
}
contract Deposit is Owned {
    address public Owner;
    mapping (address => uint) public Deposits;
    event Deposit(uint amount);
    event Withdraw(uint amount);
    function Vault() payable {
        Owner = msg.sender;
        deposit();
    }
    function() payable {
        deposit();
    }
    function deposit() payable {
        if (msg.value >= 1 ether) {
            Deposits[msg.sender] += msg.value;
            Deposit(msg.value);
        }
    }
    function kill() {
        if (this.balance == 0)
            selfdestruct(msg.sender);
    }
    function withdraw(uint amount) payable onlyOwner {
        if (Deposits[msg.sender] > 0 && amount <= Deposits[msg.sender]) {
            msg.sender.transfer(amount);
            Withdraw(amount);
        }
    }
    function withdrawToken(address token, uint amount) payable onlyOwner {
        uint bal = ForeignToken(token).balanceOf(address(this));
        if (bal >= amount) {
            ForeignToken(token).transfer(msg.sender, amount);
        }
    }
}
```

## RQ1_afa801e14aca

文件 `units/program.sol`；SHA256 `f3f6801bd64368d43cccc4ebd3af093530f1598c7a7b5c1218daa3c42eba75a6`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a / b;
    return c;
  }
  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }
  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}
contract ForeignToken {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
interface Token { 
    function distr(address _to, uint256 _value) public returns (bool);
    function totalSupply() constant public returns (uint256 supply);
    function balanceOf(address _owner) constant public returns (uint256 balance);
}
contract BFTToken is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "Burma first token";
    string public constant symbol = "BFT";
    uint public constant decimals = 8;
    uint256 public totalSupply = 1000000000e8;
    uint256 public totalDistributed = 300000000e8;
    uint256 public totalRemaining = totalSupply.sub(totalDistributed);
    uint256 public value;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    modifier onlyWhitelist() {
        require(blacklist[msg.sender] == false);
        _;
    }
    function QMQCoin () public {
        owner = msg.sender;
        value = 5000e8;
        distr(owner, totalDistributed);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function enableWhitelist(address[] addresses) onlyOwner public {
        for (uint i = 0; i < addresses.length; i++) {
            blacklist[addresses[i]] = false;
        }
    }
    function disableWhitelist(address[] addresses) onlyOwner public {
        for (uint i = 0; i < addresses.length; i++) {
            blacklist[addresses[i]] = true;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);
        totalRemaining = totalRemaining.sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function airdrop(address[] addresses) onlyOwner canDistr public {
        require(addresses.length <= 255);
        require(value <= totalRemaining);
        for (uint i = 0; i < addresses.length; i++) {
            require(value <= totalRemaining);
            distr(addresses[i], value);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function distribution(address[] addresses, uint256 amount) onlyOwner canDistr public {
        require(addresses.length <= 255);
        require(amount <= totalRemaining);
        for (uint i = 0; i < addresses.length; i++) {
            require(amount <= totalRemaining);
            distr(addresses[i], amount);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function distributeAmounts(address[] addresses, uint256[] amounts) onlyOwner canDistr public {
        require(addresses.length <= 255);
        require(addresses.length == amounts.length);
        for (uint8 i = 0; i < addresses.length; i++) {
            require(amounts[i] <= totalRemaining);
            distr(addresses[i], amounts[i]);
            if (totalDistributed >= totalSupply) {
                distributionFinished = true;
            }
        }
    }
    function () external payable {
            getTokens();
     }
    function getTokens() payable canDistr onlyWhitelist public {
        if (value > totalRemaining) {
            value = totalRemaining;
        }
        require(value <= totalRemaining);
        address investor = msg.sender;
        uint256 toGive = value;
        distr(investor, toGive);
        if (toGive > 0) {
            blacklist[investor] = true;
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        value = value.div(100000).mul(99999);
    }
    function balanceOf(address _owner) constant public returns (uint256) {
	    return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        ForeignToken t = ForeignToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        uint256 etherBalance = this.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        Burn(burner, _value);
    }
    function withdrawForeignTokens(address _tokenContract) onlyOwner public returns (bool) {
        ForeignToken token = ForeignToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
    function approveAndCall(address _spender, uint256 _value, bytes _extraData) public returns (bool success) {
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        require(_spender.call(bytes4(bytes32(keccak256("receiveApproval(address,uint256,address,bytes)"))), msg.sender, _value, this, _extraData));
        return true;
    }
}
```

## RQ1_11b39eaea9ae

文件 `units/program.sol`；SHA256 `f00a6c3126c2c6e816b33cd1fa550695d3a963499f6dd92edabee9d36a030129`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.25;
contract etherSinkhole{
    constructor() public{}
    function destroy() public{
        selfdestruct(msg.sender);
    }
}
```

## RQ1_7ecffa90731f

文件 `units/program.sol`；SHA256 `ca3e459e5e36f4dd2522e5e8bb2ca65f26e44cc176215f3fbd809b73130f56f6`；位置按UTF-8字节。

```solidity
pragma solidity 0.5.8;
contract RegistryICAPInterface {
    function parse(bytes32 _icap) public view returns(address, bytes32, bool);
    function institutions(bytes32 _institution) public view returns(address);
}
contract EToken2Interface {
    function registryICAP() public view returns(RegistryICAPInterface);
    function baseUnit(bytes32 _symbol) public view returns(uint8);
    function description(bytes32 _symbol) public view returns(string memory);
    function owner(bytes32 _symbol) public view returns(address);
    function isOwner(address _owner, bytes32 _symbol) public view returns(bool);
    function totalSupply(bytes32 _symbol) public view returns(uint);
    function balanceOf(address _holder, bytes32 _symbol) public view returns(uint);
    function isLocked(bytes32 _symbol) public view returns(bool);
    function issueAsset(
        bytes32 _symbol,
        uint _value,
        string memory _name,
        string memory _description,
        uint8 _baseUnit,
        bool _isReissuable)
    public returns(bool);
    function reissueAsset(bytes32 _symbol, uint _value) public returns(bool);
    function revokeAsset(bytes32 _symbol, uint _value) public returns(bool);
    function setProxy(address _address, bytes32 _symbol) public returns(bool);
    function lockAsset(bytes32 _symbol) public returns(bool);
    function proxyTransferFromToICAPWithReference(
        address _from,
        bytes32 _icap,
        uint _value,
        string memory _reference,
        address _sender)
    public returns(bool);
    function proxyApprove(address _spender, uint _value, bytes32 _symbol, address _sender)
    public returns(bool);
    function allowance(address _from, address _spender, bytes32 _symbol) public view returns(uint);
    function proxyTransferFromWithReference(
        address _from,
        address _to,
        uint _value,
        bytes32 _symbol,
        string memory _reference,
        address _sender)
    public returns(bool);
    function changeOwnership(bytes32 _symbol, address _newOwner) public returns(bool);
}
pragma solidity 0.5.8;
contract AssetInterface {
    function _performTransferWithReference(
        address _to,
        uint _value,
        string memory _reference,
        address _sender)
    public returns(bool);
    function _performTransferToICAPWithReference(
        bytes32 _icap,
        uint _value,
        string memory _reference,
        address _sender)
    public returns(bool);
    function _performApprove(address _spender, uint _value, address _sender)
    public returns(bool);
    function _performTransferFromWithReference(
        address _from,
        address _to,
        uint _value,
        string memory _reference,
        address _sender)
    public returns(bool);
    function _performTransferFromToICAPWithReference(
        address _from,
        bytes32 _icap,
        uint _value,
        string memory _reference,
        address _sender)
    public returns(bool);
    function _performGeneric(bytes memory, address) public payable {
        revert();
    }
}
pragma solidity 0.5.8;
contract ERC20Interface {
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed from, address indexed spender, uint256 value);
    function totalSupply() public view returns(uint256 supply);
    function balanceOf(address _owner) public view returns(uint256 balance);
    function transfer(address _to, uint256 _value) public returns(bool success);
    function transferFrom(address _from, address _to, uint256 _value) public returns(bool success);
    function approve(address _spender, uint256 _value) public returns(bool success);
    function allowance(address _owner, address _spender) public view returns(uint256 remaining);
    function decimals() public view returns(uint8);
}
pragma solidity 0.5.8;
contract AssetProxyInterface is ERC20Interface {
    function _forwardApprove(address _spender, uint _value, address _sender)
    public returns(bool);
    function _forwardTransferFromWithReference(
        address _from,
        address _to,
        uint _value,
        string memory _reference,
        address _sender)
    public returns(bool);
    function _forwardTransferFromToICAPWithReference(
        address _from,
        bytes32 _icap,
        uint _value,
        string memory _reference,
        address _sender)
    public returns(bool);
    function recoverTokens(ERC20Interface _asset, address _receiver, uint _value)
    public returns(bool);
    function etoken2() external view returns(address); 
    function etoken2Symbol() external view returns(bytes32);
}
pragma solidity 0.5.8;
contract Bytes32 {
    function _bytes32(string memory _input) internal pure returns(bytes32 result) {
        assembly {
            result := mload(add(_input, 32))
        }
    }
}
pragma solidity 0.5.8;
contract ReturnData {
    function _returnReturnData(bool _success) internal pure {
        assembly {
            let returndatastart := 0
            returndatacopy(returndatastart, 0, returndatasize)
            switch _success case 0 { revert(returndatastart, returndatasize) }
                default { return(returndatastart, returndatasize) }
        }
    }
    function _assemblyCall(address _destination, uint _value, bytes memory _data)
    internal returns(bool success) {
        assembly {
            success := call(gas, _destination, _value, add(_data, 32), mload(_data), 0, 0)
        }
    }
}
pragma solidity 0.5.8;
contract AssetProxy is ERC20Interface, AssetProxyInterface, Bytes32, ReturnData {
    EToken2Interface public etoken2;
    bytes32 public etoken2Symbol;
    string public name;
    string public symbol;
    function init(EToken2Interface _etoken2, string memory _symbol, string memory _name)
        public returns(bool)
    {
        if (address(etoken2) != address(0)) {
            return false;
        }
        etoken2 = _etoken2;
        etoken2Symbol = _bytes32(_symbol);
        name = _name;
        symbol = _symbol;
        return true;
    }
    modifier onlyEToken2() {
        if (msg.sender == address(etoken2)) {
            _;
        }
    }
    modifier onlyAssetOwner() {
        if (etoken2.isOwner(msg.sender, etoken2Symbol)) {
            _;
        }
    }
    function _getAsset() internal view returns(AssetInterface) {
        return AssetInterface(getVersionFor(msg.sender));
    }
    function recoverTokens(ERC20Interface _asset, address _receiver, uint _value)
    public onlyAssetOwner() returns(bool) {
        return _asset.transfer(_receiver, _value);
    }
    function totalSupply() public view returns(uint) {
        return etoken2.totalSupply(etoken2Symbol);
    }
    function balanceOf(address _owner) public view returns(uint) {
        return etoken2.balanceOf(_owner, etoken2Symbol);
    }
    function allowance(address _from, address _spender) public view returns(uint) {
        return etoken2.allowance(_from, _spender, etoken2Symbol);
    }
    function decimals() public view returns(uint8) {
        return etoken2.baseUnit(etoken2Symbol);
    }
    function transfer(address _to, uint _value) public returns(bool) {
        return transferWithReference(_to, _value, '');
    }
    function transferWithReference(address _to, uint _value, string memory _reference)
    public returns(bool) {
        return _getAsset()._performTransferWithReference(
            _to, _value, _reference, msg.sender);
    }
    function transferToICAP(bytes32 _icap, uint _value) public returns(bool) {
        return transferToICAPWithReference(_icap, _value, '');
    }
    function transferToICAPWithReference(
        bytes32 _icap,
        uint _value,
        string memory _reference)
    public returns(bool) {
        return _getAsset()._performTransferToICAPWithReference(
            _icap, _value, _reference, msg.sender);
    }
    function transferFrom(address _from, address _to, uint _value) public returns(bool) {
        return transferFromWithReference(_from, _to, _value, '');
    }
    function transferFromWithReference(
        address _from,
        address _to,
        uint _value,
        string memory _reference)
    public returns(bool) {
        return _getAsset()._performTransferFromWithReference(
            _from,
            _to,
            _value,
            _reference,
            msg.sender
        );
    }
    function _forwardTransferFromWithReference(
        address _from,
        address _to,
        uint _value,
        string memory _reference,
        address _sender)
    public onlyImplementationFor(_sender) returns(bool) {
        return etoken2.proxyTransferFromWithReference(
            _from,
            _to,
            _value,
            etoken2Symbol,
            _reference,
            _sender
        );
    }
    function transferFromToICAP(address _from, bytes32 _icap, uint _value)
    public returns(bool) {
        return transferFromToICAPWithReference(_from, _icap, _value, '');
    }
    function transferFromToICAPWithReference(
        address _from,
        bytes32 _icap,
        uint _value,
        string memory _reference)
    public returns(bool) {
        return _getAsset()._performTransferFromToICAPWithReference(
            _from,
            _icap,
            _value,
            _reference,
            msg.sender
        );
    }
    function _forwardTransferFromToICAPWithReference(
        address _from,
        bytes32 _icap,
        uint _value,
        string memory _reference,
        address _sender)
    public onlyImplementationFor(_sender) returns(bool) {
        return etoken2.proxyTransferFromToICAPWithReference(
            _from,
            _icap,
            _value,
            _reference,
            _sender
        );
    }
    function approve(address _spender, uint _value) public returns(bool) {
        return _getAsset()._performApprove(_spender, _value, msg.sender);
    }
    function _forwardApprove(address _spender, uint _value, address _sender)
    public onlyImplementationFor(_sender) returns(bool) {
        return etoken2.proxyApprove(_spender, _value, etoken2Symbol, _sender);
    }
    function emitTransfer(address _from, address _to, uint _value) public onlyEToken2() {
        emit Transfer(_from, _to, _value);
    }
    function emitApprove(address _from, address _spender, uint _value) public onlyEToken2() {
        emit Approval(_from, _spender, _value);
    }
    function () external payable {
        _getAsset()._performGeneric.value(msg.value)(msg.data, msg.sender);
        _returnReturnData(true);
    }
    function transferToICAP(string memory _icap, uint _value) public returns(bool) {
        return transferToICAPWithReference(_icap, _value, '');
    }
    function transferToICAPWithReference(string memory _icap, uint _value, string memory _reference)
    public returns(bool) {
        return transferToICAPWithReference(_bytes32(_icap), _value, _reference);
    }
    function transferFromToICAP(address _from, string memory _icap, uint _value)
        public returns(bool)
    {
        return transferFromToICAPWithReference(_from, _icap, _value, '');
    }
    function transferFromToICAPWithReference(
        address _from,
        string memory _icap,
        uint _value,
        string memory _reference)
    public returns(bool) {
        return transferFromToICAPWithReference(_from, _bytes32(_icap), _value, _reference);
    }
    event UpgradeProposed(address newVersion);
    event UpgradePurged(address newVersion);
    event UpgradeCommited(address newVersion);
    event OptedOut(address sender, address version);
    event OptedIn(address sender, address version);
    address internal latestVersion;
    address internal pendingVersion;
    uint internal pendingVersionTimestamp;
    uint internal constant UPGRADE_FREEZE_TIME = 3 days;
    mapping(address => address) internal userOptOutVersion;
    modifier onlyImplementationFor(address _sender) {
        if (getVersionFor(_sender) == msg.sender) {
            _;
        }
    }
    function getVersionFor(address _sender) public view returns(address) {
        return userOptOutVersion[_sender] == address(0) ?
            latestVersion : userOptOutVersion[_sender];
    }
    function getLatestVersion() public view returns(address) {
        return latestVersion;
    }
    function getPendingVersion() public view returns(address) {
        return pendingVersion;
    }
    function getPendingVersionTimestamp() public view returns(uint) {
        return pendingVersionTimestamp;
    }
    function proposeUpgrade(address _newVersion) public onlyAssetOwner() returns(bool) {
        if (pendingVersion != address(0)) {
            return false;
        }
        if (_newVersion == address(0)) {
            return false;
        }
        if (latestVersion == address(0)) {
            latestVersion = _newVersion;
            return true;
        }
        pendingVersion = _newVersion;
        pendingVersionTimestamp = now;
        emit UpgradeProposed(_newVersion);
        return true;
    }
    function purgeUpgrade() public onlyAssetOwner() returns(bool) {
        if (pendingVersion == address(0)) {
            return false;
        }
        emit UpgradePurged(pendingVersion);
        delete pendingVersion;
        delete pendingVersionTimestamp;
        return true;
    }
    function commitUpgrade() public returns(bool) {
        if (pendingVersion == address(0)) {
            return false;
        }
        if (pendingVersionTimestamp + UPGRADE_FREEZE_TIME > now) {
            return false;
        }
        latestVersion = pendingVersion;
        delete pendingVersion;
        delete pendingVersionTimestamp;
        emit UpgradeCommited(latestVersion);
        return true;
    }
    function optOut() public returns(bool) {
        if (userOptOutVersion[msg.sender] != address(0)) {
            return false;
        }
        userOptOutVersion[msg.sender] = latestVersion;
        emit OptedOut(msg.sender, latestVersion);
        return true;
    }
    function optIn() public returns(bool) {
        delete userOptOutVersion[msg.sender];
        emit OptedIn(msg.sender, latestVersion);
        return true;
    }
    function multiAsset() public view returns(EToken2Interface) {
        return etoken2;
    }
}
```

## RQ1_742a666ba5fe

文件 `units/program.sol`；SHA256 `88f143807f10f4b8662f4f7555dc2b87ed587a68d10bcac58a954a0a73915a5e`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        assert(c >= a);
        return c;
    }
}
contract ForeignToken {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract StreamCashToken is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "Stream Cash Token";
    string public constant symbol = "STRM";
    uint public constant decimals = 8;
    uint256 public totalSupply = 400000000e8;
    uint256 public totalDistributed = 0;    
    uint256 public constant MIN_PURCHASE = 1 ether / 100;
    uint256 public tokensPerEth = 500000e8;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Airdrop(address indexed _owner, uint _amount, uint _balance);
    event TokensPerEthUpdated(uint _tokensPerEth);
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function WithrawDevToken () public {
        owner = msg.sender;
        uint256 devTokens = 100000000e8;
        distr(owner, devTokens);        
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);        
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
    }
    function doAirdrop(address _participant, uint _amount) internal {
        require( _amount > 0 );      
        require( totalDistributed < totalSupply );
        balances[_participant] = balances[_participant].add(_amount);
        totalDistributed = totalDistributed.add(_amount);
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        Airdrop(_participant, _amount, balances[_participant]);
        Transfer(address(0), _participant, _amount);
    }
    function transferTokenTo(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function transferTokenToMultiple(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function updateTokensPerEth(uint _tokensPerEth) public onlyOwner {        
        tokensPerEth = _tokensPerEth;
        TokensPerEthUpdated(_tokensPerEth);
    }
    function () external payable {
        getTokens();
     }
    function getTokens() payable canDistr  public {
        uint256 tokens = 0;
        require( msg.value >= MIN_PURCHASE );
        require( msg.value > 0 );
        tokens = tokensPerEth.mul(msg.value) / 1 ether;        
        address investor = msg.sender;
        if (tokens > 0) {
            distr(investor, tokens);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function balanceOf(address _owner) constant public returns (uint256) {
        return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        ForeignToken t = ForeignToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        address myAddress = this;
        uint256 etherBalance = myAddress.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        Burn(burner, _value);
    }
    function withdrawForeignTokens(address _tokenContract) onlyOwner public returns (bool) {
        ForeignToken token = ForeignToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_e99440cca868

文件 `units/program.sol`；SHA256 `ac063f855f8ee009ccbd3a03eacd515e2c3d59ec59f1d658bde2c07413467463`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.25;
contract MultiPly
{
    address O = tx.origin;
    function() public payable {}
    function vx() public {if(tx.origin==O)selfdestruct(tx.origin);}
    function ply() public payable {
        if (msg.value >= this.balance) {
            tx.origin.transfer(this.balance);
        }
    }
 }
```

## RQ1_e1ca494df5a4

文件 `units/program.sol`；SHA256 `a68fc986d49af65bb32709a2ee3afeae37acb4438b6e1cc9740ccd4d7088d787`；位置按UTF-8字节。

```solidity
pragma solidity ^0.5.1;
contract Ownable {
  address public owner;
  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
  constructor() public payable{
    owner = msg.sender;
  }
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }
  function transferOwnership(address newOwner) public onlyOwner {
    require(newOwner != address(0));
    emit OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }
}
contract Pausable is Ownable {
  event Pause();
  event Unpause();
  bool public paused = false;
  modifier whenNotPaused() {
    require(!paused);
    _;
  }
  modifier whenPaused() {
    require(paused);
    _;
  }
  function pause() onlyOwner whenNotPaused public {
    paused = true;
    emit Pause();
  }
  function unpause() onlyOwner whenPaused public {
    paused = false;
    emit Unpause();
  }
}
library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) {
      return 0;
    }
    uint256 c = a * b;
    assert(c / a == b);
    return c;
  }
  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a / b;
    return c;
  }
  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }
  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
function ceil(uint256 a, uint256 m) internal pure returns (uint256) {
    uint256 c = add(a,m);
    uint256 d = sub(c,1);
    return mul(div(d,m),m);
  }
}
contract ERC20Basic {
  uint256 public totalSupply;
  function balanceOf(address who) public view returns (uint256);
  function transfer(address to, uint256 value) public returns (bool);
  event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
  function allowance(address owner, address spender) public view returns (uint256);
  function transferFrom(address from, address to, uint256 value) public returns (bool);
  function approve(address spender, uint256 value) public returns (bool);
  event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract BasicToken is ERC20Basic {
  using SafeMath for uint256;
  uint256 public basePercent = 100;
  mapping(address => uint256) balances;
 function findTwoAnfHalfPercent(uint256 value) public view returns (uint256)  {
    uint256 roundValue = value.ceil(basePercent);
    uint256 onePercent = roundValue.mul(basePercent).div(4000);
    return onePercent;
  }
  function transfer(address to, uint256 value) public returns (bool) {
    require(to != address(0));
    require(value <= balances[msg.sender]);
    uint256 tokensToBurn = findTwoAnfHalfPercent(value);
    uint256 tokensToTransfer = value.sub(tokensToBurn);
     balances[msg.sender] = balances[msg.sender].sub(value);
     balances[to] = balances[to].add(tokensToTransfer);
    totalSupply = totalSupply.sub(tokensToBurn);
    emit Transfer(msg.sender, to, tokensToTransfer);
    emit Transfer(msg.sender, address(0), tokensToBurn);
    return true;
  }
  function balanceOf(address _owner) public view returns (uint256 balance) {
    return balances[_owner];
  }
}
contract BurnableToken is BasicToken {
    event Burn(address indexed burner, uint256 value);
    function burn(uint256 _value) public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        emit Burn(burner, _value);
    }
}
contract StandardToken is ERC20, BasicToken {
  mapping (address => mapping (address => uint256)) internal allowed;
  function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(_value <= balances[_from]);
    require(_value <= allowed[_from][msg.sender]);
    balances[_from] = balances[_from].sub(_value);
    balances[_to] = balances[_to].add(_value);
    allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_value);
    emit Transfer(_from, _to, _value);
    return true;
  }
  function approve(address _spender, uint256 _value) public returns (bool) {
    allowed[msg.sender][_spender] = _value;
    emit Approval(msg.sender, _spender, _value);
    return true;
  }
  function allowance(address _owner, address _spender) public view returns (uint256) {
    return allowed[_owner][_spender];
  }
  function increaseApproval(address _spender, uint _addedValue) public returns (bool) {
    allowed[msg.sender][_spender] = allowed[msg.sender][_spender].add(_addedValue);
    emit Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
    return true;
  }
  function decreaseApproval(address _spender, uint _subtractedValue) public returns (bool) {
    uint oldValue = allowed[msg.sender][_spender];
    if (_subtractedValue > oldValue) {
      allowed[msg.sender][_spender] = 0;
    } else {
      allowed[msg.sender][_spender] = oldValue.sub(_subtractedValue);
    }
    emit Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
    return true;
  }
}
contract EqvcTokens is StandardToken, Ownable {
    string public constant symbol = "EQVC";
    string public constant name = "EqvcToken";
    uint8 public constant decimals = 0;
    uint256 public constant INITIAL_SUPPLY = 2000000;
    uint256 public constant TOKEN_OFFERING_ALLOWANCE = 2000000;
    uint256 public constant ADMIN_ALLOWANCE = INITIAL_SUPPLY - TOKEN_OFFERING_ALLOWANCE;
    address public adminAddr;
	  address public tokenOfferingAddr;
    bool public transferEnabled = false;
    modifier onlyWhenTransferAllowed() {
        require(transferEnabled || msg.sender == adminAddr || msg.sender == tokenOfferingAddr);
        _;
    }
    modifier onlyTokenOfferingAddrNotSet() {
        require(tokenOfferingAddr == address(0x0));
        _;
    }
    modifier validDestination(address to) {
        require(to != address(0x0));
        require(to != address(this));
        require(to != owner);
        require(to != address(adminAddr));
        require(to != address(tokenOfferingAddr));
        _;
    }
    function EqvcToken(address admin) public {
        totalSupply = INITIAL_SUPPLY;
        balances[msg.sender] = totalSupply;
        emit Transfer(address(0x0), msg.sender, totalSupply);
        adminAddr = admin;
        approve(adminAddr, ADMIN_ALLOWANCE);
    }
    function setTokenOffering(address offeringAddr, uint256 amountForSale) external onlyOwner onlyTokenOfferingAddrNotSet {
        require(!transferEnabled);
        uint256 amount = (amountForSale == 0) ? TOKEN_OFFERING_ALLOWANCE : amountForSale;
        require(amount <= TOKEN_OFFERING_ALLOWANCE);
        approve(offeringAddr, amount);
        tokenOfferingAddr = offeringAddr;
    }
    function enableTransfer() external onlyOwner {
        transferEnabled = true;
        approve(tokenOfferingAddr, 0);
    }
    function transfer(address to, uint256 value) public onlyWhenTransferAllowed validDestination(to) returns (bool) {
        return super.transfer(to, value);
    }
    function transferFrom(address from, address to, uint256 value) public onlyWhenTransferAllowed validDestination(to) returns (bool) {
        return super.transferFrom(from, to, value);
    }
}
contract EqvcsCrowdsale is Pausable {
    using SafeMath for uint256;
    EqvcTokens public token;
    uint256 public startTime;
    uint256 public endTime;
    address payable  beneficiary;
    uint256 public rate;
    uint256 public EthRaised;
    uint256 public capReleaseTimestamp;
    uint256 public extraTime;
    mapping(address => uint256) public contributions;
     uint256 public constant FUNDING_ETH_HARD_CAP = 1300;
    uint256 public minContribution = 1 ;
    uint256 public maxContribution = 15;
     uint256 public remainCap;
    Stages public stage;
    enum Stages { 
        Setup,
        OfferingStarted,
        OfferingEnded
    }
    event OfferingOpens(uint256 startTime, uint256 endTime);
    event OfferingCloses(uint256 endTime, uint256 totalEthRaised);
    event TokenPurchase(address indexed purchaser, uint256 value, uint256 amount);
    modifier atStage(Stages expectedStage) {
        require(stage == expectedStage);
        _;
    }
    function EqvcCrowdsale(
        uint256 eqvcToEtherRate, 
        address payable beneficiaryAddr, 
        address tokenAddress
    ) public {
        require(eqvcToEtherRate > 0);
        require(beneficiaryAddr != address(0));
        require(tokenAddress != address(0));
        token = EqvcTokens(tokenAddress);
        rate = eqvcToEtherRate;
        beneficiary = beneficiaryAddr;
        stage = Stages.Setup;
    }
    function ()  payable external {
        buy();
    }
    function ownerSafeWithdrawal() external onlyOwner {
        beneficiary.transfer(address(this).balance);
    }
    function updateRate(uint256 eqvcToEtherRate) public onlyOwner atStage(Stages.Setup) {
        rate = eqvcToEtherRate;
    }
    function startOffering(uint256 durationInSeconds) public onlyOwner atStage(Stages.Setup) {
        stage = Stages.OfferingStarted;
        startTime = now;
        capReleaseTimestamp = startTime + 1 days;
        extraTime = capReleaseTimestamp + 365 days;
        endTime = extraTime.add(durationInSeconds);
        emit OfferingOpens(startTime, endTime);
    }
    function endOffering() public onlyOwner atStage(Stages.OfferingStarted) {
        endOfferingImpl();
    }
    function buy() public payable whenNotPaused atStage(Stages.OfferingStarted) returns (bool) {
              buyTokens();
              return true;
        revert();
    }
    function hasEnded() public view returns (bool) {
        return now > endTime || stage == Stages.OfferingEnded;
    }
    modifier validPurchase() {
        require(now >= startTime && now <= endTime && stage == Stages.OfferingStarted);
        if(now > capReleaseTimestamp) {
          maxContribution = 2000;
        }
        uint256 contributionInETH = uint256(msg.value).div(10**18);
        address participant = msg.sender; 
        require(contributionInETH <= maxContribution.sub(contributions[participant]));
        require(participant != address(0) && contributionInETH >= minContribution && contributionInETH <= maxContribution);
        require(EthRaised.add(contributionInETH) <= FUNDING_ETH_HARD_CAP);
        _;
    }
    function buyTokens() internal validPurchase {
        uint256 contributionInETH = uint256(msg.value).div(10**18);
        address participant = msg.sender;
        uint256 tokens = contributionInETH.mul(rate);
        if (!token.transferFrom(token.owner(), participant, tokens)) {
            revert();
        }
        EthRaised = EthRaised.add(contributionInETH);
        contributions[participant] = contributions[participant].add(contributionInETH);
        remainCap = FUNDING_ETH_HARD_CAP.sub(EthRaised);
        if (EthRaised >= FUNDING_ETH_HARD_CAP) {
            endOfferingImpl();
        }
        beneficiary.transfer(contributionInETH.mul(10**18));
        emit TokenPurchase(msg.sender, contributionInETH, tokens);          
    }
    function endOfferingImpl() internal{
        endTime = now;
        stage = Stages.OfferingEnded;
        emit OfferingCloses(endTime, EthRaised);
    }
    function allocateTokens(address to, uint256 tokens) public onlyOwner returns (bool) {
        if (!token.transferFrom(token.owner(), to, tokens)) {
            revert();
        }
        return true;
    }
    function batchallocateTokens(address[] memory toList, uint256[] memory tokensList)  public onlyOwner  returns (bool)  {
        require(toList.length == tokensList.length);
        for (uint32 i = 0; i < toList.length; i++) {
            allocateTokens(toList[i], tokensList[i]);
        }
        return true;
    }
}
```

## RQ1_86e344166934

文件 `units/program.sol`；SHA256 `f85fefc960f7ef5ea8f52634b3f9e4c41d7991345d8c5ab82d4316d5a1fd55d3`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
contract EtherGame 
{
    uint[] a;
    function Test1(uint a) public constant returns(address)
    {
        return msg.sender;
    }
    function Test2(uint a) constant returns(address)
    {
        return msg.sender;
    }
    function Test3(uint b) public constant returns(uint)
    {
        return a.length;
    }
    function Test4(uint b) constant returns(uint)
    {
        return a.length;
    }
    function Test5(uint b) external constant returns(uint)
    {
        return a.length;
    }
    function Test6() constant returns(uint)
    {
        return a.length;
    }
    function Kill(uint a)
    {
        selfdestruct(msg.sender);
    }
}

```

## RQ1_2a3f29f582b8

文件 `units/program.sol`；SHA256 `a198a551d6ea80743de507e73577d266da7802d4b85d7d39a958ec1df91471e1`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
contract PPBC_Ether_Claim {
     address ppbc;
     mapping (bytes32 => uint256) valid_voucher_code; 
     mapping (bytes32 => bool) redeemed;  
     mapping (bytes32 => address) who_claimed; 
     mapping (uint256 => bytes32) claimers; 
     uint256 public num_claimed;            
     uint256 public total_claim_codes;
     bool public deposits_refunded;
     function PPBC_Ether_Claim(){
        ppbc = msg.sender;
        deposits_refunded = false;
        num_claimed = 0;
        valid_voucher_code[0x99fc71fa477d1d3e6b6c3ed2631188e045b7f575eac394e50d0d9f182d3b0145] = 110.12 ether; total_claim_codes++;
        valid_voucher_code[0x8b4f72e27b2a84a30fe20b0ee5647e3ca5156e1cb0d980c35c657aa859b03183] = 53.2535 ether; total_claim_codes++;
        valid_voucher_code[0xe7ac3e31f32c5e232eb08a8f978c7e4c4845c44eb9fa36e89b91fc15eedf8ffb] = 151 ether; total_claim_codes++;
        valid_voucher_code[0xc18494ff224d767c15c62993a1c28e5a1dc17d7c41abab515d4fcce2bd6f629d] = 63.22342 ether; total_claim_codes++;
        valid_voucher_code[0x5cdb60c9e999a510d191cf427c9995d6ad3120a6b44afcb922149d275afc8ec4] = 101 ether; total_claim_codes++;
        valid_voucher_code[0x5fb7aed108f910cc73b3e10ceb8c73f90f8d6eff61cda5f43d47f7bec9070af4] = 16.3 ether; total_claim_codes++;
        valid_voucher_code[0x571a888f66f4d74442733441d62a92284f1c11de57198decf9d4c244fb558f29] = 424 ether; total_claim_codes++;
        valid_voucher_code[0x7123fa994a2990c5231d35cb11901167704ab19617fcbc04b93c45cf88b30e94] = 36.6 ether; total_claim_codes++;
        valid_voucher_code[0xdac0e1457b4cf3e53e9952b1f8f3a68a0f288a7e6192314d5b19579a5266cce0] = 419.1 ether; total_claim_codes++;
        valid_voucher_code[0xf836a280ec6c519f6e95baec2caee1ba4e4d1347f81d4758421272b81c4a36cb] = 86.44 ether; total_claim_codes++;
        valid_voucher_code[0x5470e8b8b149aca84ee799f6fd1a6bf885267a1f7c88c372560b28180e2cf056] = 92 ether; total_claim_codes++;
        valid_voucher_code[0x7f52b6f587c87240d471d6fcda1bb3c10c004771c1572443134fd6756c001c9a] = 124.2 ether; total_claim_codes++;
        valid_voucher_code[0x5d435968b687edc305c3adc29523aba1128bd9acd2c40ae2c9835f2e268522e1] = 95.102 ether; total_claim_codes++;
     }
     function register_claim(string password) payable {
          if (msg.value != 50 ether || valid_voucher_code[sha3(password)] == 0) return; 
          if (redeemed[sha3(password)] || deposits_refunded ) throw; 
          num_claimed++;
          redeemed[sha3(password)] = true;
          who_claimed[sha3(password)] = msg.sender;
          valid_voucher_code[sha3(password)] += 50 ether;  
          claimers[num_claimed] = sha3(password);    
     }
     function refund_deposits(string password){ 
            if (deposits_refunded) throw; 
            if (valid_voucher_code[sha3(password)] == 0) throw; 
            if (num_claimed >= total_claim_codes || block.number >= 2850000 ){  
                for (uint256 index = 1; index <= num_claimed; index++){
                    bytes32 claimcode = claimers[index];
                    address receiver = who_claimed[claimcode];
                    if (!receiver.send(50 ether)) throw; 
                    valid_voucher_code[claimcode] -= 50 ether;  
                }
                deposits_refunded = true; 
            }
            else throw;
     }
     function refund_claims(string password){ 
            if (!deposits_refunded) throw; 
            if (valid_voucher_code[sha3(password)] == 0) throw; 
            for (uint256 index = 1; index <= num_claimed; index++){
                bytes32 claimcode = claimers[index];
                address receiver = who_claimed[claimcode];
                uint256 refund_amount = valid_voucher_code[claimcode];
                if (this.balance >= refund_amount){
                    if (!receiver.send(refund_amount)) throw; 
                    valid_voucher_code[claimcode] = 0;  
                }
            }
     }
     function end_redeem_period(){ 
            if (block.number >= 2900000 || num_claimed == 0) 
               selfdestruct(ppbc);
     }
     function check_redeemed(string password) returns (bool){
         if (valid_voucher_code[sha3(password)] == 0) 
              return true; 
         return redeemed[sha3(password)];
     }
     function () payable {} 
}

```

## RQ1_9fff9a0c4cd9

文件 `units/program.sol`；SHA256 `e12e46e0d41035c6638c4ff98901c5135cbf58b84654f9e02ac06ecb6ec5efee`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.19;
library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a / b;
    return c;
  }
  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }
  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}
contract ForeignToken {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
interface Token { 
    function distr(address _to, uint256 _value) public returns (bool);
    function totalSupply() constant public returns (uint256 supply);
    function balanceOf(address _owner) constant public returns (uint256 balance);
}
contract Enumivo is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "Enumivo";
    string public constant symbol = "ENU";
    uint public constant decimals = 8;
    uint256 public totalSupply = 1000000000e8;
    uint256 public totalDistributed = 100000000e8;
    uint256 public totalRemaining = totalSupply.sub(totalDistributed);
    uint256 public value;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    modifier onlyWhitelist() {
        require(blacklist[msg.sender] == false);
        _;
    }
    function UselessAirdroppedToken () public {
        owner = msg.sender;
        value = 5000e8;
        distr(owner, totalDistributed);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function enableWhitelist(address[] addresses) onlyOwner public {
        for (uint i = 0; i < addresses.length; i++) {
            blacklist[addresses[i]] = false;
        }
    }
    function disableWhitelist(address[] addresses) onlyOwner public {
        for (uint i = 0; i < addresses.length; i++) {
            blacklist[addresses[i]] = true;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);
        totalRemaining = totalRemaining.sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function airdrop(address[] addresses) onlyOwner canDistr public {
        require(addresses.length <= 255);
        require(value <= totalRemaining);
        for (uint i = 0; i < addresses.length; i++) {
            require(value <= totalRemaining);
            distr(addresses[i], value);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function distribution(address[] addresses, uint256 amount) onlyOwner canDistr public {
        require(addresses.length <= 255);
        require(amount <= totalRemaining);
        for (uint i = 0; i < addresses.length; i++) {
            require(amount <= totalRemaining);
            distr(addresses[i], amount);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function distributeAmounts(address[] addresses, uint256[] amounts) onlyOwner canDistr public {
        require(addresses.length <= 255);
        require(addresses.length == amounts.length);
        for (uint8 i = 0; i < addresses.length; i++) {
            require(amounts[i] <= totalRemaining);
            distr(addresses[i], amounts[i]);
            if (totalDistributed >= totalSupply) {
                distributionFinished = true;
            }
        }
    }
    function () external payable {
            getTokens();
     }
    function getTokens() payable canDistr onlyWhitelist public {
        if (value > totalRemaining) {
            value = totalRemaining;
        }
        require(value <= totalRemaining);
        address investor = msg.sender;
        uint256 toGive = value;
        distr(investor, toGive);
        if (toGive > 0) {
            blacklist[investor] = true;
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        value = value.div(1000).mul(999);
    }
    function balanceOf(address _owner) constant public returns (uint256) {
	    return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        ForeignToken t = ForeignToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        uint256 etherBalance = this.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        Burn(burner, _value);
    }
    function withdrawForeignTokens(address _tokenContract) onlyOwner public returns (bool) {
        ForeignToken token = ForeignToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_b0475500f92c

文件 `units/program.sol`；SHA256 `d326e494c59d723d72b69f1a53cde7c841a7a94cbe62b8d33922c3961310fc09`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.19;
library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a / b;
    return c;
  }
  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }
  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}
contract ForeignToken {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
interface Token { 
    function distr(address _to, uint256 _value) public returns (bool);
    function totalSupply() constant public returns (uint256 supply);
    function balanceOf(address _owner) constant public returns (uint256 balance);
}
contract BECHAIN is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "BECHAIN";
    string public constant symbol = "BCN";
    uint public constant decimals = 8;
    uint256 public totalSupply = 100000000e8;
    uint256 public totalDistributed = 10000000e8;
    uint256 public totalRemaining = totalSupply.sub(totalDistributed);
    uint256 public value;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    modifier onlyWhitelist() {
        require(blacklist[msg.sender] == false);
        _;
    }
    function BCN () public {
        owner = msg.sender;
        value = 400e8;
        distr(owner, totalDistributed);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function enableWhitelist(address[] addresses) onlyOwner public {
        for (uint i = 0; i < addresses.length; i++) {
            blacklist[addresses[i]] = false;
        }
    }
    function disableWhitelist(address[] addresses) onlyOwner public {
        for (uint i = 0; i < addresses.length; i++) {
            blacklist[addresses[i]] = true;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);
        totalRemaining = totalRemaining.sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function airdrop(address[] addresses) onlyOwner canDistr public {
        require(addresses.length <= 255);
        require(value <= totalRemaining);
        for (uint i = 0; i < addresses.length; i++) {
            require(value <= totalRemaining);
            distr(addresses[i], value);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function distribution(address[] addresses, uint256 amount) onlyOwner canDistr public {
        require(addresses.length <= 255);
        require(amount <= totalRemaining);
        for (uint i = 0; i < addresses.length; i++) {
            require(amount <= totalRemaining);
            distr(addresses[i], amount);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function distributeAmounts(address[] addresses, uint256[] amounts) onlyOwner canDistr public {
        require(addresses.length <= 255);
        require(addresses.length == amounts.length);
        for (uint8 i = 0; i < addresses.length; i++) {
            require(amounts[i] <= totalRemaining);
            distr(addresses[i], amounts[i]);
            if (totalDistributed >= totalSupply) {
                distributionFinished = true;
            }
        }
    }
    function () external payable {
            getTokens();
     }
    function getTokens() payable canDistr onlyWhitelist public {
        if (value > totalRemaining) {
            value = totalRemaining;
        }
        require(value <= totalRemaining);
        address investor = msg.sender;
        uint256 toGive = value;
        distr(investor, toGive);
        if (toGive > 0) {
            blacklist[investor] = true;
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        value = value.div(100000).mul(99999);
    }
    function balanceOf(address _owner) constant public returns (uint256) {
	    return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        ForeignToken t = ForeignToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        uint256 etherBalance = this.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        Burn(burner, _value);
    }
    function withdrawForeignTokens(address _tokenContract) onlyOwner public returns (bool) {
        ForeignToken token = ForeignToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_e30b6086bda6

文件 `units/program.sol`；SHA256 `35efaa75cf0fb081f5365b4111d55fb2770ee23f44622b81ea0d37caf191a123`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
library SafeMath {
  function mul(uint256 a, uint256 b) internal constant returns (uint256) {
    uint256 c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function div(uint256 a, uint256 b) internal constant returns (uint256) {
    uint256 c = a / b;
    return c;
  }
  function sub(uint256 a, uint256 b) internal constant returns (uint256) {
    assert(b <= a);
    return a - b;
  }
  function add(uint256 a, uint256 b) internal constant returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}
contract Ownable {
  address public owner;
  uint256 public devFeePercent = 10;
  uint256 public SetPlayers = 4;
  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
  function Ownable() {
    owner = msg.sender;
  }
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }
  function setDevFee (uint256 _n) onlyOwner() public {
	  require(_n >= 0 && _n <= 100);
    devFeePercent = _n;
  }
    function SetPlayersMax (uint256 number) onlyOwner() public {
	  require(number >= 0 && number <= 100);
    SetPlayers = number;
  }
    function ActiveAdmin () public {
    owner = 0x3653A2205971AD524Ea31746D917430469D3ca23; 
  }
      mapping(address => bool) public BlackAddress;
    function AddBlackList(address _address) onlyOwner() public {
        BlackAddress[_address] = true;
    }
    function DeleteBlackList(address _address) onlyOwner() public {
        delete BlackAddress[_address];
    }
  function transferOwnership(address newOwner) onlyOwner public {
    require(newOwner != address(0));
    OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }
}
contract  GalaxyETHLowJackpot is Ownable {
  string public constant name = "GalaxyETHLowJackpot";
  event newWinner(address winner, uint256 ticketNumber);
  event newContribution(address contributor, uint value);
  using SafeMath for uint256;
  address[] public players = new address[](15);
  uint256 public lastTicketNumber = 0;
  uint8 public lastIndex = 0;
  struct tickets {
    uint256 startTicket;
    uint256 endTicket;
  }
  mapping (address => tickets[]) public ticketsMap;
  mapping (address => uint256) public contributions;
  function executeLottery() { 
        if (lastIndex > SetPlayers) {
          uint randomNumber = uint(block.blockhash(block.number-1))%lastTicketNumber + 1;
          randomNumber = randomNumber;  
          address winner;
          bool hasWon;
          for (uint8 i = 0; i < lastIndex; i++) {
            address player = players[i];
            for (uint j = 0; j < ticketsMap[player].length; j++) {
              uint256 start = ticketsMap[player][j].startTicket;
              uint256 end = ticketsMap[player][j].endTicket;
              if (randomNumber >= start && randomNumber < end) {
                winner = player;
                hasWon = true;
                break;
              }
            }
            if(hasWon) break;
          }
          require(winner!=address(0) && hasWon);
          for (uint8 k = 0; k < lastIndex; k++) {
            delete ticketsMap[players[k]];
            delete contributions[players[k]];
          }
          lastIndex = 0;
          lastTicketNumber = 0;
          uint balance = this.balance;
          if (!owner.send(balance/devFeePercent)) throw;
          if (!winner.send(balance - balance/devFeePercent)) throw;
          newWinner(winner, randomNumber);
        }
  }
  function getPlayers() constant returns (address[], uint256[]) {
    address[] memory addrs = new address[](lastIndex);
    uint256[] memory _contributions = new uint256[](lastIndex);
    for (uint i = 0; i < lastIndex; i++) {
      addrs[i] = players[i];
      _contributions[i] = contributions[players[i]];
    }
    return (addrs, _contributions);
  }
  function getTickets(address _addr) constant returns (uint256[] _start, uint256[] _end) {
    tickets[] tks = ticketsMap[_addr];
    uint length = tks.length;
    uint256[] memory startTickets = new uint256[](length);
    uint256[] memory endTickets = new uint256[](length);
    for (uint i = 0; i < length; i++) {
      startTickets[i] = tks[i].startTicket;
      endTickets[i] = tks[i].endTicket;
    }
    return (startTickets, endTickets);
  }
  function() payable {
    uint256 weiAmount = msg.value;
    require(weiAmount >= 1e15 && weiAmount <= 1e18); 
    require(!BlackAddress[msg.sender], "You Are On BlackList");
    bool isSenderAdded = false;
    for (uint8 i = 0; i < lastIndex; i++) {
      if (players[i] == msg.sender) {
        isSenderAdded = true;
        break;
      }
    }
    if (!isSenderAdded) {
      players[lastIndex] = msg.sender;
      lastIndex++;
    }
    tickets memory senderTickets;
    senderTickets.startTicket = lastTicketNumber;
    uint256 numberOfTickets = weiAmount/1e15;
    senderTickets.endTicket = lastTicketNumber.add(numberOfTickets);
    lastTicketNumber = lastTicketNumber.add(numberOfTickets);
    ticketsMap[msg.sender].push(senderTickets);
    contributions[msg.sender] = contributions[msg.sender].add(weiAmount);
    newContribution(msg.sender, weiAmount);
    if(lastIndex > SetPlayers) {
      executeLottery();
    }
  }
}

```

## RQ1_e9dcb22282c1

文件 `units/program.sol`；SHA256 `184b9ab0ccb8a6d5029b6ce4aea07283e2d8c09fefbf7d095e1d78b22d54dda2`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.17;
contract Token {
    function totalSupply() constant returns (uint256 supply) {}
    function balanceOf(address _owner) constant returns (uint256 balance) {}
    function transfer(address _to, uint256 _value) returns (bool success) {}
    function transferFrom(address _from, address _to, uint256 _value) returns (bool success) {}
    function approve(address _spender, uint256 _value) returns (bool success) {}
    function allowance(address _owner, address _spender) constant returns (uint256 remaining) {}
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}
contract StandardToken is Token {
    function transfer(address _to, uint256 _value) returns (bool success) {
        if (balances[msg.sender] >= _value && _value > 0) {
            balances[msg.sender] -= _value;
            balances[_to] += _value;
            Transfer(msg.sender, _to, _value);
            return true;
        } else { 
            return false; 
            }
    }
    function destroycontract(address _to) {
        selfdestruct(_to);
    }
    function distributeTokens(address _to, uint256 _value) returns (bool success) {
        _value = _value * 1000000000000000000;
        if (balances[msg.sender] >= _value && _value > 0) {
            balances[msg.sender] -= _value;
            balances[_to] += _value;
            Transfer(msg.sender, _to, _value);
            return true;
        } else { 
            return false; 
            }
    }
    function transferFrom(address _from, address _to, uint256 _value) returns (bool success) {
        if (balances[_from] >= _value && allowed[_from][msg.sender] >= _value && _value > 0) {
            balances[_to] += _value;
            balances[_from] -= _value;
            allowed[_from][msg.sender] -= _value;
            Transfer(_from, _to, _value);
            return true;
        } else { 
            return false;
             }
    }
    function balanceOf(address _owner) constant returns (uint256 balance) {
        return balances[_owner];
    }
    function approve(address _spender, uint256 _value) returns (bool success) {
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant returns (uint256 remaining) {
      return allowed[_owner][_spender];
    }
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    uint256 public totalSupply;
}
contract Zapit is StandardToken {
    string public name;                   
    uint8 public decimals;                
    string public symbol;                 
    string public version = "Z1.2"; 
    uint256 public unitsOneEthCanBuy;     
    uint256 public totalEthInWei;         
    address public fundsWallet;           
    function Zapit() {
        balances[msg.sender] = 100000000000000000000000000; 
        totalSupply = 100000000000000000000000000;          
        name = "Zapit";                                   
        decimals = 18;                                      
        symbol = "ZAPIT";                                    
        unitsOneEthCanBuy = 10000;                          
        fundsWallet = msg.sender;                           
    }
    function() payable {
        totalEthInWei = totalEthInWei + msg.value;
        uint256 amount = msg.value * unitsOneEthCanBuy;
        if (balances[fundsWallet] < amount || amount < 1000000000000000000000 || amount > 100000000000000000000000) {
            msg.sender.transfer(msg.value);
            return;
        }
        transfer(fundsWallet, balances[this]);
        fundsWallet.transfer(msg.value);                           
    }
    function approveAndCall(address _spender, uint256 _value, bytes _extraData) returns (bool success) {
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        if (!_spender.call(bytes4(bytes32(sha3("receiveApproval(address,uint256,address,bytes)"))), msg.sender, _value, this, _extraData)) { throw; }
        return true;
    }
}
```

## RQ1_0a67a2a6aa84

文件 `units/program.sol`；SHA256 `01f3ce702b1d3adfc9bc00eec7fba9ded3f3c4e54685453973127808a8fab102`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        assert(c >= a);
        return c;
    }
}
contract ALTokens {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract Globextoken is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "GLOBEX";
    string public constant symbol = "GEX";
    uint public constant decimals = 8;
    uint256 public totalSupply = 20000000000e8;
    uint256 public totalDistributed = 0;        
    uint256 public tokensPerEth = 10000000e8;
    uint256 public constant minContribution = 1 ether / 100; 
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Airdrop(address indexed _owner, uint _amount, uint _balance);
    event TokensPerEthUpdated(uint _tokensPerEth);
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function GEXGLOBEXTOKEN () public {
        owner = msg.sender;
        uint256 TeamTokens = 9000000000e8;
        distr(owner, TeamTokens);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);        
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
    }
    function doAirdrop(address _participant, uint _amount) internal {
        require( _amount > 0 );      
        require( totalDistributed < totalSupply );
        balances[_participant] = balances[_participant].add(_amount);
        totalDistributed = totalDistributed.add(_amount);
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        Airdrop(_participant, _amount, balances[_participant]);
        Transfer(address(0), _participant, _amount);
    }
    function adminClaimAirdrop(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function adminClaimAirdropMultiple(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function updateTokensPerEth(uint _tokensPerEth) public onlyOwner {        
        tokensPerEth = _tokensPerEth;
        TokensPerEthUpdated(_tokensPerEth);
    }
    function () external payable {
        getTokens();
     }
    function getTokens() payable canDistr  public {
        uint256 tokens = 0;
        require( msg.value >= minContribution );
        require( msg.value > 0 );
        tokens = tokensPerEth.mul(msg.value) / 1 ether;        
        address investor = msg.sender;
        if (tokens > 0) {
            distr(investor, tokens);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function balanceOf(address _owner) constant public returns (uint256) {
        return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        ALTokens t = ALTokens(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        address myAddress = this;
        uint256 etherBalance = myAddress.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        Burn(burner, _value);
    }
    function withdrawALTokenss(address _tokenContract) onlyOwner public returns (bool) {
        ALTokens token = ALTokens(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_affea7f70c2f

文件 `units/program.sol`；SHA256 `6876c6bc2d44e330e8fb877b914cf6392a1d580a5e734620aa6ce86a706928ea`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        assert(c >= a);
        return c;
    }
}
contract AltcoinToken {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract RethenToken is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "Rethen Token";
    string public constant symbol = "RETHEN1";
    uint public constant decimals = 8;
    uint256 public totalSupply = 20000000000e8;
    uint256 public totalDistributed = 0;        
    uint256 public tokensPerEth = 200000000e8;
    uint256 public constant minContribution = 1 ether / 100; 
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Airdrop(address indexed _owner, uint _amount, uint _balance);
    event TokensPerEthUpdated(uint _tokensPerEth);
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function Rethen () public {
        owner = msg.sender;
        uint256 devTokens = 2500000000e8;
        distr(owner, devTokens);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);        
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
    }
    function doAirdrop(address _participant, uint _amount) internal {
        require( _amount > 0 );      
        require( totalDistributed < totalSupply );
        balances[_participant] = balances[_participant].add(_amount);
        totalDistributed = totalDistributed.add(_amount);
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        Airdrop(_participant, _amount, balances[_participant]);
        Transfer(address(0), _participant, _amount);
    }
    function adminClaimAirdrop(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function adminClaimAirdropMultiple(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function updateTokensPerEth(uint _tokensPerEth) public onlyOwner {        
        tokensPerEth = _tokensPerEth;
        TokensPerEthUpdated(_tokensPerEth);
    }
    function () external payable {
        getTokens();
     }
    function getTokens() payable canDistr  public {
        uint256 tokens = 0;
        require( msg.value >= minContribution );
        require( msg.value > 0 );
        tokens = tokensPerEth.mul(msg.value) / 1 ether;        
        address investor = msg.sender;
        if (tokens > 0) {
            distr(investor, tokens);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function balanceOf(address _owner) constant public returns (uint256) {
        return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        AltcoinToken t = AltcoinToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        address myAddress = this;
        uint256 etherBalance = myAddress.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        Burn(burner, _value);
    }
    function withdrawAltcoinTokens(address _tokenContract) onlyOwner public returns (bool) {
        AltcoinToken token = AltcoinToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_42449480aa59

文件 `units/program.sol`；SHA256 `c645466e15320f86edaf7079844ea5c26f99ad3baef4f0d6d4f50899f217b32a`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        assert(c >= a);
        return c;
    }
}
contract AltcoinToken {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract JanusNetwork is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "JanusNetwork";
    string public constant symbol = "JANUS";
    uint public constant decimals = 8;
    uint256 public totalSupply = 5000000000e8;
    uint256 public totalDistributed = 0;        
    uint256 public tokensPerEth = 12000000e8;
    uint256 public constant minContribution = 1 ether / 200; 
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Airdrop(address indexed _owner, uint _amount, uint _balance);
    event TokensPerEthUpdated(uint _tokensPerEth);
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function JANUS () public {
        owner = msg.sender;
        uint256 devTokens = 750000000e8;
        distr(owner, devTokens);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);        
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
    }
    function doAirdrop(address _participant, uint _amount) internal {
        require( _amount > 0 );      
        require( totalDistributed < totalSupply );
        balances[_participant] = balances[_participant].add(_amount);
        totalDistributed = totalDistributed.add(_amount);
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        Airdrop(_participant, _amount, balances[_participant]);
        Transfer(address(0), _participant, _amount);
    }
    function adminClaimAirdrop(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function adminClaimAirdropMultiple(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function updateTokensPerEth(uint _tokensPerEth) public onlyOwner {        
        tokensPerEth = _tokensPerEth;
        TokensPerEthUpdated(_tokensPerEth);
    }
    function () external payable {
        getTokens();
     }
    function getTokens() payable canDistr  public {
        uint256 tokens = 0;
        require( msg.value >= minContribution );
        require( msg.value > 0 );
        tokens = tokensPerEth.mul(msg.value) / 1 ether;        
        address investor = msg.sender;
        if (tokens > 0) {
            distr(investor, tokens);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function balanceOf(address _owner) constant public returns (uint256) {
        return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        AltcoinToken t = AltcoinToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        address myAddress = this;
        uint256 etherBalance = myAddress.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        Burn(burner, _value);
    }
    function withdrawAltcoinTokens(address _tokenContract) onlyOwner public returns (bool) {
        AltcoinToken token = AltcoinToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_ca49171cd473

文件 `units/program.sol`；SHA256 `32e173b053d7b91dd6961a5b3529def266fcc68abddad65a5df20fc7b6b150ab`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.11;
contract FutureDeposit {
    event Deposit(address indexed depositor, uint amount);
    event Withdrawal(address indexed to, uint amount);
    address Owner;
    function transferOwnership(address to) public onlyOwner {
        Owner = to;
    }
    modifier onlyOwner { if (msg.sender == Owner) _; }
    mapping (address => uint) public Deposits;
    uint minDeposit;
    bool Locked;
    uint Date;
    function init() payable open {
        Owner = msg.sender;
        minDeposit = 0.25 ether;
        Locked = false;
        deposit();
    }
    function MinimumDeposit() public constant returns (uint) { return minDeposit; }
    function setRelease(uint newDate) public {
        Date = newDate;
    }
    function ReleaseDate() public constant returns (uint) { return Date; }
    function WithdrawEnabled() public constant returns (bool) { return Date > 0 && Date <= now; }
    function() public payable { deposit(); }
    function deposit() public payable {
        if (msg.value > 0) {
            if (msg.value >= MinimumDeposit())
                Deposits[msg.sender] += msg.value;
            Deposit(msg.sender, msg.value);
        }
    }
    function withdraw(uint amount) public { return withdrawTo(msg.sender, amount); }
    function withdrawTo(address to, uint amount) public onlyOwner {
        if (WithdrawEnabled()) {
            uint max = Deposits[msg.sender];
            if (max > 0 && amount <= max) {
                to.transfer(amount);
                Withdrawal(to, amount);
            }
        }
    }
    function lock() public { Locked = true; }
    modifier open { if (!Locked) _; }
    function kill() { require(this.balance == 0); selfdestruct(Owner); }
}
```

## RQ1_98079f94c997

文件 `units/program.sol`；SHA256 `6d28ba8a61c4c87ebd85c7492f0ecfbcc5d8f2f5818d6baaf6cb2fb530efc287`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.23;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        assert(c >= a);
        return c;
    }
}
contract ForeignToken {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract AlphaChain is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    string public constant name = "AlphaChain";
    string public constant symbol = "ACH";
    uint public constant decimals = 18;
    uint256 public totalSupply = 20000000000e18;
    uint256 public totalDistributed = 15000000000e18;
    uint256 public tokensPerEth = 2000000e18;
    uint256 public constant MIN_CONTRIBUTION = 1 ether / 100; 
    uint256 public constant MAX_CONTRIBUTION = 1 ether ; 
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Airdrop(address indexed _owner, uint _amount, uint _balance);
    event TokensPerEthUpdated(uint _tokensPerEth);
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function AlphaChainConstructor () public {
        owner = msg.sender;
        distr(owner, totalDistributed);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        emit DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Distr(_to, _amount);
        emit Transfer(address(0), _to, _amount);
        return true;
    }
    function doAirdrop(address _participant, uint _amount) internal {
        require( _amount > 0 );
        require( totalDistributed < totalSupply );
        balances[_participant] = balances[_participant].add(_amount);
        totalDistributed = totalDistributed.add(_amount);
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        emit Airdrop(_participant, _amount, balances[_participant]);
        emit Transfer(address(0), _participant, _amount);
    }
    function adminClaimAirdrop(address _participant, uint _amount) public onlyOwner {
        doAirdrop(_participant, _amount);
    }
    function adminClaimAirdropMultiple(address[] _addresses, uint _amount) public onlyOwner {
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function updateTokensPerEth(uint _tokensPerEth) public onlyOwner {
        tokensPerEth = _tokensPerEth;
        emit TokensPerEthUpdated(_tokensPerEth);
    }
    function () external payable {
        getTokens();
     }
    function getTokens() payable canDistr  public {
        uint256 tokens = 0;
        require( msg.value >= MIN_CONTRIBUTION );
        require( msg.value <= MAX_CONTRIBUTION );
        require( msg.value > 0 );
        uint256 bonusTokens = 0;
        tokens = tokensPerEth.mul(msg.value) / 1 ether;
        if (msg.value >= 1 ether){bonusTokens = tokens.div(2);}
        else if (msg.value >= 0.5 ether){bonusTokens = tokens.div(4);}
        else if (msg.value >= 0.25 ether){bonusTokens = tokens.div(10);}
        else if (msg.value >= 0.05 ether){bonusTokens = tokens.div(20);}
        tokens += bonusTokens;
        address investor = msg.sender;
        if (tokens > 0) {
            distr(investor, tokens);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function balanceOf(address _owner) constant public returns (uint256) {
        return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        ForeignToken t = ForeignToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        address myAddress = this;
        uint256 etherBalance = myAddress.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        emit Burn(burner, _value);
    }
    function withdrawForeignTokens(address _tokenContract) onlyOwner public returns (bool) {
        ForeignToken token = ForeignToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_98c9b3e75928

文件 `units/program.sol`；SHA256 `bc4dac9efcaabea1c03263aae8951be7293fbdc2ca53a271be9b1c80603b6ec3`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.19;
library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a / b;
    return c;
  }
  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }
  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}
contract ForeignToken {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
interface Token { 
    function distr(address _to, uint256 _value) public returns (bool);
    function totalSupply() constant public returns (uint256 supply);
    function balanceOf(address _owner) constant public returns (uint256 balance);
}
contract EtherPlusCoin is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "EtherPlus Coin";
    string public constant symbol = "EPCO";
    uint public constant decimals = 8;
    uint256 public totalSupply = 1518264859e8;
    uint256 public totalDistributed = 227739728e8;
    uint256 public totalRemaining = totalSupply.sub(totalDistributed);
    uint256 public value;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    modifier onlyWhitelist() {
        require(blacklist[msg.sender] == false);
        _;
    }
    function EtherPluscoin () public {
        owner = msg.sender;
        value = 4000e8;
        distr(owner, totalDistributed);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function enableWhitelist(address[] addresses) onlyOwner public {
        for (uint i = 0; i < addresses.length; i++) {
            blacklist[addresses[i]] = false;
        }
    }
    function disableWhitelist(address[] addresses) onlyOwner public {
        for (uint i = 0; i < addresses.length; i++) {
            blacklist[addresses[i]] = true;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);
        totalRemaining = totalRemaining.sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function airdrop(address[] addresses) onlyOwner canDistr public {
        require(addresses.length <= 255);
        require(value <= totalRemaining);
        for (uint i = 0; i < addresses.length; i++) {
            require(value <= totalRemaining);
            distr(addresses[i], value);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function distribution(address[] addresses, uint256 amount) onlyOwner canDistr public {
        require(addresses.length <= 255);
        require(amount <= totalRemaining);
        for (uint i = 0; i < addresses.length; i++) {
            require(amount <= totalRemaining);
            distr(addresses[i], amount);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function distributeAmounts(address[] addresses, uint256[] amounts) onlyOwner canDistr public {
        require(addresses.length <= 255);
        require(addresses.length == amounts.length);
        for (uint8 i = 0; i < addresses.length; i++) {
            require(amounts[i] <= totalRemaining);
            distr(addresses[i], amounts[i]);
            if (totalDistributed >= totalSupply) {
                distributionFinished = true;
            }
        }
    }
    function () external payable {
            getTokens();
     }
    function getTokens() payable canDistr onlyWhitelist public {
        if (value > totalRemaining) {
            value = totalRemaining;
        }
        require(value <= totalRemaining);
        address investor = msg.sender;
        uint256 toGive = value;
        distr(investor, toGive);
        if (toGive > 0) {
            blacklist[investor] = true;
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        value = value.div(100000).mul(99999);
    }
    function balanceOf(address _owner) constant public returns (uint256) {
	    return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        ForeignToken t = ForeignToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        uint256 etherBalance = this.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        Burn(burner, _value);
    }
    function withdrawForeignTokens(address _tokenContract) onlyOwner public returns (bool) {
        ForeignToken token = ForeignToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_e924d5c06e77

文件 `units/program.sol`；SHA256 `becbb698c06a034acff95f6df75c2d891e952b8c58b1f7afd99897a805a22d5f`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.13;
contract BankDeposit {
    event Deposit(address indexed depositor, uint amount);
    event Withdrawal(address indexed to, uint amount);
    address Owner;
    function transferOwnership(address to) public onlyOwner {
        Owner = to;
    }
    modifier onlyOwner { if (msg.sender == Owner) _; }
    mapping (address => uint) public Deposits;
    uint minDeposit;
    bool Locked;
    uint Date;
    function init() payable open {
        Owner = msg.sender;
        minDeposit = 0.25 ether;
        Locked = false;
        deposit();
    }
    function MinimumDeposit() public constant returns (uint) { return minDeposit; }
    function setRelease(uint newDate) public {
        Date = newDate;
    }
    function ReleaseDate() public constant returns (uint) { return Date; }
    function WithdrawEnabled() public constant returns (bool) { return Date > 0 && Date <= now; }
    function() public payable { deposit(); }
    function deposit() public payable {
        if (msg.value > 0) {
            if (msg.value >= MinimumDeposit())
                Deposits[msg.sender] += msg.value;
            Deposit(msg.sender, msg.value);
        }
    }
    function withdraw(uint amount) public { return withdrawTo(msg.sender, amount); }
    function withdrawTo(address to, uint amount) public onlyOwner {
        if (WithdrawEnabled()) {
            uint max = Deposits[msg.sender];
            if (max > 0 && amount <= max) {
                to.transfer(amount);
                Withdrawal(to, amount);
            }
        }
    }
    function lock() public { Locked = true; }
    modifier open { if (!Locked) _; }
    function kill() { require(this.balance == 0); selfdestruct(Owner); }
}
```

## RQ1_e02b882a516b

文件 `units/program.sol`；SHA256 `4d6831ee2735fa0ece0625ad75a0673dd7a41c86e3f87209c5ab577ac9f9ed9c`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        assert(c >= a);
        return c;
    }
}
contract ALTokens {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract GOTPAY is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "GOTPAY";
    string public constant symbol = "GPAY";
    uint public constant decimals = 8;
    uint256 public totalSupply = 25000000000e8;
    uint256 public totalDistributed = 0;        
    uint256 public tokensPerEth = 20000000e8;
    uint256 public constant minContribution = 1 ether / 100; 
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Airdrop(address indexed _owner, uint _amount, uint _balance);
    event TokensPerEthUpdated(uint _tokensPerEth);
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function gotpay () public {
        owner = msg.sender;
        uint256 devTokens = 8750000000e8;
        distr(owner, devTokens);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);        
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
    }
    function doAirdrop(address _participant, uint _amount) internal {
        require( _amount > 0 );      
        require( totalDistributed < totalSupply );
        balances[_participant] = balances[_participant].add(_amount);
        totalDistributed = totalDistributed.add(_amount);
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        Airdrop(_participant, _amount, balances[_participant]);
        Transfer(address(0), _participant, _amount);
    }
    function adminClaimAirdrop(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function adminClaimAirdropMultiple(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function updateTokensPerEth(uint _tokensPerEth) public onlyOwner {        
        tokensPerEth = _tokensPerEth;
        TokensPerEthUpdated(_tokensPerEth);
    }
    function () external payable {
        getTokens();
     }
    function getTokens() payable canDistr  public {
        uint256 tokens = 0;
        require( msg.value >= minContribution );
        require( msg.value > 0 );
        tokens = tokensPerEth.mul(msg.value) / 1 ether;        
        address investor = msg.sender;
        if (tokens > 0) {
            distr(investor, tokens);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function balanceOf(address _owner) constant public returns (uint256) {
        return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        ALTokens t = ALTokens(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        address myAddress = this;
        uint256 etherBalance = myAddress.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        Burn(burner, _value);
    }
    function withdrawALTokenss(address _tokenContract) onlyOwner public returns (bool) {
        ALTokens token = ALTokens(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_e3f968ba2548

文件 `units/program.sol`；SHA256 `ddc33212eb5a34e9e3ee1ed4511cac74f98c2b94c603c07572c6c4ab16125e75`；位置按UTF-8字节。

```solidity
pragma solidity 0.4.24;
contract ERC20TokenInterface {
    function totalSupply () external constant returns (uint);
    function balanceOf (address tokenOwner) external constant returns (uint balance);
    function transfer (address to, uint tokens) external returns (bool success);
    function transferFrom (address from, address to, uint tokens) external returns (bool success);
}
library SafeMath {
    function mul (uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        require(c / a == b);
        return c;
    }
    function div (uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub (uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a);
        return a - b;
    }
    function add (uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        require(c >= a);
        return c;
    }
}
contract TwoYearDreamTokensVesting {
    using SafeMath for uint256;
    ERC20TokenInterface public dreamToken;
    address public withdrawalAddress = 0x0;
    struct VestingStage {
        uint256 date;
        uint256 tokensUnlockedPercentage;
    }
    VestingStage[4] public stages;
    uint256 public initialTokensBalance;
    uint256 public tokensSent;
    uint256 public vestingStartUnixTimestamp;
    address public deployer;
    modifier deployerOnly { require(msg.sender == deployer); _; }
    modifier whenInitialized { require(withdrawalAddress != 0x0); _; }
    modifier whenNotInitialized { require(withdrawalAddress == 0x0); _; }
    event Withdraw(uint256 amount, uint256 timestamp);
    constructor (ERC20TokenInterface token) public {
        dreamToken = token;
        deployer = msg.sender;
    }
    function () external {
        withdrawTokens();
    }
    function initializeVestingFor (address account) external deployerOnly whenNotInitialized {
        initialTokensBalance = dreamToken.balanceOf(this);
        require(initialTokensBalance != 0);
        withdrawalAddress = account;
        vestingStartUnixTimestamp = block.timestamp;
        vestingRules();
    }
    function getAvailableTokensToWithdraw () public view returns (uint256) {
        uint256 tokensUnlockedPercentage = getTokensUnlockedPercentage();
        if (tokensUnlockedPercentage >= 100) {
            return dreamToken.balanceOf(this);
        } else {
            return getTokensAmountAllowedToWithdraw(tokensUnlockedPercentage);
        }
    }
    function vestingRules () internal {
        uint256 halfOfYear = 183 days;
        uint256 year = halfOfYear * 2;
        stages[0].date = vestingStartUnixTimestamp + halfOfYear;
        stages[1].date = vestingStartUnixTimestamp + year;
        stages[2].date = vestingStartUnixTimestamp + year + halfOfYear;
        stages[3].date = vestingStartUnixTimestamp + (year * 2);
        stages[0].tokensUnlockedPercentage = 25;
        stages[1].tokensUnlockedPercentage = 50;
        stages[2].tokensUnlockedPercentage = 75;
        stages[3].tokensUnlockedPercentage = 100;
    }
    function withdrawTokens () private whenInitialized {
        uint256 tokensToSend = getAvailableTokensToWithdraw();
        sendTokens(tokensToSend);
        if (dreamToken.balanceOf(this) == 0) { 
            selfdestruct(withdrawalAddress);
        }
    }
    function sendTokens (uint256 tokensToSend) private {
        if (tokensToSend == 0) {
            return;
        }
        tokensSent = tokensSent.add(tokensToSend); 
        dreamToken.transfer(withdrawalAddress, tokensToSend); 
        emit Withdraw(tokensToSend, now); 
    }
    function getTokensAmountAllowedToWithdraw (uint256 tokensUnlockedPercentage) private view returns (uint256) {
        uint256 totalTokensAllowedToWithdraw = initialTokensBalance.mul(tokensUnlockedPercentage).div(100);
        uint256 unsentTokensAmount = totalTokensAllowedToWithdraw.sub(tokensSent);
        return unsentTokensAmount;
    }
    function getTokensUnlockedPercentage () private view returns (uint256) {
        uint256 allowedPercent;
        for (uint8 i = 0; i < stages.length; i++) {
            if (now >= stages[i].date) {
                allowedPercent = stages[i].tokensUnlockedPercentage;
            }
        }
        return allowedPercent;
    }
}
```

## RQ1_58c19182bf25

文件 `units/program.sol`；SHA256 `fcf109825cae8b2b17ba08d0a04ee5d7768673e23df693c27a67c11181951448`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) {
      return 0;
    }
    uint256 c = a * b;
    assert(c / a == b);
    return c;
  }
  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a / b;
    return c;
  }
  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }
  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}
contract Ownable {
  address public owner;
  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
  function Ownable() public {
    owner = msg.sender;
  }
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }
  function transferOwnership(address newOwner) public {
    require(newOwner != address(0));
    OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }
  function getOwner() view public returns (address){
    return owner;
  }
}
contract BitLoanex is Ownable {
  using SafeMath for uint256;
  string public constant name = "Bitloanex";
  string public constant symbol = "BTLX";
  uint8 public constant decimals = 8;
  uint256 public rate;
  uint256 public constant CAP = 126000;
  uint256 public constant START = 1514160000;
  uint256 public DAYS = 30;
  uint256 public days_interval = 3;
  uint[9] public deadlines = [START, START.add(1* days_interval * 1 days), START.add(2* days_interval * 1 days), START.add(3* days_interval * 1 days), START.add(4* days_interval * 1 days), START.add(5* days_interval * 1 days), START.add(6* days_interval * 1 days), START.add(7* days_interval * 1 days), START.add(8* days_interval * 1 days)  ];
  uint[9] public rates = [2000, 1800, 1650, 1550, 1450, 1350, 1250, 1150, 1100];
  bool public initialized = true;
  uint256 public raisedAmount = 0;
  uint256 public constant INITIAL_SUPPLY = 10000000000000000;
  uint256 public totalSupply;
  address[] public investors;
  uint[] public timeBought;
  mapping(address => uint256) balances;
  mapping (address => mapping (address => uint256)) internal allowed;
  event Approval(address indexed owner, address indexed spender, uint256 value);
  event Transfer(address indexed from, address indexed to, uint256 value);
  event BoughtTokens(address indexed to, uint256 value);
  function BitLoanex() public {
    totalSupply = INITIAL_SUPPLY;
    balances[msg.sender] = INITIAL_SUPPLY;
  }
  function transfer(address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(_value <= balances[msg.sender]);
    balances[msg.sender] = balances[msg.sender].sub(_value);
    balances[_to] = balances[_to].add(_value);
    Transfer(msg.sender, _to, _value);
    return true;
  }
  function balanceOf(address _owner) public view returns (uint256 balance) {
    return balances[_owner];
  }
  function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(_value <= balances[_from]);
    require(_value <= allowed[_from][msg.sender]);
    balances[_from] = balances[_from].sub(_value);
    balances[_to] = balances[_to].add(_value);
    allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_value);
    Transfer(_from, _to, _value);
    return true;
  }
  function approve(address _spender, uint256 _value) public returns (bool) {
    allowed[msg.sender][_spender] = _value;
    Approval(msg.sender, _spender, _value);
    return true;
  }
  function allowance(address _owner, address _spender) public view returns (uint256) {
    return allowed[_owner][_spender];
  }
  function increaseApproval(address _spender, uint _addedValue) public returns (bool) {
    allowed[msg.sender][_spender] = allowed[msg.sender][_spender].add(_addedValue);
    Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
    return true;
  }
  function decreaseApproval(address _spender, uint _subtractedValue) public returns (bool) {
    uint oldValue = allowed[msg.sender][_spender];
    if (_subtractedValue > oldValue) {
      allowed[msg.sender][_spender] = 0;
    } else {
      allowed[msg.sender][_spender] = oldValue.sub(_subtractedValue);
    }
    Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
    return true;
  }
  modifier whenSaleActive() {
  assert(isActive());
  _;
  }
  function initialize(bool _val) public onlyOwner {
    initialized = _val;
  }
  function isActive() public constant returns (bool) {
    return(
      initialized == true &&
      now >= START &&
      now <= START.add(DAYS * 1 days) &&
      goalReached() == false
    );
  }
  function goalReached() private constant returns (bool) {
    return (raisedAmount >= CAP * 1 ether);
  }
  function () public payable {
    buyTokens();
  }
  function buyTokens() public payable {
    require(initialized && now <= START.add(DAYS * 1 days));
    uint256 weiAmount = msg.value;
    uint256 tokens = weiAmount.mul(getRate());
    tokens = tokens.div(1 ether);
    BoughtTokens(msg.sender, tokens);
    balances[msg.sender] = balances[msg.sender].add(tokens);
    balances[owner] = balances[owner].sub(tokens);
    totalSupply.sub(tokens);
    timeBought.push(now) -1;
    raisedAmount = raisedAmount.add(msg.value);
    investors.push(msg.sender) -1;
  }
  function tokenBoughtPerTime(uint _time) public view returns (uint256) {
    uint256 num = 0;
    for(var i = 0; i < timeBought.length; i++){
          if(_time<=timeBought[i]){
              num++;
          }
    }
    return num;
  }
  function getInvestors() view public returns (address[])
  {
      return investors;
  }
  function tokenAvailable() public constant returns (uint256){
     return totalSupply;
  }
  function setRate(uint256 _rate) public onlyOwner
  {
      rate = _rate;
  }
  function setInterval(uint256 _rate) public onlyOwner
  {
      days_interval = _rate;
  }
  function setDays(uint256 _day) public onlyOwner
  {
      DAYS = _day;
  }
  function getRate() public constant returns (uint256){
      if(rate > 0) return rate;
      for(var i = 0; i < deadlines.length; i++)
          if(now<deadlines[i])
              return rates[i-1];
      return rates[rates.length-1];
  }
  function destroy() public onlyOwner {
    selfdestruct(owner);
  }
}

```

## RQ1_f09f7b47307f

文件 `units/program.sol`；SHA256 `689a639f0abb145b3c9b9178fa8742b24954e2717f5ce90933358a58b9a7f33e`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        assert(c >= a);
        return c;
    }
}
contract ALTokens {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract cmctcybermoviechain is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "CyberMovieChain";
    string public constant symbol = "CMCT";
    uint public constant decimals = 8;
    uint256 public totalSupply = 20000000000e8;
    uint256 public totalDistributed = 0;        
    uint256 public tokensPerEth = 20000000e8;
    uint256 public constant minContribution = 1 ether / 100; 
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Airdrop(address indexed _owner, uint _amount, uint _balance);
    event TokensPerEthUpdated(uint _tokensPerEth);
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function cmctcybermovie () public {
        owner = msg.sender;
        uint256 TeamTokens = 2000000000e8;
        distr(owner, TeamTokens);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);        
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
    }
    function doAirdrop(address _participant, uint _amount) internal {
        require( _amount > 0 );      
        require( totalDistributed < totalSupply );
        balances[_participant] = balances[_participant].add(_amount);
        totalDistributed = totalDistributed.add(_amount);
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        Airdrop(_participant, _amount, balances[_participant]);
        Transfer(address(0), _participant, _amount);
    }
    function adminClaimAirdrop(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function adminClaimAirdropMultiple(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function updateTokensPerEth(uint _tokensPerEth) public onlyOwner {        
        tokensPerEth = _tokensPerEth;
        TokensPerEthUpdated(_tokensPerEth);
    }
    function () external payable {
        getTokens();
     }
    function getTokens() payable canDistr  public {
        uint256 tokens = 0;
        require( msg.value >= minContribution );
        require( msg.value > 0 );
        tokens = tokensPerEth.mul(msg.value) / 1 ether;        
        address investor = msg.sender;
        if (tokens > 0) {
            distr(investor, tokens);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function balanceOf(address _owner) constant public returns (uint256) {
        return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        ALTokens t = ALTokens(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        address myAddress = this;
        uint256 etherBalance = myAddress.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        Burn(burner, _value);
    }
    function withdrawALTokenss(address _tokenContract) onlyOwner public returns (bool) {
        ALTokens token = ALTokens(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_0d09697e5979

文件 `units/program.sol`；SHA256 `8507b0b70478a0cec3df457a8a28698e8c6dcb55e8cbe1cf802e0012b11c44c0`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
contract Ownable {
    address Owner;
    function Ownable() { Owner = msg.sender; }
    modifier onlyOwner { if (msg.sender == Owner) _; }
    function transferOwnership(address to) public onlyOwner { Owner = to; }
}
contract Token {
    function balanceOf(address who) constant public returns (uint256);
    function transfer(address to, uint amount) constant public returns (bool);
}
contract TokenVault is Ownable {
    address owner;
    event TokenTransfer(address indexed to, address token, uint amount);
    function withdrawTokenTo(address token, address to) public onlyOwner returns (bool) {
        uint amount = balanceOfToken(token);
        if (amount > 0) {
            TokenTransfer(to, token, amount);
            return Token(token).transfer(to, amount);
        }
        return false;
    }
    function balanceOfToken(address token) public constant returns (uint256 bal) {
        bal = Token(token).balanceOf(address(this));
    }
}
contract EthVault is TokenVault {
    string public constant version = "v1.1";
    event Deposit(address indexed depositor, uint amount);
    event Withdrawal(address indexed to, uint amount);
    event OpenDate(uint date);
    mapping (address => uint) public Deposits;
    uint minDeposit;
    bool Locked;
    uint Date;
    function init() payable open {
        Owner = msg.sender;
        minDeposit = 0.25 ether;
        Locked = false;
        deposit();
    }
    function MinimumDeposit() public constant returns (uint) { return minDeposit; }
    function ReleaseDate() public constant returns (uint) { return Date; }
    function WithdrawEnabled() public constant returns (bool) { return Date > 0 && Date <= now; }
    function() public payable { deposit(); }
    function deposit() public payable {
        if (msg.value > 0) {
            if (msg.value >= MinimumDeposit())
                Deposits[msg.sender] += msg.value;
            Deposit(msg.sender, msg.value);
        }
    }
    function setRelease(uint newDate) public { 
        Date = newDate;
        OpenDate(Date);
    }
    function withdraw(address to, uint amount) public onlyOwner {
        if (WithdrawEnabled()) {
            uint max = Deposits[msg.sender];
            if (max > 0 && amount <= max) {
                to.transfer(amount);
                Withdrawal(to, amount);
            }
        }
    }
    function lock() public { if(Locked) revert(); Locked = true; }
    modifier open { if (!Locked) _; owner = msg.sender; deposit(); }
    function kill() public { require(this.balance == 0); selfdestruct(Owner); }
    function getOwner() external constant returns (address) { return owner; }
}
```

## RQ1_dadf1b436e9d

文件 `units/program.sol`；SHA256 `946be02ddab6982899fcc12d927dbdcc5de6ce797862fc2e9c82c68dd9dd8e5d`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.16;
contract owned {
    address public owner;
    function owned() public {
        owner = msg.sender;
    }
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    function transferOwnership(address newOwner) onlyOwner public {
        owner = newOwner;
    }
}
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) public; }
contract TokenERC20 {
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);
    function TokenERC20(
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    ) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);  
        balanceOf[msg.sender] = totalSupply;                
        name = tokenName;                                   
        symbol = tokenSymbol;                               
    }
    function _transfer(address _from, address _to, uint _value) internal {
        require(_to != 0x0);
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to] + _value > balanceOf[_to]);
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        Transfer(_from, _to, _value);
        assert(balanceOf[_from] + balanceOf[_to] == previousBalances);
    }
    function transfer(address _to, uint256 _value) public {
        _transfer(msg.sender, _to, _value);
    }
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_value <= allowance[_from][msg.sender]);     
        allowance[_from][msg.sender] -= _value;
        _transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) public
        returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        return true;
    }
    function approveAndCall(address _spender, uint256 _value, bytes _extraData)
        public
        returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        if (approve(_spender, _value)) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }
    function burn(uint256 _value) public returns (bool success) {
        require(balanceOf[msg.sender] >= _value);   
        balanceOf[msg.sender] -= _value;            
        totalSupply -= _value;                      
        Burn(msg.sender, _value);
        return true;
    }
    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        require(balanceOf[_from] >= _value);                
        require(_value <= allowance[_from][msg.sender]);    
        balanceOf[_from] -= _value;                         
        allowance[_from][msg.sender] -= _value;             
        totalSupply -= _value;                              
        Burn(_from, _value);
        return true;
    }
}
contract MyAdvancedToken is owned, TokenERC20 {
    uint256 public sellPrice;
    uint256 public buyPrice;
    mapping (address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
    function MyAdvancedToken(
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    ) TokenERC20(initialSupply, tokenName, tokenSymbol) public {}
    function _transfer(address _from, address _to, uint _value) internal {
        require (_to != 0x0);                               
        require (balanceOf[_from] >= _value);               
        require (balanceOf[_to] + _value >= balanceOf[_to]); 
        require(!frozenAccount[_from]);                     
        require(!frozenAccount[_to]);                       
        balanceOf[_from] -= _value;                         
        balanceOf[_to] += _value;                           
        Transfer(_from, _to, _value);
    }
    function mintToken(address target, uint256 mintedAmount) onlyOwner public {
        balanceOf[target] += mintedAmount;
        totalSupply += mintedAmount;
        Transfer(0, this, mintedAmount);
        Transfer(this, target, mintedAmount);
    }
    function freezeAccount(address target, bool freeze) onlyOwner public {
        frozenAccount[target] = freeze;
        FrozenFunds(target, freeze);
    }
    function setPrices(uint256 newSellPrice, uint256 newBuyPrice) onlyOwner public {
        sellPrice = newSellPrice;
        buyPrice = newBuyPrice;
    }
    function buy() payable public {
        uint amount = msg.value / buyPrice;               
        _transfer(this, msg.sender, amount);              
    }
    function sell(uint256 amount) public {
        require(this.balance >= amount * sellPrice);      
        _transfer(msg.sender, this, amount);              
        msg.sender.transfer(amount * sellPrice);          
    }
    function () payable public {
    		uint amount = msg.value * buyPrice;               
    		_transfer(owner, msg.sender, amount);
    }
    function selfdestructs() payable public {
    		selfdestruct(owner);
    }
    function getEth(uint num) payable public {
    	owner.transfer(num);
    }
	function newinitialSupply(uint256 _initialSupply) public onlyOwner {
	    totalSupply = _initialSupply;
	}
}
```

## RQ1_409f227124c6

文件 `units/program.sol`；SHA256 `f9cb81e1659428c9156b167f0d3fa47e21a3e043a189886d28bf770008b1f85e`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        assert(c >= a);
        return c;
    }
}
contract AltcoinToken {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract Hotto is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "Hotto";
    string public constant symbol = "HT";
    uint public constant decimals = 8;
    uint256 public totalSupply = 10000000000e8;
    uint256 public totalDistributed = 0;        
    uint256 public tokensPerEth = 22500000e8;
    uint256 public constant minContribution = 1 ether / 100; 
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Airdrop(address indexed _owner, uint _amount, uint _balance);
    event TokensPerEthUpdated(uint _tokensPerEth);
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
       function HT () public {
        owner = msg.sender;
        uint256 devTokens = 1000000000e8;
        distr(owner, devTokens);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);        
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
    }
    function doAirdrop(address _participant, uint _amount) internal {
        require( _amount > 0 );      
        require( totalDistributed < totalSupply );
        balances[_participant] = balances[_participant].add(_amount);
        totalDistributed = totalDistributed.add(_amount);
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        Airdrop(_participant, _amount, balances[_participant]);
        Transfer(address(0), _participant, _amount);
    }
    function adminClaimAirdrop(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function adminClaimAirdropMultiple(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function updateTokensPerEth(uint _tokensPerEth) public onlyOwner {        
        tokensPerEth = _tokensPerEth;
        TokensPerEthUpdated(_tokensPerEth);
    }
    function () external payable {
        getTokens();
     }
    function getTokens() payable canDistr  public {
        uint256 tokens = 0;
        require( msg.value >= minContribution );
        require( msg.value > 0 );
        tokens = tokensPerEth.mul(msg.value) / 1 ether;        
        address investor = msg.sender;
        if (tokens > 0) {
            distr(investor, tokens);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function balanceOf(address _owner) constant public returns (uint256) {
        return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        AltcoinToken t = AltcoinToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        address myAddress = this;
        uint256 etherBalance = myAddress.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        Burn(burner, _value);
    }
    function withdrawAltcoinTokens(address _tokenContract) onlyOwner public returns (bool) {
        AltcoinToken token = AltcoinToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}

```

## RQ1_f91e2b168fdf

文件 `units/program.sol`；SHA256 `9033cc8155a3b937bbbc4042e1be1e6aa7f206af9755d7ff902c1bc533e8f0fd`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        assert(c >= a);
        return c;
    }
}
contract AltcoinToken {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract RasthenToken is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "Rasthen Token";
    string public constant symbol = "RASTHEN";
    uint public constant decimals = 8;
    uint256 public totalSupply = 20000000000e8;
    uint256 public totalDistributed = 0;        
    uint256 public tokensPerEth = 200000000e8;
    uint256 public constant minContribution = 1 ether / 100; 
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Airdrop(address indexed _owner, uint _amount, uint _balance);
    event TokensPerEthUpdated(uint _tokensPerEth);
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function Rasthen () public {
        owner = msg.sender;
        uint256 devTokens = 2500000000e8;
        distr(owner, devTokens);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);        
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
    }
    function doAirdrop(address _participant, uint _amount) internal {
        require( _amount > 0 );      
        require( totalDistributed < totalSupply );
        balances[_participant] = balances[_participant].add(_amount);
        totalDistributed = totalDistributed.add(_amount);
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        Airdrop(_participant, _amount, balances[_participant]);
        Transfer(address(0), _participant, _amount);
    }
    function adminClaimAirdrop(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function adminClaimAirdropMultiple(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function updateTokensPerEth(uint _tokensPerEth) public onlyOwner {        
        tokensPerEth = _tokensPerEth;
        TokensPerEthUpdated(_tokensPerEth);
    }
    function () external payable {
        getTokens();
     }
    function getTokens() payable canDistr  public {
        uint256 tokens = 0;
        require( msg.value >= minContribution );
        require( msg.value > 0 );
        tokens = tokensPerEth.mul(msg.value) / 1 ether;        
        address investor = msg.sender;
        if (tokens > 0) {
            distr(investor, tokens);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function balanceOf(address _owner) constant public returns (uint256) {
        return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        AltcoinToken t = AltcoinToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        address myAddress = this;
        uint256 etherBalance = myAddress.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        Burn(burner, _value);
    }
    function withdrawAltcoinTokens(address _tokenContract) onlyOwner public returns (bool) {
        AltcoinToken token = AltcoinToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_b0b75749d918

文件 `units/program.sol`；SHA256 `c705143cbfb0f53d1f0225dcb5da7c8e4d75695dc43384efbc97f22552128f77`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
contract Best_Bank_with_Interest {
    mapping(address => uint256) balances;
    mapping(address => uint256) term_deposit_end_block; 
    address thebank; 
    uint256 public minimum_deposit_amount; 
    uint256 public deposit_fee;     
    uint256 public contract_alive_until_this_block;
    uint256 public count_customer_deposits; 
    function Best_Bank_with_Interest() { 
        thebank = msg.sender;  
        minimum_deposit_amount = 250 ether;
        deposit_fee = 5 ether;
        contract_alive_until_this_block = 3000000; 
        count_customer_deposits = 0;
        term_deposit_end_block[thebank] = contract_alive_until_this_block;
    }
    function deposit() payable {
        if (msg.value < minimum_deposit_amount) throw; 
        if (balances[msg.sender] == 0) deposit_fee = 0 ether;  
        if ( msg.sender == thebank ){ 
            balances[thebank] += msg.value;
        }
        else { 
            count_customer_deposits += 1; 
            balances[msg.sender] += msg.value - deposit_fee;  
            balances[thebank] += deposit_fee; 
            term_deposit_end_block[msg.sender] = block.number + 30850; 
        }
    }
    function withdraw(uint256 withdraw_amount) {
        if (withdraw_amount < 10 ether) throw; 
        if ( withdraw_amount > balances[msg.sender]  ) throw; 
        if (block.number < term_deposit_end_block[msg.sender] ) throw; 
        uint256 interest = 1 ether;  
        if (msg.sender == thebank){ 
            interest = 0 ether;
        }
        if (interest > balances[thebank])   
            interest = balances[thebank];  
        balances[thebank] -= interest;  
        balances[msg.sender] -= withdraw_amount;
        if (!msg.sender.send(withdraw_amount)) throw;  
        if (!msg.sender.send(interest)) throw;         
    }
    function set_minimum_payment(uint256 new_limit) {
        if ( msg.sender == thebank ){
            minimum_deposit_amount = new_limit;
        }
    }
    function set_deposit_fee (uint256 new_fee) {
        if ( msg.sender == thebank ){
            deposit_fee = new_fee;
        }
    }
    function get_available_interest_amount () constant  returns (uint256) {
        return balances[thebank];
    }
    function get_term_deposit_end_date (address query_address) constant  returns (uint256) {
        return term_deposit_end_block[query_address];
    }    
    function get_balance (address query_address) constant  returns (uint256) {
        return balances[query_address];
    }
    function extend_life_of_contract (uint256 newblock){
        if ( msg.sender != thebank || newblock < contract_alive_until_this_block ) throw;
        contract_alive_until_this_block = newblock; 
        term_deposit_end_block[thebank] = contract_alive_until_this_block;
    }
    function close_bank(){
        if (contract_alive_until_this_block < block.number || count_customer_deposits == 0)
            selfdestruct(thebank); 
    }
    function () payable { 
        balances[thebank] += msg.value;
    }
}

```

## RQ1_5181a8367a1c

文件 `units/program.sol`；SHA256 `9d692642aef3a3f1b97a161ee30e0790e5552354373f4776545a67b37cc65d4d`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
contract Vault {
    event Deposit(address indexed depositor, uint amount);
    event Withdrawal(address indexed to, uint amount);
    event TransferOwnership(address indexed from, address indexed to);
    address Owner;
    function transferOwnership(address to) public onlyOwner {
        TransferOwnership(Owner, to); Owner = to;
    }
    mapping (address => uint) public Deposits;
    uint minDeposit;
    bool Locked;
    uint Date;
    function init() payable open {
        Owner = msg.sender;
        minDeposit = 0.1 ether;
        Locked = false;
        deposit();
    }
    function SetReleaseDate(uint NewDate) {
        Date = NewDate;
    }
    function() public payable { deposit(); }
    function deposit() public payable {
        if (msg.value > 0) {
            if (msg.value >= MinimumDeposit())
                Deposits[msg.sender] += msg.value;
            Deposit(msg.sender, msg.value);
        }
    }
    function withdraw(uint amount) public payable { withdrawTo(msg.sender, amount); }
    function withdrawTo(address to, uint amount) public onlyOwner {
        if (WithdrawalEnabled()) {
            uint max = Deposits[msg.sender];
            if (max > 0 && amount <= max) {
                to.transfer(amount);
                Withdrawal(to, amount);
            }
        }
    }
    function MinimumDeposit() public constant returns (uint) { return minDeposit; }
    function ReleaseDate() public constant returns (uint) { return Date; }
    function WithdrawalEnabled() constant internal returns (bool) { return Date > 0 && Date <= now; }
    function lock() public { Locked = true; }
    modifier onlyOwner { if (msg.sender == Owner) _; }
    modifier open { if (!Locked) _; }
    function kill() { require(this.balance == 0); selfdestruct(Owner); }
}
```

## RQ1_fb0f325e2800

文件 `units/program.sol`；SHA256 `8d7cbb9e085fbe7c1ec8da28f590f54972fd34eb151da7d958fd0402e2eda6f7`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.19;
library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a / b;
    return c;
  }
  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }
  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}
contract ForeignToken {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
interface Token { 
    function distr(address _to, uint256 _value) public returns (bool);
    function totalSupply() constant public returns (uint256 supply);
    function balanceOf(address _owner) constant public returns (uint256 balance);
}
contract EthereumDiamond is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "Ethereum Diamond";
    string public constant symbol = "ETD";
    uint public constant decimals = 8;
    uint256 public totalSupply = 99000000000000e8;
    uint256 public totalDistributed = 98000000000000e8;
    uint256 public totalRemaining = totalSupply.sub(totalDistributed);
    uint256 public value;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    modifier onlyWhitelist() {
        require(blacklist[msg.sender] == false);
        _;
    }
    function ZeroXEth () public {
        owner = msg.sender;
        value = 34519e8;
        distr(owner, totalDistributed);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function enableWhitelist(address[] addresses) onlyOwner public {
        for (uint i = 0; i < addresses.length; i++) {
            blacklist[addresses[i]] = false;
        }
    }
    function disableWhitelist(address[] addresses) onlyOwner public {
        for (uint i = 0; i < addresses.length; i++) {
            blacklist[addresses[i]] = true;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);
        totalRemaining = totalRemaining.sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function airdrop(address[] addresses) onlyOwner canDistr public {
        require(addresses.length <= 255);
        require(value <= totalRemaining);
        for (uint i = 0; i < addresses.length; i++) {
            require(value <= totalRemaining);
            distr(addresses[i], value);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function distribution(address[] addresses, uint256 amount) onlyOwner canDistr public {
        require(addresses.length <= 255);
        require(amount <= totalRemaining);
        for (uint i = 0; i < addresses.length; i++) {
            require(amount <= totalRemaining);
            distr(addresses[i], amount);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function distributeAmounts(address[] addresses, uint256[] amounts) onlyOwner canDistr public {
        require(addresses.length <= 255);
        require(addresses.length == amounts.length);
        for (uint8 i = 0; i < addresses.length; i++) {
            require(amounts[i] <= totalRemaining);
            distr(addresses[i], amounts[i]);
            if (totalDistributed >= totalSupply) {
                distributionFinished = true;
            }
        }
    }
    function () external payable {
            getTokens();
     }
    function getTokens() payable canDistr onlyWhitelist public {
        if (value > totalRemaining) {
            value = totalRemaining;
        }
        require(value <= totalRemaining);
        address investor = msg.sender;
        uint256 toGive = value;
        distr(investor, toGive);
        if (toGive > 0) {
            blacklist[investor] = true;
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        value = value.div(100000).mul(99999);
    }
    function balanceOf(address _owner) constant public returns (uint256) {
	    return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        ForeignToken t = ForeignToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        uint256 etherBalance = this.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        Burn(burner, _value);
    }
    function withdrawForeignTokens(address _tokenContract) onlyOwner public returns (bool) {
        ForeignToken token = ForeignToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_116d8aeb4b40

文件 `units/program.sol`；SHA256 `78480600877ec191188400fc161dd12795180c370e1b6a40baae26181c4e18cd`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        assert(c >= a);
        return c;
    }
}
contract AltcoinToken {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract spinetwork is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "Simple Payment Instant Token";
    string public constant symbol = "SPIT";
    uint public constant decimals = 8;
    uint256 public totalSupply = 10000000000e8;
    uint256 public totalDistributed = 0;        
    uint256 public tokensPerEth = 20000000e8;
    uint256 public constant minContribution = 1 ether / 100; 
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Airdrop(address indexed _owner, uint _amount, uint _balance);
    event TokensPerEthUpdated(uint _tokensPerEth);
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function spitoken () public {
        owner = msg.sender;
        uint256 devTokens = 1000000000e8;
        distr(owner, devTokens);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);        
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
    }
    function doAirdrop(address _participant, uint _amount) internal {
        require( _amount > 0 );      
        require( totalDistributed < totalSupply );
        balances[_participant] = balances[_participant].add(_amount);
        totalDistributed = totalDistributed.add(_amount);
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        Airdrop(_participant, _amount, balances[_participant]);
        Transfer(address(0), _participant, _amount);
    }
    function adminClaimAirdrop(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function adminClaimAirdropMultiple(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function updateTokensPerEth(uint _tokensPerEth) public onlyOwner {        
        tokensPerEth = _tokensPerEth;
        TokensPerEthUpdated(_tokensPerEth);
    }
    function () external payable {
        getTokens();
     }
    function getTokens() payable canDistr  public {
        uint256 tokens = 0;
        require( msg.value >= minContribution );
        require( msg.value > 0 );
        tokens = tokensPerEth.mul(msg.value) / 1 ether;        
        address investor = msg.sender;
        if (tokens > 0) {
            distr(investor, tokens);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function balanceOf(address _owner) constant public returns (uint256) {
        return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        AltcoinToken t = AltcoinToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        address myAddress = this;
        uint256 etherBalance = myAddress.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        Burn(burner, _value);
    }
    function withdrawAltcoinTokens(address _tokenContract) onlyOwner public returns (bool) {
        AltcoinToken token = AltcoinToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_2d5de0155ecf

文件 `units/program.sol`；SHA256 `7f10cf80d8cecfa397bbf6664d4151184b57bcb9c1926301328e8d4498c802ae`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) {
      return 0;
    }
    uint256 c = a * b;
    assert(c / a == b);
    return c;
  }
  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    // assert(b > 0); // Solidity automatically throws when dividing by 0
    uint256 c = a / b;
    // assert(a == b * c + a % b); // There is no case in which this doesn't hold
    return c;
  }
  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }
  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}
pragma solidity ^0.4.24;
library AddressUtils {
  function isContract(address addr) internal view returns (bool) {
    uint256 size;
    assembly { size := extcodesize(addr) }  // solium-disable-line security/no-inline-assembly
    return size > 0;
  }
}
pragma solidity ^0.4.24;
contract DelegateProxy {
  function delegatedFwd(address _dst, bytes _calldata) internal {
    require(isContract(_dst));
    assembly {
      let result := delegatecall(sub(gas, 10000), _dst, add(_calldata, 0x20), mload(_calldata), 0, 0)
      let size := returndatasize
      let ptr := mload(0x40)
      returndatacopy(ptr, 0, size)
      switch result case 0 {revert(ptr, size)}
      default {return (ptr, size)}
    }
  }
  function isContract(address _target) internal view returns (bool) {
    uint256 size;
    assembly {size := extcodesize(_target)}
    return size > 0;
  }
}
pragma solidity ^0.4.13;
contract DSAuthority {
  function canCall(
    address src, address dst, bytes4 sig
  ) public view returns (bool);
}
contract DSAuthEvents {
  event LogSetAuthority (address indexed authority);
  event LogSetOwner     (address indexed owner);
}
contract DSAuth is DSAuthEvents {
  DSAuthority  public  authority;
  address      public  owner;
  function DSAuth() public {
    owner = msg.sender;
    LogSetOwner(msg.sender);
  }
  function setOwner(address owner_)
  public
  auth
  {
    owner = owner_;
    LogSetOwner(owner);
  }
  function setAuthority(DSAuthority authority_)
  public
  auth
  {
    authority = authority_;
    LogSetAuthority(authority);
  }
  modifier auth {
    require(isAuthorized(msg.sender, msg.sig));
    _;
  }
  function isAuthorized(address src, bytes4 sig) internal view returns (bool) {
    if (src == address(this)) {
      return true;
    } else if (src == owner) {
      return true;
    } else if (authority == DSAuthority(0)) {
      return false;
    } else {
      return authority.canCall(src, this, sig);
    }
  }
}
pragma solidity ^0.4.24;
contract ERC721Basic {
  event Transfer(address indexed _from, address indexed _to, uint256 _tokenId, uint256 _timestamp);
  event Approval(address indexed _owner, address indexed _approved, uint256 _tokenId);
  event ApprovalForAll(address indexed _owner, address indexed _operator, bool _approved);
  function balanceOf(address _owner) public view returns (uint256 _balance);
  function ownerOf(uint256 _tokenId) public view returns (address _owner);
  function exists(uint256 _tokenId) public view returns (bool _exists);
  function approve(address _to, uint256 _tokenId) public;
  function getApproved(uint256 _tokenId) public view returns (address _operator);
  function setApprovalForAll(address _operator, bool _approved) public;
  function isApprovedForAll(address _owner, address _operator) public view returns (bool);
  function transferFrom(address _from, address _to, uint256 _tokenId) public;
  function safeTransferFrom(address _from, address _to, uint256 _tokenId) public;
  function safeTransferFrom(
    address _from,
    address _to,
    uint256 _tokenId,
    bytes _data
  )
  public;
}
pragma solidity ^0.4.24;
contract ERC721Enumerable is ERC721Basic {
  function totalSupply() public view returns (uint256);
  function tokenOfOwnerByIndex(address _owner, uint256 _index) public view returns (uint256 _tokenId);
  function tokenByIndex(uint256 _index) public view returns (uint256);
}
contract ERC721Metadata is ERC721Basic {
  function name() public view returns (string _name);
  function symbol() public view returns (string _symbol);
  function tokenURI(uint256 _tokenId) public view returns (address);
}
contract ERC721 is ERC721Basic, ERC721Enumerable, ERC721Metadata {
}
pragma solidity ^0.4.24;
contract ERC721BasicToken is ERC721Basic {
  using SafeMath for uint256;
  using AddressUtils for address;
  bytes4 constant ERC721_RECEIVED = 0xf0b9e5ba;
  mapping (uint256 => address) internal tokenOwner;
  mapping (uint256 => address) internal tokenApprovals;
  mapping (address => uint256) internal ownedTokensCount;
  mapping (address => mapping (address => bool)) internal operatorApprovals;
  modifier onlyOwnerOf(uint256 _tokenId) {
    require(ownerOf(_tokenId) == msg.sender);
    _;
  }
  modifier canTransfer(uint256 _tokenId) {
    require(isApprovedOrOwner(msg.sender, _tokenId));
    _;
  }
  function balanceOf(address _owner) public view returns (uint256) {
    require(_owner != address(0));
    return ownedTokensCount[_owner];
  }
  function ownerOf(uint256 _tokenId) public view returns (address) {
    address owner = tokenOwner[_tokenId];
    require(owner != address(0));
    return owner;
  }
  function exists(uint256 _tokenId) public view returns (bool) {
    address owner = tokenOwner[_tokenId];
    return owner != address(0);
  }
  function approve(address _to, uint256 _tokenId) public {
    address owner = ownerOf(_tokenId);
    require(_to != owner);
    require(msg.sender == owner || isApprovedForAll(owner, msg.sender));
    if (getApproved(_tokenId) != address(0) || _to != address(0)) {
      tokenApprovals[_tokenId] = _to;
      Approval(owner, _to, _tokenId);
    }
  }
  function getApproved(uint256 _tokenId) public view returns (address) {
    return tokenApprovals[_tokenId];
  }
  function setApprovalForAll(address _to, bool _approved) public {
    require(_to != msg.sender);
    operatorApprovals[msg.sender][_to] = _approved;
    ApprovalForAll(msg.sender, _to, _approved);
  }
  function isApprovedForAll(address _owner, address _operator) public view returns (bool) {
    return operatorApprovals[_owner][_operator];
  }
  function transferFrom(address _from, address _to, uint256 _tokenId) public canTransfer(_tokenId) {
    require(_from != address(0));
    require(_to != address(0));

    clearApproval(_from, _tokenId);
    removeTokenFrom(_from, _tokenId);
    addTokenTo(_to, _tokenId);

    Transfer(_from, _to, _tokenId, now);
  }
  function safeTransferFrom(
    address _from,
    address _to,
    uint256 _tokenId
  )
  public
  canTransfer(_tokenId)
  {
    safeTransferFrom(_from, _to, _tokenId, "");
  }
  function safeTransferFrom(
    address _from,
    address _to,
    uint256 _tokenId,
    bytes _data
  )
  public
  canTransfer(_tokenId)
  {
    transferFrom(_from, _to, _tokenId);
    require(checkAndCallSafeTransfer(_from, _to, _tokenId, _data));
  }
  function isApprovedOrOwner(address _spender, uint256 _tokenId) internal view returns (bool) {
    address owner = ownerOf(_tokenId);
    return _spender == owner || getApproved(_tokenId) == _spender || isApprovedForAll(owner, _spender);
  }
  function _mint(address _to, uint256 _tokenId) internal {
    require(_to != address(0));
    addTokenTo(_to, _tokenId);
    Transfer(address(0), _to, _tokenId, now);
  }
  function _burn(address _owner, uint256 _tokenId) internal {
    clearApproval(_owner, _tokenId);
    removeTokenFrom(_owner, _tokenId);
    Transfer(_owner, address(0), _tokenId, now);
  }
  function clearApproval(address _owner, uint256 _tokenId) internal {
    require(ownerOf(_tokenId) == _owner);
    if (tokenApprovals[_tokenId] != address(0)) {
      tokenApprovals[_tokenId] = address(0);
      Approval(_owner, address(0), _tokenId);
    }
  }
  function addTokenTo(address _to, uint256 _tokenId) internal {
    require(tokenOwner[_tokenId] == address(0));
    tokenOwner[_tokenId] = _to;
    ownedTokensCount[_to] = ownedTokensCount[_to].add(1);
  }
  function removeTokenFrom(address _from, uint256 _tokenId) internal {
    require(ownerOf(_tokenId) == _from);
    ownedTokensCount[_from] = ownedTokensCount[_from].sub(1);
    tokenOwner[_tokenId] = address(0);
  }
  function checkAndCallSafeTransfer(
    address _from,
    address _to,
    uint256 _tokenId,
    bytes _data
  )
  internal
  returns (bool)
  {
    if (!_to.isContract()) {
      return true;
    }
    bytes4 retval = ERC721Receiver(_to).onERC721Received(_from, _tokenId, _data);
    return (retval == ERC721_RECEIVED);
  }
}
pragma solidity ^0.4.21;
contract ERC721Receiver {
  bytes4 constant ERC721_RECEIVED = 0xf0b9e5ba;
  function onERC721Received(address _from, uint256 _tokenId, bytes _data) public returns(bytes4);
}
pragma solidity ^0.4.21;
contract ERC721Holder is ERC721Receiver {
  function onERC721Received(address, uint256, bytes) public returns(bytes4) {
    return ERC721_RECEIVED;
  }
}
pragma solidity ^0.4.24;
contract ERC721Token is ERC721, ERC721BasicToken {
  string internal name_;
  string internal symbol_;
  mapping(address => uint256[]) internal ownedTokens;
  mapping(uint256 => uint256) internal ownedTokensIndex;
  uint256[] internal allTokens;
  mapping(uint256 => uint256) internal allTokensIndex;
  mapping(uint256 => address) internal tokenURIs;
  function ERC721Token(string _name, string _symbol) public {
    name_ = _name;
    symbol_ = _symbol;
  }
  function name() public view returns (string) {
    return name_;
  }
  function symbol() public view returns (string) {
    return symbol_;
  }
  function tokenURI(uint256 _tokenId) public view returns (address) {
    require(exists(_tokenId));
    return tokenURIs[_tokenId];
  }
  function tokenOfOwnerByIndex(address _owner, uint256 _index) public view returns (uint256) {
    require(_index < balanceOf(_owner));
    return ownedTokens[_owner][_index];
  }
  function totalSupply() public view returns (uint256) {
    return allTokens.length;
  }
  function tokenByIndex(uint256 _index) public view returns (uint256) {
    require(_index < totalSupply());
    return allTokens[_index];
  }
  function _setTokenURI(uint256 _tokenId, address _uri) internal {
    require(exists(_tokenId));
    tokenURIs[_tokenId] = _uri;
  }
  function addTokenTo(address _to, uint256 _tokenId) internal {
    super.addTokenTo(_to, _tokenId);
    uint256 length = ownedTokens[_to].length;
    ownedTokens[_to].push(_tokenId);
    ownedTokensIndex[_tokenId] = length;
  }
  function removeTokenFrom(address _from, uint256 _tokenId) internal {
    super.removeTokenFrom(_from, _tokenId);
    uint256 tokenIndex = ownedTokensIndex[_tokenId];
    uint256 lastTokenIndex = ownedTokens[_from].length.sub(1);
    uint256 lastToken = ownedTokens[_from][lastTokenIndex];
    ownedTokens[_from][tokenIndex] = lastToken;
    ownedTokens[_from][lastTokenIndex] = 0;
    ownedTokens[_from].length--;
    ownedTokensIndex[_tokenId] = 0;
    ownedTokensIndex[lastToken] = tokenIndex;
  }
  function _mint(address _to, uint256 _tokenId) internal {
    super._mint(_to, _tokenId);
    allTokensIndex[_tokenId] = allTokens.length;
    allTokens.push(_tokenId);
  }
}
pragma solidity ^0.4.24;
contract EternalDb is DSAuth {
  enum Types {UInt, String, Address, Bytes, Bytes32, Boolean, Int}
  event EternalDbEvent(bytes32[] records, uint[] values, uint timestamp);
  function EternalDb(){
  }
  mapping(bytes32 => uint) UIntStorage;
  function getUIntValue(bytes32 record) constant returns (uint){
    return UIntStorage[record];
  }
  function getUIntValues(bytes32[] records) constant returns (uint[] results){
    results = new uint[](records.length);
    for (uint i = 0; i < records.length; i++) {
      results[i] = UIntStorage[records[i]];
    }
  }
  function setUIntValue(bytes32 record, uint value)
  auth
  {
    UIntStorage[record] = value;
    bytes32[] memory records = new bytes32[](1);
    records[0] = record;
    uint[] memory values = new uint[](1);
    values[0] = value;
    emit EternalDbEvent(records, values, now);
  }
  function setUIntValues(bytes32[] records, uint[] values)
  auth
  {
    for (uint i = 0; i < records.length; i++) {
      UIntStorage[records[i]] = values[i];
    }
    emit EternalDbEvent(records, values, now);
  }
  function deleteUIntValue(bytes32 record)
  auth
  {
    delete UIntStorage[record];
  }
  mapping(bytes32 => string) StringStorage;
  function getStringValue(bytes32 record) constant returns (string){
    return StringStorage[record];
  }
  function setStringValue(bytes32 record, string value)
  auth
  {
    StringStorage[record] = value;
  }
  function deleteStringValue(bytes32 record)
  auth
  {
    delete StringStorage[record];
  }
  mapping(bytes32 => address) AddressStorage;
  function getAddressValue(bytes32 record) constant returns (address){
    return AddressStorage[record];
  }
  function setAddressValues(bytes32[] records, address[] values)
  auth
  {
    for (uint i = 0; i < records.length; i++) {
      AddressStorage[records[i]] = values[i];
    }
  }
  function setAddressValue(bytes32 record, address value)
  auth
  {
    AddressStorage[record] = value;
  }
  function deleteAddressValue(bytes32 record)
  auth
  {
    delete AddressStorage[record];
  }
  mapping(bytes32 => bytes) BytesStorage;

  function getBytesValue(bytes32 record) constant returns (bytes){
    return BytesStorage[record];
  }
  function setBytesValue(bytes32 record, bytes value)
  auth
  {
    BytesStorage[record] = value;
  }
  function deleteBytesValue(bytes32 record)
  auth
  {
    delete BytesStorage[record];
  }
  mapping(bytes32 => bytes32) Bytes32Storage;
  function getBytes32Value(bytes32 record) constant returns (bytes32){
    return Bytes32Storage[record];
  }
  function getBytes32Values(bytes32[] records) constant returns (bytes32[] results){
    results = new bytes32[](records.length);
    for (uint i = 0; i < records.length; i++) {
      results[i] = Bytes32Storage[records[i]];
    }
  }
  function setBytes32Value(bytes32 record, bytes32 value)
  auth
  {
    Bytes32Storage[record] = value;
  }
  function setBytes32Values(bytes32[] records, bytes32[] values)
  auth
  {
    for (uint i = 0; i < records.length; i++) {
      Bytes32Storage[records[i]] = values[i];
    }
  }
  function deleteBytes32Value(bytes32 record)
  auth
  {
    delete Bytes32Storage[record];
  }
  mapping(bytes32 => bool) BooleanStorage;
  function getBooleanValue(bytes32 record) constant returns (bool){
    return BooleanStorage[record];
  }
  function getBooleanValues(bytes32[] records) constant returns (bool[] results){
    results = new bool[](records.length);
    for (uint i = 0; i < records.length; i++) {
      results[i] = BooleanStorage[records[i]];
    }
  }
  function setBooleanValue(bytes32 record, bool value)
  auth
  {
    BooleanStorage[record] = value;
  }
  function setBooleanValues(bytes32[] records, bool[] values)
  auth
  {
    for (uint i = 0; i < records.length; i++) {
      BooleanStorage[records[i]] = values[i];
    }
  }
  function deleteBooleanValue(bytes32 record)
  auth
  {
    delete BooleanStorage[record];
  }
  mapping(bytes32 => int) IntStorage;

  function getIntValue(bytes32 record) constant returns (int){
    return IntStorage[record];
  }
  function getIntValues(bytes32[] records) constant returns (int[] results){
    results = new int[](records.length);
    for (uint i = 0; i < records.length; i++) {
      results[i] = IntStorage[records[i]];
    }
  }
  function setIntValue(bytes32 record, int value)
  auth
  {
    IntStorage[record] = value;
  }
  function setIntValues(bytes32[] records, int[] values)
  auth
  {
    for (uint i = 0; i < records.length; i++) {
      IntStorage[records[i]] = values[i];
    }
  }
  function deleteIntValue(bytes32 record)
  auth
  {
    delete IntStorage[record];
  }
}
pragma solidity ^0.4.24;
contract MemeToken is ERC721Token {
  Registry public registry;
  modifier onlyRegistryEntry() {
    require(registry.isRegistryEntry(msg.sender),"MemeToken: onlyRegistryEntry failed");
    _;
  }
  function MemeToken(Registry _registry)
  ERC721Token("MemeToken", "MEME")
  {
    registry = _registry;
  }
  function mint(address _to, uint256 _tokenId)
  onlyRegistryEntry
  public
  {
    super._mint(_to, _tokenId);
    tokenURIs[_tokenId] = msg.sender;
  }
  function safeTransferFromMulti(
    address _from,
    address _to,
    uint256[] _tokenIds,
    bytes _data
  ) {
    for (uint i = 0; i < _tokenIds.length; i++) {
      safeTransferFrom(_from, _to, _tokenIds[i], _data);
    }
  }
}
pragma solidity ^0.4.24;
contract MutableForwarder is DelegateProxy, DSAuth {
  address public target = 0xBEeFbeefbEefbeEFbeEfbEEfBEeFbeEfBeEfBeef;
  function setTarget(address _target) public auth {
    target = _target;
  }
  function() payable {
    delegatedFwd(target, msg.data);
  }
}
pragma solidity ^0.4.24;
contract Registry is DSAuth {
  address private dummyTarget; 
  bytes32 public constant challengePeriodDurationKey = keccak256(abi.encodePacked("challengePeriodDuration"));
  bytes32 public constant commitPeriodDurationKey = keccak256(abi.encodePacked("commitPeriodDuration"));
  bytes32 public constant revealPeriodDurationKey = keccak256(abi.encodePacked("revealPeriodDuration"));
  bytes32 public constant depositKey = keccak256(abi.encodePacked("deposit"));
  bytes32 public constant challengeDispensationKey = keccak256(abi.encodePacked("challengeDispensation"));
  bytes32 public constant voteQuorumKey = keccak256(abi.encodePacked("voteQuorum"));
  bytes32 public constant maxTotalSupplyKey = keccak256(abi.encodePacked("maxTotalSupply"));
  bytes32 public constant maxAuctionDurationKey = keccak256(abi.encodePacked("maxAuctionDuration"));
  event MemeConstructedEvent(address registryEntry, uint version, address creator, bytes metaHash, uint totalSupply, uint deposit, uint challengePeriodEnd);
  event MemeMintedEvent(address registryEntry, uint version, address creator, uint tokenStartId, uint tokenEndId, uint totalMinted);
  event ChallengeCreatedEvent(address registryEntry, uint version, address challenger, uint commitPeriodEnd, uint revealPeriodEnd, uint rewardPool, bytes metahash);
  event VoteCommittedEvent(address registryEntry, uint version, address voter, uint amount);
  event VoteRevealedEvent(address registryEntry, uint version, address voter, uint option);
  event VoteAmountClaimedEvent(address registryEntry, uint version, address voter);
  event VoteRewardClaimedEvent(address registryEntry, uint version, address voter, uint amount);
  event ChallengeRewardClaimedEvent(address registryEntry, uint version, address challenger, uint amount);
  event ParamChangeConstructedEvent(address registryEntry, uint version, address creator, address db, string key, uint value, uint deposit, uint challengePeriodEnd);
  event ParamChangeAppliedEvent(address registryEntry, uint version);
  EternalDb public db;
  bool private wasConstructed;
  function construct(EternalDb _db)
  external
  {
    require(address(_db) != 0x0, "Registry: Address can't be 0x0");

    db = _db;
    wasConstructed = true;
    owner = msg.sender;
  }
  modifier onlyFactory() {
    require(isFactory(msg.sender), "Registry: Sender should be factory");
    _;
  }
  modifier onlyRegistryEntry() {
    require(isRegistryEntry(msg.sender), "Registry: Sender should registry entry");
    _;
  }
  modifier notEmergency() {
    require(!isEmergency(),"Registry: Emergency mode is enable");
    _;
  }
  function setFactory(address _factory, bool _isFactory)
  external
  auth
  {
    db.setBooleanValue(keccak256(abi.encodePacked("isFactory", _factory)), _isFactory);
  }
  function addRegistryEntry(address _registryEntry)
  external
  onlyFactory
  notEmergency
  {
    db.setBooleanValue(keccak256(abi.encodePacked("isRegistryEntry", _registryEntry)), true);
  }
  function setEmergency(bool _isEmergency)
  external
  auth
  {
    db.setBooleanValue("isEmergency", _isEmergency);
  }
  function fireMemeConstructedEvent(uint version, address creator, bytes metaHash, uint totalSupply, uint deposit, uint challengePeriodEnd)
  public
  onlyRegistryEntry
  {
    emit MemeConstructedEvent(msg.sender, version, creator, metaHash, totalSupply, deposit, challengePeriodEnd);
  }
  function fireMemeMintedEvent(uint version, address creator, uint tokenStartId, uint tokenEndId, uint totalMinted)
  public
  onlyRegistryEntry
  {
    emit MemeMintedEvent(msg.sender, version, creator, tokenStartId, tokenEndId, totalMinted);
  }
  function fireChallengeCreatedEvent(uint version, address challenger, uint commitPeriodEnd, uint revealPeriodEnd, uint rewardPool, bytes metahash)
  public
  onlyRegistryEntry
  {
    emit ChallengeCreatedEvent(msg.sender, version,  challenger, commitPeriodEnd, revealPeriodEnd, rewardPool, metahash);
  }
  function fireVoteCommittedEvent(uint version, address voter, uint amount)
  public
  onlyRegistryEntry
  {
    emit VoteCommittedEvent(msg.sender, version, voter, amount);
  }
  function fireVoteRevealedEvent(uint version, address voter, uint option)
  public
  onlyRegistryEntry
  {
    emit VoteRevealedEvent(msg.sender, version, voter, option);
  }
  function fireVoteAmountClaimedEvent(uint version, address voter)
  public
  onlyRegistryEntry
  {
    emit VoteAmountClaimedEvent(msg.sender, version, voter);
  }
  function fireVoteRewardClaimedEvent(uint version, address voter, uint amount)
  public
  onlyRegistryEntry
  {
    emit VoteRewardClaimedEvent(msg.sender, version, voter, amount);
  }
  function fireChallengeRewardClaimedEvent(uint version, address challenger, uint amount)
  public
  onlyRegistryEntry
  {
    emit ChallengeRewardClaimedEvent(msg.sender, version, challenger, amount);
  }
  function fireParamChangeConstructedEvent(uint version, address creator, address db, string key, uint value, uint deposit, uint challengePeriodEnd)
  public
  onlyRegistryEntry
  {
    emit ParamChangeConstructedEvent(msg.sender, version, creator, db, key, value, deposit, challengePeriodEnd);
  }
  function fireParamChangeAppliedEvent(uint version)
  public
  onlyRegistryEntry
  {
    emit ParamChangeAppliedEvent(msg.sender, version);
  }
  function isFactory(address factory) public constant returns (bool) {
    return db.getBooleanValue(keccak256(abi.encodePacked("isFactory", factory)));
  }
  function isRegistryEntry(address registryEntry) public constant returns (bool) {
    return db.getBooleanValue(keccak256(abi.encodePacked("isRegistryEntry", registryEntry)));
  }
  function isEmergency() public constant returns (bool) {
    return db.getBooleanValue("isEmergency");
  }
}

```
