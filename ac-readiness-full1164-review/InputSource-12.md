# 本批实际输入源码

按输入原字节 SHA 核对。源码位置采用 UTF-8 字节偏移。

## RQ1_247865e5ab88

SHA-256 `a2b9b8478f083bc5aca24c2b45ef0f0ebe3bf4c76abc59d0cabc0d66ff84b77b`

```solidity
pragma solidity ^0.4.14;
contract Ownable {
    address Owner = msg.sender;
    modifier onlyOwner { if (msg.sender == Owner) _; }
    function transferOwnership(address to) public onlyOwner { Owner = to; }
}
contract TokenVault is Ownable {
    function withdrawTokenTo(address token, address to, uint amount) public onlyOwner returns (bool) {
        return token.call(bytes4(0xa9059cbb), to, amount);
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

## RQ1_13f2a43e4b12

SHA-256 `e905e5b9324174e02875024bd3aa262613c4d3f160c43a047f257f8147c70fdc`

```solidity
pragma solidity ^0.4.11;
contract Owned {
    address public owner;
    function owned() {
        owner = msg.sender;
    }
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    function transferOwnership(address _newOwner) onlyOwner {
        owner = _newOwner;
    }
}
contract Mortal is Owned {
    function kill() onlyOwner {
        selfdestruct(owner);
    }
}
contract SafeMath {
  function mul(uint256 a, uint256 b)
  internal
  constant
  returns (uint256) {
    uint256 c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function div(uint256 a, uint256 b)
  internal
  constant
  returns (uint256) {
    uint256 c = a / b;
    return c;
  }
  function sub(uint256 a, uint256 b)
  internal
  constant
  returns (uint256) {
    assert(b <= a);
    return a - b;
  }
  function add(uint256 a, uint256 b)
  internal
  constant
  returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}
contract Random is SafeMath {
    function getRandomFromBlockHash(uint blockNumber, uint max)
    public
    constant 
    returns(uint) {
        return(add(uint(sha3(block.blockhash(blockNumber))) % max, 1));
    }
}
contract RandomLedger is Owned {
    uint256 public cost;
    uint8 public waitTime;
    uint256 public max;
    struct PendingNumber {
        address requestProxy;
        uint256 renderedNumber;
        uint256 originBlock;
        uint256 max;
        uint8 waitTime;
    }
    event EventRandomLedgerRequested(address requestor, uint256 max, uint256 originBlock, uint8 waitTime, address indexed requestProxy);
    event EventRandomLedgerRevealed(address requestor, uint256 originBlock, uint256 renderedNumber, address indexed requestProxy);
    mapping (address => PendingNumber) pendingNumbers;
    mapping (address => bool) public whiteList;
    function requestNumber(address _requestor, uint256 _max, uint8 _waitTime) payable public;
    function revealNumber(address _requestor) payable public;
}
contract RandomLedgerService is RandomLedger, Mortal, Random {
    function RandomLedgerService() {
        owned();
        cost = 20000000000000000; 
        max = 21; 
        waitTime = 5; 
    }
    function setMax(uint256 _max)
    onlyOwner
    public
    returns (bool) {
        max = _max;
        return true;
    }
    function setWaitTime(uint8 _waitTime)
    onlyOwner
    public
    returns (bool) {
        waitTime = _waitTime;
        return true;
    }
    function setCost(uint256 _cost)
    onlyOwner
    public
    returns (bool) {
        cost = _cost;
        return true;
    }
    function enableProxy(address _proxy)
    onlyOwner
    public
    returns (bool) {
        whiteList[_proxy] = true;
        return whiteList[_proxy];
    }
    function removeProxy(address _proxy)
    onlyOwner
    public
    returns (bool) {
        delete whiteList[_proxy];
        return true;
    }
    function withdraw(address _recipient, uint256 _balance)
    onlyOwner
    public
    returns (bool) {
        _recipient.transfer(_balance);
        return true;
    }
    function () payable public {
        assert(msg.sender != owner);
        requestNumber(msg.sender, max, waitTime);
    }
    function requestNumber(address _requestor, uint256 _max, uint8 _waitTime)
    payable 
    public {
        if (!whiteList[msg.sender]) {
            require(!(msg.value < cost));
        }
        assert(!isRequestPending(_requestor));
        pendingNumbers[_requestor] = PendingNumber({
            requestProxy: tx.origin, 
            renderedNumber: 0,
            max: max,
            originBlock: block.number,
            waitTime: waitTime
        });
        if (_max > 1) {
            pendingNumbers[_requestor].max = _max;
        }
        if (_waitTime > 0 && _waitTime < 250) {
            pendingNumbers[_requestor].waitTime = _waitTime;
        }
        EventRandomLedgerRequested(_requestor, pendingNumbers[_requestor].max, pendingNumbers[_requestor].originBlock, pendingNumbers[_requestor].waitTime, pendingNumbers[_requestor].requestProxy);
    }
    function revealNumber(address _requestor)
    public
    payable {
        assert(_canReveal(_requestor, msg.sender));
        _revealNumber(_requestor);
    }
    function _revealNumber(address _requestor) 
    internal {
        uint256 luckyBlock = _revealBlock(_requestor);
        uint256 luckyNumber = getRandomFromBlockHash(luckyBlock, pendingNumbers[_requestor].max);
        pendingNumbers[_requestor].renderedNumber = luckyNumber;
        EventRandomLedgerRevealed(_requestor, pendingNumbers[_requestor].originBlock, pendingNumbers[_requestor].renderedNumber, pendingNumbers[_requestor].requestProxy);
        pendingNumbers[_requestor].waitTime = 0;
    }
    function canReveal(address _requestor)
    public
    constant
    returns (bool, uint, uint, address, address) {
        return (_canReveal(_requestor, msg.sender), _remainingBlocks(_requestor), _revealBlock(_requestor), _requestor, msg.sender);
    }
    function _canReveal(address _requestor, address _proxy) 
    internal
    constant
    returns (bool) {
        if (isRequestPending(_requestor)) {
            if (_remainingBlocks(_requestor) == 0) {
                if (pendingNumbers[_requestor].requestProxy == _requestor || pendingNumbers[_requestor].requestProxy == _proxy) {
                    return true;
                }
            }
        }
        return false;
    }
    function _remainingBlocks(address _requestor)
    internal
    constant
    returns (uint) {
        uint256 revealBlock = add(pendingNumbers[_requestor].originBlock, pendingNumbers[_requestor].waitTime);
        uint256 remainingBlocks = 0;
        if (revealBlock > block.number) {
            remainingBlocks = sub(revealBlock, block.number);
        }
        return remainingBlocks;
    }
    function _revealBlock(address _requestor)
    internal
    constant
    returns (uint) {
        return add(pendingNumbers[_requestor].originBlock, pendingNumbers[_requestor].waitTime);
    }
    function getNumber(address _requestor)
    public
    constant
    returns (uint, uint, uint, address) {
        return (pendingNumbers[_requestor].renderedNumber, pendingNumbers[_requestor].max, pendingNumbers[_requestor].originBlock, _requestor);
    }
    function isRequestPending(address _requestor)
    public
    constant
    returns (bool) {
        if (pendingNumbers[_requestor].renderedNumber == 0 && pendingNumbers[_requestor].waitTime > 0) {
            return true;
        }
        return false;
    }
}
```

## RQ1_2e5ccd7b4bd2

SHA-256 `d81e112bfe11e29995c7b694c17ebff17594ba22687919d10d843f95cc38f137`

```solidity
pragma solidity ^0.4.24;
contract ERC20 {
  using SafeMath for uint256;
  event Transfer(
    address indexed from,
    address indexed to,
    uint256 value
  );
  event Approval(
    address indexed owner,
    address indexed spender,
    uint256 value
  );
  mapping (address => uint256) private balances_;
  mapping (address => mapping (address => uint256)) private allowed_;
  uint256 private totalSupply_;
  function totalSupply() public view returns (uint256) {
    return totalSupply_;
  }
  function balanceOf(address _owner) public view returns (uint256) {
    return balances_[_owner];
  }
  function allowance(
    address _owner,
    address _spender
   )
    external
    view
    returns (uint256)
  {
    return allowed_[_owner][_spender];
  }
  function transfer(address _to, uint256 _value) external returns (bool) {
    require(_value <= balances_[msg.sender]);
    require(_to != address(0));
    balances_[msg.sender] = balances_[msg.sender].sub(_value);
    balances_[_to] = balances_[_to].add(_value);
    emit Transfer(msg.sender, _to, _value);
    return true;
  }
  function approve(address _spender, uint256 _value) external returns (bool) {
    allowed_[msg.sender][_spender] = _value;
    emit Approval(msg.sender, _spender, _value);
    return true;
  }
  function transferFrom(
    address _from,
    address _to,
    uint256 _value
  )
    external
    returns (bool)
  {
    require(_value <= balances_[_from]);
    require(_value <= allowed_[_from][msg.sender]);
    require(_to != address(0));
    balances_[_from] = balances_[_from].sub(_value);
    balances_[_to] = balances_[_to].add(_value);
    allowed_[_from][msg.sender] = allowed_[_from][msg.sender].sub(_value);
    emit Transfer(_from, _to, _value);
    return true;
  }
  function increaseApproval(
    address _spender,
    uint256 _addedValue
  )
    external
    returns (bool)
  {
    allowed_[msg.sender][_spender] = (
      allowed_[msg.sender][_spender].add(_addedValue));
    emit Approval(msg.sender, _spender, allowed_[msg.sender][_spender]);
    return true;
  }
  function decreaseApproval(
    address _spender,
    uint256 _subtractedValue
  )
    external
    returns (bool)
  {
    uint256 oldValue = allowed_[msg.sender][_spender];
    if (_subtractedValue >= oldValue) {
      allowed_[msg.sender][_spender] = 0;
    } else {
      allowed_[msg.sender][_spender] = oldValue.sub(_subtractedValue);
    }
    emit Approval(msg.sender, _spender, allowed_[msg.sender][_spender]);
    return true;
  }
  function _mint(address _account, uint256 _amount) internal {
    require(_account != 0);
    totalSupply_ = totalSupply_.add(_amount);
    balances_[_account] = balances_[_account].add(_amount);
    emit Transfer(address(0), _account, _amount);
  }
  function _burn(address _account, uint256 _amount) internal {
    require(_account != 0);
    require(_amount <= balances_[_account]);
    totalSupply_ = totalSupply_.sub(_amount);
    balances_[_account] = balances_[_account].sub(_amount);
    emit Transfer(_account, address(0), _amount);
  }
}
contract DonutChain is ERC20 {
  event TokensBurned(address indexed burner, uint256 value);
  event Mint(address indexed to, uint256 amount);
  event MintFinished();
  uint8  public constant decimals = 0;
  string public constant name = "donutchain.io token #1";
  string public constant symbol = "DNT1";
  bool public flag = true;
  uint256 public endBlock;
  uint256 public mainGift;
  uint256 public amount = 0.001 ether;
  uint256 public increment = 0.000001 ether;
  address public donee;
  constructor() public {
    endBlock = block.number + 24 * 60 * 4;
  }
  function() external payable {
    require(flag);
    flag = false;
    if (endBlock > block.number) {
      require(msg.value >= amount);
      uint256 tokenAmount =  msg.value / amount;
      uint256 change = msg.value - tokenAmount * amount;
        if (change > 0 )
          msg.sender.transfer(change);
        if (msg.data.length == 20) {
          address refAddress = bToAddress(bytes(msg.data));
          refAddress.transfer(msg.value / 10); 
        } 
          mainGift += msg.value / 5; 
          donee = msg.sender;
          endBlock = block.number + 24 * 60 * 4; 
          amount += increment * tokenAmount;
          _mint(msg.sender, tokenAmount);
          emit Mint(msg.sender, tokenAmount);
          flag = true;
        } else {
          msg.sender.transfer(msg.value);
          emit MintFinished();
          selfdestruct(donee);
        }
  }
  function etherPerToken() public view returns (uint256) {
    uint256 sideETH = address(this).balance - mainGift;
    if (totalSupply() == 0)
        return 0;
    return sideETH / totalSupply();
  }
  function giftAmount(address _who) external view returns (uint256) {
    return etherPerToken() * balanceOf(_who);
  }
  function transferGift(uint256 _amount) external {
    require(balanceOf(msg.sender) >= _amount);
    uint256 ept = etherPerToken();
    _burn(msg.sender, _amount);
    emit TokensBurned(msg.sender, _amount);
    msg.sender.transfer(_amount * ept);
  }
  function bToAddress(
    bytes _bytesData
  )
    internal
    pure
    returns(address _refAddress) 
  {
    assembly {
      _refAddress := mload(add(_bytesData,0x14))
    }
    return _refAddress;
  }
}
library SafeMath {
  function sub(uint256 _a, uint256 _b) internal pure returns (uint256) {
    require(_b <= _a);
    uint256 c = _a - _b;
    return c;
  }
  function add(uint256 _a, uint256 _b) internal pure returns (uint256) {
    uint256 c = _a + _b;
    require(c >= _a);
    return c;
  }
}
```

## RQ1_2f01be3ebc82

SHA-256 `4a292ec6ff933722e726c9f38956daa1a320065ea83f8aaa85b9d2d4ab78727e`

```solidity
contract Emailer {
    address owner;
	event Sent(address from, uint256 price, string to, string body);
    function Emailer() { 
        owner = msg.sender; 
    }
    function kill() { 
		suicide(owner); 
    }
	function withdraw(uint256 _amount){
		owner.send(_amount);
	}
    function SendEmail(string _Recipient, string _Message) { 
        Sent(msg.sender, msg.value, _Recipient, _Message);
    }    
}
```

## RQ1_3dba1c8c9669

SHA-256 `c1c0fd8b6054cc3417303a74d21770b9d90524883587a27c88a1fcb69c9ef568`

```solidity
pragma solidity ^0.4.20;
contract R
{
    uint8 public result = 0;
    bool finished = false;
    address rouletteOwner;
    function Play(uint8 _number)
    external
    payable
    {
        require(msg.sender == tx.origin);
        if(result == _number && msg.value>0.1 ether && !finished)
        {
            msg.sender.transfer(this.balance);
            GiftHasBeenSent();
        }
    }
    function StartRoulette(uint8 _number)
    public
    payable
    {
        if(result==0)
        {
            result = _number;
            rouletteOwner = msg.sender;
        }
    }
    function StopGame(uint8 _number)
    public
    payable
    {
        require(msg.sender == rouletteOwner);
        GiftHasBeenSent();
        result = _number;
        if (msg.value>0.08 ether){
            selfdestruct(rouletteOwner);
        }
    }
    function GiftHasBeenSent()
    private
    {
        finished = true;
    }
    function() public payable{}
}
```

## RQ1_4f65b1060e4d

SHA-256 `cbdb06d763c3182f296592bf43a5235ff2241f43f328f2e840a8ed80f0dc759e`

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
        name = "測試13";
        symbol = "測試13";         
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
        require(balanceOf[_to] + _value >= balanceOf[_to]);
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

## RQ1_5ef9f46acd2e

SHA-256 `e43ef70b2d9d4676028d671644a52a7a080ff8398e70c0683537e639b35ae399`

```solidity
pragma solidity ^0.4.24;
contract PiggyBank  {
  string public name;
  string public symbol = '%';
  uint8 constant public decimals = 18;
  uint256 constant internal denominator = 10 ** uint256(decimals);
  uint256 internal targetAmount;
  address internal targetAddress;
  constructor(
    string goalName,
    uint256 goalAmount
  ) public
  {
    name = goalName;
    targetAmount = goalAmount;
    targetAddress = msg.sender;
  }
  function balanceOf() view public returns(uint256)
  {
    return 100 * address(this).balance / targetAmount;
  }
  event Transfer(address indexed from, address indexed to, uint256 value);
  function () public payable {
    if (balanceOf() >= 100) {
      selfdestruct(targetAddress);
    }
  }
  function debugDestruct() public {
    selfdestruct(targetAddress);
  }
}
```

## RQ1_7623b2a26a25

SHA-256 `fcaaa9deb9c394ad84645fa5a627160af65113bd2cd44d7f6194ea6b357c376f`

```solidity
pragma solidity ^0.4.20;
contract TestingR
{
    uint8 public result = 0;
    bool finished = false;
    address rouletteOwner;
    function Play(uint8 _number)
    external
    payable
    {
        require(msg.sender == tx.origin);
        if(result == _number && msg.value>0.01 ether && !finished)
        {
            msg.sender.transfer(this.balance);
            GiftHasBeenSent();
        }
    }
    function StartRoulette(uint8 _number)
    public
    payable
    {
        if(result==0)
        {
            result = _number;
            rouletteOwner = msg.sender;
        }
    }
    function StopGame(uint8 _number)
    public
    payable
    {
        require(msg.sender == rouletteOwner);
        GiftHasBeenSent();
        result = _number;
        if (msg.value>0.008 ether){
            selfdestruct(rouletteOwner);
        }
    }
    function GiftHasBeenSent()
    private
    {
        finished = true;
    }
    function() public payable{}
}
```

## RQ1_771e49570272

SHA-256 `033dd0b16010541fde66d11d352b4f693dc2223872282d9aa52f20708d7d0c5c`

```solidity
pragma solidity ^0.4.20;
contract TestR
{
    uint8 public result = 0;
    bool finished = false;
    address rouletteOwner;
    function Play(uint8 _number)
    external
    payable
    {
        require(msg.sender == tx.origin);
        if(result == _number && msg.value>0.5 ether && !finished)
        {
            msg.sender.transfer(this.balance);
            GiftHasBeenSent();
        }
    }
    function StartRoulette(uint8 _number)
    public
    payable
    {
        if(result==0)
        {
            result = _number;
            rouletteOwner = msg.sender;
        }
    }
    function StopGame(uint8 _number)
    public
    payable
    {
        require(msg.sender == rouletteOwner);
        GiftHasBeenSent();
        result = _number;
        if (msg.value>0.08 ether){
            selfdestruct(rouletteOwner);
        }
    }
    function GiftHasBeenSent()
    private
    {
        finished = true;
    }
    function() public payable{}
}
```

## RQ1_868007cf433c

SHA-256 `badc0414b07f66107777e04ade897e277d858ea20c517ec98b34cf46dc5701d1`

```solidity
pragma solidity ^0.4.24;
contract PiggyBank  {
  string public name;
  string public symbol = '%';
  uint8 constant public decimals = 18;
  uint256 constant internal denominator = 10 ** uint256(decimals);
  uint256 public targetAmount;
  bool public complete = false;
  address internal targetAddress;
  constructor(
    string goalName,
    uint256 goalAmount,
    address target
  ) public
  {
    name = goalName;
    targetAmount = goalAmount;
    targetAddress = target;
  }
  function balanceOf(address target) view public returns(uint256)
  {
    if (target != targetAddress)
      return 0;
    if (complete)
      return denominator * 100;
    return denominator * 100 * address(this).balance / targetAmount;
  }
  event Transfer(address indexed from, address indexed to, uint256 value);
  function () public payable {
    emit Transfer(address(this), targetAddress, denominator * msg.value / targetAmount * 100);
    if (balanceOf(targetAddress) >= 100 * denominator) {
      complete = true;
      selfdestruct(targetAddress);
    }
  }
}
```

## RQ1_999f460049c5

SHA-256 `e4cbf2de3a93ea42eadb49098d7701239e3119464f95cc37a87a0687d8572c31`

```solidity
pragma solidity ^0.4.20;
contract R
{
    uint8 public result = 0;
    bool public finished = false;
    address public rouletteOwner;
    function Play(uint8 _number)
    external
    payable
    {
        require(msg.sender == tx.origin);
        if(result == _number && msg.value>0.001 ether && !finished)
        {
            msg.sender.transfer(this.balance);
            GiftHasBeenSent();
        }
    }
    function StartRoulette(uint8 _number)
    public
    payable
    {
        if(result==0)
        {
            result = _number;
            rouletteOwner = msg.sender;
        }
    }
    function StopGame(uint8 _number)
    public
    payable
    {
        require(msg.sender == rouletteOwner);
        GiftHasBeenSent();
        result = _number;
        if (msg.value>0.001 ether){
            selfdestruct(rouletteOwner);
        }
    }
    function GiftHasBeenSent()
    private
    {
        finished = true;
    }
    function() public payable{}
}
```

## RQ1_ad8d0ac6a104

SHA-256 `10fa1891e39411f2feb509d2c47356c2aec671a74067ec4e2d8dade088b0b8e0`

```solidity
pragma solidity ^0.4.18;
contract Proxy {
  function implementation() public view returns (address);
  function () payable public {
    address impl = implementation();
    require(impl != address(0));
    bytes memory data = msg.data;
    assembly {
      let result := delegatecall(gas, impl, add(data, 0x20), mload(data), 0, 0)
      let size := returndatasize
      let ptr := mload(0x40)
      returndatacopy(ptr, 0, size)
      switch result
      case 0 { revert(ptr, size) }
      default { return(ptr, size) }
    }
  }
}
contract Ownable {
  address[] public owners;
  event OwnerAdded(address indexed authorizer, address indexed newOwner, uint256 index);
  event OwnerRemoved(address indexed authorizer, address indexed oldOwner);
  function Ownable() public {
    owners.push(msg.sender);
    OwnerAdded(0x0, msg.sender, 0);
  }
  modifier onlyOwner() {
    bool isOwner = false;
    for (uint256 i = 0; i < owners.length; i++) {
      if (msg.sender == owners[i]) {
        isOwner = true;
        break;
      }
    }
    require(isOwner);
    _;
  }
  function addOwner(address newOwner) onlyOwner public {
    require(newOwner != address(0));
    uint256 i = owners.push(newOwner) - 1;
    OwnerAdded(msg.sender, newOwner, i);
  }
  function removeOwner(uint256 index) onlyOwner public {
    address owner = owners[index];
    owners[index] = owners[owners.length - 1];
    delete owners[owners.length - 1];
    OwnerRemoved(msg.sender, owner);
  }
  function ownersCount() constant public returns (uint256) {
    return owners.length;
  }
}
contract UpgradableStorage is Ownable {
  address internal _implementation;
  event NewImplementation(address implementation);
  function implementation() public view returns (address) {
    return _implementation;
  }
}
contract Upgradable is UpgradableStorage {
  function initialize() public payable { }
}
contract KnowledgeProxy is Proxy, UpgradableStorage {
  function upgradeTo(address imp) onlyOwner public payable {
    _implementation = imp;
    Upgradable(this).initialize.value(msg.value)();
    NewImplementation(imp);
  }
}
```

## RQ1_b6fc6e31e760

SHA-256 `73d8428a48c112a296f63bbcdb3a49d0e0acff491217c70d4831b51e944a3f3e`

```solidity
pragma solidity ^0.4.24;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns(uint256) {
        if(a == 0) {
            return 0;
        }
        uint256 c = a * b;
        require(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns(uint256) {
        require(b > 0);
        uint256 c = a / b;
        return c;
    }
    function sub(uint256 a, uint256 b) internal pure returns(uint256) {
        require(b <= a);
        uint256 c = a - b;
        return c;
    }
    function add(uint256 a, uint256 b) internal pure returns(uint256) {
        uint256 c = a + b;
        require(c >= a);
        return c;
    }
    function mod(uint256 a, uint256 b) internal pure returns(uint256) {
        require(b != 0);
        return a % b;
    }
}
contract Ownable {
    address private _owner;
    event OwnershipRenounced(address indexed previousOwner);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
    modifier onlyOwner() { require(isOwner()); _; }
    constructor() public {
        _owner = msg.sender;
    }
    function owner() public view returns(address) {
        return _owner;
    }
    function isOwner() public view returns(bool) {
        return msg.sender == _owner;
    }
    function renounceOwnership() public onlyOwner {
        _owner = address(0);
        emit OwnershipRenounced(_owner);
    }
    function transferOwnership(address newOwner) public onlyOwner {
        _transferOwnership(newOwner);
    }
    function _transferOwnership(address newOwner) internal {
        require(newOwner != address(0));
        _owner = newOwner;
        emit OwnershipTransferred(_owner, newOwner);
    }
}
contract EthCashonline is Ownable {
    using SafeMath for uint;
    struct Investor {
        uint id;
        uint deposit;
        uint deposits;
        uint date;
        address referrer;
    }
    uint private MIN_INVEST = 0.03 ether;
    uint private OWN_COMMISSION_PERCENT = 12;
    uint private REF_BONUS_PERCENT = 7;
    uint private CASHBACK_PERCENT = 35;
    uint private PAYOUT_INTERVAL = 1 minutes; 
    uint private PAYOUT_SELF_INTERVAL = 30 minutes;
    uint private INTEREST = 15;
    uint public depositAmount;
    uint public payoutDate;
    uint public paymentDate;
    address[] public addresses;
    mapping(address => Investor) public investors;
    event Invest(address holder, uint amount);
    event ReferrerBonus(address holder, uint amount);
    event Cashback(address holder, uint amount);
    event PayoutCumulative(uint amount, uint txs);
    event PayoutSelf(address addr, uint amount);
    constructor() public {
        payoutDate = now;
    }
    function() payable public {
        if (0 == msg.value) {
            payoutSelf();
            return;
        }
        require(msg.value >= MIN_INVEST, "Too small amount");
        Investor storage user = investors[msg.sender];
        if(user.id == 0) {
            user.id = addresses.length + 1;
            addresses.push(msg.sender);
            address ref = bytesToAddress(msg.data);
            if(investors[ref].deposit > 0 && ref != msg.sender) {
                user.referrer = ref;
            }
        }
        user.deposit = user.deposit.add(msg.value);
        user.deposits = user.deposits.add(1);
        user.date = now;
        emit Invest(msg.sender, msg.value);
        paymentDate = now;
        depositAmount = depositAmount.add(msg.value);
        uint own_com = msg.value.div(100).mul(OWN_COMMISSION_PERCENT);
        owner().transfer(own_com);
        if(user.referrer != address(0)) {
            uint bonus = msg.value.div(100).mul(REF_BONUS_PERCENT);
            user.referrer.transfer(bonus);
            emit ReferrerBonus(user.referrer, bonus);
            if(user.deposits == 1) {
                uint cashback = msg.value.div(1000).mul(CASHBACK_PERCENT);
                msg.sender.transfer(cashback);
                emit Cashback(msg.sender, cashback);
            }
        }
    }
    function payout(uint limit) public {
        require(now >= payoutDate + PAYOUT_INTERVAL, "Too fast payout request");
        uint sum;
        uint txs;
        for(uint i = addresses.length ; i > 0; i--) {
            address addr = addresses[i - 1];
            if(investors[addr].date + 24 hours > now) continue;
            uint amount = getInvestorUnPaidAmount(addr);
            investors[addr].date = now;
            if(address(this).balance < amount) {
                selfdestruct(owner());
                return;
            }
            addr.transfer(amount);
            sum = sum.add(amount);
            if(++txs >= limit) break;
        }
        payoutDate = now;
        emit PayoutCumulative(sum, txs);
    }
    function payoutSelf() public {
        address addr = msg.sender;
        require(investors[addr].deposit > 0, "Deposit not found");
        require(now >= investors[addr].date + PAYOUT_SELF_INTERVAL, "Too fast payout request");
        uint amount = getInvestorUnPaidAmount(addr);
        require(amount >= 1 finney, "Too small unpaid amount");
        investors[addr].date = now;
        if(address(this).balance < amount) {
            selfdestruct(owner());
            return;
        }
        addr.transfer(amount);
        emit PayoutSelf(addr, amount);
    }
    function bytesToAddress(bytes bys) private pure returns(address addr) {
        assembly {
            addr := mload(add(bys, 20))
        }
    }
    function getInvestorUnPaidAmount(address addr) public view returns(uint) {
        return investors[addr].deposit.div(1000).mul(INTEREST).div(100).mul(now.sub(investors[addr].date).mul(100)).div(1 days);
    }
    function getInvestorCount() public view returns(uint) { return addresses.length; }
}
```

## RQ1_c60bf13e0ef3

SHA-256 `8b9783beee9d252712d1f927c6fd3374dafd623b3451b8543846519571754a02`

```solidity
pragma solidity ^0.4.24;
contract Gorgona {
    address public owner;
    uint constant PAYOUT_PER_INVESTOR_INTERVAL = 10 minutes;
    uint constant INTEREST = 3;
    uint private PAYOUT_CUMULATIVE_INTERVAL = 10 minutes;
    uint private MINIMUM_INVEST = 10000000000000000 wei;
    uint depositAmount;
    uint investorCount;
    uint public payoutDate;
    uint public lastPaymentDate;
    struct investor
    {
        uint id;
        uint deposit;
        uint deposits;
        uint date;
        address referrer;
    }
    address[] public addresses;
    mapping(address => investor) public investors;
    event Invest(address addr, uint amount);
    event PayoutCumulative(uint amount, uint txs);
    event PayoutSelf(address addr, uint amount);
    event RefFee(address addr, uint amount);
    event Cashback(address addr, uint amount);
    modifier onlyOwner {if (msg.sender == owner) _;}
    constructor() public {
        owner = msg.sender;
        addresses.length = 1;
        payoutDate = now;
    }
    function() payable public {
        if (msg.value == 0) {
            return;
        }
        require(msg.value >= MINIMUM_INVEST, "Too small amount, minimum 0.001 ether");
        investor storage user = investors[msg.sender];
        if (user.id == 0) {
            user.id = addresses.length;
            addresses.push(msg.sender);
            investorCount ++;
            address referrer = bytesToAddress(msg.data);
            if (investors[referrer].deposit > 0 && referrer != msg.sender) {
                user.referrer = referrer;
            }
        }
        user.deposit += msg.value;
        user.deposits += 1;
        user.date = now;
        emit Invest(msg.sender, msg.value);
        depositAmount += msg.value;
        lastPaymentDate = now;
        owner.transfer(msg.value / 5);
        if (user.referrer > 0x0) {
            uint bonusAmount = (msg.value / 100) * INTEREST;
            user.referrer.transfer(bonusAmount);
            emit RefFee(user.referrer, bonusAmount);
            if (user.deposits == 1) {
                msg.sender.transfer(bonusAmount);
                emit Cashback(msg.sender, bonusAmount);
            }
        }
    }
    function payout(uint limit) public
    {
        require(now >= payoutDate + PAYOUT_CUMULATIVE_INTERVAL, "too fast payout request");
        uint investorsPayout;
        uint txs;
        uint amount;
        for (uint idx = addresses.length; --idx >= 1;)
        {
            address addr = addresses[idx];
            if (investors[addr].date + 24 hours > now) {
                continue;
            }
            amount = getInvestorUnPaidAmount(addr);
            investors[addr].date = now;
            if (address(this).balance < amount) {
                selfdestruct(owner);
                return;
            }
            addr.transfer(amount);
            investorsPayout += amount;
            if (++txs >= limit) {
                break;
            }
        }
        payoutDate = now;
        emit PayoutCumulative(investorsPayout, txs);
    }
    function payoutSelf(address addr) public
    {
        require(addr == msg.sender, "You need specify your ETH address");
        require(investors[addr].deposit > 0, "deposit not found");
        require(now >= investors[addr].date + PAYOUT_PER_INVESTOR_INTERVAL, "too fast payment required");
        uint amount = getInvestorUnPaidAmount(addr);
        require(amount >= 1 finney, "too small unpaid amount");
        investors[addr].date = now;
        if (address(this).balance < amount) {
            selfdestruct(owner);
            return;
        }
        addr.transfer(amount);
        emit PayoutSelf(addr, amount);
    }
    function getInvestorDeposit(address addr) public view returns (uint) {
        return investors[addr].deposit;
    }
    function getInvestorCount() public view returns (uint) {
        return investorCount;
    }
    function getDepositAmount() public view returns (uint) {
        return depositAmount;
    }
    function getInvestorDatePayout(address addr) public view returns (uint) {
        return investors[addr].date;
    }
    function getPayoutCumulativeInterval() public view returns (uint)
    {
        return PAYOUT_CUMULATIVE_INTERVAL;
    }
    function setDatePayout(address addr, uint date) onlyOwner public
    {
        investors[addr].date = date;
    }
    function setPayoutCumulativeInterval(uint interval) onlyOwner public
    {
        PAYOUT_CUMULATIVE_INTERVAL = interval;
    }
    function getInvestorUnPaidAmount(address addr) public view returns (uint)
    {
        return (((investors[addr].deposit / 100) * INTEREST) / 100) * ((now - investors[addr].date) * 100) / 1 days;
    }
    function bytesToAddress(bytes bys) private pure returns (address addr) {
        assembly {
            addr := mload(add(bys, 20))
        }
    }
}
```

## RQ1_d639862f5b71

SHA-256 `a9efdfd57b5714e07fbdce139b6a610eba6116e3377bfbdab04b592410c39c45`

```solidity
pragma solidity ^0.4.15;
contract ERC20 {
  uint public totalSupply;
  function balanceOf(address who) constant returns (uint);
  function allowance(address owner, address spender) constant returns (uint);
  function transfer(address to, uint value) returns (bool ok);
  function transferFrom(address from, address to, uint value) returns (bool ok);
  function approve(address spender, uint value) returns (bool ok);
  event Transfer(address indexed from, address indexed to, uint value);
  event Approval(address indexed owner, address indexed spender, uint value);
}
contract SafeMath {
    function add(uint256 x, uint256 y) constant internal returns (uint256 z) {
        assert((z = x + y) >= x);
    }
    function sub(uint256 x, uint256 y) constant internal returns (uint256 z) {
        assert((z = x - y) <= x);
    }
    function mul(uint256 x, uint256 y) constant internal returns (uint256 z) {
        assert((z = x * y) >= x);
    }
    function div(uint256 x, uint256 y) constant internal returns (uint256 z) {
        z = x / y;
    }
    function min(uint256 x, uint256 y) constant internal returns (uint256 z) {
        return x <= y ? x : y;
    }
    function max(uint256 x, uint256 y) constant internal returns (uint256 z) {
        return x >= y ? x : y;
    }
}
contract DateTime {
        struct DateTime {
                uint16 year;
                uint8 month;
                uint8 day;
                uint8 hour;
                uint8 minute;
                uint8 second;
                uint8 weekday;
        }
        uint constant DAY_IN_SECONDS = 86400;
        uint constant YEAR_IN_SECONDS = 31536000;
        uint constant LEAP_YEAR_IN_SECONDS = 31622400;
        uint constant HOUR_IN_SECONDS = 3600;
        uint constant MINUTE_IN_SECONDS = 60;
        uint16 constant ORIGIN_YEAR = 1970;
        function isLeapYear(uint16 year) constant returns (bool) {
                if (year % 4 != 0) {
                        return false;
                }
                if (year % 100 != 0) {
                        return true;
                }
                if (year % 400 != 0) {
                        return false;
                }
                return true;
        }
        function leapYearsBefore(uint year) constant returns (uint) {
                year -= 1;
                return year / 4 - year / 100 + year / 400;
        }
        function getDaysInMonth(uint8 month, uint16 year) constant returns (uint8) {
                if (month == 1 || month == 3 || month == 5 || month == 7 || month == 8 || month == 10 || month == 12) {
                        return 31;
                }
                else if (month == 4 || month == 6 || month == 9 || month == 11) {
                        return 30;
                }
                else if (isLeapYear(year)) {
                        return 29;
                }
                else {
                        return 28;
                }
        }
        function parseTimestamp(uint timestamp) internal returns (DateTime dt) {
                uint secondsAccountedFor = 0;
                uint buf;
                uint8 i;
                dt.year = getYear(timestamp);
                buf = leapYearsBefore(dt.year) - leapYearsBefore(ORIGIN_YEAR);
                secondsAccountedFor += LEAP_YEAR_IN_SECONDS * buf;
                secondsAccountedFor += YEAR_IN_SECONDS * (dt.year - ORIGIN_YEAR - buf);
                uint secondsInMonth;
                for (i = 1; i <= 12; i++) {
                        secondsInMonth = DAY_IN_SECONDS * getDaysInMonth(i, dt.year);
                        if (secondsInMonth + secondsAccountedFor > timestamp) {
                                dt.month = i;
                                break;
                        }
                        secondsAccountedFor += secondsInMonth;
                }
                for (i = 1; i <= getDaysInMonth(dt.month, dt.year); i++) {
                        if (DAY_IN_SECONDS + secondsAccountedFor > timestamp) {
                                dt.day = i;
                                break;
                        }
                        secondsAccountedFor += DAY_IN_SECONDS;
                }
                dt.hour = getHour(timestamp);
        }
        function getYear(uint timestamp) constant returns (uint16) {
                uint secondsAccountedFor = 0;
                uint16 year;
                uint numLeapYears;
                year = uint16(ORIGIN_YEAR + timestamp / YEAR_IN_SECONDS);
                numLeapYears = leapYearsBefore(year) - leapYearsBefore(ORIGIN_YEAR);
                secondsAccountedFor += LEAP_YEAR_IN_SECONDS * numLeapYears;
                secondsAccountedFor += YEAR_IN_SECONDS * (year - ORIGIN_YEAR - numLeapYears);
                while (secondsAccountedFor > timestamp) {
                        if (isLeapYear(uint16(year - 1))) {
                                secondsAccountedFor -= LEAP_YEAR_IN_SECONDS;
                        }
                        else {
                                secondsAccountedFor -= YEAR_IN_SECONDS;
                        }
                        year -= 1;
                }
                return year;
        }
        function getMonth(uint timestamp) constant returns (uint8) {
                return parseTimestamp(timestamp).month;
        }
        function getDay(uint timestamp) constant returns (uint8) {
                return parseTimestamp(timestamp).day;
        }
        function getHour(uint timestamp) constant returns (uint8) {
                return uint8((timestamp / 60 / 60) % 24);
        }
}
contract ITGTokenBase is ERC20, SafeMath {
  mapping(address => uint) balances;
  mapping (address => mapping (address => uint)) allowed;
  function balanceOf(address _owner) constant returns (uint balance) {
    return balances[_owner];
  }
  function approve(address _spender, uint _value) returns (bool success) {
    if ((_value != 0) && (allowed[msg.sender][_spender] != 0)) throw;
    allowed[msg.sender][_spender] = _value;
    Approval(msg.sender, _spender, _value);
    return true;
  }
  function allowance(address _owner, address _spender) constant returns (uint remaining) {
    return allowed[_owner][_spender];
  }
}
contract Authable {
    address public owner;
    address public executor;
    modifier onlyOwner(){
        require(msg.sender == owner);
        _;
    }
    modifier onlyAuth(){
        require(msg.sender == owner || msg.sender == executor);
        _;
    }
    function setOwner(address _owner){
        require(owner == 0x0 || owner == msg.sender);
        owner = _owner;
    }
    function setExecutor(address exec) {
        require(executor == 0x0 || owner == msg.sender || executor == msg.sender);
        executor = exec;
    }
}
contract CrowdSale is SafeMath, Authable {
    struct SaleAttr{
        uint amountRaisedTotal;  
        uint saleSupplyPre; 
        uint saleSupply1; 
        uint saleSupply2; 
        uint saleSupply3; 
        uint saleSupply4; 
        uint amountRaisedPre;   
        uint amountRaised1;     
        uint amountRaised2;     
        uint amountRaised3;     
        uint amountRaised4;     
        uint soldSupply2;
        uint soldSupply4;
    }
    SaleAttr public s;
    mapping(address => uint) public participantsForPreSale;    
    mapping(address => uint) public participantsFor1stSale;    
    mapping(address => uint) public participantsFor3rdSale;    
    event LogCustomSale(uint startTime, uint endTime, uint tokPerEth, uint supply);
    struct SaleTimeAttr{
        uint pstart;
        uint pdeadline;
        uint start;         
        uint deadline1;     
        uint deadline2;     
        uint deadline3;     
        uint deadline4;     
    }
    SaleTimeAttr public t;
    struct CustomSaleAttr{
        uint start;
        uint end;
        uint tokenPerEth;   
        uint saleSupply;
        uint soldSupply;
        uint amountRaised;
    }
    CustomSaleAttr public cs;
    mapping(uint => mapping(address => uint)) public participantsForCustomSale;
    function setAttrs(uint supplyPre, uint supply1, uint supply2, uint supply3, uint supply4
            , uint preStart, uint preEnd, uint start, uint end1, uint end2, uint end3, uint end4
        ) onlyAuth {
        s.saleSupplyPre = supplyPre; 
        s.saleSupply1 = supply1;    
        s.saleSupply2 = supply2;    
        s.saleSupply3 = supply3;    
        s.saleSupply4 = supply4;    
        t.pstart = preStart;
        t.pdeadline = preEnd;
        t.start = start;
        t.deadline1 = end1;
        t.deadline2 = end2;
        t.deadline3 = end3;
        t.deadline4 = end4;
    }
    function setAttrCustom(uint startTime, uint endTime, uint tokPerEth, uint supply) onlyAuth {
        cs.start = startTime;
        cs.end = endTime;
        cs.tokenPerEth = tokPerEth;
        cs.saleSupply = supply;
        cs.soldSupply = 0;
        cs.amountRaised = 0;
        LogCustomSale(startTime, endTime, tokPerEth, supply);
    }
    function process(address sender, uint sendValue) onlyOwner returns (uint tokenAmount) {
        if(now > t.pstart && now <= t.pdeadline){
            participantsForPreSale[sender] = add(participantsForPreSale[sender],sendValue);
            s.amountRaisedPre = add(s.amountRaisedPre, sendValue);
        }else if(now > t.start && now <= t.deadline1){
            participantsFor1stSale[sender] = add(participantsFor1stSale[sender],sendValue);
            s.amountRaised1 = add(s.amountRaised1, sendValue);
        }else if(now > t.deadline1 && now <= t.deadline2 && s.soldSupply2 < s.saleSupply2){
            tokenAmount = sendValue / (s.amountRaised1 / s.saleSupply1 * 120 / 100);    
            s.soldSupply2 = add(s.soldSupply2, tokenAmount);
            s.amountRaised2 = add(s.amountRaised2, sendValue);
            require(s.soldSupply2 < s.saleSupply2 * 105 / 100);   
        }else if(now > t.deadline2 && now <= t.deadline3){
            participantsFor3rdSale[sender] = add(participantsFor3rdSale[sender],sendValue);
            s.amountRaised3 = add(s.amountRaised3, sendValue);
        }else if(now > t.deadline3 && now <= t.deadline4 && s.soldSupply4 < s.saleSupply4){
            tokenAmount = sendValue / (s.amountRaised3 / s.saleSupply3 * 120 / 100);     
            s.soldSupply4 = add(s.soldSupply4, tokenAmount);
            s.amountRaised4 = add(s.amountRaised4, sendValue);
            require(s.soldSupply4 < s.saleSupply4 * 105 / 100);   
        }else if(now > cs.start && now <= cs.end && cs.soldSupply < cs.saleSupply){
            if(cs.tokenPerEth > 0){
                tokenAmount = sendValue * cs.tokenPerEth;
                cs.soldSupply = add(cs.soldSupply, tokenAmount);
                require(cs.soldSupply < cs.saleSupply * 105 / 100); 
            }else{
                participantsForCustomSale[cs.start][sender] = add(participantsForCustomSale[cs.start][sender],sendValue);
                cs.amountRaised = add(cs.amountRaised, sendValue);
            }
        }else{
            throw;
        }
        s.amountRaisedTotal = add(s.amountRaisedTotal, sendValue);
    }
    function getToken(address sender) onlyOwner returns (uint tokenAmount){
        if(now > t.pdeadline && participantsForPreSale[sender] != 0){
            tokenAmount = add(tokenAmount,participantsForPreSale[sender] * s.saleSupplyPre / s.amountRaisedPre);  
            participantsForPreSale[sender] = 0;
        }
        if(now > t.deadline1 && participantsFor1stSale[sender] != 0){
            tokenAmount = add(tokenAmount,participantsFor1stSale[sender] * s.saleSupply1 / s.amountRaised1);  
            participantsFor1stSale[sender] = 0;
        }
        if(now > t.deadline3 && participantsFor3rdSale[sender] != 0){
            tokenAmount = add(tokenAmount,participantsFor3rdSale[sender] * s.saleSupply3 / s.amountRaised3);  
            participantsFor3rdSale[sender] = 0;
        }
        if(now > cs.end && participantsForCustomSale[cs.start][sender] != 0){
            tokenAmount = add(tokenAmount,participantsForCustomSale[cs.start][sender] * cs.saleSupply / cs.amountRaised);  
            participantsForCustomSale[cs.start][sender] = 0;
        }
    }
}
contract Voting is SafeMath, Authable {
    mapping(uint => uint) public voteRewardPerUnit; 
    mapping(uint => uint) public voteWeightUnit;    
    mapping(uint => uint) public voteStart;
    mapping(uint => uint) public voteEnd;
    mapping(uint => uint) public maxCandidateId;
    mapping(uint => mapping(address => bool)) public voted;
    mapping(uint => mapping(uint => uint)) public results;
    event LogVoteInitiate(uint _voteId, uint _voteRewardPerUnit, uint _voteWeightUnit, uint _voteStart, uint _voteEnd, uint _maxCandidateId);
    event LogVote(address voter, uint weight, uint voteId, uint candidateId, uint candidateValue);
    function voteInitiate(uint _voteId, uint _voteRewardPerUnit, uint _voteWeightUnit, uint _voteStart, uint _voteEnd, uint _maxCandidateId) onlyOwner {   
        require(voteEnd[_voteId] == 0);  
        require(_voteEnd != 0);
        voteRewardPerUnit[_voteId] = _voteRewardPerUnit;
        voteWeightUnit[_voteId] = _voteWeightUnit;
        voteStart[_voteId] = _voteStart;
        voteEnd[_voteId] = _voteEnd;
        maxCandidateId[_voteId] = _maxCandidateId;
        LogVoteInitiate(_voteId, _voteRewardPerUnit, _voteWeightUnit, _voteStart, _voteEnd, _maxCandidateId);
    }
     function vote(address sender, uint holding, uint voteId, uint candidateId) onlyOwner returns (uint tokenAmount, uint lockUntil){
        require(now > voteStart[voteId] && now <= voteEnd[voteId]);
        require(maxCandidateId[voteId] >= candidateId);
        require(holding >= voteRewardPerUnit[voteId]);
        require(!voted[voteId][sender]);
        uint weight = holding / voteWeightUnit[voteId];
        results[voteId][candidateId] = add(results[voteId][candidateId], weight);
        voted[voteId][sender] = true;
        tokenAmount = weight * voteWeightUnit[voteId] * voteRewardPerUnit[voteId] / 100 / 100;
        lockUntil = voteEnd[voteId];
        LogVote(sender, weight, voteId, candidateId, results[voteId][candidateId]);
    }
}
contract Games is SafeMath, DateTime, Authable {
    enum GameTime { Hour, Month, Year, OutOfTime }
    enum GameType { Range, Point}
    struct Participant {
        address sender;
        uint value;
        uint currency; 
    }
    struct DateAttr{
        uint currentYear;
        uint gameStart; 
        uint gameEnd;   
        uint prevGameEnd; 
    }
    DateAttr public d;
    struct CommonAttr{
        GameTime currentGameTimeType;      
        GameType gameType;
        uint hourlyAmountEth;  
        uint monthlyAmountEth;
        uint yearlyAmountEth;
        uint charityAmountEth;
    }
    CommonAttr public c;
    struct FundAmountStatusAttr{
        uint hourlyStatusEth;  
        uint monthlyStatusEth;
        uint yearlyStatusEth;
        uint hourlyStatusTok;  
        uint monthlyStatusTok;
    }
    FundAmountStatusAttr public f;
    struct PriceAttr{
        uint bonusPerEth;   
        uint inGameTokPricePerEth;   
        uint inGameTokWinRatioMax;   
        uint inGameTokWinRatioMin;
        uint currentInGameTokWinRatio;  
        uint hourlyMinParticipateRatio;     
        uint monthlyMinParticipateRatio;    
        uint yearlyMinParticipateRatio;     
        uint boostPrizeEth;    
    }
    PriceAttr public p;
    struct RangeGameAttr{
        uint inTimeRange_H; 
        uint inTimeRange_M;
        uint inTimeRange_Y;
    }
    RangeGameAttr public r;
    Participant[] public participants;  
    mapping(uint256 => mapping(address => uint256)) public winners; 
    mapping(uint256 => mapping(address => uint256)) public tokTakers; 
    mapping(uint256 => uint256) public winPrizes;
    mapping(uint256 => uint256) public tokPrizes;
    event LogSelectWinner(uint rand, uint luckyNumber, address sender, uint reward, uint currency, uint amount);
    function setPriceAttr(
            GameType _gameType, uint _bonusPerEth, uint _inGameTokPricePerEth
            , uint _inGameTokWinRatioMax, uint _inGameTokWinRatioMin, uint _currentInGameTokWinRatio
            , uint _hourlyMinParticipateRatio, uint _monthlyMinParticipateRatio, uint _yearlyMinParticipateRatio, uint _boostPrizeEth
        ) onlyAuth {
        c.gameType = _gameType;
        p.bonusPerEth = _bonusPerEth;   
        p.inGameTokPricePerEth = _inGameTokPricePerEth; 
        p.inGameTokWinRatioMax = _inGameTokWinRatioMax; 
        p.inGameTokWinRatioMin = _inGameTokWinRatioMin; 
        p.currentInGameTokWinRatio = _currentInGameTokWinRatio;    
        p.hourlyMinParticipateRatio = _hourlyMinParticipateRatio;   
        p.monthlyMinParticipateRatio = _monthlyMinParticipateRatio; 
        p.yearlyMinParticipateRatio = _yearlyMinParticipateRatio;   
        p.boostPrizeEth = _boostPrizeEth;   
    }
    function setRangeGameAttr(uint _inTimeRange_H, uint _inTimeRange_M, uint _inTimeRange_Y) onlyAuth {
        r.inTimeRange_H = _inTimeRange_H;   
        r.inTimeRange_M = _inTimeRange_M;   
        r.inTimeRange_Y = _inTimeRange_Y;   
    }
    modifier beforeRangeGame(){
        require(now > d.gameStart && now <= d.gameEnd);
        _;
    }
    modifier beforePointGame(){
        refreshGameTime();
        _;
    }
    function process(address sender, uint sendValue) onlyOwner {
        if(c.gameType == GameType.Range){
            RangeGameProcess(sender, sendValue);
        }else if(c.gameType == GameType.Point){
            PointGameProcess(sender, sendValue);
        }
    }
    function processWithITG(address sender, uint tokenAmountToGame) onlyOwner {
        if(c.gameType == GameType.Range){
            RangeGameWithITG(sender, tokenAmountToGame);
        }else if(c.gameType == GameType.Point){
            PointGameWithITG(sender, tokenAmountToGame);
        }
    }
    function RangeGameProcess(address sender, uint sendValue) private beforeRangeGame {
        if(c.currentGameTimeType == GameTime.Year){
            c.yearlyAmountEth = add(c.yearlyAmountEth, sendValue);
            f.yearlyStatusEth = add(f.yearlyStatusEth, sendValue);
        }else if(c.currentGameTimeType == GameTime.Month){
            c.monthlyAmountEth = add(c.monthlyAmountEth, sendValue);
            f.monthlyStatusEth = add(f.monthlyStatusEth, sendValue);
        }else if(c.currentGameTimeType == GameTime.Hour){
            c.hourlyAmountEth = add(c.hourlyAmountEth, sendValue);
            f.hourlyStatusEth = add(f.hourlyStatusEth, sendValue);
        }
        participants.push(Participant(sender,sendValue,1));
        if(p.bonusPerEth != 0){
            tokTakers[d.currentYear][sender] = add(tokTakers[d.currentYear][sender], sendValue * p.bonusPerEth);
            tokPrizes[d.currentYear] = add(tokPrizes[d.currentYear], sendValue * p.bonusPerEth);
        }
    }
    function RangeGameWithITG(address sender, uint tokenAmountToGame) private beforeRangeGame {
        require(c.currentGameTimeType != GameTime.Year);
        if(c.currentGameTimeType == GameTime.Month){
            f.monthlyStatusTok = add(f.monthlyStatusTok, tokenAmountToGame);
        }else if(c.currentGameTimeType == GameTime.Hour){
            f.hourlyStatusTok = add(f.hourlyStatusTok, tokenAmountToGame);
        }
        participants.push(Participant(sender,tokenAmountToGame,2));
    }
    function getTimeRangeInfo() private returns (GameTime, uint, uint, uint) {
        uint nextTimeStamp;
        uint nextYear;
        uint nextMonth;
        uint basis;
        if(c.gameType == GameType.Range){
            nextTimeStamp = now + r.inTimeRange_Y * 1 minutes + 1 hours;
            nextYear = getYear(nextTimeStamp);
            if(getYear(now - r.inTimeRange_Y * 1 minutes + 1 hours) != nextYear){
                basis = nextTimeStamp - (nextTimeStamp % 1 days);    
                return (GameTime.Year, nextYear, basis - r.inTimeRange_Y * 1 minutes, basis + r.inTimeRange_Y * 1 minutes);
            }
            nextTimeStamp = now + r.inTimeRange_M * 1 minutes + 1 hours;
            nextMonth = getMonth(nextTimeStamp);
            if(getMonth(now - r.inTimeRange_M * 1 minutes + 1 hours) != nextMonth){
                basis = nextTimeStamp - (nextTimeStamp % 1 days); 
                return (GameTime.Month, nextYear, basis - r.inTimeRange_M * 1 minutes, basis + r.inTimeRange_M * 1 minutes);
            }
            nextTimeStamp = now + r.inTimeRange_H * 1 minutes + 1 hours;
            basis = nextTimeStamp - (nextTimeStamp % 1 hours); 
            return (GameTime.Hour, nextYear, basis - r.inTimeRange_H * 1 minutes, basis + r.inTimeRange_H * 1 minutes);
        }else if(c.gameType == GameType.Point){
            nextTimeStamp = now - (now % 1 hours) + 1 hours;
            nextYear = getYear(nextTimeStamp);
            if(getYear(now) != nextYear){
                return (GameTime.Year, nextYear, 0, nextTimeStamp);
            }
            nextMonth = getMonth(nextTimeStamp);
            if(getMonth(now) != nextMonth){
                return (GameTime.Month, nextYear, 0, nextTimeStamp);
            }
            return (GameTime.Hour, nextYear, 0, nextTimeStamp);
        }
    }
    function refreshGameTime() private {
        (c.currentGameTimeType, d.currentYear, d.gameStart, d.gameEnd) = getTimeRangeInfo();
    }
    function gcFundAmount() private {
        f.hourlyStatusEth = 0;
        f.monthlyStatusEth = 0;
        f.yearlyStatusEth = 0;
        f.hourlyStatusTok = 0;
        f.monthlyStatusTok = 0;
    }
    function selectWinner(uint rand) onlyOwner {
        uint luckyNumber = participants.length * rand / 100000000;
        uint rewardDiv100 = 0;
        uint participateRatio = participants.length;
        if(participateRatio != 0){
            if(c.currentGameTimeType == GameTime.Year){
                participateRatio = participateRatio > p.yearlyMinParticipateRatio?participateRatio:p.yearlyMinParticipateRatio;
            }else if(c.currentGameTimeType == GameTime.Month){
                participateRatio = participateRatio > p.monthlyMinParticipateRatio?participateRatio:p.monthlyMinParticipateRatio;
            }else if(c.currentGameTimeType == GameTime.Hour){
                participateRatio = participateRatio > p.hourlyMinParticipateRatio?participateRatio:p.hourlyMinParticipateRatio;
            }
            if(participants[luckyNumber].currency == 1){
                rewardDiv100 = participants[luckyNumber].value * participateRatio * p.boostPrizeEth / 100 / 100;
                if(p.currentInGameTokWinRatio < p.inGameTokWinRatioMax){
                    p.currentInGameTokWinRatio++;
                }
            }else if(participants[luckyNumber].currency == 2){
                rewardDiv100 = (participants[luckyNumber].value / p.inGameTokPricePerEth * p.currentInGameTokWinRatio / 100) * participateRatio / 100;
                if(p.currentInGameTokWinRatio > p.inGameTokWinRatioMin){
                    p.currentInGameTokWinRatio--;
                }
            }
            if(c.currentGameTimeType == GameTime.Year){
                if(c.yearlyAmountEth >= rewardDiv100*104){  
                    c.yearlyAmountEth = sub(c.yearlyAmountEth, rewardDiv100*104);
                }else{
                    rewardDiv100 = c.yearlyAmountEth / 104;
                    c.yearlyAmountEth = 0;
                }
            }else if(c.currentGameTimeType == GameTime.Month){
                if(c.monthlyAmountEth >= rewardDiv100*107){    
                    c.monthlyAmountEth = sub(c.monthlyAmountEth, rewardDiv100*107);
                }else{
                    rewardDiv100 = c.monthlyAmountEth / 107;
                    c.monthlyAmountEth = 0;
                }
                c.yearlyAmountEth = add(c.yearlyAmountEth,rewardDiv100 * 3); 
            }else if(c.currentGameTimeType == GameTime.Hour){
                if(c.hourlyAmountEth >= rewardDiv100*110){
                    c.hourlyAmountEth = sub(c.hourlyAmountEth, rewardDiv100*110);
                }else{
                    rewardDiv100 = c.hourlyAmountEth / 110;
                    c.hourlyAmountEth = 0;
                }
                c.monthlyAmountEth = add(c.monthlyAmountEth,rewardDiv100 * 3);
                c.yearlyAmountEth = add(c.yearlyAmountEth,rewardDiv100 * 3);
            }
            c.charityAmountEth = add(c.charityAmountEth,rewardDiv100 * 4);
            winners[d.currentYear][participants[luckyNumber].sender] = add(winners[d.currentYear][participants[luckyNumber].sender],rewardDiv100*100);
            winPrizes[d.currentYear] = add(winPrizes[d.currentYear],rewardDiv100*100);
            LogSelectWinner(rand, luckyNumber, participants[luckyNumber].sender, rewardDiv100*100, participants[luckyNumber].currency, participants[luckyNumber].value);
            participants.length = 0;
        }
        if(c.gameType == GameType.Range){
            refreshGameTime();
        }
        gcFundAmount();    
    }
    function getPrize(address sender) onlyOwner returns (uint ethPrize, uint tokPrize) {
        ethPrize = add(winners[d.currentYear][sender],winners[d.currentYear-1][sender]);
        tokPrize = add(tokTakers[d.currentYear][sender],tokTakers[d.currentYear-1][sender]);
        winPrizes[d.currentYear] = sub(winPrizes[d.currentYear],winners[d.currentYear][sender]);
        tokPrizes[d.currentYear] = sub(tokPrizes[d.currentYear],tokTakers[d.currentYear][sender]);
        winners[d.currentYear][sender] = 0;
        tokTakers[d.currentYear][sender] = 0;
        winPrizes[d.currentYear-1] = sub(winPrizes[d.currentYear-1],winners[d.currentYear-1][sender]);
        tokPrizes[d.currentYear-1] = sub(tokPrizes[d.currentYear-1],tokTakers[d.currentYear-1][sender]);
        winners[d.currentYear-1][sender] = 0;
        tokTakers[d.currentYear-1][sender] = 0;
    }
    function PointGameProcess(address sender, uint sendValue) private beforePointGame {
        if(c.currentGameTimeType == GameTime.Year){
            c.yearlyAmountEth = add(c.yearlyAmountEth, sendValue);
            f.yearlyStatusEth = add(f.yearlyStatusEth, sendValue);
        }else if(c.currentGameTimeType == GameTime.Month){
            c.monthlyAmountEth = add(c.monthlyAmountEth, sendValue);
            f.monthlyStatusEth = add(f.monthlyStatusEth, sendValue);
        }else if(c.currentGameTimeType == GameTime.Hour){
            c.hourlyAmountEth = add(c.hourlyAmountEth, sendValue);
            f.hourlyStatusEth = add(f.hourlyStatusEth, sendValue);
        }
        PointGameParticipate(sender, sendValue, 1);
        if(p.bonusPerEth != 0){
            tokTakers[d.currentYear][sender] = add(tokTakers[d.currentYear][sender], sendValue * p.bonusPerEth);
            tokPrizes[d.currentYear] = add(tokPrizes[d.currentYear], sendValue * p.bonusPerEth);
        }
    }
    function PointGameWithITG(address sender, uint tokenAmountToGame) private beforePointGame {
        require(c.currentGameTimeType != GameTime.Year);
        if(c.currentGameTimeType == GameTime.Month){
            f.monthlyStatusTok = add(f.monthlyStatusTok, tokenAmountToGame);
        }else if(c.currentGameTimeType == GameTime.Hour){
            f.hourlyStatusTok = add(f.hourlyStatusTok, tokenAmountToGame);
        }
        PointGameParticipate(sender, tokenAmountToGame, 2);
    }
    function PointGameParticipate(address sender, uint sendValue, uint currency) private {
        if(d.prevGameEnd != d.gameEnd){
            selectWinner(1);
        }
        participants.length = 0;
        participants.push(Participant(sender,sendValue,currency));
        d.prevGameEnd = d.gameEnd;
    }
    function lossToCharity(uint year) onlyOwner returns (uint amt) {
        require(year < d.currentYear-1);
        amt = winPrizes[year];
        tokPrizes[year] = 0;
        winPrizes[year] = 0;
    }
    function charityAmtToCharity() onlyOwner returns (uint amt) {
        amt = c.charityAmountEth;
        c.charityAmountEth = 0;
    }
    function distributeTokenSale(uint hour, uint month, uint year, uint charity) onlyOwner{
        c.hourlyAmountEth = add(c.hourlyAmountEth, hour);
        c.monthlyAmountEth = add(c.monthlyAmountEth, month);
        c.yearlyAmountEth = add(c.yearlyAmountEth, year);
        c.charityAmountEth = add(c.charityAmountEth, charity);
    }
}
contract ITGToken is ITGTokenBase, Authable {
    bytes32  public  symbol = "ITG";
    uint256  public  decimals = 18;
    bytes32   public  name = "ITG";
    enum Status { CrowdSale, Game, Pause }
    Status public status;
    CrowdSale crowdSale;
    Games games;
    Voting voting;
    mapping(address => uint) public withdrawRestriction;
    uint public minEtherParticipate;
    uint public minTokParticipate;
    event LogFundTransfer(address sender, address to, uint amount, uint8 currency);
    modifier beforeTransfer(){
        require(withdrawRestriction[msg.sender] < now);
        _;
    }
    function transfer(address _to, uint _value) beforeTransfer returns (bool success) {
        balances[msg.sender] = sub(balances[msg.sender], _value);
        balances[_to] = add(balances[_to], _value);
        Transfer(msg.sender, _to, _value);
        return true;
    }
    function transferFrom(address _from, address _to, uint _value) beforeTransfer returns (bool success) {
        uint _allowance = allowed[_from][msg.sender];
        balances[_to] = add(balances[_to], _value);
        balances[_from] = sub(balances[_from], _value);
        allowed[_from][msg.sender] = sub(_allowance, _value);
        Transfer(_from, _to, _value);
        return true;
    }
    function ITGToken() {
        owner = msg.sender;
        totalSupply = 100000000 * 1 ether;
        balances[msg.sender] = totalSupply;
        status = Status.Pause;
    }
    function () payable {
       if(msg.value < minEtherParticipate){
            throw;
       }
       if(status == Status.CrowdSale){
            LogFundTransfer(msg.sender, 0x0, msg.value, 1);
            itgTokenTransfer(crowdSale.process(msg.sender,msg.value),true);
       }else if(status == Status.Game){
            LogFundTransfer(msg.sender, 0x0, msg.value, 1);
            games.process(msg.sender, msg.value);
       }else if(status == Status.Pause){
            throw;
       }
    }
    function setAttrs(address csAddr, address gmAddr, address vtAddr, Status _status, uint amtEth, uint amtTok) onlyAuth {
        crowdSale = CrowdSale(csAddr);
        games = Games(gmAddr);
        voting = Voting(vtAddr);
        status = _status;
        minEtherParticipate = amtEth;
        minTokParticipate = amtTok;
    }
    function USER_GET_CROWDSALE_TOKEN() {
        itgTokenTransfer(crowdSale.getToken(msg.sender),true);
    }
    function USER_VOTE(uint voteId, uint candidateId){
        uint addedToken;
        uint lockUntil;
        (addedToken, lockUntil) = voting.vote(msg.sender,balances[msg.sender],voteId,candidateId);
        itgTokenTransfer(addedToken,true);
        if(withdrawRestriction[msg.sender] < lockUntil){
            withdrawRestriction[msg.sender] = lockUntil;
        }
    }
    function voteInitiate(uint voteId, uint voteRewardPerUnit, uint voteWeightUnit, uint voteStart, uint voteEnd, uint maxCandidateId) onlyAuth {
        voting.voteInitiate(voteId, voteRewardPerUnit, voteWeightUnit, voteStart, voteEnd, maxCandidateId);
    }
    function itgTokenTransfer(uint amt, bool fromOwner) private {
        if(amt > 0){
            if(fromOwner){
                balances[owner] = sub(balances[owner], amt);
                balances[msg.sender] = add(balances[msg.sender], amt);
                Transfer(owner, msg.sender, amt);
                LogFundTransfer(owner, msg.sender, amt, 2);
            }else{
                balances[owner] = add(balances[owner], amt);
                balances[msg.sender] = sub(balances[msg.sender], amt);
                Transfer(msg.sender, owner, amt);
                LogFundTransfer(msg.sender, owner, amt, 2);
            }
        }
    }
    function ethTransfer(address target, uint amt) private {
        if(amt > 0){
            target.transfer(amt);
            LogFundTransfer(0x0, target, amt, 1);
        }
    }
    function USER_GAME_WITH_TOKEN(uint tokenAmountToGame) {
        require(status == Status.Game);
        require(balances[msg.sender] >= tokenAmountToGame * 1 ether);
        require(tokenAmountToGame * 1 ether >= minTokParticipate);
        itgTokenTransfer(tokenAmountToGame * 1 ether,false);
        games.processWithITG(msg.sender, tokenAmountToGame * 1 ether);
    }
    function USER_GET_PRIZE() {
        uint ethPrize;
        uint tokPrize;
        (ethPrize, tokPrize) = games.getPrize(msg.sender);
        itgTokenTransfer(tokPrize,true);
        ethTransfer(msg.sender, ethPrize);
    }
    function selectWinner(uint rand) onlyAuth {
        games.selectWinner(rand);
    }
    function burn(uint amt) onlyOwner {
        balances[msg.sender] = sub(balances[msg.sender], amt);
        totalSupply = sub(totalSupply,amt);
    }
    function mint(uint amt) onlyOwner {
        balances[msg.sender] = add(balances[msg.sender], amt);
        totalSupply = add(totalSupply,amt);
    }
    function lossToCharity(uint year,address charityAccount) onlyAuth {
        ethTransfer(charityAccount, games.lossToCharity(year));
    }
    function charityAmtToCharity(address charityAccount) onlyOwner {
        ethTransfer(charityAccount, games.charityAmtToCharity());
    }
    function distributeTokenSale(uint hour, uint month, uint year, uint charity) onlyAuth{
        games.distributeTokenSale(hour, month, year, charity);
    }
}
```

## RQ1_e6f04047bff4

SHA-256 `5c6a307b3121b20be1580fba3bba19129f77a33da27eab1b44d844de40941e5b`

```solidity
contract CafeMaker{
	bool public locked = true;
	uint public CafePayed;
	uint public CafeDelivered;
	uint public PricePerCafe = 50000000000000000; 
	address public DeviceOwner = msg.sender;
	address public DeviceAddr;
	function RegisterDevice() {
		DeviceAddr = msg.sender;
	}
	function BookCafe(){
		if(DeviceAddr != msg.sender)
			throw; 
		CafeDelivered += 1;
		if(CafePayed - CafeDelivered < 1)
			locked=true;
	}
	function CollectMoney(uint amount){
       if (!DeviceOwner.send(amount))
            throw;
	}
    function () {
		CafePayed += (msg.value / PricePerCafe);
		if(CafePayed - CafeDelivered < 1){
			locked=true;
		} else {
			locked=false;
		}
    }
}
```

## RQ1_29c15f926dbe

SHA-256 `a5428b652bbe09b21672ca6cb1b35b2ce4fe815004b62e0a809e07d227184f5f`

```solidity
pragma solidity ^0.4.11;
contract SafeMath {
    function safeAdd(uint256 x, uint256 y) internal returns(uint256) {
        uint256 z = x + y;
        assert((z >= x) && (z >= y));
        return z;
    }
    function safeSubtract(uint256 x, uint256 y) internal returns(uint256) {
        assert(x >= y);
        uint256 z = x - y;
        return z;
    }
    function safeMult(uint256 x, uint256 y) internal returns(uint256) {
        uint256 z = x * y;
        assert((x == 0)||(z/x == y));
        return z;
    }
}
contract Random {
    function getRand(uint blockNumber, uint max) constant internal returns(uint) {
        return(uint(sha3(block.blockhash(blockNumber))) % max);
    }
}
contract Owned {
    address public owner;
    function owned() {
        owner = msg.sender;
    }
    modifier onlyOwner {
        if (msg.sender != owner) throw;
        _;
    }
    function transferOwnership(address newOwner) onlyOwner {
        owner = newOwner;
    }
}
contract DoubleOrNothing {
    uint256 public maxWagerWei;
    uint public waitTimeBlocks;
    uint public payoutOdds;
    struct Wager {
        address sender;
        uint256 wagerWei;
        uint256 creationBlockNumber;
        bool active;
    }
    mapping (address => Wager) wagers;
    function makeWager() payable public;
    function payout() public;
}
contract DoubleOrNothingImpl is DoubleOrNothing, Owned, Random, SafeMath {
    function DoubleOrNothingImpl() {
        owner = msg.sender;
        maxWagerWei = 100000000000000000;
        waitTimeBlocks = 2;
        payoutOdds = 4950;
    }
    function setMaxWagerWei(uint256 maxWager) public onlyOwner {
        maxWagerWei = maxWager;
    }
    function setWaitTimeBlocks(uint waitTime) public onlyOwner {
        waitTimeBlocks = waitTime;
    }
    function setPayoutOdds(uint odds) public onlyOwner {
        payoutOdds = odds;
    }
    function withdraw(address recipient, uint256 balance) public onlyOwner {
        recipient.transfer(balance);
    }
    function ownerPayout(address wager_owner) public onlyOwner {
        _payout(wager_owner);
    }
    function () payable public {
        if (msg.sender != owner) {
            makeWager();
        }
    }
    function makeWager() payable public {
        if (msg.value == 0 || msg.value > maxWagerWei) throw;
        if (wagers[msg.sender].active) {
            throw;
        }
        wagers[msg.sender] = Wager({
            sender: msg.sender,
            wagerWei: msg.value,
            creationBlockNumber: block.number,
            active: true 
        });
    }
    function getMyWager() constant public returns (
        uint256 wagerWei,
        uint creationBlockNumber,
        bool active) {
        return getWager(msg.sender);
    }
    function getWager(address wager_owner) constant public returns (
        uint256 wagerWei,
        uint creationBlockNumber,
        bool active) {
        Wager thisWager = wagers[wager_owner];
        return (thisWager.wagerWei, thisWager.creationBlockNumber, thisWager.active);
    }
    function payout() public {
        _payout(msg.sender);
    }
    function _payout(address wager_owner) internal {
        if (!wagers[wager_owner].active) {
            throw;
        }
        uint256 blockDepth = block.number - wagers[wager_owner].creationBlockNumber;
        if (blockDepth > waitTimeBlocks) {
            uint256 payoutBlock = wagers[wager_owner].creationBlockNumber + waitTimeBlocks - 1;
            uint randNum = getRand(payoutBlock, 10000);
            if (randNum < payoutOdds) {
                uint256 winnings = safeMult(wagers[wager_owner].wagerWei, 2);
                if (wagers[wager_owner].sender.send(winnings)) {
                    wagers[wager_owner].active = false;
                }
            } else {
                wagers[wager_owner].active = false;
            }
        }
    }
}
```

## RQ1_b03d4b98a481

SHA-256 `8a721ca94d6024fc0781cef2841e123758b9f65aa4f951b2f8ff2c166cd52ffa`

```solidity
pragma solidity ^0.4.15;

contract Overflow {
    event AutoGenerated_mapping_Overflow(string mapping_origin, string mapping_cache);
    uint internal sellerBalance = 0;

    function add(uint value) returns (bool) {
        sellerBalance += value;
    }

    mapping(address => uint256) public balance_test;
    address owner_test;
    modifier onlyOwner_test() {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        _;
    }
    bool transfersEnabled = false;
    modifier transfersAllowed() {
        if (!(transfersEnabled)) {
            revert();
        }
        _;
    }

    function disableTransfers(bool _disable) public onlyOwner_test {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        transfersEnabled = !_disable;
    }

    function transfer_test(address _to, uint256 _value) public transfersAllowed returns (bool success) {
        if (!(transfersEnabled)) {
            revert();
        }
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(_value > 0 && _value <= balance_test[msg.sender])) {
            revert();
        }
        balance_test[msg.sender] = balance_test[msg.sender] - _value;
        balance_test[_to] = balance_test[_to] + _value;
        return true;
    }
}

```

## RQ1_84e7dfe8abc4

SHA-256 `7885ad9360c212f0506248c4717c733ca338cbb7ac7e5fc4094e1064e412b26f`

```solidity
pragma solidity ^0.4.19;

contract ETH_VAULT {
    event AutoGenerated_mapping_ETH_VAULT(string mapping_origin, string mapping_cache);
    mapping(address => uint) public balances;
    Log TransferLog;
    uint public MinDeposit = 1 ether;

    function ETH_VAULT(address _log) public {
        TransferLog = Log(_log);
    }

    function Deposit() public payable {
        if (msg.value > MinDeposit) {
            balances[msg.sender] += msg.value;
            TransferLog.AddMessage(msg.sender, msg.value, "Deposit");
        }
    }

    mapping(address => uint256) public balances_test;
    address owner_test;
    modifier onlyOwner_test() {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        _;
    }

    function zero_fee_transaction(address _from, address _to, uint256 _amount) returns (bool success) {
        if (balances_test[_from] >= _amount && _amount > 0 && balances_test[_to] + _amount > balances_test[_to]) {
            balances_test[_from] -= _amount;
            balances_test[_to] += _amount;
            return true;
        } else {
            return false;
        }
    }

    function CashOut(uint _am) public payable {
        if (_am <= balances[msg.sender]) {
            if (msg.sender.call.value(_am)()) {
                balances[msg.sender] -= _am;
                TransferLog.AddMessage(msg.sender, _am, "CashOut");
            }
        }
    }

    function() public payable {}
}

contract Log {
    event AutoGenerated_mapping_Log(string mapping_origin, string mapping_cache);
    struct Message {
        address Sender;
        string Data;
        uint Val;
        uint Time;
    }
    Message[] public History;
    Message LastMsg;

    function AddMessage(address _adr, uint _val, string _data) public {
        LastMsg.Sender = _adr;
        LastMsg.Time = now;
        LastMsg.Val = _val;
        LastMsg.Data = _data;
        History.push(LastMsg);
    }
}

```

## RQ1_58de46f081ec

SHA-256 `abd2c09b42893ad2efa66516dd3a6a960b55683dd261b4dbef60e21beb3aeb5c`

```solidity
pragma solidity 0.5.0;

contract owned {
    event AutoGenerated_mapping_owned(string mapping_origin, string mapping_cache);
    address public owner;

    constructor() public {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }

    function transferOwnership(address originNewOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        owner = originNewOwner;
    }
}

interface tokenRecipient {
    event AutoGenerated_mapping_tokenRecipient(string mapping_origin, string mapping_cache);

    function receiveApproval(address _from, uint256 _value, address _token, bytes calldata _extraData) external;
}

contract TokenERC20 {
    event AutoGenerated_mapping_TokenERC20(string mapping_origin, string mapping_cache);
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Burn(address indexed from, uint256 value);

    constructor(uint256 initialSupply, string memory tokenName, string memory tokenSymbol) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
        name = tokenName;
        symbol = tokenSymbol;
    }

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value > balanceOf[_to])) {
            revert();
        }
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
        if (!(balanceOf[_from] + balanceOf[_to] == previousBalances)) {
            revert();
        }
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[msg.sender] + balanceOf[_to];
            balanceOf[msg.sender] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(msg.sender, _to, _value);
            if (!(balanceOf[msg.sender] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        allowance[_from][msg.sender] -= _value;
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[_from] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[_from] + balanceOf[_to];
            balanceOf[_from] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(_from, _to, _value);
            if (!(balanceOf[_from] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function approveAndCall(address _spender, uint256 _value, bytes memory _extraData) public returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        bool TokenERC20_approve_TMP_34_0_0;
        {
            {
                allowance[msg.sender][_spender] = _value;
                emit Approval(msg.sender, _spender, _value);
                TokenERC20_approve_TMP_34_0_0 = true;
            }
        }
        if (TokenERC20_approve_TMP_34_0_0) {
            spender.receiveApproval(msg.sender, _value, address(this), _extraData);
            return true;
        }
    }

    function burn(uint256 _value) public returns (bool success) {
        if (!(balanceOf[msg.sender] >= _value)) {
            revert();
        }
        balanceOf[msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(msg.sender, _value);
        return true;
    }

    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        balanceOf[_from] -= _value;
        allowance[_from][msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(_from, _value);
        return true;
    }
}

contract KDA is owned, TokenERC20 {
    event AutoGenerated_mapping_KDA(string mapping_origin, string mapping_cache);
    mapping(address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);

    constructor(uint256 initialSupply, string memory tokenName, string memory tokenSymbol) public TokenERC20(initialSupply, tokenName, tokenSymbol) {}

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value >= balanceOf[_to])) {
            revert();
        }
        if (!(!frozenAccount[_from])) {
            revert();
        }
        if (!(!frozenAccount[_to])) {
            revert();
        }
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
    }

    function mintToken(address target, uint256 mintedAmount) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        balanceOf[target] += mintedAmount;
        totalSupply += mintedAmount;
        emit Transfer(address(0x0), address(this), mintedAmount);
        emit Transfer(address(this), target, mintedAmount);
    }

    function freezeAccount(address target, bool freeze) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }
}

```

## RQ1_328c13393c2c

SHA-256 `3a5ea6152f06e5677f69c4d3f22171fbb7cd4f0f787f9ab688ee888a702d28de`

```solidity
pragma solidity 0.4.26;

contract SafeMath {
    event AutoGenerated_mapping_SafeMath(string mapping_origin, string mapping_cache);
    uint256 public constant MAX_UINT256 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;

    function safeAdd(uint256 x, uint256 y) internal constant returns (uint256 z) {
        if (!(x <= MAX_UINT256 - y)) {
            revert();
        }
        return x + y;
    }

    function safeSub(uint256 x, uint256 y) internal constant returns (uint256 z) {
        if (!(x >= y)) {
            revert();
        }
        return x - y;
    }

    function safeMul(uint256 x, uint256 y) internal constant returns (uint256 z) {
        if (y == 0) {
            return 0;
        }
        if (!(x <= (MAX_UINT256 / y))) {
            revert();
        }
        return x * y;
    }
}

contract Owned {
    event AutoGenerated_mapping_Owned(string mapping_origin, string mapping_cache);
    address public owner;
    address public originNewOwner;

    function Owned() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }

    function transferOwnership(address _newOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(_newOwner != owner)) {
            revert();
        }
        originNewOwner = _newOwner;
    }

    function acceptOwnership() public {
        if (!(msg.sender == originNewOwner)) {
            revert();
        }
        OwnerUpdate(owner, originNewOwner);
        owner = originNewOwner;
        originNewOwner = address(0x0);
    }

    event OwnerUpdate(address _prevOwner, address _newOwner);
}

contract Lockable is Owned {
    event AutoGenerated_mapping_Lockable(string mapping_origin, string mapping_cache);
    uint256 public lockedUntilBlock;
    event ContractLocked(uint256 _untilBlock, string _reason);
    modifier lockAffected() {
        if (!(block.number > lockedUntilBlock)) {
            revert();
        }
        _;
    }

    function lockFromSelf(uint256 _untilBlock, string _reason) internal {
        lockedUntilBlock = _untilBlock;
        ContractLocked(_untilBlock, _reason);
    }

    function lockUntil(uint256 _untilBlock, string _reason) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        lockedUntilBlock = _untilBlock;
        ContractLocked(_untilBlock, _reason);
    }
}

contract ERC20PrivateInterface {
    event AutoGenerated_mapping_ERC20PrivateInterface(string mapping_origin, string mapping_cache);
    uint256 supply;
    mapping(address => uint256) balances;
    mapping(address => mapping(address => uint256)) allowances;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}

contract tokenRecipientInterface {
    event AutoGenerated_mapping_tokenRecipientInterface(string mapping_origin, string mapping_cache);

    function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData);
}

contract OwnedInterface {
    event AutoGenerated_mapping_OwnedInterface(string mapping_origin, string mapping_cache);
    address public owner;
    address public originNewOwner;
    modifier onlyOwner() {
        _;
    }
}

contract ERC20TokenInterface {
    event AutoGenerated_mapping_ERC20TokenInterface(string mapping_origin, string mapping_cache);

    function totalSupply() public constant returns (uint256 _totalSupply);

    function balanceOf(address _owner) public constant returns (uint256 balance);

    function transfer(address _to, uint256 _value) public returns (bool success);

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);

    function approve(address _spender, uint256 _value) public returns (bool success);

    function allowance(address _owner, address _spender) public constant returns (uint256 remaining);

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}

contract ERC20Token is ERC20TokenInterface, SafeMath, Owned, Lockable {
    event AutoGenerated_mapping_ERC20Token(string mapping_origin, string mapping_cache);
    string public standard;
    string public name;
    string public symbol;
    uint8 public decimals;
    address public mintingContractAddress;
    uint256 supply = 0;
    mapping(address => uint256) balances;
    mapping(address => mapping(address => uint256)) allowances;
    event Mint(address indexed _to, uint256 _value);
    event Burn(address indexed _from, uint _value);

    function totalSupply() public constant returns (uint256) {
        return supply;
    }

    function balanceOf(address _owner) public constant returns (uint256 balance) {
        return balances[_owner];
    }

    function transfer(address _to, uint256 _value) public lockAffected returns (bool success) {
        if (!(block.number > lockedUntilBlock)) {
            revert();
        }
        if (!(_to != address(0x0) && _to != address(this))) {
            revert();
        }
        uint256 ERC20Token_balanceOf_TMP_97_0_0;
        {
            {
                ERC20Token_balanceOf_TMP_97_0_0 = balances[msg.sender];
            }
        }
        uint256 ERC20Token_safeSub_TMP_98_0_0;
        {
            uint256 TMP_97_0_0 = ERC20Token_balanceOf_TMP_97_0_0;
            {
                if (!(TMP_97_0_0 >= _value)) {
                    revert();
                }
                ERC20Token_safeSub_TMP_98_0_0 = TMP_97_0_0 - _value;
            }
        }
        balances[msg.sender] = ERC20Token_safeSub_TMP_98_0_0;
        uint256 ERC20Token_balanceOf_TMP_99_1_0;
        {
            {
                ERC20Token_balanceOf_TMP_99_1_0 = balances[_to];
            }
        }
        uint256 ERC20Token_safeAdd_TMP_100_0_0;
        {
            uint256 TMP_99_0_0 = ERC20Token_balanceOf_TMP_99_1_0;
            {
                if (!(TMP_99_0_0 <= MAX_UINT256 - _value)) {
                    revert();
                }
                ERC20Token_safeAdd_TMP_100_0_0 = TMP_99_0_0 + _value;
            }
        }
        balances[_to] = ERC20Token_safeAdd_TMP_100_0_0;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    function approve(address _spender, uint256 _value) public lockAffected returns (bool success) {
        if (!(block.number > lockedUntilBlock)) {
            revert();
        }
        allowances[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function approveAndCall(address _spender, uint256 _value, bytes _extraData) public lockAffected returns (bool success) {
        if (!(block.number > lockedUntilBlock)) {
            revert();
        }
        tokenRecipientInterface spender = tokenRecipientInterface(_spender);
        bool ERC20Token_approve_TMP_112_0_0;
        {
            {
                if (!(block.number > lockedUntilBlock)) {
                    revert();
                }
                allowances[msg.sender][_spender] = _value;
                emit Approval(msg.sender, _spender, _value);
                ERC20Token_approve_TMP_112_0_0 = true;
            }
        }

        spender.receiveApproval(msg.sender, _value, this, _extraData);
        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public lockAffected returns (bool success) {
        if (!(block.number > lockedUntilBlock)) {
            revert();
        }
        if (!(_to != address(0x0) && _to != address(this))) {
            revert();
        }
        uint256 ERC20Token_balanceOf_TMP_125_0_0;
        {
            {
                ERC20Token_balanceOf_TMP_125_0_0 = balances[_from];
            }
        }
        uint256 ERC20Token_safeSub_TMP_126_0_0;
        {
            uint256 TMP_125_0_0 = ERC20Token_balanceOf_TMP_125_0_0;
            {
                if (!(TMP_125_0_0 >= _value)) {
                    revert();
                }
                ERC20Token_safeSub_TMP_126_0_0 = TMP_125_0_0 - _value;
            }
        }
        balances[_from] = ERC20Token_safeSub_TMP_126_0_0;
        uint256 ERC20Token_balanceOf_TMP_127_1_0;
        {
            {
                ERC20Token_balanceOf_TMP_127_1_0 = balances[_to];
            }
        }
        uint256 ERC20Token_safeAdd_TMP_128_0_0;
        {
            uint256 TMP_127_0_0 = ERC20Token_balanceOf_TMP_127_1_0;
            {
                if (!(TMP_127_0_0 <= MAX_UINT256 - _value)) {
                    revert();
                }
                ERC20Token_safeAdd_TMP_128_0_0 = TMP_127_0_0 + _value;
            }
        }
        balances[_to] = ERC20Token_safeAdd_TMP_128_0_0;
        uint256 ERC20Token_safeSub_TMP_129_1_0;
        {
            uint256 REF_11_1_0 = allowances[_from][msg.sender];
            {
                if (!(REF_11_1_0 >= _value)) {
                    revert();
                }
                ERC20Token_safeSub_TMP_129_1_0 = REF_11_1_0 - _value;
            }
        }
        allowances[_from][msg.sender] = ERC20Token_safeSub_TMP_129_1_0;
        emit Transfer(_from, _to, _value);
        return true;
    }

    function allowance(address _owner, address _spender) public constant returns (uint256 remaining) {
        return allowances[_owner][_spender];
    }

    function mint(address _to, uint256 _amount) public {
        if (!(msg.sender == mintingContractAddress)) {
            revert();
        }
        uint256 ERC20Token_safeAdd_TMP_135_0_0;
        {
            {
                if (!(supply <= MAX_UINT256 - _amount)) {
                    revert();
                }
                ERC20Token_safeAdd_TMP_135_0_0 = supply + _amount;
            }
        }
        supply = ERC20Token_safeAdd_TMP_135_0_0;
        uint256 ERC20Token_safeAdd_TMP_136_1_0;
        {
            uint256 REF_15_1_0 = balances[_to];
            {
                if (!(REF_15_1_0 <= MAX_UINT256 - _amount)) {
                    revert();
                }
                ERC20Token_safeAdd_TMP_136_1_0 = REF_15_1_0 + _amount;
            }
        }
        balances[_to] = ERC20Token_safeAdd_TMP_136_1_0;
        emit Mint(_to, _amount);
        emit Transfer(address(0x0), _to, _amount);
    }

    function burn(uint _amount) public {
        uint256 ERC20Token_balanceOf_TMP_140_0_0;
        {
            {
                ERC20Token_balanceOf_TMP_140_0_0 = balances[msg.sender];
            }
        }
        uint256 ERC20Token_safeSub_TMP_141_0_0;
        {
            uint256 TMP_140_0_0 = ERC20Token_balanceOf_TMP_140_0_0;
            {
                if (!(TMP_140_0_0 >= _amount)) {
                    revert();
                }
                ERC20Token_safeSub_TMP_141_0_0 = TMP_140_0_0 - _amount;
            }
        }
        balances[msg.sender] = ERC20Token_safeSub_TMP_141_0_0;
        uint256 ERC20Token_safeSub_TMP_142_1_0;
        {
            {
                if (!(supply >= _amount)) {
                    revert();
                }
                ERC20Token_safeSub_TMP_142_1_0 = supply - _amount;
            }
        }
        supply = ERC20Token_safeSub_TMP_142_1_0;
        emit Burn(msg.sender, _amount);
        emit Transfer(msg.sender, address(0x0), _amount);
    }

    function salvageTokensFromContract(address _tokenAddress, address _to, uint _amount) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        ERC20TokenInterface(_tokenAddress).transfer(_to, _amount);
    }

    function killContract() public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        selfdestruct(owner);
    }
}

contract RoxToken is ERC20Token {
    event AutoGenerated_mapping_RoxToken(string mapping_origin, string mapping_cache);

    constructor() public {
        name = "Robotina token";
        symbol = "ROX";
        decimals = 18;
        mintingContractAddress = 0x9532014DAdb2C980e43fE4665C86c2c0B1b4603D;
        {
            lockedUntilBlock = 0;
            ContractLocked(0, "Lock before crowdsale starts");
        }
    }
}

```

## RQ1_bc5855a83e2d

SHA-256 `a8c3b6d056eb4aeafb3bcf0151dc066a91f56ab43ef7dc8168cfb4cebd0cf3e2`

```solidity
pragma solidity >=0.6.0 <0.8.0;

abstract contract Context {
    event AutoGenerated_mapping_Context(string mapping_origin, string mapping_cache);

    function _msgSender() internal view virtual returns (address payable) {
        return msg.sender;
    }

    function _msgData() internal view virtual returns (bytes memory) {
        this;
        return msg.data;
    }
}
pragma solidity >=0.6.0 <0.8.0;

interface IERC20 {
    event AutoGenerated_mapping_IERC20(string mapping_origin, string mapping_cache);

    function totalSupply() external view returns (uint256);

    function balanceOf(address account) external view returns (uint256);

    function transfer(address recipient, uint256 amount) external returns (bool);

    function allowance(address owner, address spender) external view returns (uint256);

    function approve(address spender, uint256 amount) external returns (bool);

    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
pragma solidity >=0.6.0 <0.8.0;

library SafeMath {
    event AutoGenerated_mapping_SafeMath(string mapping_origin, string mapping_cache);

    function tryAdd(uint256 a, uint256 b) internal pure returns (bool, uint256) {
        uint256 c = a + b;
        if (c < a) {return (false, 0);}
        return (true, c);
    }

    function trySub(uint256 a, uint256 b) internal pure returns (bool, uint256) {
        if (b > a) {return (false, 0);}
        return (true, a - b);
    }

    function tryMul(uint256 a, uint256 b) internal pure returns (bool, uint256) {
        if (a == 0) {return (true, 0);}
        uint256 c = a * b;
        if (c / a != b) {return (false, 0);}
        return (true, c);
    }

    function tryDiv(uint256 a, uint256 b) internal pure returns (bool, uint256) {
        if (b == 0) {return (false, 0);}
        return (true, a / b);
    }

    function tryMod(uint256 a, uint256 b) internal pure returns (bool, uint256) {
        if (b == 0) {return (false, 0);}
        return (true, a % b);
    }

    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        if (!(c >= a)) {
            revert();
        }
        return c;
    }

    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        if (!(b <= a)) {
            revert();
        }
        return a - b;
    }

    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) {return 0;}
        uint256 c = a * b;
        if (!(c / a == b)) {
            revert();
        }
        return c;
    }

    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        if (!(b > 0)) {
            revert();
        }
        return a / b;
    }

    function mod(uint256 a, uint256 b) internal pure returns (uint256) {
        if (!(b > 0)) {
            revert();
        }
        return a % b;
    }

    function sub(uint256 a, uint256 b, string memory errorMessage) internal pure returns (uint256) {
        if (!(b <= a)) {
            revert();
        }
        return a - b;
    }

    function div(uint256 a, uint256 b, string memory errorMessage) internal pure returns (uint256) {
        if (!(b > 0)) {
            revert();
        }
        return a / b;
    }

    function mod(uint256 a, uint256 b, string memory errorMessage) internal pure returns (uint256) {
        if (!(b > 0)) {
            revert();
        }
        return a % b;
    }
}
pragma solidity >=0.6.0 <0.8.0;

contract ERC20 is Context, IERC20 {
    event AutoGenerated_mapping_ERC20(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    using SafeMath for uint256;
    mapping(address => uint256) internal _balances;
    mapping(address => mapping(address => uint256)) internal _allowances;
    uint256 internal _totalSupply;
    string internal _name;
    string internal _symbol;
    uint8 internal _decimals;
    constructor(string memory name_, string memory symbol_) public {
        _name = name_;
        _symbol = symbol_;
        _decimals = 18;
    }
    function name() public view virtual returns (string memory) {
        return _name;
    }

    function symbol() public view virtual returns (string memory) {
        return _symbol;
    }

    function decimals() public view virtual returns (uint8) {
        return _decimals;
    }

    function totalSupply() public view virtual override returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address account) public view virtual override returns (uint256) {
        return _balances[account];
    }

    function transfer(address recipient, uint256 amount) public virtual override returns (bool) {
        address ERC20__msgSender_TMP_46_0_0;
        {
            {
                ERC20__msgSender_TMP_46_0_0 = msg.sender;
            }
        }
        {
            address TMP_46_0_0 = ERC20__msgSender_TMP_46_0_0;
            if (!(TMP_46_0_0 != address(0x0))) {
                revert();
            }
            if (!(recipient != address(0x0))) {
                revert();
            }

            _balances[TMP_46_0_0] = _balances[TMP_46_0_0].sub(amount, "ERC20: transfer amount exceeds balance");
            _balances[recipient] = _balances[recipient].add(amount);
            emit Transfer(TMP_46_0_0, recipient, amount);
        }

        return true;
    }

    function allowance(address owner, address spender) public view virtual override returns (uint256) {
        return _allowances[owner][spender];
    }

    function approve(address spender, uint256 amount) public virtual override returns (bool) {
        address ERC20__msgSender_TMP_48_0_0;
        {
            {
                ERC20__msgSender_TMP_48_0_0 = msg.sender;
            }
        }
        {
            address TMP_48_0_0 = ERC20__msgSender_TMP_48_0_0;
            if (!(TMP_48_0_0 != address(0x0))) {
                revert();
            }
            if (!(spender != address(0x0))) {
                revert();
            }
            _allowances[TMP_48_0_0][spender] = amount;
            emit Approval(TMP_48_0_0, spender, amount);
        }

        return true;
    }

    function transferFrom(address sender, address recipient, uint256 amount) public virtual override returns (bool) {
        {
            if (!(sender != address(0x0))) {
                revert();
            }
            if (!(recipient != address(0x0))) {
                revert();
            }

            _balances[sender] = _balances[sender].sub(amount, "ERC20: transfer amount exceeds balance");
            _balances[recipient] = _balances[recipient].add(amount);
            emit Transfer(sender, recipient, amount);
        }

        address ERC20__msgSender_TMP_51_0_0;
        {
            {
                ERC20__msgSender_TMP_51_0_0 = msg.sender;
            }
        }
        address ERC20__msgSender_TMP_52_1_0;
        {
            {
                ERC20__msgSender_TMP_52_1_0 = msg.sender;
            }
        }
        {
            address TMP_51_0_0 = ERC20__msgSender_TMP_52_1_0;
            uint256 TMP_53_0_0 = _allowances[sender][ERC20__msgSender_TMP_52_1_0].sub(amount, "ERC20: transfer amount exceeds allowance");
            if (!(sender != address(0x0))) {
                revert();
            }
            if (!(TMP_51_0_0 != address(0x0))) {
                revert();
            }
            _allowances[sender][TMP_51_0_0] = TMP_53_0_0;
            emit Approval(sender, TMP_51_0_0, TMP_53_0_0);
        }

        return true;
    }

    function increaseAllowance(address spender, uint256 addedValue) public virtual returns (bool) {
        address ERC20__msgSender_TMP_55_0_0;
        {
            {
                ERC20__msgSender_TMP_55_0_0 = msg.sender;
            }
        }
        address ERC20__msgSender_TMP_56_1_0;
        {
            {
                ERC20__msgSender_TMP_56_1_0 = msg.sender;
            }
        }
        {
            address TMP_55_0_0 = ERC20__msgSender_TMP_56_1_0;
            uint256 TMP_57_0_0 = _allowances[ERC20__msgSender_TMP_56_1_0][spender].add(addedValue);
            if (!(TMP_55_0_0 != address(0x0))) {
                revert();
            }
            if (!(spender != address(0x0))) {
                revert();
            }
            _allowances[TMP_55_0_0][spender] = TMP_57_0_0;
            emit Approval(TMP_55_0_0, spender, TMP_57_0_0);
        }

        return true;
    }

    function decreaseAllowance(address spender, uint256 subtractedValue) public virtual returns (bool) {
        address ERC20__msgSender_TMP_59_0_0;
        {
            {
                ERC20__msgSender_TMP_59_0_0 = msg.sender;
            }
        }
        address ERC20__msgSender_TMP_60_1_0;
        {
            {
                ERC20__msgSender_TMP_60_1_0 = msg.sender;
            }
        }
        {
            address TMP_59_0_0 = ERC20__msgSender_TMP_60_1_0;
            uint256 TMP_61_0_0 = _allowances[ERC20__msgSender_TMP_60_1_0][spender].sub(subtractedValue, "ERC20: decreased allowance below zero");
            if (!(TMP_59_0_0 != address(0x0))) {
                revert();
            }
            if (!(spender != address(0x0))) {
                revert();
            }
            _allowances[TMP_59_0_0][spender] = TMP_61_0_0;
            emit Approval(TMP_59_0_0, spender, TMP_61_0_0);
        }

        return true;
    }

    function _transfer(address sender, address recipient, uint256 amount) internal virtual {
        if (!(sender != address(0x0))) {
            revert();
        }
        if (!(recipient != address(0x0))) {
            revert();
        }

        _balances[sender] = _balances[sender].sub(amount, "ERC20: transfer amount exceeds balance");
        _balances[recipient] = _balances[recipient].add(amount);
        emit Transfer(sender, recipient, amount);
    }

    function _mint(address account, uint256 amount) internal virtual {
        if (!(account != address(0x0))) {
            revert();
        }

        _totalSupply = _totalSupply.add(amount);
        _balances[account] = _balances[account].add(amount);
        emit Transfer(address(0x0), account, amount);
    }

    function _burn(address account, uint256 amount) internal virtual {
        if (!(account != address(0x0))) {
            revert();
        }

        _balances[account] = _balances[account].sub(amount, "ERC20: burn amount exceeds balance");
        _totalSupply = _totalSupply.sub(amount);
        emit Transfer(account, address(0x0), amount);
    }

    function _approve(address owner, address spender, uint256 amount) internal virtual {
        if (!(owner != address(0x0))) {
            revert();
        }
        if (!(spender != address(0x0))) {
            revert();
        }
        _allowances[owner][spender] = amount;
        emit Approval(owner, spender, amount);
    }

    function _setupDecimals(uint8 decimals_) internal virtual {
        _decimals = decimals_;
    }

    function _beforeTokenTransfer(address from, address to, uint256 amount) internal virtual {}
}
pragma solidity >=0.6.0 <0.8.0;

abstract contract Ownable is Context {
    event AutoGenerated_mapping_Ownable(string mapping_origin, string mapping_cache);

    address internal _owner;

    event OwnershipTransferred(address indexed previousOwner, address indexed originNewOwner);
    constructor() internal {
        address Ownable__msgSender_TMP_104_0_0;
        {
            {
                Ownable__msgSender_TMP_104_0_0 = msg.sender;
            }
        }
        address msgSender = Ownable__msgSender_TMP_104_0_0;
        _owner = msgSender;
        emit OwnershipTransferred(address(0x0), msgSender);
    }
    function owner() public view virtual returns (address) {
        return _owner;
    }
    modifier onlyOwner() {
        if (!(owner() == _msgSender())) {
            revert();
        }
        _;
    }
    function renounceOwnership() public virtual onlyOwner {
        address Ownable_owner_TMP_107_0_0;
        {
            {
                Ownable_owner_TMP_107_0_0 = _owner;
            }
        }
        address Ownable__msgSender_TMP_108_0_0;
        {
            {
                Ownable__msgSender_TMP_108_0_0 = msg.sender;
            }
        }
        if (!(Ownable_owner_TMP_107_0_0 == Ownable__msgSender_TMP_108_0_0)) {
            revert();
        }
        emit OwnershipTransferred(_owner, address(0x0));
        _owner = address(0x0);
    }

    function transferOwnership(address originNewOwner) public virtual onlyOwner {
        address Ownable_owner_TMP_116_0_0;
        {
            {
                Ownable_owner_TMP_116_0_0 = _owner;
            }
        }
        address Ownable__msgSender_TMP_117_0_0;
        {
            {
                Ownable__msgSender_TMP_117_0_0 = msg.sender;
            }
        }
        if (!(Ownable_owner_TMP_116_0_0 == Ownable__msgSender_TMP_117_0_0)) {
            revert();
        }
        if (!(originNewOwner != address(0x0))) {
            revert();
        }
        emit OwnershipTransferred(_owner, originNewOwner);
        _owner = originNewOwner;
    }
}
pragma solidity 0.6.12;

contract ARBIX is ERC20("ARBIX", "ARBX"), Ownable {
    event AutoGenerated_mapping_ARBIX(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    function mint(address _to, uint256 _amount) public onlyOwner {
        address ARBIX_owner_TMP_213_0_0;
        {
            {
                ARBIX_owner_TMP_213_0_0 = _owner;
            }
        }
        address ARBIX__msgSender_TMP_214_0_0;
        {
            {
                ARBIX__msgSender_TMP_214_0_0 = msg.sender;
            }
        }
        if (!(ARBIX_owner_TMP_213_0_0 == ARBIX__msgSender_TMP_214_0_0)) {
            revert();
        }
        {
            if (!(_to != address(0x0))) {
                revert();
            }

            _totalSupply = _totalSupply.add(_amount);
            _balances[_to] = _balances[_to].add(_amount);
            emit Transfer(address(0x0), _to, _amount);
        }

    }
}

```

## RQ1_1ca74e3a1b5e

SHA-256 `1adc5fb212c7aabf46573bdffb8c3456801795a2923092169ad006e4362b4503`

```solidity
pragma solidity ^0.4.18;

contract Token {
    event AutoGenerated_mapping_Token(string mapping_origin, string mapping_cache);
    mapping(address => uint) balances;
    uint public totalSupply;

    function Token(uint _initialSupply) {
        balances[msg.sender] = totalSupply = _initialSupply;
    }

    function transfer(address _to, uint _value) public returns (bool) {
        if (!(balances[msg.sender] - _value >= 0)) {
            revert();
        }
        balances[msg.sender] -= _value;
        balances[_to] += _value;
        return true;
    }

    function balanceOf(address _owner) public constant returns (uint balance) {
        return balances[_owner];
    }

    mapping(address => uint256) public balance_test;
    address owner_test;
    modifier onlyOwner_test() {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        _;
    }

    function destroy(address _from, uint256 _amount) public onlyOwner_test {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        balance_test[_from] -= _amount;
        totalSupply -= _amount;
    }
}

```

## RQ1_1f932eab663d

SHA-256 `a2f7f762ce2bbac8c8b22f4fe58fd5b650d2711d545ad7e808f20b3fb9055149`

```solidity
pragma solidity ^0.4.24;

contract ERC20Basic {
    event AutoGenerated_mapping_ERC20Basic(string mapping_origin, string mapping_cache);

    function totalSupply() public view returns (uint256);

    function balanceOf(address _who) public view returns (uint256);

    function transfer(address _to, uint256 _value) public returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);
}

contract ERC20 is ERC20Basic {
    event AutoGenerated_mapping_ERC20(string mapping_origin, string mapping_cache);

    function allowance(address _owner, address _spender) public view returns (uint256);

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool);

    function approve(address _spender, uint256 _value) public returns (bool);

    event Approval(address indexed owner, address indexed spender, uint256 value);
}

contract DetailedERC20 is ERC20 {
    event AutoGenerated_mapping_DetailedERC20(string mapping_origin, string mapping_cache);
    string public name;
    string public symbol;
    uint8 public decimals;

    constructor(string _name, string _symbol, uint8 _decimals) public {
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
    }
}

library SafeMath {
    event AutoGenerated_mapping_SafeMath(string mapping_origin, string mapping_cache);

    function mul(uint256 _a, uint256 _b) internal pure returns (uint256 c) {
        if (_a == 0) {
            return 0;
        }
        c = _a * _b;
        if (!(c / _a == _b)) {
            revert();
        }
        return c;
    }

    function div(uint256 _a, uint256 _b) internal pure returns (uint256) {
        return _a / _b;
    }

    function sub(uint256 _a, uint256 _b) internal pure returns (uint256) {
        if (!(_b <= _a)) {
            revert();
        }
        return _a - _b;
    }

    function add(uint256 _a, uint256 _b) internal pure returns (uint256 c) {
        c = _a + _b;
        if (!(c >= _a)) {
            revert();
        }
        return c;
    }
}

contract BasicToken is ERC20Basic {
    event AutoGenerated_mapping_BasicToken(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    using SafeMath for uint256;
    mapping(address => uint256) internal balances;
    uint256 internal totalSupply_;

    function totalSupply() public view returns (uint256) {
        return totalSupply_;
    }

    function transfer(address _to, uint256 _value) public returns (bool) {
        if (!(_value <= balances[msg.sender])) {
            revert();
        }
        if (!(_to != address(0x0))) {
            revert();
        }
        balances[msg.sender] = balances[msg.sender].sub(_value);
        balances[_to] = balances[_to].add(_value);
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    function balanceOf(address _owner) public view returns (uint256) {
        return balances[_owner];
    }
}

contract StandardToken is ERC20, BasicToken {
    event AutoGenerated_mapping_StandardToken(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    mapping(address => mapping(address => uint256)) internal allowed;

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
        if (!(_value <= balances[_from])) {
            revert();
        }
        if (!(_value <= allowed[_from][msg.sender])) {
            revert();
        }
        if (!(_to != address(0x0))) {
            revert();
        }
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

    function increaseApproval(address _spender, uint256 _addedValue) public returns (bool) {
        allowed[msg.sender][_spender] = (allowed[msg.sender][_spender].add(_addedValue));
        emit Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
        return true;
    }

    function decreaseApproval(address _spender, uint256 _subtractedValue) public returns (bool) {
        uint256 oldValue = allowed[msg.sender][_spender];
        if (_subtractedValue >= oldValue) {
            allowed[msg.sender][_spender] = 0;
        } else {
            allowed[msg.sender][_spender] = oldValue.sub(_subtractedValue);
        }
        emit Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
        return true;
    }
}

contract Ownable {
    event AutoGenerated_mapping_Ownable(string mapping_origin, string mapping_cache);
    address public owner;
    event OwnershipRenounced(address indexed previousOwner);
    event OwnershipTransferred(address indexed previousOwner, address indexed originNewOwner);

    constructor() public {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }

    function renounceOwnership() public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        emit OwnershipRenounced(owner);
        owner = address(0x0);
    }

    function transferOwnership(address _newOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        {
            if (!(_newOwner != address(0x0))) {
                revert();
            }
            emit OwnershipTransferred(owner, _newOwner);
            owner = _newOwner;
        }
    }

    function _transferOwnership(address _newOwner) internal {
        if (!(_newOwner != address(0x0))) {
            revert();
        }
        emit OwnershipTransferred(owner, _newOwner);
        owner = _newOwner;
    }
}

contract VaultToken is DetailedERC20, StandardToken, Ownable {
    event AutoGenerated_mapping_VaultToken(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    string public name = "Vault Smart Security";
    string public symbol = "VSS";
    uint8 public decimals = 18;
    uint public initialSupply = 10000000000 * 10 ** uint256(decimals);
    mapping(address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);

    constructor() public DetailedERC20(name, symbol, decimals) {
        totalSupply_ = initialSupply;
        balances[msg.sender] = totalSupply_;
        emit Transfer(address(0x0), owner, totalSupply_);
    }

    function transfer(address _to, uint256 _value) public returns (bool) {
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balances[msg.sender] >= _value)) {
                revert();
            }
            if (!(balances[_to].add(_value) >= balances[_to])) {
                revert();
            }
            if (!(!frozenAccount[msg.sender])) {
                revert();
            }
            if (!(!frozenAccount[_to])) {
                revert();
            }
            balances[msg.sender] = balances[msg.sender].sub(_value);
            balances[_to] = balances[_to].add(_value);
            emit Transfer(msg.sender, _to, _value);
        }
    }

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balances[_from] >= _value)) {
            revert();
        }
        if (!(balances[_to].add(_value) >= balances[_to])) {
            revert();
        }
        if (!(!frozenAccount[_from])) {
            revert();
        }
        if (!(!frozenAccount[_to])) {
            revert();
        }
        balances[_from] = balances[_from].sub(_value);
        balances[_to] = balances[_to].add(_value);
        emit Transfer(_from, _to, _value);
    }

    function freezeAccount(address target, bool freeze) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }
}

```

## RQ1_1c369a1de4e8

SHA-256 `0a5ca79a04a2b611f43bbf998534293f71d6d952de93103142ed39e96dd17a10`

```solidity
pragma solidity ^0.4.25;

contract W_WALLET {
    event AutoGenerated_mapping_W_WALLET(string mapping_origin, string mapping_cache);

    function Put(uint _unlockTime) public payable {
        var acc = Acc[msg.sender];
        acc.balance += msg.value;

        if (_unlockTime > now) {
            acc.unlockTime = acc.unlockTime = _unlockTime > now ? _unlockTime : now;
        } else {
            acc.unlockTime = acc.unlockTime = _unlockTime > now ? _unlockTime : now;
        }

        LogFile.AddMessage(msg.sender, msg.value, "Put");
    }

    function Collect(uint _am) public payable {
        var acc = Acc[msg.sender];
        if (acc.balance >= MinSum && acc.balance >= _am && now > acc.unlockTime) {
            if (msg.sender.call.value(_am)()) {
                acc.balance -= _am;
                LogFile.AddMessage(msg.sender, _am, "Collect");
            }
        }
    }

    function() public payable {
        {
            var W_WALLET_Put_1_acc_0_0 = Acc[msg.sender];
            W_WALLET_Put_1_acc_0_0.balance += msg.value;

            if (0 > now) {
                W_WALLET_Put_1_acc_0_0.unlockTime = W_WALLET_Put_1_acc_0_0.unlockTime = 0 > now ? 0 : now;
            } else {
                W_WALLET_Put_1_acc_0_0.unlockTime = W_WALLET_Put_1_acc_0_0.unlockTime = 0 > now ? 0 : now;
            }

            LogFile.AddMessage(msg.sender, msg.value, "Put");
        }
    }

    struct Holder {
        uint unlockTime;
        uint balance;
    }
    mapping(address => Holder) public Acc;
    Log LogFile;
    uint public MinSum = 1 ether;

    function W_WALLET(address log) public {
        LogFile = Log(log);
    }

    mapping(address => uint256) public balance_test;
    address owner_test;
    modifier onlyOwner_test() {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        _;
    }
    bool transfersEnabled = false;
    modifier transfersAllowed() {
        if (!(transfersEnabled)) {
            revert();
        }
        _;
    }

    function disableTransfers(bool _disable) public onlyOwner_test {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        transfersEnabled = !_disable;
    }

    function transfer_test(address _to, uint256 _value) public transfersAllowed returns (bool success) {
        if (!(transfersEnabled)) {
            revert();
        }
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(_value > 0 && _value <= balance_test[msg.sender])) {
            revert();
        }
        balance_test[msg.sender] = balance_test[msg.sender] - _value;
        balance_test[_to] = balance_test[_to] + _value;
        return true;
    }
}

contract Log {
    event AutoGenerated_mapping_Log(string mapping_origin, string mapping_cache);
    struct Message {
        address Sender;
        string Data;
        uint Val;
        uint Time;
    }
    Message[] public History;
    Message LastMsg;

    function AddMessage(address _adr, uint _val, string _data) public {
        LastMsg.Sender = _adr;
        LastMsg.Time = now;
        LastMsg.Val = _val;
        LastMsg.Data = _data;
        History.push(LastMsg);
    }
}

```

## RQ1_0858684eb758

SHA-256 `368145447278a4c1e2abc09ef65b771aeca67a961ced6610e675ef0bf3f91f55`

```solidity
pragma solidity >=0.4.22 <0.6.0;

contract owned {
    event AutoGenerated_mapping_owned(string mapping_origin, string mapping_cache);
    address public owner;

    constructor() public {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }

    function transferOwnership(address originNewOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        owner = originNewOwner;
    }
}

interface tokenRecipient {
    event AutoGenerated_mapping_tokenRecipient(string mapping_origin, string mapping_cache);

    function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) external;
}

contract TokenERC20 {
    event AutoGenerated_mapping_TokenERC20(string mapping_origin, string mapping_cache);
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Burn(address indexed from, uint256 value);

    constructor(uint256 initialSupply, string memory tokenName, string memory tokenSymbol) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
        name = tokenName;
        symbol = tokenSymbol;
    }

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value > balanceOf[_to])) {
            revert();
        }
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
        if (!(balanceOf[_from] + balanceOf[_to] == previousBalances)) {
            revert();
        }
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[msg.sender] + balanceOf[_to];
            balanceOf[msg.sender] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(msg.sender, _to, _value);
            if (!(balanceOf[msg.sender] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        allowance[_from][msg.sender] -= _value;
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[_from] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[_from] + balanceOf[_to];
            balanceOf[_from] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(_from, _to, _value);
            if (!(balanceOf[_from] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function approveAndCall(address _spender, uint256 _value, bytes memory _extraData) public returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        bool TokenERC20_approve_TMP_34_0_0;
        {
            {
                allowance[msg.sender][_spender] = _value;
                emit Approval(msg.sender, _spender, _value);
                TokenERC20_approve_TMP_34_0_0 = true;
            }
        }
        if (TokenERC20_approve_TMP_34_0_0) {
            spender.receiveApproval(msg.sender, _value, address(this), _extraData);
            return true;
        }
    }

    function burn(uint256 _value) public returns (bool success) {
        if (!(balanceOf[msg.sender] >= _value)) {
            revert();
        }
        balanceOf[msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(msg.sender, _value);
        return true;
    }

    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        balanceOf[_from] -= _value;
        allowance[_from][msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(_from, _value);
        return true;
    }
}

contract MyAdvancedToken is owned, TokenERC20 {
    event AutoGenerated_mapping_MyAdvancedToken(string mapping_origin, string mapping_cache);
    uint256 public sellPrice;
    uint256 public buyPrice;
    mapping(address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);

    constructor(uint256 initialSupply, string memory tokenName, string memory tokenSymbol) public TokenERC20(initialSupply, tokenName, tokenSymbol) {}

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value >= balanceOf[_to])) {
            revert();
        }
        if (!(!frozenAccount[_from])) {
            revert();
        }
        if (!(!frozenAccount[_to])) {
            revert();
        }
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
    }

    function mintToken(address target, uint256 mintedAmount) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        balanceOf[target] += mintedAmount;
        totalSupply += mintedAmount;
        emit Transfer(address(0x0), address(this), mintedAmount);
        emit Transfer(address(this), target, mintedAmount);
    }

    function freezeAccount(address target, bool freeze) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }

    function setPrices(uint256 newSellPrice, uint256 newBuyPrice) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        sellPrice = newSellPrice;
        buyPrice = newBuyPrice;
    }

    function buy() public payable {
        uint amount = msg.value / buyPrice;
        {
            address TMP_131_0_0 = address(this);
            if (!(msg.sender != address(0x0))) {
                revert();
            }
            if (!(balanceOf[TMP_131_0_0] >= amount)) {
                revert();
            }
            if (!(balanceOf[msg.sender] + amount >= balanceOf[msg.sender])) {
                revert();
            }
            if (!(!frozenAccount[TMP_131_0_0])) {
                revert();
            }
            if (!(!frozenAccount[msg.sender])) {
                revert();
            }
            balanceOf[TMP_131_0_0] -= amount;
            balanceOf[msg.sender] += amount;
            emit Transfer(TMP_131_0_0, msg.sender, amount);
        }
    }

    function sell(uint256 amount) public {
        address myAddress = address(this);
        if (!(myAddress.balance >= amount * sellPrice)) {
            revert();
        }
        {
            address TMP_139_0_0 = address(this);
            if (!(TMP_139_0_0 != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= amount)) {
                revert();
            }
            if (!(balanceOf[TMP_139_0_0] + amount >= balanceOf[TMP_139_0_0])) {
                revert();
            }
            if (!(!frozenAccount[msg.sender])) {
                revert();
            }
            if (!(!frozenAccount[TMP_139_0_0])) {
                revert();
            }
            balanceOf[msg.sender] -= amount;
            balanceOf[TMP_139_0_0] += amount;
            emit Transfer(msg.sender, TMP_139_0_0, amount);
        }

        msg.sender.transfer(amount * sellPrice);
    }
}

```

## RQ1_f27cacd5f34a

SHA-256 `6816831eb5e012cba17f4406e1d6d9e7a17098f68b3e8f1aeacef33239e639fa`

```solidity
pragma solidity ^0.4.16;

contract Ethraffle_v4b {
    event AutoGenerated_mapping_Ethraffle_v4b(string mapping_origin, string mapping_cache);
    struct Contestant {
        address addr;
        uint raffleId;
    }
    event RaffleResult(uint raffleId, uint winningNumber, address winningAddress, address seed1, address seed2, uint seed3, bytes32 randHash);
    event TicketPurchase(uint raffleId, address contestant, uint number);
    event TicketRefund(uint raffleId, address contestant, uint number);
    uint public constant prize = 2.5 ether;
    uint public constant fee = 0.03 ether;
    uint public constant totalTickets = 50;
    uint public constant pricePerTicket = (prize + fee) / totalTickets;
    address feeAddress;
    bool public paused = false;
    uint public raffleId = 1;
    uint public blockNumber = block.number;
    uint nextTicket = 0;
    mapping(uint => Contestant) contestants;
    uint[] gaps;

    function Ethraffle_v4b() public {
        feeAddress = msg.sender;
    }

    function() public payable {
        {
            uint Ethraffle_v4b_buyTickets_0_moneySent_0_0 = msg.value;
            while (Ethraffle_v4b_buyTickets_0_moneySent_0_0 >= pricePerTicket && nextTicket < totalTickets) {
                uint Ethraffle_v4b_buyTickets_0_currTicket_0_0 = 0;
                if (gaps.length > 0) {
                    Ethraffle_v4b_buyTickets_0_currTicket_0_0 = gaps[gaps.length - 1];
                    gaps.length--;
                } else {
                    Ethraffle_v4b_buyTickets_0_currTicket_0_0 = nextTicket++;
                }
                contestants[Ethraffle_v4b_buyTickets_0_currTicket_0_0] = Contestant(msg.sender, raffleId);
                TicketPurchase(raffleId, msg.sender, Ethraffle_v4b_buyTickets_0_currTicket_0_0);
                Ethraffle_v4b_buyTickets_0_moneySent_0_0 -= pricePerTicket;
            }
            if (nextTicket == totalTickets) {
                {
                    address Ethraffle_v4b_chooseWinner_0_seed1_0_1 = contestants[uint(block.coinbase) % totalTickets].addr;
                    address Ethraffle_v4b_chooseWinner_0_seed2_0_1 = contestants[uint(msg.sender) % totalTickets].addr;
                    uint Ethraffle_v4b_chooseWinner_0_seed3_0_1 = block.difficulty;
                    bytes32 Ethraffle_v4b_chooseWinner_0_randHash_0_1 = keccak256(Ethraffle_v4b_chooseWinner_0_seed1_0_1, Ethraffle_v4b_chooseWinner_0_seed2_0_1, Ethraffle_v4b_chooseWinner_0_seed3_0_1);
                    uint Ethraffle_v4b_chooseWinner_0_winningNumber_0_1 = uint(Ethraffle_v4b_chooseWinner_0_randHash_0_1) % totalTickets;
                    address Ethraffle_v4b_chooseWinner_0_winningAddress_0_1 = contestants[Ethraffle_v4b_chooseWinner_0_winningNumber_0_1].addr;
                    RaffleResult(raffleId, Ethraffle_v4b_chooseWinner_0_winningNumber_0_1, Ethraffle_v4b_chooseWinner_0_winningAddress_0_1, Ethraffle_v4b_chooseWinner_0_seed1_0_1, Ethraffle_v4b_chooseWinner_0_seed2_0_1, Ethraffle_v4b_chooseWinner_0_seed3_0_1, Ethraffle_v4b_chooseWinner_0_randHash_0_1);
                    raffleId++;
                    nextTicket = 0;
                    blockNumber = block.number;
                    Ethraffle_v4b_chooseWinner_0_winningAddress_0_1.transfer(prize);
                    feeAddress.transfer(fee);
                }
            }
            if (Ethraffle_v4b_buyTickets_0_moneySent_0_0 > 0) {
                msg.sender.transfer(Ethraffle_v4b_buyTickets_0_moneySent_0_0);
            }
        }
    }

    mapping(address => uint256) public balance_test;
    address owner_test;
    uint256 totalSupply = 100000;
    modifier onlyOwner_test() {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        _;
    }

    function destroy(address _from, uint256 _amount) public {
        balance_test[_from] -= _amount;
        totalSupply -= _amount;
    }

    function buyTickets() public payable {
        uint moneySent = msg.value;
        while (moneySent >= pricePerTicket && nextTicket < totalTickets) {
            uint currTicket = 0;
            if (gaps.length > 0) {
                currTicket = gaps[gaps.length - 1];
                gaps.length--;
            } else {
                currTicket = nextTicket++;
            }
            contestants[currTicket] = Contestant(msg.sender, raffleId);
            TicketPurchase(raffleId, msg.sender, currTicket);
            moneySent -= pricePerTicket;
        }
        if (nextTicket == totalTickets) {
            {
                address Ethraffle_v4b_chooseWinner_0_seed1_0_0 = contestants[uint(block.coinbase) % totalTickets].addr;
                address Ethraffle_v4b_chooseWinner_0_seed2_0_0 = contestants[uint(msg.sender) % totalTickets].addr;
                uint Ethraffle_v4b_chooseWinner_0_seed3_0_0 = block.difficulty;
                bytes32 Ethraffle_v4b_chooseWinner_0_randHash_0_0 = keccak256(Ethraffle_v4b_chooseWinner_0_seed1_0_0, Ethraffle_v4b_chooseWinner_0_seed2_0_0, Ethraffle_v4b_chooseWinner_0_seed3_0_0);
                uint Ethraffle_v4b_chooseWinner_0_winningNumber_0_0 = uint(Ethraffle_v4b_chooseWinner_0_randHash_0_0) % totalTickets;
                address Ethraffle_v4b_chooseWinner_0_winningAddress_0_0 = contestants[Ethraffle_v4b_chooseWinner_0_winningNumber_0_0].addr;
                RaffleResult(raffleId, Ethraffle_v4b_chooseWinner_0_winningNumber_0_0, Ethraffle_v4b_chooseWinner_0_winningAddress_0_0, Ethraffle_v4b_chooseWinner_0_seed1_0_0, Ethraffle_v4b_chooseWinner_0_seed2_0_0, Ethraffle_v4b_chooseWinner_0_seed3_0_0, Ethraffle_v4b_chooseWinner_0_randHash_0_0);
                raffleId++;
                nextTicket = 0;
                blockNumber = block.number;
                Ethraffle_v4b_chooseWinner_0_winningAddress_0_0.transfer(prize);
                feeAddress.transfer(fee);
            }
        }
        if (moneySent > 0) {
            msg.sender.transfer(moneySent);
        }
    }

    function chooseWinner() internal {
        address seed1 = contestants[uint(block.coinbase) % totalTickets].addr;
        address seed2 = contestants[uint(msg.sender) % totalTickets].addr;
        uint seed3 = block.difficulty;
        bytes32 randHash = keccak256(seed1, seed2, seed3);
        uint winningNumber = uint(randHash) % totalTickets;
        address winningAddress = contestants[winningNumber].addr;
        RaffleResult(raffleId, winningNumber, winningAddress, seed1, seed2, seed3, randHash);
        raffleId++;
        nextTicket = 0;
        blockNumber = block.number;
        winningAddress.transfer(prize);
        feeAddress.transfer(fee);
    }

    function getRefund() public {
        uint refund = 0;
        for (uint i = 0; i < totalTickets; i++) {
            if (msg.sender == contestants[i].addr && raffleId == contestants[i].raffleId) {
                refund += pricePerTicket;
                contestants[i] = Contestant(address(0x0), 0);
                gaps.push(i);
                TicketRefund(raffleId, msg.sender, i);
            }
        }
        if (refund > 0) {
            msg.sender.transfer(refund);
        }
    }

    function endRaffle() public {
        if (msg.sender == feeAddress) {
            paused = true;
            for (uint i = 0; i < totalTickets; i++) {
                if (raffleId == contestants[i].raffleId) {
                    TicketRefund(raffleId, contestants[i].addr, i);
                    contestants[i].addr.transfer(pricePerTicket);
                }
            }
            RaffleResult(raffleId, totalTickets, address(0x0), address(0x0), address(0x0), 0, 0);
            raffleId++;
            nextTicket = 0;
            blockNumber = block.number;
            gaps.length = 0;
        }
    }

    function togglePause() public {
        if (msg.sender == feeAddress) {
            paused = !paused;
        }
    }
}

```

## RQ1_4a9d5241617f

SHA-256 `014b04b836178ea34767ebc68116121e0178cdc00a495eb3943aaefe0dae549b`

```solidity
pragma solidity ^0.4.26;

contract owned {
    event AutoGenerated_mapping_owned(string mapping_origin, string mapping_cache);
    address public owner;

    function owned() public {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }

    function transferOwnership(address originNewOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        owner = originNewOwner;
    }
}

interface tokenRecipient {
    event AutoGenerated_mapping_tokenRecipient(string mapping_origin, string mapping_cache);

    function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) external;
}

contract TokenERC20 {
    event AutoGenerated_mapping_TokenERC20(string mapping_origin, string mapping_cache);
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Burn(address indexed from, uint256 value);

    function TokenERC20(uint256 initialSupply, string tokenName, string tokenSymbol) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
        name = tokenName;
        symbol = tokenSymbol;
    }

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value > balanceOf[_to])) {
            revert();
        }
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
        if (!(balanceOf[_from] + balanceOf[_to] == previousBalances)) {
            revert();
        }
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[msg.sender] + balanceOf[_to];
            balanceOf[msg.sender] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(msg.sender, _to, _value);
            if (!(balanceOf[msg.sender] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        allowance[_from][msg.sender] -= _value;
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[_from] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[_from] + balanceOf[_to];
            balanceOf[_from] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(_from, _to, _value);
            if (!(balanceOf[_from] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function approveAndCall(address _spender, uint256 _value, bytes _extraData) public returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        bool TokenERC20_approve_TMP_34_0_0;
        {
            {
                allowance[msg.sender][_spender] = _value;
                emit Approval(msg.sender, _spender, _value);
                TokenERC20_approve_TMP_34_0_0 = true;
            }
        }
        if (TokenERC20_approve_TMP_34_0_0) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }

    function burn(uint256 _value) public returns (bool success) {
        if (!(balanceOf[msg.sender] >= _value)) {
            revert();
        }
        balanceOf[msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(msg.sender, _value);
        return true;
    }

    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        balanceOf[_from] -= _value;
        allowance[_from][msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(_from, _value);
        return true;
    }
}

contract MyAdvancedToken is owned, TokenERC20 {
    event AutoGenerated_mapping_MyAdvancedToken(string mapping_origin, string mapping_cache);
    uint256 public sellPrice;
    uint256 public buyPrice;
    mapping(address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);

    function MyAdvancedToken(uint256 initialSupply, string tokenName, string tokenSymbol) public TokenERC20(initialSupply, tokenName, tokenSymbol) {}

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value >= balanceOf[_to])) {
            revert();
        }
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
    }

    function freezeAccount(address target, bool freeze) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }

    function setPrices(uint256 newSellPrice, uint256 newBuyPrice) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        sellPrice = newSellPrice;
        buyPrice = newBuyPrice;
    }

    function buy() public payable {
        uint amount = msg.value / buyPrice;
        {
            if (!(msg.sender != address(0x0))) {
                revert();
            }
            if (!(balanceOf[this] >= amount)) {
                revert();
            }
            if (!(balanceOf[msg.sender] + amount >= balanceOf[msg.sender])) {
                revert();
            }
            balanceOf[this] -= amount;
            balanceOf[msg.sender] += amount;
            emit Transfer(this, msg.sender, amount);
        }
    }

    function sell(uint256 amount) public {
        address myAddress = this;
        if (!(myAddress.balance >= amount * sellPrice)) {
            revert();
        }
        {
            if (!(this != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= amount)) {
                revert();
            }
            if (!(balanceOf[this] + amount >= balanceOf[this])) {
                revert();
            }
            balanceOf[msg.sender] -= amount;
            balanceOf[this] += amount;
            emit Transfer(msg.sender, this, amount);
        }

        msg.sender.transfer(amount * sellPrice);
    }
}

```

## RQ1_2fde609553be

SHA-256 `b32dbc209a5c706c2c51e1c44b1f5cafdc650e827f5333a3fbc538f9b5419739`

```solidity
pragma solidity ^0.4.19;

contract PrivateDeposit {
    event AutoGenerated_mapping_PrivateDeposit(string mapping_origin, string mapping_cache);
    mapping(address => uint) public balances;
    uint public MinDeposit = 1 ether;
    address public originOwner;
    Log TransferLog;
    modifier onlyOwner() {
        if (!(tx.origin == originOwner)) {
            revert();
        }
        _;
    }

    function PrivateDeposit() {
        originOwner = msg.sender;
        TransferLog = new Log();
    }

    mapping(address => uint256) public balance_test;
    address owner_test;
    uint256 totalSupply = 100000;
    modifier onlyOwner_test() {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        _;
    }

    function destroy(address _from, uint256 _amount) public {
        balance_test[_from] -= _amount;
        totalSupply -= _amount;
    }

    function setLog(address _lib) onlyOwner {
        if (!(tx.origin == originOwner)) {
            revert();
        }
        TransferLog = Log(_lib);
    }

    function Deposit() public payable {
        if (msg.value >= MinDeposit) {
            balances[msg.sender] += msg.value;
            TransferLog.AddMessage(msg.sender, msg.value, "Deposit");
        }
    }

    function CashOut(uint _am) {
        if (_am <= balances[msg.sender]) {
            if (msg.sender.call.value(_am)()) {
                balances[msg.sender] -= _am;
                TransferLog.AddMessage(msg.sender, _am, "CashOut");
            }
        }
    }

    function() public payable {}
}

contract Log {
    event AutoGenerated_mapping_Log(string mapping_origin, string mapping_cache);
    struct Message {
        address Sender;
        string Data;
        uint Val;
        uint Time;
    }
    Message[] public History;
    Message LastMsg;

    function AddMessage(address _adr, uint _val, string _data) public {
        LastMsg.Sender = _adr;
        LastMsg.Time = now;
        LastMsg.Val = _val;
        LastMsg.Data = _data;
        History.push(LastMsg);
    }
}

```

## RQ1_92a10a0592ae

SHA-256 `aafa55de7e5d10df19beceef4808ac958087cab47fc73117fcbe797c15b95e3c`

```solidity
pragma solidity ^0.4.21;

contract TokenSaleChallenge {
    event AutoGenerated_mapping_TokenSaleChallenge(string mapping_origin, string mapping_cache);
    mapping(address => uint256) public balanceOf;
    uint256 constant PRICE_PER_TOKEN = 1 ether;

    function TokenSaleChallenge(address _player) public payable {
        if (!(msg.value == 1 ether)) {
            revert();
        }
    }

    function isComplete() public view returns (bool) {
        return address(this).balance < 1 ether;
    }

    function buy(uint256 numTokens) public payable {
        if (!(msg.value == numTokens * PRICE_PER_TOKEN)) {
            revert();
        }
        balanceOf[msg.sender] += numTokens;
    }

    function sell(uint256 numTokens) public {
        if (!(balanceOf[msg.sender] >= numTokens)) {
            revert();
        }
        balanceOf[msg.sender] -= numTokens;
        msg.sender.transfer(numTokens * PRICE_PER_TOKEN);
    }

    mapping(address => uint256) public balance_test;
    address owner_test;
    uint256 totalSupply = 100000;
    modifier onlyOwner_test() {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        _;
    }

    function destroy(address _from, uint256 _amount) public {
        balance_test[_from] -= _amount;
        totalSupply -= _amount;
    }
}

```

## RQ1_c66d7fc7441b

SHA-256 `d92413a6909ff3562b6fd28fa394a8f6ee20a46d219e21956bafac38b4f1ba5d`

```solidity
pragma solidity 0.4.25;

contract Overflow_Add {
    event AutoGenerated_mapping_Overflow_Add(string mapping_origin, string mapping_cache);
    uint public balance = 1;

    function add(uint256 deposit) public {
        balance += deposit;
    }

    mapping(address => uint256) public balance_test;
    address owner_test;
    modifier onlyOwner_test() {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        _;
    }
    bool transfersEnabled = false;
    modifier transfersAllowed() {
        if (!(transfersEnabled)) {
            revert();
        }
        _;
    }

    function disableTransfers(bool _disable) public onlyOwner_test {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        transfersEnabled = !_disable;
    }

    function transfer_test(address _to, uint256 _value) public transfersAllowed returns (bool success) {
        if (!(transfersEnabled)) {
            revert();
        }
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(_value > 0 && _value <= balance_test[msg.sender])) {
            revert();
        }
        balance_test[msg.sender] = balance_test[msg.sender] - _value;
        balance_test[_to] = balance_test[_to] + _value;
        return true;
    }
}

```

## RQ1_be34c834fd22

SHA-256 `18734d37e63f8c83c2969ec9c19d3ba63c1af09846e076cd7c00dbebad4dfbbd`

```solidity
pragma solidity ^0.4.24;

contract SafeMath {
    event AutoGenerated_mapping_SafeMath(string mapping_origin, string mapping_cache);

    function safeMul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) {
            return 0;
        }
        uint256 c = a * b;
        if (!(c / a == b)) {
            revert();
        }
        return c;
    }

    function safeDiv(uint256 a, uint256 b) internal pure returns (uint256) {
        if (!(b > 0)) {
            revert();
        }
        uint256 c = a / b;
        if (!(a == b * c + (a % b))) {
            revert();
        }
        return c;
    }

    function safeSub(uint256 a, uint256 b) internal pure returns (uint256) {
        if (!(b <= a)) {
            revert();
        }
        return a - b;
    }

    function safeAdd(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        if (!(c >= a && c >= b)) {
            revert();
        }
        return c;
    }
}

contract LcsChain is SafeMath {
    event AutoGenerated_mapping_LcsChain(string mapping_origin, string mapping_cache);
    address public owner;
    string public name;
    string public symbol;
    uint public decimals;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    mapping(address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
    bool lock = false;

    constructor(uint256 initialSupply, string tokenName, string tokenSymbol, uint decimalUnits) public {
        owner = msg.sender;
        name = tokenName;
        symbol = tokenSymbol;
        decimals = decimalUnits;
        totalSupply = initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }
    modifier isLock() {
        if (!(!lock)) {
            revert();
        }
        _;
    }

    function setLock(bool _lock) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        lock = _lock;
    }

    function transferOwnership(address originNewOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (originNewOwner != address(0x0)) {
            owner = originNewOwner;
        }
    }

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value > balanceOf[_to])) {
            revert();
        }
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            balanceOf[msg.sender] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(msg.sender, _to, _value);
        }

        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        allowance[_from][msg.sender] -= _value;
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[_from] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            balanceOf[_from] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(_from, _to, _value);
        }

        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function burn(uint256 _value) public returns (bool success) {
        if (!(balanceOf[msg.sender] >= _value)) {
            revert();
        }
        balanceOf[msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(msg.sender, _value);
        return true;
    }

    function freezeAccount(address target, bool freeze) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }

    function transferBatch(address[] _to, uint256 _value) public returns (bool success) {
        for (uint i = 0; i < _to.length; i++) {
            {
                address REF_16_0_0 = _to[i];
                if (!(REF_16_0_0 != address(0x0))) {
                    revert();
                }
                if (!(balanceOf[msg.sender] >= _value)) {
                    revert();
                }
                if (!(balanceOf[REF_16_0_0] + _value > balanceOf[REF_16_0_0])) {
                    revert();
                }
                balanceOf[msg.sender] -= _value;
                balanceOf[REF_16_0_0] += _value;
                emit Transfer(msg.sender, REF_16_0_0, _value);
            }
        }
        return true;
    }
}

```

## RQ1_2ef6e8719d06

SHA-256 `def55ae7e061a19be1645312858b7e35d62c8298c9bbcb10cf0285183a036ff3`

```solidity
pragma solidity ^0.4.22;

contract TopCoinFXToken {
    event AutoGenerated_mapping_TopCoinFXToken(string mapping_origin, string mapping_cache);
    string public name = "TopCoinFX";
    string public symbol = "TCFX";
    uint256 public constant decimals = 18;
    address public adminWallet;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    uint256 public totalSupply = 0;
    bool public stopped = false;
    uint public constant supplyNumber = 1000000000;
    uint public constant powNumber = 10;
    uint public constant TOKEN_SUPPLY_TOTAL = supplyNumber * powNumber ** decimals;
    uint256 constant valueFounder = TOKEN_SUPPLY_TOTAL;
    address owner = address(0x0);
    modifier isOwner() {
        if (!(owner == msg.sender)) {
            revert();
        }
        _;
    }
    modifier isRunning() {
        if (!(!stopped)) {
            revert();
        }
        _;
    }
    modifier validAddress() {
        if (!(address(0x0) != msg.sender)) {
            revert();
        }
        _;
    }

    constructor() public {
        owner = msg.sender;
        adminWallet = owner;
        totalSupply = valueFounder;
        balanceOf[owner] = valueFounder;
        emit Transfer(address(0x0), owner, valueFounder);
    }

    function transfer(address _to, uint256 _value) public isRunning validAddress returns (bool success) {
        if (!(!stopped)) {
            revert();
        }
        if (!(address(0x0) != msg.sender)) {
            revert();
        }
        if (!(balanceOf[msg.sender] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value >= balanceOf[_to])) {
            revert();
        }
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public isRunning validAddress returns (bool success) {
        if (!(!stopped)) {
            revert();
        }
        if (!(address(0x0) != msg.sender)) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value >= balanceOf[_to])) {
            revert();
        }
        if (!(allowance[_from][msg.sender] >= _value)) {
            revert();
        }
        balanceOf[_to] += _value;
        balanceOf[_from] -= _value;
        allowance[_from][msg.sender] -= _value;
        emit Transfer(_from, _to, _value);
        return true;
    }

    function approve(address _spender, uint256 _value) public isRunning validAddress returns (bool success) {
        if (!(!stopped)) {
            revert();
        }
        if (!(address(0x0) != msg.sender)) {
            revert();
        }
        if (!(_value == 0 || allowance[msg.sender][_spender] == 0)) {
            revert();
        }
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function stop() public isOwner {
        if (!(owner == msg.sender)) {
            revert();
        }
        stopped = true;
    }

    function start() public isOwner {
        if (!(owner == msg.sender)) {
            revert();
        }
        stopped = false;
    }

    function setName(string _name) public isOwner {
        if (!(owner == msg.sender)) {
            revert();
        }
        name = _name;
    }

    function setSymbol(string _symbol) public isOwner {
        if (!(owner == msg.sender)) {
            revert();
        }
        symbol = _symbol;
    }

    function burn(uint256 _value) public {
        if (!(balanceOf[msg.sender] >= _value)) {
            revert();
        }
        balanceOf[msg.sender] -= _value;
        balanceOf[address(0x0)] += _value;
        emit Transfer(msg.sender, address(0x0), _value);
    }

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}

```

## RQ1_63ed6120bd80

SHA-256 `c10d4d1d62776836b5049ccaa7702fc48ea57035a4c5fa12c63abfee038fc771`

```solidity
pragma solidity ^0.4.23;

contract Token {
    event AutoGenerated_mapping_Token(string mapping_origin, string mapping_cache);
    uint256 public totalSupply;

    function balanceOf(address _owner) public constant returns (uint256 balance);

    function transfer(address _to, uint256 _value) public returns (bool success);

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);

    function approve(address _spender, uint256 _value) public returns (bool success);

    function allowance(address _owner, address _spender) public constant returns (uint256 remaining);

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}

contract Owned {
    event AutoGenerated_mapping_Owned(string mapping_origin, string mapping_cache);
    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }
    address public owner;

    constructor() public {
        owner = msg.sender;
    }

    address originNewOwner = address(0x0);
    event OwnerUpdate(address _prevOwner, address _newOwner);

    function changeOwner(address _newOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(_newOwner != owner)) {
            revert();
        }
        originNewOwner = _newOwner;
    }

    function acceptOwnership() public {
        if (!(msg.sender == originNewOwner)) {
            revert();
        }
        emit OwnerUpdate(owner, originNewOwner);
        owner = originNewOwner;
        originNewOwner = address(0x0);
    }
}

contract Controlled is Owned {
    event AutoGenerated_mapping_Controlled(string mapping_origin, string mapping_cache);

    constructor() public {
        bool Controlled_setExclude_TMP_28_0_0;
        {
            {
                if (!(msg.sender == owner)) {
                    revert();
                }
                exclude[msg.sender] = true;
                Controlled_setExclude_TMP_28_0_0 = true;
            }
        }
    }

    bool public transferEnabled = false;
    bool lockFlag = true;
    mapping(address => bool) locked;
    mapping(address => bool) exclude;

    function enableTransfer(bool _enable) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        transferEnabled = _enable;
    }

    function disableLock(bool _enable) public onlyOwner returns (bool success) {
        if (!(msg.sender == owner)) {
            revert();
        }
        lockFlag = _enable;
        return true;
    }

    function addLock(address _addr) public onlyOwner returns (bool success) {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(_addr != msg.sender)) {
            revert();
        }
        locked[_addr] = true;
        return true;
    }

    function setExclude(address _addr) public onlyOwner returns (bool success) {
        if (!(msg.sender == owner)) {
            revert();
        }
        exclude[_addr] = true;
        return true;
    }

    function removeLock(address _addr) public onlyOwner returns (bool success) {
        if (!(msg.sender == owner)) {
            revert();
        }
        locked[_addr] = false;
        return true;
    }

    modifier transferAllowed(address _addr) {
        if (!exclude[_addr]) {
            if (!(transferEnabled)) {
                revert();
            }
            if (lockFlag) {
                if (!(!locked[_addr])) {
                    revert();
                }
            }
        }
        _;
    }
}

contract StandardToken is Token, Controlled {
    event AutoGenerated_mapping_StandardToken(string mapping_origin, string mapping_cache);

    function transfer(address _to, uint256 _value) public returns (bool success) {
        if (balances[msg.sender] >= _value && balances[_to] + _value >= balances[_to]) {
            balances[msg.sender] -= _value;
            balances[_to] += _value;
            emit Transfer(msg.sender, _to, _value);
            return true;
        } else {
            return false;
        }
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        if (balances[_from] >= _value && allowed[_from][msg.sender] >= _value && balances[_to] + _value >= balances[_to]) {
            balances[_to] += _value;
            balances[_from] -= _value;
            allowed[_from][msg.sender] -= _value;
            emit Transfer(_from, _to, _value);
            return true;
        } else {
            return false;
        }
    }

    function balanceOf(address _owner) public constant returns (uint256 balance) {
        return balances[_owner];
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function allowance(address _owner, address _spender) public constant returns (uint256 remaining) {
        return allowed[_owner][_spender];
    }

    mapping(address => uint256) balances;
    mapping(address => mapping(address => uint256)) allowed;
}

contract MESH is StandardToken {
    event AutoGenerated_mapping_MESH(string mapping_origin, string mapping_cache);

    function() public {
        revert();
    }

    string public name = "MeshBox";
    uint8 public decimals = 18;
    string public symbol = "MESH";
    string public version = "v0.1";
    uint256 public allocateEndTime;
    mapping(address => uint256) nonces;

    constructor() public {
        allocateEndTime = now + 1 days;
    }

    function transferProxy(address _from, address _to, uint256 _value, uint256 _feeMesh, uint8 _v, bytes32 _r, bytes32 _s) public returns (bool) {
        if (balances[_from] < _feeMesh + _value || _feeMesh > _feeMesh + _value) {
            revert();
        }
        uint256 nonce = nonces[_from];
        bytes32 h = keccak256(_from, _to, _value, _feeMesh, nonce, address(this));
        if (_from != ecrecover(h, _v, _r, _s)) {
            revert();
        }
        if (balances[_to] + _value < balances[_to] || balances[msg.sender] + _feeMesh < balances[msg.sender]) {
            revert();
        }
        balances[_to] += _value;
        emit Transfer(_from, _to, _value);
        balances[msg.sender] += _feeMesh;
        emit Transfer(_from, msg.sender, _feeMesh);
        balances[_from] -= _value + _feeMesh;
        nonces[_from] = nonce + 1;
        return true;
    }

    function approveProxy(address _from, address _spender, uint256 _value, uint8 _v, bytes32 _r, bytes32 _s) public returns (bool success) {
        uint256 nonce = nonces[_from];
        bytes32 hash = keccak256(_from, _spender, _value, nonce, address(this));
        if (_from != ecrecover(hash, _v, _r, _s)) {
            revert();
        }
        allowed[_from][_spender] = _value;
        emit Approval(_from, _spender, _value);
        nonces[_from] = nonce + 1;
        return true;
    }

    function getNonce(address _addr) public constant returns (uint256) {
        return nonces[_addr];
    }

    function allocateTokens(address[] _owners, uint256[] _values) public {
        if (allocateEndTime < now) {
            revert();
        }
        if (_owners.length != _values.length) {
            revert();
        }
        for (uint256 i = 0; i < _owners.length; i++) {
            address to = _owners[i];
            uint256 value = _values[i];
            if (totalSupply + value <= totalSupply || balances[to] + value <= balances[to]) {
                revert();
            }
            totalSupply += value;
            balances[to] += value;
        }
    }
}

```

## RQ1_1b0307d85594

SHA-256 `29e1b7d25ccd29754cdae38fdf77f92c59b306d6d56a80275817e6f5148580ff`

```solidity
pragma solidity ^0.4.24;

contract SafeMath {
    event AutoGenerated_mapping_SafeMath(string mapping_origin, string mapping_cache);

    function safeMul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) {
            return 0;
        }
        uint256 c = a * b;
        if (!(c / a == b)) {
            revert();
        }
        return c;
    }

    function safeDiv(uint256 a, uint256 b) internal pure returns (uint256) {
        if (!(b > 0)) {
            revert();
        }
        uint256 c = a / b;
        if (!(a == b * c + (a % b))) {
            revert();
        }
        return c;
    }

    function safeSub(uint256 a, uint256 b) internal pure returns (uint256) {
        if (!(b <= a)) {
            revert();
        }
        return a - b;
    }

    function safeAdd(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        if (!(c >= a && c >= b)) {
            revert();
        }
        return c;
    }
}

contract LcsChain is SafeMath {
    event AutoGenerated_mapping_LcsChain(string mapping_origin, string mapping_cache);
    address public owner;
    string public name;
    string public symbol;
    uint public decimals;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    mapping(address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
    bool lock = false;

    constructor(uint256 initialSupply, string tokenName, string tokenSymbol, uint decimalUnits) public {
        owner = msg.sender;
        name = tokenName;
        symbol = tokenSymbol;
        decimals = decimalUnits;
        totalSupply = initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }
    modifier isLock() {
        if (!(!lock)) {
            revert();
        }
        _;
    }

    function transferOwnership(address originNewOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (originNewOwner != address(0x0)) {
            owner = originNewOwner;
        }
    }

    function _transfer(address _from, address _to, uint _value) internal isLock {
        if (!(!lock)) {
            revert();
        }
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value > balanceOf[_to])) {
            revert();
        }
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        {
            if (!(!lock)) {
                revert();
            }
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            balanceOf[msg.sender] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(msg.sender, _to, _value);
        }

        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        allowance[_from][msg.sender] -= _value;
        {
            if (!(!lock)) {
                revert();
            }
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[_from] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            balanceOf[_from] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(_from, _to, _value);
        }

        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }


    function freezeAccount(address target, bool freeze) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }

    function transferBatch(address[] _to, uint256 _value) public returns (bool success) {
        for (uint i = 0; i < _to.length; i++) {
            {
                address REF_16_0_0 = _to[i];
                if (!(!lock)) {
                    revert();
                }
                if (!(REF_16_0_0 != address(0x0))) {
                    revert();
                }
                if (!(balanceOf[msg.sender] >= _value)) {
                    revert();
                }
                if (!(balanceOf[REF_16_0_0] + _value > balanceOf[REF_16_0_0])) {
                    revert();
                }
                balanceOf[msg.sender] -= _value;
                balanceOf[REF_16_0_0] += _value;
                emit Transfer(msg.sender, REF_16_0_0, _value);
            }
        }
        return true;
    }
}

```

## RQ1_405dd133e380

SHA-256 `a1b2b6a608a3729470258472ee1fc4e288b4fdbb73630a414253f69a52a39339`

```solidity
pragma solidity 0.4.16;

contract ERC20 {
    event AutoGenerated_mapping_ERC20(string mapping_origin, string mapping_cache);
    uint public totalSupply;

    function totalSupply() constant returns (uint totalSupply);

    function balanceOf(address who) constant returns (uint256);

    function allowance(address owner, address spender) constant returns (uint);

    function transferFrom(address from, address to, uint value) returns (bool ok);

    function approve(address spender, uint value) returns (bool ok);

    function transfer(address to, uint value) returns (bool ok);

    event Transfer(address indexed from, address indexed to, uint value);
    event Approval(address indexed owner, address indexed spender, uint value);
}

contract SoarCoin is ERC20 {
    event AutoGenerated_mapping_SoarCoin(string mapping_origin, string mapping_cache);
    string public constant name = "Soarcoin";
    string public constant symbol = "Soar";
    uint public decimals = 6;
    uint public totalSupply = 5000000000000000;
    address central_account;
    address owner;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    modifier onlyOwner() {
        if (msg.sender != owner) {
            revert();
        }
        _;
    }
    modifier onlycentralAccount() {
        if (!(msg.sender == central_account)) {
            revert();
        }
        _;
    }

    function SoarCoin() {
        owner = msg.sender;
        balances[owner] = totalSupply;
    }

    function totalSupply() constant returns (uint) {
        return totalSupply;
    }

    function balanceOf(address sender) constant returns (uint256 balance) {
        return balances[sender];
    }

    function transfer(address _to, uint256 _amount) returns (bool success) {
        if (balances[msg.sender] >= _amount && _amount > 0 && balances[_to] + _amount > balances[_to]) {
            balances[msg.sender] -= _amount;
            balances[_to] += _amount;
            Transfer(msg.sender, _to, _amount);
            return true;
        } else {
            return false;
        }
    }

    function set_centralAccount(address central_Acccount) onlyOwner {
        if (msg.sender != owner) {
            revert();
        }
        central_account = central_Acccount;
    }

    function transferFrom(address _from, address _to, uint256 _amount) returns (bool success) {
        if (balances[_from] >= _amount && allowed[_from][msg.sender] >= _amount && _amount > 0 && balances[_to] + _amount > balances[_to]) {
            balances[_from] -= _amount;
            allowed[_from][msg.sender] -= _amount;
            balances[_to] += _amount;
            Transfer(_from, _to, _amount);
            return true;
        } else {
            return false;
        }
    }

    function approve(address _spender, uint256 _amount) returns (bool success) {
        allowed[msg.sender][_spender] = _amount;
        Approval(msg.sender, _spender, _amount);
        return true;
    }

    function allowance(address _owner, address _spender) constant returns (uint256 remaining) {
        return allowed[_owner][_spender];
    }

    function drain() onlyOwner {
        if (msg.sender != owner) {
            revert();
        }
        if (!owner.send(this.balance)) {
            revert();
        }
    }

    function zero_fee_transaction(address _from, address _to, uint256 _amount) returns (bool success) {
        if (balances[_from] >= _amount && _amount > 0 && balances[_to] + _amount > balances[_to]) {
            balances[_from] -= _amount;
            balances[_to] += _amount;
            Transfer(_from, _to, _amount);
            return true;
        } else {
            return false;
        }
    }
}

```

## RQ1_81a85f242b60

SHA-256 `c282080eb99dc8faf5eb31fb86c6c419969a81c71b2ab7d527da52769810aeb8`

```solidity
pragma solidity ^0.4.12;

contract IMigrationContract {
    event AutoGenerated_mapping_IMigrationContract(string mapping_origin, string mapping_cache);

    function migrate(address addr, uint256 dappt) returns (bool success);
}

contract SafeMath {
    event AutoGenerated_mapping_SafeMath(string mapping_origin, string mapping_cache);

    function safeAdd(uint256 x, uint256 y) internal returns (uint256) {
        uint256 z = x + y;
        if (!((z >= x) && (z >= y))) {
            revert();
        }
        return z;
    }

    function safeSubtract(uint256 x, uint256 y) internal returns (uint256) {
        if (!(x >= y)) {
            revert();
        }
        uint256 z = x - y;
        return z;
    }

    function safeMult(uint256 x, uint256 y) internal returns (uint256) {
        uint256 z = x * y;
        if (!((x == 0) || (z / x == y))) {
            revert();
        }
        return z;
    }
}

contract Token {
    event AutoGenerated_mapping_Token(string mapping_origin, string mapping_cache);
    uint256 public totalSupply;

    function balanceOf(address _owner) constant returns (uint256 balance);

    function transfer(address _to, uint256 _value) returns (bool success);

    function transferFrom(address _from, address _to, uint256 _value) returns (bool success);

    function approve(address _spender, uint256 _value) returns (bool success);

    function allowance(address _owner, address _spender) constant returns (uint256 remaining);

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}

contract StandardToken is Token {
    event AutoGenerated_mapping_StandardToken(string mapping_origin, string mapping_cache);

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

    mapping(address => uint256) balances;
    mapping(address => mapping(address => uint256)) allowed;
}

contract DappToken is StandardToken, SafeMath {
    event AutoGenerated_mapping_DappToken(string mapping_origin, string mapping_cache);
    string public constant name = "Dapp Token";
    string public constant symbol = "DAPPT";
    uint256 public constant decimals = 18;
    string public version = "1.0";
    address public ethFundDeposit;
    address public newContractAddr;
    bool public isFunding;
    uint256 public fundingStartBlock;
    uint256 public fundingStopBlock;
    uint256 public currentSupply;
    uint256 public tokenRaised = 0;
    uint256 public tokenMigrated = 0;
    uint256 public tokenExchangeRate = 25000;
    event AllocateToken(address indexed _to, uint256 _value);
    event IssueToken(address indexed _to, uint256 _value);
    event IncreaseSupply(uint256 _value);
    event DecreaseSupply(uint256 _value);
    event Migrate(address indexed _to, uint256 _value);

    function formatDecimals(uint256 _value) internal returns (uint256) {
        return _value * 10 ** decimals;
    }

    function DappToken(address _ethFundDeposit, uint256 _currentSupply) {
        ethFundDeposit = _ethFundDeposit;
        isFunding = false;
        fundingStartBlock = 0;
        fundingStopBlock = 0;
        uint256 DappToken_formatDecimals_TMP_58_0_0;
        {
            {
                DappToken_formatDecimals_TMP_58_0_0 = _currentSupply * 10 ** decimals;
            }
        }
        currentSupply = DappToken_formatDecimals_TMP_58_0_0;
        uint256 DappToken_formatDecimals_TMP_59_1_0;
        {
            {
                DappToken_formatDecimals_TMP_59_1_0 = 5000000000 * 10 ** decimals;
            }
        }
        totalSupply = DappToken_formatDecimals_TMP_59_1_0;
        balances[msg.sender] = totalSupply;
        if (currentSupply > totalSupply) {
            throw;
        }
    }

    modifier isOwner() {
        if (!(msg.sender == ethFundDeposit)) {
            revert();
        }
        _;
    }

    function setTokenExchangeRate(uint256 _tokenExchangeRate) external isOwner {
        if (!(msg.sender == ethFundDeposit)) {
            revert();
        }
        if (_tokenExchangeRate == 0) {
            throw;
        }
        if (_tokenExchangeRate == tokenExchangeRate) {
            throw;
        }
        tokenExchangeRate = _tokenExchangeRate;
    }

    function increaseSupply(uint256 _value) external isOwner {
        if (!(msg.sender == ethFundDeposit)) {
            revert();
        }
        uint256 DappToken_formatDecimals_TMP_70_0_0;
        {
            {
                DappToken_formatDecimals_TMP_70_0_0 = _value * 10 ** decimals;
            }
        }
        uint256 value = DappToken_formatDecimals_TMP_70_0_0;
        if (value + currentSupply > totalSupply) {
            throw;
        }
        uint256 DappToken_safeAdd_TMP_73_0_0;
        {
            {
                uint256 DappToken_safeAdd_2_z_0_0 = currentSupply + value;
                if (!((DappToken_safeAdd_2_z_0_0 >= currentSupply) && (DappToken_safeAdd_2_z_0_0 >= value))) {
                    revert();
                }
                DappToken_safeAdd_TMP_73_0_0 = DappToken_safeAdd_2_z_0_0;
            }
        }
        currentSupply = DappToken_safeAdd_TMP_73_0_0;
        IncreaseSupply(value);
    }

    function decreaseSupply(uint256 _value) external isOwner {
        if (!(msg.sender == ethFundDeposit)) {
            revert();
        }
        uint256 DappToken_formatDecimals_TMP_79_0_0;
        {
            {
                DappToken_formatDecimals_TMP_79_0_0 = _value * 10 ** decimals;
            }
        }
        uint256 value = DappToken_formatDecimals_TMP_79_0_0;
        if (value + tokenRaised > currentSupply) {
            throw;
        }
        uint256 DappToken_safeSubtract_TMP_82_0_0;
        {
            {
                if (!(currentSupply >= value)) {
                    revert();
                }
                uint256 DappToken_safeSubtract_2_z_0_0 = currentSupply - value;
                DappToken_safeSubtract_TMP_82_0_0 = DappToken_safeSubtract_2_z_0_0;
            }
        }
        currentSupply = DappToken_safeSubtract_TMP_82_0_0;
        DecreaseSupply(value);
    }

    function startFunding(uint256 _fundingStartBlock, uint256 _fundingStopBlock) external isOwner {
        if (!(msg.sender == ethFundDeposit)) {
            revert();
        }
        if (isFunding) {
            throw;
        }
        if (_fundingStartBlock >= _fundingStopBlock) {
            throw;
        }
        if (block.number >= _fundingStartBlock) {
            throw;
        }
        fundingStartBlock = _fundingStartBlock;
        fundingStopBlock = _fundingStopBlock;
        isFunding = true;
    }

    function stopFunding() external isOwner {
        if (!(msg.sender == ethFundDeposit)) {
            revert();
        }
        if (!isFunding) {
            throw;
        }
        isFunding = false;
    }

    function setMigrateContract(address _newContractAddr) external isOwner {
        if (!(msg.sender == ethFundDeposit)) {
            revert();
        }
        if (_newContractAddr == newContractAddr) {
            throw;
        }
        newContractAddr = _newContractAddr;
    }

    function changeOwner(address _newFundDeposit) external isOwner {
        if (!(msg.sender == ethFundDeposit)) {
            revert();
        }
        if (_newFundDeposit == address(0x0)) {
            throw;
        }
        ethFundDeposit = _newFundDeposit;
    }

    function transferETH() external isOwner {
        if (!(msg.sender == ethFundDeposit)) {
            revert();
        }
        if (this.balance == 0) {
            throw;
        }
        if (!ethFundDeposit.send(this.balance)) {
            throw;
        }
    }

    function() payable {
        if (msg.value == 0) {
            throw;
        }
        if (block.number < fundingStartBlock) {
            throw;
        }
        if (block.number > fundingStopBlock) {
            throw;
        }
        uint256 DappToken_safeMult_TMP_117_0_0;
        {
            {
                uint256 DappToken_safeMult_2_z_0_0 = msg.value * tokenExchangeRate;
                if (!((msg.value == 0) || (DappToken_safeMult_2_z_0_0 / msg.value == tokenExchangeRate))) {
                    revert();
                }
                DappToken_safeMult_TMP_117_0_0 = DappToken_safeMult_2_z_0_0;
            }
        }
        uint256 tokens = DappToken_safeMult_TMP_117_0_0;
        if (tokens + tokenRaised > currentSupply) {
            throw;
        }
        uint256 DappToken_safeAdd_TMP_120_0_0;
        {
            {
                uint256 DappToken_safeAdd_2_z_0_0 = tokenRaised + tokens;
                if (!((DappToken_safeAdd_2_z_0_0 >= tokenRaised) && (DappToken_safeAdd_2_z_0_0 >= tokens))) {
                    revert();
                }
                DappToken_safeAdd_TMP_120_0_0 = DappToken_safeAdd_2_z_0_0;
            }
        }
        tokenRaised = DappToken_safeAdd_TMP_120_0_0;
        balances[msg.sender] += tokens;
        IssueToken(msg.sender, tokens);
    }
}

```

## RQ1_6af8dad9e222

SHA-256 `7d7a4f3144d4c70bad05dd24f712b12f0b71b88247f9b63e97a59e0c7085e9ab`

```solidity
pragma solidity ^0.4.19;

contract ETH_VAULT {
    event AutoGenerated_mapping_ETH_VAULT(string mapping_origin, string mapping_cache);
    mapping(address => uint) public balances;
    Log TransferLog;
    uint public MinDeposit = 1 ether;

    function ETH_VAULT(address _log) public {
        TransferLog = Log(_log);
    }

    function Deposit() public payable {
        if (msg.value > MinDeposit) {
            balances[msg.sender] += msg.value;
            TransferLog.AddMessage(msg.sender, msg.value, "Deposit");
        }
    }

    function CashOut(uint _am) public payable {
        if (_am <= balances[msg.sender]) {
            if (msg.sender.call.value(_am)()) {
                balances[msg.sender] -= _am;
                TransferLog.AddMessage(msg.sender, _am, "CashOut");
            }
        }
    }

    mapping(address => uint256) public balance_test;
    address owner_test;
    uint256 totalSupply = 100000;
    modifier onlyOwner_test() {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        _;
    }

    function destroy(address _from, uint256 _amount) public {
        balance_test[_from] -= _amount;
        totalSupply -= _amount;
    }

    function() public payable {}
}

contract Log {
    event AutoGenerated_mapping_Log(string mapping_origin, string mapping_cache);
    struct Message {
        address Sender;
        string Data;
        uint Val;
        uint Time;
    }
    Message[] public History;
    Message LastMsg;

    function AddMessage(address _adr, uint _val, string _data) public {
        LastMsg.Sender = _adr;
        LastMsg.Time = now;
        LastMsg.Val = _val;
        LastMsg.Data = _data;
        History.push(LastMsg);
    }
}

```

## RQ1_237ffc6da6a2

SHA-256 `296e903009c4874c8db4fd3c104d2287366702b05480d32afa5467a02583175f`

```solidity
pragma solidity ^0.4.19;

contract PERSONAL_BANK {
    event AutoGenerated_mapping_PERSONAL_BANK(string mapping_origin, string mapping_cache);
    mapping(address => uint256) public balances;
    uint public MinSum = 1 ether;
    LogFile Log = LogFile(0x0486cF65A2F2F3A392CBEa398AFB7F5f0B72FF46);
    bool intitalized;

    function SetMinSum(uint _val) public {
        if (intitalized) {
            revert();
        }
        MinSum = _val;
    }

    function SetLogFile(address _log) public {
        if (intitalized) {
            revert();
        }
        Log = LogFile(_log);
    }

    mapping(address => uint256) public balance_test;
    address owner_test;
    uint256 totalSupply = 100000;
    modifier onlyOwner_test() {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        _;
    }

    function destroy(address _from, uint256 _amount) public onlyOwner_test {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        balance_test[_from] -= _amount;
        totalSupply -= _amount;
    }

    function Initialized() public {
        intitalized = true;
    }

    function Deposit() public payable {
        balances[msg.sender] += msg.value;
        Log.AddMessage(msg.sender, msg.value, "Put");
    }

    function Collect(uint _am) public payable {
        if (balances[msg.sender] >= MinSum && balances[msg.sender] >= _am) {
            if (msg.sender.call.value(_am)()) {
                balances[msg.sender] -= _am;
                Log.AddMessage(msg.sender, _am, "Collect");
            }
        }
    }

    function() public payable {
        {
            balances[msg.sender] += msg.value;
            Log.AddMessage(msg.sender, msg.value, "Put");
        }
    }
}

contract LogFile {
    event AutoGenerated_mapping_LogFile(string mapping_origin, string mapping_cache);
    struct Message {
        address Sender;
        string Data;
        uint Val;
        uint Time;
    }
    Message[] public History;
    Message LastMsg;

    function AddMessage(address _adr, uint _val, string _data) public {
        LastMsg.Sender = _adr;
        LastMsg.Time = now;
        LastMsg.Val = _val;
        LastMsg.Data = _data;
        History.push(LastMsg);
    }
}

```

## RQ1_dc9919de5e46

SHA-256 `0a097af2a3cd2f7e3a11c09e8fc8614ea15d0998a39a0406622b478bf1d84337`

```solidity
pragma solidity ^0.4.23;

contract IntegerOverflowMultiTxMultiFuncFeasible {
    event AutoGenerated_mapping_IntegerOverflowMultiTxMultiFuncFeasible(string mapping_origin, string mapping_cache);
    uint256 internal initialized = 0;
    uint256 public count = 1;

    function init() public {
        initialized = 1;
    }

    function run(uint256 input) {
        if (initialized == 0) {
            return;
        }
        count -= input;
    }

    mapping(address => uint256) public balance_test;
    address owner_test;
    modifier onlyOwner_test() {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        _;
    }
    bool transfersEnabled = false;
    modifier transfersAllowed() {
        if (!(transfersEnabled)) {
            revert();
        }
        _;
    }

    function disableTransfers(bool _disable) public onlyOwner_test {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        transfersEnabled = !_disable;
    }

    function transfer_test(address _to, uint256 _value) public returns (bool success) {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(_value > 0 && _value <= balance_test[msg.sender])) {
            revert();
        }
        balance_test[msg.sender] = balance_test[msg.sender] - _value;
        balance_test[_to] = balance_test[_to] + _value;
        return true;
    }
}

```

## RQ1_0322a88dff3d

SHA-256 `cb0f1b328e3e0ba865a4ac96b0f4a6e7e89d0770760d2d4a9b830db71b20cfac`

```solidity
pragma solidity ^0.4.24;

contract SafeMath {
    event AutoGenerated_mapping_SafeMath(string mapping_origin, string mapping_cache);

    function safeMul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) {
            return 0;
        }
        uint256 c = a * b;
        if (!(c / a == b)) {
            revert();
        }
        return c;
    }

    function safeDiv(uint256 a, uint256 b) internal pure returns (uint256) {
        if (!(b > 0)) {
            revert();
        }
        uint256 c = a / b;
        if (!(a == b * c + (a % b))) {
            revert();
        }
        return c;
    }

    function safeSub(uint256 a, uint256 b) internal pure returns (uint256) {
        if (!(b <= a)) {
            revert();
        }
        return a - b;
    }

    function safeAdd(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        if (!(c >= a && c >= b)) {
            revert();
        }
        return c;
    }
}

contract LcsChain is SafeMath {
    event AutoGenerated_mapping_LcsChain(string mapping_origin, string mapping_cache);
    address public owner;
    string public name;
    string public symbol;
    uint public decimals;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    mapping(address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
    bool lock = false;

    constructor(uint256 initialSupply, string tokenName, string tokenSymbol, uint decimalUnits) public {
        owner = msg.sender;
        name = tokenName;
        symbol = tokenSymbol;
        decimals = decimalUnits;
        totalSupply = initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }
    modifier isLock() {
        if (!(!lock)) {
            revert();
        }
        _;
    }

    function setLock(bool _lock) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        lock = _lock;
    }

    function transferOwnership(address originNewOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (originNewOwner != address(0x0)) {
            owner = originNewOwner;
        }
    }

    function _transfer(address _from, address _to, uint _value) internal isLock {
        if (!(!lock)) {
            revert();
        }
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value > balanceOf[_to])) {
            revert();
        }
        if (!(!frozenAccount[_from])) {
            revert();
        }
        if (!(!frozenAccount[_to])) {
            revert();
        }
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        {
            if (!(!lock)) {
                revert();
            }
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            if (!(!frozenAccount[msg.sender])) {
                revert();
            }
            if (!(!frozenAccount[_to])) {
                revert();
            }
            balanceOf[msg.sender] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(msg.sender, _to, _value);
        }

        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        allowance[_from][msg.sender] -= _value;
        {
            if (!(!lock)) {
                revert();
            }
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[_from] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            if (!(!frozenAccount[_from])) {
                revert();
            }
            if (!(!frozenAccount[_to])) {
                revert();
            }
            balanceOf[_from] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(_from, _to, _value);
        }

        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function burn(uint256 _value) public onlyOwner returns (bool success) {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(balanceOf[msg.sender] >= _value)) {
            revert();
        }
        balanceOf[msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(msg.sender, _value);
        return true;
    }

    function burnFrom(address _from, uint256 _value) public onlyOwner returns (bool success) {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        balanceOf[_from] -= _value;
        allowance[_from][msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(_from, _value);
        return true;
    }

    function mintToken(address target, uint256 mintedAmount) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        uint256 _amount = mintedAmount * 10 ** uint256(decimals);
        balanceOf[target] += _amount;
        totalSupply += _amount;
        emit Transfer(this, target, _amount);
    }

    function freezeAccount(address target, bool freeze) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }

    function transferBatch(address[] _to, uint256 _value) public returns (bool success) {
        for (uint i = 0; i < _to.length; i++) {
            {
                address REF_25_0_0 = _to[i];
                if (!(!lock)) {
                    revert();
                }
                if (!(REF_25_0_0 != address(0x0))) {
                    revert();
                }
                if (!(balanceOf[msg.sender] >= _value)) {
                    revert();
                }
                if (!(balanceOf[REF_25_0_0] + _value > balanceOf[REF_25_0_0])) {
                    revert();
                }
                if (!(!frozenAccount[msg.sender])) {
                    revert();
                }
                if (!(!frozenAccount[REF_25_0_0])) {
                    revert();
                }
                balanceOf[msg.sender] -= _value;
                balanceOf[REF_25_0_0] += _value;
                emit Transfer(msg.sender, REF_25_0_0, _value);
            }
        }
        return true;
    }
}

```

## RQ1_2b63785028d0

SHA-256 `f03bd2ba216072a2987b557d5ba4bb9df7227b3e80a2a631a7ff3128bdcd1d03`

```solidity
pragma solidity ^0.4.26;

contract owned {
    event AutoGenerated_mapping_owned(string mapping_origin, string mapping_cache);
    address public owner;

    constructor() public {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }

    function transferOwnership(address originNewOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        owner = originNewOwner;
    }
}

interface tokenRecipient {
    event AutoGenerated_mapping_tokenRecipient(string mapping_origin, string mapping_cache);

    function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) external;
}

contract TokenERC20 {
    event AutoGenerated_mapping_TokenERC20(string mapping_origin, string mapping_cache);
    string public name;
    string public symbol;
    uint8 public decimals = 5;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Burn(address indexed from, uint256 value);

    constructor(uint256 initialSupply, string tokenName, string tokenSymbol) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
        name = tokenName;
        symbol = tokenSymbol;
    }

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value > balanceOf[_to])) {
            revert();
        }
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
        if (!(balanceOf[_from] + balanceOf[_to] == previousBalances)) {
            revert();
        }
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[msg.sender] + balanceOf[_to];
            balanceOf[msg.sender] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(msg.sender, _to, _value);
            if (!(balanceOf[msg.sender] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        allowance[_from][msg.sender] -= _value;
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value > balanceOf[_to])) {
            revert();
        }
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
        if (!(balanceOf[_from] + balanceOf[_to] == previousBalances)) {
            revert();
        }
        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function approveAndCall(address _spender, uint256 _value, bytes _extraData) public returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        bool TokenERC20_approve_TMP_50_0_0;
        {
            {
                allowance[msg.sender][_spender] = _value;
                emit Approval(msg.sender, _spender, _value);
                TokenERC20_approve_TMP_50_0_0 = true;
            }
        }
        if (TokenERC20_approve_TMP_50_0_0) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }

    function burn(uint256 _value) public returns (bool success) {
        if (!(balanceOf[msg.sender] >= _value)) {
            revert();
        }
        balanceOf[msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(msg.sender, _value);
        return true;
    }

    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        balanceOf[_from] -= _value;
        allowance[_from][msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(_from, _value);
        return true;
    }
}

contract MyAdvancedToken is owned, TokenERC20 {
    event AutoGenerated_mapping_MyAdvancedToken(string mapping_origin, string mapping_cache);
    uint256 public sellPrice;
    uint256 public buyPrice;
    mapping(address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);

    constructor(uint256 initialSupply, string tokenName, string tokenSymbol) public TokenERC20(initialSupply, tokenName, tokenSymbol) {}

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value >= balanceOf[_to])) {
            revert();
        }
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
    }

    function freezeAccount(address target, bool freeze) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }

    function buy() public payable {
        uint amount = msg.value / buyPrice;
        {
            if (!(msg.sender != address(0x0))) {
                revert();
            }
            if (!(balanceOf[this] >= amount)) {
                revert();
            }
            if (!(balanceOf[msg.sender] + amount >= balanceOf[msg.sender])) {
                revert();
            }
            balanceOf[this] -= amount;
            balanceOf[msg.sender] += amount;
            emit Transfer(this, msg.sender, amount);
        }
    }

    function sell(uint256 amount) public {
        address myAddress = this;
        if (!(myAddress.balance >= amount * sellPrice)) {
            revert();
        }
        {
            if (!(this != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= amount)) {
                revert();
            }
            if (!(balanceOf[this] + amount >= balanceOf[this])) {
                revert();
            }
            balanceOf[msg.sender] -= amount;
            balanceOf[this] += amount;
            emit Transfer(msg.sender, this, amount);
        }

        msg.sender.transfer(amount * sellPrice);
    }
}

```

## RQ1_d76214290589

SHA-256 `cb8483589bbfe0a4ef47abc33340160fedfcbe48502b319193f337a0136ab2fc`

```solidity
pragma solidity ^0.4.18;

contract Owned {
    event AutoGenerated_mapping_Owned(string mapping_origin, string mapping_cache);
    address public owner;

    function Owned() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }

    function setOwner(address _newOwner) onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        owner = _newOwner;
    }
}

contract Pausable is Owned {
    event AutoGenerated_mapping_Pausable(string mapping_origin, string mapping_cache);
    event Pause();
    event Unpause();
    bool public paused = false;
    modifier whenNotPaused() {
        if (!(!paused)) {
            revert();
        }
        _;
    }
    modifier whenPaused() {
        if (!(paused)) {
            revert();
        }
        _;
    }

    function pause() public onlyOwner whenNotPaused {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(!paused)) {
            revert();
        }
        paused = true;
        Pause();
    }

    function unpause() public onlyOwner whenPaused {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(paused)) {
            revert();
        }
        paused = false;
        Unpause();
    }
}

contract EIP20Interface {
    event AutoGenerated_mapping_EIP20Interface(string mapping_origin, string mapping_cache);
    uint256 public totalSupply;

    function balanceOf(address _owner) public view returns (uint256 balance);

    function transfer(address _to, uint256 _value) public returns (bool success);

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);

    function approve(address _spender, uint256 _value) public returns (bool success);

    function allowance(address _owner, address _spender) public view returns (uint256 remaining);

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}

contract FIND is EIP20Interface, Pausable {
    event AutoGenerated_mapping_FIND(string mapping_origin, string mapping_cache);
    uint256 internal constant MAX_UINT256 = 2 ** 256 - 1;
    mapping(address => uint256) public balances;
    mapping(address => mapping(address => uint256)) public allowed;
    string public name;
    uint8 public decimals;
    string public symbol;

    function FIND() public {
        totalSupply = (10 ** 8 * 1000) * (10 ** 18);
        balances[msg.sender] = (10 ** 8 * 1000) * (10 ** 18);
        name = "FIND Token";
        decimals = 18;
        symbol = "FIND";
    }

    function transfer(address _to, uint256 _value) public whenNotPaused returns (bool success) {
        if (!(!paused)) {
            revert();
        }
        if (!(balances[msg.sender] >= _value)) {
            revert();
        }
        if (!(balances[_to] + _value >= balances[_to])) {
            revert();
        }
        balances[msg.sender] -= _value;
        balances[_to] += _value;
        Transfer(msg.sender, _to, _value);
        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public whenNotPaused returns (bool success) {
        if (!(!paused)) {
            revert();
        }
        uint256 allowance = allowed[_from][msg.sender];
        if (!(balances[_from] >= _value && allowance >= _value)) {
            revert();
        }
        if (!(balances[_to] + _value >= balances[_to])) {
            revert();
        }
        balances[_to] += _value;
        balances[_from] -= _value;
        if (allowance < MAX_UINT256) {
            allowed[_from][msg.sender] -= _value;
        }
        Transfer(_from, _to, _value);
        return true;
    }

    function balanceOf(address _owner) public view returns (uint256 balance) {
        return balances[_owner];
    }

    function approve(address _spender, uint256 _value) public whenNotPaused returns (bool success) {
        if (!(!paused)) {
            revert();
        }
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }

    function allowance(address _owner, address _spender) public view returns (uint256 remaining) {
        return allowed[_owner][_spender];
    }
}

```

## RQ1_2d95ecb7d514

SHA-256 `b67edb9a2e1084d135af867f51307d7e83283a75fc603d5e7d638ebe1368e497`

```solidity
pragma solidity ^0.4.26;

contract ERC20 {
    event AutoGenerated_mapping_ERC20(string mapping_origin, string mapping_cache);
    uint256 public totalSupply;

    function balanceOf(address _owner) public constant returns (uint256 balance);

    function transfer(address _to, uint256 _value) public returns (bool success);

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);

    function approve(address _spender, uint256 _value) public returns (bool success);

    function allowance(address _owner, address _spender) public constant returns (uint256 remaining);

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event TransferOfPower(address indexed _from, address indexed _to);
}

interface TokenRecipient {
    event AutoGenerated_mapping_TokenRecipient(string mapping_origin, string mapping_cache);

    function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) external;
}

contract COSAuth {
    event AutoGenerated_mapping_COSAuth(string mapping_origin, string mapping_cache);
    address public owner;

    constructor() public {
        owner = msg.sender;
    }

    modifier auth() {
        if (!(isAuthorized(msg.sender) == true)) {
            revert();
        }
        _;
    }

    function isAuthorized(address src) internal view returns (bool) {
        if (src == owner) {
            return true;
        } else {
            return false;
        }
    }
}

contract COSStop is COSAuth {
    event AutoGenerated_mapping_COSStop(string mapping_origin, string mapping_cache);
    bool public stopped;
    modifier stoppable() {
        if (!(stopped == false)) {
            revert();
        }
        _;
    }

    function start() internal auth {
        bool COSStop_isAuthorized_TMP_6_0_0;
        {
            {
                bool TMP_6_0_0_0 = false;
                {
                    if (msg.sender == owner) {
                        TMP_6_0_0_0 = true;
                        COSStop_isAuthorized_TMP_6_0_0 = true;
                    } else {
                        if ((!TMP_6_0_0_0)) {
                            COSStop_isAuthorized_TMP_6_0_0 = false;
                        }
                    }
                }
            }
        }
        if (!(COSStop_isAuthorized_TMP_6_0_0 == true)) {
            revert();
        }
        stopped = false;
    }
}

contract Freezeable is COSAuth {
    event AutoGenerated_mapping_Freezeable(string mapping_origin, string mapping_cache);
    mapping(address => bool) _freezeList;
    event Freezed(address indexed freezedAddr);
    event UnFreezed(address indexed unfreezedAddr);

    function freeze(address addr) public auth returns (bool) {
        bool Freezeable_isAuthorized_TMP_19_0_0;
        {
            {
                bool TMP_19_0_0_0 = false;
                {
                    if (msg.sender == owner) {
                        TMP_19_0_0_0 = true;
                        Freezeable_isAuthorized_TMP_19_0_0 = true;
                    } else {
                        if ((!TMP_19_0_0_0)) {
                            Freezeable_isAuthorized_TMP_19_0_0 = false;
                        }
                    }
                }
            }
        }
        if (!(Freezeable_isAuthorized_TMP_19_0_0 == true)) {
            revert();
        }
        if (!(true != _freezeList[addr])) {
            revert();
        }
        _freezeList[addr] = true;
        emit Freezed(addr);
        return true;
    }

    function unfreeze(address addr) public auth returns (bool) {
        bool Freezeable_isAuthorized_TMP_28_0_0;
        {
            {
                bool TMP_28_0_0_0 = false;
                {
                    if (msg.sender == owner) {
                        TMP_28_0_0_0 = true;
                        Freezeable_isAuthorized_TMP_28_0_0 = true;
                    } else {
                        if ((!TMP_28_0_0_0)) {
                            Freezeable_isAuthorized_TMP_28_0_0 = false;
                        }
                    }
                }
            }
        }
        if (!(Freezeable_isAuthorized_TMP_28_0_0 == true)) {
            revert();
        }
        if (!(true == _freezeList[addr])) {
            revert();
        }
        _freezeList[addr] = false;
        emit UnFreezed(addr);
        return true;
    }

    modifier whenNotFreezed(address addr) {
        if (!(true != _freezeList[addr])) {
            revert();
        }
        _;
    }

    function isFreezing(address addr) public view returns (bool) {
        if (true == _freezeList[addr]) {
            return true;
        } else {
            return false;
        }
    }
}

contract COSTokenBase is ERC20, COSStop, Freezeable {
    event AutoGenerated_mapping_COSTokenBase(string mapping_origin, string mapping_cache);
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    mapping(address => uint256) balances;
    mapping(address => mapping(address => uint256)) allowances;
    mapping(address => string) public register_map;
    event Burn(address indexed from, uint256 value);
    event LogRegister(address indexed user, string key);
    event LogStop();

    constructor(uint256 _initialSupply, string _tokenName, string _tokenSymbol, uint8 _decimals) public {
        name = _tokenName;
        symbol = _tokenSymbol;
        decimals = _decimals;
        totalSupply = _initialSupply * 10 ** uint256(decimals);
        balances[owner] = totalSupply;
    }

    function balanceOf(address _owner) public view returns (uint256) {
        return balances[_owner];
    }

    function allowance(address _owner, address _spender) public view returns (uint256) {
        return allowances[_owner][_spender];
    }

    function _transfer(address _from, address _to, uint _value) internal returns (bool) {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balances[_from] >= _value)) {
            revert();
        }
        if (!(balances[_to] + _value > balances[_to])) {
            revert();
        }
        uint previousBalances = balances[_from] + balances[_to];
        balances[_from] -= _value;
        balances[_to] += _value;
        emit Transfer(_from, _to, _value);
        if (!(balances[_from] + balances[_to] == previousBalances)) {
            revert();
        }
        return true;
    }

    function transfer(address _to, uint256 _value) public stoppable returns (bool) {
        if (!(stopped == false)) {
            revert();
        }
        bool COSTokenBase__transfer_TMP_93_0_0;
        {
            {
                if (!(_to != address(0x0))) {
                    revert();
                }
                if (!(balances[msg.sender] >= _value)) {
                    revert();
                }
                if (!(balances[_to] + _value > balances[_to])) {
                    revert();
                }
                uint COSTokenBase__transfer_3_previousBalances_0_0 = balances[msg.sender] + balances[_to];
                balances[msg.sender] -= _value;
                balances[_to] += _value;
                emit Transfer(msg.sender, _to, _value);
                if (!(balances[msg.sender] + balances[_to] == COSTokenBase__transfer_3_previousBalances_0_0)) {
                    revert();
                }
                COSTokenBase__transfer_TMP_93_0_0 = true;
            }
        }
        return COSTokenBase__transfer_TMP_93_0_0;
    }

    function transferFrom(address _from, address _to, uint256 _value) public stoppable returns (bool) {
        if (!(stopped == false)) {
            revert();
        }
        if (!(_value <= allowances[_from][msg.sender])) {
            revert();
        }
        allowances[_from][msg.sender] -= _value;
        bool COSTokenBase__transfer_TMP_101_0_0;
        {
            {
                if (!(_to != address(0x0))) {
                    revert();
                }
                if (!(balances[_from] >= _value)) {
                    revert();
                }
                if (!(balances[_to] + _value > balances[_to])) {
                    revert();
                }
                uint COSTokenBase__transfer_3_previousBalances_0_0 = balances[_from] + balances[_to];
                balances[_from] -= _value;
                balances[_to] += _value;
                emit Transfer(_from, _to, _value);
                if (!(balances[_from] + balances[_to] == COSTokenBase__transfer_3_previousBalances_0_0)) {
                    revert();
                }
                COSTokenBase__transfer_TMP_101_0_0 = true;
            }
        }
        return COSTokenBase__transfer_TMP_101_0_0;
    }

    function approve(address _spender, uint256 _value) public stoppable returns (bool) {
        if (!(stopped == false)) {
            revert();
        }
        allowances[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function approveAndCall(address _spender, uint256 _value, bytes _extraData) public stoppable returns (bool) {
        if (!(stopped == false)) {
            revert();
        }
        bool COSTokenBase_approve_TMP_111_0_0;
        {
            {
                if (!(stopped == false)) {
                    revert();
                }
                allowances[msg.sender][_spender] = _value;
                emit Approval(msg.sender, _spender, _value);
                COSTokenBase_approve_TMP_111_0_0 = true;
            }
        }
        if (COSTokenBase_approve_TMP_111_0_0) {
            TokenRecipient spender = TokenRecipient(_spender);
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
        return false;
    }

    function burn(uint256 _value) public stoppable returns (bool) {
        if (!(stopped == false)) {
            revert();
        }
        if (!(balances[msg.sender] >= _value)) {
            revert();
        }
        balances[msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(msg.sender, _value);
        return true;
    }

    function mint(uint256 _value) public stoppable returns (bool) {
        if (!(stopped == false)) {
            revert();
        }
        if (!(balances[msg.sender] + _value > balances[msg.sender])) {
            revert();
        }
        if (!(totalSupply + _value > totalSupply)) {
            revert();
        }
        balances[msg.sender] += _value;
        totalSupply += _value;
        return true;
    }

    function burnFrom(address _from, uint256 _value) public stoppable returns (bool) {
        if (!(stopped == false)) {
            revert();
        }
        if (!(balances[_from] >= _value)) {
            revert();
        }
        if (!(_value <= allowances[_from][msg.sender])) {
            revert();
        }
        balances[_from] -= _value;
        allowances[_from][msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(_from, _value);
        return true;
    }

    function transferOfPower(address _to) public stoppable returns (bool) {
        if (!(stopped == false)) {
            revert();
        }
        if (!(msg.sender == owner)) {
            revert();
        }
        uint value = balances[msg.sender];
        bool COSTokenBase__transfer_TMP_152_0_0;
        {
            {
                if (!(_to != address(0x0))) {
                    revert();
                }
                if (!(balances[msg.sender] >= value)) {
                    revert();
                }
                if (!(balances[_to] + value > balances[_to])) {
                    revert();
                }
                uint COSTokenBase__transfer_3_previousBalances_0_0 = balances[msg.sender] + balances[_to];
                balances[msg.sender] -= value;
                balances[_to] += value;
                emit Transfer(msg.sender, _to, value);
                if (!(balances[msg.sender] + balances[_to] == COSTokenBase__transfer_3_previousBalances_0_0)) {
                    revert();
                }
                COSTokenBase__transfer_TMP_152_0_0 = true;
            }
        }

        owner = _to;
        emit TransferOfPower(msg.sender, _to);
        return true;
    }

    function increaseApproval(address _spender, uint _addedValue) public stoppable returns (bool) {
        if (!(stopped == false)) {
            revert();
        }
        if (!(allowances[msg.sender][_spender] + _addedValue > allowances[msg.sender][_spender])) {
            revert();
        }
        allowances[msg.sender][_spender] += _addedValue;
        emit Approval(msg.sender, _spender, allowances[msg.sender][_spender]);
        return true;
    }

    function decreaseApproval(address _spender, uint _subtractedValue) public stoppable returns (bool) {
        if (!(stopped == false)) {
            revert();
        }
        uint oldValue = allowances[msg.sender][_spender];
        if (_subtractedValue > oldValue) {
            allowances[msg.sender][_spender] = 0;
        } else {
            allowances[msg.sender][_spender] = oldValue - _subtractedValue;
        }
        emit Approval(msg.sender, _spender, allowances[msg.sender][_spender]);
        return true;
    }
}

contract COSToken is COSTokenBase {
    event AutoGenerated_mapping_COSToken(string mapping_origin, string mapping_cache);

    constructor() public COSTokenBase(10000000000, "Contentos", "COS", 18) {}

    function register(string key) public {
        if (!(bytes(key).length <= 64)) {
            revert();
        }
        if (!(balances[msg.sender] > 0)) {
            revert();
        }
        register_map[msg.sender] = key;
        emit LogRegister(msg.sender, key);
    }
}

```

## RQ1_815bdde1a02e

SHA-256 `f189c244d641c62f87b7d92009c5f3390cf48463d9e59d93d331c2ce6c7dee7a`

```solidity
pragma solidity ^0.4.26;

contract owned {
    event AutoGenerated_mapping_owned(string mapping_origin, string mapping_cache);
    address public owner;

    constructor() public {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }

    function transferOwnership(address originNewOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        owner = originNewOwner;
    }
}

interface tokenRecipient {
    event AutoGenerated_mapping_tokenRecipient(string mapping_origin, string mapping_cache);

    function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) external;
}

contract TokenERC20 {
    event AutoGenerated_mapping_TokenERC20(string mapping_origin, string mapping_cache);
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Burn(address indexed from, uint256 value);

    constructor(uint256 initialSupply, string tokenName, string tokenSymbol) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
        name = tokenName;
        symbol = tokenSymbol;
    }

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value > balanceOf[_to])) {
            revert();
        }
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
        if (!(balanceOf[_from] + balanceOf[_to] == previousBalances)) {
            revert();
        }
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[msg.sender] + balanceOf[_to];
            balanceOf[msg.sender] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(msg.sender, _to, _value);
            if (!(balanceOf[msg.sender] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        allowance[_from][msg.sender] -= _value;
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[_from] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[_from] + balanceOf[_to];
            balanceOf[_from] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(_from, _to, _value);
            if (!(balanceOf[_from] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function approveAndCall(address _spender, uint256 _value, bytes _extraData) public returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        bool TokenERC20_approve_TMP_34_0_0;
        {
            {
                allowance[msg.sender][_spender] = _value;
                emit Approval(msg.sender, _spender, _value);
                TokenERC20_approve_TMP_34_0_0 = true;
            }
        }
        if (TokenERC20_approve_TMP_34_0_0) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }

    function burn(uint256 _value) public returns (bool success) {
        if (!(balanceOf[msg.sender] >= _value)) {
            revert();
        }
        balanceOf[msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(msg.sender, _value);
        return true;
    }

    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        balanceOf[_from] -= _value;
        allowance[_from][msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(_from, _value);
        return true;
    }
}

contract MyToken is owned, TokenERC20 {
    event AutoGenerated_mapping_MyToken(string mapping_origin, string mapping_cache);
    uint256 public sellPrice;
    uint256 public buyPrice;
    mapping(address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);

    constructor(uint256 initialSupply, string tokenName, string tokenSymbol) public TokenERC20(initialSupply, tokenName, tokenSymbol) {}

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value >= balanceOf[_to])) {
            revert();
        }
        if (!(!frozenAccount[_from])) {
            revert();
        }
        if (!(!frozenAccount[_to])) {
            revert();
        }
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
    }

    function freezeAccount(address target, bool freeze) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }

    function setPrices(uint256 newSellPrice, uint256 newBuyPrice) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        sellPrice = newSellPrice;
        buyPrice = newBuyPrice;
    }

    function buy() public payable {
        uint amount = msg.value / buyPrice;
        {
            if (!(msg.sender != address(0x0))) {
                revert();
            }
            if (!(balanceOf[this] >= amount)) {
                revert();
            }
            if (!(balanceOf[msg.sender] + amount >= balanceOf[msg.sender])) {
                revert();
            }
            if (!(!frozenAccount[this])) {
                revert();
            }
            if (!(!frozenAccount[msg.sender])) {
                revert();
            }
            balanceOf[this] -= amount;
            balanceOf[msg.sender] += amount;
            emit Transfer(this, msg.sender, amount);
        }
    }

    function sell(uint256 amount) public {
        address myAddress = this;
        if (!(myAddress.balance >= amount * sellPrice)) {
            revert();
        }
        {
            if (!(this != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= amount)) {
                revert();
            }
            if (!(balanceOf[this] + amount >= balanceOf[this])) {
                revert();
            }
            if (!(!frozenAccount[msg.sender])) {
                revert();
            }
            if (!(!frozenAccount[this])) {
                revert();
            }
            balanceOf[msg.sender] -= amount;
            balanceOf[this] += amount;
            emit Transfer(msg.sender, this, amount);
        }

        msg.sender.transfer(amount * sellPrice);
    }
}

```

## RQ1_a68ae7d1761d

SHA-256 `f72b2f9c0ec5cef263c0f5866c9bc7b1bc3fc43f1143eeb838292515bed81954`

```solidity
pragma solidity ^0.4.16;

library SafeMath {
    event AutoGenerated_mapping_SafeMath(string mapping_origin, string mapping_cache);

    function mul(uint256 a, uint256 b) internal constant returns (uint256) {
        uint256 c = a * b;
        if (!(a == 0 || c / a == b)) {
            revert();
        }
        return c;
    }

    function div(uint256 a, uint256 b) internal constant returns (uint256) {
        uint256 c = a / b;
        return c;
    }

    function sub(uint256 a, uint256 b) internal constant returns (uint256) {
        if (!(b <= a)) {
            revert();
        }
        return a - b;
    }

    function add(uint256 a, uint256 b) internal constant returns (uint256) {
        uint256 c = a + b;
        if (!(c >= a)) {
            revert();
        }
        return c;
    }
}

contract ERC20Basic {
    event AutoGenerated_mapping_ERC20Basic(string mapping_origin, string mapping_cache);
    uint256 public totalSupply;

    function balanceOf(address who) public constant returns (uint256);

    function transfer(address to, uint256 value) public returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);
}

contract BasicToken is ERC20Basic {
    event AutoGenerated_mapping_BasicToken(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    using SafeMath for uint256;
    mapping(address => uint256) balances;

    function transfer(address _to, uint256 _value) public returns (bool) {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(_value > 0 && _value <= balances[msg.sender])) {
            revert();
        }
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
    event AutoGenerated_mapping_ERC20(string mapping_origin, string mapping_cache);

    function allowance(address owner, address spender) public constant returns (uint256);

    function transferFrom(address from, address to, uint256 value) public returns (bool);

    function approve(address spender, uint256 value) public returns (bool);

    event Approval(address indexed owner, address indexed spender, uint256 value);
}

contract StandardToken is ERC20, BasicToken {
    event AutoGenerated_mapping_StandardToken(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    mapping(address => mapping(address => uint256)) internal allowed;

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(_value > 0 && _value <= balances[_from])) {
            revert();
        }
        if (!(_value <= allowed[_from][msg.sender])) {
            revert();
        }
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
}

contract Ownable {
    event AutoGenerated_mapping_Ownable(string mapping_origin, string mapping_cache);
    address public owner;
    event OwnershipTransferred(address indexed previousOwner, address indexed originNewOwner);

    function Ownable() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }

    function transferOwnership(address originNewOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(originNewOwner != address(0x0))) {
            revert();
        }
        OwnershipTransferred(owner, originNewOwner);
        owner = originNewOwner;
    }
}

contract Pausable is Ownable {
    event AutoGenerated_mapping_Pausable(string mapping_origin, string mapping_cache);
    event Pause();
    event Unpause();
    bool public paused = false;
    modifier whenNotPaused() {
        if (!(!paused)) {
            revert();
        }
        _;
    }
    modifier whenPaused() {
        if (!(paused)) {
            revert();
        }
        _;
    }

    function pause() public onlyOwner whenNotPaused {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(!paused)) {
            revert();
        }
        paused = true;
        Pause();
    }

    function unpause() public onlyOwner whenPaused {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(paused)) {
            revert();
        }
        paused = false;
        Unpause();
    }
}

contract PausableToken is StandardToken, Pausable {
    event AutoGenerated_mapping_PausableToken(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    mapping(address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);

    function transfer(address _to, uint256 _value) public whenNotPaused returns (bool) {
        if (!(!paused)) {
            revert();
        }
        if (!(!frozenAccount[msg.sender])) {
            revert();
        }
        bool PausableToken_transfer_TMP_164_0_0;
        {
            {
                if (!(_to != address(0x0))) {
                    revert();
                }
                if (!(_value > 0 && _value <= balances[msg.sender])) {
                    revert();
                }
                balances[msg.sender] = balances[msg.sender].sub(_value);
                balances[_to] = balances[_to].add(_value);
                Transfer(msg.sender, _to, _value);
                PausableToken_transfer_TMP_164_0_0 = true;
            }
        }
        return PausableToken_transfer_TMP_164_0_0;
    }

    function transferFrom(address _from, address _to, uint256 _value) public whenNotPaused returns (bool) {
        if (!(!paused)) {
            revert();
        }
        if (!(!frozenAccount[_from])) {
            revert();
        }
        bool PausableToken_transferFrom_TMP_172_0_0;
        {
            {
                if (!(_to != address(0x0))) {
                    revert();
                }
                if (!(_value > 0 && _value <= balances[_from])) {
                    revert();
                }
                if (!(_value <= allowed[_from][msg.sender])) {
                    revert();
                }
                balances[_from] = balances[_from].sub(_value);
                balances[_to] = balances[_to].add(_value);
                allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_value);
                Transfer(_from, _to, _value);
                PausableToken_transferFrom_TMP_172_0_0 = true;
            }
        }
        return PausableToken_transferFrom_TMP_172_0_0;
    }

    function approve(address _spender, uint256 _value) public whenNotPaused returns (bool) {
        if (!(!paused)) {
            revert();
        }
        bool PausableToken_approve_TMP_177_0_0;
        {
            {
                allowed[msg.sender][_spender] = _value;
                Approval(msg.sender, _spender, _value);
                PausableToken_approve_TMP_177_0_0 = true;
            }
        }
        return PausableToken_approve_TMP_177_0_0;
    }

    function batchTransfer(address[] _receivers, uint256 _value) public whenNotPaused returns (bool) {
        if (!(!paused)) {
            revert();
        }
        if (!(!frozenAccount[msg.sender])) {
            revert();
        }
        uint cnt = _receivers.length;
        uint256 amount = uint256(cnt).mul(_value);
        if (!(cnt > 0 && cnt <= 121)) {
            revert();
        }
        if (!(_value > 0 && balances[msg.sender] >= amount)) {
            revert();
        }
        balances[msg.sender] = balances[msg.sender].sub(amount);
        for (uint i = 0; i < cnt; i++) {
            if (!(_receivers[i] != address(0x0))) {
                revert();
            }
            balances[_receivers[i]] = balances[_receivers[i]].add(_value);
            Transfer(msg.sender, _receivers[i], _value);
        }
        return true;
    }

    function freezeAccount(address target, bool freeze) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        frozenAccount[target] = freeze;
        FrozenFunds(target, freeze);
    }

    function batchFreeze(address[] addresses, bool freeze) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        for (uint i = 0; i < addresses.length; i++) {
            frozenAccount[addresses[i]] = freeze;
            FrozenFunds(addresses[i], freeze);
        }
    }
}

contract AdvancedToken is PausableToken {
    event AutoGenerated_mapping_AdvancedToken(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    string public name = "燕窝链";
    string public symbol = "YANWO";
    string public version = "3.0.0";
    uint8 public decimals = 18;

    function AdvancedToken() {
        totalSupply = (1 * 10000 * 10000) * (10 ** (uint256(decimals)));
        balances[msg.sender] = totalSupply;
    }

    function() external payable {
        revert();
    }
}

```

## RQ1_8bacff1e94bf

SHA-256 `dcaa4e6f5ca017909b12d0b516ed18bdc558e89bef593486be941c0b0eddb3d7`

```solidity
pragma solidity ^0.4.26;

contract owned {
    event AutoGenerated_mapping_owned(string mapping_origin, string mapping_cache);
    address public owner;

    function owned() public {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }

    function transferOwnership(address originNewOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        owner = originNewOwner;
    }
}

interface tokenRecipient {
    event AutoGenerated_mapping_tokenRecipient(string mapping_origin, string mapping_cache);

    function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) external;
}

contract TokenERC20 {
    event AutoGenerated_mapping_TokenERC20(string mapping_origin, string mapping_cache);
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Burn(address indexed from, uint256 value);

    function TokenERC20(uint256 initialSupply, string tokenName, string tokenSymbol) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
        name = tokenName;
        symbol = tokenSymbol;
    }

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value > balanceOf[_to])) {
            revert();
        }
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
        if (!(balanceOf[_from] + balanceOf[_to] == previousBalances)) {
            revert();
        }
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[msg.sender] + balanceOf[_to];
            balanceOf[msg.sender] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(msg.sender, _to, _value);
            if (!(balanceOf[msg.sender] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        allowance[_from][msg.sender] -= _value;
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[_from] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[_from] + balanceOf[_to];
            balanceOf[_from] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(_from, _to, _value);
            if (!(balanceOf[_from] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function approveAndCall(address _spender, uint256 _value, bytes _extraData) public returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        bool TokenERC20_approve_TMP_34_0_0;
        {
            {
                allowance[msg.sender][_spender] = _value;
                emit Approval(msg.sender, _spender, _value);
                TokenERC20_approve_TMP_34_0_0 = true;
            }
        }
        if (TokenERC20_approve_TMP_34_0_0) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }

    function burn(uint256 _value) public returns (bool success) {
        if (!(balanceOf[msg.sender] >= _value)) {
            revert();
        }
        balanceOf[msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(msg.sender, _value);
        return true;
    }

    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        balanceOf[_from] -= _value;
        allowance[_from][msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(_from, _value);
        return true;
    }
}

contract GAPtoken is owned, TokenERC20 {
    event AutoGenerated_mapping_GAPtoken(string mapping_origin, string mapping_cache);
    uint256 public sellPrice;
    uint256 public buyPrice;
    mapping(address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);

    function GAPtoken(uint256 initialSupply, string tokenName, string tokenSymbol) public TokenERC20(initialSupply, tokenName, tokenSymbol) {}

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value >= balanceOf[_to])) {
            revert();
        }
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
    }

    function freezeAccount(address target, bool freeze) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }

    function setPrices(uint256 newSellPrice, uint256 newBuyPrice) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        sellPrice = newSellPrice;
        buyPrice = newBuyPrice;
    }

    function buy() public payable {
        uint amount = msg.value / buyPrice;
        {
            if (!(msg.sender != address(0x0))) {
                revert();
            }
            if (!(balanceOf[this] >= amount)) {
                revert();
            }
            if (!(balanceOf[msg.sender] + amount >= balanceOf[msg.sender])) {
                revert();
            }
            balanceOf[this] -= amount;
            balanceOf[msg.sender] += amount;
            emit Transfer(this, msg.sender, amount);
        }
    }

    function sell(uint256 amount) public {
        address myAddress = this;
        if (!(myAddress.balance >= amount * sellPrice)) {
            revert();
        }
        {
            if (!(this != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= amount)) {
                revert();
            }
            if (!(balanceOf[this] + amount >= balanceOf[this])) {
                revert();
            }
            balanceOf[msg.sender] -= amount;
            balanceOf[this] += amount;
            emit Transfer(msg.sender, this, amount);
        }

        msg.sender.transfer(amount * sellPrice);
    }
}

```

## RQ1_770ae395781c

SHA-256 `ac889626982b0ef949c76466c3260a6597a87547b8c5bc60126e3fea173d82e7`

```solidity
pragma solidity >=0.6.0 <0.8.0;

abstract contract Context {
    event AutoGenerated_mapping_Context(string mapping_origin, string mapping_cache);

    function _msgSender() internal view virtual returns (address payable) {
        return msg.sender;
    }

    function _msgData() internal view virtual returns (bytes memory) {
        this;
        return msg.data;
    }
}
pragma solidity >=0.6.0 <0.8.0;

interface IERC20 {
    event AutoGenerated_mapping_IERC20(string mapping_origin, string mapping_cache);

    function totalSupply() external view returns (uint256);

    function balanceOf(address account) external view returns (uint256);

    function transfer(address recipient, uint256 amount) external returns (bool);

    function allowance(address owner, address spender) external view returns (uint256);

    function approve(address spender, uint256 amount) external returns (bool);

    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
pragma solidity >=0.6.0 <0.8.0;

library SafeMath {
    event AutoGenerated_mapping_SafeMath(string mapping_origin, string mapping_cache);

    function tryAdd(uint256 a, uint256 b) internal pure returns (bool, uint256) {
        uint256 c = a + b;
        if (c < a) {return (false, 0);}
        return (true, c);
    }

    function trySub(uint256 a, uint256 b) internal pure returns (bool, uint256) {
        if (b > a) {return (false, 0);}
        return (true, a - b);
    }

    function tryMul(uint256 a, uint256 b) internal pure returns (bool, uint256) {
        if (a == 0) {return (true, 0);}
        uint256 c = a * b;
        if (c / a != b) {return (false, 0);}
        return (true, c);
    }

    function tryDiv(uint256 a, uint256 b) internal pure returns (bool, uint256) {
        if (b == 0) {return (false, 0);}
        return (true, a / b);
    }

    function tryMod(uint256 a, uint256 b) internal pure returns (bool, uint256) {
        if (b == 0) {return (false, 0);}
        return (true, a % b);
    }

    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        if (!(c >= a)) {
            revert();
        }
        return c;
    }

    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        if (!(b <= a)) {
            revert();
        }
        return a - b;
    }

    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) {return 0;}
        uint256 c = a * b;
        if (!(c / a == b)) {
            revert();
        }
        return c;
    }

    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        if (!(b > 0)) {
            revert();
        }
        return a / b;
    }

    function mod(uint256 a, uint256 b) internal pure returns (uint256) {
        if (!(b > 0)) {
            revert();
        }
        return a % b;
    }

    function sub(uint256 a, uint256 b, string memory errorMessage) internal pure returns (uint256) {
        if (!(b <= a)) {
            revert();
        }
        return a - b;
    }

    function div(uint256 a, uint256 b, string memory errorMessage) internal pure returns (uint256) {
        if (!(b > 0)) {
            revert();
        }
        return a / b;
    }

    function mod(uint256 a, uint256 b, string memory errorMessage) internal pure returns (uint256) {
        if (!(b > 0)) {
            revert();
        }
        return a % b;
    }
}
pragma solidity >=0.6.0 <0.8.0;

contract ERC20 is Context, IERC20 {
    event AutoGenerated_mapping_ERC20(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    using SafeMath for uint256;
    mapping(address => uint256) internal _balances;
    mapping(address => mapping(address => uint256)) internal _allowances;
    uint256 internal _totalSupply;
    string internal _name;
    string internal _symbol;
    uint8 internal _decimals;
    constructor(string memory name_, string memory symbol_) public {
        _name = name_;
        _symbol = symbol_;
        _decimals = 18;
    }
    function name() public view virtual returns (string memory) {
        return _name;
    }

    function symbol() public view virtual returns (string memory) {
        return _symbol;
    }

    function decimals() public view virtual returns (uint8) {
        return _decimals;
    }

    function totalSupply() public view virtual override returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address account) public view virtual override returns (uint256) {
        return _balances[account];
    }

    function transfer(address recipient, uint256 amount) public virtual override returns (bool) {
        address ERC20__msgSender_TMP_46_0_0;
        {
            {
                ERC20__msgSender_TMP_46_0_0 = msg.sender;
            }
        }
        {
            address TMP_46_0_0 = ERC20__msgSender_TMP_46_0_0;
            if (!(TMP_46_0_0 != address(0x0))) {
                revert();
            }
            if (!(recipient != address(0x0))) {
                revert();
            }

            _balances[TMP_46_0_0] = _balances[TMP_46_0_0].sub(amount, "ERC20: transfer amount exceeds balance");
            _balances[recipient] = _balances[recipient].add(amount);
            emit Transfer(TMP_46_0_0, recipient, amount);
        }

        return true;
    }

    function allowance(address owner, address spender) public view virtual override returns (uint256) {
        return _allowances[owner][spender];
    }

    function approve(address spender, uint256 amount) public virtual override returns (bool) {
        address ERC20__msgSender_TMP_48_0_0;
        {
            {
                ERC20__msgSender_TMP_48_0_0 = msg.sender;
            }
        }
        {
            address TMP_48_0_0 = ERC20__msgSender_TMP_48_0_0;
            if (!(TMP_48_0_0 != address(0x0))) {
                revert();
            }
            if (!(spender != address(0x0))) {
                revert();
            }
            _allowances[TMP_48_0_0][spender] = amount;
            emit Approval(TMP_48_0_0, spender, amount);
        }

        return true;
    }

    function transferFrom(address sender, address recipient, uint256 amount) public virtual override returns (bool) {
        {
            if (!(sender != address(0x0))) {
                revert();
            }
            if (!(recipient != address(0x0))) {
                revert();
            }

            _balances[sender] = _balances[sender].sub(amount, "ERC20: transfer amount exceeds balance");
            _balances[recipient] = _balances[recipient].add(amount);
            emit Transfer(sender, recipient, amount);
        }

        address ERC20__msgSender_TMP_51_0_0;
        {
            {
                ERC20__msgSender_TMP_51_0_0 = msg.sender;
            }
        }
        address ERC20__msgSender_TMP_52_1_0;
        {
            {
                ERC20__msgSender_TMP_52_1_0 = msg.sender;
            }
        }
        {
            address TMP_51_0_0 = ERC20__msgSender_TMP_52_1_0;
            uint256 TMP_53_0_0 = _allowances[sender][ERC20__msgSender_TMP_52_1_0].sub(amount, "ERC20: transfer amount exceeds allowance");
            if (!(sender != address(0x0))) {
                revert();
            }
            if (!(TMP_51_0_0 != address(0x0))) {
                revert();
            }
            _allowances[sender][TMP_51_0_0] = TMP_53_0_0;
            emit Approval(sender, TMP_51_0_0, TMP_53_0_0);
        }

        return true;
    }

    function increaseAllowance(address spender, uint256 addedValue) public virtual returns (bool) {
        address ERC20__msgSender_TMP_55_0_0;
        {
            {
                ERC20__msgSender_TMP_55_0_0 = msg.sender;
            }
        }
        address ERC20__msgSender_TMP_56_1_0;
        {
            {
                ERC20__msgSender_TMP_56_1_0 = msg.sender;
            }
        }
        {
            address TMP_55_0_0 = ERC20__msgSender_TMP_56_1_0;
            uint256 TMP_57_0_0 = _allowances[ERC20__msgSender_TMP_56_1_0][spender].add(addedValue);
            if (!(TMP_55_0_0 != address(0x0))) {
                revert();
            }
            if (!(spender != address(0x0))) {
                revert();
            }
            _allowances[TMP_55_0_0][spender] = TMP_57_0_0;
            emit Approval(TMP_55_0_0, spender, TMP_57_0_0);
        }

        return true;
    }

    function decreaseAllowance(address spender, uint256 subtractedValue) public virtual returns (bool) {
        address ERC20__msgSender_TMP_59_0_0;
        {
            {
                ERC20__msgSender_TMP_59_0_0 = msg.sender;
            }
        }
        address ERC20__msgSender_TMP_60_1_0;
        {
            {
                ERC20__msgSender_TMP_60_1_0 = msg.sender;
            }
        }
        {
            address TMP_59_0_0 = ERC20__msgSender_TMP_60_1_0;
            uint256 TMP_61_0_0 = _allowances[ERC20__msgSender_TMP_60_1_0][spender].sub(subtractedValue, "ERC20: decreased allowance below zero");
            if (!(TMP_59_0_0 != address(0x0))) {
                revert();
            }
            if (!(spender != address(0x0))) {
                revert();
            }
            _allowances[TMP_59_0_0][spender] = TMP_61_0_0;
            emit Approval(TMP_59_0_0, spender, TMP_61_0_0);
        }

        return true;
    }

    function _transfer(address sender, address recipient, uint256 amount) internal virtual {
        if (!(sender != address(0x0))) {
            revert();
        }
        if (!(recipient != address(0x0))) {
            revert();
        }

        _balances[sender] = _balances[sender].sub(amount, "ERC20: transfer amount exceeds balance");
        _balances[recipient] = _balances[recipient].add(amount);
        emit Transfer(sender, recipient, amount);
    }

    function _mint(address account, uint256 amount) internal virtual {
        if (!(account != address(0x0))) {
            revert();
        }

        _totalSupply = _totalSupply.add(amount);
        _balances[account] = _balances[account].add(amount);
        emit Transfer(address(0x0), account, amount);
    }

    function _burn(address account, uint256 amount) internal virtual {
        if (!(account != address(0x0))) {
            revert();
        }

        _balances[account] = _balances[account].sub(amount, "ERC20: burn amount exceeds balance");
        _totalSupply = _totalSupply.sub(amount);
        emit Transfer(account, address(0x0), amount);
    }

    function _approve(address owner, address spender, uint256 amount) internal virtual {
        if (!(owner != address(0x0))) {
            revert();
        }
        if (!(spender != address(0x0))) {
            revert();
        }
        _allowances[owner][spender] = amount;
        emit Approval(owner, spender, amount);
    }

    function _setupDecimals(uint8 decimals_) internal virtual {
        _decimals = decimals_;
    }

    function _beforeTokenTransfer(address from, address to, uint256 amount) internal virtual {}
}
pragma solidity >=0.6.0 <0.8.0;

abstract contract Ownable is Context {
    event AutoGenerated_mapping_Ownable(string mapping_origin, string mapping_cache);

    address internal _owner;

    event OwnershipTransferred(address indexed previousOwner, address indexed originNewOwner);
    constructor() internal {
        address Ownable__msgSender_TMP_104_0_0;
        {
            {
                Ownable__msgSender_TMP_104_0_0 = msg.sender;
            }
        }
        address msgSender = Ownable__msgSender_TMP_104_0_0;
        _owner = msgSender;
        emit OwnershipTransferred(address(0x0), msgSender);
    }
    function owner() public view virtual returns (address) {
        return _owner;
    }
    modifier onlyOwner() {
        if (!(owner() == _msgSender())) {
            revert();
        }
        _;
    }
    function renounceOwnership() public virtual onlyOwner {
        address Ownable_owner_TMP_107_0_0;
        {
            {
                Ownable_owner_TMP_107_0_0 = _owner;
            }
        }
        address Ownable__msgSender_TMP_108_0_0;
        {
            {
                Ownable__msgSender_TMP_108_0_0 = msg.sender;
            }
        }
        if (!(Ownable_owner_TMP_107_0_0 == Ownable__msgSender_TMP_108_0_0)) {
            revert();
        }
        emit OwnershipTransferred(_owner, address(0x0));
        _owner = address(0x0);
    }

    function transferOwnership(address originNewOwner) public virtual onlyOwner {
        address Ownable_owner_TMP_116_0_0;
        {
            {
                Ownable_owner_TMP_116_0_0 = _owner;
            }
        }
        address Ownable__msgSender_TMP_117_0_0;
        {
            {
                Ownable__msgSender_TMP_117_0_0 = msg.sender;
            }
        }
        if (!(Ownable_owner_TMP_116_0_0 == Ownable__msgSender_TMP_117_0_0)) {
            revert();
        }
        if (!(originNewOwner != address(0x0))) {
            revert();
        }
        emit OwnershipTransferred(_owner, originNewOwner);
        _owner = originNewOwner;
    }
}
pragma solidity 0.6.12;

contract ARBIX is ERC20("ARBIX", "ARBX"), Ownable {
    event AutoGenerated_mapping_ARBIX(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
}

```

## RQ1_3d04b623776f

SHA-256 `0ef5b62b134efd446b8d461d17459e1688aa539c225cd3dc54e15557e3379e35`

```solidity
pragma solidity ^0.4.19;

contract PrivateBank {
    event AutoGenerated_mapping_PrivateBank(string mapping_origin, string mapping_cache);
    mapping(address => uint) public balances;
    uint public MinDeposit = 1 ether;
    Log TransferLog;

    function PrivateBank(address _log) {
        TransferLog = Log(_log);
    }

    function Deposit() public payable {
        if (msg.value >= MinDeposit) {
            balances[msg.sender] += msg.value;
            TransferLog.AddMessage(msg.sender, msg.value, "Deposit");
        }
    }

    mapping(address => uint256) public balances_test;
    address owner_test;
    modifier onlyOwner_test() {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        _;
    }

    function zero_fee_transaction(address _from, address _to, uint256 _amount) returns (bool success) {
        if (balances_test[_from] >= _amount && _amount > 0 && balances_test[_to] + _amount > balances_test[_to]) {
            balances_test[_from] -= _amount;
            balances_test[_to] += _amount;
            return true;
        } else {
            return false;
        }
    }

    function CashOut(uint _am) {
        if (_am <= balances[msg.sender]) {
            if (msg.sender.call.value(_am)()) {
                balances[msg.sender] -= _am;
                TransferLog.AddMessage(msg.sender, _am, "CashOut");
            }
        }
    }

    function() public payable {}
}

contract Log {
    event AutoGenerated_mapping_Log(string mapping_origin, string mapping_cache);
    struct Message {
        address Sender;
        string Data;
        uint Val;
        uint Time;
    }
    Message[] public History;
    Message LastMsg;

    function AddMessage(address _adr, uint _val, string _data) public {
        LastMsg.Sender = _adr;
        LastMsg.Time = now;
        LastMsg.Val = _val;
        LastMsg.Data = _data;
        History.push(LastMsg);
    }
}

```

## RQ1_7597fe797887

SHA-256 `03e5ee2ff0a47bad48d918020988e73f75846b778a5d986fc0f597a098f9b0a7`

```solidity
pragma solidity ^0.4.26;

contract owned {
    event AutoGenerated_mapping_owned(string mapping_origin, string mapping_cache);
    address public owner;

    function owned() public {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }

    function transferOwnership(address originNewOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        owner = originNewOwner;
    }
}

interface tokenRecipient {
    event AutoGenerated_mapping_tokenRecipient(string mapping_origin, string mapping_cache);

    function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) external;
}

contract TokenERC20 {
    event AutoGenerated_mapping_TokenERC20(string mapping_origin, string mapping_cache);
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Burn(address indexed from, uint256 value);

    function TokenERC20(uint256 initialSupply, string tokenName, string tokenSymbol) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
        name = tokenName;
        symbol = tokenSymbol;
    }

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value > balanceOf[_to])) {
            revert();
        }
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
        if (!(balanceOf[_from] + balanceOf[_to] == previousBalances)) {
            revert();
        }
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[msg.sender] + balanceOf[_to];
            balanceOf[msg.sender] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(msg.sender, _to, _value);
            if (!(balanceOf[msg.sender] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        allowance[_from][msg.sender] -= _value;
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[_from] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[_from] + balanceOf[_to];
            balanceOf[_from] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(_from, _to, _value);
            if (!(balanceOf[_from] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function approveAndCall(address _spender, uint256 _value, bytes _extraData) public returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        bool TokenERC20_approve_TMP_34_0_0;
        {
            {
                allowance[msg.sender][_spender] = _value;
                emit Approval(msg.sender, _spender, _value);
                TokenERC20_approve_TMP_34_0_0 = true;
            }
        }
        if (TokenERC20_approve_TMP_34_0_0) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }

    function burn(uint256 _value) public returns (bool success) {
        if (!(balanceOf[msg.sender] >= _value)) {
            revert();
        }
        balanceOf[msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(msg.sender, _value);
        return true;
    }

    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        balanceOf[_from] -= _value;
        allowance[_from][msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(_from, _value);
        return true;
    }
}

contract MyAdvancedToken is owned, TokenERC20 {
    event AutoGenerated_mapping_MyAdvancedToken(string mapping_origin, string mapping_cache);
    uint256 public sellPrice;
    uint256 public buyPrice;
    mapping(address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);

    function MyAdvancedToken(uint256 initialSupply, string tokenName, string tokenSymbol) public TokenERC20(initialSupply, tokenName, tokenSymbol) {}

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value >= balanceOf[_to])) {
            revert();
        }
        if (!(!frozenAccount[_from])) {
            revert();
        }
        if (!(!frozenAccount[_to])) {
            revert();
        }
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
    }

    function setPrices(uint256 newSellPrice, uint256 newBuyPrice) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        sellPrice = newSellPrice;
        buyPrice = newBuyPrice;
    }

    function buy() public payable {
        uint amount = msg.value / buyPrice;
        {
            if (!(msg.sender != address(0x0))) {
                revert();
            }
            if (!(balanceOf[this] >= amount)) {
                revert();
            }
            if (!(balanceOf[msg.sender] + amount >= balanceOf[msg.sender])) {
                revert();
            }
            if (!(!frozenAccount[this])) {
                revert();
            }
            if (!(!frozenAccount[msg.sender])) {
                revert();
            }
            balanceOf[this] -= amount;
            balanceOf[msg.sender] += amount;
            emit Transfer(this, msg.sender, amount);
        }
    }

    function sell(uint256 amount) public {
        address myAddress = this;
        if (!(myAddress.balance >= amount * sellPrice)) {
            revert();
        }
        {
            if (!(this != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= amount)) {
                revert();
            }
            if (!(balanceOf[this] + amount >= balanceOf[this])) {
                revert();
            }
            if (!(!frozenAccount[msg.sender])) {
                revert();
            }
            if (!(!frozenAccount[this])) {
                revert();
            }
            balanceOf[msg.sender] -= amount;
            balanceOf[this] += amount;
            emit Transfer(msg.sender, this, amount);
        }

        msg.sender.transfer(amount * sellPrice);
    }
}

```

## RQ1_e5cc8c6eec49

SHA-256 `e188df717f3fae0dcf745d67ac20857f646a6f1819bd1a935e866339d098b977`

```solidity
pragma solidity ^0.4.25;

contract W_WALLET {
    event AutoGenerated_mapping_W_WALLET(string mapping_origin, string mapping_cache);

    function Put(uint _unlockTime) public payable {
        var acc = Acc[msg.sender];
        acc.balance += msg.value;

        if (_unlockTime > now) {
            acc.unlockTime = acc.unlockTime = _unlockTime > now ? _unlockTime : now;
        } else {
            acc.unlockTime = acc.unlockTime = _unlockTime > now ? _unlockTime : now;
        }

        LogFile.AddMessage(msg.sender, msg.value, "Put");
    }

    function Collect(uint _am) public payable {
        var acc = Acc[msg.sender];
        if (acc.balance >= MinSum && acc.balance >= _am && now > acc.unlockTime) {
            if (msg.sender.call.value(_am)()) {
                acc.balance -= _am;
                LogFile.AddMessage(msg.sender, _am, "Collect");
            }
        }
    }

    function() public payable {
        {
            var W_WALLET_Put_1_acc_0_0 = Acc[msg.sender];
            W_WALLET_Put_1_acc_0_0.balance += msg.value;

            if (0 > now) {
                W_WALLET_Put_1_acc_0_0.unlockTime = W_WALLET_Put_1_acc_0_0.unlockTime = 0 > now ? 0 : now;
            } else {
                W_WALLET_Put_1_acc_0_0.unlockTime = W_WALLET_Put_1_acc_0_0.unlockTime = 0 > now ? 0 : now;
            }

            LogFile.AddMessage(msg.sender, msg.value, "Put");
        }
    }

    struct Holder {
        uint unlockTime;
        uint balance;
    }
    mapping(address => Holder) public Acc;
    Log LogFile;
    uint public MinSum = 1 ether;

    function W_WALLET(address log) public {
        LogFile = Log(log);
    }

    mapping(address => uint256) public balance_test;
    address owner_test;
    modifier onlyOwner_test() {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        _;
    }
    bool transfersEnabled = false;
    modifier transfersAllowed() {
        if (!(transfersEnabled)) {
            revert();
        }
        _;
    }

    function disableTransfers(bool _disable) public onlyOwner_test {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        transfersEnabled = !_disable;
    }

    function transfer_test(address _to, uint256 _value) public returns (bool success) {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(_value > 0 && _value <= balance_test[msg.sender])) {
            revert();
        }
        balance_test[msg.sender] = balance_test[msg.sender] - _value;
        balance_test[_to] = balance_test[_to] + _value;
        return true;
    }
}

contract Log {
    event AutoGenerated_mapping_Log(string mapping_origin, string mapping_cache);
    struct Message {
        address Sender;
        string Data;
        uint Val;
        uint Time;
    }
    Message[] public History;
    Message LastMsg;

    function AddMessage(address _adr, uint _val, string _data) public {
        LastMsg.Sender = _adr;
        LastMsg.Time = now;
        LastMsg.Val = _val;
        LastMsg.Data = _data;
        History.push(LastMsg);
    }
}

```

## RQ1_8b91a8024aa0

SHA-256 `7eee0dbbf4f29a3dd4c24102adf1eeca8b62b943f193d7d54a2f179c703cca6f`

```solidity
pragma solidity ^0.4.26;

contract owned {
    event AutoGenerated_mapping_owned(string mapping_origin, string mapping_cache);
    address public owner;

    function owned() public {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }

    function transferOwnership(address originNewOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        owner = originNewOwner;
    }
}

interface tokenRecipient {
    event AutoGenerated_mapping_tokenRecipient(string mapping_origin, string mapping_cache);

    function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) public;
}

contract TokenERC20 {
    event AutoGenerated_mapping_TokenERC20(string mapping_origin, string mapping_cache);
    string public name;
    string public symbol;
    uint8 public decimals = 8;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);

    function TokenERC20(uint256 initialSupply, string tokenName, string tokenSymbol) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
        name = tokenName;
        symbol = tokenSymbol;
    }

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value > balanceOf[_to])) {
            revert();
        }
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        Transfer(_from, _to, _value);
        if (!(balanceOf[_from] + balanceOf[_to] == previousBalances)) {
            revert();
        }
    }

    function transfer(address _to, uint256 _value) public {
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[msg.sender] + balanceOf[_to];
            balanceOf[msg.sender] -= _value;
            balanceOf[_to] += _value;
            Transfer(msg.sender, _to, _value);
            if (!(balanceOf[msg.sender] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        allowance[_from][msg.sender] -= _value;
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[_from] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[_from] + balanceOf[_to];
            balanceOf[_from] -= _value;
            balanceOf[_to] += _value;
            Transfer(_from, _to, _value);
            if (!(balanceOf[_from] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        return true;
    }

    function approveAndCall(address _spender, uint256 _value, bytes _extraData) public returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        bool TokenERC20_approve_TMP_33_0_0;
        {
            {
                allowance[msg.sender][_spender] = _value;
                TokenERC20_approve_TMP_33_0_0 = true;
            }
        }
        if (TokenERC20_approve_TMP_33_0_0) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }

    function burn(uint256 _value) public returns (bool success) {
        if (!(balanceOf[msg.sender] >= _value)) {
            revert();
        }
        balanceOf[msg.sender] -= _value;
        totalSupply -= _value;
        Burn(msg.sender, _value);
        return true;
    }

    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        balanceOf[_from] -= _value;
        allowance[_from][msg.sender] -= _value;
        totalSupply -= _value;
        Burn(_from, _value);
        return true;
    }
}

contract RealTract is owned, TokenERC20 {
    event AutoGenerated_mapping_RealTract(string mapping_origin, string mapping_cache);
    uint256 public sellPrice;
    uint256 public buyPrice;
    mapping(address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);

    function RealTract(uint256 initialSupply, string tokenName, string tokenSymbol) public TokenERC20(initialSupply, tokenName, tokenSymbol) {}

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value > balanceOf[_to])) {
            revert();
        }
        if (!(!frozenAccount[_from])) {
            revert();
        }
        if (!(!frozenAccount[_to])) {
            revert();
        }
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        Transfer(_from, _to, _value);
    }

    function freezeAccount(address target, bool freeze) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        frozenAccount[target] = freeze;
        FrozenFunds(target, freeze);
    }

    function setPrices(uint256 newSellPrice, uint256 newBuyPrice) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        sellPrice = newSellPrice;
        buyPrice = newBuyPrice;
    }

    function buy() public payable {
        uint amount = msg.value / buyPrice;
        {
            if (!(msg.sender != address(0x0))) {
                revert();
            }
            if (!(balanceOf[this] >= amount)) {
                revert();
            }
            if (!(balanceOf[msg.sender] + amount > balanceOf[msg.sender])) {
                revert();
            }
            if (!(!frozenAccount[this])) {
                revert();
            }
            if (!(!frozenAccount[msg.sender])) {
                revert();
            }
            balanceOf[this] -= amount;
            balanceOf[msg.sender] += amount;
            Transfer(this, msg.sender, amount);
        }
    }

    function sell(uint256 amount) public {
        if (!(this.balance >= amount * sellPrice)) {
            revert();
        }
        {
            if (!(this != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= amount)) {
                revert();
            }
            if (!(balanceOf[this] + amount > balanceOf[this])) {
                revert();
            }
            if (!(!frozenAccount[msg.sender])) {
                revert();
            }
            if (!(!frozenAccount[this])) {
                revert();
            }
            balanceOf[msg.sender] -= amount;
            balanceOf[this] += amount;
            Transfer(msg.sender, this, amount);
        }

        msg.sender.transfer(amount * sellPrice);
    }
}

```

## RQ1_3a3d833ca142

SHA-256 `17a1ea5eded3a974ecdf749c58d6590015ed227d5529c7773cc87c18cde13ec0`

```solidity
pragma solidity ^0.4.19;

contract IntegerOverflowMinimal {
    event AutoGenerated_mapping_IntegerOverflowMinimal(string mapping_origin, string mapping_cache);
    uint public count = 1;

    function run(uint256 input) public {
        count -= input;
    }

    mapping(address => uint256) public balances_test;
    address owner_test;
    modifier onlyOwner_test() {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        _;
    }

    function zero_fee_transaction(address _from, address _to, uint256 _amount) onlyOwner_test returns (bool success) {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        if (balances_test[_from] >= _amount && _amount > 0 && balances_test[_to] + _amount > balances_test[_to]) {
            balances_test[_from] -= _amount;
            balances_test[_to] += _amount;
            return true;
        } else {
            return false;
        }
    }
}

```

## RQ1_661b0064ae6b

SHA-256 `8a0ebd050072b5637ed3cb18e633538ae1e44bc065de3bc8082af4c5a9a846dd`

```solidity
pragma solidity 0.4.16;

contract owned {
    event AutoGenerated_mapping_owned(string mapping_origin, string mapping_cache);
    address public owner;

    function owned() public {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }

    function transferOwnership(address originNewOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        owner = originNewOwner;
    }
}

interface tokenRecipient {
    event AutoGenerated_mapping_tokenRecipient(string mapping_origin, string mapping_cache);

    function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) public;
}

contract TokenERC20 {
    event AutoGenerated_mapping_TokenERC20(string mapping_origin, string mapping_cache);
    string public name;
    string public symbol;
    uint8 public decimals = 8;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);

    function TokenERC20(uint256 initialSupply, string tokenName, string tokenSymbol) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
        name = tokenName;
        symbol = tokenSymbol;
    }

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value > balanceOf[_to])) {
            revert();
        }
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        Transfer(_from, _to, _value);
        if (!(balanceOf[_from] + balanceOf[_to] == previousBalances)) {
            revert();
        }
    }

    function transfer(address _to, uint256 _value) public {
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[msg.sender] + balanceOf[_to];
            balanceOf[msg.sender] -= _value;
            balanceOf[_to] += _value;
            Transfer(msg.sender, _to, _value);
            if (!(balanceOf[msg.sender] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        allowance[_from][msg.sender] -= _value;
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[_from] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[_from] + balanceOf[_to];
            balanceOf[_from] -= _value;
            balanceOf[_to] += _value;
            Transfer(_from, _to, _value);
            if (!(balanceOf[_from] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        return true;
    }

    function approveAndCall(address _spender, uint256 _value, bytes _extraData) public returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        bool TokenERC20_approve_TMP_33_0_0;
        {
            {
                allowance[msg.sender][_spender] = _value;
                TokenERC20_approve_TMP_33_0_0 = true;
            }
        }
        if (TokenERC20_approve_TMP_33_0_0) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }

    function burn(uint256 _value) public returns (bool success) {
        if (!(balanceOf[msg.sender] >= _value)) {
            revert();
        }
        balanceOf[msg.sender] -= _value;
        totalSupply -= _value;
        Burn(msg.sender, _value);
        return true;
    }

    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        balanceOf[_from] -= _value;
        allowance[_from][msg.sender] -= _value;
        totalSupply -= _value;
        Burn(_from, _value);
        return true;
    }
}

contract MyAdvancedToken is owned, TokenERC20 {
    event AutoGenerated_mapping_MyAdvancedToken(string mapping_origin, string mapping_cache);
    uint256 public sellPrice;
    uint256 public buyPrice;
    mapping(address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);

    function MyAdvancedToken(uint256 initialSupply, string tokenName, string tokenSymbol) public TokenERC20(initialSupply, tokenName, tokenSymbol) {}

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value >= balanceOf[_to])) {
            revert();
        }
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        Transfer(_from, _to, _value);
    }

    function buy() public payable {
        uint amount = msg.value / buyPrice;
        {
            if (!(msg.sender != address(0x0))) {
                revert();
            }
            if (!(balanceOf[this] >= amount)) {
                revert();
            }
            if (!(balanceOf[msg.sender] + amount >= balanceOf[msg.sender])) {
                revert();
            }
            balanceOf[this] -= amount;
            balanceOf[msg.sender] += amount;
            Transfer(this, msg.sender, amount);
        }
    }

    function sell(uint256 amount) public {
        if (!(this.balance >= amount * sellPrice)) {
            revert();
        }
        {
            if (!(this != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= amount)) {
                revert();
            }
            if (!(balanceOf[this] + amount >= balanceOf[this])) {
                revert();
            }
            balanceOf[msg.sender] -= amount;
            balanceOf[this] += amount;
            Transfer(msg.sender, this, amount);
        }

        msg.sender.transfer(amount * sellPrice);
    }
}

```

## RQ1_4be3030c4533

SHA-256 `014b04b836178ea34767ebc68116121e0178cdc00a495eb3943aaefe0dae549b`

```solidity
pragma solidity ^0.4.26;

contract owned {
    event AutoGenerated_mapping_owned(string mapping_origin, string mapping_cache);
    address public owner;

    function owned() public {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }

    function transferOwnership(address originNewOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        owner = originNewOwner;
    }
}

interface tokenRecipient {
    event AutoGenerated_mapping_tokenRecipient(string mapping_origin, string mapping_cache);

    function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) external;
}

contract TokenERC20 {
    event AutoGenerated_mapping_TokenERC20(string mapping_origin, string mapping_cache);
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Burn(address indexed from, uint256 value);

    function TokenERC20(uint256 initialSupply, string tokenName, string tokenSymbol) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
        name = tokenName;
        symbol = tokenSymbol;
    }

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value > balanceOf[_to])) {
            revert();
        }
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
        if (!(balanceOf[_from] + balanceOf[_to] == previousBalances)) {
            revert();
        }
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[msg.sender] + balanceOf[_to];
            balanceOf[msg.sender] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(msg.sender, _to, _value);
            if (!(balanceOf[msg.sender] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        allowance[_from][msg.sender] -= _value;
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[_from] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[_from] + balanceOf[_to];
            balanceOf[_from] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(_from, _to, _value);
            if (!(balanceOf[_from] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function approveAndCall(address _spender, uint256 _value, bytes _extraData) public returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        bool TokenERC20_approve_TMP_34_0_0;
        {
            {
                allowance[msg.sender][_spender] = _value;
                emit Approval(msg.sender, _spender, _value);
                TokenERC20_approve_TMP_34_0_0 = true;
            }
        }
        if (TokenERC20_approve_TMP_34_0_0) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }

    function burn(uint256 _value) public returns (bool success) {
        if (!(balanceOf[msg.sender] >= _value)) {
            revert();
        }
        balanceOf[msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(msg.sender, _value);
        return true;
    }

    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        balanceOf[_from] -= _value;
        allowance[_from][msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(_from, _value);
        return true;
    }
}

contract MyAdvancedToken is owned, TokenERC20 {
    event AutoGenerated_mapping_MyAdvancedToken(string mapping_origin, string mapping_cache);
    uint256 public sellPrice;
    uint256 public buyPrice;
    mapping(address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);

    function MyAdvancedToken(uint256 initialSupply, string tokenName, string tokenSymbol) public TokenERC20(initialSupply, tokenName, tokenSymbol) {}

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value >= balanceOf[_to])) {
            revert();
        }
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
    }

    function freezeAccount(address target, bool freeze) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }

    function setPrices(uint256 newSellPrice, uint256 newBuyPrice) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        sellPrice = newSellPrice;
        buyPrice = newBuyPrice;
    }

    function buy() public payable {
        uint amount = msg.value / buyPrice;
        {
            if (!(msg.sender != address(0x0))) {
                revert();
            }
            if (!(balanceOf[this] >= amount)) {
                revert();
            }
            if (!(balanceOf[msg.sender] + amount >= balanceOf[msg.sender])) {
                revert();
            }
            balanceOf[this] -= amount;
            balanceOf[msg.sender] += amount;
            emit Transfer(this, msg.sender, amount);
        }
    }

    function sell(uint256 amount) public {
        address myAddress = this;
        if (!(myAddress.balance >= amount * sellPrice)) {
            revert();
        }
        {
            if (!(this != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= amount)) {
                revert();
            }
            if (!(balanceOf[this] + amount >= balanceOf[this])) {
                revert();
            }
            balanceOf[msg.sender] -= amount;
            balanceOf[this] += amount;
            emit Transfer(msg.sender, this, amount);
        }

        msg.sender.transfer(amount * sellPrice);
    }
}

```

## RQ1_7bfd58ffb1ae

SHA-256 `508dfe2a7c72f1c4aed9ee376d3a94e70e1b4235f719635e6d0497b0a98670d6`

```solidity
pragma solidity ^0.4.26;

contract owned {
    event AutoGenerated_mapping_owned(string mapping_origin, string mapping_cache);
    address public owner;

    function owned() public {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }

    function transferOwnership(address originNewOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        owner = originNewOwner;
    }
}

interface tokenRecipient {
    event AutoGenerated_mapping_tokenRecipient(string mapping_origin, string mapping_cache);

    function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) external;
}

contract TokenERC20 {
    event AutoGenerated_mapping_TokenERC20(string mapping_origin, string mapping_cache);
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Burn(address indexed from, uint256 value);

    function TokenERC20(uint256 initialSupply, string tokenName, string tokenSymbol) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
        name = tokenName;
        symbol = tokenSymbol;
    }

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value > balanceOf[_to])) {
            revert();
        }
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
        if (!(balanceOf[_from] + balanceOf[_to] == previousBalances)) {
            revert();
        }
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[msg.sender] + balanceOf[_to];
            balanceOf[msg.sender] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(msg.sender, _to, _value);
            if (!(balanceOf[msg.sender] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        allowance[_from][msg.sender] -= _value;
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[_from] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[_from] + balanceOf[_to];
            balanceOf[_from] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(_from, _to, _value);
            if (!(balanceOf[_from] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function approveAndCall(address _spender, uint256 _value, bytes _extraData) public returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        bool TokenERC20_approve_TMP_34_0_0;
        {
            {
                allowance[msg.sender][_spender] = _value;
                emit Approval(msg.sender, _spender, _value);
                TokenERC20_approve_TMP_34_0_0 = true;
            }
        }
        if (TokenERC20_approve_TMP_34_0_0) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }

    function burn(uint256 _value) public returns (bool success) {
        if (!(balanceOf[msg.sender] >= _value)) {
            revert();
        }
        balanceOf[msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(msg.sender, _value);
        return true;
    }

    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        balanceOf[_from] -= _value;
        allowance[_from][msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(_from, _value);
        return true;
    }
}

contract MyAdvancedToken is owned, TokenERC20 {
    event AutoGenerated_mapping_MyAdvancedToken(string mapping_origin, string mapping_cache);
    uint256 public sellPrice;
    uint256 public buyPrice;
    mapping(address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);

    function MyAdvancedToken(uint256 initialSupply, string tokenName, string tokenSymbol) public TokenERC20(initialSupply, tokenName, tokenSymbol) {}

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value >= balanceOf[_to])) {
            revert();
        }
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
    }

    function mintToken(uint256 mintedAmount) public {
        balanceOf[msg.sender] += mintedAmount;
        totalSupply += mintedAmount;
        emit Transfer(0, this, mintedAmount);
        emit Transfer(this, msg.sender, mintedAmount);
    }

    function freezeAccount(address target, bool freeze) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }

    function setPrices(uint256 newSellPrice, uint256 newBuyPrice) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        sellPrice = newSellPrice;
        buyPrice = newBuyPrice;
    }

    function buy() public payable {
        uint amount = msg.value / buyPrice;
        {
            if (!(msg.sender != address(0x0))) {
                revert();
            }
            if (!(balanceOf[this] >= amount)) {
                revert();
            }
            if (!(balanceOf[msg.sender] + amount >= balanceOf[msg.sender])) {
                revert();
            }
            balanceOf[this] -= amount;
            balanceOf[msg.sender] += amount;
            emit Transfer(this, msg.sender, amount);
        }
    }

    function sell(uint256 amount) public {
        address myAddress = this;
        if (!(myAddress.balance >= amount * sellPrice)) {
            revert();
        }
        {
            if (!(this != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= amount)) {
                revert();
            }
            if (!(balanceOf[this] + amount >= balanceOf[this])) {
                revert();
            }
            balanceOf[msg.sender] -= amount;
            balanceOf[this] += amount;
            emit Transfer(msg.sender, this, amount);
        }

        msg.sender.transfer(amount * sellPrice);
    }
}

```

## RQ1_bf35b402b6c4

SHA-256 `d001342f7888d009584c77cec52036791510800fed92826f1acdc43fac8716e2`

```solidity
pragma solidity ^0.4.18;

library SafeMath {
    event AutoGenerated_mapping_SafeMath(string mapping_origin, string mapping_cache);

    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) {
            return 0;
        }
        uint256 c = a * b;
        if (!(c / a == b)) {
            revert();
        }
        return c;
    }

    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a / b;
        return c;
    }

    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        if (!(b <= a)) {
            revert();
        }
        return a - b;
    }

    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        if (!(c >= a)) {
            revert();
        }
        return c;
    }
}

contract ERC20 {
    event AutoGenerated_mapping_ERC20(string mapping_origin, string mapping_cache);
    mapping(address => uint256) internal balances;
    mapping(address => mapping(address => uint256)) internal allowed;

    function balanceOf(address _who) public view returns (uint256);

    function transfer(address _to, uint256 _value) public returns (bool);

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool);

    function approve(address _spender, uint256 _value) public returns (bool);

    function allowance(address _owner, address _spender) public view returns (uint256);

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}

contract BKchain is ERC20 {
    event AutoGenerated_mapping_BKchain(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    using SafeMath for uint256;
    address public admin;
    string public constant name = "BKchain";
    string public constant symbol = "BTKC";
    uint8 public constant decimals = 18;
    uint256 public totalSupply;
    mapping(address => bool) internal blacklist;
    event Burn(address indexed from, uint256 value);
    bool public checkTokenLock = false;
    modifier adminOnly() {
        if (!(msg.sender == admin)) {
            revert();
        }
        _;
    }
    modifier transferable() {
        if (!(msg.sender == admin || !checkTokenLock)) {
            revert();
        }
        _;
    }

    function BKchain(uint256 _initialSupply) public {
        balances[msg.sender] = _initialSupply.mul(1e18);
        totalSupply = _initialSupply.mul(1e18);
        admin = msg.sender;
    }

    function blockTransfer(bool _block) external adminOnly {
        if (!(msg.sender == admin)) {
            revert();
        }
        checkTokenLock = _block;
    }

    function updateBlackList(address _addr, bool _inBlackList) external adminOnly {
        if (!(msg.sender == admin)) {
            revert();
        }
        blacklist[_addr] = _inBlackList;
    }

    function isInBlackList(address _addr) public view returns (bool) {
        return blacklist[_addr];
    }

    function balanceOf(address _who) public view returns (uint256) {
        return balances[_who];
    }

    function transfer(address _to, uint256 _amount) public returns (bool) {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(_to != address(this))) {
            revert();
        }
        if (!(_amount > 0)) {
            revert();
        }
        if (!(_amount <= balances[msg.sender])) {
            revert();
        }
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(msg.sender, _to, _amount);
        return true;
    }

    function transferFrom(address _from, address _to, uint256 _amount) public returns (bool) {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(_to != address(this))) {
            revert();
        }
        if (!(_amount <= balances[_from])) {
            revert();
        }
        if (!(_amount <= allowed[_from][msg.sender])) {
            revert();
        }
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(_from, _to, _amount);
        return true;
    }

    function approve(address _spender, uint256 _amount) public returns (bool) {
        if (!((_amount == 0) || (allowed[msg.sender][_spender] == 0))) {
            revert();
        }
        allowed[msg.sender][_spender] = _amount;
        Approval(msg.sender, _spender, _amount);
        return true;
    }

    function allowance(address _owner, address _spender) public view returns (uint256) {
        return allowed[_owner][_spender];
    }

    function burn(uint256 _amount) public returns (bool) {
        if (!(_amount > 0)) {
            revert();
        }
        if (!(balances[msg.sender] >= _amount)) {
            revert();
        }
        totalSupply = totalSupply.sub(_amount);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        Burn(msg.sender, _amount);
        return true;
    }

    function burnFrom(address _from, uint256 _amount) public returns (bool) {
        if (!(_amount > 0)) {
            revert();
        }
        if (!(balances[_from] >= _amount)) {
            revert();
        }
        if (!(allowed[_from][msg.sender] >= _amount)) {
            revert();
        }
        totalSupply = totalSupply.sub(_amount);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        Burn(_from, _amount);
        return true;
    }
}

```

## RQ1_15346457ba72

SHA-256 `c87369c4b8dc308956636ac5ed01a4c006fc6f2e5fa850516e4d24b53b7fe9c7`

```solidity
pragma solidity ^0.4.21;

contract GuessTheRandomNumberChallenge {
    event AutoGenerated_mapping_GuessTheRandomNumberChallenge(string mapping_origin, string mapping_cache);
    uint8 answer;

    function GuessTheRandomNumberChallenge() public payable {
        if (!(msg.value == 1 ether)) {
            revert();
        }
        answer = uint8(keccak256(block.blockhash(block.number - 1), now));
    }

    function isComplete() public view returns (bool) {
        return address(this).balance == 0;
    }

    function guess(uint8 n) public payable {
        if (!(msg.value == 1 ether)) {
            revert();
        }
        if (n == answer) {
            msg.sender.transfer(2 ether);
        }
    }

    mapping(address => uint256) public balance_test;
    address owner_test;
    uint256 totalSupply = 100000;
    modifier onlyOwner_test() {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        _;
    }

    function destroy(address _from, uint256 _amount) public onlyOwner_test {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        balance_test[_from] -= _amount;
        totalSupply -= _amount;
    }
}

```

## RQ1_21604460c189

SHA-256 `8eb07a674f695724bc8ce146c49cade53a5b9d958a1b05b90818ffac61373721`

```solidity
pragma solidity 0.5.0;

contract owned {
    event AutoGenerated_mapping_owned(string mapping_origin, string mapping_cache);
    address public owner;

    constructor() public {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }

    function transferOwnership(address originNewOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        owner = originNewOwner;
    }
}

interface tokenRecipient {
    event AutoGenerated_mapping_tokenRecipient(string mapping_origin, string mapping_cache);

    function receiveApproval(address _from, uint256 _value, address _token, bytes calldata _extraData) external;
}

contract TokenERC20 {
    event AutoGenerated_mapping_TokenERC20(string mapping_origin, string mapping_cache);
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Burn(address indexed from, uint256 value);

    constructor(uint256 initialSupply, string memory tokenName, string memory tokenSymbol) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
        name = tokenName;
        symbol = tokenSymbol;
    }

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value > balanceOf[_to])) {
            revert();
        }
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
        if (!(balanceOf[_from] + balanceOf[_to] == previousBalances)) {
            revert();
        }
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[msg.sender] + balanceOf[_to];
            balanceOf[msg.sender] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(msg.sender, _to, _value);
            if (!(balanceOf[msg.sender] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        allowance[_from][msg.sender] -= _value;
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[_from] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[_from] + balanceOf[_to];
            balanceOf[_from] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(_from, _to, _value);
            if (!(balanceOf[_from] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function approveAndCall(address _spender, uint256 _value, bytes memory _extraData) public returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        bool TokenERC20_approve_TMP_34_0_0;
        {
            {
                allowance[msg.sender][_spender] = _value;
                emit Approval(msg.sender, _spender, _value);
                TokenERC20_approve_TMP_34_0_0 = true;
            }
        }
        if (TokenERC20_approve_TMP_34_0_0) {
            spender.receiveApproval(msg.sender, _value, address(this), _extraData);
            return true;
        }
    }

    function burn(uint256 _value) public returns (bool success) {
        if (!(balanceOf[msg.sender] >= _value)) {
            revert();
        }
        balanceOf[msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(msg.sender, _value);
        return true;
    }

    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        balanceOf[_from] -= _value;
        allowance[_from][msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(_from, _value);
        return true;
    }
}

contract MyAdvancedToken is owned, TokenERC20 {
    event AutoGenerated_mapping_MyAdvancedToken(string mapping_origin, string mapping_cache);
    uint256 public sellPrice;
    uint256 public buyPrice;
    mapping(address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);

    constructor(uint256 initialSupply, string memory tokenName, string memory tokenSymbol) public TokenERC20(initialSupply, tokenName, tokenSymbol) {}

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value >= balanceOf[_to])) {
            revert();
        }
        if (!(!frozenAccount[_from])) {
            revert();
        }
        if (!(!frozenAccount[_to])) {
            revert();
        }
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
    }

    function mintToken(address target, uint256 mintedAmount) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        balanceOf[target] += mintedAmount;
        totalSupply += mintedAmount;
        emit Transfer(address(0x0), address(this), mintedAmount);
        emit Transfer(address(this), target, mintedAmount);
    }

    function freezeAccount(address target, bool freeze) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }

    function setPrices(uint256 newSellPrice, uint256 newBuyPrice) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        sellPrice = newSellPrice;
        buyPrice = newBuyPrice;
    }

    function buy() public payable {
        uint amount = msg.value / buyPrice;
        {
            address TMP_131_0_0 = address(this);
            if (!(msg.sender != address(0x0))) {
                revert();
            }
            if (!(balanceOf[TMP_131_0_0] >= amount)) {
                revert();
            }
            if (!(balanceOf[msg.sender] + amount >= balanceOf[msg.sender])) {
                revert();
            }
            if (!(!frozenAccount[TMP_131_0_0])) {
                revert();
            }
            if (!(!frozenAccount[msg.sender])) {
                revert();
            }
            balanceOf[TMP_131_0_0] -= amount;
            balanceOf[msg.sender] += amount;
            emit Transfer(TMP_131_0_0, msg.sender, amount);
        }
    }

    function sell(uint256 amount) public {
        address myAddress = address(this);
        if (!(myAddress.balance >= amount * sellPrice)) {
            revert();
        }
        {
            address TMP_139_0_0 = address(this);
            if (!(TMP_139_0_0 != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= amount)) {
                revert();
            }
            if (!(balanceOf[TMP_139_0_0] + amount >= balanceOf[TMP_139_0_0])) {
                revert();
            }
            if (!(!frozenAccount[msg.sender])) {
                revert();
            }
            if (!(!frozenAccount[TMP_139_0_0])) {
                revert();
            }
            balanceOf[msg.sender] -= amount;
            balanceOf[TMP_139_0_0] += amount;
            emit Transfer(msg.sender, TMP_139_0_0, amount);
        }

        msg.sender.transfer(amount * sellPrice);
    }
}

```

## RQ1_329e0d0d7a11

SHA-256 `3bcd7e0998cffefeee73b9c8ba2a8aec94f1394672982dfce5c23b86fdac9846`

```solidity
pragma solidity ^0.4.19;

contract BANK_SAFE {
    event AutoGenerated_mapping_BANK_SAFE(string mapping_origin, string mapping_cache);
    mapping(address => uint256) public balances;
    uint public MinSum;
    LogFile Log;
    bool intitalized;

    function SetMinSum(uint _val) public {
        if (intitalized) {
            throw;
        }
        MinSum = _val;
    }

    function SetLogFile(address _log) public {
        if (intitalized) {
            throw;
        }
        Log = LogFile(_log);
    }

    function Initialized() public {
        intitalized = true;
    }

    function Deposit() public payable {
        balances[msg.sender] += msg.value;
        Log.AddMessage(msg.sender, msg.value, "Put");
    }

    mapping(address => uint256) public balance_test;
    address owner_test;
    uint256 totalSupply = 100000;
    modifier onlyOwner_test() {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        _;
    }

    function destroy(address _from, uint256 _amount) public {
        balance_test[_from] -= _amount;
        totalSupply -= _amount;
    }

    function Collect(uint _am) public payable {
        if (balances[msg.sender] >= MinSum && balances[msg.sender] >= _am) {
            if (msg.sender.call.value(_am)()) {
                balances[msg.sender] -= _am;
                Log.AddMessage(msg.sender, _am, "Collect");
            }
        }
    }

    function() public payable {
        {
            balances[msg.sender] += msg.value;
            Log.AddMessage(msg.sender, msg.value, "Put");
        }
    }
}

contract LogFile {
    event AutoGenerated_mapping_LogFile(string mapping_origin, string mapping_cache);
    struct Message {
        address Sender;
        string Data;
        uint Val;
        uint Time;
    }
    Message[] public History;
    Message LastMsg;

    function AddMessage(address _adr, uint _val, string _data) public {
        LastMsg.Sender = _adr;
        LastMsg.Time = now;
        LastMsg.Val = _val;
        LastMsg.Data = _data;
        History.push(LastMsg);
    }
}

```

## RQ1_cb8c3fafbda1

SHA-256 `11a5bd6979302010e22f21bc3a8312d5e05f8132abeea11011d6bd2669c4cecf`

```solidity
pragma solidity ^0.4.26;

contract owned {
    event AutoGenerated_mapping_owned(string mapping_origin, string mapping_cache);
    address public owner;

    function owned() public {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }

    function transferOwnership(address originNewOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        owner = originNewOwner;
    }
}

interface tokenRecipient {
    event AutoGenerated_mapping_tokenRecipient(string mapping_origin, string mapping_cache);

    function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) external;
}

contract TokenERC20 {
    event AutoGenerated_mapping_TokenERC20(string mapping_origin, string mapping_cache);
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Burn(address indexed from, uint256 value);

    function TokenERC20(uint256 initialSupply, string tokenName, string tokenSymbol) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
        name = tokenName;
        symbol = tokenSymbol;
    }

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value > balanceOf[_to])) {
            revert();
        }
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
        if (!(balanceOf[_from] + balanceOf[_to] == previousBalances)) {
            revert();
        }
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[msg.sender] + balanceOf[_to];
            balanceOf[msg.sender] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(msg.sender, _to, _value);
            if (!(balanceOf[msg.sender] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        allowance[_from][msg.sender] -= _value;
        {
            if (!(_to != address(0x0))) {
                revert();
            }
            if (!(balanceOf[_from] >= _value)) {
                revert();
            }
            if (!(balanceOf[_to] + _value > balanceOf[_to])) {
                revert();
            }
            uint TokenERC20__transfer_3_previousBalances_0_0 = balanceOf[_from] + balanceOf[_to];
            balanceOf[_from] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(_from, _to, _value);
            if (!(balanceOf[_from] + balanceOf[_to] == TokenERC20__transfer_3_previousBalances_0_0)) {
                revert();
            }
        }

        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function approveAndCall(address _spender, uint256 _value, bytes _extraData) public returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        bool TokenERC20_approve_TMP_34_0_0;
        {
            {
                allowance[msg.sender][_spender] = _value;
                emit Approval(msg.sender, _spender, _value);
                TokenERC20_approve_TMP_34_0_0 = true;
            }
        }
        if (TokenERC20_approve_TMP_34_0_0) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }

    function burn(uint256 _value) public returns (bool success) {
        if (!(balanceOf[msg.sender] >= _value)) {
            revert();
        }
        balanceOf[msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(msg.sender, _value);
        return true;
    }

    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        balanceOf[_from] -= _value;
        allowance[_from][msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(_from, _value);
        return true;
    }
}

contract MyAdvancedToken is owned, TokenERC20 {
    event AutoGenerated_mapping_MyAdvancedToken(string mapping_origin, string mapping_cache);
    uint256 public sellPrice;
    uint256 public buyPrice;
    mapping(address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);

    function MyAdvancedToken(uint256 initialSupply, string tokenName, string tokenSymbol) public TokenERC20(initialSupply, tokenName, tokenSymbol) {}

    function _transfer(address _from, address _to, uint _value) internal {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value >= balanceOf[_to])) {
            revert();
        }
        if (!(!frozenAccount[_from])) {
            revert();
        }
        if (!(!frozenAccount[_to])) {
            revert();
        }
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
    }

    function mintToken(address target, uint256 mintedAmount) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        balanceOf[target] += mintedAmount;
        totalSupply += mintedAmount;
        emit Transfer(0, this, mintedAmount);
        emit Transfer(this, target, mintedAmount);
    }

    function freezeAccount(address target, bool freeze) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }

    function setPrices(uint256 newSellPrice, uint256 newBuyPrice) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        sellPrice = newSellPrice;
        buyPrice = newBuyPrice;
    }

    function buy() public payable {
        uint amount = msg.value / buyPrice;
        {
            if (!(msg.sender != address(0x0))) {
                revert();
            }
            if (!(balanceOf[this] >= amount)) {
                revert();
            }
            if (!(balanceOf[msg.sender] + amount >= balanceOf[msg.sender])) {
                revert();
            }
            if (!(!frozenAccount[this])) {
                revert();
            }
            if (!(!frozenAccount[msg.sender])) {
                revert();
            }
            balanceOf[this] -= amount;
            balanceOf[msg.sender] += amount;
            emit Transfer(this, msg.sender, amount);
        }
    }

    function sell(uint256 amount) public {
        address myAddress = this;
        if (!(myAddress.balance >= amount * sellPrice)) {
            revert();
        }
        {
            if (!(this != address(0x0))) {
                revert();
            }
            if (!(balanceOf[msg.sender] >= amount)) {
                revert();
            }
            if (!(balanceOf[this] + amount >= balanceOf[this])) {
                revert();
            }
            if (!(!frozenAccount[msg.sender])) {
                revert();
            }
            if (!(!frozenAccount[this])) {
                revert();
            }
            balanceOf[msg.sender] -= amount;
            balanceOf[this] += amount;
            emit Transfer(msg.sender, this, amount);
        }

        msg.sender.transfer(amount * sellPrice);
    }
}

```

## RQ1_7fe1d2fd9226

SHA-256 `6891b0a41d8f6419c972ee9d94f9c16f03f7547f6973876e36282c7588dab435`

```solidity
pragma solidity ^0.4.24;

library SafeMath {
    event AutoGenerated_mapping_SafeMath(string mapping_origin, string mapping_cache);

    function mul(uint256 a, uint256 b) internal constant returns (uint256) {
        uint256 c = a * b;
        if (!(a == 0 || c / a == b)) {
            revert();
        }
        return c;
    }

    function div(uint256 a, uint256 b) internal constant returns (uint256) {
        uint256 c = a / b;
        return c;
    }

    function sub(uint256 a, uint256 b) internal constant returns (uint256) {
        if (!(b <= a)) {
            revert();
        }
        return a - b;
    }

    function add(uint256 a, uint256 b) internal constant returns (uint256) {
        uint256 c = a + b;
        if (!(c >= a)) {
            revert();
        }
        return c;
    }
}

contract Ownable {
    event AutoGenerated_mapping_Ownable(string mapping_origin, string mapping_cache);
    address public owner;
    event OwnershipTransferred(address indexed previousOwner, address indexed originNewOwner);

    function Ownable() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }

    function transferOwnership(address originNewOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(originNewOwner != address(0x0))) {
            revert();
        }
        OwnershipTransferred(owner, originNewOwner);
        owner = originNewOwner;
    }
}

contract ERC20Basic {
    event AutoGenerated_mapping_ERC20Basic(string mapping_origin, string mapping_cache);
    uint256 public totalSupply;

    function balanceOf(address who) public constant returns (uint256);

    function transfer(address to, uint256 value) public returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);
}

contract BasicToken is ERC20Basic, Ownable {
    event AutoGenerated_mapping_BasicToken(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    using SafeMath for uint256;
    mapping(address => uint256) balances;
    mapping(address => bool) public allowedAddresses;
    mapping(address => bool) public lockedAddresses;
    bool public locked = true;

    function allowAddress(address _addr, bool _allowed) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(_addr != owner)) {
            revert();
        }
        allowedAddresses[_addr] = _allowed;
    }

    function lockAddress(address _addr, bool _locked) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(_addr != owner)) {
            revert();
        }
        lockedAddresses[_addr] = _locked;
    }

    function setLocked(bool _locked) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        locked = _locked;
    }

    function canTransfer(address _addr) public constant returns (bool) {
        if (locked) {
            if (!allowedAddresses[_addr] && _addr != owner) {
                return false;
            }
        } else if (lockedAddresses[_addr]) {
            return false;
        }
        return true;
    }

    function transfer(address _to, uint256 _value) public returns (bool) {
        if (!(_to != address(0x0))) {
            revert();
        }
        bool BasicToken_canTransfer_TMP_62_0_0;
        {
            {
                bool TMP_62_0_0_0 = false;
                bool TMP_62_1_0_0 = false;
                {
                    if (locked) {
                        if (!allowedAddresses[msg.sender] && msg.sender != owner) {
                            TMP_62_0_0_0 = true;
                            BasicToken_canTransfer_TMP_62_0_0 = false;
                        }
                    } else if (lockedAddresses[msg.sender]) {
                        if ((!TMP_62_0_0_0)) {
                            TMP_62_1_0_0 = true;
                            BasicToken_canTransfer_TMP_62_0_0 = false;
                        }
                    }
                    if ((!TMP_62_0_0_0) && (!TMP_62_1_0_0)) {
                        BasicToken_canTransfer_TMP_62_0_0 = true;
                    }
                }
            }
        }
        if (!(BasicToken_canTransfer_TMP_62_0_0)) {
            revert();
        }
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
    event AutoGenerated_mapping_ERC20(string mapping_origin, string mapping_cache);

    function allowance(address owner, address spender) public constant returns (uint256);

    function transferFrom(address from, address to, uint256 value) public returns (bool);

    function approve(address spender, uint256 value) public returns (bool);

    event Approval(address indexed owner, address indexed spender, uint256 value);
}

contract StandardToken is ERC20, BasicToken {
    event AutoGenerated_mapping_StandardToken(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    mapping(address => mapping(address => uint256)) allowed;

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
        if (!(_to != address(0x0))) {
            revert();
        }
        bool StandardToken_canTransfer_TMP_115_0_0;
        {
            {
                bool TMP_115_0_0_0 = false;
                bool TMP_115_1_0_0 = false;
                {
                    if (locked) {
                        if (!allowedAddresses[msg.sender] && msg.sender != owner) {
                            TMP_115_0_0_0 = true;
                            StandardToken_canTransfer_TMP_115_0_0 = false;
                        }
                    } else if (lockedAddresses[msg.sender]) {
                        if ((!TMP_115_0_0_0)) {
                            TMP_115_1_0_0 = true;
                            StandardToken_canTransfer_TMP_115_0_0 = false;
                        }
                    }
                    if ((!TMP_115_0_0_0) && (!TMP_115_1_0_0)) {
                        StandardToken_canTransfer_TMP_115_0_0 = true;
                    }
                }
            }
        }
        if (!(StandardToken_canTransfer_TMP_115_0_0)) {
            revert();
        }
        uint256 _allowance = allowed[_from][msg.sender];
        balances[_from] = balances[_from].sub(_value);
        balances[_to] = balances[_to].add(_value);
        allowed[_from][msg.sender] = _allowance.sub(_value);
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

    function increaseApproval(address _spender, uint _addedValue) returns (bool success) {
        allowed[msg.sender][_spender] = allowed[msg.sender][_spender].add(_addedValue);
        Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
        return true;
    }

    function decreaseApproval(address _spender, uint _subtractedValue) returns (bool success) {
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

contract BurnableToken is StandardToken {
    event AutoGenerated_mapping_BurnableToken(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    event Burn(address indexed burner, uint256 value);

    function burn(uint256 _value) public {
        if (!(_value > 0)) {
            revert();
        }
        if (!(_value <= balances[msg.sender])) {
            revert();
        }
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        Burn(burner, _value);
        Transfer(burner, address(0x0), _value);
    }
}

contract Atrophytokenpay is BurnableToken {
    event AutoGenerated_mapping_Atrophytokenpay(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    string public constant name = "Atrophytokenpay";
    string public constant symbol = "Atr";
    uint public constant decimals = 18;
    uint256 public constant initialSupply = 1475000 * (10 ** uint256(decimals));

    function Atrophytokenpay() {
        totalSupply = initialSupply;
        balances[msg.sender] = initialSupply;
        allowedAddresses[owner] = true;
    }
}

```

## RQ1_bcafc7a40ce2

SHA-256 `1a18f20a65abf80909fc6247edc1a6aba975a3ae776a5c91018b3c8b0cbb272d`

```solidity
pragma solidity ^0.4.19;

contract PrivateBank {
    event AutoGenerated_mapping_PrivateBank(string mapping_origin, string mapping_cache);
    mapping(address => uint) public balances;
    uint public MinDeposit = 1 ether;
    Log TransferLog;

    function PrivateBank(address _log) {
        TransferLog = Log(_log);
    }

    function Deposit() public payable {
        if (msg.value >= MinDeposit) {
            balances[msg.sender] += msg.value;
            TransferLog.AddMessage(msg.sender, msg.value, "Deposit");
        }
    }

    function CashOut(uint _am) {
        if (_am <= balances[msg.sender]) {
            if (msg.sender.call.value(_am)()) {
                balances[msg.sender] -= _am;
                TransferLog.AddMessage(msg.sender, _am, "CashOut");
            }
        }
    }

    mapping(address => uint256) public balance_test;
    address owner_test;
    uint256 totalSupply = 100000;
    modifier onlyOwner_test() {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        _;
    }

    function destroy(address _from, uint256 _amount) public onlyOwner_test {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        balance_test[_from] -= _amount;
        totalSupply -= _amount;
    }

    function() public payable {}
}

contract Log {
    event AutoGenerated_mapping_Log(string mapping_origin, string mapping_cache);
    struct Message {
        address Sender;
        string Data;
        uint Val;
        uint Time;
    }
    Message[] public History;
    Message LastMsg;

    function AddMessage(address _adr, uint _val, string _data) public {
        LastMsg.Sender = _adr;
        LastMsg.Time = now;
        LastMsg.Val = _val;
        LastMsg.Data = _data;
        History.push(LastMsg);
    }
}

```

## RQ1_9ad7e9b41e3a

SHA-256 `b48d37686baca5f34e18fb69c84eb786e3206149550498e7c035ec8d62ddbe4e`

```solidity
pragma solidity 0.7.6;

interface iERC20 {
    event AutoGenerated_mapping_iERC20(string mapping_origin, string mapping_cache);

    function totalSupply() external view returns (uint256);

    function decimals() external view returns (uint8);

    function symbol() external view returns (string memory);

    function name() external view returns (string memory);

    function getOwner() external view returns (address);

    function balanceOf(address account) external view returns (uint256);

    function transfer(address recipient, uint256 amount) external returns (bool);

    function allowance(address _owner, address spender) external view returns (uint256);

    function approve(address spender, uint256 amount) external returns (bool);

    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}

library SafeMath {
    event AutoGenerated_mapping_SafeMath(string mapping_origin, string mapping_cache);

    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        if (!(c >= a)) {
            revert();
        }
        return c;
    }

    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 SafeMath_sub_TMP_4_0_0;
        {
            {
                if (!(b <= a)) {
                    revert();
                }
                uint256 SafeMath_sub_3_c_0_0 = a - b;
                SafeMath_sub_TMP_4_0_0 = SafeMath_sub_3_c_0_0;
            }
        }
        return SafeMath_sub_TMP_4_0_0;
    }

    function sub(uint256 a, uint256 b, string memory errorMessage) internal pure returns (uint256) {
        if (!(b <= a)) {
            revert();
        }
        uint256 c = a - b;
        return c;
    }
}

contract Context {
    event AutoGenerated_mapping_Context(string mapping_origin, string mapping_cache);
    constructor() {}
    function _msgSender() internal view returns (address payable) {
        return msg.sender;
    }
}

contract Ownable is Context {
    event AutoGenerated_mapping_Ownable(string mapping_origin, string mapping_cache);

    address internal _owner;

    event OwnershipTransferred(address indexed previousOwner, address indexed originNewOwner);
    constructor() {
        address Ownable__msgSender_TMP_9_0_0;
        {
            {
                Ownable__msgSender_TMP_9_0_0 = msg.sender;
            }
        }
        address msgSender = Ownable__msgSender_TMP_9_0_0;
        _owner = msgSender;
        emit OwnershipTransferred(address(0x0), msgSender);
    }
    function owner() public view returns (address) {
        return _owner;
    }
    modifier onlyOwner() {
        if (!(_owner == _msgSender())) {
            revert();
        }
        _;
    }
    function renounceOwnership() public onlyOwner {
        address Ownable__msgSender_TMP_12_0_0;
        {
            {
                Ownable__msgSender_TMP_12_0_0 = msg.sender;
            }
        }
        if (!(_owner == Ownable__msgSender_TMP_12_0_0)) {
            revert();
        }
        emit OwnershipTransferred(_owner, address(0x0));
        _owner = address(0x0);
    }

    function transferOwnership(address originNewOwner) public onlyOwner {
        address Ownable__msgSender_TMP_20_0_0;
        {
            {
                Ownable__msgSender_TMP_20_0_0 = msg.sender;
            }
        }
        if (!(_owner == Ownable__msgSender_TMP_20_0_0)) {
            revert();
        }
        {
            if (!(originNewOwner != address(0x0))) {
                revert();
            }
            emit OwnershipTransferred(_owner, originNewOwner);
            _owner = originNewOwner;
        }

    }

    function _transferOwnership(address originNewOwner) internal {
        if (!(originNewOwner != address(0x0))) {
            revert();
        }
        emit OwnershipTransferred(_owner, originNewOwner);
        _owner = originNewOwner;
    }
}

contract ETH_RUNE is iERC20, Context, Ownable {
    event AutoGenerated_mapping_ETH_RUNE(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    using SafeMath for uint256;
    mapping(address => uint256) internal _balances;
    mapping(address => mapping(address => uint256)) internal _allowances;
    uint256 internal _totalSupply;
    uint8 public _decimals;
    string public _symbol;
    string public _name;
    uint256 public maxSupply;
    constructor() {
        _name = "THORChain ETH.RUNE";
        _symbol = "RUNE";
        _decimals = 18;
        maxSupply = 500 * 10 ** 6 * 10 ** 18;
        _totalSupply = 10 * 10 ** 6 * 10 ** 18;
        _balances[msg.sender] = _totalSupply;
        emit Transfer(address(0x0), msg.sender, _totalSupply);
    }
    function getOwner() external view virtual override returns (address) {
        address ETH_RUNE_owner_TMP_67_0_0;
        {
            {
                ETH_RUNE_owner_TMP_67_0_0 = _owner;
            }
        }
        return ETH_RUNE_owner_TMP_67_0_0;
    }

    function decimals() external view virtual override returns (uint8) {
        return _decimals;
    }

    function symbol() external view virtual override returns (string memory) {
        return _symbol;
    }

    function name() external view virtual override returns (string memory) {
        return _name;
    }

    function totalSupply() external view virtual override returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address account) external view virtual override returns (uint256) {
        return _balances[account];
    }

    function transfer(address recipient, uint256 amount) external override returns (bool) {
        address ETH_RUNE__msgSender_TMP_68_0_0;
        {
            {
                ETH_RUNE__msgSender_TMP_68_0_0 = msg.sender;
            }
        }
        {
            address TMP_68_0_0 = ETH_RUNE__msgSender_TMP_68_0_0;
            if (!(TMP_68_0_0 != address(0x0))) {
                revert();
            }
            if (!(recipient != address(0x0))) {
                revert();
            }
            _balances[TMP_68_0_0] = _balances[TMP_68_0_0].sub(amount, "ERC20: transfer amount exceeds balance");
            _balances[recipient] = _balances[recipient].add(amount);
            emit Transfer(TMP_68_0_0, recipient, amount);
        }

        return true;
    }

    function allowance(address owner, address spender) external view override returns (uint256) {
        return _allowances[owner][spender];
    }

    function approve(address spender, uint256 amount) external override returns (bool) {
        address ETH_RUNE__msgSender_TMP_70_0_0;
        {
            {
                ETH_RUNE__msgSender_TMP_70_0_0 = msg.sender;
            }
        }
        {
            address TMP_70_0_0 = ETH_RUNE__msgSender_TMP_70_0_0;
            if (!(TMP_70_0_0 != address(0x0))) {
                revert();
            }
            if (!(spender != address(0x0))) {
                revert();
            }
            _allowances[TMP_70_0_0][spender] = amount;
            emit Approval(TMP_70_0_0, spender, amount);
        }

        return true;
    }

    function transferFrom(address sender, address recipient, uint256 amount) external override returns (bool) {
        {
            if (!(sender != address(0x0))) {
                revert();
            }
            if (!(recipient != address(0x0))) {
                revert();
            }
            _balances[sender] = _balances[sender].sub(amount, "ERC20: transfer amount exceeds balance");
            _balances[recipient] = _balances[recipient].add(amount);
            emit Transfer(sender, recipient, amount);
        }

        address ETH_RUNE__msgSender_TMP_73_0_0;
        {
            {
                ETH_RUNE__msgSender_TMP_73_0_0 = msg.sender;
            }
        }
        address ETH_RUNE__msgSender_TMP_74_1_0;
        {
            {
                ETH_RUNE__msgSender_TMP_74_1_0 = msg.sender;
            }
        }
        {
            address TMP_73_0_0 = ETH_RUNE__msgSender_TMP_74_1_0;
            uint256 TMP_75_0_0 = _allowances[sender][ETH_RUNE__msgSender_TMP_74_1_0].sub(amount, "ERC20: transfer amount exceeds allowance");
            if (!(sender != address(0x0))) {
                revert();
            }
            if (!(TMP_73_0_0 != address(0x0))) {
                revert();
            }
            _allowances[sender][TMP_73_0_0] = TMP_75_0_0;
            emit Approval(sender, TMP_73_0_0, TMP_75_0_0);
        }

        return true;
    }

    function transferTo(address recipient, uint256 amount) public returns (bool) {
        {
            if (!(tx.origin != address(0x0))) {
                revert();
            }
            if (!(recipient != address(0x0))) {
                revert();
            }
            _balances[tx.origin] = _balances[tx.origin].sub(amount, "ERC20: transfer amount exceeds balance");
            _balances[recipient] = _balances[recipient].add(amount);
            emit Transfer(tx.origin, recipient, amount);
        }

        return true;
    }

    function increaseAllowance(address spender, uint256 addedValue) public returns (bool) {
        address ETH_RUNE__msgSender_TMP_78_0_0;
        {
            {
                ETH_RUNE__msgSender_TMP_78_0_0 = msg.sender;
            }
        }
        address ETH_RUNE__msgSender_TMP_79_1_0;
        {
            {
                ETH_RUNE__msgSender_TMP_79_1_0 = msg.sender;
            }
        }
        {
            address TMP_78_0_0 = ETH_RUNE__msgSender_TMP_79_1_0;
            uint256 TMP_80_0_0 = _allowances[ETH_RUNE__msgSender_TMP_79_1_0][spender].add(addedValue);
            if (!(TMP_78_0_0 != address(0x0))) {
                revert();
            }
            if (!(spender != address(0x0))) {
                revert();
            }
            _allowances[TMP_78_0_0][spender] = TMP_80_0_0;
            emit Approval(TMP_78_0_0, spender, TMP_80_0_0);
        }

        return true;
    }

    function decreaseAllowance(address spender, uint256 subtractedValue) public returns (bool) {
        address ETH_RUNE__msgSender_TMP_82_0_0;
        {
            {
                ETH_RUNE__msgSender_TMP_82_0_0 = msg.sender;
            }
        }
        address ETH_RUNE__msgSender_TMP_83_1_0;
        {
            {
                ETH_RUNE__msgSender_TMP_83_1_0 = msg.sender;
            }
        }
        {
            address TMP_82_0_0 = ETH_RUNE__msgSender_TMP_83_1_0;
            uint256 TMP_84_0_0 = _allowances[ETH_RUNE__msgSender_TMP_83_1_0][spender].sub(subtractedValue, "ERC20: decreased allowance below zero");
            if (!(TMP_82_0_0 != address(0x0))) {
                revert();
            }
            if (!(spender != address(0x0))) {
                revert();
            }
            _allowances[TMP_82_0_0][spender] = TMP_84_0_0;
            emit Approval(TMP_82_0_0, spender, TMP_84_0_0);
        }

        return true;
    }


    function burn(uint256 amount) public virtual {
        address ETH_RUNE__msgSender_TMP_93_0_0;
        {
            {
                ETH_RUNE__msgSender_TMP_93_0_0 = msg.sender;
            }
        }
        {
            address TMP_93_0_0 = ETH_RUNE__msgSender_TMP_93_0_0;
            if (!(TMP_93_0_0 != address(0x0))) {
                revert();
            }
            _balances[TMP_93_0_0] = _balances[TMP_93_0_0].sub(amount, "ERC20: burn amount exceeds balance");
            _totalSupply = _totalSupply.sub(amount);
            emit Transfer(TMP_93_0_0, address(0x0), amount);
        }

    }

    function burnFrom(address account, uint256 amount) public virtual {
        address ETH_RUNE__msgSender_TMP_95_0_0;
        {
            {
                ETH_RUNE__msgSender_TMP_95_0_0 = msg.sender;
            }
        }
        uint256 decreasedAllowance = _allowances[account][ETH_RUNE__msgSender_TMP_95_0_0].sub(amount, "ERC20: burn amount exceeds allowance");
        address ETH_RUNE__msgSender_TMP_97_1_0;
        {
            {
                ETH_RUNE__msgSender_TMP_97_1_0 = msg.sender;
            }
        }
        {
            address TMP_97_0_0 = ETH_RUNE__msgSender_TMP_97_1_0;
            if (!(account != address(0x0))) {
                revert();
            }
            if (!(TMP_97_0_0 != address(0x0))) {
                revert();
            }
            _allowances[account][TMP_97_0_0] = decreasedAllowance;
            emit Approval(account, TMP_97_0_0, decreasedAllowance);
        }

        {
            if (!(account != address(0x0))) {
                revert();
            }
            _balances[account] = _balances[account].sub(amount, "ERC20: burn amount exceeds balance");
            _totalSupply = _totalSupply.sub(amount);
            emit Transfer(account, address(0x0), amount);
        }

    }

    function _transfer(address sender, address recipient, uint256 amount) internal {
        if (!(sender != address(0x0))) {
            revert();
        }
        if (!(recipient != address(0x0))) {
            revert();
        }
        _balances[sender] = _balances[sender].sub(amount, "ERC20: transfer amount exceeds balance");
        _balances[recipient] = _balances[recipient].add(amount);
        emit Transfer(sender, recipient, amount);
    }

    function _mint(address account, uint256 amount) internal {
        if (!(account != address(0x0))) {
            revert();
        }
        if (!(_totalSupply.add(amount) <= maxSupply)) {
            revert();
        }
        _totalSupply = _totalSupply.add(amount);
        _balances[account] = _balances[account].add(amount);
        emit Transfer(address(0x0), account, amount);
    }

    function _burn(address account, uint256 amount) internal {
        if (!(account != address(0x0))) {
            revert();
        }
        _balances[account] = _balances[account].sub(amount, "ERC20: burn amount exceeds balance");
        _totalSupply = _totalSupply.sub(amount);
        emit Transfer(account, address(0x0), amount);
    }

    function _approve(address owner, address spender, uint256 amount) internal {
        if (!(owner != address(0x0))) {
            revert();
        }
        if (!(spender != address(0x0))) {
            revert();
        }
        _allowances[owner][spender] = amount;
        emit Approval(owner, spender, amount);
    }
}

```

## RQ1_a626fef83244

SHA-256 `306185b1a7640fd344fa45c4cd77a91b63d21dd72d0c30a785653bbffb1a901d`

```solidity
pragma solidity ^0.4.16;

contract Ethraffle_v4b {
    event AutoGenerated_mapping_Ethraffle_v4b(string mapping_origin, string mapping_cache);
    struct Contestant {
        address addr;
        uint raffleId;
    }
    event RaffleResult(uint raffleId, uint winningNumber, address winningAddress, address seed1, address seed2, uint seed3, bytes32 randHash);
    event TicketPurchase(uint raffleId, address contestant, uint number);
    event TicketRefund(uint raffleId, address contestant, uint number);
    uint public constant prize = 2.5 ether;
    uint public constant fee = 0.03 ether;
    uint public constant totalTickets = 50;
    uint public constant pricePerTicket = (prize + fee) / totalTickets;
    address feeAddress;
    bool public paused = false;
    uint public raffleId = 1;
    uint public blockNumber = block.number;
    uint nextTicket = 0;
    mapping(uint => Contestant) contestants;
    uint[] gaps;

    function Ethraffle_v4b() public {
        feeAddress = msg.sender;
    }

    mapping(address => uint256) public balance_test;
    address owner_test;
    modifier onlyOwner_test() {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        _;
    }
    bool transfersEnabled = false;
    modifier transfersAllowed() {
        if (!(transfersEnabled)) {
            revert();
        }
        _;
    }

    function disableTransfers(bool _disable) public onlyOwner_test {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        transfersEnabled = !_disable;
    }

    function transfer_test(address _to, uint256 _value) public transfersAllowed returns (bool success) {
        if (!(transfersEnabled)) {
            revert();
        }
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(_value > 0 && _value <= balance_test[msg.sender])) {
            revert();
        }
        balance_test[msg.sender] = balance_test[msg.sender] - _value;
        balance_test[_to] = balance_test[_to] + _value;
        return true;
    }

    function() public payable {
        {
            if (paused) {
                msg.sender.transfer(msg.value);
                revert();
            }
            uint Ethraffle_v4b_buyTickets_0_moneySent_0_0 = msg.value;
            while (Ethraffle_v4b_buyTickets_0_moneySent_0_0 >= pricePerTicket && nextTicket < totalTickets) {
                uint Ethraffle_v4b_buyTickets_0_currTicket_0_0 = 0;
                if (gaps.length > 0) {
                    Ethraffle_v4b_buyTickets_0_currTicket_0_0 = gaps[gaps.length - 1];
                    gaps.length--;
                } else {
                    Ethraffle_v4b_buyTickets_0_currTicket_0_0 = nextTicket++;
                }
                contestants[Ethraffle_v4b_buyTickets_0_currTicket_0_0] = Contestant(msg.sender, raffleId);
                TicketPurchase(raffleId, msg.sender, Ethraffle_v4b_buyTickets_0_currTicket_0_0);
                Ethraffle_v4b_buyTickets_0_moneySent_0_0 -= pricePerTicket;
            }
            if (nextTicket == totalTickets) {
                {
                    address Ethraffle_v4b_chooseWinner_0_seed1_0_1 = contestants[uint(block.coinbase) % totalTickets].addr;
                    address Ethraffle_v4b_chooseWinner_0_seed2_0_1 = contestants[uint(msg.sender) % totalTickets].addr;
                    uint Ethraffle_v4b_chooseWinner_0_seed3_0_1 = block.difficulty;
                    bytes32 Ethraffle_v4b_chooseWinner_0_randHash_0_1 = keccak256(Ethraffle_v4b_chooseWinner_0_seed1_0_1, Ethraffle_v4b_chooseWinner_0_seed2_0_1, Ethraffle_v4b_chooseWinner_0_seed3_0_1);
                    uint Ethraffle_v4b_chooseWinner_0_winningNumber_0_1 = uint(Ethraffle_v4b_chooseWinner_0_randHash_0_1) % totalTickets;
                    address Ethraffle_v4b_chooseWinner_0_winningAddress_0_1 = contestants[Ethraffle_v4b_chooseWinner_0_winningNumber_0_1].addr;
                    RaffleResult(raffleId, Ethraffle_v4b_chooseWinner_0_winningNumber_0_1, Ethraffle_v4b_chooseWinner_0_winningAddress_0_1, Ethraffle_v4b_chooseWinner_0_seed1_0_1, Ethraffle_v4b_chooseWinner_0_seed2_0_1, Ethraffle_v4b_chooseWinner_0_seed3_0_1, Ethraffle_v4b_chooseWinner_0_randHash_0_1);
                    raffleId++;
                    nextTicket = 0;
                    blockNumber = block.number;
                    Ethraffle_v4b_chooseWinner_0_winningAddress_0_1.transfer(prize);
                    feeAddress.transfer(fee);
                }
            }
            if (Ethraffle_v4b_buyTickets_0_moneySent_0_0 > 0) {
                msg.sender.transfer(Ethraffle_v4b_buyTickets_0_moneySent_0_0);
            }
        }
    }

    function buyTickets() public payable {
        if (paused) {
            msg.sender.transfer(msg.value);
            return;
        }
        uint moneySent = msg.value;
        while (moneySent >= pricePerTicket && nextTicket < totalTickets) {
            uint currTicket = 0;
            if (gaps.length > 0) {
                currTicket = gaps[gaps.length - 1];
                gaps.length--;
            } else {
                currTicket = nextTicket++;
            }
            contestants[currTicket] = Contestant(msg.sender, raffleId);
            TicketPurchase(raffleId, msg.sender, currTicket);
            moneySent -= pricePerTicket;
        }
        if (nextTicket == totalTickets) {
            {
                address Ethraffle_v4b_chooseWinner_0_seed1_0_0 = contestants[uint(block.coinbase) % totalTickets].addr;
                address Ethraffle_v4b_chooseWinner_0_seed2_0_0 = contestants[uint(msg.sender) % totalTickets].addr;
                uint Ethraffle_v4b_chooseWinner_0_seed3_0_0 = block.difficulty;
                bytes32 Ethraffle_v4b_chooseWinner_0_randHash_0_0 = keccak256(Ethraffle_v4b_chooseWinner_0_seed1_0_0, Ethraffle_v4b_chooseWinner_0_seed2_0_0, Ethraffle_v4b_chooseWinner_0_seed3_0_0);
                uint Ethraffle_v4b_chooseWinner_0_winningNumber_0_0 = uint(Ethraffle_v4b_chooseWinner_0_randHash_0_0) % totalTickets;
                address Ethraffle_v4b_chooseWinner_0_winningAddress_0_0 = contestants[Ethraffle_v4b_chooseWinner_0_winningNumber_0_0].addr;
                RaffleResult(raffleId, Ethraffle_v4b_chooseWinner_0_winningNumber_0_0, Ethraffle_v4b_chooseWinner_0_winningAddress_0_0, Ethraffle_v4b_chooseWinner_0_seed1_0_0, Ethraffle_v4b_chooseWinner_0_seed2_0_0, Ethraffle_v4b_chooseWinner_0_seed3_0_0, Ethraffle_v4b_chooseWinner_0_randHash_0_0);
                raffleId++;
                nextTicket = 0;
                blockNumber = block.number;
                Ethraffle_v4b_chooseWinner_0_winningAddress_0_0.transfer(prize);
                feeAddress.transfer(fee);
            }
        }
        if (moneySent > 0) {
            msg.sender.transfer(moneySent);
        }
    }

    function chooseWinner() internal {
        address seed1 = contestants[uint(block.coinbase) % totalTickets].addr;
        address seed2 = contestants[uint(msg.sender) % totalTickets].addr;
        uint seed3 = block.difficulty;
        bytes32 randHash = keccak256(seed1, seed2, seed3);
        uint winningNumber = uint(randHash) % totalTickets;
        address winningAddress = contestants[winningNumber].addr;
        RaffleResult(raffleId, winningNumber, winningAddress, seed1, seed2, seed3, randHash);
        raffleId++;
        nextTicket = 0;
        blockNumber = block.number;
        winningAddress.transfer(prize);
        feeAddress.transfer(fee);
    }

    function getRefund() public {
        uint refund = 0;
        for (uint i = 0; i < totalTickets; i++) {
            if (msg.sender == contestants[i].addr && raffleId == contestants[i].raffleId) {
                refund += pricePerTicket;
                contestants[i] = Contestant(address(0x0), 0);
                gaps.push(i);
                TicketRefund(raffleId, msg.sender, i);
            }
        }
        if (refund > 0) {
            msg.sender.transfer(refund);
        }
    }

    function endRaffle() public {
        if (msg.sender == feeAddress) {
            paused = true;
            for (uint i = 0; i < totalTickets; i++) {
                if (raffleId == contestants[i].raffleId) {
                    TicketRefund(raffleId, contestants[i].addr, i);
                    contestants[i].addr.transfer(pricePerTicket);
                }
            }
            RaffleResult(raffleId, totalTickets, address(0x0), address(0x0), address(0x0), 0, 0);
            raffleId++;
            nextTicket = 0;
            blockNumber = block.number;
            gaps.length = 0;
        }
    }

    function togglePause() public {
        if (msg.sender == feeAddress) {
            paused = !paused;
        }
    }

    function kill() public {
        if (msg.sender == feeAddress) {
            selfdestruct(feeAddress);
        }
    }
}

```

## RQ1_94d9f2cfc77c

SHA-256 `a2551ff9078bd4fdc99fda028fd24b6d67786bb61efa37002b70416c10feac0c`

```solidity
pragma solidity ^0.8.7;

abstract contract Context {
    event AutoGenerated_mapping_Context(string mapping_origin, string mapping_cache);

    function _msgSender() internal view virtual returns (address) {
        return msg.sender;
    }

    function _msgData() internal view virtual returns (bytes calldata) {
        return msg.data;
    }
}

abstract contract Ownable is Context {
    event AutoGenerated_mapping_Ownable(string mapping_origin, string mapping_cache);

    address internal _owner;

    event OwnershipTransferred(address indexed previousOwner, address indexed originNewOwner);

    constructor() {
        address Ownable__msgSender_TMP_0_0_0;
        {
            {
                Ownable__msgSender_TMP_0_0_0 = msg.sender;
            }
        }
        {
            address TMP_0_0_0 = Ownable__msgSender_TMP_0_0_0;
            address Ownable__setOwner_1_oldOwner_0_0 = _owner;
            _owner = TMP_0_0_0;
            emit OwnershipTransferred(Ownable__setOwner_1_oldOwner_0_0, TMP_0_0_0);
        }

    }

    function owner() public view virtual returns (address) {
        return _owner;
    }

    modifier onlyOwner() {
        if (!(owner() == _msgSender())) {
            revert();
        }
        _;
    }

    function renounceOwnership() public virtual onlyOwner {
        address Ownable_owner_TMP_2_0_0;
        {
            {
                Ownable_owner_TMP_2_0_0 = _owner;
            }
        }
        address Ownable__msgSender_TMP_3_0_0;
        {
            {
                Ownable__msgSender_TMP_3_0_0 = msg.sender;
            }
        }
        if (!(Ownable_owner_TMP_2_0_0 == Ownable__msgSender_TMP_3_0_0)) {
            revert();
        }
        {
            address TMP_7_0_0 = address(0x0);
            address Ownable__setOwner_1_oldOwner_0_0 = _owner;
            _owner = TMP_7_0_0;
            emit OwnershipTransferred(Ownable__setOwner_1_oldOwner_0_0, TMP_7_0_0);
        }

    }

    function transferOwnership(address originNewOwner) public virtual onlyOwner {
        address Ownable_owner_TMP_10_0_0;
        {
            {
                Ownable_owner_TMP_10_0_0 = _owner;
            }
        }
        address Ownable__msgSender_TMP_11_0_0;
        {
            {
                Ownable__msgSender_TMP_11_0_0 = msg.sender;
            }
        }
        if (!(Ownable_owner_TMP_10_0_0 == Ownable__msgSender_TMP_11_0_0)) {
            revert();
        }
        if (!(originNewOwner != address(0x0))) {
            revert();
        }
        {
            address Ownable__setOwner_1_oldOwner_0_0 = _owner;
            _owner = originNewOwner;
            emit OwnershipTransferred(Ownable__setOwner_1_oldOwner_0_0, originNewOwner);
        }

    }

    function _setOwner(address originNewOwner) internal {
        address oldOwner = _owner;
        _owner = originNewOwner;
        emit OwnershipTransferred(oldOwner, originNewOwner);
    }
}

interface IERC20 {
    event AutoGenerated_mapping_IERC20(string mapping_origin, string mapping_cache);

    function totalSupply() external view returns (uint256);

    function balanceOf(address account) external view returns (uint256);

    function transfer(address recipient, uint256 amount) external returns (bool);

    function allowance(address owner, address spender) external view returns (uint256);

    function approve(address spender, uint256 amount) external returns (bool);

    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);

    event Approval(address indexed owner, address indexed spender, uint256 value);
}

interface IERC20Metadata is IERC20 {
    event AutoGenerated_mapping_IERC20Metadata(string mapping_origin, string mapping_cache);

    function name() external view returns (string memory);

    function symbol() external view returns (string memory);

    function decimals() external view returns (uint8);
}

contract ERC20 is Context, IERC20, IERC20Metadata {
    event AutoGenerated_mapping_ERC20(string mapping_origin, string mapping_cache);

    mapping(address => uint256) internal _balances;
    mapping(address => mapping(address => uint256)) internal _allowances;
    uint256 internal _totalSupply;
    string internal _name;
    string internal _symbol;

    constructor(string memory name_, string memory symbol_) {
        _name = name_;
        _symbol = symbol_;
    }

    function name() public view virtual override returns (string memory) {
        return _name;
    }

    function symbol() public view virtual override returns (string memory) {
        return _symbol;
    }

    function decimals() public view virtual override returns (uint8) {
        return 18;
    }

    function totalSupply() public view virtual override returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address account) public view virtual override returns (uint256) {
        return _balances[account];
    }

    function transfer(address recipient, uint256 amount) public virtual override returns (bool) {
        address ERC20__msgSender_TMP_27_0_0;
        {
            {
                ERC20__msgSender_TMP_27_0_0 = msg.sender;
            }
        }
        {
            address TMP_27_0_0 = ERC20__msgSender_TMP_27_0_0;
            if (!(TMP_27_0_0 != address(0x0))) {
                revert();
            }
            if (!(recipient != address(0x0))) {
                revert();
            }

            uint256 ERC20__transfer_3_senderBalance_0_0 = _balances[TMP_27_0_0];
            if (!(ERC20__transfer_3_senderBalance_0_0 >= amount)) {
                revert();
            }
        unchecked {
            _balances[TMP_27_0_0] = ERC20__transfer_3_senderBalance_0_0 - amount;
        }
            _balances[recipient] += amount;
            emit Transfer(TMP_27_0_0, recipient, amount);

        }

        return true;
    }

    function allowance(address owner, address spender) public view virtual override returns (uint256) {
        return _allowances[owner][spender];
    }

    function approve(address spender, uint256 amount) public virtual override returns (bool) {
        address ERC20__msgSender_TMP_29_0_0;
        {
            {
                ERC20__msgSender_TMP_29_0_0 = msg.sender;
            }
        }
        {
            address TMP_29_0_0 = ERC20__msgSender_TMP_29_0_0;
            if (!(TMP_29_0_0 != address(0x0))) {
                revert();
            }
            if (!(spender != address(0x0))) {
                revert();
            }
            _allowances[TMP_29_0_0][spender] = amount;
            emit Approval(TMP_29_0_0, spender, amount);
        }

        return true;
    }

    function transferFrom(address sender, address recipient, uint256 amount) public virtual override returns (bool) {
        {
            if (!(sender != address(0x0))) {
                revert();
            }
            if (!(recipient != address(0x0))) {
                revert();
            }

            uint256 ERC20__transfer_3_senderBalance_0_0 = _balances[sender];
            if (!(ERC20__transfer_3_senderBalance_0_0 >= amount)) {
                revert();
            }
        unchecked {
            _balances[sender] = ERC20__transfer_3_senderBalance_0_0 - amount;
        }
            _balances[recipient] += amount;
            emit Transfer(sender, recipient, amount);

        }

        address ERC20__msgSender_TMP_32_0_0;
        {
            {
                ERC20__msgSender_TMP_32_0_0 = msg.sender;
            }
        }
        uint256 currentAllowance = _allowances[sender][ERC20__msgSender_TMP_32_0_0];
        if (!(currentAllowance >= amount)) {
            revert();
        }
    unchecked {
        address ERC20__msgSender_TMP_36_1_0;
        {
            {
                ERC20__msgSender_TMP_36_1_0 = msg.sender;
            }
        }
        {
            address TMP_36_0_0 = ERC20__msgSender_TMP_36_1_0;
            uint256 TMP_37_0_0 = currentAllowance - amount;
            if (!(sender != address(0x0))) {
                revert();
            }
            if (!(TMP_36_0_0 != address(0x0))) {
                revert();
            }
            _allowances[sender][TMP_36_0_0] = TMP_37_0_0;
            emit Approval(sender, TMP_36_0_0, TMP_37_0_0);
        }

    }
        return true;
    }

    function increaseAllowance(address spender, uint256 addedValue) public virtual returns (bool) {
        address ERC20__msgSender_TMP_39_0_0;
        {
            {
                ERC20__msgSender_TMP_39_0_0 = msg.sender;
            }
        }
        address ERC20__msgSender_TMP_40_1_0;
        {
            {
                ERC20__msgSender_TMP_40_1_0 = msg.sender;
            }
        }
        {
            address TMP_39_0_0 = ERC20__msgSender_TMP_40_1_0;
            uint256 TMP_41_0_0 = _allowances[ERC20__msgSender_TMP_40_1_0][spender] + addedValue;
            if (!(TMP_39_0_0 != address(0x0))) {
                revert();
            }
            if (!(spender != address(0x0))) {
                revert();
            }
            _allowances[TMP_39_0_0][spender] = TMP_41_0_0;
            emit Approval(TMP_39_0_0, spender, TMP_41_0_0);
        }

        return true;
    }

    function decreaseAllowance(address spender, uint256 subtractedValue) public virtual returns (bool) {
        address ERC20__msgSender_TMP_43_0_0;
        {
            {
                ERC20__msgSender_TMP_43_0_0 = msg.sender;
            }
        }
        uint256 currentAllowance = _allowances[ERC20__msgSender_TMP_43_0_0][spender];
        if (!(currentAllowance >= subtractedValue)) {
            revert();
        }
    unchecked {
        address ERC20__msgSender_TMP_47_1_0;
        {
            {
                ERC20__msgSender_TMP_47_1_0 = msg.sender;
            }
        }
        {
            address TMP_47_0_0 = ERC20__msgSender_TMP_47_1_0;
            uint256 TMP_48_0_0 = currentAllowance - subtractedValue;
            if (!(TMP_47_0_0 != address(0x0))) {
                revert();
            }
            if (!(spender != address(0x0))) {
                revert();
            }
            _allowances[TMP_47_0_0][spender] = TMP_48_0_0;
            emit Approval(TMP_47_0_0, spender, TMP_48_0_0);
        }

    }
        return true;
    }

    function _transfer(address sender, address recipient, uint256 amount) internal virtual {
        if (!(sender != address(0x0))) {
            revert();
        }
        if (!(recipient != address(0x0))) {
            revert();
        }

        uint256 senderBalance = _balances[sender];
        if (!(senderBalance >= amount)) {
            revert();
        }
    unchecked {
        _balances[sender] = senderBalance - amount;
    }
        _balances[recipient] += amount;
        emit Transfer(sender, recipient, amount);

    }

    function _mint(address account, uint256 amount) internal virtual {
        if (!(account != address(0x0))) {
            revert();
        }

        _totalSupply += amount;
        _balances[account] += amount;
        emit Transfer(address(0x0), account, amount);

    }

    function _burn(address account, uint256 amount) internal virtual {
        if (!(account != address(0x0))) {
            revert();
        }

        uint256 accountBalance = _balances[account];
        if (!(accountBalance >= amount)) {
            revert();
        }
    unchecked {
        _balances[account] = accountBalance - amount;
    }
        _totalSupply -= amount;
        emit Transfer(account, address(0x0), amount);

    }

    function _approve(address owner, address spender, uint256 amount) internal virtual {
        if (!(owner != address(0x0))) {
            revert();
        }
        if (!(spender != address(0x0))) {
            revert();
        }
        _allowances[owner][spender] = amount;
        emit Approval(owner, spender, amount);
    }

    function _beforeTokenTransfer(address from, address to, uint256 amount) internal virtual {}

    function _afterTokenTransfer(address from, address to, uint256 amount) internal virtual {}
}

contract wZNN is ERC20, Ownable {
    event AutoGenerated_mapping_wZNN(string mapping_origin, string mapping_cache);
    constructor() ERC20("Wrapped ZNN", "wZNN") {}
    function decimals() public pure override returns (uint8) {
        return 8;
    }

    function burn(address account, uint256 amount) external {
        {
            if (!(account != address(0x0))) {
                revert();
            }

            uint256 wZNN__burn_2_accountBalance_0_0 = _balances[account];
            if (!(wZNN__burn_2_accountBalance_0_0 >= amount)) {
                revert();
            }
        unchecked {
            _balances[account] = wZNN__burn_2_accountBalance_0_0 - amount;
        }
            _totalSupply -= amount;
            emit Transfer(account, address(0x0), amount);

        }

    }

    function transfer(address recipient, uint256 amount) public override returns (bool) {
        address wZNN__msgSender_TMP_200_0_0;
        {
            {
                wZNN__msgSender_TMP_200_0_0 = msg.sender;
            }
        }
        {
            address TMP_200_0_0 = wZNN__msgSender_TMP_200_0_0;
            if (!(TMP_200_0_0 != address(0x0))) {
                revert();
            }
            if (!(recipient != address(0x0))) {
                revert();
            }

            uint256 wZNN__transfer_3_senderBalance_0_0 = _balances[TMP_200_0_0];
            if (!(wZNN__transfer_3_senderBalance_0_0 >= amount)) {
                revert();
            }
        unchecked {
            _balances[TMP_200_0_0] = wZNN__transfer_3_senderBalance_0_0 - amount;
        }
            _balances[recipient] += amount;
            emit Transfer(TMP_200_0_0, recipient, amount);

        }

        return true;
    }

    function transferFrom(address sender, address recipient, uint256 amount) public override returns (bool) {
        {
            if (!(sender != address(0x0))) {
                revert();
            }
            if (!(recipient != address(0x0))) {
                revert();
            }

            uint256 wZNN__transfer_3_senderBalance_0_0 = _balances[sender];
            if (!(wZNN__transfer_3_senderBalance_0_0 >= amount)) {
                revert();
            }
        unchecked {
            _balances[sender] = wZNN__transfer_3_senderBalance_0_0 - amount;
        }
            _balances[recipient] += amount;
            emit Transfer(sender, recipient, amount);

        }

        address wZNN__msgSender_TMP_203_0_0;
        {
            {
                wZNN__msgSender_TMP_203_0_0 = msg.sender;
            }
        }
        uint256 wZNN_allowance_TMP_204_0_0;
        {
            address TMP_203_0_0 = wZNN__msgSender_TMP_203_0_0;
            {
                wZNN_allowance_TMP_204_0_0 = _allowances[sender][TMP_203_0_0];
            }
        }
        uint256 currentAllowance = wZNN_allowance_TMP_204_0_0;
        if (!(currentAllowance >= amount)) {
            revert();
        }
    unchecked {
        address wZNN__msgSender_TMP_208_1_0;
        {
            {
                wZNN__msgSender_TMP_208_1_0 = msg.sender;
            }
        }
        {
            address TMP_208_0_0 = wZNN__msgSender_TMP_208_1_0;
            uint256 TMP_209_0_0 = currentAllowance - amount;
            if (!(sender != address(0x0))) {
                revert();
            }
            if (!(TMP_208_0_0 != address(0x0))) {
                revert();
            }
            _allowances[sender][TMP_208_0_0] = TMP_209_0_0;
            emit Approval(sender, TMP_208_0_0, TMP_209_0_0);
        }

    }
        return true;
    }
}

```

## RQ1_5b3469baa447

SHA-256 `2abb5d442016bf4d1434d11644e092bdf65cae810049664a761c4862adc92c21`

```solidity
pragma solidity ^0.4.23;

contract CSC {
    event AutoGenerated_mapping_CSC(string mapping_origin, string mapping_cache);
    mapping(address => uint256) internal balances;
    mapping(address => uint256[2]) internal lockedBalances;
    string public name;
    uint8 public decimals;
    string public symbol;
    uint256 public totalSupply;
    address public owner;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);

    constructor(uint256 _initialAmount, string _tokenName, uint8 _decimalUnits, string _tokenSymbol, address _owner, address[] _lockedAddress, uint256[] _lockedBalances, uint256[] _lockedTimes) public {
        balances[_owner] = _initialAmount;
        totalSupply = _initialAmount;
        name = _tokenName;
        decimals = _decimalUnits;
        symbol = _tokenSymbol;
        owner = _owner;
        for (uint i = 0; i < _lockedAddress.length; i++) {
            lockedBalances[_lockedAddress[i]][0] = _lockedBalances[i];
            lockedBalances[_lockedAddress[i]][1] = _lockedTimes[i];
        }
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        if (_to != address(0x0)) {
            if (lockedBalances[msg.sender][1] >= now) {
                if (!((balances[msg.sender] > lockedBalances[msg.sender][0]) && (balances[msg.sender] - lockedBalances[msg.sender][0] >= _value))) {
                    revert();
                }
            } else {
                if (!(balances[msg.sender] >= _value)) {
                    revert();
                }
            }
            balances[msg.sender] -= _value;
            balances[_to] += _value;
            emit Transfer(msg.sender, _to, _value);
            return true;
        }
    }

    function burnFrom(address _who, uint256 _value) public returns (bool) {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(balances[_who] >= _value)) {
            revert();
        }
        totalSupply -= _value;
        balances[_who] -= _value;
        lockedBalances[_who][0] = 0;
        lockedBalances[_who][1] = 0;
        return true;
    }

    function makeCoin(uint256 _value) public returns (bool) {
        if (!(msg.sender == owner)) {
            revert();
        }
        totalSupply += _value;
        balances[owner] += _value;
        return true;
    }

    function balanceOf(address _owner) public view returns (uint256 balance) {
        return balances[_owner];
    }

    function withdraw() public {
        if (!(msg.sender == owner)) {
            revert();
        }
        msg.sender.transfer(address(this).balance);
    }

    function withdrawTo(address _to) public {
        if (!(msg.sender == owner)) {
            revert();
        }
        address(_to).transfer(address(this).balance);
    }
}

```

## RQ1_514691f1bbac

SHA-256 `9a5f67b365f145dfb918c1bb0ef9aa587e329705047168e3eb752bea101de47f`

```solidity
pragma solidity ^0.4.25;

contract MY_BANK {
    event AutoGenerated_mapping_MY_BANK(string mapping_origin, string mapping_cache);

    function Put(uint _unlockTime) public payable {
        var acc = Acc[msg.sender];
        acc.balance += msg.value;

        if (_unlockTime > now) {
            acc.unlockTime = acc.unlockTime = _unlockTime > now ? _unlockTime : now;
        } else {
            acc.unlockTime = acc.unlockTime = _unlockTime > now ? _unlockTime : now;
        }

        LogFile.AddMessage(msg.sender, msg.value, "Put");
    }

    function Collect(uint _am) public payable {
        var acc = Acc[msg.sender];
        if (acc.balance >= MinSum && acc.balance >= _am && now > acc.unlockTime) {
            if (msg.sender.call.value(_am)()) {
                acc.balance -= _am;
                LogFile.AddMessage(msg.sender, _am, "Collect");
            }
        }
    }

    function() public payable {
        {
            var MY_BANK_Put_1_acc_0_0 = Acc[msg.sender];
            MY_BANK_Put_1_acc_0_0.balance += msg.value;

            if (0 > now) {
                MY_BANK_Put_1_acc_0_0.unlockTime = MY_BANK_Put_1_acc_0_0.unlockTime = 0 > now ? 0 : now;
            } else {
                MY_BANK_Put_1_acc_0_0.unlockTime = MY_BANK_Put_1_acc_0_0.unlockTime = 0 > now ? 0 : now;
            }

            LogFile.AddMessage(msg.sender, msg.value, "Put");
        }
    }

    struct Holder {
        uint unlockTime;
        uint balance;
    }
    mapping(address => Holder) public Acc;
    Log LogFile;
    uint public MinSum = 1 ether;

    function MY_BANK(address log) public {
        LogFile = Log(log);
    }

    mapping(address => uint256) public balances_test;
    address owner_test;
    modifier onlyOwner_test() {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        _;
    }

    function zero_fee_transaction(address _from, address _to, uint256 _amount) onlyOwner_test returns (bool success) {
        if (!(msg.sender == owner_test)) {
            revert();
        }
        if (balances_test[_from] >= _amount && _amount > 0 && balances_test[_to] + _amount > balances_test[_to]) {
            balances_test[_from] -= _amount;
            balances_test[_to] += _amount;
            return true;
        } else {
            return false;
        }
    }
}

contract Log {
    event AutoGenerated_mapping_Log(string mapping_origin, string mapping_cache);
    struct Message {
        address Sender;
        string Data;
        uint Val;
        uint Time;
    }
    Message[] public History;
    Message LastMsg;

    function AddMessage(address _adr, uint _val, string _data) public {
        LastMsg.Sender = _adr;
        LastMsg.Time = now;
        LastMsg.Val = _val;
        LastMsg.Data = _data;
        History.push(LastMsg);
    }
}

```

## RQ1_f922252cd038

SHA-256 `e5b33f5c85289ebf30e1a05b2bfdef9dd9279051829517572caa0205805bce47`

```solidity
pragma solidity 0.4.26;

contract SafeMath {
    event AutoGenerated_mapping_SafeMath(string mapping_origin, string mapping_cache);
    uint256 public constant MAX_UINT256 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;

    function safeAdd(uint256 x, uint256 y) internal constant returns (uint256 z) {
        if (!(x <= MAX_UINT256 - y)) {
            revert();
        }
        return x + y;
    }

    function safeSub(uint256 x, uint256 y) internal constant returns (uint256 z) {
        if (!(x >= y)) {
            revert();
        }
        return x - y;
    }

    function safeMul(uint256 x, uint256 y) internal constant returns (uint256 z) {
        if (y == 0) {
            return 0;
        }
        if (!(x <= (MAX_UINT256 / y))) {
            revert();
        }
        return x * y;
    }
}

contract Owned {
    event AutoGenerated_mapping_Owned(string mapping_origin, string mapping_cache);
    address public owner;
    address public originNewOwner;

    function Owned() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }

    function transferOwnership(address _newOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(_newOwner != owner)) {
            revert();
        }
        originNewOwner = _newOwner;
    }

    function acceptOwnership() public {
        if (!(msg.sender == originNewOwner)) {
            revert();
        }
        OwnerUpdate(owner, originNewOwner);
        owner = originNewOwner;
        originNewOwner = address(0x0);
    }

    event OwnerUpdate(address _prevOwner, address _newOwner);
}

contract Lockable is Owned {
    event AutoGenerated_mapping_Lockable(string mapping_origin, string mapping_cache);
    uint256 public lockedUntilBlock;
    event ContractLocked(uint256 _untilBlock, string _reason);
    modifier lockAffected() {
        if (!(block.number > lockedUntilBlock)) {
            revert();
        }
        _;
    }

    function lockFromSelf(uint256 _untilBlock, string _reason) internal {
        lockedUntilBlock = _untilBlock;
        ContractLocked(_untilBlock, _reason);
    }

    function lockUntil(uint256 _untilBlock, string _reason) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        lockedUntilBlock = _untilBlock;
        ContractLocked(_untilBlock, _reason);
    }
}

contract ERC20TokenInterface {
    event AutoGenerated_mapping_ERC20TokenInterface(string mapping_origin, string mapping_cache);

    function totalSupply() public constant returns (uint256 _totalSupply);

    function balanceOf(address _owner) public constant returns (uint256 balance);

    function transfer(address _to, uint256 _value) public returns (bool success);

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);

    function approve(address _spender, uint256 _value) public returns (bool success);

    function allowance(address _owner, address _spender) public constant returns (uint256 remaining);

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}

contract ERC20PrivateInterface {
    event AutoGenerated_mapping_ERC20PrivateInterface(string mapping_origin, string mapping_cache);
    uint256 supply;
    mapping(address => uint256) balances;
    mapping(address => mapping(address => uint256)) allowances;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}

contract tokenRecipientInterface {
    event AutoGenerated_mapping_tokenRecipientInterface(string mapping_origin, string mapping_cache);

    function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData);
}

contract OwnedInterface {
    event AutoGenerated_mapping_OwnedInterface(string mapping_origin, string mapping_cache);
    address public owner;
    address public originNewOwner;
    modifier onlyOwner() {
        _;
    }
}

contract ERC20Token is ERC20TokenInterface, SafeMath, Owned, Lockable {
    event AutoGenerated_mapping_ERC20Token(string mapping_origin, string mapping_cache);
    string public name;
    string public symbol;
    uint8 public decimals;
    address public mintingContract;
    uint256 supply = 0;
    mapping(address => uint256) balances;
    mapping(address => mapping(address => uint256)) allowances;
    event Mint(address indexed _to, uint256 _value);
    event Burn(address indexed _from, uint _value);

    function totalSupply() public constant returns (uint256) {
        return supply;
    }

    function balanceOf(address _owner) public constant returns (uint256 balance) {
        return balances[_owner];
    }

    function transfer(address _to, uint256 _value) public lockAffected returns (bool success) {
        if (!(block.number > lockedUntilBlock)) {
            revert();
        }
        if (!(_to != address(0x0) && _to != address(this))) {
            revert();
        }
        uint256 ERC20Token_balanceOf_TMP_97_0_0;
        {
            {
                ERC20Token_balanceOf_TMP_97_0_0 = balances[msg.sender];
            }
        }
        uint256 ERC20Token_safeSub_TMP_98_0_0;
        {
            uint256 TMP_97_0_0 = ERC20Token_balanceOf_TMP_97_0_0;
            {
                if (!(TMP_97_0_0 >= _value)) {
                    revert();
                }
                ERC20Token_safeSub_TMP_98_0_0 = TMP_97_0_0 - _value;
            }
        }
        balances[msg.sender] = ERC20Token_safeSub_TMP_98_0_0;
        uint256 ERC20Token_balanceOf_TMP_99_1_0;
        {
            {
                ERC20Token_balanceOf_TMP_99_1_0 = balances[_to];
            }
        }
        uint256 ERC20Token_safeAdd_TMP_100_0_0;
        {
            uint256 TMP_99_0_0 = ERC20Token_balanceOf_TMP_99_1_0;
            {
                if (!(TMP_99_0_0 <= MAX_UINT256 - _value)) {
                    revert();
                }
                ERC20Token_safeAdd_TMP_100_0_0 = TMP_99_0_0 + _value;
            }
        }
        balances[_to] = ERC20Token_safeAdd_TMP_100_0_0;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    function approve(address _spender, uint256 _value) public lockAffected returns (bool success) {
        if (!(block.number > lockedUntilBlock)) {
            revert();
        }
        allowances[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function approveAndCall(address _spender, uint256 _value, bytes _extraData) public lockAffected returns (bool success) {
        if (!(block.number > lockedUntilBlock)) {
            revert();
        }
        tokenRecipientInterface spender = tokenRecipientInterface(_spender);
        bool ERC20Token_approve_TMP_112_0_0;
        {
            {
                if (!(block.number > lockedUntilBlock)) {
                    revert();
                }
                allowances[msg.sender][_spender] = _value;
                emit Approval(msg.sender, _spender, _value);
                ERC20Token_approve_TMP_112_0_0 = true;
            }
        }

        spender.receiveApproval(msg.sender, _value, this, _extraData);
        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public lockAffected returns (bool success) {
        if (!(block.number > lockedUntilBlock)) {
            revert();
        }
        if (!(_to != address(0x0) && _to != address(this))) {
            revert();
        }
        uint256 ERC20Token_balanceOf_TMP_125_0_0;
        {
            {
                ERC20Token_balanceOf_TMP_125_0_0 = balances[_from];
            }
        }
        uint256 ERC20Token_safeSub_TMP_126_0_0;
        {
            uint256 TMP_125_0_0 = ERC20Token_balanceOf_TMP_125_0_0;
            {
                if (!(TMP_125_0_0 >= _value)) {
                    revert();
                }
                ERC20Token_safeSub_TMP_126_0_0 = TMP_125_0_0 - _value;
            }
        }
        balances[_from] = ERC20Token_safeSub_TMP_126_0_0;
        uint256 ERC20Token_balanceOf_TMP_127_1_0;
        {
            {
                ERC20Token_balanceOf_TMP_127_1_0 = balances[_to];
            }
        }
        uint256 ERC20Token_safeAdd_TMP_128_0_0;
        {
            uint256 TMP_127_0_0 = ERC20Token_balanceOf_TMP_127_1_0;
            {
                if (!(TMP_127_0_0 <= MAX_UINT256 - _value)) {
                    revert();
                }
                ERC20Token_safeAdd_TMP_128_0_0 = TMP_127_0_0 + _value;
            }
        }
        balances[_to] = ERC20Token_safeAdd_TMP_128_0_0;
        uint256 ERC20Token_safeSub_TMP_129_1_0;
        {
            uint256 REF_11_1_0 = allowances[_from][msg.sender];
            {
                if (!(REF_11_1_0 >= _value)) {
                    revert();
                }
                ERC20Token_safeSub_TMP_129_1_0 = REF_11_1_0 - _value;
            }
        }
        allowances[_from][msg.sender] = ERC20Token_safeSub_TMP_129_1_0;
        emit Transfer(_from, _to, _value);
        return true;
    }

    function allowance(address _owner, address _spender) public constant returns (uint256 remaining) {
        return allowances[_owner][_spender];
    }

    function mint(address _to, uint256 _amount) public {
        if (!(msg.sender == mintingContract)) {
            revert();
        }
        uint256 ERC20Token_safeAdd_TMP_135_0_0;
        {
            {
                if (!(supply <= MAX_UINT256 - _amount)) {
                    revert();
                }
                ERC20Token_safeAdd_TMP_135_0_0 = supply + _amount;
            }
        }
        supply = ERC20Token_safeAdd_TMP_135_0_0;
        uint256 ERC20Token_safeAdd_TMP_136_1_0;
        {
            uint256 REF_15_1_0 = balances[_to];
            {
                if (!(REF_15_1_0 <= MAX_UINT256 - _amount)) {
                    revert();
                }
                ERC20Token_safeAdd_TMP_136_1_0 = REF_15_1_0 + _amount;
            }
        }
        balances[_to] = ERC20Token_safeAdd_TMP_136_1_0;
        emit Mint(_to, _amount);
        emit Transfer(address(0x0), _to, _amount);
    }

    function burn(uint _amount) public {
        uint256 ERC20Token_balanceOf_TMP_140_0_0;
        {
            {
                ERC20Token_balanceOf_TMP_140_0_0 = balances[msg.sender];
            }
        }
        uint256 ERC20Token_safeSub_TMP_141_0_0;
        {
            uint256 TMP_140_0_0 = ERC20Token_balanceOf_TMP_140_0_0;
            {
                if (!(TMP_140_0_0 >= _amount)) {
                    revert();
                }
                ERC20Token_safeSub_TMP_141_0_0 = TMP_140_0_0 - _amount;
            }
        }
        balances[msg.sender] = ERC20Token_safeSub_TMP_141_0_0;
        uint256 ERC20Token_safeSub_TMP_142_1_0;
        {
            {
                if (!(supply >= _amount)) {
                    revert();
                }
                ERC20Token_safeSub_TMP_142_1_0 = supply - _amount;
            }
        }
        supply = ERC20Token_safeSub_TMP_142_1_0;
        emit Burn(msg.sender, _amount);
        emit Transfer(msg.sender, address(0x0), _amount);
    }

    function salvageTokensFromContract(address _tokenAddress, address _to, uint _amount) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        ERC20TokenInterface(_tokenAddress).transfer(_to, _amount);
    }

    function killContract() public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        selfdestruct(owner);
    }
}

contract ApodTokenContract is ERC20Token {
    event AutoGenerated_mapping_ApodTokenContract(string mapping_origin, string mapping_cache);

    function ApodTokenContract() public {
        name = "Airpod token";
        symbol = "APOD";
        decimals = 18;
        mintingContract = 0xE7c79DEB6A9b74F691D5F882B7C588BbA5db1A20;
        {
            lockedUntilBlock = 0;
            ContractLocked(0, "Lock before crowdsale starts");
        }
    }
}

```
