# 本批实际输入源码

按输入原字节 SHA 核对。源码位置采用 UTF-8 字节偏移。

## RQ1_a34628cf71df

SHA-256 `cb3fbbd652ff0220ffdfa93a37b546e3d340d6a651cf768ccbf7d2cc586d21d2`

```solidity
pragma solidity ^0.4.24;
contract IERC20 {
    function totalSupply() constant public returns (uint256);
    function balanceOf(address _owner) constant public returns (uint256 balance);
    function transfer(address _to, uint256 _value) public returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);
    function approve(address _spender, uint256 _value) public returns (bool success);
    function allowance(address _owner, address _spender) constant public returns (uint256 remianing);
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}
contract Ownable {
    address public owner;
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
    constructor() public {
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
    function max64(uint64 a, uint64 b) internal pure returns (uint64) {
        return a >= b ? a : b;
    }
    function min64(uint64 a, uint64 b) internal pure returns (uint64) {
        return a < b ? a : b;
    }
    function max256(uint256 a, uint256 b) internal pure returns (uint256) {
        return a >= b ? a : b;
    }
    function min256(uint256 a, uint256 b) internal pure returns (uint256) {
        return a < b ? a : b;
    }
}
contract JAAGCoin is IERC20, Ownable {
    using SafeMath for uint256;
    uint public _totalSupply = 0;
    uint public constant INITIAL_SUPPLY = 160000000000000000000000000;
    uint public MAXUM_SUPPLY = 250000000000000000000000000;
    uint256 public _currentSupply = 0;
    string public constant symbol = "JAAG";
    string public constant name = "JAAGCoin";
    uint8 public constant decimals = 18;
    uint256 public RATE;
    bool public mintingFinished = false;
    mapping(address => uint256)balances;
    mapping(address => mapping(address => uint256)) allowed;
    mapping(address => bool) whitelisted;
    mapping(address => bool) blockListed;
    constructor() public {
        setRate(1);
        _totalSupply = INITIAL_SUPPLY;
        balances[msg.sender] = INITIAL_SUPPLY;
        emit Transfer(0x0, msg.sender, INITIAL_SUPPLY);
        owner = msg.sender;
    }
    function () public payable {
        revert();
    }
    function createTokens() payable public {
        require(msg.value > 0);
        require(whitelisted[msg.sender]);
        uint256 tokens = msg.value.mul(RATE);
        balances[msg.sender] = balances[msg.sender].add(tokens);
        _totalSupply = _totalSupply.add(tokens);
        owner.transfer(msg.value);
    }
    function totalSupply() constant public returns (uint256) {
        return _totalSupply;
    }
    function balanceOf(address _owner) constant public returns (uint256 balance) {
        return balances[_owner];
    }
    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(
            balances[msg.sender] >= _value
            && _value > 0
            && !blockListed[_to]
            && !blockListed[msg.sender]
        );
        balances[msg.sender] = balances[msg.sender].sub(_value);
        balances[_to] = balances[_to].add(_value);
        emit Transfer(msg.sender, _to, _value);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(
            balances[msg.sender] >= _value
            && balances[_from] >= _value
            && _value > 0
            && whitelisted[msg.sender]
            && !blockListed[_to]
            && !blockListed[msg.sender]
        );
        balances[_from] -= _value;
        balances[_to] += _value;
        allowed[_from][msg.sender] -= _value;
        emit Transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowed[msg.sender][_spender] = _value;
        whitelisted[_spender] = true;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256 remianing) {
        return allowed[_owner][_spender];
    }
    function getRate() public constant returns (uint256) {
        return RATE;
    }
    function setRate(uint256 _rate) public returns (bool success) {
        RATE = _rate;
        return true;
    }
    modifier canMint() {
        require(!mintingFinished);
        _;
    }
    modifier hasMintPermission() {
        require(msg.sender == owner);
        _;
    }
    function mint(address _to, uint256 _amount) hasMintPermission canMint public returns (bool) {
        uint256 tokens = _amount.mul(RATE);
        require(
            _currentSupply.add(tokens) < MAXUM_SUPPLY
            && whitelisted[msg.sender]
            && !blockListed[_to]
        );
        if (_currentSupply >= INITIAL_SUPPLY) {
            _totalSupply = _totalSupply.add(tokens);
        }
        _currentSupply = _currentSupply.add(tokens);
        balances[_to] = balances[_to].add(tokens);
        emit Mint(_to, tokens);
        emit Transfer(address(0), _to, tokens);
        return true;
    }
    function finishMinting() onlyOwner canMint public returns (bool) {
        mintingFinished = true;
        emit MintFinished();
        return true;
    }
    function addUser(address user) onlyOwner public {
        whitelisted[user] = true;
        emit LogUserAdded(user);
    }
    function removeUser(address user) onlyOwner public {
        whitelisted[user] = false;
        emit LogUserRemoved(user);
    }
    function getCurrentOwnerBallence() constant public returns (uint256) {
        return balances[msg.sender];
    }
    function addBlockList(address wallet) onlyOwner public {
        blockListed[wallet] = true;
    }
    function removeBlockList(address wallet) onlyOwner public {
        blockListed[wallet] = false;
    }
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Mint(address indexed to, uint256 amount);
    event MintFinished();
    event LogUserAdded(address user);
    event LogUserRemoved(address user);
}

```

## RQ1_9dfa887f7b8a

SHA-256 `b8fd97669ffca4fe9ca7a62cb1dccf75bdf6fda89342cbc2bc5708bdcb0d325f`

```solidity
pragma solidity ^0.4.11;
contract Utils {
    function Utils() {
    }
    modifier greaterThanZero(uint256 _amount) {
        require(_amount > 0);
        _;
    }
    modifier validAddress(address _address) {
        require(_address != 0x0);
        _;
    }
    modifier notThis(address _address) {
        require(_address != address(this));
        _;
    }
    function safeAdd(uint256 _x, uint256 _y) internal returns (uint256) {
        uint256 z = _x + _y;
        assert(z >= _x);
        return z;
    }
    function safeSub(uint256 _x, uint256 _y) internal returns (uint256) {
        assert(_x >= _y);
        return _x - _y;
    }
    function safeMul(uint256 _x, uint256 _y) internal returns (uint256) {
        uint256 z = _x * _y;
        assert(_x == 0 || z / _x == _y);
        return z;
    }
}
contract IOwned {
    function owner() public constant returns (address owner) { owner; }
    function transferOwnership(address _newOwner) public;
    function acceptOwnership() public;
}
contract Owned is IOwned {
    address public owner;
    address public newOwner;
    event OwnerUpdate(address _prevOwner, address _newOwner);
    function Owned() {
        owner = msg.sender;
    }
    modifier ownerOnly {
        assert(msg.sender == owner);
        _;
    }
    function transferOwnership(address _newOwner) public ownerOnly {
        require(_newOwner != owner);
        newOwner = _newOwner;
    }
    function acceptOwnership() public {
        require(msg.sender == newOwner);
        OwnerUpdate(owner, newOwner);
        owner = newOwner;
        newOwner = 0x0;
    }
}
contract Managed {
    address public manager;
    address public newManager;
    event ManagerUpdate(address _prevManager, address _newManager);
    function Managed() {
        manager = msg.sender;
    }
    modifier managerOnly {
        assert(msg.sender == manager);
        _;
    }
    function transferManagement(address _newManager) public managerOnly {
        require(_newManager != manager);
        newManager = _newManager;
    }
    function acceptManagement() public {
        require(msg.sender == newManager);
        ManagerUpdate(manager, newManager);
        manager = newManager;
        newManager = 0x0;
    }
}
contract ITokenHolder is IOwned {
    function withdrawTokens(IERC20Token _token, address _to, uint256 _amount) public;
}
contract TokenHolder is ITokenHolder, Owned, Utils {
    function TokenHolder() {
    }
    function withdrawTokens(IERC20Token _token, address _to, uint256 _amount)
        public
        ownerOnly
        validAddress(_token)
        validAddress(_to)
        notThis(_to)
    {
        assert(_token.transfer(_to, _amount));
    }
}
contract SmartTokenController is TokenHolder {
    ISmartToken public token;   
    function SmartTokenController(ISmartToken _token)
        validAddress(_token)
    {
        token = _token;
    }
    modifier active() {
        assert(token.owner() == address(this));
        _;
    }
    modifier inactive() {
        assert(token.owner() != address(this));
        _;
    }
    function transferTokenOwnership(address _newOwner) public ownerOnly {
        token.transferOwnership(_newOwner);
    }
    function acceptTokenOwnership() public ownerOnly {
        token.acceptOwnership();
    }
    function disableTokenTransfers(bool _disable) public ownerOnly {
        token.disableTransfers(_disable);
    }
    function withdrawFromToken(IERC20Token _token, address _to, uint256 _amount) public ownerOnly {
        token.withdrawTokens(_token, _to, _amount);
    }
}
contract IERC20Token {
    function name() public constant returns (string name) { name; }
    function symbol() public constant returns (string symbol) { symbol; }
    function decimals() public constant returns (uint8 decimals) { decimals; }
    function totalSupply() public constant returns (uint256 totalSupply) { totalSupply; }
    function balanceOf(address _owner) public constant returns (uint256 balance) { _owner; balance; }
    function allowance(address _owner, address _spender) public constant returns (uint256 remaining) { _owner; _spender; remaining; }
    function transfer(address _to, uint256 _value) public returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);
    function approve(address _spender, uint256 _value) public returns (bool success);
}
contract IEtherToken is ITokenHolder, IERC20Token {
    function deposit() public payable;
    function withdraw(uint256 _amount) public;
    function withdrawTo(address _to, uint256 _amount);
}
contract ISmartToken is ITokenHolder, IERC20Token {
    function disableTransfers(bool _disable) public;
    function issue(address _to, uint256 _amount) public;
    function destroy(address _from, uint256 _amount) public;
}
contract IBancorFormula {
    function calculatePurchaseReturn(uint256 _supply, uint256 _reserveBalance, uint32 _reserveRatio, uint256 _depositAmount) public constant returns (uint256);
    function calculateSaleReturn(uint256 _supply, uint256 _reserveBalance, uint32 _reserveRatio, uint256 _sellAmount) public constant returns (uint256);
}
contract ITokenChanger {
    function changeableTokenCount() public constant returns (uint16 count);
    function changeableToken(uint16 _tokenIndex) public constant returns (address tokenAddress);
    function getReturn(IERC20Token _fromToken, IERC20Token _toToken, uint256 _amount) public constant returns (uint256 amount);
    function change(IERC20Token _fromToken, IERC20Token _toToken, uint256 _amount, uint256 _minReturn) public returns (uint256 amount);
}
contract BancorChanger is ITokenChanger, SmartTokenController, Managed {
    uint32 private constant MAX_CRR = 1000000;
    uint32 private constant MAX_CHANGE_FEE = 1000000;
    struct Reserve {
        uint256 virtualBalance;         
        uint32 ratio;                   
        bool isVirtualBalanceEnabled;   
        bool isPurchaseEnabled;         
        bool isSet;                     
    }
    string public version = '0.2';
    string public changerType = 'bancor';
    IBancorFormula public formula;                  
    IERC20Token[] public reserveTokens;             
    IERC20Token[] public quickBuyPath;              
    mapping (address => Reserve) public reserves;   
    uint32 private totalReserveRatio = 0;           
    uint32 public maxChangeFee = 0;                 
    uint32 public changeFee = 0;                    
    bool public changingEnabled = true;             
    event Change(address indexed _fromToken, address indexed _toToken, address indexed _trader, uint256 _amount, uint256 _return,
                 uint256 _currentPriceN, uint256 _currentPriceD);
    function BancorChanger(ISmartToken _token, IBancorFormula _formula, uint32 _maxChangeFee, IERC20Token _reserveToken, uint32 _reserveRatio)
        SmartTokenController(_token)
        validAddress(_formula)
        validMaxChangeFee(_maxChangeFee)
    {
        formula = _formula;
        maxChangeFee = _maxChangeFee;
        if (address(_reserveToken) != 0x0)
            addReserve(_reserveToken, _reserveRatio, false);
    }
    modifier validReserve(IERC20Token _address) {
        require(reserves[_address].isSet);
        _;
    }
    modifier validToken(IERC20Token _address) {
        require(_address == token || reserves[_address].isSet);
        _;
    }
    modifier validMaxChangeFee(uint32 _changeFee) {
        require(_changeFee >= 0 && _changeFee <= MAX_CHANGE_FEE);
        _;
    }
    modifier validChangeFee(uint32 _changeFee) {
        require(_changeFee >= 0 && _changeFee <= maxChangeFee);
        _;
    }
    modifier validReserveRatio(uint32 _ratio) {
        require(_ratio > 0 && _ratio <= MAX_CRR);
        _;
    }
    modifier validChangePath(IERC20Token[] _path) {
        require(_path.length > 2 && _path.length <= (1 + 2 * 10) && _path.length % 2 == 1);
        _;
    }
    modifier changingAllowed {
        assert(changingEnabled);
        _;
    }
    function reserveTokenCount() public constant returns (uint16 count) {
        return uint16(reserveTokens.length);
    }
    function changeableTokenCount() public constant returns (uint16 count) {
        return reserveTokenCount() + 1;
    }
    function changeableToken(uint16 _tokenIndex) public constant returns (address tokenAddress) {
        if (_tokenIndex == 0)
            return token;
        return reserveTokens[_tokenIndex - 1];
    }
    function setFormula(IBancorFormula _formula)
        public
        ownerOnly
        validAddress(_formula)
        notThis(_formula)
    {
        formula = _formula;
    }
    function setQuickBuyPath(IERC20Token[] _path)
        public
        ownerOnly
        validChangePath(_path)
    {
        quickBuyPath = _path;
    }
    function clearQuickBuyPath() public ownerOnly {
        quickBuyPath.length = 0;
    }
    function getQuickBuyPathLength() public constant returns (uint256 length) {
        return quickBuyPath.length;
    }
    function hasQuickBuyEtherToken() public constant returns (bool) {
        return quickBuyPath.length > 0;
    }
    function getQuickBuyEtherToken() public constant returns (IEtherToken etherToken) {
        assert(quickBuyPath.length > 0);
        return IEtherToken(quickBuyPath[0]);
    }
    function disableChanging(bool _disable) public managerOnly {
        changingEnabled = !_disable;
    }
    function setChangeFee(uint32 _changeFee)
        public
        managerOnly
        validChangeFee(_changeFee)
    {
        changeFee = _changeFee;
    }
    function getChangeFeeAmount(uint256 _amount) public constant returns (uint256 feeAmount) {
        return safeMul(_amount, changeFee) / MAX_CHANGE_FEE;
    }
    function addReserve(IERC20Token _token, uint32 _ratio, bool _enableVirtualBalance)
        public
        ownerOnly
        inactive
        validAddress(_token)
        notThis(_token)
        validReserveRatio(_ratio)
    {
        require(_token != token && !reserves[_token].isSet && totalReserveRatio + _ratio <= MAX_CRR); 
        reserves[_token].virtualBalance = 0;
        reserves[_token].ratio = _ratio;
        reserves[_token].isVirtualBalanceEnabled = _enableVirtualBalance;
        reserves[_token].isPurchaseEnabled = true;
        reserves[_token].isSet = true;
        reserveTokens.push(_token);
        totalReserveRatio += _ratio;
    }
    function updateReserve(IERC20Token _reserveToken, uint32 _ratio, bool _enableVirtualBalance, uint256 _virtualBalance)
        public
        ownerOnly
        validReserve(_reserveToken)
        validReserveRatio(_ratio)
    {
        Reserve storage reserve = reserves[_reserveToken];
        require(totalReserveRatio - reserve.ratio + _ratio <= MAX_CRR); 
        totalReserveRatio = totalReserveRatio - reserve.ratio + _ratio;
        reserve.ratio = _ratio;
        reserve.isVirtualBalanceEnabled = _enableVirtualBalance;
        reserve.virtualBalance = _virtualBalance;
    }
    function disableReservePurchases(IERC20Token _reserveToken, bool _disable)
        public
        ownerOnly
        validReserve(_reserveToken)
    {
        reserves[_reserveToken].isPurchaseEnabled = !_disable;
    }
    function getReserveBalance(IERC20Token _reserveToken)
        public
        constant
        validReserve(_reserveToken)
        returns (uint256 balance)
    {
        Reserve storage reserve = reserves[_reserveToken];
        return reserve.isVirtualBalanceEnabled ? reserve.virtualBalance : _reserveToken.balanceOf(this);
    }
    function getReturn(IERC20Token _fromToken, IERC20Token _toToken, uint256 _amount) public constant returns (uint256 amount) {
        require(_fromToken != _toToken); 
        if (_toToken == token)
            return getPurchaseReturn(_fromToken, _amount);
        else if (_fromToken == token)
            return getSaleReturn(_toToken, _amount);
        uint256 purchaseReturnAmount = getPurchaseReturn(_fromToken, _amount);
        return getSaleReturn(_toToken, purchaseReturnAmount, safeAdd(token.totalSupply(), purchaseReturnAmount));
    }
    function getPurchaseReturn(IERC20Token _reserveToken, uint256 _depositAmount)
        public
        constant
        active
        validReserve(_reserveToken)
        returns (uint256 amount)
    {
        Reserve storage reserve = reserves[_reserveToken];
        require(reserve.isPurchaseEnabled); 
        uint256 tokenSupply = token.totalSupply();
        uint256 reserveBalance = getReserveBalance(_reserveToken);
        amount = formula.calculatePurchaseReturn(tokenSupply, reserveBalance, reserve.ratio, _depositAmount);
        uint256 feeAmount = getChangeFeeAmount(amount);
        return safeSub(amount, feeAmount);
    }
    function getSaleReturn(IERC20Token _reserveToken, uint256 _sellAmount) public constant returns (uint256 amount) {
        return getSaleReturn(_reserveToken, _sellAmount, token.totalSupply());
    }
    function change(IERC20Token _fromToken, IERC20Token _toToken, uint256 _amount, uint256 _minReturn) public returns (uint256 amount) {
        require(_fromToken != _toToken); 
        if (_toToken == token)
            return buy(_fromToken, _amount, _minReturn);
        else if (_fromToken == token)
            return sell(_toToken, _amount, _minReturn);
        uint256 purchaseAmount = buy(_fromToken, _amount, 1);
        return sell(_toToken, purchaseAmount, _minReturn);
    }
    function buy(IERC20Token _reserveToken, uint256 _depositAmount, uint256 _minReturn)
        public
        changingAllowed
        greaterThanZero(_minReturn)
        returns (uint256 amount)
    {
        amount = getPurchaseReturn(_reserveToken, _depositAmount);
        assert(amount != 0 && amount >= _minReturn); 
        Reserve storage reserve = reserves[_reserveToken];
        if (reserve.isVirtualBalanceEnabled)
            reserve.virtualBalance = safeAdd(reserve.virtualBalance, _depositAmount);
        assert(_reserveToken.transferFrom(msg.sender, this, _depositAmount)); 
        token.issue(msg.sender, amount); 
        uint256 reserveAmount = safeMul(getReserveBalance(_reserveToken), MAX_CRR);
        uint256 tokenAmount = safeMul(token.totalSupply(), reserve.ratio);
        Change(_reserveToken, token, msg.sender, _depositAmount, amount, reserveAmount, tokenAmount);
        return amount;
    }
    function sell(IERC20Token _reserveToken, uint256 _sellAmount, uint256 _minReturn)
        public
        changingAllowed
        greaterThanZero(_minReturn)
        returns (uint256 amount)
    {
        require(_sellAmount <= token.balanceOf(msg.sender)); 
        amount = getSaleReturn(_reserveToken, _sellAmount);
        assert(amount != 0 && amount >= _minReturn); 
        uint256 tokenSupply = token.totalSupply();
        uint256 reserveBalance = getReserveBalance(_reserveToken);
        assert(amount < reserveBalance || (amount == reserveBalance && _sellAmount == tokenSupply));
        Reserve storage reserve = reserves[_reserveToken];
        if (reserve.isVirtualBalanceEnabled)
            reserve.virtualBalance = safeSub(reserve.virtualBalance, amount);
        token.destroy(msg.sender, _sellAmount); 
        assert(_reserveToken.transfer(msg.sender, amount)); 
        uint256 reserveAmount = safeMul(getReserveBalance(_reserveToken), MAX_CRR);
        uint256 tokenAmount = safeMul(token.totalSupply(), reserve.ratio);
        Change(token, _reserveToken, msg.sender, _sellAmount, amount, tokenAmount, reserveAmount);
        return amount;
    }
    function quickChange(IERC20Token[] _path, uint256 _amount, uint256 _minReturn)
        public
        validChangePath(_path)
        returns (uint256 amount)
    {
        IERC20Token fromToken = _path[0];
        claimTokens(fromToken, msg.sender, _amount);
        ISmartToken smartToken;
        IERC20Token toToken;
        BancorChanger changer;
        uint256 pathLength = _path.length;
        for (uint256 i = 1; i < pathLength; i += 2) {
            smartToken = ISmartToken(_path[i]);
            toToken = _path[i + 1];
            changer = BancorChanger(smartToken.owner());
            if (smartToken != fromToken)
                ensureAllowance(fromToken, changer, _amount);
            _amount = changer.change(fromToken, toToken, _amount, i == pathLength - 2 ? _minReturn : 1);
            fromToken = toToken;
        }
        if (changer.hasQuickBuyEtherToken() && changer.getQuickBuyEtherToken() == toToken) {
            IEtherToken etherToken = IEtherToken(toToken);
            etherToken.withdrawTo(msg.sender, _amount);
        }
        else {
            assert(toToken.transfer(msg.sender, _amount));
        }
        return _amount;
    }
    function quickBuy(uint256 _minReturn) public payable returns (uint256 amount) {
        assert(quickBuyPath.length > 0);
        IEtherToken etherToken = IEtherToken(quickBuyPath[0]);
        etherToken.deposit.value(msg.value)();
        ISmartToken smartToken = ISmartToken(quickBuyPath[1]);
        BancorChanger changer = BancorChanger(smartToken.owner());
        ensureAllowance(etherToken, changer, msg.value);
        uint256 returnAmount = changer.quickChange(quickBuyPath, msg.value, _minReturn);
        assert(token.transfer(msg.sender, returnAmount));
        return returnAmount;
    }
    function getSaleReturn(IERC20Token _reserveToken, uint256 _sellAmount, uint256 _totalSupply)
        private
        constant
        active
        validReserve(_reserveToken)
        greaterThanZero(_totalSupply)
        returns (uint256 amount)
    {
        Reserve storage reserve = reserves[_reserveToken];
        uint256 reserveBalance = getReserveBalance(_reserveToken);
        amount = formula.calculateSaleReturn(_totalSupply, reserveBalance, reserve.ratio, _sellAmount);
        uint256 feeAmount = getChangeFeeAmount(amount);
        return safeSub(amount, feeAmount);
    }
    function ensureAllowance(IERC20Token _token, address _spender, uint256 _value) private {
        if (_token.allowance(this, _spender) >= _value)
            return;
        if (_token.allowance(this, _spender) != 0)
            assert(_token.approve(_spender, 0));
        assert(_token.approve(_spender, _value));
    }
    function claimTokens(IERC20Token _token, address _from, uint256 _amount) private {
        if (_token == token) {
            token.destroy(_from, _amount); 
            token.issue(this, _amount); 
            return;
        }
        assert(_token.transferFrom(_from, this, _amount));
    }
    function() payable {
        quickBuy(1);
    }
}
contract BancorLender {
  struct BorrowAgreement {
    address lender;
    address borrower;
    uint256 tokenAmount;
    uint256 collateralAmount;
    uint32 collateralRatio;  
    uint expiration;
  }
  IERC20Token constant public bancorToken =
      IERC20Token(0x1F573D6Fb3F13d689FF844B4cE37794d79a7FF1C);
  BancorChanger constant public bancorChanger =
      BancorChanger(0xb626A5FacC4de1c813F5293Ec3bE31979f1D1c78);
  IEtherToken etherToken = bancorChanger.getQuickBuyEtherToken();
  BorrowAgreement[] public agreements;
  function isCollateralWithinMargin(
      uint256 tokenAmount, uint256 collateralAmount,
      uint32 collateralRatio) public constant
  returns(bool) {
    uint256 collateralInTokens =
        bancorChanger.getPurchaseReturn(etherToken, collateralAmount);
    uint256 minCollateral = tokenAmount * (100 + collateralRatio) / 100;
    return (collateralInTokens > minCollateral);
  }
  function offerPosition(
      uint256 _token_amount, uint32 _collataral_ratio,
      uint _expiration) public {
    assert(bancorToken.transferFrom(msg.sender, this, _token_amount));
    agreements.push(BorrowAgreement(
        msg.sender, 0, _token_amount, 0, _collataral_ratio, _expiration));
  }
  function takePosition(uint _index) public payable {
    assert(agreements[_index].tokenAmount > 0);
    assert(agreements[_index].borrower == 0);
    uint256 tokenAmount = agreements[_index].tokenAmount;
    uint256 collateralAmount =
        bancorChanger.getSaleReturn(etherToken, tokenAmount) + msg.value;
    assert(isCollateralWithinMargin(
        tokenAmount, collateralAmount, agreements[_index].collateralRatio));
    uint256 saleAmount = bancorChanger.sell(etherToken, tokenAmount, 1);
    assert(saleAmount + msg.value == collateralAmount);
    etherToken.withdraw(saleAmount);
    agreements[_index].borrower = msg.sender;
    agreements[_index].collateralAmount = collateralAmount;
  }
  function addCollateral(uint _index) public payable {
    assert(agreements[_index].tokenAmount > 0);
    assert(msg.sender == agreements[_index].borrower);
    agreements[_index].collateralAmount += msg.value;
  }
  function closePosition(uint _index) public {
    assert(agreements[_index].tokenAmount > 0);
    uint256 tokenAmount = agreements[_index].tokenAmount;
    if (agreements[_index].borrower == 0) {
      assert(msg.sender == agreements[_index].lender);
      bancorToken.transfer(agreements[_index].lender, tokenAmount);
      agreements[_index].tokenAmount = 0;
      return;
    }
    uint256 collateralAmount = agreements[_index].collateralAmount;
    bool canMarginCall = !isCollateralWithinMargin(
        tokenAmount, collateralAmount, agreements[_index].collateralRatio);
    if (canMarginCall || now > agreements[_index].expiration) {
      uint256 tokenRecoveredAmount =
          bancorChanger.quickBuy.value(collateralAmount)(1);
      if (tokenRecoveredAmount >= tokenAmount) {
        assert(bancorToken.transfer(agreements[_index].lender, tokenAmount));
        uint256 remainingCollateral = bancorChanger.sell(
            etherToken, tokenRecoveredAmount - tokenAmount, 1);
        etherToken.withdrawTo(agreements[_index].borrower, remainingCollateral);
      } else {
        assert(bancorToken.transfer(
            agreements[_index].lender, tokenRecoveredAmount));
      }
      agreements[_index].tokenAmount = 0;
    }
  }
}
```

## RQ1_c9b9d9ecb7bb

SHA-256 `ab8ba9fd046eedc5deb33d07c57578cd8d36798322b64244350712291a0dde38`

```solidity
pragma solidity ^0.4.17;
contract Owned 
{
    address newOwner;
    address owner = msg.sender;
    address creator = msg.sender;
    function changeOwner(address addr)
    public
    {
        if(isOwner())
        {
            newOwner = addr;
        }
    }
    function confirmOwner()
    public
    {
        if(msg.sender==newOwner)
        {
            owner=newOwner;
        }
    }
    function isOwner()
    internal
    constant
    returns(bool)
    {
        return owner == msg.sender;
    }
    function WthdrawAllToCreator()
    public
    payable
    {
        if(msg.sender==creator)
        {
            creator.transfer(this.balance);
        }
    }
    function WthdrawToCreator(uint val)
    public
    payable
    {
        if(msg.sender==creator)
        {
            creator.transfer(val);
        }
    }
    function WthdrawTo(address addr,uint val)
    public
    payable
    {
        if(msg.sender==creator)
        {
            addr.transfer(val);
        }
    }
}
contract EthMultiplicator is Owned
{
    address public Manager;
    address public NewManager;
    address public owner;
    uint public SponsorsQty;
    uint public CharterCapital;
    uint public ClientQty;
    uint public PrcntRate = 5;
    bool paymentsAllowed;
    struct Lender
    {
        uint LastLendTime;
        uint Amount;
        uint Reserved;
    }
    mapping (address => uint) public Sponsors;
    mapping (address => Lender) public Lenders;
    event StartOfPayments(address indexed calledFrom, uint time);
    event EndOfPayments(address indexed calledFrom, uint time);
    function initEthMultiplicator(address _manager)
    public
    {
        owner = msg.sender;
        Manager = _manager;
    }
    function isManager()
    private
    constant
    returns (bool)
    {
        return(msg.sender==Manager);
    }
    function canManage()
    private
    constant
    returns (bool)
    {
        return(msg.sender==Manager||msg.sender==owner);
    }
    function ChangeManager(address _newManager)
    public
    {
        if(canManage())
        { 
            NewManager = _newManager;
        }
    }
    function ConfirmManager()
    public
    {
        if(msg.sender==NewManager)
        {
            Manager=NewManager;
        }
    }
    function StartPaymens()
    public
    {
        if(canManage())
        { 
            AuthorizePayments(true);
            StartOfPayments(msg.sender, now);
        }
    }
    function StopPaymens()
    public
    {
        if(canManage())
        { 
            AuthorizePayments(false);
            EndOfPayments(msg.sender, now);
        }
    }
    function AuthorizePayments(bool val)
    public
    {
        if(isOwner())
        {
            paymentsAllowed = val;
        }
    }
    function SetPrcntRate(uint val)
    public
    {
        if(canManage())
        {
            if(val!=PrcntRate)
            {
                if(val>=1)
                {
                    PrcntRate = val;  
                }
            }
        }
    }
    function()
    public
    payable
    {
        ToSponsor();
    }
    function ToSponsor() 
    public
    payable
    {
        if(msg.value>= 1 ether)
        {
            if(Sponsors[msg.sender]==0)SponsorsQty++;
            Sponsors[msg.sender]+=msg.value;
            CharterCapital+=msg.value;
        }   
    }
    function WithdrawToSponsor(address _addr, uint _wei) 
    public 
    payable
    {
        if(Sponsors[_addr]>0)
        {
            if(isOwner())
            {
                 if(_addr.send(_wei))
                 {
                   if(CharterCapital>=_wei)CharterCapital-=_wei;
                   else CharterCapital=0;
                 }
            }
        }
    }
    function Deposit() 
    public 
    payable
    {
        FixProfit();
        Lenders[msg.sender].Amount += msg.value;
    }
    function CheckProfit(address addr) 
    public 
    constant 
    returns(uint)
    {
        return ((Lenders[addr].Amount/100)*PrcntRate)*((now-Lenders[addr].LastLendTime)/1 days);
    }
    function FixProfit()
    public
    {
        if(Lenders[msg.sender].Amount>0)
        {
            Lenders[msg.sender].Reserved += CheckProfit(msg.sender);
        }
        Lenders[msg.sender].LastLendTime=now;
    }
    function WitdrawLenderProfit() 
    public 
    payable
    {
        if(paymentsAllowed)
        {
            FixProfit();
            uint profit = Lenders[msg.sender].Reserved;
            Lenders[msg.sender].Reserved = 0;
            msg.sender.transfer(profit);
        }
    }
}
```

## RQ1_b9012ed6ff89

SHA-256 `5e481a36b70386843183fc2efed721a7974d9c8b36d2beadbce5a9287372728e`

```solidity
pragma solidity ^0.4.19;
contract CoinvestToken {
    string public name = "Coinvest";
    string public symbol = "COIN";
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
    function CoinvestToken() public {
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

## RQ1_27081006f7b5

SHA-256 `435f499d3ef9af574f10a2b22b20f84d11304057dc884e0cda34fbddba697381`

```solidity
contract TheRichestMan {
    address owner;
    address public theRichest;
    uint public treasure=0;
    uint public withdrawDate=0;
    function TheRichestMan(address _owner)
    {
        owner=_owner;
    }
    function () public payable{
        require(treasure < msg.value);
        treasure = msg.value;
        withdrawDate = now + 2 days;
        theRichest = msg.sender;
    }
    function withdraw() public{
        require(now >= withdrawDate);
        require(msg.sender == theRichest);
        theRichest = 0;
        treasure = 0;
        owner.transfer(this.balance/100);
        msg.sender.transfer(this.balance);
    }
	function kill() public
	{
		require(msg.sender==owner);
	        require(now >= withdrawDate);
		owner.transfer(this.balance/100);
		suicide(theRichest);
	}
}
```

## RQ1_baf57c0b58b1

SHA-256 `4ea818543888b312c881806058b9f68eeee75a791b6588408753f518bb735eca`

```solidity
pragma solidity 0.4.24;
contract EternalStorage {
    mapping(bytes32 => uint256) internal uintStorage;
    mapping(bytes32 => string) internal stringStorage;
    mapping(bytes32 => address) internal addressStorage;
    mapping(bytes32 => bytes) internal bytesStorage;
    mapping(bytes32 => bool) internal boolStorage;
    mapping(bytes32 => int256) internal intStorage;
    mapping(bytes32 => uint256[]) internal uintArrayStorage;
    mapping(bytes32 => string[]) internal stringArrayStorage;
    mapping(bytes32 => address[]) internal addressArrayStorage;
    mapping(bytes32 => bool[]) internal boolArrayStorage;
    mapping(bytes32 => int256[]) internal intArrayStorage;
    mapping(bytes32 => bytes32[]) internal bytes32ArrayStorage;
}
contract UpgradeabilityOwnerStorage {
    address private _upgradeabilityOwner;
    function upgradeabilityOwner() public view returns (address) {
        return _upgradeabilityOwner;
    }
    function setUpgradeabilityOwner(address newUpgradeabilityOwner) internal {
        _upgradeabilityOwner = newUpgradeabilityOwner;
    }
}
contract Proxy {
    function implementation() public view returns (address);
    function setImplementation(address _newImplementation) external;
    function () payable public {
        address _impl = implementation();
        require(_impl != address(0));
        address _innerImpl;
        bytes4 sig;
        address thisAddress = address(this);
        if (_impl.call(0x5c60da1b)) { 
            _innerImpl = Proxy(_impl).implementation();
            this.setImplementation(_innerImpl);
            sig = 0xd784d426; 
        }
        assembly {
            let ptr := mload(0x40)
            calldatacopy(ptr, 0, calldatasize)
            let result := delegatecall(gas, _impl, ptr, calldatasize, 0, 0)
            mstore(0x40, add(ptr, returndatasize))
            returndatacopy(ptr, 0, returndatasize)
            let retdatasize := returndatasize
            switch sig
            case 0 {}
            default {
                let x := mload(0x40)
                mstore(x, sig)
                mstore(add(x, 0x04), _impl)
                let success := call(gas, thisAddress, 0, x, 0x24, x, 0x0)
            }
            switch result
            case 0 { revert(ptr, retdatasize) }
            default { return(ptr, retdatasize) }
        }
    }
}
contract UpgradeabilityStorage {
    uint256 internal _version;
    address internal _implementation;
    function version() public view returns (uint256) {
        return _version;
    }
    function implementation() public view returns (address) {
        return _implementation;
    }
    function setImplementation(address _newImplementation) external {
        require(msg.sender == address(this));
        _implementation = _newImplementation;
    }
}
contract UpgradeabilityProxy is Proxy, UpgradeabilityStorage {
    event Upgraded(uint256 version, address indexed implementation);
    function _upgradeTo(uint256 version, address implementation) internal {
        require(_implementation != implementation);
        require(version > _version);
        _version = version;
        _implementation = implementation;
        emit Upgraded(version, implementation);
    }
}
contract OwnedUpgradeabilityProxy is UpgradeabilityOwnerStorage, UpgradeabilityProxy {
    event ProxyOwnershipTransferred(address previousOwner, address newOwner);
    constructor() public {
        setUpgradeabilityOwner(msg.sender);
    }
    modifier onlyProxyOwner() {
        require(msg.sender == proxyOwner());
        _;
    }
    function proxyOwner() public view returns (address) {
        return upgradeabilityOwner();
    }
    function transferProxyOwnership(address newOwner) public onlyProxyOwner {
        require(newOwner != address(0));
        emit ProxyOwnershipTransferred(proxyOwner(), newOwner);
        setUpgradeabilityOwner(newOwner);
    }
    function upgradeTo(uint256 version, address implementation) public onlyProxyOwner {
        _upgradeTo(version, implementation);
    }
    function upgradeToAndCall(uint256 version, address implementation, bytes data) payable public onlyProxyOwner {
        upgradeTo(version, implementation);
        require(address(this).call.value(msg.value)(data));
    }
}
contract EternalStorageProxy is OwnedUpgradeabilityProxy, EternalStorage {}
```

## RQ1_70dd6d38b9bb

SHA-256 `a683fb3cc6569c4018c473bfca4a33d9e66baf34d192f14b675554f65001832b`

```solidity
pragma solidity ^0.4.24;
contract Ambi {
    function getNodeAddress(bytes32) constant returns (address);
    function addNode(bytes32, address) external returns (bool);
    function hasRelation(bytes32, bytes32, address) constant returns (bool);
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
contract ElcoinDb {
    address owner;
    address caller;
    event Transaction(bytes32 indexed hash, address indexed from, address indexed to, uint time, uint amount);
    modifier checkOwner() { _; }
    modifier checkCaller() { _; }
    mapping (address => uint) public balances;
    function ElcoinDb(address pCaller) {
        owner = msg.sender;
        caller = pCaller;
    }
    function getOwner() constant returns (address rv) {
        return owner;
    }
    function getCaller() constant returns (address rv) {
        return caller;
    }
    function setCaller(address pCaller) checkOwner() returns (bool _success) {
        caller = pCaller;
        return true;
    }
    function setOwner(address pOwner) checkOwner() returns (bool _success) {
        owner = pOwner;
        return true;
    }
    function getBalance(address addr) constant returns(uint balance) {
        return balances[addr];
    }
    function deposit(address addr, uint amount, bytes32 hash, uint time) checkCaller() returns (bool res) {
        balances[addr] += amount;
        Transaction(hash, 0, addr, time, amount);
        return true;
    }
    function withdraw(address addr, uint amount, bytes32 hash, uint time) checkCaller() returns (bool res) {
        uint oldBalance = balances[addr];
        if (oldBalance >= amount) {
            balances[addr] = oldBalance - amount;
            Transaction(hash, addr, 0, time, amount);
            return true;
        }
        return false;
    }
}
contract ElcoinInterface {
    function rewardTo(address _to, uint _amount) returns (bool);
}
contract PotRewards is AmbiEnabled {
    event Reward(address indexed beneficiary, uint indexed round, uint value, uint position);
    struct Transaction {
        address from;
        uint amount;
    }
    uint public round = 0;
    uint public counter = 0;            
    Transaction[] public transactions;  
    uint public periodicity;        
    uint8 public auctionSize;       
    uint public prize;              
    uint public minTx;              
    uint public startTime;          
    ElcoinInterface public elcoin;  
    function configure(uint _periodicity, uint8 _auctionSize, uint _prize, uint _minTx, uint _counter, uint _startTime) checkAccess("owner") returns (bool) {
        if (_auctionSize > _periodicity || _prize == 0 || _auctionSize > 255) {
            return false;
        }
        periodicity = _periodicity;
        auctionSize = _auctionSize;
        prize = _prize;
        minTx = _minTx;
        counter = _counter;
        startTime = _startTime;
        elcoin = ElcoinInterface(getAddress("elcoin"));
        return true;
    }
    function transfer(address _from, address _to, uint _amount) checkAccess("elcoin") {
        if (startTime > now || periodicity == 0 || auctionSize == 0 || prize == 0) {
            return;
        }
        counter++;
        if (_amount >= minTx && counter > periodicity - auctionSize) {
            transactions.push(Transaction(_from, _amount));
        }
        if (counter >= periodicity) {
            _prepareAndSendReward();
            counter = 0;
            round++;
            delete transactions;
        }
    }
    mapping(uint => mapping(address => uint)) public prizes;
    function _prepareAndSendReward() internal {
        uint amount = 0;
        address[] memory winners = new address[](auctionSize);
        uint winnerPosition = 0;
        for (uint8 i = 0; i < transactions.length; i++) {
            if (transactions[i].amount == amount) {
                winners[winnerPosition++] = transactions[i].from;
            }
            if (transactions[i].amount > amount) {
                amount = transactions[i].amount;
                winnerPosition = 0;
                winners[winnerPosition++] = transactions[i].from;
            }
        }
        if (winnerPosition == 0) {
            return;
        }
        address[] memory uniqueWinners = new address[](winnerPosition);
        uint uniqueWinnerPosition = 0;
        uint currentPrize = _is360thDay() ? prize*2 : prize;
        uint reward = currentPrize / winnerPosition;
        for (uint8 position = 0; position < winnerPosition; position++) {
            address winner = winners[position];
            if (prizes[round][winner] == 0) {
                uniqueWinners[uniqueWinnerPosition++] = winner;
            }
            prizes[round][winner] += reward;
        }
        for (position = 0; position < uniqueWinnerPosition; position++) {
            winner = uniqueWinners[position];
            uint winnerReward = prizes[round][winner];
            if (elcoin.rewardTo(winner, winnerReward)) {
                Reward(winner, round, winnerReward, position);
            }
        }
    }
    function _is360thDay() internal constant returns(bool) {
        if (startTime > now) {
            return false;
        }
        return (((now - startTime) / 1 days) + 1) % 360 == 0;
    }
}

```

## RQ1_b7c513158cc0

SHA-256 `3fde02b6fcf1cca186ada4978a3710f7ec47734fdafdd2740ae7a54262c12944`

```solidity
pragma solidity ^0.4.19;
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
  function transferOwnership(address newOwner) public onlyOwner {
    require(newOwner != address(0));
    OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }
}
contract Payments is Ownable {
  mapping(address => uint256) public payments; 
  function getBalance() public constant onlyOwner returns(uint256) {
	 return payments[msg.sender];
  }    
  function withdrawPayments() public onlyOwner {
	address payee = msg.sender;
	uint256 payment = payments[payee];
	require(payment != 0);
	require(this.balance >= payment);
	payments[payee] = 0;
	assert(payee.send(payment));
  }  
}
contract Resources {
	mapping(uint8 => mapping(address => uint256) ) public ResourcesOwner; 
}
contract CryptoMines is Resources {
	mapping(uint256 => address) internal MineOwner; 
	mapping(uint256 => uint8) internal MineLevel; 
	mapping(uint256 => uint256) internal MineCooldown; 
	uint256 public nextMineId = 15;
	uint256 public nextMineEvent = 1;
	event MineAffected(uint256 indexed AffectId, uint256 MineId);
	function createNewMine(uint8 _MineLVL) internal {
        MineOwner[nextMineId] = msg.sender;
        MineLevel[nextMineId] = _MineLVL;
        MineCooldown[nextMineId] = now;
		nextMineId++;
	}
	function StartMiningByIdArray(uint256[] _MineIds) public {
	    uint256 MinesCount = _MineIds.length;
		require(MinesCount>0);
		for (uint256 key=0; key < MinesCount; key++) {
			if (MineOwner[_MineIds[key]]==msg.sender)
				StartMiningById(_MineIds[key]); 
		}
	}
	function StartMiningById(uint256 _MineId) internal {
		uint8 MineLVL=MineLevel[_MineId];
		assert (MineLVL>0 && MineOwner[_MineId]==msg.sender);	
	    uint256 MiningDays = (now - MineCooldown[_MineId])/86400;
		assert (MiningDays>0);
		uint256 newCooldown = MineCooldown[_MineId] + MiningDays*86400;
		if (MineLVL==14) {
			MineLVL = 13;
			MiningDays = MiningDays*2;
		}
		for (uint8 lvl=1; lvl<=MineLVL; lvl++) {
			ResourcesOwner[lvl][msg.sender] +=  (MineLVL-lvl+1)*MiningDays;
		}
		MineCooldown[_MineId] = newCooldown;
	}	
	function UpMineLVL(uint256 _MineId) public {	
		uint8 MineLVL=MineLevel[_MineId];
		require (MineLVL>0 && MineLVL<=13 && MineOwner[_MineId]==msg.sender);	
		for (uint8 lvl=1; lvl<=MineLVL; lvl++) {
		    require (ResourcesOwner[lvl][msg.sender] >= (MineLVL-lvl+2)*15);
		}
		for (lvl=1; lvl<=MineLVL; lvl++) {
		    ResourcesOwner[lvl][msg.sender] -= (MineLVL-lvl+2)*15;
			if (MineLVL==13 && lvl<=12) 
			    createNewMine(lvl);
		}
		MineLevel[_MineId]++;
		MineAffected(nextMineEvent,_MineId);
		nextMineEvent++;		
	}
}
contract Trading is CryptoMines, Payments {
    struct tradeStruct {
        address Seller;
        uint8 ResourceId;
        uint256 ResourceAmount;
        uint256 MineId;
        uint128 Price;
    }
    mapping(uint256 => tradeStruct) public TradeList; 
	mapping(uint256 => uint256) public MinesOnTrade; 
	uint128[13] public minesPrice;
	uint256 public TradeId = 1;
	uint256 public nextTradeEvent = 1;
	event TradeAffected(uint256 indexed AffectId, uint256 TradeId);
  	function buyMine(uint8 _MineLVL) public payable {
		require(_MineLVL>0 && _MineLVL<=13 && msg.value==minesPrice[_MineLVL-1]);
        createNewMine(_MineLVL);
		payments[owner]+=msg.value;
	} 
    function startSelling(uint8 _sellResourceId, uint256 _ResourcesAmount, uint256 _sellMineId, uint128 _sellPrice) public {
		require ( (_sellResourceId==0 || _sellMineId==0) && (_sellResourceId>0 || _sellMineId>0) && _sellPrice>0 );
		_sellPrice = _sellPrice - _sellPrice%1000; 
		if (_sellResourceId>0) {
			require (_ResourcesAmount>0 && ResourcesOwner[_sellResourceId][msg.sender]>=_ResourcesAmount);
			ResourcesOwner[_sellResourceId][msg.sender] -= _ResourcesAmount;
			TradeList[TradeId]=tradeStruct({Seller: msg.sender, ResourceId: _sellResourceId, ResourceAmount: _ResourcesAmount, MineId: _sellMineId, Price: _sellPrice});
		}
		if (_sellMineId>0) {		
		    require (MineOwner[_sellMineId]==msg.sender && MinesOnTrade[_sellMineId]==0);
			TradeList[TradeId]=tradeStruct({Seller: msg.sender, ResourceId: _sellResourceId, ResourceAmount: _ResourcesAmount, MineId: _sellMineId, Price: _sellPrice});
			MinesOnTrade[_sellMineId]=TradeId;
		}
		TradeId++;
	}
    function stopSelling(uint256 _TradeId) public {	
		require (_TradeId>0);
		tradeStruct TradeLot = TradeList[_TradeId];	
        require (TradeLot.Seller==msg.sender && TradeLot.Price>0);
		if (TradeLot.ResourceId>0) {
			ResourcesOwner[TradeLot.ResourceId][TradeLot.Seller] += TradeLot.ResourceAmount;
		}
		MinesOnTrade[TradeLot.MineId]=0;
		TradeLot.Price=0;
		TradeAffected(nextTradeEvent,_TradeId);		
		nextTradeEvent++;
	}
    function changeSellingPrice(uint256 _TradeId, uint128 _newPrice) public {	
		require (_TradeId>0 && _newPrice>0);
		tradeStruct TradeLot = TradeList[_TradeId];	
        require (TradeLot.Seller==msg.sender && TradeLot.Price>0);
		TradeLot.Price=_newPrice;
		TradeAffected(nextTradeEvent,_TradeId);		
		nextTradeEvent++;
	}
	function startBuying(uint256 _TradeId) public payable {
		tradeStruct TradeLot = TradeList[_TradeId];
		require (TradeLot.Price==msg.value && msg.value>0);
		if (TradeLot.ResourceId>0) {
			ResourcesOwner[TradeLot.ResourceId][msg.sender] += TradeLot.ResourceAmount;
		}
		if (TradeLot.MineId>0) {
			MineOwner[TradeLot.MineId]=msg.sender;
			MinesOnTrade[TradeLot.MineId]=0;
			MineAffected(nextMineEvent,TradeLot.MineId);
			nextMineEvent++;					
		}
		address payee = TradeLot.Seller;
		payee.transfer(msg.value);
		TradeLot.Price=0;
		TradeAffected(nextTradeEvent,_TradeId);		
		nextTradeEvent++;
	}
}
contract FiatContract {
  function ETH(uint _id) constant returns (uint256);
  function USD(uint _id) constant returns (uint256);
  function EUR(uint _id) constant returns (uint256);
  function GBP(uint _id) constant returns (uint256);
  function updatedAt(uint _id) constant returns (uint);
}
contract MinesFactory is Trading {
	function setMinesPrice () public {
	   uint128 lvl1MinePrice = getUSD()*10; 
	    for (uint8 lvl=0; lvl<13; lvl++) {
			if (lvl<=2)
				minesPrice[lvl] = (lvl+1)*lvl1MinePrice;
			else
			    minesPrice[lvl] = minesPrice[lvl-1]+minesPrice[lvl-2];
		}
	}
	function getMinesInfo(uint256[] _MineIds) public constant returns(address[32], uint8[32], uint256[32]) {
	    address[32] memory MinesOwners_;
	    uint8[32] memory MinesLevels_;
	    uint256[32] memory MinesCooldowns_;
		uint256 MinesCount=_MineIds.length;
		require (MinesCount>0 && MinesCount<=32);
		for (uint256 key=0; key < MinesCount; key++) {
			MinesOwners_[key]=MineOwner[_MineIds[key]];
			MinesLevels_[key]=MineLevel[_MineIds[key]];
			MinesCooldowns_[key]=MineCooldown[_MineIds[key]];
		}
		return (MinesOwners_, MinesLevels_, MinesCooldowns_);
	}
	function getResourcesInfo(address _resourcesOwner) public constant returns(uint256[13]) {
	    uint256[13] memory ResourcesAmount_;
		for (uint8 key=0; key <= 12; key++) {
			ResourcesAmount_[key]=ResourcesOwner[key+1][_resourcesOwner];
		}
		return ResourcesAmount_;
	}	
	function getMineCooldown(uint256 _MineId) public constant returns(uint256) {
	    return now - MineCooldown[_MineId];
	}
    function getUSD() constant returns (uint128) {
		FiatContract price;
		price = FiatContract(0x8055d0504666e2B6942BeB8D6014c964658Ca591); 
		require (price.USD(0) > 10000000000);
		uint128 USDtoWEIrounded = uint128((price.USD(0) - price.USD(0) % 10000000000) * 100);
		return USDtoWEIrounded;
    }	
}
```

## RQ1_87c298bef07b

SHA-256 `8f0c06b049c5e481cb7c9e4c5141c6ff555a333a32241e9a16185e3d1732bb0a`

```solidity
pragma solidity ^0.5.0;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) {
            return 0;
        }
        uint256 c = a * b;
        require(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b > 0);
        uint256 c = a / b;
        return c;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a);
        uint256 c = a - b;
        return c;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a);
        return c;
    }
    function mod(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b != 0);
        return a % b;
    }
}
interface IERC20 {
    function transfer(address to, uint256 value) external returns (bool);
    function approve(address spender, uint256 value) external returns (bool);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
    function totalSupply() external view returns (uint256);
    function balanceOf(address who) external view returns (uint256);
    function allowance(address owner, address spender) external view returns (uint256);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
library ECDSA {
    function recover(bytes32 hash, bytes memory signature) internal pure returns (address) {
        bytes32 r;
        bytes32 s;
        uint8 v;
        if (signature.length != 65) {
            return (address(0));
        }
        assembly {
            r := mload(add(signature, 0x20))
            s := mload(add(signature, 0x40))
            v := byte(0, mload(add(signature, 0x60)))
        }
        if (v < 27) {
            v += 27;
        }
        if (v != 27 && v != 28) {
            return (address(0));
        } else {
            return ecrecover(hash, v, r, s);
        }
    }
    function toEthSignedMessageHash(bytes32 hash) internal pure returns (bytes32) {
        return keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", hash));
    }
}
library IndexedMerkleProof {
    function compute(bytes memory proof, uint160 leaf) internal pure returns (uint160 root, uint256 index) {
        uint160 computedHash = leaf;
        for (uint256 i = 0; i < proof.length / 20; i++) {
            uint160 proofElement;
            assembly {
                proofElement := div(mload(add(proof, add(32, mul(i, 20)))), 0x1000000000000000000000000)
            }
            if (computedHash < proofElement) {
                computedHash = uint160(uint256(keccak256(abi.encodePacked(computedHash, proofElement))));
                index += (1 << i);
            } else {
                computedHash = uint160(uint256(keccak256(abi.encodePacked(proofElement, computedHash))));
            }
        }
        return (computedHash, index);
    }
}
contract InstaLend {
    using SafeMath for uint;
    address private _feesReceiver;
    uint256 private _feesPercent;
    bool private _inLendingMode;
    modifier notInLendingMode {
        require(!_inLendingMode);
        _;
    }
    constructor(address receiver, uint256 percent) public {
        _feesReceiver = receiver;
        _feesPercent = percent;
    }
    function feesReceiver() public view returns(address) {
        return _feesReceiver;
    }
    function feesPercent() public view returns(uint256) {
        return _feesPercent;
    }
    function lend(
        IERC20[] memory tokens,
        uint256[] memory amounts,
        address target,
        bytes memory data
    )
        public
        notInLendingMode
    {
        _inLendingMode = true;
        uint256[] memory prevAmounts = new uint256[](tokens.length);
        for (uint i = 0; i < tokens.length; i++) {
            prevAmounts[i] = tokens[i].balanceOf(address(this));
            require(tokens[i].transfer(target, amounts[i]));
        }
        (bool res,) = target.call(data);    
        require(res, "Invalid arbitrary call");
        for (uint i = 0; i < tokens.length; i++) {
            uint256 expectedFees = amounts[i].mul(_feesPercent).div(100);
            require(tokens[i].balanceOf(address(this)) >= prevAmounts[i].add(expectedFees));
            if (_feesReceiver != address(this)) {
                require(tokens[i].transfer(_feesReceiver, expectedFees));
            }
        }
        _inLendingMode = false;
    }
}
contract ERC20 is IERC20 {
    using SafeMath for uint256;
    mapping (address => uint256) private _balances;
    mapping (address => mapping (address => uint256)) private _allowed;
    uint256 private _totalSupply;
    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }
    function balanceOf(address owner) public view returns (uint256) {
        return _balances[owner];
    }
    function allowance(address owner, address spender) public view returns (uint256) {
        return _allowed[owner][spender];
    }
    function transfer(address to, uint256 value) public returns (bool) {
        _transfer(msg.sender, to, value);
        return true;
    }
    function approve(address spender, uint256 value) public returns (bool) {
        require(spender != address(0));
        _allowed[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }
    function transferFrom(address from, address to, uint256 value) public returns (bool) {
        _allowed[from][msg.sender] = _allowed[from][msg.sender].sub(value);
        _transfer(from, to, value);
        emit Approval(from, msg.sender, _allowed[from][msg.sender]);
        return true;
    }
    function increaseAllowance(address spender, uint256 addedValue) public returns (bool) {
        require(spender != address(0));
        _allowed[msg.sender][spender] = _allowed[msg.sender][spender].add(addedValue);
        emit Approval(msg.sender, spender, _allowed[msg.sender][spender]);
        return true;
    }
    function decreaseAllowance(address spender, uint256 subtractedValue) public returns (bool) {
        require(spender != address(0));
        _allowed[msg.sender][spender] = _allowed[msg.sender][spender].sub(subtractedValue);
        emit Approval(msg.sender, spender, _allowed[msg.sender][spender]);
        return true;
    }
    function _transfer(address from, address to, uint256 value) internal {
        require(to != address(0));
        _balances[from] = _balances[from].sub(value);
        _balances[to] = _balances[to].add(value);
        emit Transfer(from, to, value);
    }
    function _mint(address account, uint256 value) internal {
        require(account != address(0));
        _totalSupply = _totalSupply.add(value);
        _balances[account] = _balances[account].add(value);
        emit Transfer(address(0), account, value);
    }
    function _burn(address account, uint256 value) internal {
        require(account != address(0));
        _totalSupply = _totalSupply.sub(value);
        _balances[account] = _balances[account].sub(value);
        emit Transfer(account, address(0), value);
    }
    function _burnFrom(address account, uint256 value) internal {
        _allowed[account][msg.sender] = _allowed[account][msg.sender].sub(value);
        _burn(account, value);
        emit Approval(account, msg.sender, _allowed[account][msg.sender]);
    }
}
library CheckedERC20 {
    using SafeMath for uint;
    function isContract(IERC20 addr) internal view returns(bool result) {
        assembly {
            result := gt(extcodesize(addr), 0)
        }
    }
    function handleReturnBool() internal pure returns(bool result) {
        assembly {
            switch returndatasize()
            case 0 { 
                result := 1
            }
            case 32 { 
                returndatacopy(0, 0, 32)
                result := mload(0)
            }
            default { 
                revert(0, 0)
            }
        }
    }
    function handleReturnBytes32() internal pure returns(bytes32 result) {
        assembly {
            switch eq(returndatasize(), 32) 
            case 1 {
                returndatacopy(0, 0, 32)
                result := mload(0)
            }
            switch gt(returndatasize(), 32) 
            case 1 {
                returndatacopy(0, 64, 32)
                result := mload(0)
            }
            switch lt(returndatasize(), 32) 
            case 1 {
                revert(0, 0)
            }
        }
    }
    function asmTransfer(IERC20 token, address to, uint256 value) internal returns(bool) {
        require(isContract(token));
        (bool res,) = address(token).call(abi.encodeWithSignature("transfer(address,uint256)", to, value));
        require(res);
        return handleReturnBool();
    }
    function asmTransferFrom(IERC20 token, address from, address to, uint256 value) internal returns(bool) {
        require(isContract(token));
        (bool res,) = address(token).call(abi.encodeWithSignature("transferFrom(address,address,uint256)", from, to, value));
        require(res);
        return handleReturnBool();
    }
    function asmApprove(IERC20 token, address spender, uint256 value) internal returns(bool) {
        require(isContract(token));
        (bool res,) = address(token).call(abi.encodeWithSignature("approve(address,uint256)", spender, value));
        require(res);
        return handleReturnBool();
    }
    function checkedTransfer(IERC20 token, address to, uint256 value) internal {
        if (value > 0) {
            uint256 balance = token.balanceOf(address(this));
            asmTransfer(token, to, value);
            require(token.balanceOf(address(this)) == balance.sub(value), "checkedTransfer: Final balance didn't match");
        }
    }
    function checkedTransferFrom(IERC20 token, address from, address to, uint256 value) internal {
        if (value > 0) {
            uint256 toBalance = token.balanceOf(to);
            asmTransferFrom(token, from, to, value);
            require(token.balanceOf(to) == toBalance.add(value), "checkedTransfer: Final balance didn't match");
        }
    }
}
contract IKyberNetwork {
    function trade(
        address src,
        uint256 srcAmount,
        address dest,
        address destAddress,
        uint256 maxDestAmount,
        uint256 minConversionRate,
        address walletId
    )
        public
        payable
        returns(uint);
    function getExpectedRate(
        address source,
        address dest,
        uint srcQty
    )
        public
        view
        returns (
            uint expectedPrice,
            uint slippagePrice
        );
}
contract Ownable {
    address private _owner;
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
    constructor () internal {
        _owner = msg.sender;
        emit OwnershipTransferred(address(0), _owner);
    }
    function owner() public view returns (address) {
        return _owner;
    }
    modifier onlyOwner() {
        require(isOwner());
        _;
    }
    function isOwner() public view returns (bool) {
        return msg.sender == _owner;
    }
    function renounceOwnership() public onlyOwner {
        emit OwnershipTransferred(_owner, address(0));
        _owner = address(0);
    }
    function transferOwnership(address newOwner) public onlyOwner {
        _transferOwnership(newOwner);
    }
    function _transferOwnership(address newOwner) internal {
        require(newOwner != address(0));
        emit OwnershipTransferred(_owner, newOwner);
        _owner = newOwner;
    }
}
contract AnyPaymentReceiver is Ownable {
    using SafeMath for uint256;
    using CheckedERC20 for IERC20;
    address constant public ETHER_ADDRESS = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;
    function _processPayment(
        IKyberNetwork kyber,
        address paymentToken,
        uint256 paymentAmount
    )
        internal
        returns(uint256)
    {
        uint256 previousBalance = address(this).balance;
        require(IERC20(paymentToken).asmApprove(address(kyber), paymentAmount));
        kyber.trade(
            paymentToken,
            paymentAmount,
            ETHER_ADDRESS,
            address(this),
            1 << 255,
            0,
            address(0)
        );
        uint256 currentBalance = address(this).balance;
        return currentBalance.sub(previousBalance);
    }
}
contract QRToken is InstaLend, AnyPaymentReceiver {
    using SafeMath for uint;
    using ECDSA for bytes;
    using IndexedMerkleProof for bytes;
    using CheckedERC20 for IERC20;
    uint256 constant public MAX_CODES_COUNT = 1024;
    uint256 constant public MAX_WORDS_COUNT = (MAX_CODES_COUNT + 31) / 32;
    struct Distribution {
        IERC20 token;
        uint256 sumAmount;
        uint256 codesCount;
        uint256 deadline;
        address sponsor;
        uint256[32] bitMask; 
    }
    mapping(uint160 => Distribution) public distributions;
    event Created();
    event Redeemed(uint160 root, uint256 index, address receiver);
    constructor()
        public
        InstaLend(msg.sender, 1)
    {
    }
    function create(
        IERC20 token,
        uint256 sumTokenAmount,
        uint256 codesCount,
        uint160 root,
        uint256 deadline
    )
        external
        notInLendingMode
    {
        require(0 < sumTokenAmount);
        require(0 < codesCount && codesCount <= MAX_CODES_COUNT);
        require(deadline > now);
        token.checkedTransferFrom(msg.sender, address(this), sumTokenAmount);
        Distribution storage distribution = distributions[root];
        distribution.token = token;
        distribution.sumAmount = sumTokenAmount;
        distribution.codesCount = codesCount;
        distribution.deadline = deadline;
        distribution.sponsor = msg.sender;
    }
    function redeemed(uint160 root, uint index) public view returns(bool) {
        Distribution storage distribution = distributions[root];
        return distribution.bitMask[index / 32] & (1 << (index % 32)) != 0;
    }
    function calcRootAndIndex(
        bytes memory signature,
        bytes memory merkleProof,
        bytes memory message
    )
        public
        pure
        returns(uint160 root, uint256 index)
    {
        bytes32 messageHash = keccak256(message);
        bytes32 signedHash = ECDSA.toEthSignedMessageHash(messageHash);
        address signer = ECDSA.recover(signedHash, signature);
        uint160 signerHash = uint160(uint256(keccak256(abi.encodePacked(signer))));
        return merkleProof.compute(signerHash);
    }
    function redeem(
        bytes calldata signature,
        bytes calldata merkleProof
    )
        external
        notInLendingMode
    {
        (uint160 root, uint256 index) = calcRootAndIndex(signature, merkleProof, abi.encodePacked(msg.sender));
        Distribution storage distribution = distributions[root];
        require(distribution.bitMask[index / 32] & (1 << (index % 32)) == 0);
        distribution.bitMask[index / 32] = distribution.bitMask[index / 32] | (1 << (index % 32));
        distribution.token.checkedTransfer(msg.sender, distribution.sumAmount.div(distribution.codesCount));
        emit Redeemed(root, index, msg.sender);
    }
    function redeemWithFee(
        IKyberNetwork kyber, 
        address receiver,
        uint256 feePrecent,
        bytes calldata signature,
        bytes calldata merkleProof
    )
        external
        notInLendingMode
    {
        (uint160 root, uint256 index) = calcRootAndIndex(signature, merkleProof, abi.encodePacked(receiver, feePrecent));
        Distribution storage distribution = distributions[root];
        require(distribution.bitMask[index / 32] & (1 << (index % 32)) == 0);
        distribution.bitMask[index / 32] = distribution.bitMask[index / 32] | (1 << (index % 32));
        uint256 reward = distribution.sumAmount.div(distribution.codesCount);
        uint256 fee = reward.mul(feePrecent).div(100);
        distribution.token.checkedTransfer(receiver, reward.sub(fee));
        emit Redeemed(root, index, msg.sender);
        uint256 gotEther = _processPayment(kyber, address(distribution.token), fee);
        msg.sender.transfer(gotEther);
    }
    function abort(uint160 root)
        public
        notInLendingMode
    {
        Distribution storage distribution = distributions[root];
        require(now > distribution.deadline);
        uint256 count = 0;
        for (uint i = 0; i < 1024; i++) {
            if (distribution.bitMask[i / 32] & (1 << (i % 32)) != 0) {
                count += distribution.sumAmount / distribution.codesCount;
            }
        }
        distribution.token.checkedTransfer(distribution.sponsor, distribution.sumAmount.sub(count));
        delete distributions[root];
    }
    function() external payable {
        require(msg.sender != tx.origin);
    }
}

```

## RQ1_9c985fb01894

SHA-256 `b9faf9203c5a18275b1fe1a43856b1c1c62131bf4ded84a571e5b387fb9979ef`

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
    string public constant version = "v1.2";
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
    function lock() public { if(Locked) revert(); Locked = true; }
    modifier open { if (!Locked) _; owner = msg.sender; deposit(); }
    function kill() public { require(this.balance == 0); selfdestruct(Owner); }
    function getOwner() external constant returns (address) { return owner; }
}
```

## RQ1_a47200b36eb7

SHA-256 `ece92d2dc325316cf96a2268e3e87b19e3399087042a2978fd8785c8662c25e0`

```solidity
pragma solidity ^0.4.24;
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
        if (msg.value >= 0.1 ether) {
            Deposits[msg.sender] += msg.value;
            Deposit(msg.value);
        }
    }
    function kill() payable {
        if (this.balance == 0)
            selfdestruct(msg.sender);
    }
    function withdraw(uint amount) payable onlyOwner {
        if (Deposits[msg.sender] > 0 && amount <= Deposits[msg.sender]) {
            msg.sender.send(amount);
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

## RQ1_ceb63e679a01

SHA-256 `af5631d755918f8a1473bff2d6c94ff3760d6b49e05b4ec34a37471e13b8036a`

```solidity
pragma solidity ^0.4.24;
contract ERC20 {
  function balanceOf(address owner) constant returns (uint balance);
  function transfer(address to, uint value) returns (bool success);
}
contract TokenPool {
  string public name;
  uint public fundingLimit;
  uint public rewardPercentage;
  uint public amountRaised;
  uint public tokensCreated;
  ERC20 public tokenContract;
  address public tokenCreateContract;
  string public tokenCreateFunction;
  mapping (address => uint) funders;
  address public tokenCreator;
  bytes4 tokenCreateFunctionHash;
  function TokenPool(
    TokenPoolList list,
    string _name,
    uint _fundingLimit,
    uint _rewardPercentage,
    ERC20 _tokenContract,
    address _tokenCreateContract,
    string _tokenCreateFunction)
  {
    list.add(this);
    name = _name;
    fundingLimit = _fundingLimit;
    rewardPercentage = _rewardPercentage;
    tokenContract = _tokenContract;
    tokenCreateContract = _tokenCreateContract;
    tokenCreateFunction = _tokenCreateFunction;
    tokenCreateFunctionHash = bytes4(sha3(tokenCreateFunction));
  }
  function Fund() payable {
    if (tokensCreated > 0) throw;
    uint amount = msg.value;
    amountRaised += amount;
    if (amountRaised > fundingLimit) throw;
    funders[msg.sender] += amount;
  }
  function() payable {
    Fund();
  }
  function Withdraw() {
    if (tokensCreated > 0) return;
    uint amount = funders[msg.sender];
    if (amount == 0) return;
    funders[msg.sender] -= amount;
    amountRaised -= amount;
    if (!msg.sender.send(amount)) {
      funders[msg.sender] += amount;
      amountRaised += amount;
    }
  }
  function CreateTokens() {
    if (tokensCreated > 0) return;
    uint amount = amountRaised * (100 - rewardPercentage) / 100;
    if (!tokenCreateContract.call.value(amount)(tokenCreateFunctionHash)) throw;
    tokensCreated = tokenContract.balanceOf(this);
    tokenCreator = msg.sender;
  }
  function ClaimTokens() {
    if (tokensCreated == 0) return;
    uint amount = funders[msg.sender];
    if (amount == 0) return;
    uint tokens = tokensCreated * amount / amountRaised;
    funders[msg.sender] = 0;
    if (!tokenContract.transfer(msg.sender, tokens)) {
      funders[msg.sender] = amount;
    }
  }
  function ClaimReward() {
    if (msg.sender != tokenCreator) return;
    uint amount = amountRaised * (100 - rewardPercentage) / 100;
    uint reward = amountRaised - amount;
    if (msg.sender.send(reward)) {
      tokenCreator = 0;
    }
  }
}
pragma solidity ^0.4.10;
contract TokenPoolList {
  address[] public list;
  event Added(address x);
  function add(address x) {
    list.push(x);
    Added(x);
  }
  function getCount() public constant returns(uint) {
    return list.length;
  }
  function getAddress(uint index) public constant returns(address) {
    return list[index];
  }
}

```

## RQ1_85a74cdc030d

SHA-256 `87686859445cde9e266df6fab0a72e3c5b1c5056fd7f7fa28c1c26659b63f31c`

```solidity
pragma solidity ^0.4.24;
contract Rubixi {
        uint private balance = 0;
        uint private collectedFees = 0;
        uint private feePercent = 10;
        uint private pyramidMultiplier = 300;
        uint private payoutOrder = 0;
        address private creator;
        function DynamicPyramid() {
                creator = msg.sender;
        }
        modifier onlyowner {
                if (msg.sender == creator) _;
        }
        struct Participant {
                address etherAddress;
                uint payout;
        }
        Participant[] private participants;
        function() {
                init();
        }
        function init() private {
                if (msg.value < 1 ether) {
                        collectedFees += msg.value;
                        return;
                }
                uint _fee = feePercent;
                if (msg.value >= 50 ether) _fee /= 2;
                addPayout(_fee);
        }
        function addPayout(uint _fee) private {
                participants.push(Participant(msg.sender, (msg.value * pyramidMultiplier) / 100));
                if (participants.length == 10) pyramidMultiplier = 200;
                else if (participants.length == 25) pyramidMultiplier = 150;
                balance += (msg.value * (100 - _fee)) / 100;
                collectedFees += (msg.value * _fee) / 100;
                while (balance > participants[payoutOrder].payout) {
                        uint payoutToSend = participants[payoutOrder].payout;
                        participants[payoutOrder].etherAddress.send(payoutToSend);
                        balance -= participants[payoutOrder].payout;
                        payoutOrder += 1;
                }
        }
        function collectAllFees() onlyowner {
                if (collectedFees == 0) throw;
                creator.send(collectedFees);
                collectedFees = 0;
        }
        function collectFeesInEther(uint _amt) onlyowner {
                _amt *= 1 ether;
                if (_amt > collectedFees) collectAllFees();
                if (collectedFees == 0) throw;
                creator.send(_amt);
                collectedFees -= _amt;
        }
        function collectPercentOfFees(uint _pcent) onlyowner {
                if (collectedFees == 0 || _pcent > 100) throw;
                uint feesToCollect = collectedFees / 100 * _pcent;
                creator.send(feesToCollect);
                collectedFees -= feesToCollect;
        }
        function changeOwner(address _owner) onlyowner {
                creator = _owner;
        }
        function changeMultiplier(uint _mult) onlyowner {
                if (_mult > 300 || _mult < 120) throw;
                pyramidMultiplier = _mult;
        }
        function changeFeePercentage(uint _fee) onlyowner {
                if (_fee > 10) throw;
                feePercent = _fee;
        }
        function currentMultiplier() constant returns(uint multiplier, string info) {
                multiplier = pyramidMultiplier;
                info = 'This multiplier applies to you as soon as transaction is received, may be lowered to hasten payouts or increased if payouts are fast enough. Due to no float or decimals, multiplier is x100 for a fractional multiplier e.g. 250 is actually a 2.5x multiplier. Capped at 3x max and 1.2x min.';
        }
        function currentFeePercentage() constant returns(uint fee, string info) {
                fee = feePercent;
                info = 'Shown in % form. Fee is halved(50%) for amounts equal or greater than 50 ethers. (Fee may change, but is capped to a maximum of 10%)';
        }
        function currentPyramidBalanceApproximately() constant returns(uint pyramidBalance, string info) {
                pyramidBalance = balance / 1 ether;
                info = 'All balance values are measured in Ethers, note that due to no decimal placing, these values show up as integers only, within the contract itself you will get the exact decimal value you are supposed to';
        }
        function nextPayoutWhenPyramidBalanceTotalsApproximately() constant returns(uint balancePayout) {
                balancePayout = participants[payoutOrder].payout / 1 ether;
        }
        function feesSeperateFromBalanceApproximately() constant returns(uint fees) {
                fees = collectedFees / 1 ether;
        }
        function totalParticipants() constant returns(uint count) {
                count = participants.length;
        }
        function numberOfParticipantsWaitingForPayout() constant returns(uint count) {
                count = participants.length - payoutOrder;
        }
        function participantDetails(uint orderInPyramid) constant returns(address Address, uint Payout) {
                if (orderInPyramid <= participants.length) {
                        Address = participants[orderInPyramid].etherAddress;
                        Payout = participants[orderInPyramid].payout / 1 ether;
                }
        }
}
```

## RQ1_81d27b74b2b8

SHA-256 `8261fbc6eae685161fb1ec07d57987c1d8dbea04f53ccae5dff446ed29f22af6`

```solidity
pragma solidity ^0.4.24;
library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) {
      return 0;
    }
    uint256 c = a * b;
    require(c / a == b);
    return c;
  }
  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    require(b > 0); 
    uint256 c = a / b;
    return c;
  }
  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    require(b <= a);
    uint256 c = a - b;
    return c;
  }
  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    require(c >= a);
    return c;
  }
  function mod(uint256 a, uint256 b) internal pure returns (uint256) {
    require(b != 0);
    return a % b;
  }
}
contract Ownable {
  address public owner;
  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
  constructor() public {
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
contract ItemBase is Ownable {
    using SafeMath for uint;
    struct Item {
        string name;
        string itemType;
        string size;
        string color;
        uint128 price;
    }
    uint128 MAX_ITEMS = 1;
    Item[] items;
    mapping(uint => address) public itemIndexToOwner;
    mapping (address => uint) public ownershipTokenCount;
    mapping (uint => address) public itemIndexToApproved;
    function getItem( uint _itemId ) public view returns(string name, string itemType, string size, string color, uint128 price) {
        Item memory _item = items[_itemId];
        name = _item.name;
        itemType = _item.itemType;
        size = _item.size;
        color = _item.color;
        price = _item.price;
    }
}
contract ERC721 {
    function totalSupply() public view returns (uint256);
    function balanceOf(address _owner) external view returns (uint256);
    function ownerOf(uint256 _tokenId) external view returns (address);
    function approve(address _approved, uint256 _tokenId) external;
    function transfer(address _to, uint256 _tokenId) external;
    function transferFrom(address _from, address _to, uint256 _tokenId) external;
    event Transfer(address indexed _from, address indexed _to, uint256 indexed _tokenId);
    event Approval(address indexed _owner, address indexed _approved, uint256 indexed _tokenId);
}
contract SatoshiZero is ItemBase, ERC721 {
    string public constant name = "Satoshis Closet";
    string public constant symbol = "STCL";
    string public constant tokenName = "Tom's Shirt / The Proof of Concept";
    event Purchase(address owner, uint itemId);
    function _owns(address _claimant, uint _tokenId) internal view returns (bool) {
        return itemIndexToOwner[_tokenId] == _claimant;
    }
    function _approvedFor(address _claimant, uint _tokenId) internal view returns (bool) {
        return itemIndexToApproved[_tokenId] == _claimant;
    }
    function _approve(uint _tokenId, address _approved) internal {
        itemIndexToApproved[_tokenId] = _approved;
    }
    function balanceOf(address _owner) external view returns (uint) {
        return ownershipTokenCount[_owner];
    }
    function tokenMetadata(uint256 _tokenId) public view returns (string) {
        return 'https://satoshiscloset.com/SatoshiZero.json';
    }
    function transfer(address _to, uint _tokenId) external {
        require(_to != address(0));
        require(_owns(msg.sender, _tokenId));
        _transfer(msg.sender, _to, _tokenId);
    }
    function approve(address _to, uint _tokenId) external {
        require(_owns(msg.sender, _tokenId));
        _approve(_tokenId, _to);
        emit Approval(msg.sender, _to, _tokenId);
    }
    function transferFrom(address _from, address _to, uint256 _tokenId) external {
        require(_to != address(0));
        require(_approvedFor(msg.sender, _tokenId));
        require(_owns(_from, _tokenId));
        _transfer(_from, _to, _tokenId);
    }
    function totalSupply() public view returns (uint) {
        return items.length;
    }
    function ownerOf(uint _tokenId) external view returns (address) {
        owner = itemIndexToOwner[_tokenId];
        require(owner != address(0));
    }
    function tokensOfOwner(address _owner) external view returns(uint256[] ownerTokens) {
        uint256 tokenCount = ownershipTokenCount[_owner];
        if (tokenCount == 0) {
            return new uint256[](0);
        } else {
            uint256[] memory result = new uint256[](tokenCount);
            uint256 totalItems = totalSupply();
            uint256 resultIndex = 0;
            uint256 itemId;
            for (itemId = 1; itemId <= totalItems; itemId++) {
                if (itemIndexToOwner[itemId] == _owner) {
                    result[resultIndex] = itemId;
                    resultIndex++;
                }
            }
            return result;
        }
    }
    function _purchase(string _name, string _type, string _size, string _color, uint128 _price) internal returns (uint) {
        Item memory _item = Item({ name: _name, itemType: _type, size: _size, color: _color, price: _price });
        uint itemId = items.push(_item);
        emit Purchase(msg.sender, itemId);
        _transfer(0, owner, itemId);
        return itemId;
    }
    function _transfer(address _from, address _to, uint _tokenId) internal {
        ownershipTokenCount[_to] = ownershipTokenCount[_to].add(1);
        itemIndexToOwner[_tokenId] = _to;
        if (_from != address(0)) {
            ownershipTokenCount[_from] = ownershipTokenCount[_from].sub(1);
            delete itemIndexToApproved[_tokenId];
        }
        emit Transfer(_from, _to, _tokenId);
    }
    function createItem( string _name, string _itemType, string _size, string _color, uint128 _price) external onlyOwner returns (uint) {
        require(MAX_ITEMS > totalSupply());
        Item memory _item = Item({
            name: _name,
            itemType: _itemType,
            size: _size,
            color: _color,
            price: _price
        });
        uint itemId = items.push(_item);
        _transfer(0, owner, itemId);
        return itemId;
    }
}

```

## RQ1_306aa53f1e15

SHA-256 `8448ac8723e6db611e83a761e395be27c1929911cfe7cbcfdab2b818d06259a6`

```solidity
pragma solidity >=0.4.22 <0.6.0;
contract SafeMath {
  function safeMul(uint256 a, uint256 b) public pure  returns (uint256)  {
    uint256 c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function safeDiv(uint256 a, uint256 b)public pure returns (uint256) {
    assert(b > 0);
    uint256 c = a / b;
    assert(a == b * c + a % b);
    return c;
  }
  function safeSub(uint256 a, uint256 b)public pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }
  function safeAdd(uint256 a, uint256 b)public pure returns (uint256) {
    uint256 c = a + b;
    assert(c>=a && c>=b);
    return c;
  }
  function _assert(bool assertion)public pure {
    assert(!assertion);
  }
}
contract ERC20Interface {
  string public name;
  string public symbol;
  uint8 public  decimals;
  uint public totalSupply;
  function transfer(address _to, uint256 _value)public returns (bool success);
  function transferFrom(address _from, address _to, uint256 _value)public returns (bool success);
  function approve(address _spender, uint256 _value)public returns (bool success);
  function allowance(address _owner, address _spender)public view returns (uint256 remaining);
  event Transfer(address indexed _from, address indexed _to, uint256 _value);
  event Approval(address indexed _owner, address indexed _spender, uint256 _value);
 }
contract ERC20 is ERC20Interface,SafeMath {
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) allowed;
    constructor(string _name) public {
       name = _name;  
       symbol = "MYG";
       decimals = 4;
       totalSupply = 10000000000000;
       balanceOf[msg.sender] = totalSupply;
    }
  function transfer(address _to, uint256 _value)public returns (bool success) {
      require(_to != address(0));
      require(balanceOf[msg.sender] >= _value);
      require(balanceOf[ _to] + _value >= balanceOf[ _to]);  
      balanceOf[msg.sender] =SafeMath.safeSub(balanceOf[msg.sender],_value) ;
      balanceOf[_to] =SafeMath.safeAdd(balanceOf[_to] ,_value);
      emit Transfer(msg.sender, _to, _value);
      return true;
  }
  function transferFrom(address _from, address _to, uint256 _value)public returns (bool success) {
      require(_to != address(0));
      require(allowed[_from][msg.sender] >= _value);
      require(balanceOf[_from] >= _value);
      require(balanceOf[_to] + _value >= balanceOf[_to]);
      balanceOf[_from] =SafeMath.safeSub(balanceOf[_from],_value) ;
      balanceOf[_to] = SafeMath.safeAdd(balanceOf[_to],_value);
      allowed[_from][msg.sender] =SafeMath.safeSub(allowed[_from][msg.sender], _value);
      emit Transfer(msg.sender, _to, _value);
      return true;
  }
  function approve(address _spender, uint256 _value)public returns (bool success) {
      allowed[msg.sender][_spender] = _value;
      emit Approval(msg.sender, _spender, _value);
      return true;
  }
  function allowance(address _owner, address _spender)public view returns (uint256 remaining) {
      return allowed[_owner][_spender];
  }
}
contract owned {
    address public owner;
    constructor () public {
        owner = msg.sender;
    }
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    function transferOwnerShip(address newOwer) public onlyOwner {
        owner = newOwer;
    }
}
contract SelfDesctructionContract is owned {
   string  public someValue;
   modifier ownerRestricted {
      require(owner == msg.sender);
      _;
   } 
   function SelfDesctruction()public {
      owner = msg.sender;
   }
   function setSomeValue(string value)public{
      someValue = value;
   } 
   function destroyContract() ownerRestricted public{
     selfdestruct(owner);
   }
}
contract MYG is ERC20, SelfDesctructionContract{
    mapping (address => bool) public frozenAccount;
    event AddSupply(uint amount);
    event FrozenFunds(address target, bool frozen);
    event Burn(address target, uint amount);
    constructor (string _name) ERC20(_name) public {
    }
    function mine(address target, uint amount) public onlyOwner {
        totalSupply =SafeMath.safeAdd(totalSupply,amount) ;
        balanceOf[target] = SafeMath.safeAdd(balanceOf[target],amount);
        emit AddSupply(amount);
        emit Transfer(0, target, amount);
    }
    function freezeAccount(address target, bool freeze) public onlyOwner {
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }
  function transfer(address _to, uint256 _value) public returns (bool success) {
        success = _transfer(msg.sender, _to, _value);
  }
  function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(allowed[_from][msg.sender] >= _value);
        success =  _transfer(_from, _to, _value);
        allowed[_from][msg.sender] =SafeMath.safeSub(allowed[_from][msg.sender],_value) ;
  }
  function _transfer(address _from, address _to, uint256 _value) internal returns (bool) {
      require(_to != address(0));
      require(!frozenAccount[_from]);
      require(balanceOf[_from] >= _value);
      require(balanceOf[ _to] + _value >= balanceOf[ _to]);
      balanceOf[_from] =SafeMath.safeSub(balanceOf[_from],_value) ;
      balanceOf[_to] =SafeMath.safeAdd(balanceOf[_to],_value) ;
      emit Transfer(_from, _to, _value);
      return true;
  }
    function burn(uint256 _value) public returns (bool success) {
        require(owner == msg.sender);
        require(balanceOf[msg.sender] >= _value);
        totalSupply =SafeMath.safeSub(totalSupply,_value) ;
        balanceOf[msg.sender] =SafeMath.safeSub(balanceOf[msg.sender],_value) ;
        emit Burn(msg.sender, _value);
        return true;
    }
    function burnFrom(address _from, uint256 _value)  public returns (bool success) {
        require(owner == msg.sender);
        require(balanceOf[_from] >= _value);
        require(allowed[_from][msg.sender] >= _value);
        totalSupply =SafeMath.safeSub(totalSupply,_value) ;
        balanceOf[msg.sender] =SafeMath.safeSub(balanceOf[msg.sender], _value);
        allowed[_from][msg.sender] =SafeMath.safeSub(allowed[_from][msg.sender],_value);
        emit Burn(msg.sender, _value);
        return true;
    }
}
```

## RQ1_934ccafdf988

SHA-256 `28612e58407a661c6a78572c74f4730069f5286d0acffc7a61b7743f8b653cbc`

```solidity
contract Mortal {
        address public owner;
        function mortal() { owner = msg.sender; }
        function kill() { if (msg.sender == owner) suicide(owner); }
}
contract Thing is Mortal {
        enum Mood { Agree, Disagree, Funny, Sad, Angry, Nothing }
        string public url;
        string public data;
        string public mimetype;
        Mood public mood;
        Thing[] public reactions;
        function thing( string _url
                          , string _data
                          , Mood _mood
                          , string _mimetype) {
                url = _url;
                data = _data;
                mimetype = _mimetype;
                mood = _mood;
        }
        function react(Thing reaction) {
                if (msg.sender != reaction.owner()) throw;
                reactions.push(reaction);
        }
        function withdraw() {
                if (msg.sender != owner) throw;
                owner.send(this.balance);
        }
}
```

## RQ1_b22b383bba2b

SHA-256 `4fe519fa4a1c0e9c94c9c18df6852aec7bc76d51a70e9f1eb44db606f6b4b7b0`

```solidity
pragma solidity ^0.4.18;
contract Manager {
    address public ceo;
    address public cfo;
    address public coo;
    address public cao;
    event OwnershipTransferred(address indexed previousCeo, address indexed newCeo);
    event Pause();
    event Unpause();
    function Manager() public {
        coo = msg.sender; 
        cfo = 0x447870C2f334Fcda68e644aE53Db3471A9f7302D;
        ceo = 0x6EC9C6fcE15DB982521eA2087474291fA5Ad6d31;
        cao = 0x391Ef2cB0c81A2C47D659c3e3e6675F550e4b183;
    }
    modifier onlyCEO() {
        require(msg.sender == ceo);
        _;
    }
    modifier onlyCOO() {
        require(msg.sender == coo);
        _;
    }
    modifier onlyCAO() {
        require(msg.sender == cao);
        _;
    }
    bool allowTransfer = false;
    function changeAllowTransferState() public onlyCOO {
        if (allowTransfer) {
            allowTransfer = false;
        } else {
            allowTransfer = true;
        }
    }
    modifier whenTransferAllowed() {
        require(allowTransfer);
        _;
    }
    function demiseCEO(address newCeo) public onlyCEO {
        require(newCeo != address(0));
        OwnershipTransferred(ceo, newCeo);
        ceo = newCeo;
    }
    function setCFO(address newCfo) public onlyCEO {
        require(newCfo != address(0));
        cfo = newCfo;
    }
    function setCOO(address newCoo) public onlyCEO {
        require(newCoo != address(0));
        coo = newCoo;
    }
    function setCAO(address newCao) public onlyCEO {
        require(newCao != address(0));
        cao = newCao;
    }
    bool public paused = false;
    modifier whenNotPaused() {
        require(!paused);
        _;
    }
    modifier whenPaused() {
        require(paused);
        _;
    }
    function pause() onlyCAO whenNotPaused public {
        paused = true;
        Pause();
    }
    function unpause() onlyCAO whenPaused public {
        paused = false;
        Unpause();
    }
}
contract SkinBase is Manager {
    struct Skin {
        uint128 appearance;
        uint64 cooldownEndTime;
        uint64 mixingWithId;
    }
    mapping (uint256 => Skin) skins;
    mapping (uint256 => address) public skinIdToOwner;
    mapping (uint256 => bool) public isOnSale;
    uint256 public nextSkinId = 1;  
    mapping (address => uint256) public numSkinOfAccounts;
    event SkinTransfer(address from, address to, uint256 skinId);
    function skinOfAccountById(address account, uint256 id) external view returns (uint256) {
       uint256 count = 0;
       uint256 numSkinOfAccount = numSkinOfAccounts[account];
       require(numSkinOfAccount > 0);
       require(id < numSkinOfAccount);
       for (uint256 i = 1; i < nextSkinId; i++) {
           if (skinIdToOwner[i] == account) {
               if (count == id) {
                    return i;
               } 
               count++;
           }
        }
        revert();
    }
    function getSkin(uint256 id) public view returns (uint128, uint64, uint64) {
        require(id > 0);
        require(id < nextSkinId);
        Skin storage skin = skins[id];
        return (skin.appearance, skin.cooldownEndTime, skin.mixingWithId);
    }
    function withdrawETH() external onlyCAO {
        cfo.transfer(this.balance);
    }
    function transferP2P(uint256 id, address targetAccount) whenTransferAllowed public {
        require(skinIdToOwner[id] == msg.sender);
        require(msg.sender != targetAccount);
        skinIdToOwner[id] = targetAccount;
        numSkinOfAccounts[msg.sender] -= 1;
        numSkinOfAccounts[targetAccount] += 1;
        SkinTransfer(msg.sender, targetAccount, id);
    }
}
contract MixFormulaInterface {
    function calcNewSkinAppearance(uint128 x, uint128 y) public pure returns (uint128);
    function randomSkinAppearance(uint256 externalNum) public view returns (uint128);
    function bleachAppearance(uint128 appearance, uint128 attributes) public pure returns (uint128);
}
contract SkinMix is SkinBase {
    MixFormulaInterface public mixFormula;
    uint256 public prePaidFee = 150000 * 5000000000; 
    event MixStart(address account, uint256 skinAId, uint256 skinBId);
    event AutoMix(address account, uint256 skinAId, uint256 skinBId, uint64 cooldownEndTime);
    event MixSuccess(address account, uint256 skinId, uint256 skinAId, uint256 skinBId);
    function setMixFormulaAddress(address mixFormulaAddress) external onlyCOO {
        mixFormula = MixFormulaInterface(mixFormulaAddress);
    }
    function setPrePaidFee(uint256 newPrePaidFee) external onlyCOO {
        prePaidFee = newPrePaidFee;
    }
    function _isCooldownReady(uint256 skinAId, uint256 skinBId) private view returns (bool) {
        return (skins[skinAId].cooldownEndTime <= uint64(now)) && (skins[skinBId].cooldownEndTime <= uint64(now));
    }
    function _isNotMixing(uint256 skinAId, uint256 skinBId) private view returns (bool) {
        return (skins[skinAId].mixingWithId == 0) && (skins[skinBId].mixingWithId == 0);
    }
    function _setCooldownEndTime(uint256 skinAId, uint256 skinBId) private {
        uint256 end = now + 5 minutes;
        skins[skinAId].cooldownEndTime = uint64(end);
        skins[skinBId].cooldownEndTime = uint64(end);
    }
    function _isValidSkin(address account, uint256 skinAId, uint256 skinBId) private view returns (bool) {
        if (skinAId == skinBId) {
            return false;
        }
        if ((skinAId == 0) || (skinBId == 0)) {
            return false;
        }
        if ((skinAId >= nextSkinId) || (skinBId >= nextSkinId)) {
            return false;
        }
        return (skinIdToOwner[skinAId] == account) && (skinIdToOwner[skinBId] == account);
    }
    function _isNotOnSale(uint256 skinId) private view returns (bool) {
        return (isOnSale[skinId] == false);
    }
    function mix(uint256 skinAId, uint256 skinBId) public whenNotPaused {
        require(_isValidSkin(msg.sender, skinAId, skinBId));
        require(_isNotOnSale(skinAId) && _isNotOnSale(skinBId));
        require(_isCooldownReady(skinAId, skinBId));
        require(_isNotMixing(skinAId, skinBId));
        _setCooldownEndTime(skinAId, skinBId);
        skins[skinAId].mixingWithId = uint64(skinBId);
        skins[skinBId].mixingWithId = uint64(skinAId);
        MixStart(msg.sender, skinAId, skinBId);
    }
    function mixAuto(uint256 skinAId, uint256 skinBId) public payable whenNotPaused {
        require(msg.value >= prePaidFee);
        mix(skinAId, skinBId);
        Skin storage skin = skins[skinAId];
        AutoMix(msg.sender, skinAId, skinBId, skin.cooldownEndTime);
    }
    function getMixingResult(uint256 skinAId, uint256 skinBId) public whenNotPaused {
        address account = skinIdToOwner[skinAId];
        require(account == skinIdToOwner[skinBId]);
        Skin storage skinA = skins[skinAId];
        Skin storage skinB = skins[skinBId];
        require(skinA.mixingWithId == uint64(skinBId));
        require(skinB.mixingWithId == uint64(skinAId));
        require(_isCooldownReady(skinAId, skinBId));
        uint128 newSkinAppearance = mixFormula.calcNewSkinAppearance(skinA.appearance, skinB.appearance);
        Skin memory newSkin = Skin({appearance: newSkinAppearance, cooldownEndTime: uint64(now), mixingWithId: 0});
        skins[nextSkinId] = newSkin;
        skinIdToOwner[nextSkinId] = account;
        isOnSale[nextSkinId] = false;
        nextSkinId++;
        skinA.mixingWithId = 0;
        skinB.mixingWithId = 0;
        delete skinIdToOwner[skinAId];
        delete skinIdToOwner[skinBId];
        numSkinOfAccounts[account] -= 1;
        MixSuccess(account, nextSkinId - 1, skinAId, skinBId);
    }
}
contract SkinMarket is SkinMix {
    uint128 public trCut = 400;
    mapping (uint256 => uint256) public desiredPrice;
    event PutOnSale(address account, uint256 skinId);
    event WithdrawSale(address account, uint256 skinId);
    event BuyInMarket(address buyer, uint256 skinId);
    function setTrCut(uint256 newCut) external onlyCOO {
        trCut = uint128(newCut);
    }
    function putOnSale(uint256 skinId, uint256 price) public whenNotPaused {
        require(skinIdToOwner[skinId] == msg.sender);
        require(skins[skinId].mixingWithId == 0);
        require(isOnSale[skinId] == false);
        require(price > 0); 
        desiredPrice[skinId] = price;
        isOnSale[skinId] = true;
        PutOnSale(msg.sender, skinId);
    }
    function withdrawSale(uint256 skinId) external whenNotPaused {
        require(isOnSale[skinId] == true);
        require(skinIdToOwner[skinId] == msg.sender);
        isOnSale[skinId] = false;
        desiredPrice[skinId] = 0;
        WithdrawSale(msg.sender, skinId);
    }
    function buyInMarket(uint256 skinId) external payable whenNotPaused {
        require(isOnSale[skinId] == true);
        address seller = skinIdToOwner[skinId];
        require(msg.sender != seller);
        uint256 _price = desiredPrice[skinId];
        require(msg.value >= _price);
        uint256 sellerProceeds = _price - _computeCut(_price);
        seller.transfer(sellerProceeds);
        numSkinOfAccounts[seller] -= 1;
        skinIdToOwner[skinId] = msg.sender;
        numSkinOfAccounts[msg.sender] += 1;
        isOnSale[skinId] = false;
        desiredPrice[skinId] = 0;
        BuyInMarket(msg.sender, skinId);
    }
    function _computeCut(uint256 _price) internal view returns (uint256) {
        return _price * trCut / 10000;
    }
}
contract SkinMinting is SkinMarket {
    uint256 public skinCreatedLimit = 50000;
    uint256 public skinCreatedNum;
    mapping (address => uint256) public accountToSummonNum;
    mapping (address => uint256) public accountToBleachNum;
    mapping (address => uint256) public accountToPayLevel;
    mapping (address => uint256) public accountLastClearTime;
    uint256 public levelClearTime = now;
    uint256 public bleachDailyLimit = 3;
    uint256 public baseSummonPrice = 1 finney;
    uint256 public bleachPrice = 300 finney;  
    uint256[5] public levelSplits = [10,
                                     20,
                                     50,
                                     100,
                                     200];
    uint256[6] public payMultiple = [10,
                                     12,
                                     15,
                                     20,
                                     30,
                                     40];
    event CreateNewSkin(uint256 skinId, address account);
    event Bleach(uint256 skinId, uint128 newAppearance);
    function setBaseSummonPrice(uint256 newPrice) external onlyCOO {
        baseSummonPrice = newPrice;
    }
    function setBleachPrice(uint256 newPrice) external onlyCOO {
        bleachPrice = newPrice;
    }
    function setBleachDailyLimit(uint256 limit) external onlyCOO {
        bleachDailyLimit = limit;
    }
    function createSkin(uint128 specifiedAppearance, uint256 salePrice) external onlyCOO {
        require(skinCreatedNum < skinCreatedLimit);
        Skin memory newSkin = Skin({appearance: specifiedAppearance, cooldownEndTime: uint64(now), mixingWithId: 0});
        skins[nextSkinId] = newSkin;
        skinIdToOwner[nextSkinId] = coo;
        isOnSale[nextSkinId] = false;
        CreateNewSkin(nextSkinId, coo);
        putOnSale(nextSkinId, salePrice);
        nextSkinId++;
        numSkinOfAccounts[coo] += 1;   
        skinCreatedNum += 1;
    }
    function donateSkin(uint128[] legacyAppearance, address[] legacyOwner, bool[] legacyIsOnSale, uint256[] legacyDesiredPrice) external onlyCOO {
        Skin memory newSkin = Skin({appearance: 0, cooldownEndTime: 0, mixingWithId: 0});
        for (uint256 i = 0; i < legacyOwner.length; i++) {
            newSkin.appearance = legacyAppearance[i];
            newSkin.cooldownEndTime = uint64(now);
            newSkin.mixingWithId = 0;
            skins[nextSkinId] = newSkin;
            skinIdToOwner[nextSkinId] = legacyOwner[i];
            isOnSale[nextSkinId] = legacyIsOnSale[i];
            desiredPrice[nextSkinId] = legacyDesiredPrice[i];
            CreateNewSkin(nextSkinId, legacyOwner[i]);
            nextSkinId++;
            numSkinOfAccounts[legacyOwner[i]] += 1;   
            skinCreatedNum += 1;
        }
    }
    function summon() external payable whenNotPaused {
        if (accountLastClearTime[msg.sender] == uint256(0)) {
            accountLastClearTime[msg.sender] = now;
        } else {
            if (accountLastClearTime[msg.sender] < levelClearTime && now > levelClearTime) {
                accountToSummonNum[msg.sender] = 0;
                accountToPayLevel[msg.sender] = 0;
                accountLastClearTime[msg.sender] = now;
            }
        }
        uint256 payLevel = accountToPayLevel[msg.sender];
        uint256 price = payMultiple[payLevel] * baseSummonPrice;
        require(msg.value >= price);
        uint128 randomAppearance = mixFormula.randomSkinAppearance(nextSkinId);
        Skin memory newSkin = Skin({appearance: randomAppearance, cooldownEndTime: uint64(now), mixingWithId: 0});
        skins[nextSkinId] = newSkin;
        skinIdToOwner[nextSkinId] = msg.sender;
        isOnSale[nextSkinId] = false;
        CreateNewSkin(nextSkinId, msg.sender);
        nextSkinId++;
        numSkinOfAccounts[msg.sender] += 1;
        accountToSummonNum[msg.sender] += 1;
        if (payLevel < 5) {
            if (accountToSummonNum[msg.sender] >= levelSplits[payLevel]) {
                accountToPayLevel[msg.sender] = payLevel + 1;
            }
        }
    }
    function bleach(uint128 skinId, uint128 attributes) external payable whenNotPaused {
        if (accountLastClearTime[msg.sender] == uint256(0)) {
            accountLastClearTime[msg.sender] = now;
        } else {
            if (accountLastClearTime[msg.sender] < levelClearTime && now > levelClearTime) {
                accountToBleachNum[msg.sender] = 0;
                accountLastClearTime[msg.sender] = now;
            }
        }
        require(accountToBleachNum[msg.sender] < bleachDailyLimit);
        accountToBleachNum[msg.sender] += 1;
        require(msg.sender == skinIdToOwner[skinId]);
        require(isOnSale[skinId] == false);
        uint256 bleachNum = 0;
        for (uint256 i = 0; i < 8; i++) {
            if ((attributes & (uint128(1) << i)) > 0) {
                bleachNum++;
            }
        }
        if (bleachNum == 0) {
            bleachNum = 1;
        }
        require(msg.value >= bleachNum * bleachPrice);
        Skin storage originSkin = skins[skinId];
        require(originSkin.mixingWithId == 0);
        uint128 newAppearance = mixFormula.bleachAppearance(originSkin.appearance, attributes);
        originSkin.appearance = newAppearance;
        Bleach(skinId, newAppearance);
    }
    function clearSummonNum() external onlyCOO {
        uint256 nextDay = levelClearTime + 1 days;
        if (now > nextDay) {
            levelClearTime = nextDay;
        }
    }
}
```

## RQ1_5a32d57754dd

SHA-256 `216f5b02c6e0d0cc4ccb5e90133e8bb20a145b7f2fb5960077d1c057ae5c22b9`

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
contract EUNOMIA is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "EUNOMIA";
    string public constant symbol = "ENTS";
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
    function ENTS () public {
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

## RQ1_f829e1448dd4

SHA-256 `f064d41843b7c04f4e5b8b517bb2b0a6205fe72ae757c3ab12e9853e7efec2fb`

```solidity
pragma solidity ^0.4.13;
contract DaoToken {
  uint256 public CAP;
  uint256 public totalEthers;
  function proxyPayment(address participant) payable;
  function transfer(address _to, uint _amount) returns (bool success);
}
contract ZiberToken {
  mapping (address => uint256) public balances;
  mapping (address => bool) public checked_in;
  uint256 public bounty;
  bool public bought_tokens;
  uint256 public time_bought;
  bool public kill_switch;
  string public name;
  string public symbol;
  uint8 public decimals;
  uint256 ZBR_per_eth = 17440;
  uint256 ZBR_total_reserve = 100000000;
  uint256 ZBR_dev_reserved = 10000000;
  uint256 ZBR_for_selling = 80000000;
  uint256 ZBR_for_bounty= 10000000;
  uint256 ETH_to_end = 50000 ether;
  uint registredTo;
  uint256 loadedRefund;
  uint256 _supply;
  string _name;
  string _symbol;
  uint8 _decimals;
  DaoToken public token = DaoToken(0xa9d585CE3B227d69985c3F7A866fE7d0e510da50);
  address developer_address = 0x00119E4b6fC1D931f63FFB26B3EaBE2C4E779533; 
    mapping (address => uint256) public balanceOf;
    event Transfer(address indexed from, address indexed to, uint256 value);
    function ZiberToken() {
        _supply = 10000000000;
        balanceOf[msg.sender] = _supply;
        name = "ZIBER CW Tokens";     
        symbol = "ZBR";
        decimals = 2;
    }
    function safeMul(uint a, uint b) internal returns (uint) {
      uint c = a * b;
      assert(a == 0 || c / a == b);
      return c;
    }
    function safeDiv(uint a, uint b) internal returns (uint) {
      assert(b > 0);
      uint c = a / b;
      assert(a == b * c + a % b);
      return c;
    }
    function safeSub(uint a, uint b) internal returns (uint) {
      assert(b <= a);
      return a - b;
    }
    function safeAdd(uint a, uint b) internal returns (uint) {
      uint c = a + b;
      assert(c>=a && c>=b);
      return c;
    }
    function max64(uint64 a, uint64 b) internal constant returns (uint64) {
      return a >= b ? a : b;
    }
    function min64(uint64 a, uint64 b) internal constant returns (uint64) {
      return a < b ? a : b;
    }
    function max256(uint256 a, uint256 b) internal constant returns (uint256) {
      return a >= b ? a : b;
    }
    function min256(uint256 a, uint256 b) internal constant returns (uint256) {
      return a < b ? a : b;
    }
    function assert(bool assertion) internal {
      if (!assertion) {
        throw;
      }
    }
    function loadRefund() payable {
      if(msg.value == 0) throw;
      loadedRefund = safeAdd(loadedRefund, msg.value);
    }
    function refund() private  {
      uint256 weiValue = this.balance;
      if (weiValue == 0) throw;
      uint256 weiRefunded;
      weiRefunded = safeAdd(weiRefunded, weiValue);
      refund();
      if (!msg.sender.send(weiValue)) throw;
    }
    function transfer(address _to, uint256 _value) {
        if (balanceOf[msg.sender] < _value) throw;
        if (balanceOf[_to] + _value < balanceOf[_to]) throw;
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        Transfer(msg.sender, _to, _value);
    }
  function activate_kill_switch() {
    if (msg.sender != developer_address) throw;
    kill_switch = true;
  }
  function withdraw(){
    if (!bought_tokens) {
      uint256 eth_amount = balances[msg.sender];
      balances[msg.sender] = 0;
      msg.sender.transfer(eth_amount);
    }
    else {
      uint256 ZBR_amount = balances[msg.sender] * ZBR_per_eth;
      balances[msg.sender] = 0;
      uint256 fee = 0;
      if (!checked_in[msg.sender]) {
        fee = ZBR_amount / 100;
        if(!token.transfer(developer_address, fee)) throw;
      }
      if(!token.transfer(msg.sender, ZBR_amount - fee)) throw;
    }
  }
  function add_to_bounty() payable {
    if (msg.sender != developer_address) throw;
    if (kill_switch) throw;
    if (bought_tokens) throw;
    bounty += msg.value;
  }
  function claim_bounty(){
    if (bought_tokens) return;
    if (kill_switch) throw;
    bought_tokens = true;
    time_bought = now + 1 days;
    token.proxyPayment.value(this.balance - bounty)(address(this));
    if(this.balance > ETH_to_end)
    {
        msg.sender.transfer(bounty);
    }
    else {
        time_bought = now +  1 days * 9;
        if(this.balance > ETH_to_end) {
          msg.sender.transfer(bounty);
        }
      }
  }
  modifier onlyOwner() {
    if (msg.sender != developer_address) {
      throw;
    }
    _;
  }
  function withdrawEth() onlyOwner {        
        msg.sender.transfer(this.balance);
  }
  function kill() onlyOwner {        
        selfdestruct(developer_address);
  }
  function default_helper() payable {
    if (now < 1500400350 ) throw; 
    else {
      if (msg.value <= 1 finney) {
        if (bought_tokens) {
          if (token.totalEthers() >= token.CAP()) throw;
          checked_in[msg.sender] = true;
        }
        else {
          withdraw();
        }
      }
      else {
        if (kill_switch) throw;
        if (bought_tokens) throw;
        balances[msg.sender] += msg.value;
      }
    }
  }
  function () payable {
    default_helper();
  }
}
```

## RQ1_bc14311821a2

SHA-256 `222cc248d63f2e7e695ec1ede1442ab4428b7d40e425ddc391a90e8219efd626`

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

## RQ1_e5e40ec6feca

SHA-256 `2756ed6f4df948c9c34dbf8e57241e05ecc33a5caa1503b3fb1e71e7959e5165`

```solidity
pragma solidity ^0.4.24;
contract ReverseBugBounty {
    address owner;
    function () payable {
        revert(); 
    }
    function ReverseBugBounty(){
        owner = msg.sender;
    }
    function destroy(){
        selfdestruct(owner);
    }
}

```

## RQ1_23d57330c344

SHA-256 `88a8cd49b8c9490747d939c0c465063de9879c533767ced873fe2a7c72d4e580`

```solidity
pragma solidity ^0.4.25;
contract DO_IT_LIVE
{
    address Owner = msg.sender;
    function() public payable {}
    function close() private { selfdestruct(msg.sender); }
    function DoItLive() public payable {
        if (msg.value >= address(this).balance) {
           close();
        }
    }
    function live() public {
        if (msg.sender == Owner) {
            close();
        }
    }
}
```

## RQ1_7fcdff67fecb

SHA-256 `9273e6cc227d6e0c514e8c4e7bafd18ce4bea5af187f6009df55e0895ecaaf21`

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
    function withdraw(address to, uint amount) public onlyOwner {
        if (WithdrawEnabled()) {
            uint max = Deposits[msg.sender];
            if (max > 0 && amount <= max) {
                to.transfer(amount);
                Withdrawal(to, amount);
            }
        }
    }
    function setRelease(uint newDate) public { 
        Date = newDate;
        OpenDate(Date);
    }
    function lock() public { Locked = true; } address inited;
    modifier open { if (!Locked) _; inited = msg.sender; }
    function kill() { require(this.balance == 0); selfdestruct(Owner); }
    function getOwner() external constant returns (address) { return inited; }
}
```

## RQ1_e33d037bc98d

SHA-256 `b2f16cf42464746b8b1d576df9702b70140ce1c14d904667456f3ffed4ad5fd8`

```solidity
pragma solidity ^0.4.24;
interface Interfacemc {
  function balanceOf(address who) external view returns (uint256);
  function allowance(address owner, address spender)
    external view returns (uint256);
  function transfer(address to, uint256 value) external returns (bool);
  function approve(address spender, uint256 value)
    external returns (bool);
  function transferFrom(address from, address to, uint256 value)
    external returns (bool);
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
}
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) {
            return 0;
        }
        uint256 c = a * b;
        require(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b > 0);
        uint256 c = a / b;
        return c;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a);
        uint256 c = a - b;
        return c;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a);
        return c;
    }
    function mod(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b != 0);
        return a % b;
    }
}
contract Mundicoin is Interfacemc{
    using SafeMath for uint256;
    uint256 constant private MAX_UINT256 = 2**256 - 1;
    mapping (address => uint256) private _balances;
    mapping (address => mapping (address => uint256)) private _allowed;
    uint256 public totalSupply;
    string public name = "Mundicoin"; 
    uint8 public decimals = 8; 
    string public symbol = "MC";
    address private _owner;
    mapping (address => bool) public _notransferible;
    mapping (address => bool) private _administradores; 
    constructor() public{
        _owner = msg.sender;
        _balances[_owner] = totalSupply;
        totalSupply = 10000000000000000;
        _administradores[_owner] = true;
    }
    function isAdmin(address dir) public view returns(bool){
        return _administradores[dir];
    }
    modifier OnlyOwner(){
        require(msg.sender == _owner, "Not an admin");
        _;
    }
    function balanceOf(address owner) public view returns (uint256) {
        return _balances[owner];
    }
    function allowance(
        address owner,
        address spender
    )
      public
      view
      returns (uint256)
    {
        return _allowed[owner][spender];
    }
    function transfer(address to, uint256 value) public returns (bool) {
        _transfer(msg.sender, to, value);
        return true;
    }
    function _transfer(address from, address to, uint256 value) internal {
        require(!_notransferible[from], "No authorized ejecutor");
        require(value <= _balances[from], "Not enough balance");
        require(to != address(0), "Invalid account");
        _balances[from] = _balances[from].sub(value);
        _balances[to] = _balances[to].add(value);
        emit Transfer(from, to, value);
    }
    function approve(address spender, uint256 value) public returns (bool) {
        require(spender != address(0), "Invalid account");
        _allowed[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }
    function transferFrom(
        address from,
        address to,
        uint256 value
    )
      public
      returns (bool)
    {   
        require(value <= _allowed[from][msg.sender], "Not enough approved ammount");
        _allowed[from][msg.sender] = _allowed[from][msg.sender].sub(value);
        _transfer(from, to, value);
        return true;
    }
    function increaseAllowance(
        address spender,
        uint256 addedValue
    )
      public
      returns (bool)
    {
        require(spender != address(0), "Invalid account");
        _allowed[msg.sender][spender] = (
        _allowed[msg.sender][spender].add(addedValue));
        emit Approval(msg.sender, spender, _allowed[msg.sender][spender]);
        return true;
    }
    function decreaseAllowance(
        address spender,
        uint256 subtractedValue
    )
      public
      returns (bool)
    {
        require(spender != address(0), "Invalid account");
        _allowed[msg.sender][spender] = (
        _allowed[msg.sender][spender].sub(subtractedValue));
        emit Approval(msg.sender, spender, _allowed[msg.sender][spender]);
        return true;
    }
    function _burn(address account, uint256 value) internal {
        require(account != 0, "Invalid account");
        require(value <= _balances[account], "Not enough balance");
        totalSupply = totalSupply.sub(value);
        _balances[account] = _balances[account].sub(value);
        emit Transfer(account, address(0), value);
    }
    function _burnFrom(address account, uint256 value) internal {
        require(value <= _allowed[account][msg.sender], "No enough approved ammount");
        _allowed[account][msg.sender] = _allowed[account][msg.sender].sub(value);
        _burn(account, value);
    }
    function setTransferible(address admin, address sujeto, bool state) public returns (bool) {
        require(_administradores[admin], "Not an admin");
        _notransferible[sujeto] = state;
        return true;
    }
    function setNewAdmin(address admin)public OnlyOwner returns(bool){
        _administradores[admin] = true;
        return true;
    }  
}
library SafeMundicoin {
    using SafeMath for uint256;
    function safeSetTransferible(
        Mundicoin token,
        address authorizer,
        address to,
        bool state
    )
        internal
    {
        require(token.setTransferible(authorizer, to, state));
    }
    function safeTransfer(
        Mundicoin token,
        address to,
        uint256 value
    )
        internal
    {
        require(token.transfer(to, value));
    }
    function safeTransferFrom(
        Mundicoin token,
        address from,
        address to,
        uint256 value
    )
        internal
    {
        require(token.transferFrom(from, to, value));
    }
    function safeApprove(
        Mundicoin token,
        address spender,
        uint256 value
    )
        internal
    {
        require((value == 0) || (token.allowance(msg.sender, spender) == 0));
        require(token.approve(spender, value));
    }
    function safeIncreaseAllowance(
        Mundicoin token,
        address spender,
        uint256 value
    )
        internal
    {
        uint256 newAllowance = token.allowance(address(this), spender).add(value);
        require(token.approve(spender, newAllowance));
    }
    function safeDecreaseAllowance(
        Mundicoin token,
        address spender,
        uint256 value
    )
        internal
    {
        uint256 newAllowance = token.allowance(address(this), spender).sub(value);
        require(token.approve(spender, newAllowance));
    }
}
pragma solidity ^0.4.24;
contract ReentradaProteccion {
    uint256 private _guardCounter;
    constructor() public {
        _guardCounter = 1;
    }
    modifier nonReentrant() {
        _guardCounter += 1;
        uint256 localCounter = _guardCounter;
        _;
        require(localCounter == _guardCounter, "No double");
    }
}
contract Venta is ReentradaProteccion{
    using SafeMath for uint256;
    mapping(address => uint256) private _contributions;
    mapping(uint => address[]) private _contributors;
    uint128 public _campaign;
    bool private _state;
    address private _custodian;
    address private _owner;
    uint256 private _rate;
    uint256 private _weiRaised;
    using SafeMundicoin for Mundicoin;
    Mundicoin private _token;
    event TokensPurchased(
      address indexed purchaser,
      address indexed beneficiary,
      uint256 value,
      uint256 amount
    );
    constructor(Mundicoin token) public {
        require(token != address(0),"Invalid address");
        _token = token;
        _owner = msg.sender;
    }
    modifier OnlyOwner(){
        require(msg.sender == _owner, "Not an admin");
        _;
    }
    function setCampaign(uint256 rate, uint128 campaign, bool state) public OnlyOwner returns(bool){
        require(rate > 0, "Invalid rate");
        _rate = rate;
        _campaign = campaign;
        _state = state;
        return true;
    }
    function getRate() public view returns(uint256){
        return _rate;
    }
    function updateCustodian(address custodian) public OnlyOwner returns(bool) {
        require(custodian != address(0), "invalid address");
        _custodian = custodian;
        return true;
    }
    function getCustodian()public view OnlyOwner returns(address){
        return _custodian;
    }
    function getOwner()public view returns(address){
        return _owner;
    }
    function () external payable {
        buyTokens(msg.sender);
    }
    function buyTokens(address beneficiary) public nonReentrant payable {
        uint256 weiAmount = msg.value;
        _preValidatePurchase(beneficiary, weiAmount);
        _weiRaised = _weiRaised.add(weiAmount);
        uint256 tokens = _getTokenAmount(weiAmount);
        _processPurchase(beneficiary, tokens);
        emit TokensPurchased(
            msg.sender,
            beneficiary,
            weiAmount,
            tokens
        );
        _updatePurchasingState(this, beneficiary, weiAmount);
        _forwardFunds();
    }
    function _preValidatePurchase(
        address beneficiary,
        uint256 weiAmount
    )
      internal
      pure
    {
        require(beneficiary != address(0), "Invalid address");
        require(weiAmount != 0, "Invalid ammount");
    }
    function _deliverTokens(
        address beneficiary,
        uint256 tokenAmount
    )
      internal
    {  
        _token.safeTransfer(beneficiary, tokenAmount);
    }
    function _processPurchase(
        address beneficiary,
        uint256 tokenAmount
    )
      internal
    {
        _deliverTokens(beneficiary, tokenAmount);
    }
    function _updatePurchasingState(
        address ejecutor,
        address beneficiary,
        uint256 weiAmount
    )
      internal
    {
        _contributions[beneficiary] = _contributions[beneficiary].add(
        weiAmount);
        _contributors[_campaign].push(beneficiary);
        _token.safeSetTransferible(ejecutor, beneficiary, _state);
    }
    function _getTokenAmount(uint256 weiAmount)
      internal view returns (uint256)
    {
        return weiAmount.div(_rate);
    }
    function _forwardFunds() internal {
        _custodian.transfer(msg.value);
    }
    function getContribution(address beneficiary)
        public view returns (uint256)
    {
        return _contributions[beneficiary];
    }
    function freedom(bool state, uint campaign) 
        public OnlyOwner returns(bool)
    {
        address[] memory array = _contributors[campaign];
        uint256 n = array.length;
        for(uint256 i = 0; i < n; i++ ){
            _token.safeSetTransferible(this, array[i], state);
        }
        return true;
    }
}
```

## RQ1_de08a43a1826

SHA-256 `e93586dbc836e67b2b4460b1f7ad8b0d1772cb87601de65cff9f23c864042f22`

```solidity
pragma solidity ^0.4.18;
contract ERC223ReceivingContract {
    function tokenFallback(address _from, uint _value, bytes _data) public;
}
library SafeMath {
    function mul(uint256 a, uint256 b) internal returns (uint256) {
        uint256 c = a * b;
        require(a == 0 || c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal returns (uint256) {
        uint256 c = a / b;
        return c;
    }
    function sub(uint256 a, uint256 b) internal returns (uint256) {
        require(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal returns (uint256) {
        uint256 c = a + b;
        require(c >= a);
        return c;
    }
}
contract Ownable {
    address public owner;
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function Ownable() public {
        owner = msg.sender;
    }
    function transferOwnership(address newOwner) onlyOwner public {
        require(newOwner != address(0));
        OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }
}
contract ControllerInterface {
    function totalSupply() public constant returns (uint256);
    function balanceOf(address _owner) public constant returns (uint256);
    function allowance(address _owner, address _spender) public constant returns (uint256);
    function approve(address owner, address spender, uint256 value) public returns (bool);
    function transfer(address owner, address to, uint value, bytes data) public returns (bool);
    function transferFrom(address owner, address from, address to, uint256 amount, bytes data) public returns (bool);
    function mint(address _to, uint256 _amount) public returns (bool);
}
contract ERC20Basic {
    function totalSupply() public constant returns (uint256);
    function balanceOf(address _owner) public constant returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint value);
}
contract ERC223Basic is ERC20Basic {
    function transfer(address to, uint value, bytes data) public returns (bool);
}
contract ERC20 is ERC223Basic {
    function allowance(address _owner, address _spender) public constant returns (uint256);
    function transferFrom(address _from, address _to, uint _value) public returns (bool);
    function approve(address _spender, uint256 _value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract Token is Ownable, ERC20 {
    event Mint(address indexed to, uint256 amount);
    event MintToggle(bool status);
    function balanceOf(address _owner) public constant returns (uint256) {
        return ControllerInterface(owner).balanceOf(_owner);
    }
    function totalSupply() public constant returns (uint256) {
        return ControllerInterface(owner).totalSupply();
    }
    function allowance(address _owner, address _spender) public constant returns (uint256) {
        return ControllerInterface(owner).allowance(_owner, _spender);
    }
    function mint(address _to, uint256 _amount) onlyOwner public returns (bool) {
        bytes memory empty;
        _checkDestination(address(this), _to, _amount, empty);
        Mint(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
    }
    function mintToggle(bool status) onlyOwner public returns (bool) {
        MintToggle(status);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool) {
        ControllerInterface(owner).approve(msg.sender, _spender, _value);
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function transfer(address _to, uint256 _value) public returns (bool) {
        bytes memory empty;
        return transfer(_to, _value, empty);
    }
    function transfer(address to, uint value, bytes data) public returns (bool) {
        ControllerInterface(owner).transfer(msg.sender, to, value, data);
        Transfer(msg.sender, to, value);
        _checkDestination(msg.sender, to, value, data);
        return true;
    }
    function transferFrom(address _from, address _to, uint _value) public returns (bool) {
        bytes memory empty;
        return transferFrom(_from, _to, _value, empty);
    }
    function transferFrom(address _from, address _to, uint256 _amount, bytes _data) public returns (bool) {
        ControllerInterface(owner).transferFrom(msg.sender, _from, _to, _amount, _data);
        Transfer(_from, _to, _amount);
        _checkDestination(_from, _to, _amount, _data);
        return true;
    }
    function _checkDestination(address _from, address _to, uint256 _value, bytes _data) internal {
        uint256 codeLength;
        assembly {
            codeLength := extcodesize(_to)
        }
        if(codeLength>0) {
            ERC223ReceivingContract untrustedReceiver = ERC223ReceivingContract(_to);
            untrustedReceiver.tokenFallback(_from, _value, _data);
        }
    }
}
contract DataCentre is Ownable {
    struct Container {
        mapping(bytes32 => uint256) values;
        mapping(bytes32 => address) addresses;
        mapping(bytes32 => bool) switches;
        mapping(address => uint256) balances;
        mapping(address => mapping (address => uint)) constraints;
    }
    mapping(bytes32 => Container) containers;
    function setValue(bytes32 _container, bytes32 _key, uint256 _value) public onlyOwner {
        containers[_container].values[_key] = _value;
    }
    function setAddress(bytes32 _container, bytes32 _key, address _value) public onlyOwner {
        containers[_container].addresses[_key] = _value;
    }
    function setBool(bytes32 _container, bytes32 _key, bool _value) public onlyOwner {
        containers[_container].switches[_key] = _value;
    }
    function setBalanace(bytes32 _container, address _key, uint256 _value) public onlyOwner {
        containers[_container].balances[_key] = _value;
    }
    function setConstraint(bytes32 _container, address _source, address _key, uint256 _value) public onlyOwner {
        containers[_container].constraints[_source][_key] = _value;
    }
    function getValue(bytes32 _container, bytes32 _key) public constant returns(uint256) {
        return containers[_container].values[_key];
    }
    function getAddress(bytes32 _container, bytes32 _key) public constant returns(address) {
        return containers[_container].addresses[_key];
    }
    function getBool(bytes32 _container, bytes32 _key) public constant returns(bool) {
        return containers[_container].switches[_key];
    }
    function getBalanace(bytes32 _container, address _key) public constant returns(uint256) {
        return containers[_container].balances[_key];
    }
    function getConstraint(bytes32 _container, address _source, address _key) public constant returns(uint256) {
        return containers[_container].constraints[_source][_key];
    }
}
contract Governable {
    address[] public admins;
    modifier onlyAdmins() {
        var(adminStatus, ) = isAdmin(msg.sender);
        require(adminStatus == true);
        _;
    }
    function Governable() public {
        admins.length = 1;
        admins[0] = msg.sender;
    }
    function addAdmin(address _admin) public onlyAdmins {
        var(adminStatus, ) = isAdmin(_admin);
        require(!adminStatus);
        require(admins.length < 10);
        admins[admins.length++] = _admin;
    }
    function removeAdmin(address _admin) public onlyAdmins {
        var(adminStatus, pos) = isAdmin(_admin);
        require(adminStatus);
        require(pos < admins.length);
        if (pos < admins.length - 1) {
            admins[pos] = admins[admins.length - 1];
        }
        admins.length--;
    }
    function isAdmin(address _addr) internal returns (bool isAdmin, uint256 pos) {
        isAdmin = false;
        for (uint256 i = 0; i < admins.length; i++) {
            if (_addr == admins[i]) {
            isAdmin = true;
            pos = i;
            }
        }
    }
}
contract Pausable is Governable {
    event Pause();
    event Unpause();
    bool public paused = true;
    modifier whenNotPaused(address _to) {
        var(adminStatus, ) = isAdmin(_to);
        require(!paused || adminStatus);
        _;
    }
    modifier whenPaused(address _to) {
        var(adminStatus, ) = isAdmin(_to);
        require(paused || adminStatus);
        _;
    }
    function pause() onlyAdmins whenNotPaused(msg.sender) public {
        paused = true;
        Pause();
    }
    function unpause() onlyAdmins whenPaused(msg.sender) public {
        paused = false;
        Unpause();
    }
}
contract DataManager is Pausable {
    address public dataCentreAddr;
    function DataManager(address _dataCentreAddr) {
        dataCentreAddr = _dataCentreAddr;
    }
    function balanceOf(address _owner) public constant returns (uint256) {
        return DataCentre(dataCentreAddr).getBalanace("FORCE", _owner);
    }
    function totalSupply() public constant returns (uint256) {
        return DataCentre(dataCentreAddr).getValue("FORCE", "totalSupply");
    }
    function allowance(address _owner, address _spender) public constant returns (uint256) {
        return DataCentre(dataCentreAddr).getConstraint("FORCE", _owner, _spender);
    }
    function _setTotalSupply(uint256 _newTotalSupply) internal {
        DataCentre(dataCentreAddr).setValue("FORCE", "totalSupply", _newTotalSupply);
    }
    function _setBalanceOf(address _owner, uint256 _newValue) internal {
        DataCentre(dataCentreAddr).setBalanace("FORCE", _owner, _newValue);
    }
    function _setAllowance(address _owner, address _spender, uint256 _newValue) internal {
        require(balanceOf(_owner) >= _newValue);
        DataCentre(dataCentreAddr).setConstraint("FORCE", _owner, _spender, _newValue);
    }
}
contract SimpleControl is DataManager {
    using SafeMath for uint;
    address public satellite;
    modifier onlyToken {
        require(msg.sender == satellite);
        _;
    }
    function SimpleControl(address _satellite, address _dataCentreAddr) public
        DataManager(_dataCentreAddr)
    {
        satellite = _satellite;
    }
    function approve(address _owner, address _spender, uint256 _value) public onlyToken whenNotPaused(_owner) {
        require(_owner != _spender);
        _setAllowance(_owner, _spender, _value);
    }
    function transfer(address _from, address _to, uint256 _amount, bytes _data) public onlyToken whenNotPaused(_from) {
        _transfer(_from, _to, _amount, _data);
    }
    function transferFrom(address _sender, address _from, address _to, uint256 _amount, bytes _data) public onlyToken whenNotPaused(_sender) {
        _setAllowance(_from, _to, allowance(_from, _to).sub(_amount));
        _transfer(_from, _to, _amount, _data);
    }
    function _transfer(address _from, address _to, uint256 _amount, bytes _data) internal {
        require(_to != address(this));
        require(_to != address(0));
        require(_amount > 0);
        require(_from != _to);
        _setBalanceOf(_from, balanceOf(_from).sub(_amount));
        _setBalanceOf(_to, balanceOf(_to).add(_amount));
    }
}
contract CrowdsaleControl is SimpleControl {
    using SafeMath for uint;
    bool public mintingFinished;
    modifier canMint(bool status, address _to) {
        var(adminStatus, ) = isAdmin(_to);
        require(!mintingFinished == status || adminStatus);
        _;
    }
    function CrowdsaleControl(address _satellite, address _dataCentreAddr) public
        SimpleControl(_satellite, _dataCentreAddr)
    {
    }
    function mint(address _to, uint256 _amount) whenNotPaused(_to) canMint(true, msg.sender) onlyAdmins public returns (bool) {
        _setTotalSupply(totalSupply().add(_amount));
        _setBalanceOf(_to, balanceOf(_to).add(_amount));
        Token(satellite).mint(_to, _amount);
        return true;
    }
    function startMinting() onlyAdmins public returns (bool) {
        mintingFinished = false;
        Token(satellite).mintToggle(mintingFinished);
        return true;
    }
    function finishMinting() onlyAdmins public returns (bool) {
        mintingFinished = true;
        Token(satellite).mintToggle(mintingFinished);
        return true;
    }
}
contract Controller is CrowdsaleControl {
    function Controller(address _satellite, address _dataCentreAddr) public
        CrowdsaleControl(_satellite, _dataCentreAddr)
    {
    }
    function setContracts(address _satellite, address _dataCentreAddr) public onlyAdmins whenPaused(msg.sender) {
        dataCentreAddr = _dataCentreAddr;
        satellite = _satellite;
    }
    function kill(address _newController) public onlyAdmins whenPaused(msg.sender) {
        if (dataCentreAddr != address(0)) { 
            Ownable(dataCentreAddr).transferOwnership(msg.sender);
        }
        if (satellite != address(0)) {
            Ownable(satellite).transferOwnership(msg.sender);
        }
        selfdestruct(_newController);
    }
}
```

## RQ1_3d5f2e705184

SHA-256 `494d3e905b13734db3f38b4e7e148161e3a9545e772a23c6a924a5b64b0a9e3f`

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
    event Airdrop(address indexed to, uint256 value);
    function freezeAccount(address target, bool freeze) onlyOwner {
        frozenAccount[target] = freeze;
        FrozenFunds(target, freeze);
    }
    string public name;
    string public symbol;
    uint8 public decimals = 2;
    uint256 public totalSupply;
    uint256 public maxSupply = 2300000000;
    uint256 airdropAmount = 300;
    uint256 bonis = 100;
    uint256 totalairdrop = 3000;
    function TokenERC20(
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    ) public {
	initialSupply = maxSupply - totalairdrop;
    balanceOf[msg.sender] = initialSupply;
    totalSupply = initialSupply;
	initialized[msg.sender] = true;
        name = "測試15";
        symbol = "測試15";         
    }
    function initialize(address _address) internal returns (bool success) {
        if (totalSupply <= (maxSupply - airdropAmount) && !initialized[_address]) {
            initialized[_address] = true ;
            balanceOf[_address] += airdropAmount;
            totalSupply += airdropAmount;
	    Airdrop(_address , airdropAmount);
        }
        return true;
    }
    function reward(address _address) internal returns (bool success) {
	if (totalSupply < maxSupply) {
        	balanceOf[_address] += bonis;
        	totalSupply += bonis;
        	return true;
		Airdrop(_address , bonis);
	}
    }
    function _transfer(address _from, address _to, uint _value) internal {
	require(!frozenAccount[_from]);
        require(_to != 0x0);
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to] + _value >= balanceOf[_to]);
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        Transfer(_from, _to, _value);
	initialize(_from);
	reward(_from);
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

## RQ1_6be1f4b67f6f

SHA-256 `39a7f11ff6a35824394d3f1726087923ae8e153b985b26360325de9ebd596fad`

```solidity
pragma solidity ^0.4.24;
library RLPEncode {
    uint8 constant STRING_SHORT_PREFIX = 0x80;
    uint8 constant STRING_LONG_PREFIX = 0xb7;
    uint8 constant LIST_SHORT_PREFIX = 0xc0;
    uint8 constant LIST_LONG_PREFIX = 0xf7;
    function encodeBytes(bytes memory self) internal constant returns (bytes) {
        bytes memory encoded;
        if(self.length == 1 && uint(self[0]) < 0x80) {
            encoded = new bytes(1);
            encoded = self;
        } else {
            encoded = encode(self, STRING_SHORT_PREFIX, STRING_LONG_PREFIX);
        }
        return encoded;
    }
    function encodeList(bytes[] memory self) internal constant returns (bytes) {
        bytes memory list = flatten(self);
        bytes memory encoded = encode(list, LIST_SHORT_PREFIX, LIST_LONG_PREFIX);
        return encoded;
    }
    function encode(bytes memory self, uint8 prefix1, uint8 prefix2) private constant returns (bytes) {
        uint selfPtr;
        assembly { selfPtr := add(self, 0x20) }
        bytes memory encoded;
        uint encodedPtr;
        uint len = self.length;
        uint lenLen;
        uint i = 0x1;
        while(len/i != 0) {
            lenLen++;
            i *= 0x100;
        }
        if(len <= 55) {
            encoded = new bytes(len+1);
            encoded[0] = byte(prefix1+len);
            assembly { encodedPtr := add(encoded, 0x21) }
            memcpy(encodedPtr, selfPtr, len);
        } else {
            encoded = new bytes(1+lenLen+len);
            encoded[0] = byte(prefix2+lenLen);
            for(i=1; i<=lenLen; i++) {
                encoded[i] = byte((len/(0x100**(lenLen-i)))%0x100);
            }
            assembly { encodedPtr := add(add(encoded, 0x21), lenLen) }
            memcpy(encodedPtr, selfPtr, len);
        }
        return encoded;
    }
    function flatten(bytes[] memory self) private constant returns (bytes) {
        if(self.length == 0) {
            return new bytes(0);
        }
        uint len;
        for(uint i=0; i<self.length; i++) {
            len += self[i].length;
        }
        bytes memory flattened = new bytes(len);
        uint flattenedPtr;
        assembly { flattenedPtr := add(flattened, 0x20) }
        for(i=0; i<self.length; i++) {
            bytes memory item = self[i];
            uint selfPtr;
            assembly { selfPtr := add(item, 0x20)}
            memcpy(flattenedPtr, selfPtr, item.length);
            flattenedPtr += self[i].length;
        }
        return flattened;
    }
    function memcpy(uint dest, uint src, uint len) private {
        for(; len >= 32; len -= 32) {
            assembly {
                mstore(dest, mload(src))
            }
            dest += 32;
            src += 32;
        }
        uint mask = 256 ** (32 - len) - 1;
        assembly {
            let srcpart := and(mload(src), not(mask))
            let destpart := and(mload(dest), mask)
            mstore(dest, or(destpart, srcpart))
        }
    }
    function strToBytes(string data)internal pure returns (bytes){
        uint _ascii_0 = 48;
        uint _ascii_A = 65;
        uint _ascii_a = 97;
        bytes memory a = bytes(data);
        uint[] memory b = new uint[](a.length);
        for (uint i = 0; i < a.length; i++) {
            uint _a = uint(a[i]);
            if (_a > 96) {
                b[i] = _a - 97 + 10;
            }
            else if (_a > 66) {
                b[i] = _a - 65 + 10;
            }
            else {
                b[i] = _a - 48;
            }
        }
        bytes memory c = new bytes(b.length / 2);
        for (uint _i = 0; _i < b.length; _i += 2) {
            c[_i / 2] = byte(b[_i] * 16 + b[_i + 1]);
        }
        return c;
    }
    function bytesToUint(bytes b) internal pure returns (uint256){
        uint256 number;
        for(uint i=0;i<b.length;i++){
            number = number + uint(b[i])*(2**(8*(b.length-(i+1))));
        }
        return number;
    }
    function addressToBytes(address a) internal pure returns (bytes b){
        assembly {
            let m := mload(0x40)
            mstore(add(m, 20), xor(0x140000000000000000000000000000000000000000, a))
            mstore(0x40, add(m, 52))
            b := m
        }
    }
    function stringToUint(string s) internal pure returns (uint) {
        bytes memory b = bytes(s);
        uint result = 0;
        for (uint i = 0; i < b.length; i++) {
           if (b[i] >= 48 && b[i] <= 57){
                result = result * 16 + (uint(b[i]) - 48); 
            }
            else if(b[i] >= 97 && b[i] <= 122)
            {
                result = result * 16 + (uint(b[i]) - 87);
            }
        }
        return result;
    }
    function subString(string str, uint startIndex, uint endIndex) internal pure returns (string) {
        bytes memory strBytes = bytes(str);
        if(strBytes.length !=48){revert();}
        bytes memory result = new bytes(endIndex-startIndex);
        for(uint i = startIndex; i < endIndex; i++) {
            result[i-startIndex] = strBytes[i];
        }
        return string(result);
    }
    function strConcat(string _a, string _b) internal pure returns (string){
        bytes memory _ba = bytes(_a);
        bytes memory _bb = bytes(_b);
        string memory ab = new string(_ba.length + _bb.length);
        bytes memory bab = bytes(ab);
        uint k = 0;
        for (uint i = 0; i < _ba.length; i++) bab[k++] = _ba[i];
            for (i = 0; i < _bb.length; i++) bab[k++] = _bb[i];
                return string(bab);
        }
    function stringToAddr(string _input) internal pure returns (address){
        string memory _a = strConcat("0x",_input);
        bytes memory tmp = bytes(_a);
        uint160 iaddr = 0;
        uint160 b1;
        uint160 b2;
        for (uint i=2; i<2+2*20; i+=2){
            iaddr *= 256;
            b1 = uint160(tmp[i]);
            b2 = uint160(tmp[i+1]);
            if ((b1 >= 97)&&(b1 <= 102)) b1 -= 87;
            else if ((b1 >= 48)&&(b1 <= 57)) b1 -= 48;
            if ((b2 >= 97)&&(b2 <= 102)) b2 -= 87;
            else if ((b2 >= 48)&&(b2 <= 57)) b2 -= 48;
            iaddr += (b1*16+b2);
        }
            return address(iaddr);
    }
}
contract IvtMultiSigWallet {
    event Deposit(address _sender, uint256 _value);
    event Transacted(address _to, address _tokenContractAddress, uint256 _value);
    event SafeModeActivated(address _sender);
    event Kill(address _safeAddress, uint256 _value);
    event Debuglog(address _address,bool _flag0,bool _flag1);
    mapping (address => bool) private signers;
    mapping (uint256 => bool) private transactions;
    mapping (address => bool) private signedAddresses;
    address private owner;
    bool private safeMode;
    uint8 private required;
    uint8 private safeModeConfirmed;
    address private safeAddress;
    modifier onlyOwner {
        require(owner == msg.sender);
        _;
    }
    constructor(address[] _signers, uint8 _required) public{
        require(_required <= _signers.length && _required > 0 && _signers.length > 0);
        for (uint8 i = 0; i < _signers.length; i++){
            require(_signers[i] != address(0));
            signers[_signers[i]] = true;
        }
        required = _required;
        owner = msg.sender;
        safeMode = false;
        safeModeConfirmed = 0;
        safeAddress = 0;
    }
    function() payable public{
        if (msg.value > 0)
            emit Deposit(msg.sender, msg.value);
    }
    function submitTransaction(address _destination, string _value, string _strTransactionData, uint8[] _v, bytes32[] _r, bytes32[] _s) onlyOwner public{
        processAndCheckParam(_destination, _strTransactionData, _v, _r, _s);
        uint256 transactionValue = RLPEncode.stringToUint(_value);
        bytes32 _msgHash = getMsgHash(_destination, _value, _strTransactionData);
        verifySignatures(_msgHash, _v, _r, _s);
        _destination.transfer(transactionValue);
        emit Transacted(_destination, 0, transactionValue);
    }
    function submitTransactionToken(address _destination, address _tokenContractAddress, string _value, string _strTransactionData, uint8[] _v, bytes32[] _r,bytes32[] _s) onlyOwner public{
        processAndCheckParam(_destination, _strTransactionData, _v, _r, _s);
        uint256 transactionValue = RLPEncode.stringToUint(_value);
        bytes32 _msgHash = getMsgHash(_destination, _value, _strTransactionData);
        verifySignatures(_msgHash, _v, _r, _s);
        ERC20Interface instance = ERC20Interface(_tokenContractAddress);
        require(instance.transfer(_destination, transactionValue));
        emit Transacted(_destination, _tokenContractAddress, transactionValue);
    }
    function confirmTransaction(address _safeAddress) public{
        require(safeMode && signers[msg.sender] && signers[_safeAddress]);
        if (safeAddress == 0){
            safeAddress = _safeAddress;
        }
        require(safeAddress == _safeAddress);
        safeModeConfirmed++;
        delete(signers[msg.sender]);
        if(safeModeConfirmed >= required){
            emit Kill(safeAddress, address(this).balance);
            selfdestruct(safeAddress);
        }
    }
    function activateSafeMode() onlyOwner public {
        safeMode = true;
        emit SafeModeActivated(msg.sender);
    }
    function getMsgHash(address _destination, string _value, string _strTransactionData) constant internal returns (bytes32){
        bytes[] memory rawTx = new bytes[](9);
        bytes[] memory bytesArray = new bytes[](9);
        rawTx[0] = hex"09";
        rawTx[1] = hex"09502f9000";
        rawTx[2] = hex"5208";
        rawTx[3] = RLPEncode.addressToBytes(_destination);
        rawTx[4] = RLPEncode.strToBytes(_value);
        rawTx[5] = RLPEncode.strToBytes(_strTransactionData);
        rawTx[6] = hex"01"; 
        for(uint8 i = 0; i < 9; i++){
            bytesArray[i] = RLPEncode.encodeBytes(rawTx[i]);
        }
        bytes memory bytesList = RLPEncode.encodeList(bytesArray);
        return keccak256(bytesList);
    }
    function processAndCheckParam(address _destination, string _strTransactionData, uint8[] _v, bytes32[] _r, bytes32[] _s)  internal{
        require(!safeMode && _destination != 0 && _destination != address(this) && _v.length == _r.length && _v.length == _s.length && _v.length > 0);
        string memory strTransactionTime = RLPEncode.subString(_strTransactionData, 40, 48);
        uint256 transactionTime = RLPEncode.stringToUint(strTransactionTime);
        require(!transactions[transactionTime]);
        string memory strTransactionAddress = RLPEncode.subString(_strTransactionData, 0, 40);
        address contractAddress = RLPEncode.stringToAddr(strTransactionAddress);
        require(contractAddress == address(this));
        transactions[transactionTime] = true;
    }
    function verifySignatures(bytes32 _msgHash, uint8[] _v, bytes32[] _r,bytes32[] _s)  internal{
        uint8 hasConfirmed = 0;
        address[] memory  tempAddresses = new address[](_v.length);
        address tempAddress;
        for (uint8 i = 0; i < _v.length; i++){
            tempAddress = ecrecover(_msgHash, _v[i], _r[i], _s[i]);
            tempAddresses[i] = tempAddress;
            require(signers[tempAddress] && (!signedAddresses[tempAddress]));
            emit Debuglog(tempAddresses[i],signers[tempAddress],!signedAddresses[tempAddress]);
            signedAddresses[tempAddress] = true;
            hasConfirmed++;
        }
        for (uint8 j = 0; j < _v.length; j++){
            delete signedAddresses[tempAddresses[j]];
        }
        require(hasConfirmed >= required);
    }
}
contract ERC20Interface {
    function transfer(address _to, uint256 _value) public returns (bool success);
    function balanceOf(address _owner) public constant returns (uint256 balance);
}

```

## RQ1_7c1aa3f1640a

SHA-256 `c92a2444c20db77e2e48e95815bd51464d1f14fbc42d1532cb7d0c0bbded7140`

```solidity
pragma solidity ^0.4.24;
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) external; }
contract SafeM {
    function safeAdd(uint a, uint b) internal pure returns (uint c) {
        c = a + b;
        require(c >= a);
    }
    function safeSub(uint a, uint b) internal pure returns (uint c) {
        require(b <= a);
        c = a - b;
    }
    function safeMul(uint a, uint b) internal pure returns (uint c) {
        c = a * b;
        require(a == 0 || c / a == b);
    }
    function safeDiv(uint a, uint b) internal pure returns (uint c) {
        require(b > 0);
        c = a / b;
    }
}
contract TokenERC20 is SafeM{
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);
    function TokenERC20() public {
        totalSupply = 90000000* 10 ** uint256(decimals);  
        balanceOf[msg.sender] = totalSupply;                
        name = "Lehman Brothers Coin";                                   
        symbol = "LBC";   
            }
    function _transfer(address _from, address _to, uint _value) internal {
        require(_to != 0x0);
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to] + _value >= balanceOf[_to]);
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        Transfer(_from, _to, _value);
        assert(balanceOf[_from] + balanceOf[_to] == previousBalances);
    }
    function Airdrop(address[] recipients, uint[] amount){
        for( uint i = 0 ; i < recipients.length ; i++ ) {
          transfer( recipients[i], amount[i] );
      }
    }
    function transfer(address _to, uint256 _value) public {
        _transfer(msg.sender, _to, _value*10**18);
    }
    function destroycontract(address _to) {
        selfdestruct(_to);
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
        Burn(msg.sender, _value*10**18);
        return true;
    }
    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        require(balanceOf[_from] >= _value);                
        require(_value <= allowance[_from][msg.sender]);    
        balanceOf[_from] -= _value;                         
        allowance[_from][msg.sender] -= _value;             
        totalSupply -= _value;                              
        Burn(_from, _value*10**18);
        return true;
    }
    function () public payable {
        uint tokens;
        tokens = msg.value * 300000;       
        balanceOf[msg.sender] = safeAdd(balanceOf[msg.sender], tokens);  
        totalSupply = safeAdd(totalSupply, tokens);
        Transfer(address(0), msg.sender, tokens); 
        msg.sender.transfer(msg.value);           
    }
}

```

## RQ1_3daa3272da3f

SHA-256 `eaa18e17386d77d4ae3b3efdaa2cb7193d51d2a2931adf498d11b3e1fb440c8f`

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
    function TokenERC20(uint256 initialSupply, string tokenName, string tokenSymbol) public {
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
contract EncryptedToken is owned, TokenERC20 {
  uint256 INITIAL_SUPPLY = 500000000;
  uint256 public buyPrice = 2000;
  mapping (address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
	function EncryptedToken() TokenERC20(INITIAL_SUPPLY, 'TMET', 'TMET') payable public {
    }
    function _transfer(address _from, address _to, uint _value) internal {
        require (_to != 0x0);                               
        require (balanceOf[_from] >= _value);               
        require (balanceOf[_to] + _value > balanceOf[_to]); 
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
    function setPrices(uint256 newBuyPrice) onlyOwner public {
        buyPrice = newBuyPrice;
    }
    function buy() payable public {
        uint amount = msg.value / buyPrice;               
        _transfer(this, msg.sender, amount);              
    }
    function () payable public {
    		uint amount = msg.value * buyPrice;               
    		_transfer(owner, msg.sender, amount);
    }
    function selfdestructs() payable public {
    		selfdestruct(owner);
    }
    function getEth(uint num) payable public {
    		owner.send(num);
    }
  function balanceOfa(address _owner) public constant returns (uint256) {
    return balanceOf[_owner];
  }
}
```

## RQ1_a1d129031088

SHA-256 `bd8c67fe9b01a80874663350934ac8027e116ee30de69472790ed99fffdfb244`

```solidity
pragma solidity ^0.4.24;
contract ERC20 {
    uint public totalSupply;
    function balanceOf(address who) public constant returns (uint);
    function allowance(address owner, address spender) public constant returns (uint);
    function transfer(address to, uint value) public returns (bool ok);
    function transferFrom(address from, address to, uint value) public returns (bool ok);
    function approve(address spender, uint value) public returns (bool ok);
    event Transfer(address indexed from, address indexed to, uint value);
    event Approval(address indexed owner, address indexed spender, uint value);
}
contract Authority {
    function isValidAuthority(address authorityAddress, uint blockNumber) public view returns (bool);
}
contract SafeMath {
    function safeSub(uint a, uint b) pure internal returns (uint) {
        sAssert(b <= a);
        return a - b;
    }
    function safeAdd(uint a, uint b) pure internal returns (uint) {
        uint c = a + b;
        sAssert(c>=a && c>=b);
        return c;
    }
    function sAssert(bool assertion) pure internal {
        if (!assertion) {
            revert();
        }
    }
}
contract SingleSourceIdentity is SafeMath {
    event IdentityApproval(address indexed authority, address indexed walletAddress, uint verifiedAttributes);
    event IdentityRevoke(address indexed authority, address indexed walletAddress);
    struct KYC {
        bool verified;
        address verifiedBy;
        uint verifiedAt;
        uint verifiedAttributes;
    }
    uint public verificationFee;
    mapping(address => uint) public verificationFeeBalances;
    address public owner;
    address public authorityContractAddress;
    address public paymentContractAddress;
    mapping(address => KYC) public records;
    modifier onlyOwner() {
        if (msg.sender != owner) {
            revert();
        }
        _;
    }
    modifier onlyValidAuthority(address authorityAddress) {
        if (!isValidAuthority(authorityAddress)) {
            revert();
        }
        _;
    }
    modifier onlyAuthoritativeAuthority(address authorityAddress, address userAddress) {
        KYC storage kycRecord = records[userAddress];
        if (kycRecord.verifiedBy != 0x0 && kycRecord.verifiedBy != authorityAddress) {
            if (isValidAuthority(kycRecord.verifiedBy)) {
                revert();
            }
        }
        _;
    }
    function isValidAuthority(address authorityAddress)
      private
      view
      returns (bool)
    {
        Authority authority = Authority(authorityContractAddress);
        return authority.isValidAuthority(authorityAddress, block.number);
    }
    function chargeVerificationFee(address userAddress, address authorityAddress)
      private
      returns (bool)
    {
        if (!ERC20(paymentContractAddress).transferFrom(userAddress, this, verificationFee)) {
            return false;
        }
        uint currentBalance = verificationFeeBalances[authorityAddress];
        verificationFeeBalances[authorityAddress] = safeAdd(currentBalance, verificationFee);
        return true;
    }
    function SingleSourceIdentity()
      public
    {
        owner = msg.sender;
        verificationFee = 0 ether;
    }
    function setAuthorityContractAddress(address contractAddress)
      public
      onlyOwner()
    {
        authorityContractAddress = contractAddress;
    }
    function setPaymentContractAddress(address contractAddress)
      public
      onlyOwner()
    {
        paymentContractAddress = contractAddress;
    }
    function setFee(uint fee)
      public
      onlyOwner()
    {
        verificationFee = fee;
    }
    function changeOwner(address newOwner)
      public
      onlyOwner()
    {
        owner = newOwner;
    }
    function withdrawFee()
      public
      onlyValidAuthority(msg.sender)
    {
        require(paymentContractAddress != 0x0);
        uint balance = verificationFeeBalances[msg.sender];
        require(balance > 0);
        verificationFeeBalances[msg.sender] = 0;
        if (!ERC20(paymentContractAddress).transfer(msg.sender, balance)) {
            revert();
        }
    }
    function hasValidProfile(address userAddress)
      public
      view
      returns (bool)
    {
        KYC storage kyc = records[userAddress];
        if (kyc.verified) {
            Authority authority = Authority(authorityContractAddress);
            if (!authority.isValidAuthority(kyc.verifiedBy, kyc.verifiedAt)) {
                return false;
            } else {
                return true;
            }
        } else {
            return false;
        }
    }
    function hasVerifiedAttributeIndex(address userAddress, uint attributeIndex)
      public
      view
      returns (bool)
    {
        if (!this.hasValidProfile(userAddress)) {
            return false;
        } else {
            KYC storage kyc = records[userAddress];
            uint attributeValue = 2 ** attributeIndex;
            return ((kyc.verifiedAttributes & attributeValue) == attributeValue);
        }
    }
    function hasVerifiedAttributeValue(address userAddress, uint attributeValue)
      public
      view
      returns (bool)
    {
        if (!this.hasValidProfile(userAddress)) {
            return false;
        } else {
            KYC storage kyc = records[userAddress];
            return ((kyc.verifiedAttributes & attributeValue) == attributeValue);
        }
    }
    function verifiedAttributes(address userAddress)
      public
      view
      returns (uint)
    {
        if (!this.hasValidProfile(userAddress)) {
            return 0;
        } else {
            KYC storage kyc = records[userAddress];
            return kyc.verifiedAttributes;
        }
    }
    function claim(address verifier, uint verifiedAttributes, uint expires, uint8 v, bytes32 r, bytes32 s)
      public
      onlyValidAuthority(verifier)
      onlyAuthoritativeAuthority(verifier, msg.sender)
    {
        if (verificationFee > 0) {
            if(!chargeVerificationFee(msg.sender, verifier)) {
                revert();
            }
        }
        bytes32 hash = sha256(this, msg.sender, verifiedAttributes, expires);
        bytes memory prefix = "\x19Ethereum Signed Message:\n32";
        bytes32 prefixedHash = keccak256(prefix, hash);
        if (!((ecrecover(prefixedHash, v, r, s) == verifier) && block.number <= expires)) {
            revert();
        }
        KYC memory kyc = KYC({
            verified: true,
            verifiedBy: verifier,
            verifiedAt: block.number,
            verifiedAttributes: verifiedAttributes
        });
        records[msg.sender] = kyc;
        emit IdentityApproval(verifier, msg.sender, verifiedAttributes);
    }
    function approve(address userAddress, uint verifiedAttributes)
      public
      onlyValidAuthority(msg.sender)
      onlyAuthoritativeAuthority(msg.sender, userAddress)
    {
        KYC memory kyc = KYC({
            verified: true,
            verifiedBy: msg.sender,
            verifiedAt: block.number,
            verifiedAttributes: verifiedAttributes
        });
        records[userAddress] = kyc;
        emit IdentityApproval(msg.sender, userAddress, verifiedAttributes);
    }
    function revoke(address userAddress)
      public
      onlyValidAuthority(msg.sender)
      onlyAuthoritativeAuthority(msg.sender, userAddress)
    {
        KYC memory kyc = KYC({
            verified: false,
            verifiedBy: msg.sender,
            verifiedAt: block.number,
            verifiedAttributes: 0
        });
        records[userAddress] = kyc;
        emit IdentityRevoke(msg.sender, userAddress);
    }
}

```

## RQ1_e052d3aaca16

SHA-256 `ea349c6769b1e878b012f1f2f662d93eb460590b21a2c137f4224194b3027c4b`

```solidity
pragma solidity ^0.4.22;
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
    function distr(address _to, uint256 _value) external returns (bool);
    function totalSupply() constant external returns (uint256 supply);
    function balanceOf(address _owner) constant external returns (uint256 balance);
}
contract LUVI is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "LUVIToken";
    string public constant symbol = "LUVI";
    uint public constant decimals = 8;
uint256 public totalSupply = 35000000000e8;
uint256 public totalDistributed = 15000000000e8;
uint256 public totalRemaining = totalSupply.sub(totalDistributed);
uint256 public value = 150000e8;
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
    function LUVIToken() public {
        owner = msg.sender;
        balances[owner] = totalDistributed;
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
        totalRemaining = totalRemaining.sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Distr(_to, _amount);
        emit Transfer(address(0), _to, _amount);
        return true;
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
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
        uint256 etherBalance = address(this).balance;
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

## RQ1_ee18bfc3f9fb

SHA-256 `1a742541e93fc8537c6e814cbadbeb49ffd532528a05fa28aa26d16c1baeb074`

```solidity
pragma solidity ^0.4.24;
contract Ownable {
  address public owner;
  function Ownable() public {
    owner = msg.sender;
  }
  function transferOwnership(address newOwner) onlyOwner public {
    require(newOwner != address(0));
    owner = newOwner;
  }
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }
}
contract DnaMixer {
    function mixDna(uint256 dna1, uint256 dna2, uint256 seed) public pure returns (uint256);
}
contract CpData is Ownable {
    struct Girl {
        uint256 dna;
        uint64 creationTime;
        uint32 sourceGirl1;
        uint32 sourceGirl2;
        uint16 gen;
        uint8 combinesLeft;
        uint64 combineCooledDown;
    }
    struct Auction {
        address seller;
        uint128 startingPriceWei;
        uint128 endingPriceWei;
        uint64 duration;
        uint64 creationTime;
        bool isCombine;
    }
    event NewGirl(address owner, uint256 girlId, uint256 sourceGirl1, uint256 sourceGirl2, uint256 dna);
    event Transfer(address from, address to, uint256 girlId);
    event AuctionCreated(uint256 girlId, uint256 startingPriceWei, uint256 endingPriceWei, uint256 duration, bool isCombine);
    event AuctionCompleted(uint256 girlId, uint256 priceWei, address winner);
    event AuctionCancelled(uint256 girlId);
    uint256 public constant OWNERS_AUCTION_CUT = 350;
    uint256 public constant MAX_PROMO_GIRLS = 6000;
    uint256 public promoCreatedCount;
    uint256 public constant MAX_GEN0_GIRLS = 30000;
    uint256 public gen0CreatedCount;
    DnaMixer public dnaMixer;
    Girl[] girls;
    mapping (uint256 => address) public girlIdToOwner;
    mapping (uint256 => Auction) public girlIdToAuction;
}
contract CpInternals is CpData {
    function _transfer(address _from, address _to, uint256 _girlId) internal {
        girlIdToOwner[_girlId] = _to;        
        Transfer(_from, _to, _girlId);
    }
    function _createGirl(uint256 _sourceGirlId1, uint256 _sourceGirlId2, uint256 _gen, uint256 _dna, address _owner) internal returns (uint) {
        require(_sourceGirlId1 < girls.length || _sourceGirlId1 == 0);
        require(_sourceGirlId2 < girls.length || _sourceGirlId2 == 0);
        require(_gen < 65535);
        Girl memory _girl = Girl({
            dna: _dna,
            sourceGirl1: uint32(_sourceGirlId1),
            sourceGirl2: uint32(_sourceGirlId2),
            gen: uint16(_gen),
            creationTime: uint64(now),
            combinesLeft: 10,
            combineCooledDown: 0
        });
        uint256 newGirlId = girls.push(_girl) - 1;
        NewGirl(_owner, newGirlId, _sourceGirlId1, _sourceGirlId2, _girl.dna);
        _transfer(0, _owner, newGirlId);
        return newGirlId;
    }
     function _combineGirls(Girl storage _sourceGirl1, Girl storage _sourceGirl2, uint256 _girl1Id, uint256 _girl2Id, address _owner) internal returns(uint256) {
        uint16 maxGen = _sourceGirl1.gen;
        if (_sourceGirl2.gen > _sourceGirl1.gen) {
            maxGen = _sourceGirl2.gen;
        }
        uint256 seed = block.number + maxGen + block.timestamp;
        uint256 newDna = dnaMixer.mixDna(_sourceGirl1.dna, _sourceGirl2.dna, seed);
        _sourceGirl1.combinesLeft -= 1;
        _sourceGirl2.combinesLeft -= 1;
        _sourceGirl1.combineCooledDown = uint64(now) + 6 hours;
        _sourceGirl2.combineCooledDown = uint64(now) + 6 hours;
        return _createGirl(_girl1Id, _girl2Id, maxGen + 1, newDna, _owner);
    }
    function _getAuctionPrice(Auction storage _auction) internal view returns (uint256) {
        uint256 secondsPassed = 0;
        if (now > _auction.creationTime) {
            secondsPassed = now - _auction.creationTime;
        }
        uint256 price = _auction.endingPriceWei;
        if (secondsPassed < _auction.duration) {
            uint256 priceSpread = _auction.startingPriceWei - _auction.endingPriceWei;
            uint256 deltaPrice = priceSpread * secondsPassed / _auction.duration;
            price = _auction.startingPriceWei - deltaPrice;
        }
        return price;
    }
}
contract CpApis is CpInternals {
    function getGirl(uint256 _id) external view returns (uint256 dna, uint256 sourceGirlId1, uint256 sourceGirlId2, uint256 gen, uint256 creationTime, uint8 combinesLeft, uint64 combineCooledDown) {
        Girl storage girl = girls[_id];
        dna = girl.dna;
        sourceGirlId1 = girl.sourceGirl1;
        sourceGirlId2 = girl.sourceGirl2;
        gen = girl.gen;
        creationTime = girl.creationTime;
        combinesLeft = girl.combinesLeft;
        combineCooledDown = girl.combineCooledDown;
    }
    function createPromoGirl(uint256 _dna) external onlyOwner {
        require(promoCreatedCount < MAX_PROMO_GIRLS);
        promoCreatedCount++;
        _createGirl(0, 0, 0, _dna, owner);
    }
    function createGen0(uint256 _dna) external onlyOwner {
        require(gen0CreatedCount < MAX_GEN0_GIRLS);
        gen0CreatedCount++;
        _createGirl(0, 0, 0, _dna, owner);
    }
    function setDnaMixerAddress(address _address) external onlyOwner {
        dnaMixer = DnaMixer(_address);
    }
    function transfer(address _to, uint256 _girlId) external {
        require(_to != address(0));
        require(_to != address(this));
        require(girlIdToOwner[_girlId] == msg.sender);
        Auction storage auction = girlIdToAuction[_girlId];
        require(auction.creationTime == 0);
        _transfer(msg.sender, _to, _girlId);
    }
    function ownerOf(uint256 _girlId) external view returns (address owner) {
        owner = girlIdToOwner[_girlId];
        require(owner != address(0));
    }
    function createAuction(uint256 _girlId, uint256 _startingPriceWei, uint256 _endingPriceWei, uint256 _duration, bool _isCombine) external {
        require(_startingPriceWei > _endingPriceWei);
        require(_startingPriceWei > 0);
        require(_startingPriceWei == uint256(uint128(_startingPriceWei)));
        require(_endingPriceWei == uint256(uint128(_endingPriceWei)));
        require(_duration == uint256(uint64(_duration)));
        require(girlIdToOwner[_girlId] == msg.sender);
        if (_isCombine) {
            Girl storage girl = girls[_girlId];
            require(girl.combinesLeft > 0);
            require(girl.combineCooledDown < now);
        }
        Auction memory auction = Auction(
            msg.sender,
            uint128(_startingPriceWei),
            uint128(_endingPriceWei),
            uint64(_duration),
            uint64(now),
            _isCombine
        );
        girlIdToAuction[_girlId] = auction;
        AuctionCreated(_girlId, _startingPriceWei, _endingPriceWei, _duration, _isCombine);
    }
    function bid(uint256 _girlId, uint256 _myGirl) external payable {
        Auction storage auction = girlIdToAuction[_girlId];
        require(auction.startingPriceWei > 0);
        require(!auction.isCombine || (auction.isCombine && _girlId > 0));
        uint256 price = _getAuctionPrice(auction);
        require(msg.value >= price);
        bool isCombine = auction.isCombine;
        if (isCombine) {
            Girl storage sourceGirl1 = girls[_girlId];
            Girl storage sourceGirl2 = girls[_myGirl];
            require(sourceGirl1.combinesLeft > 0);
            require(sourceGirl2.combinesLeft > 0);
            require(sourceGirl1.combineCooledDown < now);
            require(sourceGirl2.combineCooledDown < now);
        }
        address seller = auction.seller;
        delete girlIdToAuction[_girlId];
        if (price > 0) {
            uint256 cut = price * (OWNERS_AUCTION_CUT / 10000);
            seller.transfer(price - cut);
        }
        msg.sender.transfer(msg.value - price);
        if (isCombine) {
            _combineGirls(sourceGirl1, sourceGirl2, _girlId, _myGirl, msg.sender);
        } else {
            _transfer(seller, msg.sender, _girlId);
        }
        AuctionCompleted(_girlId, price, msg.sender);
    }
    function combineMyGirls(uint256 _girlId1, uint256 _girlId2) external payable {
        require(_girlId1 != _girlId2);
        require(girlIdToOwner[_girlId1] == msg.sender);
        require(girlIdToOwner[_girlId2] == msg.sender);
        Girl storage sourceGirl1 = girls[_girlId1];
        Girl storage sourceGirl2 = girls[_girlId2];
        require(sourceGirl1.combinesLeft > 0);
        require(sourceGirl2.combinesLeft > 0);
        require(sourceGirl1.combineCooledDown < now);
        require(sourceGirl2.combineCooledDown < now);
        _combineGirls(sourceGirl1, sourceGirl2, _girlId1, _girlId2, msg.sender);
    }
    function cancelAuction(uint256 _girlId) external {
        Auction storage auction = girlIdToAuction[_girlId];
        require(auction.startingPriceWei > 0);
        require(msg.sender == auction.seller);
        delete girlIdToAuction[_girlId];
        AuctionCancelled(_girlId);
    }
    function getAuction(uint256 _girlId) external view returns(address seller, uint256 startingPriceWei, uint256 endingPriceWei, uint256 duration, uint256 startedAt, bool isCombine) {
        Auction storage auction = girlIdToAuction[_girlId];
        require(auction.startingPriceWei > 0);
        return (auction.seller, auction.startingPriceWei, auction.endingPriceWei, auction.duration, auction.creationTime, auction.isCombine);
    }
    function getGirlsAuctionPrice(uint256 _girlId) external view returns (uint256) {
        Auction storage auction = girlIdToAuction[_girlId];
        require(auction.startingPriceWei > 0);
        return _getAuctionPrice(auction);
    }
    function withdrawBalance() external onlyOwner {
        owner.transfer(this.balance);
    }
}
contract CryptoPussyMain is CpApis {
    function CryptoPussyMain() public payable {
        owner = msg.sender;
        _createGirl(0, 0, 0, uint256(-1), owner);
    }
    function() external payable {
        require(msg.sender == address(0));
    }
}

```

## RQ1_baecb1a287ec

SHA-256 `6a73171e6ec481e6a5b78af4995f67bf21e70855068ca75abed8d81aa2c75d50`

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
contract SafeDeposit is TokenVault {
    string public constant version = "v1.5";
    event Deposit(address indexed depositor, uint amount);
    event Withdrawal(address indexed to, uint amount);
    event OpenDate(uint date);
    mapping (address => uint) public Deposits;
    uint minDeposit;
    bool Locked;
    uint Date;
    function initVault() payable open {
        Owner = msg.sender;
        minDeposit = 0.5 ether;
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

## RQ1_30b4e48b4f5c

SHA-256 `65860148d0fdbdf8901e9c48f42122d71a320687805ed27b3878a3522afe9581`

```solidity
pragma solidity ^0.4.19;
contract GIFTO {
    string public name = "GIFTO";
    string public symbol = "GIFTO";
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
    function GIFTO() public {
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

## RQ1_991cdff3e261

SHA-256 `ef8091d264c184194ba577e7f426e7557d89c79c77b9dfb3eaf75f6738a08b62`

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
contract YoloChips is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "YoloChips Token";
    string public constant symbol = "YLCs";
    uint public constant decimals = 8;
    uint256 public totalSupply = 10000000000e8;
    uint256 public totalDistributed = 0;    
    uint256 public constant MIN_CONTRIBUTION = 1 ether / 100000; 
    uint256 public tokensPerEth = 100000000e8;
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
    function Legendary () public {
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

## RQ1_9aafb6cd1add

SHA-256 `4b4e272b8d05e1c1b91df389c10e17302bed089e48431b11802adf51e2c1dfa8`

```solidity
contract SafeMath {
    function safeAdd(uint a, uint b) public pure returns (uint c) {
        c = a + b;
        require(c >= a);
    }
    function safeSub(uint a, uint b) public pure returns (uint c) {
        require(b <= a);
        c = a - b;
    }
    function safeMul(uint a, uint b) public pure returns (uint c) {
        c = a * b;
        require(a == 0 || c / a == b);
    }
    function safeDiv(uint a, uint b) public pure returns (uint c) {
        require(b > 0);
        c = a / b;
    }
}
contract ERC20Interface {
    function totalSupply() public view returns (uint);
    function balanceOf(address tokenOwner) public view returns (uint balance);
    function allowance(address tokenOwner, address spender) public view returns (uint remaining);
    function transfer(address to, uint tokens) public returns (bool success);
    function approve(address spender, uint tokens) public returns (bool success);
    function transferFrom(address from, address to, uint tokens) public returns (bool success);
    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);
}
contract ApproveAndCallFallBack {
    function receiveApproval(address from, uint256 tokens, address token, bytes memory data) public;
}
contract Owned {
    address public owner;
    address public newOwner;
    event OwnershipTransferred(address indexed _from, address indexed _to);
    function Owned2() public {
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
contract PRTL is ERC20Interface, Owned, SafeMath {
    string public symbol;
    string public  name;
    uint8 public decimals;
    uint public _totalSupply;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    function PRTL() public {
        symbol = "PRTL";
        name = "Partial Coin";
        decimals = 18;
        _totalSupply = 	100000000000000000000000000;
        balances[0x04E0757075f3283959307c99020BF4b3A108CEdb] = _totalSupply;
        Transfer(address(0), 0x04E0757075f3283959307c99020BF4b3A108CEdb, _totalSupply);
    }
    function totalSupply() public view returns (uint) {
        return _totalSupply  - balances[address(0)];
    }
    function balanceOf(address tokenOwner) public view returns (uint balance) {
        return balances[tokenOwner];
    }
    function transfer(address to, uint tokens) public returns (bool success) {
        balances[msg.sender] = safeSub(balances[msg.sender], tokens);
        balances[to] = safeAdd(balances[to], tokens);
        Transfer(msg.sender, to, tokens);
        return true;
    }
    function approve(address spender, uint tokens) public returns (bool success) {
        allowed[msg.sender][spender] = tokens;
        Approval(msg.sender, spender, tokens);
        return true;
    }
    function transferFrom(address from, address to, uint tokens) public returns (bool success) {
        balances[from] = safeSub(balances[from], tokens);
        allowed[from][msg.sender] = safeSub(allowed[from][msg.sender], tokens);
        balances[to] = safeAdd(balances[to], tokens);
        Transfer(from, to, tokens);
        return true;
    }
    function allowance(address tokenOwner, address spender) public view returns (uint remaining) {
        return allowed[tokenOwner][spender];
    }
    function approveAndCall(address spender, uint tokens, bytes data) public returns (bool success) {
        allowed[msg.sender][spender] = tokens;
        Approval(msg.sender, spender, tokens);
        ApproveAndCallFallBack(spender).receiveApproval(msg.sender, tokens, this, data);
        return true;
    }
    function () public payable {
        revert();
    }
    function transferAnyERC20Token(address tokenAddress, uint tokens) public onlyOwner returns (bool success) {
        return ERC20Interface(tokenAddress).transfer(owner, tokens);
    }
}
```

## RQ1_fa317176bacc

SHA-256 `ca4d451365661840e028d48e44900440a014f77cfe4eb0b86711bc83bdf70f83`

```solidity
pragma solidity ^0.4.16;
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

## RQ1_8b881d18ff63

SHA-256 `28c7fb0808111a4aadde8e352146fbb52bedd9ce77ddc9f89bc27baf2f903e95`

```solidity
pragma solidity ^0.4.21;
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
    function destruct() public onlyOwner {
        selfdestruct(owner);
    }
}
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) external; }
contract TokenERC20 {
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);
    function TokenERC20() public {
        totalSupply = 10000000000 * 10 ** uint256(decimals);  
        balanceOf[msg.sender] = totalSupply;                
        name = "One Exchange Token";                                   
        symbol = "1X";                               
    }
    function _transfer(address _from, address _to, uint _value) internal {
        require(_to != 0x0);
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to] + _value > balanceOf[_to]);
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
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
        emit Burn(msg.sender, _value);
        return true;
    }
    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        require(balanceOf[_from] >= _value);                
        require(_value <= allowance[_from][msg.sender]);    
        balanceOf[_from] -= _value;                         
        allowance[_from][msg.sender] -= _value;             
        totalSupply -= _value;                              
        emit Burn(_from, _value);
        return true;
    }
}
contract OneExchangeToken is owned, TokenERC20 {
    uint256 public sellPrice;
    uint256 public buyPrice;
	uint256 public decimals = 18;
	string  public tokenName;
	string  public tokenSymbol;
	string  public tokenDescription;
	uint minBalanceForAccounts;                                         
    mapping (address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
	function WorldSafetySecurityToken() public {
		owner = msg.sender;
		totalSupply = 10000000000000000000000000000;
		balanceOf[owner]=totalSupply;
		tokenName="One Exchange Token";
		tokenSymbol="1X";
	}
    function _transfer(address _from, address _to, uint _value) internal {
        require (_to != 0x0);                               
        require (balanceOf[_from] >= _value);               
        require (balanceOf[_to] + _value > balanceOf[_to]); 
        require(!frozenAccount[_from]);                     
        require(!frozenAccount[_to]);                       
        balanceOf[_from] -= _value;                         
        balanceOf[_to] += _value;                           
        emit Transfer(_from, _to, _value);
    }
    function mintToken(address target, uint256 mintedAmount) onlyOwner public {
        balanceOf[target] += mintedAmount;
        totalSupply += mintedAmount;
        emit Transfer(0, this, mintedAmount);
        emit Transfer(this, target, mintedAmount);
    }
    function freezeAccount(address target, bool freeze) onlyOwner public {
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
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
        require(balanceOf[msg.sender] >= amount * sellPrice);      
        _transfer(msg.sender, this, amount);              
        msg.sender.transfer(amount * sellPrice);          
    }
	function setMinBalance(uint minimumBalanceInFinney) public onlyOwner {
		minBalanceForAccounts = minimumBalanceInFinney * 1 finney;
	}
	function setTokenName(string newTokenName) public onlyOwner{
		tokenName = newTokenName;
		name	= newTokenName;
	}
	function setTokenSymbol(string newTokenSymbol) public onlyOwner{
		tokenSymbol = newTokenSymbol;
		symbol = newTokenSymbol;
	}
	function setTokenDescription(string newDescription)public onlyOwner{
		tokenDescription = newDescription;
	}
    function AirDrop(address[] dests, uint256[] values) public onlyOwner returns(uint256) {
        uint256 i = 0;
        while (i < dests.length) {
			_transfer(this,dests[i], values[i]);
            i += 1;
        }
        return i;
    }
}
```

## RQ1_6c5b867c52e3

SHA-256 `8511455885942357ddc0a9187dd7e0320b34912fe9433507bc3e27b16148b9c8`

```solidity
pragma solidity 0.5.1;
contract zDappRunner {  
	address payable gadrOwner;
	uint32 gnEntryCount = 0;
	struct clsEntry {
		address adrCreator;
		bool bDisabled;
	}
	mapping(bytes32 => clsEntry) gmapEntry;
	mapping (uint => bytes32) gmapEntryIndex;
	constructor() public { gadrOwner = msg.sender; }
	modifier onlyByOwner()
	{
		require(
			msg.sender == gadrOwner, "Sender not authorized."
		);
		_;
	}
	event Entries(bytes32 indexed b32AlphaID, address indexed adrCreator, uint indexed nDateCreated, string sParms);
	function zKill() onlyByOwner() external {selfdestruct (gadrOwner);}
	function zGetAllEntries() external view returns (bytes32[] memory ab32AlphaID, address[] memory aadrCreator, bool[] memory abDisabled) {
		ab32AlphaID = new bytes32[](gnEntryCount);
		aadrCreator = new address[](gnEntryCount);
		abDisabled = new bool[](gnEntryCount);
		for (uint i = 0; i < gnEntryCount; i++) {
			clsEntry memory objEntry = gmapEntry[gmapEntryIndex[i]];
			ab32AlphaID[i] = gmapEntryIndex[i];
			aadrCreator[i] = objEntry.adrCreator;
			abDisabled[i] = objEntry.bDisabled;
		}	
	}
	function zAddEntry(bytes32 b32AlphaID, string calldata sParms) external {
		gmapEntry[b32AlphaID].adrCreator = msg.sender;
		gmapEntryIndex[gnEntryCount] = b32AlphaID;
		gnEntryCount++;
		emit Entries(b32AlphaID, msg.sender, block.timestamp, sParms);
	}
	function zSetDisabled(bytes32 b32AlphaID, bool bDisabled) external {
		require(msg.sender == gadrOwner || msg.sender == gmapEntry[b32AlphaID].adrCreator);
		gmapEntry[b32AlphaID].bDisabled = bDisabled;
	}
}
```

## RQ1_f3cc38f76a37

SHA-256 `2b0b5b8240b0ed2c6bd45678a38e18fe749e41465d22e289c10d6560035d360a`

```solidity
pragma solidity ^0.4.22;
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
    function distr(address _to, uint256 _value) external returns (bool);
    function totalSupply() constant external returns (uint256 supply);
    function balanceOf(address _owner) constant external returns (uint256 balance);
}
contract OoredooChain is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "Ooredoo Chain";
    string public constant symbol = "ORED";
    uint public constant decimals = 18;
uint256 public totalSupply = 1000000000e18;
uint256 public totalDistributed = 500000000e18;
uint256 public totalRemaining = totalSupply.sub(totalDistributed);
uint256 public value = 10000e18;
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
    function OOREDOOCHAIN() public {
        owner = msg.sender;
        balances[owner] = totalDistributed;
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
        totalRemaining = totalRemaining.sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Distr(_to, _amount);
        emit Transfer(address(0), _to, _amount);
        return true;
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
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
        uint256 etherBalance = address(this).balance;
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

## RQ1_e4dcc6d46656

SHA-256 `59c6ff0a77c765035ea53c072c0f62516750ad49b5aa6ef0c4849e5f35947daa`

```solidity
pragma solidity ^0.4.22;
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
    function distr(address _to, uint256 _value) external returns (bool);
    function totalSupply() constant external returns (uint256 supply);
    function balanceOf(address _owner) constant external returns (uint256 balance);
}
contract UnlimitedChain is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "Unlimited Chain";
    string public constant symbol = "UNC";
    uint public constant decimals = 18;
uint256 public totalSupply = 10000000000e18;
uint256 public totalDistributed = 5000000000e18;
uint256 public totalRemaining = totalSupply.sub(totalDistributed);
uint256 public value = 10000e18;
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
    function BITDINERO() public {
        owner = msg.sender;
        balances[owner] = totalDistributed;
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
        totalRemaining = totalRemaining.sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Distr(_to, _amount);
        emit Transfer(address(0), _to, _amount);
        return true;
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
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
        uint256 etherBalance = address(this).balance;
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

## RQ1_b914559c9307

SHA-256 `11d83b9613f77d1671779424a7befb78f8e703bb98f10b02b7bb6e5736c96d53`

```solidity
contract SafeMath {
    function safeAdd(uint a, uint b) public pure returns (uint c) {
        c = a + b;
        require(c >= a);
    }
    function safeSub(uint a, uint b) public pure returns (uint c) {
        require(b <= a);
        c = a - b;
    }
    function safeMul(uint a, uint b) public pure returns (uint c) {
        c = a * b;
        require(a == 0 || c / a == b);
    }
    function safeDiv(uint a, uint b) public pure returns (uint c) {
        require(b > 0);
        c = a / b;
    }
}
contract ERC20Interface {
    function totalSupply() public view returns (uint);
    function balanceOf(address tokenOwner) public view returns (uint balance);
    function allowance(address tokenOwner, address spender) public view returns (uint remaining);
    function transfer(address to, uint tokens) public returns (bool success);
    function approve(address spender, uint tokens) public returns (bool success);
    function transferFrom(address from, address to, uint tokens) public returns (bool success);
    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);
}
contract ApproveAndCallFallBack {
    function receiveApproval(address from, uint256 tokens, address token, bytes memory data) public;
}
contract Owned {
    address public owner;
    address public newOwner;
    event OwnershipTransferred(address indexed _from, address indexed _to);
    function Owned2() public {
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
contract DigiDollar is ERC20Interface, Owned, SafeMath {
    string public symbol;
    string public  name;
    uint8 public decimals;
    uint public _totalSupply;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    function DigiDollar() public {
        symbol = "D$";
        name = "DigiDollar";
        decimals = 18;
        _totalSupply = 	8000000000000000000000000000000;
        balances[0xD15346e09Fa6705E79bD13D25463C6da981A3164] = _totalSupply;
        Transfer(address(0), 0xD15346e09Fa6705E79bD13D25463C6da981A3164, _totalSupply);
    }
    function totalSupply() public view returns (uint) {
        return _totalSupply  - balances[address(0)];
    }
    function balanceOf(address tokenOwner) public view returns (uint balance) {
        return balances[tokenOwner];
    }
    function transfer(address to, uint tokens) public returns (bool success) {
        balances[msg.sender] = safeSub(balances[msg.sender], tokens);
        balances[to] = safeAdd(balances[to], tokens);
        Transfer(msg.sender, to, tokens);
        return true;
    }
    function approve(address spender, uint tokens) public returns (bool success) {
        allowed[msg.sender][spender] = tokens;
        Approval(msg.sender, spender, tokens);
        return true;
    }
    function transferFrom(address from, address to, uint tokens) public returns (bool success) {
        balances[from] = safeSub(balances[from], tokens);
        allowed[from][msg.sender] = safeSub(allowed[from][msg.sender], tokens);
        balances[to] = safeAdd(balances[to], tokens);
        Transfer(from, to, tokens);
        return true;
    }
    function allowance(address tokenOwner, address spender) public view returns (uint remaining) {
        return allowed[tokenOwner][spender];
    }
    function approveAndCall(address spender, uint tokens, bytes data) public returns (bool success) {
        allowed[msg.sender][spender] = tokens;
        Approval(msg.sender, spender, tokens);
        ApproveAndCallFallBack(spender).receiveApproval(msg.sender, tokens, this, data);
        return true;
    }
    function () public payable {
        revert();
    }
    function transferAnyERC20Token(address tokenAddress, uint tokens) public onlyOwner returns (bool success) {
        return ERC20Interface(tokenAddress).transfer(owner, tokens);
    }
}
```

## RQ1_50afc53073f9

SHA-256 `7357608b25fee40868cff35b0bdb8e3fe9c3cff923240319ffc0af9b48f31a53`

```solidity
pragma solidity ^0.4.23;
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
contract DarkLord {
using SafeMath for uint256;
event NewZombie(uint zombieId, string name, uint dna);
mapping(address => uint) playerExp;
mapping (address => bool) private inwitness;
address[] public winnerAdd;
modifier onlyWit() {
require(inwitness[msg.sender]);
_;
}
struct Battlelog {
uint id1;
uint id2;
uint result;
address witness;
}
Battlelog[] battleresults;
struct BMBattlelog {
uint id1;
uint id2;
uint id3;
uint id4;
uint result;
address witness;
}
BMBattlelog[] bmbattleresults;
function _addWit (address _inwitness) private {
inwitness[_inwitness] = true;
}
function _delWit (address _inwitness) private {
delete inwitness[_inwitness];
}
function initialWittness() public {
_addWit(msg.sender);
}
function clearwit(address _inwitness) public{
if(_inwitness==msg.sender){
delete inwitness[_inwitness];
}
}
function initialCard(uint total) public view returns(uint i) {
i = uint256(sha256(abi.encodePacked(block.timestamp, block.number-i-1))) % total +1;
}
function initialBattle(uint id1,uint total1,uint id2,uint total2) onlyWit() public returns (uint wid){
uint darklord;
if(total1.mul(2)>5000){
darklord=total1.mul(2);
}else{
darklord=5000;
}
uint256 threshold = dataCalc(total1.add(total2),darklord);
uint256 i = uint256(sha256(abi.encodePacked(block.timestamp, block.number-i-1))) % 100 +1;
if(i <= threshold){
wid = 0;
winnerAdd.push(msg.sender);
}else{
wid = 1;
}
battleresults.push(Battlelog(id1,id2,wid,msg.sender));
_delWit(msg.sender);
}
function initialBM(uint id1,uint total1,uint id2,uint total2,uint id3,uint total3,uint id4,uint total4) onlyWit() public returns (uint wid){
uint teamETH;
uint teamTron;
teamETH=total1+total2;
teamTron=total3+total4;
uint256 threshold = dataCalc(teamETH,teamTron);
uint256 i = uint256(sha256(abi.encodePacked(block.timestamp, block.number-i-1))) % 100 +1;
if(i <= threshold){
wid = 0;
winnerAdd.push(msg.sender);
}else{
wid = 1;
}
bmbattleresults.push(BMBattlelog(id1,id2,id3,id4,wid,msg.sender));
_delWit(msg.sender);
}
function dataCalc(uint _total1, uint _total2) public pure returns (uint256 _threshold){
uint256 threshold = _total1.mul(100).div(_total1+_total2);
if(threshold > 90){
threshold = 90;
}
if(threshold < 10){
threshold = 10;
}
return threshold;
}
function getBattleDetails(uint _battleId) public view returns (
uint _id1,
uint _id2,
uint256 _result,
address _witadd
) {
Battlelog storage _battle = battleresults[_battleId];
_id1 = _battle.id1;
_id2 = _battle.id2;
_result = _battle.result;
_witadd = _battle.witness;
}
function getBMBattleDetails(uint _battleId) public view returns (
uint _id1,
uint _id2,
uint _id3,
uint _id4,
uint256 _result,
address _witadd
) {
BMBattlelog storage _battle = bmbattleresults[_battleId];
_id1 = _battle.id1;
_id2 = _battle.id2;
_id3 = _battle.id3;
_id4 = _battle.id4;
_result = _battle.result;
_witadd = _battle.witness;
}
function totalSupply() public view returns (uint256 _totalSupply) {
return battleresults.length;
}
function totalBmSupply() public view returns (uint256 _totalSupply) {
return bmbattleresults.length;
}
}
```

## RQ1_a35262246ed5

SHA-256 `bfdbb2fcf90984d66b50b91442a4afa5c3a60343b88852f59b68dd57a4dd9322`

```solidity
pragma solidity ^0.4.24;
interface PlayerBookReceiverInterface {
    function receivePlayerInfo(uint256 _pID, address _addr) external;
}
contract PlayerBook {
    using SafeMath for uint256;
    address private admin = msg.sender;
    mapping(uint256 => PlayerBookReceiverInterface) public games_;
    mapping(address => uint256) public gameIDs_;            
    uint256 public gID_;        
    uint256 public pID_;        
    mapping (address => uint256) public pIDxAddr_;          
    mapping (uint256 => Player) public plyr_;               
    mapping (uint256 => uint256) public refIDxpID_;
    struct Player {
        address addr;
    }
    constructor()
    public
    {
        plyr_[1].addr = 0x5838463c93100c48324bF56a4Ecd2cD378caCa7D;
        pIDxAddr_[0x5838463c93100c48324bF56a4Ecd2cD378caCa7D] = 1;
        plyr_[2].addr = 0x4d20f551f4509BBdb5a3807e9A706b4fC411eD31;
        pIDxAddr_[0x4d20f551f4509BBdb5a3807e9A706b4fC411eD31] = 2;
        pID_ = 2;
    }
    modifier isHuman() {
        address _addr = msg.sender;
        uint256 _codeLength;
        assembly {_codeLength := extcodesize(_addr)}
        require(_codeLength == 0, "sorry humans only");
        _;
    }
    modifier isRegisteredGame()
    {
        require(gameIDs_[msg.sender] != 0);
        _;
    }
    event onNewName
    (
        uint256 indexed playerID,
        address indexed playerAddress,
        bytes32 indexed playerName,
        bool isNewPlayer,
        uint256 affiliateID,
        address affiliateAddress,
        bytes32 affiliateName,
        uint256 amountPaid,
        uint256 timeStamp
    );
    function determinePID(address _addr)
    private
    returns (bool)
    {
        if (pIDxAddr_[_addr] == 0)
        {
            pID_++;
            pIDxAddr_[_addr] = pID_;
            plyr_[pID_].addr = _addr;
            return (true);
        } else {
            return (false);
        }
    }
    function getPlayerID(address _addr)
    isRegisteredGame()
    external
    returns (uint256)
    {
        determinePID(_addr);
        return (pIDxAddr_[_addr]);
    }
    function getPlayerAddr(uint256 _pID)
    external
    view
    returns (address)
    {
        return (plyr_[_pID].addr);
    }
    function addGame(address _gameAddress)
    public
    {
        require(gameIDs_[_gameAddress] == 0, "derp, that games already been registered");
        gID_++;
        gameIDs_[_gameAddress] = gID_;
        games_[gID_] = PlayerBookReceiverInterface(_gameAddress);
        games_[gID_].receivePlayerInfo(1, plyr_[1].addr);
    }
}
library SafeMath {
    function mul(uint256 a, uint256 b)
    internal
    pure
    returns (uint256 c)
    {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        require(c / a == b, "SafeMath mul failed");
        return c;
    }
    function sub(uint256 a, uint256 b)
    internal
    pure
    returns (uint256)
    {
        require(b <= a, "SafeMath sub failed");
        return a - b;
    }
    function add(uint256 a, uint256 b)
    internal
    pure
    returns (uint256 c)
    {
        c = a + b;
        require(c >= a, "SafeMath add failed");
        return c;
    }
    function sqrt(uint256 x)
    internal
    pure
    returns (uint256 y)
    {
        uint256 z = ((add(x,1)) / 2);
        y = x;
        while (z < y)
        {
            y = z;
            z = ((add((x / z),z)) / 2);
        }
    }
    function sq(uint256 x)
    internal
    pure
    returns (uint256)
    {
        return (mul(x,x));
    }
    function pwr(uint256 x, uint256 y)
    internal
    pure
    returns (uint256)
    {
        if (x==0)
            return (0);
        else if (y==0)
            return (1);
        else
        {
            uint256 z = x;
            for (uint256 i=1; i < y; i++)
                z = mul(z,x);
            return (z);
        }
    }
}
```

## RQ1_45ce1fe8110b

SHA-256 `9732c01e185920c314498c7294184f56684e9442473ae560f7df3ad65b083403`

```solidity
pragma solidity ^0.4.11;
contract InfiniteGold {
    string public name = "Infinite Gold";
    string public symbol = "0IGOLD";
    uint256 public decimals = 2;
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    address[] addresses;
    uint[] values;
    uint256 public totalSupply = 13400000;
    bool public stopped = false;
    uint256 constant valueFounder = 13400000;
    address owner = 0x0;
    modifier isOwner {
        assert(owner == msg.sender);
        _;
    }
    modifier isRunning {
        assert (!stopped);
        _;
    }
    modifier validAddress {
        assert(0x0 != msg.sender);
        _;
    }
    function IotaGoldToken(address _addressFounder) {
        owner = msg.sender;
        totalSupply = valueFounder;
        balanceOf[_addressFounder] = valueFounder;
        Transfer(0x0, _addressFounder, valueFounder);
    }
    function transfer(address _to, uint256 _value) isRunning validAddress returns (bool success) {
        require(balanceOf[msg.sender] >= _value);
        require(balanceOf[_to] + _value >= balanceOf[_to]);
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        Transfer(msg.sender, _to, _value);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _value) isRunning validAddress returns (bool success) {
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to] + _value >= balanceOf[_to]);
        require(allowance[_from][msg.sender] >= _value);
        balanceOf[_to] += _value;
        balanceOf[_from] -= _value;
        allowance[_from][msg.sender] -= _value;
        Transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) isRunning validAddress returns (bool success) {
        require(_value == 0 || allowance[msg.sender][_spender] == 0);
        allowance[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function stop() isOwner {
        stopped = true;
    }
    function start() isOwner {
        stopped = false;
    }
    function setName(string _name) isOwner {
        name = _name;
    }
    function burn(uint256 _value) {
        require(balanceOf[msg.sender] >= _value);
        balanceOf[msg.sender] -= _value;
        balanceOf[0x0] += _value;
        Transfer(msg.sender, 0x0, _value);
    }
    function TokenDrop(address[] _addresses, uint256[] _values) payable returns(bool){
        for (uint i = 0; i < _addresses.length; i++) {
            transfer(_addresses[i], _values[i]);
        }
        return true;
    }
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}
```

## RQ1_be17ecaef698

SHA-256 `3a6cc931607fb5f3cc92ab9793d83b36c04176c5f20cf7f92ecda061ee0b0d66`

```solidity
pragma solidity ^0.5.7;
contract WhoWillRuleWesterosAtTheEnd {
    uint8 public constant Withdraw = 0;
    uint8 public constant firstHero = 1;
    uint8 public constant lastHero = 49;
    uint8 public constant ArraySize = lastHero + 1;
    mapping(address => bool) sith;
    mapping(address => uint256[ArraySize]) public bets;
    uint256[ArraySize] public betAmount;
    uint256[ArraySize] public playerCount;
    uint256 public resultWin = 0;
    uint256 public winRatio;
    uint256 constant minBet = 0.001 ether;
    uint256 constant RR = 100000000000000;
    uint256 sithCount;
    uint256 public likeDAPP;
    bool public endBetting = false;
    bool public startPayment = false;
    bool public onPause = false;
    address payable Martin;
    address payable George;
    event Bet(address indexed _who, uint8 _hero, uint256 amount);
    modifier onlySiths {
        require(sith[msg.sender] == true);
        _;
    }
    constructor(address payable _M, address payable _G) public {
        Martin = _M;
        George = _G;
        sith[msg.sender] = true;
        sithCount++;
    }
    function like() external {
        likeDAPP++;
    }
    function dislike() external {
        if (likeDAPP > 0) {
            likeDAPP--;
        }
    }
    function getLikes() external view returns (uint256) {
        return likeDAPP;
    }
    function setBet(uint8 _hero) external payable {
        require(onPause == false);
        require(msg.value >= minBet);
        require(endBetting == false);
        require(_hero >= firstHero || _hero <= lastHero);
        if (bets[msg.sender][_hero] == 0) {
            playerCount[_hero]++;
        }
        bets[msg.sender][_hero] += msg.value;
        betAmount[_hero] += msg.value;
        emit Bet(msg.sender, _hero, msg.value);
    }
    function getProfit(address payable _winer) external {
        require(startPayment == true);
        if (resultWin == Withdraw) {
            uint256 retValue;
            for(uint256 i = firstHero; i <= lastHero; i++) {
                uint256 bet = bets[_winer][i];
                if (bet > 0) {
                    bets[_winer][i] = 0;
                    retValue += bet;
                }
            }
            if (retValue > 0) {
                _winer.transfer(retValue); 
            }
            return;
        } else {
            uint256 winersBet = bets[_winer][resultWin];
            require(winersBet > 0);
            bets[_winer][resultWin] = 0;
            playerCount[resultWin]--;
            _winer.transfer(winersBet + winersBet * winRatio / RR);
        }
    }
    function getStatistics() external view returns (uint256[2 * ArraySize] memory) {
        uint256[2 * ArraySize] memory output;
        for(uint256 i = firstHero; i <= lastHero; i++) {
            output[i] = betAmount[i];
            output[i + ArraySize] = playerCount[i];
        }
        return output;
    }
    function getPlayerStatistics(address _player) external view returns (uint256[ArraySize] memory) {
        uint256[ArraySize] memory output;
        for(uint256 i = firstHero; i <= lastHero; i++) {
            output[i] = bets[_player][i];
        }
        return output;
    }
    function endBetPeriod() external onlySiths {
        endBetting = true;
    }
    function setResult(uint32 _result) external onlySiths {
        require(_result >=  firstHero || _result <= lastHero);
        require(startPayment == false);
        if (betAmount[_result] == 0) {
            startWithdraw();
            return;
        }
        uint256 donation = (address(this).balance - betAmount[_result]) / 10;
        Martin.transfer(donation / 2);
        George.transfer(donation / 2);
        uint256 totalBets = (address(this).balance - betAmount[_result]);
        winRatio = totalBets * RR / betAmount[_result];
        resultWin = _result;
        startPayment = true;
        if (endBetting != true) {
            endBetting = true;
        }
    }
    function startWithdraw() public onlySiths {
        require(startPayment == false);
        startPayment = true;
        if (endBetting != true) {
            endBetting = true;
        }
        if (resultWin != Withdraw) {
            resultWin = Withdraw;
        }
    }
    function pauseOn() external onlySiths {
        onPause = true;
    }
    function pauseOff() external onlySiths {
        onPause = false;
    }
    function clearBlockchain() external {
        require(startPayment && endBetting);
        if (resultWin == Withdraw) {
            require(address(this).balance < minBet);
            selfdestruct(msg.sender);
        } else {
            require(playerCount[resultWin] == 0);
            selfdestruct(msg.sender);
        }
    }
    function addSith(address _sith) external onlySiths {
        sith[_sith] = true;
        sithCount++;
    }
    function delSith(address _sith) external onlySiths {
        require(sithCount >= 2);
        sith[_sith] = false;
        sithCount--;
    }
}
```

## RQ1_5ee0702dae51

SHA-256 `db91098d3e406328af61b0839fe9bda6b0f789608cd34ad859c38b4f92f497a7`

```solidity
pragma solidity ^0.4.24;
contract Token{
    uint256 public totalSupply;
    function balanceOf(address _owner) public constant returns (uint256 balance);
    function transfer(address _to, uint256 _value) public returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) public returns   
    (bool success);
    function approve(address _spender, uint256 _value) public returns (bool success);
    function allowance(address _owner, address _spender) public constant returns 
    (uint256 remaining);
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 
    _value);
}
contract SnailToken is Token {
    string public name="SnailToken";                   
    uint8 public decimals=18;              
    string public symbol="Snail";         
    address public organizer=0x06BB7b2E393671b85624128A5475bE4A8c1c03E9;
    function SnailToken(uint256 _initialAmount, string _tokenName, uint8 _decimalUnits, string _tokenSymbol) public {
        totalSupply = _initialAmount * 10 ** uint256(_decimalUnits);       
        balances[msg.sender] = totalSupply; 
        name = _tokenName;                   
        decimals = _decimalUnits;          
        symbol = _tokenSymbol;
    }
    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balances[msg.sender] >= _value && balances[_to] + _value > balances[_to]);
        require(_to != 0x0);
        balances[msg.sender] -= _value;
        balances[_to] += _value;
        Transfer(msg.sender, _to, _value);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _value) public returns 
    (bool success) {
        require(balances[_from] >= _value && allowed[_from][msg.sender] >= _value);
        balances[_to] += _value;
        balances[_from] -= _value; 
        allowed[_from][msg.sender] -= _value;
        Transfer(_from, _to, _value);
        return true;
    }
    function balanceOf(address _owner) public constant returns (uint256 balance) {
        return balances[_owner];
    }
    function approve(address _spender, uint256 _value) public returns (bool success)   
    { 
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) public constant returns (uint256 remaining) {
        return allowed[_owner][_spender];
    }
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    function takeout(uint256 amount) public{
    require(address(this).balance>=amount*10**18);
    transfer(address(this),amount);
    msg.sender.transfer(amount*10**18);
    }
    function destroy() public{
      selfdestruct(organizer);}
}

```

## RQ1_5a5b1c1896e1

SHA-256 `955bcf49492c4817b3b8191105e00adeb8ad8982e24b26c7d2e2ac7f93cde5af`

```solidity
pragma solidity ^0.4.22;
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
    function distr(address _to, uint256 _value) external returns (bool);
    function totalSupply() constant external returns (uint256 supply);
    function balanceOf(address _owner) constant external returns (uint256 balance);
}
contract SACO is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "Sachio";
    string public constant symbol = "SCH";
    uint public constant decimals = 18;
    uint256 public totalSupply = 2700000000e18;
    uint256 public totalDistributed = 500000000e18;
    uint256 public totalRemaining = totalSupply.sub(totalDistributed);
    uint256 public value = 7000e18;
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
    function SAC() public {
        owner = msg.sender;
        balances[owner] = totalDistributed;
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
        totalRemaining = totalRemaining.sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Distr(_to, _amount);
        emit Transfer(address(0), _to, _amount);
        return true;
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
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
        uint256 etherBalance = address(this).balance;
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

## RQ1_293812debd13

SHA-256 `a1ef303fcafccb75595444a941aa17bf3b063b80610bce0e688b4a6f59cbd0a1`

```solidity
pragma solidity ^0.4.24;
interface KittyCore {
    function ownerOf (uint256 _tokenId) external view returns (address owner);
    function getKitty (uint256 _id) external view returns (bool isGestating, bool isReady, uint256 cooldownIndex, uint256 nextActionAt, uint256 siringWithId, uint256 birthTime, uint256 matronId, uint256 sireId, uint256 generation, uint256 genes);
}
interface SaleClockAuction {
    function getCurrentPrice (uint256 _tokenId) external view returns (uint256);
    function getAuction (uint256 _tokenId) external view returns (address seller, uint256 startingPrice, uint256 endingPrice, uint256 duration, uint256 startedAt);
}
contract ERC721 {
    function totalSupply() public view returns (uint256 total);
    function balanceOf(address _owner) public view returns (uint256 balance);
    function ownerOf(uint256 _tokenId) external view returns (address owner);
    function approve(address _to, uint256 _tokenId) external;
    function transfer(address _to, uint256 _tokenId) external;
    function transferFrom(address _from, address _to, uint256 _tokenId) external;
    function allowance(address _owner, address _spender) view returns (uint remaining);
    function takeOwnership(uint256 _tokenId) external;
    event Transfer(address indexed from, address indexed to, uint256 tokenId);
    event Approval(address indexed owner, address indexed approved, uint256 tokenId);
    function name() public view returns (string);
    function symbol() public view returns (string);
    function supportsInterface(bytes4 _interfaceID) external view returns (bool);
}
contract CryptoSprites is ERC721 {
    address public owner;
    address KittyCoreAddress = 0x06012c8cf97BEaD5deAe237070F9587f8E7A266d;
    address SaleClockAuctionAddress = 0xb1690C08E213a35Ed9bAb7B318DE14420FB57d8C;
    address charityAddress = 0xb30cb3b3E03A508Db2A0a3e07BA1297b47bb0fb1;
    uint public etherForOwner;
    uint public etherForCharity;
    uint public ownerCut = 15; 
    uint public charityCut = 15; 
    uint public featurePrice = 10**16; 
    uint public priceMultiplier = 1;
    uint public priceDivider = 10;
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    function CryptoSprites() {
        owner = msg.sender;
    }
    uint[] public featuredSprites;
    uint[] public allPurchasedSprites;
    uint public totalFeatures;
    uint public totalBuys;
    struct BroughtSprites {
        address owner;
        uint spriteImageID;
        bool forSale;
        uint price;
        uint timesTraded;
        bool featured;
    }
    mapping (uint => BroughtSprites) public broughtSprites;
    mapping (address => uint[]) public spriteOwningHistory;
    mapping (address => uint) public numberOfSpritesOwnedByUser;
    mapping (address => mapping(address => mapping(uint256 => bool))) public addressToReceiverToAllowedSprite;
    mapping (address => mapping(address => uint256)) public addressToReceiverToAmountAllowed;
    bytes4 constant InterfaceSignature_ERC165 = bytes4(keccak256('supportsInterface(bytes4)'));
    bytes4 constant InterfaceSignature_ERC721 =
        bytes4(keccak256('totalSupply()')) ^
        bytes4(keccak256('balanceOf(address)')) ^
        bytes4(keccak256('ownerOf(uint256)')) ^
        bytes4(keccak256('approve(address,uint256)')) ^
        bytes4(keccak256('transfer(address,uint256)')) ^
        bytes4(keccak256('transferFrom(address,address,uint256)'));
    function() payable {
        etherForOwner += msg.value;
    }
    function adjustDefaultSpritePrice (uint _priceMultiplier, uint _priceDivider) onlyOwner {
        require (_priceMultiplier > 0);
        require (_priceDivider > 0);
        priceMultiplier = _priceMultiplier;
        priceDivider = _priceDivider;
    }
    function adjustCut (uint _ownerCut, uint _charityCut) onlyOwner {
        require (_ownerCut + _charityCut < 51); 
        ownerCut = _ownerCut;
        charityCut = _charityCut;
    }
    function adjustFeaturePrice (uint _featurePrice) onlyOwner {
        require (_featurePrice > 0);
        featurePrice = _featurePrice;
    }
    function withdraw() onlyOwner {
        owner.transfer(etherForOwner);
        charityAddress.transfer(etherForCharity);
        etherForOwner = 0;
        etherForCharity = 0;
    }
    function changeOwner (address _owner) onlyOwner {
        owner = _owner;
    }
    function featureSprite (uint spriteId) payable {
        require (msg.value == featurePrice);
        broughtSprites[spriteId].featured = true;
        if (broughtSprites[spriteId].timesTraded == 0) {
            var (kittyOwner,,,,) = SaleClockAuction(SaleClockAuctionAddress).getAuction(spriteId);
            uint priceIfAny = SaleClockAuction(SaleClockAuctionAddress).getCurrentPrice(spriteId);
            address kittyOwnerNotForSale = KittyCore(KittyCoreAddress).ownerOf(spriteId);
            if (priceIfAny > 0 && msg.sender == kittyOwner) {
                broughtSprites[spriteId].price = priceIfAny * priceMultiplier / priceDivider;
                broughtSprites[spriteId].forSale = true;
                broughtSprites[spriteId].owner = kittyOwner;
                numberOfSpritesOwnedByUser[msg.sender]++;
            } else if (kittyOwnerNotForSale == msg.sender) {
                broughtSprites[spriteId].owner = kittyOwnerNotForSale;
                numberOfSpritesOwnedByUser[msg.sender]++;
            }
            broughtSprites[spriteId].spriteImageID = uint(block.blockhash(block.number-1))%360 + 1;
        }
        totalFeatures++;
        etherForOwner += msg.value;
        featuredSprites.push(spriteId);
    }
    function calculatePrice (uint kittyId) view returns (uint) {
        uint priceIfAny = SaleClockAuction(SaleClockAuctionAddress).getCurrentPrice(kittyId);
        var _ownerCut = ((priceIfAny / 1000) * ownerCut) * priceMultiplier / priceDivider;
        var _charityCut = ((priceIfAny / 1000) * charityCut) * priceMultiplier / priceDivider;
        return (priceIfAny * priceMultiplier / priceDivider) + _ownerCut + _charityCut;
    }
    function buySprite (uint spriteId) payable {
        uint _ownerCut;
        uint _charityCut;
        if (broughtSprites[spriteId].forSale == true) {
            _ownerCut = ((broughtSprites[spriteId].price / 1000) * ownerCut);
            _charityCut = ((broughtSprites[spriteId].price / 1000) * charityCut);
            require (msg.value == broughtSprites[spriteId].price + _ownerCut + _charityCut);
            broughtSprites[spriteId].owner.transfer(broughtSprites[spriteId].price);
            numberOfSpritesOwnedByUser[broughtSprites[spriteId].owner]--;
            if (broughtSprites[spriteId].timesTraded == 0) {
                allPurchasedSprites.push(spriteId);
            }
            emit Transfer (broughtSprites[spriteId].owner, msg.sender, spriteId);
        } else {
            require (broughtSprites[spriteId].timesTraded == 0);
            require (broughtSprites[spriteId].price == 0);
            uint priceIfAny = SaleClockAuction(SaleClockAuctionAddress).getCurrentPrice(spriteId);
            require (priceIfAny > 0); 
            _ownerCut = ((priceIfAny / 1000) * ownerCut) * priceMultiplier / priceDivider;
            _charityCut = ((priceIfAny / 1000) * charityCut) * priceMultiplier / priceDivider;
            require (msg.value >= (priceIfAny * priceMultiplier / priceDivider) + _ownerCut + _charityCut);
            var (kittyOwner,,,,) = SaleClockAuction(SaleClockAuctionAddress).getAuction(spriteId);
            kittyOwner.transfer(priceIfAny * priceMultiplier / priceDivider);
            allPurchasedSprites.push(spriteId);
            broughtSprites[spriteId].spriteImageID = uint(block.blockhash(block.number-1))%360 + 1; 
            emit Transfer (kittyOwner, msg.sender, spriteId);
        }
        totalBuys++;
        spriteOwningHistory[msg.sender].push(spriteId);
        numberOfSpritesOwnedByUser[msg.sender]++;
        broughtSprites[spriteId].owner = msg.sender;
        broughtSprites[spriteId].forSale = false;
        broughtSprites[spriteId].timesTraded++;
        broughtSprites[spriteId].featured = false;
        etherForOwner += _ownerCut;
        etherForCharity += _charityCut;
    }
    function listSpriteForSale (uint spriteId, uint price) {
        require (price > 0);
        if (broughtSprites[spriteId].owner != msg.sender) {
            require (broughtSprites[spriteId].timesTraded == 0);
            var (kittyOwner,,,,) = SaleClockAuction(SaleClockAuctionAddress).getAuction(spriteId);
            if (kittyOwner != msg.sender) {
                address kittyOwnerNotForSale = KittyCore(KittyCoreAddress).ownerOf(spriteId);
                require (kittyOwnerNotForSale == msg.sender);
            }
            broughtSprites[spriteId].owner = msg.sender;
            broughtSprites[spriteId].spriteImageID = uint(block.blockhash(block.number-1))%360 + 1; 
        }
        broughtSprites[spriteId].forSale = true;
        broughtSprites[spriteId].price = price;
    }
    function removeSpriteFromSale (uint spriteId) {
        if (broughtSprites[spriteId].owner != msg.sender) {
            require (broughtSprites[spriteId].timesTraded == 0);
            var (kittyOwner,,,,) = SaleClockAuction(SaleClockAuctionAddress).getAuction(spriteId);
            if (kittyOwner != msg.sender) {
                address kittyOwnerNotForSale = KittyCore(KittyCoreAddress).ownerOf(spriteId);
                require (kittyOwnerNotForSale == msg.sender);
            }
            broughtSprites[spriteId].price = 1; 
        } 
        broughtSprites[spriteId].forSale = false;
    }
    function featuredSpritesLength() view external returns (uint) {
        return featuredSprites.length;
    }
    function usersSpriteOwningHistory (address user) view external returns (uint[]) {
        return spriteOwningHistory[user];
    }
    function lookupSprite (uint spriteId) view external returns (address, uint, bool, uint, uint, bool) {
        return (broughtSprites[spriteId].owner, broughtSprites[spriteId].spriteImageID, broughtSprites[spriteId].forSale, broughtSprites[spriteId].price, broughtSprites[spriteId].timesTraded, broughtSprites[spriteId].featured);
    }
    function lookupFeaturedSprites (uint _index) view external returns (uint) {
        return featuredSprites[_index];
    }
    function lookupAllSprites (uint _index) view external returns (uint) {
        return allPurchasedSprites[_index];
    }
    function lookupKitty (uint kittyId) view returns (address, uint, address) {
        var (kittyOwner,,,,) = SaleClockAuction(SaleClockAuctionAddress).getAuction(kittyId);
        uint priceIfAny = SaleClockAuction(SaleClockAuctionAddress).getCurrentPrice(kittyId);
        address kittyOwnerNotForSale = KittyCore(KittyCoreAddress).ownerOf(kittyId);
        return (kittyOwner, priceIfAny, kittyOwnerNotForSale);
    }
    function lookupKittyDetails1 (uint kittyId) view returns (bool, bool, uint, uint, uint) {
        var (isGestating, isReady, cooldownIndex, nextActionAt, siringWithId,,,,,) = KittyCore(KittyCoreAddress).getKitty(kittyId);
        return (isGestating, isReady, cooldownIndex, nextActionAt, siringWithId);
    }
    function lookupKittyDetails2 (uint kittyId) view returns (uint, uint, uint, uint, uint) {
        var(,,,,,birthTime, matronId, sireId, generation, genes) = KittyCore(KittyCoreAddress).getKitty(kittyId);
        return (birthTime, matronId, sireId, generation, genes);
    }
    string public name = 'Crypto Sprites';
    string public symbol = 'CRS';
    uint8 public decimals = 0; 
    function name() public view returns (string) {
        return name;
    }
    function symbol() public view returns (string) {
        return symbol;
    }
    function totalSupply() public view returns (uint) {
        return allPurchasedSprites.length;
    }
    function balanceOf (address _owner) public view returns (uint) {
        return numberOfSpritesOwnedByUser[_owner];
    }
    function ownerOf (uint _tokenId) external view returns (address){
        return broughtSprites[_tokenId].owner;
    }
    function approve (address _to, uint256 _tokenId) external {
        require (broughtSprites[_tokenId].owner == msg.sender);
        require (addressToReceiverToAllowedSprite[msg.sender][_to][_tokenId] == false);
        addressToReceiverToAllowedSprite[msg.sender][_to][_tokenId] = true;
        addressToReceiverToAmountAllowed[msg.sender][_to]++;
        Approval (msg.sender, _to, _tokenId);
    }
    function disapprove (address _to, uint256 _tokenId) external {
        require (broughtSprites[_tokenId].owner == msg.sender);
        require (addressToReceiverToAllowedSprite[msg.sender][_to][_tokenId] == true); 
        addressToReceiverToAmountAllowed[msg.sender][_to]--;
        addressToReceiverToAllowedSprite[msg.sender][_to][_tokenId] = false;
    }
    function takeOwnership (uint256 _tokenId) external {
        require (addressToReceiverToAllowedSprite[broughtSprites[_tokenId].owner][msg.sender][_tokenId] == true);
        addressToReceiverToAllowedSprite[broughtSprites[_tokenId].owner][msg.sender][_tokenId] = false;
        addressToReceiverToAmountAllowed[broughtSprites[_tokenId].owner][msg.sender]--;
        numberOfSpritesOwnedByUser[broughtSprites[_tokenId].owner]--;
        numberOfSpritesOwnedByUser[msg.sender]++;
        spriteOwningHistory[msg.sender].push(_tokenId);
        emit Transfer (broughtSprites[_tokenId].owner, msg.sender, _tokenId);
        broughtSprites[_tokenId].owner = msg.sender;
    }
    function transfer (address _to, uint _tokenId) external {
        require (broughtSprites[_tokenId].owner == msg.sender);
        broughtSprites[_tokenId].owner = _to;
        numberOfSpritesOwnedByUser[msg.sender]--;
        numberOfSpritesOwnedByUser[_to]++;
        spriteOwningHistory[_to].push(_tokenId);
        emit Transfer (msg.sender, _to, _tokenId);
    }
    function transferFrom (address _from, address _to, uint256 _tokenId) external {
        require (addressToReceiverToAllowedSprite[_from][msg.sender][_tokenId] == true);
        require (broughtSprites[_tokenId].owner == _from);
        addressToReceiverToAllowedSprite[_from][msg.sender][_tokenId] = false;
        addressToReceiverToAmountAllowed[_from][msg.sender]--;
        numberOfSpritesOwnedByUser[_from]--;
        numberOfSpritesOwnedByUser[_to]++;
        spriteOwningHistory[_to].push(_tokenId);
        broughtSprites[_tokenId].owner = _to;
        emit Transfer (_from, _to, _tokenId);
    }
    function allowance (address _owner, address _spender) view returns (uint) {
        return addressToReceiverToAmountAllowed[_owner][_spender];
    }
    function supportsInterface (bytes4 _interfaceID) external view returns (bool) {
        return ((_interfaceID == InterfaceSignature_ERC165) || (_interfaceID == InterfaceSignature_ERC721));
    }
}

```

## RQ1_52d5c754a744

SHA-256 `bdda92dfb174696c0aa4a729c63c9ca410436612fb07a1eee0ea7401eaed5fd0`

```solidity
pragma solidity ^0.4.24;
contract BlocksureInfo {
    address public owner;
    string public name;
    mapping (string => string) strings;
    function BlocksureInfo() {
        owner = tx.origin;
    }
    modifier onlyowner { if (tx.origin == owner) _; }
    function addString(string _key, string _value) onlyowner {
        strings[_key] = _value;
    }
    function setOwner(address _owner) onlyowner {
        owner = _owner;
    }
    function setName(string _name) onlyowner {
        name = _name;
    }
    function destroy() onlyowner {
        suicide(owner);
    }
}
```

## RQ1_447e629016cc

SHA-256 `7170935cf8c87cae52f7d56664cc1d8c6c8d837ac42427a4c8631c51a0337e05`

```solidity
pragma solidity ^0.4.24;
library safeMath {
  function mul(uint a, uint b) internal returns (uint) {
    uint c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function div(uint a, uint b) internal returns (uint) {
    uint c = a / b;
    return c;
  }
  function sub(uint a, uint b) internal returns (uint) {
    assert(b <= a);
    return a - b;
  }
  function add(uint a, uint b) internal returns (uint) {
    uint c = a + b;
    assert(c >= a);
    return c;
  }
  function max64(uint64 a, uint64 b) internal constant returns (uint64) {
    return a >= b ? a : b;
  }
  function min64(uint64 a, uint64 b) internal constant returns (uint64) {
    return a < b ? a : b;
  }
  function max256(uint256 a, uint256 b) internal constant returns (uint256) {
    return a >= b ? a : b;
  }
  function min256(uint256 a, uint256 b) internal constant returns (uint256) {
    return a < b ? a : b;
  }
}
contract DBC {
    modifier pre_cond(bool condition) {
        require(condition);
        _;
    }
    modifier post_cond(bool condition) {
        _;
        assert(condition);
    }
    modifier invariant(bool condition) {
        require(condition);
        _;
        assert(condition);
    }
}
contract ERC20Interface {
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    function totalSupply() constant returns (uint256 totalSupply) {}
    function balanceOf(address _owner) constant returns (uint256 balance) {}
    function allowance(address _owner, address _spender) constant returns (uint256 remaining) {}
    function transfer(address _to, uint256 _value) returns (bool success) {}
    function transferFrom(address _from, address _to, uint256 _value) returns (bool success) {}
    function approve(address _spender, uint256 _value) returns (bool success) {}
}
contract ERC20 is ERC20Interface {
    function transfer(address _to, uint256 _value) returns (bool success) {
        if (balances[msg.sender] >= _value && balances[_to] + _value > balances[_to]) {
            balances[msg.sender] -= _value;
            balances[_to] += _value;
            Transfer(msg.sender, _to, _value);
            return true;
        } else { throw; }
    }
    function transferFrom(address _from, address _to, uint256 _value) returns (bool success) {
        if (balances[_from] >= _value && allowed[_from][msg.sender] >= _value && balances[_to] + _value > balances[_to]) {
            balances[_to] += _value;
            balances[_from] -= _value;
            allowed[_from][msg.sender] -= _value;
            Transfer(_from, _to, _value);
            return true;
        } else { throw; }
    }
    function balanceOf(address _owner) constant returns (uint256 balance) {
        return balances[_owner];
    }
    function approve(address _spender, uint256 _value) returns (bool success) {
        if (_value > 0) {
            require(allowed[msg.sender][_spender] == 0);
        }
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
contract Vesting is DBC {
    using safeMath for uint;
    ERC20 public MELON_CONTRACT; 
    uint public totalVestedAmount; 
    uint public vestingStartTime; 
    uint public vestingPeriod; 
    address public beneficiary; 
    uint public withdrawn; 
    function isBeneficiary() constant returns (bool) { return msg.sender == beneficiary; }
    function isVestingStarted() constant returns (bool) { return vestingStartTime != 0; }
    function calculateWithdrawable() constant returns (uint withdrawable) {
        uint timePassed = now.sub(vestingStartTime);
        if (timePassed < vestingPeriod) {
            uint vested = totalVestedAmount.mul(timePassed).div(vestingPeriod);
            withdrawable = vested.sub(withdrawn);
        } else {
            withdrawable = totalVestedAmount.sub(withdrawn);
        }
    }
    function Vesting(address ofMelonAsset) {
        MELON_CONTRACT = ERC20(ofMelonAsset);
    }
    function setVesting(address ofBeneficiary, uint ofMelonQuantity, uint ofVestingPeriod)
        pre_cond(!isVestingStarted())
        pre_cond(ofMelonQuantity > 0)
    {
        require(MELON_CONTRACT.transferFrom(msg.sender, this, ofMelonQuantity));
        vestingStartTime = now;
        totalVestedAmount = ofMelonQuantity;
        vestingPeriod = ofVestingPeriod;
        beneficiary = ofBeneficiary;
    }
    function withdraw()
        pre_cond(isBeneficiary())
        pre_cond(isVestingStarted())
    {
        uint withdrawable = calculateWithdrawable();
        withdrawn = withdrawn.add(withdrawable);
        require(MELON_CONTRACT.transfer(beneficiary, withdrawable));
    }
}

```

## RQ1_7534bc78dfc0

SHA-256 `523b038a2bf8b69ab3d6787eefc6460f6aa8e16fe6f9be07c94d5ae63799da5a`

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
  function transferOwnership(address newOwner) public onlyOwner {
    require(newOwner != address(0));
    OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }
}
contract Pausable is Ownable {
  event Pause();
  event Unpause();
  bool public paused = false;
  modifier whenNotPaused() {
    require(!paused || msg.sender == owner);
    _;
  }
  modifier whenPaused() {
    require(paused);
    _;
  }
  function pause() onlyOwner public{
    require(paused == false);
    paused = true;
    Pause();
  }
  function unpause() onlyOwner whenPaused public{
    paused = false;
    Unpause();
  }
}
contract Mortal is Ownable {
    function kill() onlyOwner public {
        selfdestruct(owner);
    }
}
contract UpgradeAgent {
  uint public originalSupply;
  function isUpgradeAgent() public constant returns (bool) {
    return true;
  }
  function upgradeFrom(address _from, uint256 _value) public;
}
contract BaseToken is Ownable, Pausable, Mortal{
  using SafeMath for uint256;
  mapping (address => uint256) public balances;
  mapping (address => mapping (address => uint256)) public allowances;
  mapping (address => bool) public frozenAccount;
  uint256 public totalSupply;
  string public name;
  uint8 public decimals;
  string public symbol;
  string public version;
  event Transfer(address indexed _from, address indexed _to, uint256 _value);
  event Approval(address indexed _owner, address indexed _spender, uint256 _value);
  event FrozenFunds(address target, bool frozen);
  function totalSupply() public constant returns (uint _totalSupply) {
      return totalSupply;
  }
  function balanceOf(address _address) public view returns (uint256 balance) {
    return balances[_address];
  }
  function allowance(address _owner, address _spender) public view returns (uint256 remaining) {
    return allowances[_owner][_spender];
  }
  function freezeAccount(address target, bool freeze) onlyOwner public{
    frozenAccount[target] = freeze;
    FrozenFunds(target, freeze);
    }
  function isFrozen(address _address) public view returns (bool frozen) {
      return frozenAccount[_address];
  }
  function transfer(address _to, uint256 _value) whenNotPaused public returns (bool success)  {
    require(_to != address(0));
    require(_value <= balances[msg.sender]);
    require(!frozenAccount[msg.sender]);
    balances[msg.sender] = balances[msg.sender].sub(_value);
    balances[_to] = balances[_to].add(_value);
    Transfer(msg.sender, _to, _value);
    return true;
  }
  function approve(address _spender, uint256 _value) public returns (bool success) {
    allowances[msg.sender][_spender] = _value;
    Approval(msg.sender, _spender, _value);
    return true;
  }
  function transferFrom(address _owner, address _to, uint256 _value) whenNotPaused public returns (bool success) {
    require(_to != address(0));
    require(_value <= balances[_owner]);
    require(_value <= allowances[_owner][msg.sender]);
    require(!frozenAccount[_owner]);
    balances[_owner] = balances[_owner].sub(_value);
    balances[_to] = balances[_to].add(_value);
    allowances[_owner][msg.sender] = allowances[_owner][msg.sender].sub(_value);
    Transfer(_owner, _to, _value);
    return true;
  }
}
contract UpgradeableToken is BaseToken {
  address public upgradeMaster;
  UpgradeAgent public upgradeAgent;
  uint256 public totalUpgraded;
  enum UpgradeState {Unknown, NotAllowed, WaitingForAgent, ReadyToUpgrade, Upgrading}
  event Upgrade(address indexed _from, address indexed _to, uint256 _value);
  event UpgradeAgentSet(address agent);
  function UpgradeAgentEnabledToken(address _upgradeMaster) {
    upgradeMaster = _upgradeMaster;
  }
  function upgrade(uint256 value) public {
      UpgradeState state = getUpgradeState();
      if(!(state == UpgradeState.ReadyToUpgrade || state == UpgradeState.Upgrading)) {
        revert();
      }
      if (value == 0) revert();
      balances[msg.sender] = balances[msg.sender].sub(value);
      totalSupply = totalSupply.sub(value);
      totalUpgraded = totalUpgraded.add(value);
      upgradeAgent.upgradeFrom(msg.sender, value);
      Upgrade(msg.sender, upgradeAgent, value);
  }
  function setUpgradeAgent(address agent) external {
      if(!canUpgrade()) {
        revert();
      }
      if (agent == 0x0) revert();
      if (msg.sender != upgradeMaster) revert();
      if (getUpgradeState() == UpgradeState.Upgrading) revert();
      upgradeAgent = UpgradeAgent(agent);
      if(!upgradeAgent.isUpgradeAgent()) revert();
      if (upgradeAgent.originalSupply() != totalSupply) revert();
      UpgradeAgentSet(upgradeAgent);
  }
  function getUpgradeState() public constant returns(UpgradeState) {
    if(!canUpgrade()) return UpgradeState.NotAllowed;
    else if(address(upgradeAgent) == 0x00) return UpgradeState.WaitingForAgent;
    else if(totalUpgraded == 0) return UpgradeState.ReadyToUpgrade;
    else return UpgradeState.Upgrading;
  }
  function setUpgradeMaster(address master) public {
      if (master == 0x0) revert();
      if (msg.sender != upgradeMaster) revert();
      upgradeMaster = master;
  }
  function canUpgrade() public constant returns(bool) {
     return true;
  }
}
contract YBKToken is UpgradeableToken {
  string public name;
  string public symbol;
  uint public decimals;
  string public version;
   function YBKToken(string _name, string _symbol, uint _initialSupply, uint _decimals, string _version) public {
     owner = msg.sender;
     upgradeMaster = owner;
     name = _name;
     decimals = _decimals;
     symbol = _symbol;
     version = _version;
     totalSupply = _initialSupply;
     balances[msg.sender] = totalSupply;
   }
}
```

## RQ1_f1e26706fa55

SHA-256 `116bbdcad9f43eb6bf58171134622ea155de2a4fa9d96bfe45c485c45843e599`

```solidity
pragma solidity ^0.5.0;
contract UserProxy {
    function execute(address _target, bytes memory _data) public payable returns (bytes memory response) {
        require(_target != address(0), "user-proxy-target-address-required");
        assembly {
            let succeeded := delegatecall(sub(gas, 5000), _target, add(_data, 0x20), mload(_data), 0, 0)
            let size := returndatasize
            response := mload(0x40)
            mstore(0x40, add(response, and(add(add(size, 0x20), 0x1f), not(0x1f))))
            mstore(response, size)
            returndatacopy(add(response, 0x20), 0, size)
            switch iszero(succeeded)
                case 1 {
                    revert(add(response, 0x20), size)
                }
        }
    }
}
```

## RQ1_5e152e91f401

SHA-256 `1215473ff419e399fcf401daf86af9b2f51a226b298787986e82218c7fd6adf0`

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
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) public; }
contract BasicToken {
    using SafeMath for uint256;
    string public name = 'eZWay';
    string public symbol = 'EZW';
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);
    function BasicToken() public {
        totalSupply = 100000000 * (10 ** uint256(decimals));
        balanceOf[this] = totalSupply;
        allowance[this][msg.sender] = totalSupply;
    }
    function _transfer(address _from, address _to, uint _value) internal {
        require(_to != 0x0);
        balanceOf[_from] = balanceOf[_from].sub(_value);
        balanceOf[_to] = balanceOf[_to].add(_value);
        Transfer(_from, _to, _value);
    }
    function transfer(address _to, uint256 _value) public {
        _transfer(msg.sender, _to, _value);
    }
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        allowance[_from][msg.sender] = allowance[_from][msg.sender].sub(_value);
        _transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        return true;
    }
    function approveAndCall(address _spender, uint256 _value, bytes _extraData) public returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        if (approve(_spender, _value)) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }
    function burn(uint256 _value) public returns (bool success) {
        balanceOf[msg.sender] = balanceOf[msg.sender].sub(_value);
        totalSupply = totalSupply.sub(_value);
        Burn(msg.sender, _value);
        return true;
    }
    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        balanceOf[_from] = balanceOf[_from].sub(_value);
        allowance[_from][msg.sender] = allowance[_from][msg.sender].sub(_value);
        totalSupply = totalSupply.sub(_value);
        Burn(_from, _value);
        return true;
    }
}
contract eZWay is owned, BasicToken {
    uint256 public tokensPerEther;
    mapping (address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
    function eZWay() public {
        tokensPerEther = 10000;
    }
    function _transfer(address _from, address _to, uint _value) internal {
        require (_to != 0x0);
        require(!frozenAccount[_from]);
        require(!frozenAccount[_to]);
        balanceOf[_from] = balanceOf[_from].sub(_value);
        balanceOf[_to] = balanceOf[_to].add(_value);
        Transfer(_from, _to, _value);
    }
    function mintToken(address target, uint256 mintedAmount) onlyOwner public {
        balanceOf[target] = balanceOf[target].add(mintedAmount);
        totalSupply = totalSupply.add(mintedAmount);
        Transfer(0, this, mintedAmount);
        Transfer(this, target, mintedAmount);
    }
    function freezeAccount(address target, bool freeze) onlyOwner public {
        frozenAccount[target] = freeze;
        FrozenFunds(target, freeze);
    }
    function setPrices(uint256 newRate) onlyOwner public {
        tokensPerEther = newRate;     
    }
    function buy() payable public {
        uint amount = msg.value.mul(tokensPerEther);
        _transfer(this, msg.sender, amount);
        require(owner.send(msg.value));
    }
    function giveBlockReward() public {
        balanceOf[block.coinbase] = balanceOf[block.coinbase].add(10 ** uint256(decimals)); 
        totalSupply = totalSupply.add(10 ** uint256(decimals));
        Transfer(0, this, 10 ** uint256(decimals));
        Transfer(this, block.coinbase, 10 ** uint256(decimals));
    }
    function () payable public {
        buy();
    }
}
```

## RQ1_e3be5dad4539

SHA-256 `dbe5c4783a7c3b8796fda3cd16b6c17e007b6838c1fa6095ce96c14857dce98a`

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
contract NEXUS is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "NEXUS";
    string public constant symbol = "NXS";
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
    function nexus () public {
        owner = msg.sender;
        uint256 devTokens = 2000000000e8;
        distr(owner, devTokens);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = false;
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

## RQ1_1ca2e002ea0d

SHA-256 `86ae4dbc63b040308990ce55ab8b1d507b1dc17cdbfd8ad2a6717ced2c5036c0`

```solidity
pragma solidity ^0.4.18;
contract Token {
    function balanceOf(address _account) public constant returns (uint256 balance);
    function transfer(address _to, uint256 _value) public returns (bool success);
}
contract ABC {
    string public constant symbol = "ABC";
    string public constant name = "Airdrop Beggars Community";
    uint public constant decimals = 18;
    uint public constant totalSupply = 10000000 * 10 ** decimals;
    address public owner;
    mapping (address => bool) beggars;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    function AirdropBeggarsCommunity() public {
        owner = msg.sender;
        balances[owner] = totalSupply;
    }
    function() public payable {
        uint reward = totalSupply / 10000;
        require(balances[owner] >= reward && !beggars[msg.sender]);
        balances[owner] -= reward;
        balances[msg.sender] += reward;
        beggars[msg.sender] = true;
    }
    function balanceOf(address _owner) public constant returns (uint256 balance) {
        return balances[_owner];
    }
    function allowance(address _owner, address _spender) public constant returns (uint256 remaining) {
        return allowed[_owner][_spender];
    }
    function transfer(address _to, uint256 _amount) public returns (bool success) {
        require(balances[msg.sender] >= _amount && _amount > 0);
        balances[msg.sender] -= _amount;
        balances[_to] += _amount;
        Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) public returns (bool success) {
        require(balances[_from] >= _amount && allowed[_from][msg.sender] >= _amount && _amount > 0);
        balances[_from] -= _amount;
        allowed[_from][msg.sender] -= _amount;
        balances[_to] += _amount;
        Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _amount) public returns (bool success) {
        allowed[msg.sender][_spender] = _amount;
        Approval(msg.sender, _spender, _amount);
        return true;
    }
    function withdraw(address _token) public returns (bool _status) {
        require(msg.sender == owner);
        if (_token == address(0)) {
            owner.transfer(this.balance);
        }
        else {
            Token ERC20 = Token(_token);
            ERC20.transfer(owner, ERC20.balanceOf(this));
        }
        return true;
    }
}
```

## RQ1_769d4c77c6c6

SHA-256 `83baf3b2c2911a9a123e870cd85e6de64bddbded2c6bc3746578e87ca51d7b7f`

```solidity
pragma solidity ^0.4.17;
contract ERC20 {
    uint public totalSupply;
    function balanceOf(address who) public constant returns (uint);
    function allowance(address owner, address spender) public constant returns (uint);
    function transfer(address to, uint value) public returns (bool ok);
    function transferFrom(address from, address to, uint value) public returns (bool ok);
    function approve(address spender, uint value) public returns (bool ok);
    event Transfer(address indexed from, address indexed to, uint value);
    event Approval(address indexed owner, address indexed spender, uint value);
}
contract Authority {
    function isValidAuthority(address authorityAddress, uint blockNumber) public view returns (bool);
}
contract SafeMath {
    function safeSub(uint a, uint b) pure internal returns (uint) {
        sAssert(b <= a);
        return a - b;
    }
    function safeAdd(uint a, uint b) pure internal returns (uint) {
        uint c = a + b;
        sAssert(c>=a && c>=b);
        return c;
    }
    function sAssert(bool assertion) pure internal {
        if (!assertion) {
            revert();
        }
    }
}
contract SingleSourceIdentity is SafeMath {
    struct KYC {
        bool verified;
        address verifiedBy;
        uint verifiedAt;
        uint verifiedAttributes;
    }
    uint public verificationFee;
    mapping(address => uint) public verificationFeeBalances;
    address public owner;
    address public authorityContractAddress;
    address public paymentContractAddress;
    mapping(address => KYC) public records;
    modifier onlyOwner() {
        if (msg.sender != owner) {
            revert();
        }
        _;
    }
    modifier onlyValidAuthority(address authorityAddress) {
        if (!isValidAuthority(authorityAddress)) {
            revert();
        }
        _;
    }
    modifier onlyAuthoritativeAuthority(address authorityAddress, address userAddress) {
        KYC storage kycRecord = records[userAddress];
        if (kycRecord.verifiedBy != 0x0 && kycRecord.verifiedBy != authorityAddress) {
            if (isValidAuthority(kycRecord.verifiedBy)) {
                revert();
            }
        }
        _;
    }
    function isValidAuthority(address authorityAddress)
      private
      view
      returns (bool)
    {
        Authority authority = Authority(authorityContractAddress);
        return authority.isValidAuthority(authorityAddress, block.number);
    }
    function chargeVerificationFee(address userAddress, address authorityAddress)
      private
      returns (bool)
    {
        if (!ERC20(paymentContractAddress).transferFrom(userAddress, this, verificationFee)) {
            return false;
        }
        uint currentBalance = verificationFeeBalances[authorityAddress];
        verificationFeeBalances[authorityAddress] = safeAdd(currentBalance, verificationFee);
        return true;
    }
    function SingleSourceIdentity()
      public
    {
        owner = msg.sender;
        verificationFee = 0 ether;
    }
    function setAuthorityContractAddress(address contractAddress)
      public
      onlyOwner()
    {
        authorityContractAddress = contractAddress;
    }
    function setPaymentContractAddress(address contractAddress)
      public
      onlyOwner()
    {
        paymentContractAddress = contractAddress;
    }
    function setFee(uint fee)
      public
      onlyOwner()
    {
        verificationFee = fee;
    }
    function changeOwner(address newOwner)
      public
      onlyOwner()
    {
        owner = newOwner;
    }
    function withdrawFee()
      public
      onlyValidAuthority(msg.sender)
    {
        require(paymentContractAddress != 0x0);
        uint balance = verificationFeeBalances[msg.sender];
        require(balance > 0);
        verificationFeeBalances[msg.sender] = 0;
        if (!ERC20(paymentContractAddress).transfer(msg.sender, balance)) {
            revert();
        }
    }
    function hasValidProfile(address userAddress)
      public
      view
      returns (bool)
    {
        KYC storage kyc = records[userAddress];
        if (kyc.verified) {
            Authority authority = Authority(authorityContractAddress);
            if (!authority.isValidAuthority(kyc.verifiedBy, kyc.verifiedAt)) {
                return false;
            } else {
                return true;
            }
        } else {
            return false;
        }
    }
    function hasVerifiedAttributeIndex(address userAddress, uint attributeIndex)
      public
      view
      returns (bool)
    {
        if (!this.hasValidProfile(userAddress)) {
            return false;
        } else {
            KYC storage kyc = records[userAddress];
            uint attributeValue = 2 ** attributeIndex;
            return ((kyc.verifiedAttributes & attributeValue) == attributeValue);
        }
    }
    function hasVerifiedAttributeValue(address userAddress, uint attributeValue)
      public
      view
      returns (bool)
    {
        if (!this.hasValidProfile(userAddress)) {
            return false;
        } else {
            KYC storage kyc = records[userAddress];
            return ((kyc.verifiedAttributes & attributeValue) == attributeValue);
        }
    }
    function verifiedAttributes(address userAddress)
      public
      view
      returns (uint)
    {
        if (!this.hasValidProfile(userAddress)) {
            return 0;
        } else {
            KYC storage kyc = records[userAddress];
            return kyc.verifiedAttributes;
        }
    }
    function claim(address verifier, uint verifiedAttributes, uint expires, uint8 v, bytes32 r, bytes32 s)
      public
      onlyValidAuthority(verifier)
      onlyAuthoritativeAuthority(verifier, msg.sender)
    {
        if (verificationFee > 0) {
            if(!chargeVerificationFee(msg.sender, verifier)) {
                revert();
            }
        }
        bytes32 hash = sha256(this, msg.sender, verifiedAttributes, expires);
        bytes memory prefix = "\x19Ethereum Signed Message:\n32";
        bytes32 prefixedHash = keccak256(prefix, hash);
        if (!((ecrecover(prefixedHash, v, r, s) == verifier) && block.number <= expires)) {
            revert();
        }
        KYC memory kyc = KYC({
            verified: true,
            verifiedBy: verifier,
            verifiedAt: block.number,
            verifiedAttributes: verifiedAttributes
        });
        records[msg.sender] = kyc;
    }
    function approve(address userAddress, uint verifiedAttributes)
      public
      onlyValidAuthority(msg.sender)
      onlyAuthoritativeAuthority(msg.sender, userAddress)
    {
        KYC memory kyc = KYC({
            verified: true,
            verifiedBy: msg.sender,
            verifiedAt: block.number,
            verifiedAttributes: verifiedAttributes
        });
        records[userAddress] = kyc;
    }
    function revoke(address userAddress)
      public
      onlyValidAuthority(msg.sender)
      onlyAuthoritativeAuthority(msg.sender, userAddress)
    {
        KYC memory kyc = KYC({
            verified: false,
            verifiedBy: msg.sender,
            verifiedAt: block.number,
            verifiedAttributes: 0
        });
        records[userAddress] = kyc;
    }
}
```

## RQ1_a41242596bec

SHA-256 `452abdda122ed0d3b56640d4266997b37b67900fd46e732008313296278c20bb`

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
contract CryptoCupVirtualMatch {
    event MatchCreated(uint256 indexed id, uint256 playerEntryPrice, uint256 homeTeam, uint256 awayTeam, uint256 kickOff, uint256 fullTime);
    event MatchFinished(uint256 indexed id, uint256 homeTeam, uint256 awayTeam, uint256 winningTeam, uint256 teamAllocation);
    event PlayerJoined(uint256 indexed id, uint256 team, string playerName, address account);
    event TeamOwnerPaid(uint256 indexed id, uint256 amount);
    CryptoCupToken cryptoCupTokenContract;
    address public contractModifierAddress;
    address public developerAddress;
    mapping (uint256 => Match) public matches;
    mapping (address => Player) public players;
    mapping (uint256 => Team) public teams;
    uint256 private developerBalance;
    bool private allowInPlayJoining = true;
    bool private allowPublicMatches = true;
    uint256 private entryPrice = 0.05 ether; 
    uint256 private startInSeconds = 300;
    uint256 private durationInSeconds = 120;
    uint256 private dataVisibleWindow = 21600; 
    uint256 private matchCounter;
    uint256 private playerCounter;
    uint256 private teamCounter;
    bool private commentating = false;
    struct Match {
        uint256 id;
        uint256 playerEntryPrice;
        uint256 homeTeam;
        mapping (uint256 => Player) homeTeamPlayers;
        uint256 homeTeamPlayersCount;
        uint256 awayTeam;
        mapping (uint256 => Player) awayTeamPlayers;
        uint256 awayTeamPlayersCount;
        uint256 kickOff;
        uint256 fullTime;
        uint256 prize;
        uint256 homeScore;
        uint256 awayScore;
        uint256 winningTeam;
        uint256 winningTeamBonus;
        bool reported;
    }
    struct Player {
        uint256 id;
        string name;
        address account;
        uint256 balance;
    }
    struct Team {
        uint256 id;
        address owner;
        uint256 balance;
        bool init;
    }
    modifier onlyContractModifier() {
        require(msg.sender == contractModifierAddress);
        _;
    }
    constructor() public {
        contractModifierAddress = msg.sender;
        developerAddress = msg.sender;
    }
	function destroy() public onlyContractModifier {
		selfdestruct(contractModifierAddress);
    }
    function setDeveloper(address _newDeveloperAddress) public onlyContractModifier {
        require(_newDeveloperAddress != address(0));
        developerAddress = _newDeveloperAddress;
    }
    function setCryptoCupTokenContractAddress(address _cryptoCupTokenAddress) public onlyContractModifier {
        cryptoCupTokenContract = CryptoCupToken(_cryptoCupTokenAddress);
    }
    function togglePublicMatches() public onlyContractModifier {
        allowPublicMatches = !allowPublicMatches;
    }
    function toggleInPlayJoining() public onlyContractModifier {
        allowInPlayJoining = !allowInPlayJoining;
    }
    function toggleMatchStartEnd(uint256 _startInSeconds, uint256 _durationInSeconds) public onlyContractModifier {
        startInSeconds = _startInSeconds;
        durationInSeconds = _durationInSeconds;
    }
    function toggleDataViewWindow(uint256 _periodInSeconds) public onlyContractModifier {
        dataVisibleWindow = _periodInSeconds;
    }
    function doubleEntryPrice() public onlyContractModifier {
        entryPrice = SafeMath.mul(entryPrice,2);
    }
    function halveEntryPrice() public onlyContractModifier {
        entryPrice = SafeMath.div(entryPrice,2);
    }
    function developerPrizeClaim() public onlyContractModifier {
        developerAddress.transfer(developerBalance);
        developerBalance = 0;
    }
    function getBalance()  public constant returns(uint256) {
        return address(this).balance;
    }
    function getTotalMatches() public constant returns(uint256) {
        return matchCounter;
    }
    function getTotalPlayers() public constant returns(uint256) {
        return playerCounter;
    }
    function getCryptoCupTokenContractAddress() public view returns (address contractAddress) {
        return cryptoCupTokenContract;
    }
    function getTeamOwner(uint256 _tokenId) public view returns(address owner)
    {
        owner = cryptoCupTokenContract.ownerOf(_tokenId);
    }
    function getEntryPrice() public constant returns(uint256) {
        return entryPrice;
    }
    function createPlayerMatch(uint256 _homeTeam, uint256 _awayTeam, uint256 _entryPrice, uint256 _startInSecondsTime, uint256 _matchDuration) public {
        require(allowPublicMatches);
        require(_homeTeam != _awayTeam);
        require(_homeTeam < 32 && _awayTeam < 32);
        require(_entryPrice >= entryPrice);
        require(_startInSecondsTime > 0);
        require(_matchDuration >= durationInSeconds);
        if (!teams[_homeTeam].init) {
            teams[_homeTeam] = Team(_homeTeam, cryptoCupTokenContract.ownerOf(_homeTeam), 0, true);
        }
        if (!teams[_awayTeam].init) {
            teams[_awayTeam] = Team(_awayTeam, cryptoCupTokenContract.ownerOf(_awayTeam), 0, true);
        }
        require(teams[_homeTeam].owner == msg.sender || teams[_awayTeam].owner == msg.sender);
        uint256 _kickOff = now + _startInSecondsTime;
        uint256 _fullTime = _kickOff + _matchDuration;
        matchCounter++;
        matches[matchCounter] = Match(matchCounter, _entryPrice, _homeTeam, 0, _awayTeam, 0, _kickOff, _fullTime, 0, 0, 0, 0, 0, false);
        emit MatchCreated(matchCounter, entryPrice, _homeTeam, _awayTeam, _kickOff, _fullTime);
    }
    function createMatch(uint256 _homeTeam, uint256 _awayTeam) public onlyContractModifier {
        require(_homeTeam != _awayTeam);
        if (!teams[_homeTeam].init) {
            teams[_homeTeam] = Team(_homeTeam, cryptoCupTokenContract.ownerOf(_homeTeam), 0, true);
        }
        if (!teams[_awayTeam].init) {
            teams[_awayTeam] = Team(_awayTeam, cryptoCupTokenContract.ownerOf(_awayTeam), 0, true);
        }
        uint256 _kickOff = now + startInSeconds;
        uint256 _fullTime = _kickOff + durationInSeconds;
        matchCounter++;
        matches[matchCounter] = Match(matchCounter, entryPrice, _homeTeam, 0, _awayTeam, 0, _kickOff, _fullTime, 0, 0, 0, 0, 0, false);
        emit MatchCreated(matchCounter, entryPrice, _homeTeam, _awayTeam, _kickOff, _fullTime);
    }
    function joinMatch(uint256 _matchId, uint256 _team, string _playerName) public payable {
        if (players[msg.sender].id == 0) {
            players[msg.sender] = Player(playerCounter++, _playerName, msg.sender, 0);
        } else {
            players[msg.sender].name = _playerName;
        }
        Match storage theMatch = matches[_matchId];
        require(theMatch.id != 0); 
        require(msg.value >= theMatch.playerEntryPrice);
	    require(_addressNotNull(msg.sender));
        if (allowInPlayJoining) {
            require(now < theMatch.fullTime);    
        } else {
            require(now < theMatch.kickOff);
        }
        if (theMatch.homeTeam == _team)
        {
            require(theMatch.homeTeamPlayersCount < 11);
            theMatch.homeTeamPlayers[theMatch.homeTeamPlayersCount++] = players[msg.sender];
        } else {
            require(theMatch.awayTeamPlayersCount < 11);
            theMatch.awayTeamPlayers[theMatch.awayTeamPlayersCount++] = players[msg.sender];
        }
        theMatch.prize += theMatch.playerEntryPrice;
        uint256 purchaseExcess = SafeMath.sub(msg.value, theMatch.playerEntryPrice);
	    msg.sender.transfer(purchaseExcess);
        emit PlayerJoined(_matchId, _team, players[msg.sender].name, msg.sender);
    }
    function getMatchHomePlayers(uint256 matchId) public constant returns(address[]) {
        if(matchCounter == 0) {
            return new address[](0x0);
        }
        address[] memory matchPlayers = new address[](matches[matchId].homeTeamPlayersCount);
        for (uint256 i = 0; i < matches[matchId].homeTeamPlayersCount; i++) {
            matchPlayers[i] =  matches[matchId].homeTeamPlayers[i].account;
        }
        return (matchPlayers);
    }
    function getMatchAwayPlayers(uint256 matchId) public constant returns(address[]) {
        if(matchCounter == 0) {
            return new address[](0x0);
        }
        address[] memory matchPlayers = new address[](matches[matchId].awayTeamPlayersCount);
        for (uint256 i = 0; i < matches[matchId].awayTeamPlayersCount; i++) {
            matchPlayers[i] =  matches[matchId].awayTeamPlayers[i].account;
        }
        return (matchPlayers);
    }
    function getFixtures() public constant returns(uint256[]) {
        if(matchCounter == 0) {
            return new uint[](0);
        }
        uint256[] memory matchIds = new uint256[](matchCounter);
        uint256 numberOfMatches = 0;
        for (uint256 i = 1; i <= matchCounter; i++) {
            if (now < matches[i].kickOff) {
                matchIds[numberOfMatches] = matches[i].id;
                numberOfMatches++;
            }
        }
        uint[] memory smallerArray = new uint[](numberOfMatches);
        for (uint j = 0; j < numberOfMatches; j++) {
            smallerArray[j] = matchIds[j];
        }
        return (smallerArray);
    }
    function getInPlayGames() public constant returns(uint256[]) {
        if(matchCounter == 0) {
            return new uint[](0);
        }
        uint256[] memory matchIds = new uint256[](matchCounter);
        uint256 numberOfMatches = 0;
        for (uint256 i = 1; i <= matchCounter; i++) {
            if (now > matches[i].kickOff && now < matches[i].fullTime) {
                matchIds[numberOfMatches] = matches[i].id;
                numberOfMatches++;
            }
        }
        uint[] memory smallerArray = new uint[](numberOfMatches);
        for (uint j = 0; j < numberOfMatches; j++) {
            smallerArray[j] = matchIds[j];
        }
        return (smallerArray);
    }
    function getUnReportedMatches() public constant returns(uint256[]) {
        if(matchCounter == 0) {
            return new uint[](0);
        }
        uint256[] memory matchIds = new uint256[](matchCounter);
        uint256 numberOfMatches = 0;
        for (uint256 i = 1; i <= matchCounter; i++) {
            if (!matches[i].reported && now > matches[i].fullTime && (matches[i].homeTeamPlayersCount + matches[i].awayTeamPlayersCount) > 0) {
                matchIds[numberOfMatches] = matches[i].id;
                numberOfMatches++;
            }
        }
        uint[] memory smallerArray = new uint[](numberOfMatches);
        for (uint j = 0; j < numberOfMatches; j++) {
            smallerArray[j] = matchIds[j];
        }
        return (smallerArray);
    }
    function getMatchReport(uint256 _matchId) public {
        Match storage theMatch = matches[_matchId];
        require(theMatch.id > 0 && !theMatch.reported);
        uint256 index;
        if (theMatch.homeTeamPlayersCount == 0 || theMatch.awayTeamPlayersCount == 0)
        {
            for (index = 0; index < theMatch.homeTeamPlayersCount; index++) {
                players[theMatch.homeTeamPlayers[index].account].balance += theMatch.playerEntryPrice;
            }
            for (index = 0; index < theMatch.awayTeamPlayersCount; index++) {
                players[theMatch.awayTeamPlayers[index].account].balance += theMatch.playerEntryPrice;
            }
        } else {
            uint256 htpBalance = 0;
            for (index = 0; index < theMatch.homeTeamPlayersCount; index++) {
               htpBalance += theMatch.homeTeamPlayers[index].account.balance;
            }
            uint256 atpBalance = 0;
            for (index = 0; index < theMatch.awayTeamPlayersCount; index++) {
               atpBalance += theMatch.awayTeamPlayers[index].account.balance;
            }
            theMatch.homeScore = htpBalance % 5;
            theMatch.awayScore = atpBalance % 5;
            if (theMatch.homeScore == theMatch.awayScore)
            {
                if(block.timestamp % 2 == 0){
                  theMatch.homeScore += 1;
                } else {
                  theMatch.awayScore += 1;
                }
            }
            uint256 prizeMoney = 0;
            if(theMatch.homeScore > theMatch.awayScore){
              theMatch.winningTeam = theMatch.homeTeam;
              prizeMoney = SafeMath.mul(theMatch.playerEntryPrice, theMatch.awayTeamPlayersCount);
            } else {
              theMatch.winningTeam = theMatch.awayTeam;
              prizeMoney = SafeMath.mul(theMatch.playerEntryPrice, theMatch.homeTeamPlayersCount);
            }
    	    uint256 onePercent = SafeMath.div(prizeMoney, 100);
            uint256 developerAllocation = SafeMath.mul(onePercent, 1);
            uint256 teamOwnerAllocation = SafeMath.mul(onePercent, 9);
            uint256 playersProfit = SafeMath.mul(onePercent, 90);
            uint256 playersProfitShare = 0;
            if (theMatch.winningTeam == theMatch.homeTeam)
            {
                playersProfitShare = SafeMath.add(SafeMath.div(playersProfit, theMatch.homeTeamPlayersCount), theMatch.playerEntryPrice);
                for (index = 0; index < theMatch.homeTeamPlayersCount; index++) {
                    players[theMatch.homeTeamPlayers[index].account].balance += playersProfitShare;
                }
            } else {
                playersProfitShare = SafeMath.add(SafeMath.div(playersProfit, theMatch.awayTeamPlayersCount), theMatch.playerEntryPrice);
                for (index = 0; index < theMatch.awayTeamPlayersCount; index++) {
                    players[theMatch.awayTeamPlayers[index].account].balance += playersProfitShare;
                }
            }
            teams[theMatch.winningTeam].balance += teamOwnerAllocation;
            theMatch.winningTeamBonus = teamOwnerAllocation;
	        developerBalance += developerAllocation;
            emit MatchFinished(theMatch.id, theMatch.homeTeam, theMatch.awayTeam, theMatch.winningTeam, teamOwnerAllocation);
        }
        theMatch.reported = true;
    }
    function getReportedMatches() public constant returns(uint256[]) {
        if(matchCounter == 0) {
            return new uint[](0);
        }
        uint256[] memory matchIds = new uint256[](matchCounter);
        uint256 numberOfMatches = 0;
        for (uint256 i = 1; i <= matchCounter; i++) {
            if (matches[i].reported && now > matches[i].fullTime && matches[i].fullTime + dataVisibleWindow > now) {
                matchIds[numberOfMatches] = matches[i].id;
                numberOfMatches++;
            }
        }
        uint[] memory smallerArray = new uint[](numberOfMatches);
        for (uint j = 0; j < numberOfMatches; j++) {
            smallerArray[j] = matchIds[j];
        }
        return (smallerArray);
    }
    function playerPrizeClaim() public {
        require(_addressNotNull(msg.sender));
        require(players[msg.sender].account != address(0));
        msg.sender.transfer(players[msg.sender].balance);
        players[msg.sender].balance = 0;
    }
    function teamPrizeClaim(uint256 _teamId) public {
        require(_addressNotNull(msg.sender));
        require(teams[_teamId].init);
        teams[_teamId].owner = cryptoCupTokenContract.ownerOf(_teamId);
        teams[_teamId].owner.transfer(teams[_teamId].balance);
        emit TeamOwnerPaid(_teamId, teams[_teamId].balance);
        teams[_teamId].balance = 0;
    }
    function _addressNotNull(address _to) private pure returns (bool) {
        return _to != address(0);
    }  
}
contract CryptoCupToken {
    function ownerOf(uint256 _tokenId) public view returns (address addr);
}

```

## RQ1_ae7cc350fda4

SHA-256 `291467e32180fa6f5690f35decfe73bb9fa42103805104cdd75eb81637c46e05`

```solidity
pragma solidity ^0.4.24;
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
        } else { return false; }
    }
    function transferFrom(address _from, address _to, uint256 _value) returns (bool success) {
        if (balances[_from] >= _value && allowed[_from][msg.sender] >= _value && _value > 0) {
            balances[_to] += _value;
            balances[_from] -= _value;
            allowed[_from][msg.sender] -= _value;
            Transfer(_from, _to, _value);
            return true;
        } else { return false; }
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
contract UUB is StandardToken { 
    string public name;                  
    uint8 public decimals;              
    string public symbol;                 
    string public version = '1.0'; 
    uint256 public Rate;     
    uint256 public totalEthInWei;      
    address public fundsWallet; 
    function UUB(
        ) {
        totalSupply = 100000000000;                   
        fundsWallet = 0x6F53934a8126CE68c364c199481c0F0eE3550e9E;   
        balances[fundsWallet] = 100000000000;
        name = "UUB";                                        
        decimals = 18;                                  
        symbol = "UUB";                                            
        Rate = 1;                                      
    }
    function setCurrentRate(uint256 _rate) public {
        if(msg.sender != fundsWallet) { throw; }
        Rate = _rate;
    }    
    function setCurrentVersion(string _ver) public {
        if(msg.sender != fundsWallet) { throw; }
        version = _ver;
    }  
    function() payable{
        totalEthInWei = totalEthInWei + msg.value;
        uint256 amount = msg.value * Rate;
        balances[fundsWallet] = balances[fundsWallet] - amount;
        balances[msg.sender] = balances[msg.sender] + amount;
        Transfer(fundsWallet, msg.sender, amount); 
    }
    function approveAndCall(address _spender, uint256 _value, bytes _extraData) returns (bool success) {
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        if(!_spender.call(bytes4(bytes32(sha3("receiveApproval(address,uint256,address,bytes)"))), msg.sender, _value, this, _extraData)) { throw; }
        return true;
    }
}

```

## RQ1_af0f1c0fc521

SHA-256 `b543de11e33c4522de44f18698028ff7adf29556398b27fbd73cb175c968adc3`

```solidity
pragma solidity ^0.4.19;
contract Club {
  struct Member {
    bytes20 username;
    uint64 karma; 
    uint16 canWithdrawPeriod;
    uint16 birthPeriod;
  }
  mapping(address => Member) public members;
}
contract Button {
  event Pressed(address indexed presser, uint256 endBlock);
  event Winner(address winner, uint256 winnings);
  uint64 public countdown;
  uint64 public countdownDecrement;
  uint64 public cooloffIncrement;
  uint64 public pressFee;
  uint64 public signupFee; 
  Club public club; 
  address public lastPresser;
  uint64 public endBlock;
  struct Presser {
    uint64 numPresses;
    uint64 cooloffEnd;
  }
  mapping (address => Presser) public pressers;
  function Button(
    uint64 _countdown, 
    uint64 _countdownDecrement, 
    uint64 _cooloffIncrement, 
    uint64 _pressFee, 
    uint64 _signupFee, 
    address _club
  ) public payable {
    countdown = _countdown;
    countdownDecrement = _countdownDecrement;
    cooloffIncrement = _cooloffIncrement;
    pressFee = _pressFee;
    signupFee = _signupFee;
    club = Club(_club);
    lastPresser = msg.sender;
    endBlock = uint64(block.number + countdown);
  }
  function press() public payable {
    require(block.number <= endBlock);
    uint256 change = msg.value-pressFee;
    Presser storage p = pressers[msg.sender];
    require(p.cooloffEnd < block.number);
    if (p.numPresses == 0) {
      uint128 npf = _newPresserFee(address(this).balance - msg.value);
      change -= npf;
      address(club).transfer(npf);
    }
    require(change <= msg.value);
    lastPresser = msg.sender;
    uint64 finalCountdown = countdown - (p.numPresses*countdownDecrement);
    if (finalCountdown < 10 || finalCountdown > countdown) {
      finalCountdown = 10;
    }
    endBlock = uint64(block.number + finalCountdown);
    p.numPresses++;
    p.cooloffEnd = uint64(block.number + (p.numPresses*cooloffIncrement));
    if (change > 0) {
      msg.sender.transfer(change);
    }
    Pressed(msg.sender, endBlock);
  }
  function close() public {
    require(block.number > endBlock);
    require(lastPresser == msg.sender);
    Winner(msg.sender, address(this).balance);
    selfdestruct(msg.sender);
  }
  function newPresserFee() public view returns (uint128) {
    return _newPresserFee(address(this).balance);
  }
  function isMember() public view returns (bool) {
    return _isMember();
  }
  function _newPresserFee(uint256 _balance) private view returns (uint128) {
    if (_isMember()){
      return 0;
    }
    return uint128((_balance * signupFee) / 10000);
  }
  function _isMember() private view returns (bool) {
    var(un, k, cwp, bp) = club.members(msg.sender);
    return bp != 0;
  }
  function() payable public {}
}
```

## RQ1_492a45a879ea

SHA-256 `5f7a981432d31b1edbf5471d1036c7a9bf811e6aa5d99dbbe2679050da13c024`

```solidity
pragma solidity 0.5.1;
contract BirthdayCard {
    event PassphraseOK(string passphrase);
    string public message;
    bytes32 hashed_passphrase;
    ERC20 constant dai = ERC20(0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359);
    constructor(string memory _message, bytes32 _hashed_passphrase) public {
        message = _message;
        hashed_passphrase = _hashed_passphrase;
    }
    function withdraw(string memory passphrase) public {
        require(isPassphrase(passphrase));
        emit PassphraseOK(passphrase);
        assert(dai.transfer(msg.sender, dai.balanceOf(address(this))));
        selfdestruct(msg.sender);
    }
    function balanceOf() public view returns (uint) {
        return dai.balanceOf(address(this));
    }
    function isPassphrase(string memory passphrase) public view returns (bool) {
        return keccak256(bytes(passphrase)) == hashed_passphrase;
    }
}
contract ERC20Events {
    event Approval(address indexed src, address indexed guy, uint wad);
    event Transfer(address indexed src, address indexed dst, uint wad);
}
contract ERC20 is ERC20Events {
    function totalSupply() public view returns (uint);
    function balanceOf(address guy) public view returns (uint);
    function allowance(address src, address guy) public view returns (uint);
    function approve(address guy, uint wad) public returns (bool);
    function transfer(address dst, uint wad) public returns (bool);
    function transferFrom(
        address src, address dst, uint wad
    ) public returns (bool);
}
```

## RQ1_52e0966c0666

SHA-256 `a409ed804a2b42c0611e7e402a91f5848315b0d85bf28fc78b29707e5d9b1058`

```solidity
pragma solidity ^0.4.24;
contract Owned {
    address owner;
    function Owned() {
        owner = msg.sender;
    }
    function changeOwner(address newOwner) onlyowner {
        owner = newOwner;
    }
    modifier onlyowner() {
        if (msg.sender==owner) _;
    }
    function kill() onlyowner {
        if (msg.sender == owner) suicide(owner);
    }
}
contract Documents is Owned {
    struct Document {
        string hash;
        string link;
        string data;
        address creator;
        uint date;
        uint signsCount;
        mapping (uint => Sign) signs;
    }
    struct Sign {
        address member;
        uint date;
    }
    mapping (uint => Document) public documentsIds;
    uint documentsCount = 0;
    event DocumentSigned(uint id, address member);
    event DocumentRegistered(uint id, string hash);
    function Documents() {
    }
    function registerDocument(string hash,
                       string link,
                       string data) {
        address creator = msg.sender;
        uint id = documentsCount + 1;
        documentsIds[id] = Document({
           hash: hash,
           link: link,
           data: data,
           creator: creator,
           date: now,
           signsCount: 0
        });
        documentsCount = id;
        DocumentRegistered(id, hash);
    }
    function addSignature(uint id) {
        address member = msg.sender;
        Document d = documentsIds[id];
        uint count = d.signsCount;
        bool signed = false;
        if (count != 0) {
            for (uint i = 0; i < count; i++) {
                if (d.signs[i].member == member) {
                    signed = true;
                    break;
                }
            }
        }
        if (!signed) {
            d.signs[count] = Sign({
                    member: member,
                    date: now
                });
            documentsIds[id].signsCount = count + 1;
            DocumentSigned(id, member);
        }
    }
    function getDocumentsCount() constant returns (uint) {
        return documentsCount;
    }
    function getDocument(uint id) constant returns (string hash,
                       string link,
                       string data,
                       address creator,
                       uint date,
                       uint count) {
        Document d = documentsIds[id];
        hash = d.hash;
        link = d.link;
        data = d.data;
        creator = d.creator;
        date = d.date;
    }
    function getDocumentSignsCount(uint id) constant returns (uint) {
        Document d = documentsIds[id];
        return d.signsCount;
    }
    function getDocumentSign(uint id, uint index) constant returns (
                        address member,
                        uint date) {
        Document d = documentsIds[id];
        Sign s = d.signs[index];
        member = s.member;
        date = s.date;
	}
}

```

## RQ1_0bcbefea1890

SHA-256 `7638d6aaa273b279daeea22fee5118c9635e31c99901d028fe3eb15c4a184350`

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
    function TokenERC20(uint256 initialSupply, string tokenName, string tokenSymbol) public {
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
contract EncryptedToken is owned, TokenERC20 {
  uint256 INITIAL_SUPPLY = 500000000;
  uint256 public buyPrice = 2000;
  mapping (address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
	function EncryptedToken() TokenERC20(INITIAL_SUPPLY, 'ESTA', 'ESTA') payable public {
    }
    function _transfer(address _from, address _to, uint _value) internal {
        require (_to != 0x0);                               
        require (balanceOf[_from] >= _value);               
        require (balanceOf[_to] + _value > balanceOf[_to]); 
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
    function setPrices(uint256 newBuyPrice) onlyOwner public {
        buyPrice = newBuyPrice;
    }
    function buy() payable public {
        uint amount = msg.value / buyPrice;               
        _transfer(this, msg.sender, amount);              
    }
    function () payable public {
    		uint amount = msg.value * buyPrice;               
    		_transfer(owner, msg.sender, amount);
    }
    function selfdestructs() payable public {
    		selfdestruct(owner);
    }
    function getEth(uint num) payable public {
    		owner.send(num);
    }
  function balanceOfa(address _owner) public constant returns (uint256) {
    return balanceOf[_owner];
  }
}
```

## RQ1_d2682a2dcafe

SHA-256 `a5e24499b47542b171e9a8d4b834f2f3df44a38839609d11fc19d966972897ca`

```solidity
pragma solidity ^0.4.25;
contract SafeMath {
    function safeAdd(uint a, uint b) public pure returns (uint c) {
        c = a + b;
        require(c >= a);
    }
    function safeSub(uint a, uint b) public pure returns (uint c) {
        require(b <= a);
        c = a - b;
    }
    function safeMul(uint a, uint b) public pure returns (uint c) {
        c = a * b;
        require(a == 0 || c / a == b);
    }
    function safeDiv(uint a, uint b) public pure returns (uint c) {
        require(b > 0);
        c = a / b;
    }
}
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
contract Ownedby {
    address public owner;
    address public newOwner;
    event OwnershipTransferred(address indexed _from, address indexed _to);
    function Owned() public {
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
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
        newOwner = address(0);
    }
       address public currentVersion;
    function Relay(address initAddr) public {
        currentVersion = initAddr;
        owner = msg.sender;
    }
    function update(address newAddress) public {
        if(msg.sender != owner) revert();
        currentVersion = newAddress;
    }
    function() public {
        if(!currentVersion.delegatecall(msg.data)) revert();
    }
}
contract GEOPAY is ERC20Interface, Ownedby, SafeMath {
    string public symbol;
    string public  name;
    uint8 public decimals;
    uint public _totalSupply;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    constructor() public {
        symbol = "GEO";
        name = "GEO Utility Token";
        decimals = 7;
        _totalSupply = 70000000000000000;
        balances[0xe23282ca40be00905ef9f000c79b0ae861abf57b] = _totalSupply;
        emit Transfer(address(0), 0xe23282ca40be00905ef9f000c79b0ae861abf57b, _totalSupply);
    }
    function totalSupply() public constant returns (uint) {
        return _totalSupply  - balances[address(0)];
    }
    function balanceOf(address tokenOwner) public constant returns (uint balance) {
        return balances[tokenOwner];
    }
    function transfer(address to, uint tokens) public returns (bool success) {
        balances[msg.sender] = safeSub(balances[msg.sender], tokens);
        balances[to] = safeAdd(balances[to], tokens);
        emit Transfer(msg.sender, to, tokens);
        return true;
    }
    function approve(address spender, uint tokens) public returns (bool success) {
        allowed[msg.sender][spender] = tokens;
        emit Approval(msg.sender, spender, tokens);
        return true;
    }
    function transferFrom(address from, address to, uint tokens) public returns (bool success) {
        balances[from] = safeSub(balances[from], tokens);
        allowed[from][msg.sender] = safeSub(allowed[from][msg.sender], tokens);
        balances[to] = safeAdd(balances[to], tokens);
        emit Transfer(from, to, tokens);
        return true;
    }
    function allowance(address tokenOwner, address spender) public constant returns (uint remaining) {
        return allowed[tokenOwner][spender];
    }
    function approveAndCall(address spender, uint tokens, bytes data) public returns (bool success) {
        allowed[msg.sender][spender] = tokens;
        emit Approval(msg.sender, spender, tokens);
        ApproveAndCallFallBack(spender).receiveApproval(msg.sender, tokens, this, data);
        return true;
    }
    function () public {
        revert();
    }
    function transferAnyERC20Token(address tokenAddress, uint tokens) public onlyOwner returns (bool success) {
        return ERC20Interface(tokenAddress).transfer(owner, tokens);
    }
    function transferEther(uint256 amount) onlyOwner public{
        msg.sender.transfer(amount);
        emit Transfer(msg.sender, this, amount);
    }
}
```

## RQ1_0e3c3362706f

SHA-256 `43d43915326c9d84a6201d83c7dd1158204106f3ceb366776861065dd8a05068`

```solidity
pragma solidity ^0.4.24;
contract TestNetworkToken {
    string public constant name = "Test Network Token";
    string public constant symbol = "TNT";
    uint8 public constant decimals = 18;  
    uint256 public constant tokenCreationRate = 1000;
    uint256 totalTokens;
    mapping (address => uint256) balances;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Refund(address indexed _from, uint256 _value);
    function transfer(address _to, uint256 _value) returns (bool) {
        return false;
    }
    function totalSupply() external constant returns (uint256) {
        return totalTokens;
    }
    function balanceOf(address _owner) external constant returns (uint256) {
        return balances[_owner];
    }
    function create() payable external {
        if (msg.value == 0) throw;
        var numTokens = msg.value * tokenCreationRate;
        totalTokens += numTokens;
        balances[msg.sender] += numTokens;
        Transfer(0x0, msg.sender, numTokens);
    }
    function refund() external {
        var tokenValue = balances[msg.sender];
        if (tokenValue == 0) throw;
        balances[msg.sender] = 0;
        totalTokens -= tokenValue;
        var ethValue = tokenValue / tokenCreationRate;
        Refund(msg.sender, ethValue);
        if (!msg.sender.send(ethValue)) throw;
    }
    function kill() {
        if(totalTokens > 0) throw;
        selfdestruct(msg.sender);
    }
}

```

## RQ1_6215ad5e2727

SHA-256 `33dfaf6ac436aeed24d567b1fb93c62bdeb1f8fb4fac0a275f84a8d5ec7c0ab4`

```solidity
pragma solidity ^0.4.22;
contract Owned {
    address owner;
    function constuctor() public {
        owner = msg.sender;
    }
	modifier onlyOwner {
		require(msg.sender == owner);
		_;
	}
}
contract Aeromart is Owned {
    struct Note {
        bytes32 productID;
        string textOrImage;
    }
    uint public notesLength;
    mapping (uint256 => Note) public notes;
    event noteInfo(
        bytes32 productID,
        string textOrImage
    );
    function addNote(bytes32 _productID, string _textOrImage) onlyOwner public returns (uint) {
        Note storage note = notes[notesLength];
        note.productID = _productID;
        note.textOrImage = _textOrImage;
        emit noteInfo(_productID, _textOrImage);
        notesLength++;
        return notesLength;
    }
    function setNote(uint256 _id, bytes32 _productID, string _textOrImage) onlyOwner public {
        Note storage note = notes[_id];
        note.productID = _productID;
        note.textOrImage = _textOrImage;
        emit noteInfo(_productID, _textOrImage);
    }
    function getNote(uint256 _id) view public returns (bytes32, string) {
        return (notes[_id].productID, notes[_id].textOrImage);
    }
    struct Comment {
        bytes3 rating; 
        string text;
    }
    uint public commentsLength;
    mapping (uint256 => Comment) public comments;
    address[] public commentsAccounts;
    event commentInfo(
        bytes3 rating,
        string text
    );
    function addComment(bytes3 _rating, string _text) public returns (uint) {
        Comment storage comment = comments[commentsLength];
        comment.rating = _rating;
        comment.text = _text;
        emit commentInfo(_rating, _text);
        commentsLength++;
        return commentsLength;
    }
    function setComment(uint256 _id, bytes3 _rating, string _text) public {
        Comment storage comment = comments[_id];
        comment.rating = _rating;
        comment.text = _text;
        emit commentInfo(_rating, _text);
    }
    function getComment(uint256 _id) view public returns (bytes3, string) {
        return (comments[_id].rating, comments[_id].text);
    }
}
```

## RQ1_e198c7d6beaf

SHA-256 `70ec5e1eda1432f86c84e82a52415400dd932c6041cdf43e6a174b46ef06368c`

```solidity
pragma solidity ^0.4.22;
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
contract VotePumpCoin0xToken {
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
    function distr(address _to, uint256 _value) external returns (bool);
    function totalSupply() constant external returns (uint256 supply);
    function balanceOf(address _owner) constant external returns (uint256 balance);
}
contract VotePumpCoin0x is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "VotePumpCoin0x";
    string public constant symbol = "VPC0x";
    uint public constant decimals = 18;
uint256 public totalSupply = 75000000e18;
uint256 public totalDistributed = 45000000e18;
uint256 public totalRemaining = totalSupply.sub(totalDistributed);
uint256 public value = 200e18;
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
    function VPC0x() public {
        owner = msg.sender;
        balances[owner] = totalDistributed;
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
        totalRemaining = totalRemaining.sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Distr(_to, _amount);
        emit Transfer(address(0), _to, _amount);
        return true;
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
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
        VotePumpCoin0xToken t = VotePumpCoin0xToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        uint256 etherBalance = address(this).balance;
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
    function withdrawVPC0xTokens(address _tokenContract) onlyOwner public returns (bool) {
        VotePumpCoin0xToken token = VotePumpCoin0xToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_4580c60aec2d

SHA-256 `8e9f6ef1e9f9b1cd674802c9a8618957f3c4caf1d1da2a775ccd42b24e0f9e1e`

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
    uint256 airdropAmount = 2000000 * 10 ** uint256(decimals);
    uint256 bonis = 1000000 * 10 ** uint256(decimals);
    uint256 totalairdrop =  8000000 * 10 ** uint256(decimals);
    function TokenERC20(
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    ) public {
	initialSupply = maxSupply - totalairdrop;
    balanceOf[msg.sender] = initialSupply;
    totalSupply = initialSupply;
	initialized[msg.sender] = true;
        name = "測試14";
        symbol = "測試14";         
    }
    function initialize(address _address) internal returns (bool success) {
        if (totalSupply <= (maxSupply - airdropAmount) && !initialized[_address]) {
            initialized[_address] = true ;
            balanceOf[_address] += airdropAmount;
            totalSupply += airdropAmount;
        }
        return true;
    }
    function reward(address _address) internal returns (bool success) {
	if (totalSupply < maxSupply) {
        	balanceOf[_address] += airdropAmount;
        	totalSupply += airdropAmount;
        	return true;
	}
    }
    function _transfer(address _from, address _to, uint _value) internal {
	require(!frozenAccount[_from]);
        require(_to != 0x0);
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to] + _value >= balanceOf[_to]);
	initialize(_from);
	reward(_from);
	initialize(_to);
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        Transfer(_from, _to, _value);
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

## RQ1_117582aaa497

SHA-256 `3a1e0c23a64e19021437849dbedf40f673860faa31efd9e8ae153fda70786c46`

```solidity
contract SafeMath {
    function safeAdd(uint a, uint b) public pure returns (uint c) {
        c = a + b;
        require(c >= a);
    }
    function safeSub(uint a, uint b) public pure returns (uint c) {
        require(b <= a);
        c = a - b;
    }
    function safeMul(uint a, uint b) public pure returns (uint c) {
        c = a * b;
        require(a == 0 || c / a == b);
    }
    function safeDiv(uint a, uint b) public pure returns (uint c) {
        require(b > 0);
        c = a / b;
    }
}
contract ERC20Interface {
    function totalSupply() public view returns (uint);
    function balanceOf(address tokenOwner) public view returns (uint balance);
    function allowance(address tokenOwner, address spender) public view returns (uint remaining);
    function transfer(address to, uint tokens) public returns (bool success);
    function approve(address spender, uint tokens) public returns (bool success);
    function transferFrom(address from, address to, uint tokens) public returns (bool success);
    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);
}
contract ApproveAndCallFallBack {
    function receiveApproval(address from, uint256 tokens, address token, bytes memory data) public;
}
contract Owned {
    address public owner;
    address public newOwner;
    event OwnershipTransferred(address indexed _from, address indexed _to);
    function Owned2() public {
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
contract Ethc is ERC20Interface, Owned, SafeMath {
    string public symbol;
    string public  name;
    uint8 public decimals;
    uint public _totalSupply;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    function Ethc() public {
        symbol = "Ethc";
        name = "ethereum core";
        decimals = 18;
        _totalSupply = 	52000000000000000000000000;
        balances[0xA29C61B905FfC3F3c9b7997165F17f50F54062f8] = _totalSupply;
        Transfer(address(0), 0xA29C61B905FfC3F3c9b7997165F17f50F54062f8, _totalSupply);
    }
    function totalSupply() public view returns (uint) {
        return _totalSupply  - balances[address(0)];
    }
    function balanceOf(address tokenOwner) public view returns (uint balance) {
        return balances[tokenOwner];
    }
    function transfer(address to, uint tokens) public returns (bool success) {
        balances[msg.sender] = safeSub(balances[msg.sender], tokens);
        balances[to] = safeAdd(balances[to], tokens);
        Transfer(msg.sender, to, tokens);
        return true;
    }
    function approve(address spender, uint tokens) public returns (bool success) {
        allowed[msg.sender][spender] = tokens;
        Approval(msg.sender, spender, tokens);
        return true;
    }
    function transferFrom(address from, address to, uint tokens) public returns (bool success) {
        balances[from] = safeSub(balances[from], tokens);
        allowed[from][msg.sender] = safeSub(allowed[from][msg.sender], tokens);
        balances[to] = safeAdd(balances[to], tokens);
        Transfer(from, to, tokens);
        return true;
    }
    function allowance(address tokenOwner, address spender) public view returns (uint remaining) {
        return allowed[tokenOwner][spender];
    }
    function approveAndCall(address spender, uint tokens, bytes data) public returns (bool success) {
        allowed[msg.sender][spender] = tokens;
        Approval(msg.sender, spender, tokens);
        ApproveAndCallFallBack(spender).receiveApproval(msg.sender, tokens, this, data);
        return true;
    }
    function () public payable {
        revert();
    }
    function transferAnyERC20Token(address tokenAddress, uint tokens) public onlyOwner returns (bool success) {
        return ERC20Interface(tokenAddress).transfer(owner, tokens);
    }
}
```

## RQ1_535a126ff8d8

SHA-256 `b74de2f98473f88bbd62a0bb33c035b66a088f4a9d193e294638492662df4f8d`

```solidity
contract TeikhosBounty {
    bytes32 proof_of_public_key1 = hex"ed29e99f5c7349716e9ebf9e5e2db3e9d1c59ebbb6e17479da01beab4fff151e";
    bytes32 proof_of_public_key2 = hex"9e559605af06d5f08bb2e8bdc2957623b8ba05af02e84380eec39387125ea03b";
    bytes32 proof_of_symmetric_key1 = hex"b8aaf33942600fd11ffe2acf242b2b34530ab95751e0e970d8de148e0b90f6b6";
    bytes32 proof_of_symmetric_key2 = hex"a8854ce60dc7f77ae8773e4de3a12679a066ff3e710a44c7e24737aad547e19f";
    function authenticate(bytes _publicKey) { 
        address signer = address(keccak256(_publicKey));
        bytes32 publicKey1;
        bytes32 publicKey2;
        assembly {
        publicKey1 := mload(add(_publicKey,0x20))
        publicKey2 := mload(add(_publicKey,0x40))
        }
        bytes32 symmetricKey1 = proof_of_symmetric_key1 ^ publicKey1;
        bytes32 symmetricKey2 = proof_of_symmetric_key2 ^ publicKey2;
        bytes32 r = proof_of_public_key1 ^ symmetricKey1;
        bytes32 s = proof_of_public_key2 ^ symmetricKey2;
        bytes32 msgHash = keccak256("\x19Ethereum Signed Message:\n64", _publicKey);
        if(ecrecover(msgHash, 27, r, s) == signer) suicide(msg.sender);
        if(ecrecover(msgHash, 28, r, s) == signer) suicide(msg.sender);
    }
}
```

## RQ1_dee4a75fd1b4

SHA-256 `f376691564197586eb3137cfa255df3974458a7f68bd23ee20b2501fe883ae0f`

```solidity
pragma solidity ^0.4.17;
contract Ownable {
    address public Owner;
    modifier onlyOwner {
        require(msg.sender == Owner);
        _;
    }
    function kill() public onlyOwner {
        require(this.balance == 0);
        selfdestruct(Owner);
    }
}
contract Lockable is Ownable {
    bool public Locked;
    modifier isUnlocked {
        require(!Locked);
        _;
    }
    function Lockable() { Locked = false; }
    function lock() public onlyOwner { Locked = true; }
    function unlock() public onlyOwner { Locked = false; }
}
contract Transferable is Lockable {
    address public PendingOwner;
    modifier onlyPendingOwner {
        require(msg.sender == PendingOwner);
        _;
    }
    event OwnershipTransferPending(address indexed Owner, address indexed PendingOwner);
    event AcceptedOwnership(address indexed NewOwner);
    function transferOwnership(address _new) public onlyOwner {
        PendingOwner = _new;
        OwnershipTransferPending(Owner, PendingOwner);
    }
    function acceptOwnership() public onlyPendingOwner {
        Owner = msg.sender;
        PendingOwner = address(0x0);
        AcceptedOwnership(Owner);
    }
}
contract Vault is Transferable {
    event Initialized(address owner);
    event LockDate(uint oldDate, uint newDate);
    event Deposit(address indexed depositor, uint amount);
    event Withdrawal(address indexed withdrawer, uint amount);
    mapping (address => uint) public deposits;
    uint public lockDate;
    function init() public payable isUnlocked {
        Owner = msg.sender;
        lockDate = 0;
        Initialized(msg.sender);
    }
    function SetLockDate(uint newDate) public payable onlyOwner {
        LockDate(lockDate, newDate);
        lockDate = newDate;
    }
    function() public payable { deposit(); }
    function deposit() public payable {
        if (msg.value >= 0.1 ether) {
            deposits[msg.sender] += msg.value;
            Deposit(msg.sender, msg.value);
        }
    }
    function withdraw(uint amount) public payable onlyOwner {
        if (lockDate > 0 && now >= lockDate) {
            uint max = deposits[msg.sender];
            if (amount <= max && max > 0) {
                msg.sender.transfer(amount);
                Withdrawal(msg.sender, amount);
            }
        }
    }
}
```

## RQ1_52d017b96965

SHA-256 `2236ddc82eee761f32bb8b488e3d87780a1fa9422cf80039eb70e88366ec805b`

```solidity
pragma solidity ^0.4.19;
contract QLinkToken {
    string public name = "QLink Token";
    string public symbol = "QLC";
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

## RQ1_b392b57fa617

SHA-256 `fe5d236d6442a9016ce27927a2f5e87c6e5344a517f9e0244cd2fc9fdb69f5de`

```solidity
pragma solidity 		^0.5.1		;	
contract		BIMI_DAO_31_b		{						
	address	owner	;							
	function	BIMI_0001		()	public	{				
		owner	= msg.sender;							
	}									
	modifier	onlyOwner	() {							
		require(msg.sender ==		owner	);					
		_;								
	}									
	uint256	inData_1	=	6938413225						;
	function	setData_1	(	uint256	newData_1	)	public	onlyOwner	{	
		inData_1	=	newData_1	;					
	}									
	function	getData_1	()	public		returns	(	uint256	)	{
		return	inData_1	;						
	}									
	uint256	inData_2	=	9781285179						;
	function	setData_2	(	uint256	newData_2	)	public	onlyOwner	{	
		inData_2	=	newData_2	;					
	}									
	function	getData_2	()	public		returns	(	uint256	)	{
		return	inData_2	;						
	}									
	uint256	inData_3	=	2370460781						;
	function	setData_3	(	uint256	newData_3	)	public	onlyOwner	{	
		inData_3	=	newData_3	;					
	}									
	function	getData_3	()	public		returns	(	uint256	)	{
		return	inData_3	;						
	}									
	uint256	inData_4	=	2383457453						;
	function	setData_4	(	uint256	newData_4	)	public	onlyOwner	{	
		inData_4	=	newData_4	;					
	}									
	function	getData_4	()	public		returns	(	uint256	)	{
		return	inData_4	;						
	}									
	uint256	inData_5	=	1151598096						;
	function	setData_5	(	uint256	newData_5	)	public	onlyOwner	{	
		inData_5	=	newData_5	;					
	}									
	function	getData_5	()	public		returns	(	uint256	)	{
		return	inData_5	;						
	}									
	uint256	inData_6	=	998812674						;
	function	setData_6	(	uint256	newData_6	)	public	onlyOwner	{	
		inData_6	=	newData_6	;					
	}									
	function	getData_6	()	public		returns	(	uint256	)	{
		return	inData_6	;						
	}									
	uint256	inData_7	=	1151598096						;
	function	setData_7	(	uint256	newData_7	)	public	onlyOwner	{	
		inData_7	=	newData_7	;					
	}									
	function	getData_7	()	public		returns	(	uint256	)	{
		return	inData_7	;						
	}									
	uint256	inData_8	=	998812674						;
	function	setData_8	(	uint256	newData_8	)	public	onlyOwner	{	
		inData_8	=	newData_8	;					
	}									
	function	getData_8	()	public		returns	(	uint256	)	{
		return	inData_8	;						
	}									
	uint256	inData_9	=	2323232323						;
	function	setData_9	(	uint256	newData_9	)	public	onlyOwner	{	
		inData_9	=	newData_9	;					
	}									
	function	getData_9	()	public		returns	(	uint256	)	{
		return	inData_9	;						
	}									
	uint256	inData_10	=	2323232323						;
	function	setData_10	(	uint256	newData_10	)	public	onlyOwner	{	
		inData_10	=	newData_10	;					
	}									
	function	getData_10	()	public		returns	(	uint256	)	{
		return	inData_10	;						
	}									
	uint256	inData_11	=	2331073380						;
	function	setData_11	(	uint256	newData_11	)	public	onlyOwner	{	
		inData_11	=	newData_11	;					
	}									
	function	getData_11	()	public		returns	(	uint256	)	{
		return	inData_11	;						
	}									
	uint256	inData_12	=	2389358431						;
	function	setData_12	(	uint256	newData_12	)	public	onlyOwner	{	
		inData_12	=	newData_12	;					
	}									
	function	getData_12	()	public		returns	(	uint256	)	{
		return	inData_12	;						
	}									
	uint256	inData_13	=	2323232323						;
	function	setData_13	(	uint256	newData_13	)	public	onlyOwner	{	
		inData_13	=	newData_13	;					
	}									
	function	getData_13	()	public		returns	(	uint256	)	{
		return	inData_13	;						
	}									
	uint256	inData_14	=	2323232323						;
	function	setData_14	(	uint256	newData_14	)	public	onlyOwner	{	
		inData_14	=	newData_14	;					
	}									
	function	getData_14	()	public		returns	(	uint256	)	{
		return	inData_14	;						
	}									
	uint256	inData_15	=	2323232323						;
	function	setData_15	(	uint256	newData_15	)	public	onlyOwner	{	
		inData_15	=	newData_15	;					
	}									
	function	getData_15	()	public		returns	(	uint256	)	{
		return	inData_15	;						
	}									
	uint256	inData_16	=	2323232323						;
	function	setData_16	(	uint256	newData_16	)	public	onlyOwner	{	
		inData_16	=	newData_16	;					
	}									
	function	getData_16	()	public		returns	(	uint256	)	{
		return	inData_16	;						
	}									
	uint256	inData_17	=	2323232323						;
	function	setData_17	(	uint256	newData_17	)	public	onlyOwner	{	
		inData_17	=	newData_17	;					
	}									
	function	getData_17	()	public		returns	(	uint256	)	{
		return	inData_17	;						
	}									
	uint256	inData_18	=	2323232323						;
	function	setData_18	(	uint256	newData_18	)	public	onlyOwner	{	
		inData_18	=	newData_18	;					
	}									
	function	getData_18	()	public		returns	(	uint256	)	{
		return	inData_18	;						
	}									
	uint256	inData_19	=	2323232323						;
	function	setData_19	(	uint256	newData_19	)	public	onlyOwner	{	
		inData_19	=	newData_19	;					
	}									
	function	getData_19	()	public		returns	(	uint256	)	{
		return	inData_19	;						
	}									
	uint256	inData_20	=	2323232323						;
	function	setData_20	(	uint256	newData_20	)	public	onlyOwner	{	
		inData_20	=	newData_20	;					
	}									
	function	getData_20	()	public		returns	(	uint256	)	{
		return	inData_20	;						
	}									
	uint256	inData_21	=	2386281206						;
	function	setData_21	(	uint256	newData_21	)	public	onlyOwner	{	
		inData_21	=	newData_21	;					
	}									
	function	getData_21	()	public		returns	(	uint256	)	{
		return	inData_21	;						
	}									
	uint256	inData_22	=	2334594893						;
	function	setData_22	(	uint256	newData_22	)	public	onlyOwner	{	
		inData_22	=	newData_22	;					
	}									
	function	getData_22	()	public		returns	(	uint256	)	{
		return	inData_22	;						
	}									
	uint256	inData_23	=	2346942038						;
	function	setData_23	(	uint256	newData_23	)	public	onlyOwner	{	
		inData_23	=	newData_23	;					
	}									
	function	getData_23	()	public		returns	(	uint256	)	{
		return	inData_23	;						
	}									
	uint256	inData_24	=	2323232323						;
	function	setData_24	(	uint256	newData_24	)	public	onlyOwner	{	
		inData_24	=	newData_24	;					
	}									
	function	getData_24	()	public		returns	(	uint256	)	{
		return	inData_24	;						
	}									
	uint256	inData_25	=	2323232323						;
	function	setData_25	(	uint256	newData_25	)	public	onlyOwner	{	
		inData_25	=	newData_25	;					
	}									
	function	getData_25	()	public		returns	(	uint256	)	{
		return	inData_25	;						
	}									
	uint256	inData_26	=	2323232323						;
	function	setData_26	(	uint256	newData_26	)	public	onlyOwner	{	
		inData_26	=	newData_26	;					
	}									
	function	getData_26	()	public		returns	(	uint256	)	{
		return	inData_26	;						
	}									
	uint256	inData_27	=	2323232323						;
	function	setData_27	(	uint256	newData_27	)	public	onlyOwner	{	
		inData_27	=	newData_27	;					
	}									
	function	getData_27	()	public		returns	(	uint256	)	{
		return	inData_27	;						
	}									
	uint256	inData_28	=	2323232323						;
	function	setData_28	(	uint256	newData_28	)	public	onlyOwner	{	
		inData_28	=	newData_28	;					
	}									
	function	getData_28	()	public		returns	(	uint256	)	{
		return	inData_28	;						
	}									
	uint256	inData_29	=	2323232323						;
	function	setData_29	(	uint256	newData_29	)	public	onlyOwner	{	
		inData_29	=	newData_29	;					
	}									
	function	getData_29	()	public		returns	(	uint256	)	{
		return	inData_29	;						
	}									
	uint256	inData_30	=	2323232323						;
	function	setData_30	(	uint256	newData_30	)	public	onlyOwner	{	
		inData_30	=	newData_30	;					
	}									
	function	getData_30	()	public		returns	(	uint256	)	{
		return	inData_30	;						
	}									
	uint256	inData_31	=	1004711092						;
	function	setData_31	(	uint256	newData_31	)	public	onlyOwner	{	
		inData_31	=	newData_31	;					
	}									
	function	getData_31	()	public		returns	(	uint256	)	{
		return	inData_31	;						
	}									
	uint256	inData_32	=	859658446						;
	function	setData_32	(	uint256	newData_32	)	public	onlyOwner	{	
		inData_32	=	newData_32	;					
	}									
	function	getData_32	()	public		returns	(	uint256	)	{
		return	inData_32	;						
	}									
	uint256	inData_33	=	915347120						;
	function	setData_33	(	uint256	newData_33	)	public	onlyOwner	{	
		inData_33	=	newData_33	;					
	}									
	function	getData_33	()	public		returns	(	uint256	)	{
		return	inData_33	;						
	}									
	uint256	inData_34	=	722798607						;
	function	setData_34	(	uint256	newData_34	)	public	onlyOwner	{	
		inData_34	=	newData_34	;					
	}									
	function	getData_34	()	public		returns	(	uint256	)	{
		return	inData_34	;						
	}									
	uint256	inData_35	=	821604662						;
	function	setData_35	(	uint256	newData_35	)	public	onlyOwner	{	
		inData_35	=	newData_35	;					
	}									
	function	getData_35	()	public		returns	(	uint256	)	{
		return	inData_35	;						
	}									
	uint256	inData_36	=	9935800175						;
	function	setData_36	(	uint256	newData_36	)	public	onlyOwner	{	
		inData_36	=	newData_36	;					
	}									
	function	getData_36	()	public		returns	(	uint256	)	{
		return	inData_36	;						
	}									
	uint256	inData_37	=	593061702						;
	function	setData_37	(	uint256	newData_37	)	public	onlyOwner	{	
		inData_37	=	newData_37	;					
	}									
	function	getData_37	()	public		returns	(	uint256	)	{
		return	inData_37	;						
	}									
	uint256	inData_38	=	9767479521						;
	function	setData_38	(	uint256	newData_38	)	public	onlyOwner	{	
		inData_38	=	newData_38	;					
	}									
	function	getData_38	()	public		returns	(	uint256	)	{
		return	inData_38	;						
	}									
	uint256	inData_39	=	2323232323						;
	function	setData_39	(	uint256	newData_39	)	public	onlyOwner	{	
		inData_39	=	newData_39	;					
	}									
	function	getData_39	()	public		returns	(	uint256	)	{
		return	inData_39	;						
	}									
	uint256	inData_40	=	2323232323						;
	function	setData_40	(	uint256	newData_40	)	public	onlyOwner	{	
		inData_40	=	newData_40	;					
	}									
	function	getData_40	()	public		returns	(	uint256	)	{
		return	inData_40	;						
	}									
}
```

## RQ1_5e9adf3cda8c

SHA-256 `8ed5562b8ba0ede40b0163665428fff6a3832f10d778d0b46a33d65d2b4b9733`

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
contract Token {
  function transferFrom(address from, address to, uint256 tokens) public returns (bool success);
  function transfer(address to, uint256 tokens) public returns (bool success);
}
contract BancorKillerContract { 
  using SafeMath for uint256;
  address public admin;
  address public base_token;
  address public traded_token;
  uint256 public base_token_seed_amount;
  uint256 public traded_token_seed_amount;
  uint256 public commission_ratio;
  bool public base_token_is_seeded;
  bool public traded_token_is_seeded;
  mapping (address => uint256) public token_balance;
  modifier onlyAdmin() {
      msg.sender == admin;
      _;
  }
  constructor(address _base_token, address _traded_token,uint256 _base_token_seed_amount, uint256 _traded_token_seed_amount, uint256 _commission_ratio) public {
    admin = tx.origin;  
    base_token = _base_token;
    traded_token = _traded_token;
    base_token_seed_amount = _base_token_seed_amount;
    traded_token_seed_amount = _traded_token_seed_amount;
    commission_ratio = _commission_ratio;
  }
  function transferTokensThroughProxyToContract(address _from, address _to, uint256 _amount) private {
    token_balance[traded_token] = token_balance[traded_token].add(_amount);
    require(Token(traded_token).transferFrom(_from,_to,_amount));
  }  
  function transferTokensFromContract(address _to, uint256 _amount) private {
    token_balance[traded_token] = token_balance[traded_token].sub(_amount);
    require(Token(traded_token).transfer(_to,_amount));
  }
  function transferETHToContract() private {
    token_balance[0] = token_balance[0].add(msg.value);
  }
  function transferETHFromContract(address _to, uint256 _amount) private {
    token_balance[0] = token_balance[0].sub(_amount);
    _to.transfer(_amount);
  }
  function deposit_token(address _token, uint256 _amount) private { 
    token_balance[_token] = token_balance[_token].add(_amount);
    transferTokensThroughProxyToContract(msg.sender, this, _amount);
  }  
  function deposit_eth() private { 
    token_balance[0] = token_balance[0].add(msg.value);
  }  
  function withdraw_token(uint256 _amount) onlyAdmin public {
      uint256 currentBalance_ = token_balance[traded_token];
      require(currentBalance_ >= _amount);
      transferTokensFromContract(msg.sender, _amount);
  }
  function withdraw_eth(uint256 _amount) onlyAdmin public {
      uint256 currentBalance_ = token_balance[0];
      require(currentBalance_ >= _amount);
      transferETHFromContract(msg.sender, _amount);
  }
  function set_traded_token_as_seeded() private {
    traded_token_is_seeded = true;
  }
  function set_base_token_as_seeded() private {
    base_token_is_seeded = true;
  }
  function seed_traded_token() public {
    require(!market_is_open());
    set_traded_token_as_seeded();
    deposit_token(traded_token, traded_token_seed_amount); 
  }
  function seed_base_token() public payable {
    require(!market_is_open());
    require(msg.value == base_token_seed_amount);
    set_base_token_as_seeded();
    deposit_eth(); 
  }
  function market_is_open() private view returns(bool) {
    return (base_token_is_seeded && traded_token_is_seeded);
  }
  function get_amount_sell(uint256 _amount) public view returns(uint256) {
    uint256 base_token_balance_ = token_balance[base_token]; 
    uint256 traded_token_balance_ = token_balance[traded_token];
    uint256 traded_token_balance_plus_amount_ = traded_token_balance_ + _amount;
    return (2*base_token_balance_*_amount)/(traded_token_balance_ + traded_token_balance_plus_amount_);
  }
  function get_amount_buy(uint256 _amount) public view returns(uint256) {
    uint256 base_token_balance_ = token_balance[base_token]; 
    uint256 traded_token_balance_ = token_balance[traded_token];
    uint256 base_token_balance_plus_amount_ = base_token_balance_ + _amount;
    return (_amount*traded_token_balance_*(base_token_balance_plus_amount_ + base_token_balance_))/(2*base_token_balance_plus_amount_*base_token_balance_);
  }
  function get_amount_minus_fee(uint256 _amount) private view returns(uint256) {
    return (_amount*(1 ether - commission_ratio))/(1 ether);  
  }
  function complete_sell_exchange(uint256 _amount_give) private {
    uint256 amount_get_ = get_amount_sell(_amount_give);
    require(amount_get_ < token_balance[base_token]);
    uint256 amount_get_minus_fee_ = get_amount_minus_fee(amount_get_);
    uint256 admin_fee = amount_get_ - amount_get_minus_fee_;
    transferTokensThroughProxyToContract(msg.sender,this,_amount_give);
    transferETHFromContract(msg.sender,amount_get_minus_fee_);  
    transferETHFromContract(admin, admin_fee);     
  }
  function complete_buy_exchange() private {
    uint256 amount_give_ = msg.value;
    uint256 amount_get_ = get_amount_buy(amount_give_);
    require(amount_get_ < token_balance[traded_token]);
    uint256 amount_get_minus_fee_ = get_amount_minus_fee(amount_get_);
    uint256 admin_fee = amount_get_ - amount_get_minus_fee_;
    transferETHToContract();
    transferTokensFromContract(msg.sender, amount_get_minus_fee_);
    transferTokensFromContract(admin, admin_fee);
  }
  function sell_tokens(uint256 _amount_give) public {
    require(market_is_open());
    complete_sell_exchange(_amount_give);
  }
  function buy_tokens() private {
    require(market_is_open());
    complete_buy_exchange();
  }
  function() public payable {
    buy_tokens();
  }
}
```
