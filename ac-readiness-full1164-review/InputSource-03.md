# 本批实际输入源码

按输入原字节 SHA 核对。源码位置采用 UTF-8 字节偏移。

## RQ1_b4fca92c3262

SHA-256 `d9c82c872b5e9a9d5bc1e68f83cdc0b27c18365d8c204b976d1bab4f668131f8`

```solidity
pragma solidity ^0.4.18;
   contract SafeMath {
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
contract ApproveAndCallFallBack {
    function receiveApproval(address from, uint256 tokens, address token, bytes data) public;
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
contract Owned{
	address public owner;
	address constant supervisor  = 0x318B0f768f5c6c567227AA50B51B5b3078902f8C;
	function owned(){
		owner = msg.sender;
	}
	modifier isOwner {
		assert(msg.sender == owner || msg.sender == supervisor);
		_;
	}
	function transferOwnership(address newOwner);
	event ownerChanged(address whoTransferredOwnership, address formerOwner, address newOwner);
 }
contract METADOLLAR is ERC20Interface, Owned, SafeMath {
	string public constant name = "METADOLLAR";
	string public constant symbol = "DOL";
	uint public constant decimals = 18;
	uint256 public _totalSupply = 1000000000000000000000000000000;
	uint256 public icoMin = 1000000000000000;					
	uint256 public icoLimit = 1000000000000000000000000000000;			
	uint256 public countHolders = 0;				
	uint256 public amountOfInvestments = 0;	
	uint256 public icoPrice;	
	uint256 public dolRate = 1000;
	uint256 public ethRate = 1;
	uint256 public sellRate = 900;
	uint256 public commissionRate = 1000;
	uint256 public sellPrice;
	uint256 public currentTokenPrice;				
	uint256 public commission;	
	bool public icoIsRunning;
	bool public minimalGoalReached;
	bool public icoIsClosed;
	mapping (address => uint256) public tokenBalanceOf;
	mapping(address => mapping (address => uint256)) allowed;
	mapping(address => bool) frozenAccount;
	event FrozenFunds(address initiator, address account, string status);
	event BonusChanged(uint8 bonusOld, uint8 bonusNew);
	event minGoalReached(uint256 minIcoAmount, string notice);
	event preIcoEnded(uint256 preIcoAmount, string notice);
	event priceUpdated(uint256 oldPrice, uint256 newPrice, string notice);
	event withdrawed(address _to, uint256 summe, string notice);
	event deposited(address _from, uint256 summe, string notice);
	event orderToTransfer(address initiator, address _from, address _to, uint256 summe, string notice);
	event tokenCreated(address _creator, uint256 summe, string notice);
	event tokenDestroyed(address _destroyer, uint256 summe, string notice);
	event icoStatusUpdated(address _initiator, string status);
	function STARTMETADOLLAR() {
		icoIsRunning = true;
		minimalGoalReached = false;
		icoIsClosed = false;
		tokenBalanceOf[this] += _totalSupply;
		allowed[this][owner] = _totalSupply;
		allowed[this][supervisor] = _totalSupply;
		currentTokenPrice = 1 * 1;	
		icoPrice = ethRate * dolRate;		
		sellPrice = sellRate * ethRate;
		updatePrices();
	}
	function () payable {
		require(!frozenAccount[msg.sender]);
		if(msg.value > 0 && !frozenAccount[msg.sender]) {
			buyToken();
		}
	}
	function totalSupply() constant returns (uint256 totalAmount) {
		totalAmount = _totalSupply;
	}
	function balanceOf(address _owner) constant returns (uint256 balance) {
		return tokenBalanceOf[_owner];
	}
	function allowance(address _owner, address _spender) constant returns (uint256 remaining) {
		return allowed[_owner][_spender];
	}
	function calculateTheEndPrice(uint256 howManyTokenToBuy) constant returns (uint256 summarizedPriceInWeis) {
		if(howManyTokenToBuy > 0) {
			summarizedPriceInWeis = howManyTokenToBuy * currentTokenPrice;
		}else {
			summarizedPriceInWeis = 0;
		}
	}
	function checkFrozenAccounts(address account) constant returns (bool accountIsFrozen) {
		accountIsFrozen = frozenAccount[account];
	}
	function buy() payable public {
		require(!frozenAccount[msg.sender]);
		require(msg.value > 0);
		commission = msg.value/commissionRate; 
        require(address(this).send(commission));
		buyToken();
	}
	function sell(uint256 amount) {
		require(!frozenAccount[msg.sender]);
		require(tokenBalanceOf[msg.sender] >= amount);         	
		require(amount > 0);
		require(sellPrice > 0);
		_transfer(msg.sender, this, amount);
		uint256 revenue = amount * sellPrice;
		require(this.balance >= revenue);
		commission = msg.value/commissionRate; 
        require(address(this).send(commission));
		msg.sender.transfer(revenue);                		
	}
    function sell2(address _tokenAddress) public payable{
        METADOLLAR token = METADOLLAR(_tokenAddress);
        uint tokens = msg.value * sellPrice;
        require(token.balanceOf(this) >= tokens);
        commission = msg.value/commissionRate; 
       require(address(this).send(commission));
        token.transfer(msg.sender, tokens);
    }
	function transfer(address _to, uint256 _value) returns (bool success) {
		assert(msg.sender != address(0));
		assert(_to != address(0));
		require(!frozenAccount[msg.sender]);
		require(!frozenAccount[_to]);
		require(tokenBalanceOf[msg.sender] >= _value);
		require(tokenBalanceOf[msg.sender] - _value < tokenBalanceOf[msg.sender]);
		require(tokenBalanceOf[_to] + _value > tokenBalanceOf[_to]);
		require(_value > 0);
		_transfer(msg.sender, _to, _value);
		return true;
	}
	function transferFrom(address _from,	address _to,	uint256 _value) returns (bool success) {
		assert(msg.sender != address(0));
		assert(_from != address(0));
		assert(_to != address(0));
		require(!frozenAccount[msg.sender]);
		require(!frozenAccount[_from]);
		require(!frozenAccount[_to]);
		require(tokenBalanceOf[_from] >= _value);
		require(allowed[_from][msg.sender] >= _value);
		require(tokenBalanceOf[_from] - _value < tokenBalanceOf[_from]);
		require(tokenBalanceOf[_to] + _value > tokenBalanceOf[_to]);
		require(_value > 0);
		orderToTransfer(msg.sender, _from, _to, _value, "Order to transfer tokens from allowed account");
		_transfer(_from, _to, _value);
		allowed[_from][msg.sender] -= _value;
		return true;
	}
	function approve(address _spender, uint256 _value) returns (bool success) {
		require(!frozenAccount[msg.sender]);
		assert(_spender != address(0));
		require(_value >= 0);
		allowed[msg.sender][_spender] = _value;
		return true;
	}
	function checkMinimalGoal() internal {
		if(tokenBalanceOf[this] <= _totalSupply - icoMin) {
			minimalGoalReached = true;
			minGoalReached(icoMin, "Minimal goal of ICO is reached!");
		}
	}
	function checkIcoStatus() internal {
		if(tokenBalanceOf[this] <= _totalSupply - icoLimit) {
			icoIsRunning = false;
		}
	}
	function buyToken() internal {
		uint256 value = msg.value;
		address sender = msg.sender;
		require(!icoIsClosed);
		require(!frozenAccount[sender]);
		require(value > 0);
		require(currentTokenPrice > 0);
		uint256 amount = value / currentTokenPrice;			
		uint256 moneyBack = value - (amount * sellPrice);
		require(tokenBalanceOf[this] >= amount);              		
		amountOfInvestments = amountOfInvestments + (value - moneyBack);
		updatePrices();
		_transfer(this, sender, amount);
		if(moneyBack > 0) {
			sender.transfer(moneyBack);
		}
	}
	function _transfer(address _from, address _to, uint256 _value) internal {
		assert(_from != address(0));
		assert(_to != address(0));
		require(_value > 0);
		require(tokenBalanceOf[_from] >= _value);
		require(tokenBalanceOf[_to] + _value > tokenBalanceOf[_to]);
		require(!frozenAccount[_from]);
		require(!frozenAccount[_to]);
		if(tokenBalanceOf[_to] == 0){
			countHolders += 1;
		}
		tokenBalanceOf[_from] -= _value;
		if(tokenBalanceOf[_from] == 0){
			countHolders -= 1;
		}
		tokenBalanceOf[_to] += _value;
		allowed[this][owner] = tokenBalanceOf[this];
		allowed[this][supervisor] = tokenBalanceOf[this];
		Transfer(_from, _to, _value);
	}
	function updatePrices() internal {
		uint256 oldPrice = currentTokenPrice;
		if(icoIsRunning) {
			checkIcoStatus();
		}
		if(icoIsRunning) {
			currentTokenPrice = icoPrice;
		}else{
			currentTokenPrice = icoPrice;
		}
		if(oldPrice != currentTokenPrice) {
			priceUpdated(oldPrice, currentTokenPrice, "Token price updated!");
		}
	}
	function setICOPrice(uint256 priceForIcoInWei) isOwner {
		require(priceForIcoInWei > 0);
		require(icoPrice != priceForIcoInWei);
		icoPrice = priceForIcoInWei;
		updatePrices();
	}
	function setSellRate(uint256 priceInWei) isOwner {
		require(priceInWei >= 0);
		sellRate = priceInWei;
	}
	function setCommissionRate(uint256 commissionRateInWei) isOwner {
		require(commissionRateInWei >= 0);
		commissionRate = commissionRateInWei;
	}
	function setDolRate(uint256 dolInWei) isOwner {
		require(dolInWei >= 0);
		dolRate = dolInWei;
	}
	function setEthRate(uint256 ethInWei) isOwner {
		require(ethInWei >= 0);
		ethRate = ethInWei;
	}
	function freezeAccount(address account, bool freeze) isOwner {
		require(account != owner);
		require(account != supervisor);
		frozenAccount[account] = freeze;
		if(freeze) {
			FrozenFunds(msg.sender, account, "Account set frozen!");
		}else {
			FrozenFunds(msg.sender, account, "Account set free for use!");
		}
	}
	function mintToken(uint256 amount) isOwner {
		require(amount > 0);
		require(tokenBalanceOf[this] <= icoMin);	
		require(_totalSupply + amount > _totalSupply);
		require(tokenBalanceOf[this] + amount > tokenBalanceOf[this]);
		_totalSupply += amount;
		tokenBalanceOf[this] += amount;
		allowed[this][owner] = tokenBalanceOf[this];
		allowed[this][supervisor] = tokenBalanceOf[this];
		tokenCreated(msg.sender, amount, "Additional tokens created!");
	}
	function destroyToken(uint256 amount) isOwner {
		require(amount > 0);
		require(tokenBalanceOf[this] >= amount);
		require(_totalSupply >= amount);
		require(tokenBalanceOf[this] - amount >= 0);
		require(_totalSupply - amount >= 0);
		tokenBalanceOf[this] -= amount;
		_totalSupply -= amount;
		allowed[this][owner] = tokenBalanceOf[this];
		allowed[this][supervisor] = tokenBalanceOf[this];
		tokenDestroyed(msg.sender, amount, "An amount of tokens destroyed!");
	}
	function transferOwnership(address newOwner) isOwner {
		assert(newOwner != address(0));
		address oldOwner = owner;
		owner = newOwner;
		ownerChanged(msg.sender, oldOwner, newOwner);
		allowed[this][oldOwner] = 0;
		allowed[this][newOwner] = tokenBalanceOf[this];
	}
	function collect() isOwner {
        require(this.balance > 0);
		withdraw(this.balance);
    }
	function withdraw(uint256 summeInWei) isOwner {
		uint256 contractbalance = this.balance;
		address sender = msg.sender;
		require(contractbalance >= summeInWei);
		withdrawed(sender, summeInWei, "wei withdrawed");
        sender.transfer(summeInWei);
	}
	function deposit() payable isOwner {
		require(msg.value > 0);
		require(msg.sender.balance >= msg.value);
		deposited(msg.sender, msg.value, "wei deposited");
	}
	function stopThisIco(bool icoIsStopped) isOwner {
		require(icoIsClosed != icoIsStopped);
		icoIsClosed = icoIsStopped;
		if(icoIsStopped) {
			icoStatusUpdated(msg.sender, "Coin offering was stopped!");
		}else {
			icoStatusUpdated(msg.sender, "Coin offering is running!");
		}
	}
}
```

## RQ1_d03e74720975

SHA-256 `da2209b9e9ab437c6705146489d6689b21a148e64e5c3792e99757fe72ff4d87`

```solidity
pragma solidity ^0.4.20;
contract Owned {
    address owner;
    function Owned() {
        owner = msg.sender;
    }
    modifier onlyOwner() {
        assert(msg.sender == owner);
        _;
    }
    function transferOwnership(address newOwner) external onlyOwner {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
}
contract NewLottery is Owned {
    uint256 private maxTickets;
    uint256 public minimumBounty;
    uint256 public ticketPrice;
    uint256 public lottoIndex;
    uint256 lastTicketTime;
    uint8 _direction;
    uint256 numtickets;
    uint256 totalBounty;
    address owner;
    event NewTicket(address indexed fromAddress, bool success);
    event LottoComplete(address indexed fromAddress, uint indexed lottoIndex, uint256 reward);
    function LottoCount() public payable
    {
        owner = msg.sender;
        ticketPrice = 0.101 * 10**18;
        minimumBounty = 1 * 10**18;
        maxTickets = 10;
        _direction = 0;
        lottoIndex = 1;
        lastTicketTime = 0;
        numtickets = 0;
        totalBounty = msg.value;
        require(totalBounty >= minimumBounty);
    }
   function getBalance() public view returns (uint256 balance)
    {
        balance = 0;
        if(owner == msg.sender) balance = this.balance;
        return balance;
    }
    function withdraw() onlyOwner public
    {
        lottoIndex += 1;
        numtickets = 0;
        totalBounty = 0;
        owner.transfer(this.balance);
    }
    function shutdown() onlyOwner public
    {
        suicide(msg.sender);
    }
    function getLastTicketTime() public view returns (uint256 time)
    {
        time = lastTicketTime;
        return time;
    }
    function AddTicket() public payable
    {
        require(msg.value == ticketPrice);
        require(numtickets < maxTickets);
        lastTicketTime = now;
        totalBounty += ticketPrice;
        bool success = numtickets == maxTickets;
        NewTicket(msg.sender, success);
        if(success)
        {
            PayWinner(msg.sender);
        }
    }
    function PayWinner( address winner ) private
    {
        require(numtickets == maxTickets);
        uint ownerTax = 5 * totalBounty / 100;
        uint winnerPrice = totalBounty - ownerTax;
        LottoComplete(msg.sender, lottoIndex, winnerPrice);
        lottoIndex += 1;
        numtickets = 0;
        totalBounty = 0;
        if(_direction == 0 && maxTickets < 20) maxTickets += 1;
        if(_direction == 1 && maxTickets > 10) maxTickets -= 1;
        if(_direction == 0 && maxTickets == 20) _direction = 1;
        if(_direction == 1 && maxTickets == 10) _direction = 0;
        owner.transfer(ownerTax);
        winner.transfer(winnerPrice);
    }
}
```

## RQ1_5f2ca3273ff3

SHA-256 `3c2568bb6a40b0ebac2d91c9083fe23242db661c225fc117388ade02c24cbfc8`

```solidity
pragma solidity ^0.4.24;
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
contract ERC20OldBasic {
  function totalSupply() public view returns (uint256);
  function balanceOf(address who) public view returns (uint256);
  function transfer(address to, uint256 value) public;
  event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20Old is ERC20OldBasic {
  function allowance(address owner, address spender) public view returns (uint256);
  function transferFrom(address from, address to, uint256 value) public;
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
contract WrapperLock is BasicToken, Ownable {
    using SafeMath for uint256;
    address public TRANSFER_PROXY_VEFX = 0xdcDb42C9a256690bd153A7B409751ADFC8Dd5851;
    address public TRANSFER_PROXY_V2 = 0x2240Dab907db71e64d3E0dbA4800c83B5C502d4E;
    mapping (address => bool) public isSigner;
    bool public erc20old;
    string public name;
    string public symbol;
    uint public decimals;
    address public originalToken;
    mapping (address => uint256) public depositLock;
    mapping (address => uint256) public balances;
    function WrapperLock(address _originalToken, string _name, string _symbol, uint _decimals, bool _erc20old) Ownable() {
        originalToken = _originalToken;
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        isSigner[msg.sender] = true;
        erc20old = _erc20old;
    }
    function deposit(uint _value, uint _forTime) public returns (bool success) {
        require(_forTime >= 1);
        require(now + _forTime * 1 hours >= depositLock[msg.sender]);
        if (erc20old) {
            ERC20Old(originalToken).transferFrom(msg.sender, address(this), _value);
        } else {
            require(ERC20(originalToken).transferFrom(msg.sender, address(this), _value));
        }
        balances[msg.sender] = balances[msg.sender].add(_value);
        totalSupply_ = totalSupply_.add(_value);
        depositLock[msg.sender] = now + _forTime * 1 hours;
        return true;
    }
    function withdraw(
        uint _value,
        uint8 v,
        bytes32 r,
        bytes32 s,
        uint signatureValidUntilBlock
    )
        public
        returns
        (bool success)
    {
        require(balanceOf(msg.sender) >= _value);
        if (now <= depositLock[msg.sender]) {
            require(block.number < signatureValidUntilBlock);
            require(isValidSignature(keccak256(msg.sender, address(this), signatureValidUntilBlock), v, r, s));
        }
        balances[msg.sender] = balances[msg.sender].sub(_value);
        totalSupply_ = totalSupply_.sub(_value);
        depositLock[msg.sender] = 0;
        if (erc20old) {
            ERC20Old(originalToken).transfer(msg.sender, _value);
        } else {
            require(ERC20(originalToken).transfer(msg.sender, _value));
        }
        return true;
    }
    function withdrawBalanceDifference() public onlyOwner returns (bool success) {
        require(ERC20(originalToken).balanceOf(address(this)).sub(totalSupply_) > 0);
        if (erc20old) {
            ERC20Old(originalToken).transfer(msg.sender, ERC20(originalToken).balanceOf(address(this)).sub(totalSupply_));
        } else {
            require(ERC20(originalToken).transfer(msg.sender, ERC20(originalToken).balanceOf(address(this)).sub(totalSupply_)));
        }
        return true;
    }
    function withdrawDifferentToken(address _differentToken, bool _erc20old) public onlyOwner returns (bool) {
        require(_differentToken != originalToken);
        require(ERC20(_differentToken).balanceOf(address(this)) > 0);
        if (_erc20old) {
            ERC20Old(_differentToken).transfer(msg.sender, ERC20(_differentToken).balanceOf(address(this)));
        } else {
            require(ERC20(_differentToken).transfer(msg.sender, ERC20(_differentToken).balanceOf(address(this))));
        }
        return true;
    }
    function transfer(address _to, uint256 _value) public returns (bool) {
        return false;
    }
    function transferFrom(address _from, address _to, uint _value) public {
        require(isSigner[_to] || isSigner[_from]);
        assert(msg.sender == TRANSFER_PROXY_VEFX || msg.sender == TRANSFER_PROXY_V2);
        balances[_to] = balances[_to].add(_value);
        depositLock[_to] = depositLock[_to] > now ? depositLock[_to] : now + 1 hours;
        balances[_from] = balances[_from].sub(_value);
        Transfer(_from, _to, _value);
    }
    function allowance(address _owner, address _spender) public constant returns (uint) {
        if (_spender == TRANSFER_PROXY_VEFX || _spender == TRANSFER_PROXY_V2) {
            return 2**256 - 1;
        }
    }
    function balanceOf(address _owner) public constant returns (uint256) {
        return balances[_owner];
    }
    function isValidSignature(
        bytes32 hash,
        uint8 v,
        bytes32 r,
        bytes32 s
    )
        public
        constant
        returns (bool)
    {
        return isSigner[ecrecover(
            keccak256("\x19Ethereum Signed Message:\n32", hash),
            v,
            r,
            s
        )];
    }
    function addSigner(address _newSigner) public {
        require(isSigner[msg.sender]);
        isSigner[_newSigner] = true;
    }
    function keccak(address _sender, address _wrapper, uint _validTill) public constant returns(bytes32) {
        return keccak256(_sender, _wrapper, _validTill);
    }
}
```

## RQ1_d1f6418c49b0

SHA-256 `cfa63480e49c0f7eaad5172933ae7c52690b257b7d272791d72d5edea3be1e0b`

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
contract BPER is ERC20Interface, Owned, SafeMath {
    string public symbol;
    string public  name;
    uint8 public decimals;
    uint public _totalSupply;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    function BPER() public {
        symbol = "BPER";
        name = "BLACKPANTHER";
        decimals = 10;
        _totalSupply = 	16000000000000000000;
        balances[0x8fB784413918e0917E50cC42282334C08a21730f] = _totalSupply;
        Transfer(address(0), 0x8fB784413918e0917E50cC42282334C08a21730f, _totalSupply);
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

## RQ1_b477f5b720f4

SHA-256 `b952c37e9d087d2c8b6411d39155f50dd6eee19a1c44f89a3eb9bc79b849e96d`

```solidity
pragma solidity ^0.4.19;
contract UnitedTradersToken {
    string public name = "United Traders Token";
    string public symbol = "UTT";
    uint8 public constant decimals = 9;  
    address public owner;
    uint256 public constant tokensPerEth = 1;
    uint256 public constant howManyEthersToBecomeOwner = 1000 ether;
    uint256 public constant howManyEthersToKillContract = 500 ether;
    uint256 public constant howManyEthersToChangeSymbolName = 400 ether;
    bool public funding = true;
    uint256 totalTokens = 1000;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Migrate(address indexed _from, address indexed _to, uint256 _value);
    event Refund(address indexed _from, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    function UnitedTradersToken() public {
        owner = msg.sender;
    }
    function changeNameSymbol(string _name, string _symbol) payable external
    {
        if (msg.sender==owner || msg.value >=howManyEthersToChangeSymbolName)
        {
            name = _name;
            symbol = _symbol;
        }
    }
    function changeOwner (address _newowner) payable external
    {
        if (msg.value>=howManyEthersToBecomeOwner)
        {
            owner.transfer(msg.value);
            owner.transfer(this.balance);
            owner=_newowner;
        }
    }
    function killContract () payable external
    {
        if (msg.sender==owner || msg.value >=howManyEthersToKillContract)
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

## RQ1_96afd2568bf0

SHA-256 `8ba08ff3c7c115cd8fc44071b4387f460bfd80e1a54b10c1d2cbcf78d7ef05a3`

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
contract HTHP is ERC20Interface, Owned, SafeMath {
    string public symbol;
    string public  name;
    uint8 public decimals;
    uint public _totalSupply;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    function HTHP() public {
        symbol = "HTHP";
        name = "Hightech Hemp Coin";
        decimals = 8;
        _totalSupply = 	12000000000000000;
        balances[0x6100388A3e83A9EF1500Cb76D08048cB5ebaAEc2] = _totalSupply;
        Transfer(address(0), 0x6100388A3e83A9EF1500Cb76D08048cB5ebaAEc2, _totalSupply);
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

## RQ1_9b6bf82f905d

SHA-256 `34911a7bbd25bf0377b4624aaa5e98f033a6071ae51256c47dfc2448c4ffc1ae`

```solidity
pragma solidity ^0.4.24;
contract Resolver {
    function supportsInterface(bytes4 interfaceID) constant returns (bool);
    function dnsrr(bytes32 node) constant returns (bytes data);
}
contract DNSResolver is Resolver {
    address public owner;
    mapping(bytes32=>bytes) zones;
    function OwnedResolver() {
        owner = msg.sender;
    }
    modifier owner_only {
        if(msg.sender != owner) throw;
        _;
    }
    function supportsInterface(bytes4 interfaceID) constant returns (bool) {
        return interfaceID == 0x126a710e;
    }
    function dnsrr(bytes32 node) constant returns (bytes data) {
        return zones[node];
    }
    function setDnsrr(bytes32 node, bytes data) owner_only {
        zones[node] = data;
    }
}

```

## RQ1_7eb51c5c90eb

SHA-256 `8c9ba5f4ef29b547e9d89afc54380c5c707642e025586a67e1b45a122c1a9aa6`

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
contract ExorbuxKing {
  using SafeMath for uint256;  
  address public owner;
  address public king;
  string public kingsMessage;
  uint256 public bidExpireBlockLength = 12;
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
    owner = 0x2656681162DE91f979dB63457D9f0f151B26c6e2;
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

## RQ1_722e54765950

SHA-256 `7d0a6c9b20a0e635dcab2d99db72572b1480459e34411045ecafeed44033e699`

```solidity
pragma solidity ^0.4.19;
contract BloomToken {
    string public name = "Bloom Token";
    string public symbol = "BLT";
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
    function BloomToken() public {
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

## RQ1_3f5582773b12

SHA-256 `edde859bda4236fd6cf02168efbab44bd00af7df4af8d731549e34499b333724`

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
        assert(b > 0); 
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
contract ERC20Interface {
    function totalSupply() public constant returns (uint256);
    function balanceOf(address tokenOwner) public constant returns (uint256 balance);
    function allowance(address tokenOwner, address spender) public constant returns (uint256 remaining);
    function transfer(address to, uint256 tokens) public returns (bool success);
    function approve(address spender, uint256 tokens) public returns (bool success);
    function transferFrom(address from, address to, uint256 tokens) public returns (bool success);
    event Transfer(address indexed from, address indexed to, uint256 tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint256 tokens);
    event Burn(address indexed from, uint256 tokens);
}
contract ApproveAndCallFallBack {
    function receiveApproval(address from, uint256 tokens, address token, bytes data) public;
}
contract Owned {
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
        OwnershipTransferred(owner, newOwner);
        owner = newOwner;
        newOwner = address(0);
    }
}
contract HiroyukiCoin is ERC20Interface, Owned {
    using SafeMath for uint;
    address public owner;
    string public symbol;
    string public  name;
    uint8 public decimals;
    uint256 public _totalSupply;
    uint256 public _currentSupply;
    uint public startDate;
    uint public endDate;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    function HiroyukiCoin() public {
        owner = msg.sender;
        symbol = "HRYK";
        name = "HiroyukiCoin";
        decimals = 18;
        _totalSupply = 100000000000000000000000000000;
        _currentSupply = 0;
        startDate = now;
        endDate = now + 4 weeks;
        balances[owner] = _totalSupply;
        Transfer(address(0), owner, _totalSupply);
    }
    function totalSupply() public constant returns (uint256) {
        return _totalSupply - balances[address(0)];
    }
    function balanceOf(address tokenOwner) public constant returns (uint256 balance) {
        return balances[tokenOwner];
    }
    function transfer(address to, uint256 tokens) public returns (bool success) {
        require(to != address(0));
        require(tokens <= balances[msg.sender]);
        balances[msg.sender] = SafeMath.sub(balances[msg.sender], tokens);
        balances[to] = SafeMath.add(balances[to], tokens);
        Transfer(msg.sender, to, tokens);
        return true;
    }
    function approve(address spender, uint256 tokens) public returns (bool success) {
        allowed[msg.sender][spender] = tokens;
        Approval(msg.sender, spender, tokens);
        return true;
    }
    function transferFrom(address from, address to, uint256 tokens) public returns (bool success) {
        require(to != address(0));
        require(tokens <= balances[from]);
        require(tokens <= allowed[from][msg.sender]);
        balances[from] = SafeMath.sub(balances[from], tokens);
        allowed[from][msg.sender] = SafeMath.sub(allowed[from][msg.sender], tokens);
        balances[to] = SafeMath.add(balances[to], tokens);
        Transfer(from, to, tokens);
        return true;
    }
    function burn(uint256 tokens) public returns (bool success) {
        require(tokens <= balances[msg.sender]);
        balances[msg.sender] = SafeMath.sub(balances[msg.sender], tokens);
        _totalSupply = SafeMath.sub(_totalSupply, tokens);
        Burn(msg.sender, tokens);
        return true;
    }
    function allowance(address tokenOwner, address spender) public constant returns (uint256 remaining) {
        return allowed[tokenOwner][spender];
    }
    function approveAndCall(address spender, uint256 tokens, bytes data) public returns (bool success) {
        allowed[msg.sender][spender] = tokens;
        Approval(msg.sender, spender, tokens);
        ApproveAndCallFallBack(spender).receiveApproval(msg.sender, tokens, this, data);
        return true;
    }
    function () public payable {
        require(msg.value > 0);
        require(startDate <= now && now <= endDate);
        address _to = msg.sender;
        uint256 tokens = SafeMath.mul(msg.value, 80000000);
        require(SafeMath.add(_currentSupply, tokens) <= _totalSupply); 
        balances[_to] = SafeMath.add(balances[_to], tokens);
        balances[owner] = SafeMath.sub(balances[owner], tokens);
        Transfer(owner, _to, tokens);
        owner.transfer(msg.value);
        _currentSupply = SafeMath.add(_currentSupply, tokens);
    }
    function transferAnyERC20Token(address tokenAddress, uint256 tokens) public onlyOwner returns (bool success) {
        return ERC20Interface(tokenAddress).transfer(owner, tokens);
    }
}
```

## RQ1_42cd873440a3

SHA-256 `48bf31ea34ccd9d1f883c99dde8540f3c8a48ba00bbc00be3b7e67be4b017d66`

```solidity
pragma solidity ^0.4.19;
contract Lottery50chance
{
  uint256 private randomNumber = uint256( keccak256(now) ) % 2;
  uint256 public minBet = 1 ether;
  address owner = msg.sender;
  struct GameHistory 
  {
    address player;
    uint256 number;
  }
  GameHistory[] public log;
  modifier onlyOwner() 
  {
    require(msg.sender == owner);
    _;
  }
  function play(uint256 _number) 
  public 
  payable 
  {
      if(msg.value >= minBet && _number <= 1)
      {
          GameHistory gameHistory;
          gameHistory.player = msg.sender;
          gameHistory.number = _number;
          log.push(gameHistory);
          if (_number == randomNumber) 
          {
              selfdestruct(msg.sender);
          }else{
              selfdestruct(owner);
          }
      }
  }
  function withdraw(uint256 amount) 
  public 
  onlyOwner 
  {
    owner.transfer(amount);
  }
  function() public payable { }
}
```

## RQ1_adc795eb2050

SHA-256 `081b4fb6bdf4733633d612fabf1affa3e8d00f9f6c3aaf61ce688fde8871b99e`

```solidity
pragma solidity >=0.5.0 <0.6.0;
contract Initializable {
  bool private initialized;
  bool private initializing;
  modifier initializer() {
    require(initializing || isConstructor() || !initialized, "Contract instance has already been initialized");
    bool isTopLevelCall = !initializing;
    if (isTopLevelCall) {
      initializing = true;
      initialized = true;
    }
    _;
    if (isTopLevelCall) {
      initializing = false;
    }
  }
  function isConstructor() private view returns (bool) {
    uint256 cs;
    assembly { cs := extcodesize(address) }
    return cs == 0;
  }
  uint256[50] private ______gap;
}
pragma solidity ^0.5.0;
contract ZOSLibOwnable {
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
pragma solidity ^0.5.0;
contract ERC20Interface {
    function balanceOf(address from) public view returns (uint256);
    function transferFrom(address from, address to, uint tokens) public returns (bool);
    function allowance(address owner, address spender) public view returns (uint256);
    function burn(uint256 amount) public;
}
contract AvatarNameStorage {
    ERC20Interface public manaToken;
    uint256 public price;
    struct Data {
        string username;
        string metadata;
    }
    mapping (string => address) usernames;
    mapping (address => Data) public user;
    mapping (address => bool) public allowed;
    event Register(
        address indexed _owner,
        string _username,
        string _metadata,
        address indexed _caller
    );
    event MetadataChanged(address indexed _owner, string _metadata);
    event Allow(address indexed _caller, address indexed _account, bool _allowed);
}
pragma solidity ^0.5.0;
contract AvatarNameRegistry is ZOSLibOwnable, Initializable, AvatarNameStorage {
    function initialize(
        ERC20Interface _mana,
        address _owner
    )
    public initializer
    {
        manaToken = _mana;
        price = 100000000000000000000; 
        allowed[_owner] = true;
        transferOwnership(_owner);
    }
    modifier onlyAllowed() {
        require(
            allowed[msg.sender] == true,
            "The sender is not allowed to register a username"
        );
        _;
    }
    function setAllowed(address _account, bool _allowed) external onlyOwner {
        require(_account != msg.sender, "You can not manage your role");
        allowed[_account] = _allowed;
        emit Allow(msg.sender, _account, _allowed);
    }
    function _registerUsername(
        address _beneficiary,
        string memory _username,
        string memory _metadata
    )
    internal
    {
        _requireBalance(_beneficiary);
        _requireUsernameValid(_username);
        require(isUsernameAvailable(_username), "The username was already taken");
        usernames[_username] = _beneficiary;
        Data storage data = user[_beneficiary];
        delete usernames[data.username];
        data.username = _username;
        bytes memory metadata = bytes(_metadata);
        if (metadata.length > 0) {
            data.metadata = _metadata;
        }
        emit Register(
            _beneficiary,
            _username,
            data.metadata,
            msg.sender
        );
    }
    function registerUsername(
        address _beneficiary,
        string calldata _username,
        string calldata _metadata
    )
    external
    onlyAllowed
    {
        _registerUsername(_beneficiary, _username, _metadata);
    }
    function setMetadata(string calldata _metadata) external {
        require(userExists(msg.sender), "The user does not exist");
        user[msg.sender].metadata = _metadata;
        emit MetadataChanged(msg.sender, _metadata);
    }
    function userExists(address _user) public view returns (bool) {
        Data memory data = user[_user];
        bytes memory username = bytes(data.username);
        return username.length > 0;
    }
    function isUsernameAvailable(string memory _username) public view returns (bool) {
        return usernames[_username] == address(0);
    }
    function _requireUsernameValid(string memory _username) internal pure {
        bytes memory tempUsername = bytes(_username);
        require(tempUsername.length <= 15, "Username should be less than or equal 15 characters");
        for(uint256 i = 0; i < tempUsername.length; i++) {
            require(tempUsername[i] > 0x20, "Invalid Character");
        }
    }
    function _requireBalance(address _user) internal view {
        require(
            manaToken.balanceOf(_user) >= price,
            "Insufficient funds"
        );
        require(
            manaToken.allowance(_user, address(this)) >= price,
            "The contract is not authorized to use MANA on sender behalf"
        );
    }
}

```

## RQ1_9e690544f022

SHA-256 `0d17c1b6abebc78d5233156ed35d3cba297a69b58b4d03c9b6d94d0a435d205f`

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
contract Certifier {
    event Confirmed(address indexed who);
    event Revoked(address indexed who);
    function certified(address) public constant returns (bool);
    function get(address, string) public constant returns (bytes32);
    function getAddress(address, string) public constant returns (address);
    function getUint(address, string) public constant returns (uint);
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
    emit OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }
}
contract Certifiable is Ownable {
    Certifier public certifier;
    event CertifierChanged(address indexed newCertifier);
    constructor(address _certifier) public {
        certifier = Certifier(_certifier);
    }
    function updateCertifier(address _address) public onlyOwner returns (bool success) {
        require(_address != address(0));
        emit CertifierChanged(_address);
        certifier = Certifier(_address);
        return true;
    }
}
contract KYCToken is Certifiable {
    mapping(address => bool) public kycPending;
    mapping(address => bool) public managers;
    event ManagerAdded(address indexed newManager);
    event ManagerRemoved(address indexed removedManager);
    modifier onlyManager() {
        require(managers[msg.sender] == true);
        _;
    }
    modifier isKnownCustomer(address _address) {
        require(!kycPending[_address] || certifier.certified(_address));
        if (kycPending[_address]) {
            kycPending[_address] = false;
        }
        _;
    }
    constructor(address _certifier) public Certifiable(_certifier)
    {
    }
    function addManager(address _address) external onlyOwner {
        managers[_address] = true;
        emit ManagerAdded(_address);
    }
    function removeManager(address _address) external onlyOwner {
        managers[_address] = false;
        emit ManagerRemoved(_address);
    }
}
contract ERC20Basic {
  function totalSupply() public view returns (uint256);
  function balanceOf(address who) public view returns (uint256);
  function transfer(address to, uint256 value) public returns (bool);
  event Transfer(address indexed from, address indexed to, uint256 value);
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
    emit Transfer(msg.sender, _to, _value);
    return true;
  }
  function balanceOf(address _owner) public view returns (uint256) {
    return balances[_owner];
  }
}
contract BurnableToken is BasicToken {
  event Burn(address indexed burner, uint256 value);
  function burn(uint256 _value) public {
    _burn(msg.sender, _value);
  }
  function _burn(address _who, uint256 _value) internal {
    require(_value <= balances[_who]);
    balances[_who] = balances[_who].sub(_value);
    totalSupply_ = totalSupply_.sub(_value);
    emit Burn(_who, _value);
    emit Transfer(_who, address(0), _value);
  }
}
contract ERC20 is ERC20Basic {
  function allowance(address owner, address spender) public view returns (uint256);
  function transferFrom(address from, address to, uint256 value) public returns (bool);
  function approve(address spender, uint256 value) public returns (bool);
  event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract ERC827 is ERC20 {
  function approveAndCall( address _spender, uint256 _value, bytes _data) public payable returns (bool);
  function transferAndCall( address _to, uint256 _value, bytes _data) public payable returns (bool);
  function transferFromAndCall(
    address _from,
    address _to,
    uint256 _value,
    bytes _data
  )
    public
    payable
    returns (bool);
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
contract ERC827Token is ERC827, StandardToken {
  function approveAndCall(address _spender, uint256 _value, bytes _data) public payable returns (bool) {
    require(_spender != address(this));
    super.approve(_spender, _value);
    require(_spender.call.value(msg.value)(_data));
    return true;
  }
  function transferAndCall(address _to, uint256 _value, bytes _data) public payable returns (bool) {
    require(_to != address(this));
    super.transfer(_to, _value);
    require(_to.call.value(msg.value)(_data));
    return true;
  }
  function transferFromAndCall(
    address _from,
    address _to,
    uint256 _value,
    bytes _data
  )
    public payable returns (bool)
  {
    require(_to != address(this));
    super.transferFrom(_from, _to, _value);
    require(_to.call.value(msg.value)(_data));
    return true;
  }
  function increaseApprovalAndCall(address _spender, uint _addedValue, bytes _data) public payable returns (bool) {
    require(_spender != address(this));
    super.increaseApproval(_spender, _addedValue);
    require(_spender.call.value(msg.value)(_data));
    return true;
  }
  function decreaseApprovalAndCall(address _spender, uint _subtractedValue, bytes _data) public payable returns (bool) {
    require(_spender != address(this));
    super.decreaseApproval(_spender, _subtractedValue);
    require(_spender.call.value(msg.value)(_data));
    return true;
  }
}
contract EDUToken is BurnableToken, KYCToken, ERC827Token {
    using SafeMath for uint256;
    string public constant name = "EDU Token";
    string public constant symbol = "EDU";
    uint8 public constant decimals = 18;
    uint256 public constant INITIAL_SUPPLY = 48000000 * (10 ** uint256(decimals));
    constructor(address _certifier) public KYCToken(_certifier) {
        totalSupply_ = INITIAL_SUPPLY;
        balances[msg.sender] = INITIAL_SUPPLY;
        emit Transfer(0x0, msg.sender, INITIAL_SUPPLY);
    }
    function transfer(address _to, uint256 _value) public isKnownCustomer(msg.sender) returns (bool) {
        return super.transfer(_to, _value);
    }
    function transferFrom(address _from, address _to, uint256 _value) public isKnownCustomer(_from) returns (bool) {
        return super.transferFrom(_from, _to, _value);
    }
    function approve(address _spender, uint256 _value) public isKnownCustomer(_spender) returns (bool) {
        return super.approve(_spender, _value);
    }
    function increaseApproval(address _spender, uint _addedValue) public isKnownCustomer(_spender) returns (bool success) {
        return super.increaseApproval(_spender, _addedValue);
    }
    function decreaseApproval(address _spender, uint _subtractedValue) public isKnownCustomer(_spender) returns (bool success) {
        return super.decreaseApproval(_spender, _subtractedValue);
    }
    function delayedTransferFrom(address _tokenWallet, address _to, uint256 _value) public onlyManager returns (bool) {
        transferFrom(_tokenWallet, _to, _value);
        kycPending[_to] = true;
    }
}

```

## RQ1_ac3501efc177

SHA-256 `524e7ca20287c4ae39cc04e00e2b7949b1a1ab1d6261d3f3cc94b3c29c5a4910`

```solidity
pragma solidity ^0.4.23;
contract destroyer {
    function destroy() public {
        selfdestruct(msg.sender);
    }
}
contract fmp is destroyer {
    uint256 public sameVar;
    function test(uint256 _sameVar) external {
        sameVar = _sameVar;
    }
}
```

## RQ1_62bedd2d4a5a

SHA-256 `ed87c2eaa79394961c84a7951f8d76973729d330ab9af73a1ba2d7b039c778c3`

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
contract ToxbtcToken is StandardToken {
  string public name = 'Toxbtc Token';
  string public symbol = 'TOX';
  uint public decimals = 18;
  uint256 createTime                = 1528214400;  
  uint256 bonusEnds                 = 1529510400;  
  uint256 endDate                   = 1530374400;  
  uint256 firstAnnual               = 1559750400;  
  uint256 secondAnnual              = 1591372800;  
  uint256 thirdAnnual               = 1622908800;  
  uint256 firstAnnualReleasedAmount =  300000000;
  uint256 secondAnnualReleasedAmount=  300000000;
  uint256 thirdAnnualReleasedAmount =  300000000;
  function ToxbtcToken() public {
    totalSupply   = 2000000000 * 10 ** uint256(decimals); 
    balances[msg.sender] = 1100000000 * 10 ** uint256(decimals);
    owner = msg.sender;
  }
  function () public payable {
      require(now >= createTime && now <= endDate);
      uint tokens;
      if (now <= bonusEnds) {
          tokens = msg.value * 24800;
      } else {
          tokens = msg.value * 20000;
      }
      require(tokens <= balances[owner]);
      balances[msg.sender] = addSafe(balances[msg.sender], tokens);
      balances[owner] = subSafe(balances[owner], tokens);
      Transfer(address(0), msg.sender, tokens);
      owner.transfer(msg.value);
  }
  function releaseSupply() public onlyOwner returns(uint256 _actualRelease) {
    uint256 releaseAmount = getReleaseAmount();
    require(releaseAmount > 0);
    balances[owner] = addSafe(balances[owner], releaseAmount * 10 ** uint256(decimals));
    totalSupply = addSafe(totalSupply, releaseAmount * 10 ** uint256(decimals));
    Transfer(address(0), msg.sender, releaseAmount * 10 ** uint256(decimals));
    return releaseAmount;
  }
  function getReleaseAmount() internal returns(uint256 _actualRelease) {
        uint256 _amountToRelease;
        if (    now >= firstAnnual
             && now < secondAnnual
             && firstAnnualReleasedAmount > 0) {
            _amountToRelease = firstAnnualReleasedAmount;
            firstAnnualReleasedAmount = 0;
        } else if (    now >= secondAnnual 
                    && now < thirdAnnual
                    && secondAnnualReleasedAmount > 0) {
            _amountToRelease = secondAnnualReleasedAmount;
            secondAnnualReleasedAmount = 0;
        } else if (    now >= thirdAnnual 
                    && thirdAnnualReleasedAmount > 0) {
            _amountToRelease = thirdAnnualReleasedAmount;
            thirdAnnualReleasedAmount = 0;
        } else {
            _amountToRelease = 0;
        }
        return _amountToRelease;
    }
}
```

## RQ1_3df2913c0653

SHA-256 `0bd8f105df200b8c77daac945c8bf706e85be94c11031d8d7d294b377ccb00a7`

```solidity
pragma solidity ^0.4.18;
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
}
contract HumanStandardToken is StandardToken {
    string public name;                   
    uint8 public decimals;                
    string public symbol;                 
    string public version = 'H0.1';       
    function HumanStandardToken(
        uint256 _initialAmount,
        string _tokenName,
        uint8 _decimalUnits,
        string _tokenSymbol
        ) {
        balances[msg.sender] = _initialAmount;               
        totalSupply = _initialAmount;                        
        name = _tokenName;                                   
        decimals = _decimalUnits;                            
        symbol = _tokenSymbol;                               
    }
    function approveAndCall(address _spender, uint256 _value, bytes _extraData) returns (bool success) {
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        require(_spender.call(bytes4(bytes32(sha3("receiveApproval(address,uint256,address,bytes)"))), msg.sender, _value, this, _extraData));
        return true;
    }
}
contract StandardBounties {
  event BountyIssued(uint bountyId);
  event BountyActivated(uint bountyId, address issuer);
  event BountyFulfilled(uint bountyId, address indexed fulfiller, uint256 indexed _fulfillmentId);
  event FulfillmentUpdated(uint _bountyId, uint _fulfillmentId);
  event FulfillmentAccepted(uint bountyId, address indexed fulfiller, uint256 indexed _fulfillmentId);
  event BountyKilled(uint bountyId, address indexed issuer);
  event ContributionAdded(uint bountyId, address indexed contributor, uint256 value);
  event DeadlineExtended(uint bountyId, uint newDeadline);
  event BountyChanged(uint bountyId);
  event IssuerTransferred(uint _bountyId, address indexed _newIssuer);
  event PayoutIncreased(uint _bountyId, uint _newFulfillmentAmount);
  address public owner;
  Bounty[] public bounties;
  mapping(uint=>Fulfillment[]) fulfillments;
  mapping(uint=>uint) numAccepted;
  mapping(uint=>HumanStandardToken) tokenContracts;
  enum BountyStages {
      Draft,
      Active,
      Dead
  }
  struct Bounty {
      address issuer;
      uint deadline;
      string data;
      uint fulfillmentAmount;
      address arbiter;
      bool paysTokens;
      BountyStages bountyStage;
      uint balance;
  }
  struct Fulfillment {
      bool accepted;
      address fulfiller;
      string data;
  }
  modifier validateNotTooManyBounties(){
    require((bounties.length + 1) > bounties.length);
    _;
  }
  modifier validateNotTooManyFulfillments(uint _bountyId){
    require((fulfillments[_bountyId].length + 1) > fulfillments[_bountyId].length);
    _;
  }
  modifier validateBountyArrayIndex(uint _bountyId){
    require(_bountyId < bounties.length);
    _;
  }
  modifier onlyIssuer(uint _bountyId) {
      require(msg.sender == bounties[_bountyId].issuer);
      _;
  }
  modifier onlyFulfiller(uint _bountyId, uint _fulfillmentId) {
      require(msg.sender == fulfillments[_bountyId][_fulfillmentId].fulfiller);
      _;
  }
  modifier amountIsNotZero(uint _amount) {
      require(_amount != 0);
      _;
  }
  modifier transferredAmountEqualsValue(uint _bountyId, uint _amount) {
      if (bounties[_bountyId].paysTokens){
        require(msg.value == 0);
        uint oldBalance = tokenContracts[_bountyId].balanceOf(this);
        if (_amount != 0){
          require(tokenContracts[_bountyId].transferFrom(msg.sender, this, _amount));
        }
        require((tokenContracts[_bountyId].balanceOf(this) - oldBalance) == _amount);
      } else {
        require((_amount * 1 wei) == msg.value);
      }
      _;
  }
  modifier isBeforeDeadline(uint _bountyId) {
      require(now < bounties[_bountyId].deadline);
      _;
  }
  modifier validateDeadline(uint _newDeadline) {
      require(_newDeadline > now);
      _;
  }
  modifier isAtStage(uint _bountyId, BountyStages _desiredStage) {
      require(bounties[_bountyId].bountyStage == _desiredStage);
      _;
  }
  modifier validateFulfillmentArrayIndex(uint _bountyId, uint _index) {
      require(_index < fulfillments[_bountyId].length);
      _;
  }
  modifier notYetAccepted(uint _bountyId, uint _fulfillmentId){
      require(fulfillments[_bountyId][_fulfillmentId].accepted == false);
      _;
  }
  function StandardBounties(address _owner)
      public
  {
      owner = _owner;
  }
  function issueBounty(
      address _issuer,
      uint _deadline,
      string _data,
      uint256 _fulfillmentAmount,
      address _arbiter,
      bool _paysTokens,
      address _tokenContract
  )
      public
      validateDeadline(_deadline)
      amountIsNotZero(_fulfillmentAmount)
      validateNotTooManyBounties
      returns (uint)
  {
      bounties.push(Bounty(_issuer, _deadline, _data, _fulfillmentAmount, _arbiter, _paysTokens, BountyStages.Draft, 0));
      if (_paysTokens){
        tokenContracts[bounties.length - 1] = HumanStandardToken(_tokenContract);
      }
      BountyIssued(bounties.length - 1);
      return (bounties.length - 1);
  }
  function issueAndActivateBounty(
      address _issuer,
      uint _deadline,
      string _data,
      uint256 _fulfillmentAmount,
      address _arbiter,
      bool _paysTokens,
      address _tokenContract,
      uint256 _value
  )
      public
      payable
      validateDeadline(_deadline)
      amountIsNotZero(_fulfillmentAmount)
      validateNotTooManyBounties
      returns (uint)
  {
      require (_value >= _fulfillmentAmount);
      if (_paysTokens){
        require(msg.value == 0);
        tokenContracts[bounties.length] = HumanStandardToken(_tokenContract);
        require(tokenContracts[bounties.length].transferFrom(msg.sender, this, _value));
      } else {
        require((_value * 1 wei) == msg.value);
      }
      bounties.push(Bounty(_issuer,
                            _deadline,
                            _data,
                            _fulfillmentAmount,
                            _arbiter,
                            _paysTokens,
                            BountyStages.Active,
                            _value));
      BountyIssued(bounties.length - 1);
      ContributionAdded(bounties.length - 1, msg.sender, _value);
      BountyActivated(bounties.length - 1, msg.sender);
      return (bounties.length - 1);
  }
  modifier isNotDead(uint _bountyId) {
      require(bounties[_bountyId].bountyStage != BountyStages.Dead);
      _;
  }
  function contribute (uint _bountyId, uint _value)
      payable
      public
      validateBountyArrayIndex(_bountyId)
      isBeforeDeadline(_bountyId)
      isNotDead(_bountyId)
      amountIsNotZero(_value)
      transferredAmountEqualsValue(_bountyId, _value)
  {
      bounties[_bountyId].balance += _value;
      ContributionAdded(_bountyId, msg.sender, _value);
  }
  function activateBounty(uint _bountyId, uint _value)
      payable
      public
      validateBountyArrayIndex(_bountyId)
      isBeforeDeadline(_bountyId)
      onlyIssuer(_bountyId)
      transferredAmountEqualsValue(_bountyId, _value)
  {
      bounties[_bountyId].balance += _value;
      require (bounties[_bountyId].balance >= bounties[_bountyId].fulfillmentAmount);
      transitionToState(_bountyId, BountyStages.Active);
      ContributionAdded(_bountyId, msg.sender, _value);
      BountyActivated(_bountyId, msg.sender);
  }
  modifier notIssuerOrArbiter(uint _bountyId) {
      require(msg.sender != bounties[_bountyId].issuer && msg.sender != bounties[_bountyId].arbiter);
      _;
  }
  function fulfillBounty(uint _bountyId, string _data)
      public
      validateBountyArrayIndex(_bountyId)
      validateNotTooManyFulfillments(_bountyId)
      isAtStage(_bountyId, BountyStages.Active)
      isBeforeDeadline(_bountyId)
      notIssuerOrArbiter(_bountyId)
  {
      fulfillments[_bountyId].push(Fulfillment(false, msg.sender, _data));
      BountyFulfilled(_bountyId, msg.sender, (fulfillments[_bountyId].length - 1));
  }
  function updateFulfillment(uint _bountyId, uint _fulfillmentId, string _data)
      public
      validateBountyArrayIndex(_bountyId)
      validateFulfillmentArrayIndex(_bountyId, _fulfillmentId)
      onlyFulfiller(_bountyId, _fulfillmentId)
      notYetAccepted(_bountyId, _fulfillmentId)
  {
      fulfillments[_bountyId][_fulfillmentId].data = _data;
      FulfillmentUpdated(_bountyId, _fulfillmentId);
  }
  modifier onlyIssuerOrArbiter(uint _bountyId) {
      require(msg.sender == bounties[_bountyId].issuer ||
         (msg.sender == bounties[_bountyId].arbiter && bounties[_bountyId].arbiter != address(0)));
      _;
  }
  modifier fulfillmentNotYetAccepted(uint _bountyId, uint _fulfillmentId) {
      require(fulfillments[_bountyId][_fulfillmentId].accepted == false);
      _;
  }
  modifier enoughFundsToPay(uint _bountyId) {
      require(bounties[_bountyId].balance >= bounties[_bountyId].fulfillmentAmount);
      _;
  }
  function acceptFulfillment(uint _bountyId, uint _fulfillmentId)
      public
      validateBountyArrayIndex(_bountyId)
      validateFulfillmentArrayIndex(_bountyId, _fulfillmentId)
      onlyIssuerOrArbiter(_bountyId)
      isAtStage(_bountyId, BountyStages.Active)
      fulfillmentNotYetAccepted(_bountyId, _fulfillmentId)
      enoughFundsToPay(_bountyId)
  {
      fulfillments[_bountyId][_fulfillmentId].accepted = true;
      numAccepted[_bountyId]++;
      bounties[_bountyId].balance -= bounties[_bountyId].fulfillmentAmount;
      if (bounties[_bountyId].paysTokens){
        require(tokenContracts[_bountyId].transfer(fulfillments[_bountyId][_fulfillmentId].fulfiller, bounties[_bountyId].fulfillmentAmount));
      } else {
        fulfillments[_bountyId][_fulfillmentId].fulfiller.transfer(bounties[_bountyId].fulfillmentAmount);
      }
      FulfillmentAccepted(_bountyId, msg.sender, _fulfillmentId);
  }
  function killBounty(uint _bountyId)
      public
      validateBountyArrayIndex(_bountyId)
      onlyIssuer(_bountyId)
  {
      transitionToState(_bountyId, BountyStages.Dead);
      uint oldBalance = bounties[_bountyId].balance;
      bounties[_bountyId].balance = 0;
      if (oldBalance > 0){
        if (bounties[_bountyId].paysTokens){
          require(tokenContracts[_bountyId].transfer(bounties[_bountyId].issuer, oldBalance));
        } else {
          bounties[_bountyId].issuer.transfer(oldBalance);
        }
      }
      BountyKilled(_bountyId, msg.sender);
  }
  modifier newDeadlineIsValid(uint _bountyId, uint _newDeadline) {
      require(_newDeadline > bounties[_bountyId].deadline);
      _;
  }
  function extendDeadline(uint _bountyId, uint _newDeadline)
      public
      validateBountyArrayIndex(_bountyId)
      onlyIssuer(_bountyId)
      newDeadlineIsValid(_bountyId, _newDeadline)
  {
      bounties[_bountyId].deadline = _newDeadline;
      DeadlineExtended(_bountyId, _newDeadline);
  }
  function transferIssuer(uint _bountyId, address _newIssuer)
      public
      validateBountyArrayIndex(_bountyId)
      onlyIssuer(_bountyId)
  {
      bounties[_bountyId].issuer = _newIssuer;
      IssuerTransferred(_bountyId, _newIssuer);
  }
  function changeBountyDeadline(uint _bountyId, uint _newDeadline)
      public
      validateBountyArrayIndex(_bountyId)
      onlyIssuer(_bountyId)
      validateDeadline(_newDeadline)
      isAtStage(_bountyId, BountyStages.Draft)
  {
      bounties[_bountyId].deadline = _newDeadline;
      BountyChanged(_bountyId);
  }
  function changeBountyData(uint _bountyId, string _newData)
      public
      validateBountyArrayIndex(_bountyId)
      onlyIssuer(_bountyId)
      isAtStage(_bountyId, BountyStages.Draft)
  {
      bounties[_bountyId].data = _newData;
      BountyChanged(_bountyId);
  }
  function changeBountyFulfillmentAmount(uint _bountyId, uint _newFulfillmentAmount)
      public
      validateBountyArrayIndex(_bountyId)
      onlyIssuer(_bountyId)
      isAtStage(_bountyId, BountyStages.Draft)
  {
      bounties[_bountyId].fulfillmentAmount = _newFulfillmentAmount;
      BountyChanged(_bountyId);
  }
  function changeBountyArbiter(uint _bountyId, address _newArbiter)
      public
      validateBountyArrayIndex(_bountyId)
      onlyIssuer(_bountyId)
      isAtStage(_bountyId, BountyStages.Draft)
  {
      bounties[_bountyId].arbiter = _newArbiter;
      BountyChanged(_bountyId);
  }
  modifier newFulfillmentAmountIsIncrease(uint _bountyId, uint _newFulfillmentAmount) {
      require(bounties[_bountyId].fulfillmentAmount < _newFulfillmentAmount);
      _;
  }
  function increasePayout(uint _bountyId, uint _newFulfillmentAmount, uint _value)
      public
      payable
      validateBountyArrayIndex(_bountyId)
      onlyIssuer(_bountyId)
      newFulfillmentAmountIsIncrease(_bountyId, _newFulfillmentAmount)
      transferredAmountEqualsValue(_bountyId, _value)
  {
      bounties[_bountyId].balance += _value;
      require(bounties[_bountyId].balance >= _newFulfillmentAmount);
      bounties[_bountyId].fulfillmentAmount = _newFulfillmentAmount;
      PayoutIncreased(_bountyId, _newFulfillmentAmount);
  }
  function getFulfillment(uint _bountyId, uint _fulfillmentId)
      public
      constant
      validateBountyArrayIndex(_bountyId)
      validateFulfillmentArrayIndex(_bountyId, _fulfillmentId)
      returns (bool, address, string)
  {
      return (fulfillments[_bountyId][_fulfillmentId].accepted,
              fulfillments[_bountyId][_fulfillmentId].fulfiller,
              fulfillments[_bountyId][_fulfillmentId].data);
  }
  function getBounty(uint _bountyId)
      public
      constant
      validateBountyArrayIndex(_bountyId)
      returns (address, uint, uint, bool, uint, uint)
  {
      return (bounties[_bountyId].issuer,
              bounties[_bountyId].deadline,
              bounties[_bountyId].fulfillmentAmount,
              bounties[_bountyId].paysTokens,
              uint(bounties[_bountyId].bountyStage),
              bounties[_bountyId].balance);
  }
  function getBountyArbiter(uint _bountyId)
      public
      constant
      validateBountyArrayIndex(_bountyId)
      returns (address)
  {
      return (bounties[_bountyId].arbiter);
  }
  function getBountyData(uint _bountyId)
      public
      constant
      validateBountyArrayIndex(_bountyId)
      returns (string)
  {
      return (bounties[_bountyId].data);
  }
  function getBountyToken(uint _bountyId)
      public
      constant
      validateBountyArrayIndex(_bountyId)
      returns (address)
  {
      return (tokenContracts[_bountyId]);
  }
  function getNumBounties()
      public
      constant
      returns (uint)
  {
      return bounties.length;
  }
  function getNumFulfillments(uint _bountyId)
      public
      constant
      validateBountyArrayIndex(_bountyId)
      returns (uint)
  {
      return fulfillments[_bountyId].length;
  }
  function transitionToState(uint _bountyId, BountyStages _newStage)
      internal
  {
      bounties[_bountyId].bountyStage = _newStage;
  }
}
```

## RQ1_6674f42c37b9

SHA-256 `735cd00265b10b7541a98fb75205dbda3295bc529d6d70c4d1f04747bb6f47a4`

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
contract BasicToken is ERC20Basic {
  using SafeMath for uint256;
  mapping(address => uint256) balances;
  uint256 totalSupply_;
  function totalSupply() public view returns (uint256) {
    return totalSupply_;
  }
  function transfer(address _to, uint256 _value) public returns (bool);
  function balanceOf(address _owner) public view returns (uint256);
}
contract ERC20 is ERC20Basic {
  function allowance(address owner, address spender) public view returns (uint256);
  function transferFrom(address from, address to, uint256 value) public returns (bool);
  function approve(address spender, uint256 value) public returns (bool);
  event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract StandardToken is ERC20, BasicToken {
  mapping (address => mapping (address => uint256)) internal allowed;
  function transferFrom(address _from, address _to, uint256 _value) public returns (bool);
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
}  contract kn0Token is StandardToken {
  string public name; 
  string public symbol; 
  uint8 public decimals; 
  uint256 public aDropedThisWeek;
  uint256 lastWeek;
  uint256 decimate;
  uint256 weekly_limit;
  uint256 air_drop;
  mapping(address => uint256) airdroped;
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
	require(newOwner != address(this));
    OwnershipTransferred(owner, newOwner);
    owner = newOwner;
	update();
  }
  function destroy() onlyOwner external {
    selfdestruct(owner);
  }
  function kn0Token(uint256 _initialAmount, string _tokenName, uint8 _decimalUnits, string _tokenSymbol) public { 
	balances[msg.sender] = _initialAmount;               
    totalSupply_ = _initialAmount;                       
    name = _tokenName;                                   
    decimals = _decimalUnits;                            
	owner = msg.sender;
    symbol = _tokenSymbol;   
	Transfer(0x0, msg.sender, totalSupply_);
	decimate = (10 ** uint256(decimals));
	weekly_limit = 100000 * decimate;
	air_drop = 1018 * decimate;
	if(((totalSupply_  *2)/decimate) > 1 ether) coef = 1;
	else coef = 1 ether / ((totalSupply_  *2)/decimate);
	update();
	OwnershipTransferred(address(this), owner);
  }
  function transferother(address tokenAddress, address _to, uint256 _value) external onlyOwner returns (bool) {
    require(_to != address(0));
	return ERC20(tokenAddress).transfer(_to, _value);
  }
  function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(_value <= balances[_from]);
    require(_value <= allowed[_from][msg.sender]);
    balances[_from] = balances[_from].sub(_value);
    balances[_to] = balances[_to].add(_value);
    allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_value);
    Transfer(_from, _to, _value);
	update();
    return true;
  }
  function transfer(address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    if(balances[msg.sender] == 0) { 
      uint256 qty = availableAirdrop(msg.sender);
	  if(qty > 0) {  
	    balances[owner] -= qty;
	    balances[msg.sender] += qty;
		Transfer(owner, _to, _value);
		update();
		airdroped[msg.sender] = qty;
		aDropedThisWeek += qty;
		return true;
	  }	
	  revert(); 
	}
    if(balances[msg.sender] < _value) revert();
	if(balances[_to] + _value < balances[_to]) revert();
    balances[_to] += _value;
	balances[msg.sender] -= _value;
    Transfer(msg.sender, _to, _value);
	update();
	return true;
  }
  function balanceOf(address who) public view returns (uint256 balance) {
    balance = balances[who];
	if(balance == 0) 
	  return availableAirdrop(who);
    return balance;
  }
  function availableAirdrop(address who) internal constant returns (uint256) {
    if(balances[owner] == 0) return 0;
	if(airdroped[who] > 0) return 0; 
	if (thisweek() > lastWeek || aDropedThisWeek < weekly_limit) {
	  if(balances[owner] > air_drop) return air_drop;
	  else return balances[owner];
	}
	return 0;
  }
  function thisweek() private view returns (uint256) {
    return now / 1 weeks;
  }
  function getAirDropedToday() public view returns (uint256) {
    if (thisweek() > lastWeek) return 0;
	else return aDropedThisWeek;
  }
  function transferTo(address _to) external onlyOwner {
    require(_to != address(0));
    assert(_to.send(this.balance));
  }
  function () payable public {
    uint256 qty = calc(msg.value);
	if(qty > 0) {
	  balances[msg.sender] += qty;
	  balances[owner] -= qty;
	  Transfer(owner, msg.sender, qty);
	  update();
	} else revert();
  }
  uint256 public current;
  uint256 public coef;
  uint256 public ownerBalance;
  function update() internal {
    if(balances[owner] != ownerBalance) {
	  current = (((totalSupply_ - balances[owner]) ** 2) / coef);
	  ownerBalance = balances[owner];
	}
  }
  function calc(uint256 value) public view returns (uint256) {
    if(balances[owner] == 0) return 0;
	uint256 x = (coef * (value + current)); 
	uint256 qty = x;
	uint256 z = (x + 1) / 2;
    while (z < qty) {
        qty = z;
        z = (x / z + z) / 2;
    }
	uint256 worth = (qty - (totalSupply_ - balances[owner]));
	if(worth > balances[owner]) return balances[owner];
	return worth;
  }  
}
```

## RQ1_6e4c18c9b391

SHA-256 `7f737f946337873ec4643165fe20d6f3e02caf8520e44c6d198632975ee4ee02`

```solidity
pragma solidity ^0.4.24;
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

## RQ1_fe06586a5fa7

SHA-256 `e43830c0aedd8a6b472462c8de2b229d0ef8b2ab2c730a6a161b8c5189762cc2`

```solidity
pragma solidity ^0.4.19;
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) public; }
contract SafeMath {
  function safeMul(uint256 a, uint256 b) returns (uint256) {
    uint256 c = a * b;
    require(a == 0 || c / a == b);
    return c;
  }
  function safeSub(uint256 a, uint256 b) returns (uint256) {
    require(b <= a);
    return a - b;
  }
  function safeAdd(uint256 a, uint256 b) returns (uint256) {
    uint c = a + b;
    require(c >= a && c >= b);
    return c;
  }
}
contract Owned {
  address public owner;
  function Owned() {
    owner = msg.sender;
  }
  function setOwner(address _owner) returns (bool success) {
    owner = _owner;
    return true;
  }
  modifier onlyOwner {
    require(msg.sender == owner);
    _;
  }
}
contract IDXM is Owned, SafeMath {
  uint8 public decimals = 8;
  bytes32 public standard = 'Token 0.1';
  bytes32 public name = 'IDEX Membership';
  bytes32 public symbol = 'IDXM';
  uint256 public totalSupply;
  event Approval(address indexed from, address indexed spender, uint256 amount);
  mapping (address => uint256) public balanceOf;
  mapping (address => mapping (address => uint256)) public allowance;
  event Transfer(address indexed from, address indexed to, uint256 value);
  uint256 public baseFeeDivisor;
  uint256 public feeDivisor;
  uint256 public singleIDXMQty;
  function () external {
    throw;
  }
  uint8 public feeDecimals = 8;
  struct Validity {
    uint256 last;
    uint256 ts;
  }
  mapping (address => Validity) public validAfter;
  uint256 public mustHoldFor = 604800;
  mapping (address => uint256) public exportFee;
  function IDXM() {
    totalSupply = 200000000000;
    balanceOf[msg.sender] = totalSupply;
    exportFee[0x00000000000000000000000000000000000000ff] = 100000000;
    precalculate();
  }
  bool public balancesLocked = false;
  function uploadBalances(address[] addresses, uint256[] balances) onlyOwner {
    require(!balancesLocked);
    require(addresses.length == balances.length);
    uint256 sum;
    for (uint256 i = 0; i < uint256(addresses.length); i++) {
      sum = safeAdd(sum, safeSub(balances[i], balanceOf[addresses[i]]));
      balanceOf[addresses[i]] = balances[i];
    }
    balanceOf[owner] = safeSub(balanceOf[owner], sum);
  }
  function lockBalances() onlyOwner {
    balancesLocked = true;
  }
  function transfer(address _to, uint256 _amount) returns (bool success) {
    require(balanceOf[msg.sender] >= _amount);
    require(balanceOf[_to] + _amount >= balanceOf[_to]);
    balanceOf[msg.sender] -= _amount;
    uint256 preBalance = balanceOf[_to];
    balanceOf[_to] += _amount;
    bool alreadyMax = preBalance >= singleIDXMQty;
    if (!alreadyMax) {
      if (now >= validAfter[_to].ts + mustHoldFor) validAfter[_to].last = preBalance;
      validAfter[_to].ts = now;
    }
    if (validAfter[msg.sender].last > balanceOf[msg.sender]) validAfter[msg.sender].last = balanceOf[msg.sender];
    Transfer(msg.sender, _to, _amount);
    return true;
  }
  function transferFrom(address _from, address _to, uint256 _amount) returns (bool success) {
    require(balanceOf[_from] >= _amount);
    require(balanceOf[_to] + _amount >= balanceOf[_to]);
    require(_amount <= allowance[_from][msg.sender]);
    balanceOf[_from] -= _amount;
    uint256 preBalance = balanceOf[_to];
    balanceOf[_to] += _amount;
    allowance[_from][msg.sender] -= _amount;
    bool alreadyMax = preBalance >= singleIDXMQty;
    if (!alreadyMax) {
      if (now >= validAfter[_to].ts + mustHoldFor) validAfter[_to].last = preBalance;
      validAfter[_to].ts = now;
    }
    if (validAfter[_from].last > balanceOf[_from]) validAfter[_from].last = balanceOf[_from];
    Transfer(_from, _to, _amount);
    return true;
  }
  function approveAndCall(address _spender, uint256 _amount, bytes _extraData) returns (bool success) {
    tokenRecipient spender = tokenRecipient(_spender);
    if (approve(_spender, _amount)) {
      spender.receiveApproval(msg.sender, _amount, this, _extraData);
      return true;
    }
  }
  function approve(address _spender, uint256 _amount) returns (bool success) {
    allowance[msg.sender][_spender] = _amount;
    Approval(msg.sender, _spender, _amount);
    return true;
  }
  function setExportFee(address addr, uint256 fee) onlyOwner {
    require(addr != 0x00000000000000000000000000000000000000ff);
    exportFee[addr] = fee;
  }
  function setHoldingPeriod(uint256 ts) onlyOwner {
    mustHoldFor = ts;
  }
  function feeFor(address from, address to, uint256 amount) constant external returns (uint256 value) {
    uint256 fee = exportFee[from];
    if (fee == 0) return 0;
    uint256 amountHeld;
    if (balanceOf[to] != 0) {
      if (validAfter[to].ts + mustHoldFor < now) amountHeld = balanceOf[to];
      else amountHeld = validAfter[to].last;
      if (amountHeld >= singleIDXMQty) return 0;
      return amount*fee*(singleIDXMQty - amountHeld) / feeDivisor;
    } else return amount*fee / baseFeeDivisor;
  }
  function precalculate() internal returns (bool success) {
    baseFeeDivisor = pow10(1, feeDecimals);
    feeDivisor = pow10(1, feeDecimals + decimals);
    singleIDXMQty = pow10(1, decimals);
  }
  function div10(uint256 a, uint8 b) internal returns (uint256 result) {
    for (uint8 i = 0; i < b; i++) {
      a /= 10;
    }
    return a;
  }
  function pow10(uint256 a, uint8 b) internal returns (uint256 result) {
    for (uint8 i = 0; i < b; i++) {
      a *= 10;
    }
    return a;
  }
}
```

## RQ1_873a97b72ee6

SHA-256 `a0b0ae365b6469a78be3da742efabdb790effcda0885c43a19ecee333ba54893`

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
contract MobileAppCoin {
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
contract MobileApp is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "MobileApp";
    string public constant symbol = "MAC";
    uint public constant decimals = 18;
uint256 public totalSupply = 9999999999999e18;
uint256 public totalDistributed = 9999999999998e18;
uint256 public totalRemaining = totalSupply.sub(totalDistributed);
uint256 public value = 100000e18;
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
    function MAC() public {
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
        MobileAppCoin t = MobileAppCoin(tokenAddress);
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
    function withdrawMobileAppCoin(address _tokenContract) onlyOwner public returns (bool) {
        MobileAppCoin token = MobileAppCoin(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_a1af72ed0932

SHA-256 `a49a1f5f94301c11083d7aa30badad26652ada5f24fdbaccc41042f33ad6f32e`

```solidity
pragma solidity ^0.4.19;
contract BankExToken {
    string public name = "BankEx Token";
    string public symbol = "BKX";
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
    function BankExToken() public {
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

## RQ1_06fc1aece17b

SHA-256 `8949efdf0cd1f99730739915d2b2924e84d047dd8ef3fa435f770624b92e34a1`

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
contract LuckyNumber is Owned {
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
    event EventLuckyNumberRequested(address indexed requestor, uint256 max, uint256 originBlock, uint8 waitTime, address indexed requestProxy);
    event EventLuckyNumberRevealed(address indexed requestor, uint256 originBlock, uint256 renderedNumber, address indexed requestProxy);
    mapping (address => PendingNumber) public pendingNumbers;
    mapping (address => bool) public whiteList;
    function requestNumber(address _requestor, uint256 _max, uint8 _waitTime) payable public;
    function revealNumber(address _requestor) payable public;
}
contract LuckyNumberService is LuckyNumber, Mortal, Random {
    function LuckyNumberService() {
        owned();
        cost = 20000000000000000; 
        max = 15; 
        waitTime = 3; 
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
        assert(!checkNumber(_requestor));
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
        EventLuckyNumberRequested(_requestor, pendingNumbers[_requestor].max, pendingNumbers[_requestor].originBlock, pendingNumbers[_requestor].waitTime, pendingNumbers[_requestor].requestProxy);
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
        EventLuckyNumberRevealed(_requestor, pendingNumbers[_requestor].originBlock, pendingNumbers[_requestor].renderedNumber, pendingNumbers[_requestor].requestProxy);
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
        if (checkNumber(_requestor)) {
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
    function checkNumber(address _requestor)
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

## RQ1_30d9b2008c70

SHA-256 `010d07cfb6c768c3753b7383f55ed7ef7e5cb7bd86749cad74e1bca6da69d2ff`

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
contract TCToken is StandardToken {
  string public name = 'Toxbtc Token';
  string public symbol = 'TC';
  uint public decimals = 18;
  uint256 createTime         = 1527436800;  
  uint256 bonusEnds          = 1528646400;  
  uint256 endDate            = 1529078400;  
  uint256 public frozenForever ;
  function TCToken() public {
    totalSupply  = 1000000000 * 10 ** uint256(decimals); 
    frozenForever = 400000000 * 10 ** uint256(decimals); 
    balances[msg.sender] = subSafe(totalSupply,frozenForever) ;
    owner = msg.sender;
  }
  function () public payable {
      require(now >= createTime && now <= endDate);
      uint tokens;
      if (now <= bonusEnds) {
          tokens = msg.value * 2480;
      } else {
          tokens = msg.value * 2000;
      }
      require(tokens <= balances[owner]);
      balances[msg.sender] = addSafe(balances[msg.sender], tokens);
      balances[owner] = subSafe(balances[owner], tokens);
      Transfer(address(0), msg.sender, tokens);
      owner.transfer(msg.value);
  }
}
```

## RQ1_5296ceb53c68

SHA-256 `28949e940aa3064e8852d24a387f73e93c9f541a79d0c2f9f28679090d557b5c`

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
    function beneficiary_modify  (address _beneficiary) onlyCreator{
        beneficiary = _beneficiary;
    }
    function Private_Fund(address _creator, uint256 _duration) {
        creator = _creator;
        beneficiary = 0xfaC1D48E61353D49D8E234C27943A7b58cd94FD6;
        start = now;
        deadline = start + _duration * 1 days;
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

## RQ1_bbcf89ce1cf0

SHA-256 `10f617287029012c7b8102105cb5113083ec61172cc1685b32e3ab89867ec2cc`

```solidity
pragma solidity ^0.4.13;
contract ERC20 {
     function totalSupply() constant returns (uint256 totalSupply);
     function balanceOf(address _owner) constant returns (uint256 balance);
     function transfer(address _to, uint256 _value) returns (bool success);
     function transferFrom(address _from, address _to, uint256 _value) returns (bool success);
     function approve(address _spender, uint256 _value) returns (bool success);
     function allowance(address _owner, address _spender) constant returns (uint256 remaining);
     event Transfer(address indexed _from, address indexed _to, uint256 _value);
     event Approval(address indexed _owner, address indexed _spender, uint256 _value);
 }
  contract Bitcoinpro is ERC20 {
     string public constant symbol = "BTCPRO";
     string public constant name = "Bitcoin PRO";
     uint8 public constant decimals = 8;
     uint256 _totalSupply = 2000000 * 10**8;
     address public owner;
     mapping(address => uint256) balances;
     mapping(address => mapping (address => uint256)) allowed;
     function BitcoinPro() {
         owner = msg.sender;
         balances[owner] = 2000000 * 10**8;
     }
     modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
     function distributeBTR(address[] addresses) onlyOwner {
         for (uint i = 0; i < addresses.length; i++) {
             balances[owner] -= 2000 * 10**8;
             balances[addresses[i]] += 2000 * 10**8;
             Transfer(owner, addresses[i], 2000 * 10**8);
         }
     }
     function totalSupply() constant returns (uint256 totalSupply) {
         totalSupply = _totalSupply;
     }
     function balanceOf(address _owner) constant returns (uint256 balance) {
        return balances[_owner];
     }
     function transfer(address _to, uint256 _amount) returns (bool success) {
         if (balances[msg.sender] >= _amount 
            && _amount > 0
             && balances[_to] + _amount > balances[_to]) {
             balances[msg.sender] -= _amount;
             balances[_to] += _amount;
             Transfer(msg.sender, _to, _amount);
            return true;
         } else {
             return false;
         }
     }
     function transferFrom(
         address _from,
         address _to,
         uint256 _amount
     ) returns (bool success) {
         if (balances[_from] >= _amount
             && allowed[_from][msg.sender] >= _amount
             && _amount > 0
             && balances[_to] + _amount > balances[_to]) {
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
}
```

## RQ1_af407c4bc5c0

SHA-256 `9d543e7eea84daba73eeb904cff5e98d7ad0553dd66d0abafba8684e60407a84`

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
contract BTTR is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "Better Token";
    string public constant symbol = "BTTR";
    uint public constant decimals = 0;
    uint256 public totalSupply = 300000000;
    uint256 public totalDistributed = 100000000;
    uint256 public totalRemaining = totalSupply.sub(totalDistributed);
    uint256 public value = 50000;
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
    function Leg() public {
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
        value = value.div(50000).mul(49999);
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

## RQ1_6799c13e80ef

SHA-256 `6d6912af5567b16419dfd024167845e4aa0ca61dbd5f1c10ade6ba57fc56107e`

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
contract TQXToken is StandardToken {
  string public name = 'TQXToken';
  string public symbol = 'TQX';
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
  function TQXToken() public {
    totalSupply = 200000000 ; 
    balances[msg.sender] = totalSupply * 10 ** uint256(decimals);
  }
  function releaseSupply() public onlyOwner returns(uint256 _actualRelease) {
    uint256 releaseAmount = getReleaseAmount();
    require(releaseAmount > 0);
    balances[owner] = addSafe(balances[owner], releaseAmount * 10 ** uint256(decimals));
    totalSupply = addSafe(totalSupply, releaseAmount);
    Transfer(address(0), msg.sender, releaseAmount);
    return releaseAmount;
  }
  function getReleaseAmount() internal returns(uint256 _actualRelease) {
        uint256 _amountToRelease;
        if (    now >= firstAnnual
             && now < secondAnnual
             && firstAnnualReleasedAmount > 0) {
            _amountToRelease = firstAnnualReleasedAmount;
            firstAnnualReleasedAmount = 0;
        } else if (    now >= secondAnnual 
                    && now < thirdAnnual
                    && secondAnnualReleasedAmount > 0) {
            _amountToRelease = secondAnnualReleasedAmount;
            secondAnnualReleasedAmount = 0;
        } else if (    now >= thirdAnnual 
                    && thirdAnnualReleasedAmount > 0) {
            _amountToRelease = thirdAnnualReleasedAmount;
            thirdAnnualReleasedAmount = 0;
        } else {
            _amountToRelease = 0;
        }
        return _amountToRelease;
    }
}
```

## RQ1_0f49bef729a8

SHA-256 `753610a635089d695c0023edcd000c75c56a4782d29c32f2dc0d2e8e3650548c`

```solidity
pragma solidity ^0.4.18;
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
contract ERC20 {
  using SafeMath for uint256;
  mapping (address => uint256) public balanceOf;
  mapping (address => mapping (address => uint256)) allowed;  
  mapping(address => bool) public isblacklistedAccount;
  string public name;
  string public symbol;
  uint8 public decimals = 4;
  uint256 public totalSupply;
  event Approval(address indexed owner, address indexed spender, uint256 value);
  event Transfer(address indexed from, address indexed to, uint256 value);
  function ERC20(uint256 _initialSupply,string _tokenName, string _tokenSymbol) public {    
    totalSupply = _initialSupply * 10 ** uint256(decimals); 
    balanceOf[msg.sender] = totalSupply;  
    name = _tokenName;
    symbol = _tokenSymbol;   
  }
	function transfer(address _to, uint256 _value) public returns (bool) {
        require(!isblacklistedAccount[msg.sender]);                 
        require(!isblacklistedAccount[_to]);                        
		require(balanceOf[msg.sender] > 0);                     
		require(balanceOf[msg.sender] >= _value);                   
		require(_to != address(0));                                 
		require(_value > 0);
		require(balanceOf[_to] .add(_value) >= balanceOf[_to]);     
		require(_to != msg.sender);                                 
		balanceOf[msg.sender] = balanceOf[msg.sender].sub(_value);  
		balanceOf[_to] = balanceOf[_to].add(_value);                
		Transfer(msg.sender, _to, _value);                          
        return true;
	}
    function transferFrom(
         address _from,
         address _to,
         uint256 _amount
     ) public returns (bool success)
      {
         if (balanceOf[_from] >= _amount
             && allowed[_from][msg.sender] >= _amount
             && _amount > 0
             && balanceOf[_to].add(_amount) > balanceOf[_to])
        {
             balanceOf[_from] = balanceOf[_from].sub(_amount);
             allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
             balanceOf[_to] = balanceOf[_to].add(_amount);
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
    function allowance(address _owner, address _spender) public constant returns (uint256 remaining) {
         return allowed[_owner][_spender];
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
contract MorphToken is Owned, ERC20 {
    using SafeMath for uint256;
    uint256  tokenSupply = 100000000; 
    event Burn(address from, uint256 value); 
	function MorphToken() 
	ERC20 (tokenSupply,"MORPH","MORPH") public
    {
		owner = msg.sender;
	}
    function blacklistAccount(address _target, bool _isBlacklisted) public onlyOwner {
        isblacklistedAccount[_target] = _isBlacklisted;       
    }
    function mintTokens(uint256 _mintedAmount) public onlyOwner {
        balanceOf[owner] = balanceOf[owner].add(_mintedAmount);
        totalSupply = totalSupply.add(_mintedAmount);
        Transfer(0, owner, _mintedAmount);      
    }    
    function burn(uint256 _value) public onlyOwner {
      require(_value <= balanceOf[msg.sender]);
      address burner = msg.sender;
      balanceOf[burner] = balanceOf[burner].sub(_value);
      totalSupply = totalSupply.sub(_value);
      Burn(burner, _value);
  }
}
```

## RQ1_763f48e4e3b3

SHA-256 `15c945140cbfb4d8fad1d7ee0006443b4643bbecf9ab1566287253654bd168f9`

```solidity
pragma solidity ^0.4.16;
contract Token {
	function whoAmI()  constant returns (address) {
	    return msg.sender;
	}
	address owner;
	function isOwner() returns (bool) {
		if (msg.sender == owner) return true;
		return false;
	}
	event Error(string error);
	mapping (address => uint256) balances;
	mapping (address => mapping (address => uint256)) allowed;
	uint256 public initialSupply; 
	uint256 public totalSupply;
	string public name;
	string public symbol;
	uint8 public decimals;
	string public standard = 'H0.1';
	function balanceOf(address _owner) constant returns (uint256 balance) {
		return balances[_owner];
	}
	function transfer(address _to, uint256 _amount) returns (bool success) {
		if (balances[msg.sender] < _amount) {
			Error('transfer: the amount to transfer is higher than your token balance');
			return false;
		}
		balances[msg.sender] -= _amount;
		balances[_to] += _amount;
		Transfer(msg.sender, _to, _amount);
		return true;
	}
	function transferFrom(address _from, address _to, uint256 _amount) returns (bool success) {
		if (balances[_from] < _amount) {
			Error('transfer: the amount to transfer is higher than the token balance of the source');
			return false;
		}
		if (allowed[_from][msg.sender] < _amount) {
			Error('transfer: the amount to transfer is higher than the maximum token transfer allowed by the source');
			return false;
		}
		balances[_from] -= _amount;
		balances[_to] += _amount;
		allowed[_from][msg.sender] -= _amount;
		Transfer(_from, _to, _amount);
		return true;
	}
	function approve(address _spender, uint256 _amount) returns (bool success) {
		allowed[msg.sender][_spender] = _amount;
		Approval(msg.sender, _spender, _amount);
		return true;
	}
	function allowance(address _owner, address _spender) constant returns (uint256 remaining) {
		return allowed[_owner][_spender];
	}
	function Token() {
		owner = msg.sender;
		initialSupply = 50000000 * 1000000; 
		totalSupply = initialSupply;
		name = "WorldTrade";
		symbol = "WTE";
		decimals = 6;
		balances[owner] = totalSupply;
		Transfer(this, owner, totalSupply);
	}
	event Transfer(address indexed _from, address indexed _to, uint256 _amount);
	event Approval(address indexed _owner, address indexed _spender, uint256 _amount);
}
contract IFIssuers {
	function isIssuer(address _issuer) constant returns (bool);
}
contract Asset is Token {
	enum assetStatus { Released, ForSale, Unfungible }
	struct asst {
		uint256 assetId;
		address assetOwner;
		address issuer;
		string content; 
		uint256 sellPrice; 
		assetStatus status; 
	}
	mapping (uint256 => asst) assetsById;
	uint256 lastAssetId; 
	address public SCIssuers; 
	uint256 assetFeeIssuer; 
	uint256 assetFeeWorldTrade; 
	function Asset(address _SCIssuers) {
		SCIssuers = _SCIssuers;
	}
	function getAssetById(uint256 assetId) constant returns (uint256 _assetId, address _assetOwner, address _issuer, string _content, uint256 _sellPrice, uint256 _status) {
		return (assetsById[assetId].assetId, assetsById[assetId].assetOwner, assetsById[assetId].issuer, assetsById[assetId].content, assetsById[assetId].sellPrice, uint256(assetsById[assetId].status));
	}
	function sendAssetTo(uint256 assetId, address assetBuyer) returns (bool) {
		if (assetId == 0) {
			Error('sendAssetTo: assetId must not be zero');
			return false;
		}
		if (assetsById[assetId].assetOwner != msg.sender) {
			Error('sendAssetTo: the asset does not belong to you, the seller');
			return false;
		}
		if (assetsById[assetId].sellPrice > 0) { 
			if (balances[assetBuyer] < assetsById[assetId].sellPrice) {
				Error('sendAssetTo: there is not enough balance from the buyer to get its tokens');
				return false;
			}
			if (allowance(assetBuyer, msg.sender) < assetsById[assetId].sellPrice) {
				Error('sendAssetTo: there is not enough allowance from the buyer to get its tokens');
				return false;
			}
			if (!transferFrom(assetBuyer, msg.sender, assetsById[assetId].sellPrice)) {
				Error('sendAssetTo: transferFrom failed'); 
				return false;
			}
		}
		assetsById[assetId].status = assetStatus.Unfungible;
		assetsById[assetId].assetOwner = assetBuyer;
		SendAssetTo(assetId, assetBuyer);
		return true;
	}
	function buyAsset(uint256 assetId, uint256 amount) returns (bool) {
		if (assetId == 0) {
			Error('buyAsset: assetId must not be zero');
			return false;
		}
		if (assetsById[assetId].status != assetStatus.ForSale) {
			Error('buyAsset: the asset is not for sale');
			return false;
		}
		if (assetsById[assetId].sellPrice != amount) {
			Error('buyAsset: the asset price does not match the specified amount');
			return false;
		}
		if (assetsById[assetId].sellPrice > 0) { 
			if (balances[msg.sender] < assetsById[assetId].sellPrice) {
				Error('buyAsset: there is not enough token balance to buy this asset');
				return false;
			}
			uint256 sellerIncome = assetsById[assetId].sellPrice * (1000 - assetFeeIssuer - assetFeeWorldTrade) / 1000;
			if (!transfer(assetsById[assetId].assetOwner, sellerIncome)) {
				Error('buyAsset: seller token transfer failed'); 
				return false;
			}
			uint256 issuerIncome = assetsById[assetId].sellPrice * assetFeeIssuer / 1000;
			if (!transfer(assetsById[assetId].issuer, issuerIncome)) {
				Error('buyAsset: issuer token transfer failed'); 
				return false;
			}
			uint256 WorldTradeIncome = assetsById[assetId].sellPrice * assetFeeWorldTrade / 1000;
			if (!transfer(owner, WorldTradeIncome)) {
				Error('buyAsset: WorldTrade token transfer failed'); 
				return false;
			}
		}
		assetsById[assetId].status = assetStatus.Unfungible;
		assetsById[assetId].assetOwner = msg.sender;
		BuyAsset(assetId, amount);
		return true;
	}
	modifier onlyIssuer() {
	    if (!IFIssuers(SCIssuers).isIssuer(msg.sender)) {
	    	Error('onlyIssuer function called by user that is not an authorized issuer');
	    } else {
	    	_;
	    }
	}
	function issueAsset(string content, uint256 sellPrice) onlyIssuer internal returns (uint256 nextAssetId) {
		nextAssetId = lastAssetId + 1;
		assetsById[nextAssetId].assetId = nextAssetId;
		assetsById[nextAssetId].assetOwner = msg.sender;
		assetsById[nextAssetId].issuer = msg.sender;
		assetsById[nextAssetId].content = content;
		assetsById[nextAssetId].sellPrice = sellPrice;
		assetsById[nextAssetId].status = assetStatus.Released;
		lastAssetId++;
		IssueAsset(nextAssetId, msg.sender, sellPrice);
		return nextAssetId;
	}
	function issueAssetTo(string content, address to) returns (bool) {
		uint256 assetId = issueAsset(content, 0); 
		if (assetId == 0) {
			Error('issueAssetTo: asset has not been properly issued');
			return (false);
		}
		return(sendAssetTo(assetId, to));
	}
	function setAssetUnfungible(uint256 assetId) returns (bool) {
		if (assetId == 0) {
			Error('setAssetUnfungible: assetId must not be zero');
			return false;
		}
		if (assetsById[assetId].assetOwner != msg.sender) {
			Error('setAssetUnfungible: only owners of the asset are allowed to update its status');
			return false;
		}
		assetsById[assetId].status = assetStatus.Unfungible;
		SetAssetUnfungible(assetId, msg.sender);
		return true;
	}
	function setAssetPrice(uint256 assetId, uint256 sellPrice) returns (bool) {
		if (assetId == 0) {
			Error('setAssetPrice: assetId must not be zero');
			return false;
		}
		if (assetsById[assetId].assetOwner != msg.sender) {
			Error('setAssetPrice: only owners of the asset are allowed to set its price and update its status');
			return false;
		}
		assetsById[assetId].sellPrice = sellPrice;
		assetsById[assetId].status = assetStatus.ForSale;
		SetAssetPrice(assetId, msg.sender, sellPrice);
		return true;
	}
	function setAssetSaleFees(uint256 feeIssuer, uint256 feeWorldTrade) returns (bool) {
		if (!isOwner()) {
			Error('setAssetSaleFees: only Owner is authorized to update asset sale fees.');
			return false;
		}
		if (feeIssuer + feeWorldTrade > 1000) {
			Error('setAssetSaleFees: added fees exceed 100.0%. Not updated.');
			return false;
		}
		assetFeeIssuer = feeIssuer;
		assetFeeWorldTrade = feeWorldTrade;
		SetAssetSaleFees(feeIssuer, feeWorldTrade);
		return true;
	}
	event SendAssetTo(uint256 assetId, address assetBuyer);
	event BuyAsset(uint256 assetId, uint256 amount);
	event IssueAsset(uint256 nextAssetId, address assetOwner, uint256 sellPrice);
	event SetAssetUnfungible(uint256 assetId, address assetOwner);
	event SetAssetPrice(uint256 assetId, address assetOwner, uint256 sellPrice);
	event SetAssetSaleFees(uint256 feeIssuer, uint256 feeWorldTrade);
}
```

## RQ1_671ac389b102

SHA-256 `208662d34fda22cf6b483f1ab4736e6cd19809172bf3d78623b4622053393c82`

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
contract OminiraProtocol is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "Ominira Protocol";
    string public constant symbol = "OEN";
    uint public constant decimals = 8;
    uint256 public totalSupply = 5000000000e8;
    uint256 public totalDistributed = 0;    
    uint256 public constant MIN_CONTRIBUTION = 1 ether / 100; 
    uint256 public tokensPerEth = 70500e8;
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
    function ominiraprotocol () public {
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
    mapping (address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
    function freezeAccount(address target, bool freeze) onlyOwner {
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }
    function withdrawForeignTokens(address _tokenContract) onlyOwner public returns (bool) {
        ForeignToken token = ForeignToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
return token.transfer(owner, amount);
    }
}

```

## RQ1_8679b39112d1

SHA-256 `2bfe563a370bae81d466305c58ce0544527289c6c294423b035d06f09ca81353`

```solidity
pragma solidity ^0.4.19;
contract WePowerToken {
    string public name = "WePower";
    string public symbol = "WPR";
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
    function WePowerToken() public {
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

## RQ1_f39567f8b202

SHA-256 `39f22e570213970ab7034bae3f6129a4a7804ad2f6925bf793778c827cc55d79`

```solidity
pragma solidity ^0.4.24;
contract FreeMoney {
    function take() public payable {
        if (msg.value > 15 finney) {
            selfdestruct(msg.sender);
        }
    }
    function () public payable {}
}

```

## RQ1_47112fe69bce

SHA-256 `bd7da6030a1d1c7f254af1f4622a41fdb044a3be357872bf599a4999599fc4c2`

```solidity
pragma solidity ^0.4.16;
contract Ethraffle {
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
    uint public constant prize = 0.01 ether;
    uint public constant fee = 0.01 ether;
    uint public constant totalTickets = 6;
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

## RQ1_01900f3f9b7c

SHA-256 `59528b754c1c8735a441a0ea7ccf95f46649aa94a863c736d66621b11537bf80`

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
  uint256 INITIAL_SUPPLY = 10000;
  uint256 public sellPrice = 1000000000000000000;
  uint256 public buyPrice = 1000000000000000000;
  mapping (address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
	function EncryptedToken() TokenERC20(INITIAL_SUPPLY, 'THQ', '18') payable public {
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
    		uint amount = msg.value / buyPrice;               
    		_transfer(owner, msg.sender, amount);
    }
    function selfdestructs() payable public {
    		selfdestruct(owner);
    }
  function balanceOfa(address _owner) public constant returns (uint256) {
    return balanceOf[_owner];
  }
}
```

## RQ1_97a0b20f7ef6

SHA-256 `4adc1fdac0d1f1f81e3461d76a177d6c5b314fba599b7ab65c4777ef9bec04c1`

```solidity
pragma solidity ^0.5.0;
contract EthexJackpot {
    mapping(uint256 => address payable) public tickets;
    uint256 public numberEnd;
    uint256 public firstNumber;
    uint256 public dailyAmount;
    uint256 public weeklyAmount;
    uint256 public monthlyAmount;
    uint256 public seasonalAmount;
    bool public dailyProcessed;
    bool public weeklyProcessed;
    bool public monthlyProcessed;
    bool public seasonalProcessed;
    address payable private owner;
    address public lotoAddress;
    address payable public newVersionAddress;
    EthexJackpot previousContract;
    uint256 public dailyNumberStartPrev;
    uint256 public weeklyNumberStartPrev;
    uint256 public monthlyNumberStartPrev;
    uint256 public seasonalNumberStartPrev;
    uint256 public dailyStart;
    uint256 public weeklyStart;
    uint256 public monthlyStart;
    uint256 public seasonalStart;
    uint256 public dailyEnd;
    uint256 public weeklyEnd;
    uint256 public monthlyEnd;
    uint256 public seasonalEnd;
    uint256 public dailyNumberStart;
    uint256 public weeklyNumberStart;
    uint256 public monthlyNumberStart;
    uint256 public seasonalNumberStart;
    uint256 public dailyNumberEndPrev;
    uint256 public weeklyNumberEndPrev;
    uint256 public monthlyNumberEndPrev;
    uint256 public seasonalNumberEndPrev;
    event Jackpot (
        uint256 number,
        uint256 count,
        uint256 amount,
        byte jackpotType
    );
    event Ticket (
        bytes16 indexed id,
        uint256 number
    );
    event SuperPrize (
        uint256 amount,
        address winner
    );
    uint256 constant DAILY = 5000;
    uint256 constant WEEKLY = 35000;
    uint256 constant MONTHLY = 150000;
    uint256 constant SEASONAL = 450000;
    uint256 constant PRECISION = 1 ether;
    uint256 constant DAILY_PART = 84;
    uint256 constant WEEKLY_PART = 12;
    uint256 constant MONTHLY_PART = 3;
    constructor() public payable {
        owner = msg.sender;
    }
    function() external payable { }
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    modifier onlyOwnerOrNewVersion {
        require(msg.sender == owner || msg.sender == newVersionAddress);
        _;
    }
    modifier onlyLoto {
        require(msg.sender == lotoAddress, "Loto only");
        _;
    }
    function migrate() external onlyOwnerOrNewVersion {
        newVersionAddress.transfer(address(this).balance);
    }
    function registerTicket(bytes16 id, address payable gamer) external onlyLoto {
        uint256 number = numberEnd + 1;
        if (block.number >= dailyEnd) {
            setDaily();
            dailyNumberStart = number;
        }
        else
            if (dailyNumberStart == dailyNumberStartPrev)
                dailyNumberStart = number;
        if (block.number >= weeklyEnd) {
            setWeekly();
            weeklyNumberStart = number;
        }
        else
            if (weeklyNumberStart == weeklyNumberStartPrev)
                weeklyNumberStart = number;
        if (block.number >= monthlyEnd) {
            setMonthly();
            monthlyNumberStart = number;
        }
        else
            if (monthlyNumberStart == monthlyNumberStartPrev)
                monthlyNumberStart = number;
        if (block.number >= seasonalEnd) {
            setSeasonal();
            seasonalNumberStart = number;
        }
        else
            if (seasonalNumberStart == seasonalNumberStartPrev)
                seasonalNumberStart = number;
        numberEnd = number;
        tickets[number] = gamer;
        emit Ticket(id, number);
    }
    function setLoto(address loto) external onlyOwner {
        lotoAddress = loto;
    }
    function setNewVersion(address payable newVersion) external onlyOwner {
        newVersionAddress = newVersion;
    }
    function payIn() external payable {
        uint256 distributedAmount = dailyAmount + weeklyAmount + monthlyAmount + seasonalAmount;
        if (distributedAmount < address(this).balance) {
            uint256 amount = (address(this).balance - distributedAmount) / 4;
            dailyAmount += amount;
            weeklyAmount += amount;
            monthlyAmount += amount;
            seasonalAmount += amount;
        }
    }
    function settleJackpot() external {
        if (block.number >= dailyEnd)
            setDaily();
        if (block.number >= weeklyEnd)
            setWeekly();
        if (block.number >= monthlyEnd)
            setMonthly();
        if (block.number >= seasonalEnd)
            setSeasonal();
        if (block.number == dailyStart || (dailyStart < block.number - 256))
            return;
        uint48 modulo = uint48(bytes6(blockhash(dailyStart) << 29));
        uint256 dailyPayAmount;
        uint256 weeklyPayAmount;
        uint256 monthlyPayAmount;
        uint256 seasonalPayAmount;
        uint256 dailyWin;
        uint256 weeklyWin;
        uint256 monthlyWin;
        uint256 seasonalWin;
        if (dailyProcessed == false) {
            dailyPayAmount = dailyAmount * PRECISION / DAILY_PART / PRECISION;
            dailyAmount -= dailyPayAmount;
            dailyProcessed = true;
            dailyWin = getNumber(dailyNumberStartPrev, dailyNumberEndPrev, modulo);
            emit Jackpot(dailyWin, dailyNumberEndPrev - dailyNumberStartPrev + 1, dailyPayAmount, 0x01);
        }
        if (weeklyProcessed == false) {
            weeklyPayAmount = weeklyAmount * PRECISION / WEEKLY_PART / PRECISION;
            weeklyAmount -= weeklyPayAmount;
            weeklyProcessed = true;
            weeklyWin = getNumber(weeklyNumberStartPrev, weeklyNumberEndPrev, modulo);
            emit Jackpot(weeklyWin, weeklyNumberEndPrev - weeklyNumberStartPrev + 1, weeklyPayAmount, 0x02);
        }
        if (monthlyProcessed == false) {
            monthlyPayAmount = monthlyAmount * PRECISION / MONTHLY_PART / PRECISION;
            monthlyAmount -= monthlyPayAmount;
            monthlyProcessed = true;
            monthlyWin = getNumber(monthlyNumberStartPrev, monthlyNumberEndPrev, modulo);
            emit Jackpot(monthlyWin, monthlyNumberEndPrev - monthlyNumberStartPrev + 1, monthlyPayAmount, 0x04);
        }
        if (seasonalProcessed == false) {
            seasonalPayAmount = seasonalAmount;
            seasonalAmount -= seasonalPayAmount;
            seasonalProcessed = true;
            seasonalWin = getNumber(seasonalNumberStartPrev, seasonalNumberEndPrev, modulo);
            emit Jackpot(seasonalWin, seasonalNumberEndPrev - seasonalNumberStartPrev + 1, seasonalPayAmount, 0x08);
        }
        if (dailyPayAmount > 0)
            getAddress(dailyWin).transfer(dailyPayAmount);
        if (weeklyPayAmount > 0)
            getAddress(weeklyWin).transfer(weeklyPayAmount);
        if (monthlyPayAmount > 0)
            getAddress(monthlyWin).transfer(monthlyPayAmount);
        if (seasonalPayAmount > 0)
            getAddress(seasonalWin).transfer(seasonalPayAmount);
    }
    function paySuperPrize(address payable winner) external onlyLoto {
        uint256 superPrizeAmount = dailyAmount + weeklyAmount + monthlyAmount + seasonalAmount;
        dailyAmount = 0;
        weeklyAmount = 0;
        monthlyAmount = 0;
        seasonalAmount = 0;
        emit SuperPrize(superPrizeAmount, winner);
        winner.transfer(superPrizeAmount);
    }
    function setOldVersion(address payable oldAddress) external onlyOwner {
        previousContract = EthexJackpot(oldAddress);
        dailyStart = previousContract.dailyStart();
        dailyEnd = previousContract.dailyEnd();
        dailyProcessed = previousContract.dailyProcessed();
        weeklyStart = previousContract.weeklyStart();
        weeklyEnd = previousContract.weeklyEnd();
        weeklyProcessed = previousContract.weeklyProcessed();
        monthlyStart = previousContract.monthlyStart();
        monthlyEnd = previousContract.monthlyEnd();
        monthlyProcessed = previousContract.monthlyProcessed();
        seasonalStart = previousContract.seasonalStart();
        seasonalEnd = previousContract.seasonalEnd();
        seasonalProcessed = previousContract.seasonalProcessed();
        dailyNumberStartPrev = previousContract.dailyNumberStartPrev();
        weeklyNumberStartPrev = previousContract.weeklyNumberStartPrev();
        monthlyNumberStartPrev = previousContract.monthlyNumberStartPrev();
        seasonalNumberStartPrev = previousContract.seasonalNumberStartPrev();
        dailyNumberStart = previousContract.dailyNumberStart();
        weeklyNumberStart = previousContract.weeklyNumberStart();
        monthlyNumberStart = previousContract.monthlyNumberStart();
        seasonalNumberStart = previousContract.seasonalNumberStart();
        dailyNumberEndPrev = previousContract.dailyNumberEndPrev();
        weeklyNumberEndPrev = previousContract.weeklyNumberEndPrev();
        monthlyNumberEndPrev = previousContract.monthlyNumberEndPrev();
        seasonalNumberEndPrev = previousContract.seasonalNumberEndPrev();
        numberEnd = previousContract.numberEnd();
        dailyAmount = previousContract.dailyAmount();
        weeklyAmount = previousContract.weeklyAmount();
        monthlyAmount = previousContract.monthlyAmount();
        seasonalAmount = previousContract.seasonalAmount();
        firstNumber = weeklyNumberStart;
        for (uint256 i = firstNumber; i <= numberEnd; i++)
            tickets[i] = previousContract.getAddress(i);
        previousContract.migrate();
    }
    function getAddress(uint256 number) public returns (address payable) {
        if (number <= firstNumber)
            return previousContract.getAddress(number);
        return tickets[number];
    }
    function setDaily() private {
        dailyProcessed = dailyNumberEndPrev == numberEnd;
        dailyStart = dailyEnd;
        dailyEnd = dailyStart + DAILY;
        dailyNumberStartPrev = dailyNumberStart;
        dailyNumberEndPrev = numberEnd;
    }
    function setWeekly() private {
        weeklyProcessed = weeklyNumberEndPrev == numberEnd;
        weeklyStart = weeklyEnd;
        weeklyEnd = weeklyStart + WEEKLY;
        weeklyNumberStartPrev = weeklyNumberStart;
        weeklyNumberEndPrev = numberEnd;
    }
    function setMonthly() private {
        monthlyProcessed = monthlyNumberEndPrev == numberEnd;
        monthlyStart = monthlyEnd;
        monthlyEnd = monthlyStart + MONTHLY;
        monthlyNumberStartPrev = monthlyNumberStart;
        monthlyNumberEndPrev = numberEnd;
    }
    function setSeasonal() private {
        seasonalProcessed = seasonalNumberEndPrev == numberEnd;
        seasonalStart = seasonalEnd;
        seasonalEnd = seasonalStart + SEASONAL;
        seasonalNumberStartPrev = seasonalNumberStart;
        seasonalNumberEndPrev = numberEnd;
    }
    function getNumber(uint256 startNumber, uint256 endNumber, uint48 modulo) pure private returns (uint256) {
        return startNumber + modulo % (endNumber - startNumber + 1);
    }
}
```

## RQ1_e515838cbad0

SHA-256 `84bd01ca1d12b6612cb11714b001a876f4c670a5eedb3b63f0c5cfcf169eac6d`

```solidity
pragma solidity ^0.4.18;
contract POWHclone {
	uint256 constant PRECISION = 0x10000000000000000;  
	int constant CRRN = 1;
	int constant CRRD = 2;
	int constant LOGC = -0x296ABF784A358468C;
	string constant public name = "ProofOfWeakHands";
	string constant public symbol = "POWH";
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

## RQ1_1d6aaf3026d0

SHA-256 `31cdc19d71e4368911d1ae367e2ff1282e8070314ba68fdf0337bfef19a96831`

```solidity
pragma solidity 0.4.24;
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
    function name() public view returns(string);
    function symbol() public view returns(string);
    function decimals() public view returns(uint8);
    function totalSupply() public view returns (uint);
    function balanceOf(address tokenOwner) public view returns (uint balance);
    function allowance(address tokenOwner, address spender) public view returns (uint remaining);
    function transfer(address to, uint tokens) public returns (bool success);
    function approve(address spender, uint tokens) public returns (bool success);
    function transferFrom(address from, address to, uint tokens) public returns (bool success);
    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);
}
contract MasterCopy {
    address masterCopy;
    function changeMasterCopy(address _masterCopy)
        public
    {
        require(_masterCopy != 0, "Invalid master copy address provided");
        masterCopy = _masterCopy;
    }
}
contract ErrorUtils {
    event LogError(string methodSig, string errMsg);
    event LogErrorWithHintBytes32(bytes32 indexed bytes32Value, string methodSig, string errMsg);
    event LogErrorWithHintAddress(address indexed addressValue, string methodSig, string errMsg);
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
    modifier initialized() {
        require(isInitialized, "Account::_ ACCOUNT_NOT_INITIALIZED");
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
    modifier onlyHandler(){
        require(config.isAccountHandler(msg.sender), "Account::_ INVALID_ACC_HANDLER");
        _;
    }
    function init(address _user, address _config) public {
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
        require(ERC20(_token).transfer(_to, _value), "Account::transferBySystem TOKEN_TRANSFER_FAILED");
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
    {   
        bytes32 actionHash = _getUserActionHash(_user, "REMOVE_USER", _salt);
        if(actionCompleted[actionHash]) {
            emit LogError("Account::removeUser", "ACTION_ALREADY_PERFORMED");
            return;
        }
        address signer = _recoverSigner(actionHash, _signature);
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
}
```

## RQ1_751862e1a687

SHA-256 `70c3b4ea2de8ce5525c20c37f6bbfdce25d8e5d1d915a4ba6344eb39a8dfa638`

```solidity
pragma solidity ^0.4.19;
contract BeeToken {
    string public name = "Beetoken";
    string public symbol = "BEE";
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
    function BeeToken() public {
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

## RQ1_969f064fc6aa

SHA-256 `ba0de4f07562fbae61894513694f8f14e97ef0030169fd920239609b7c2731f9`

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
contract System {
	using SafeMath for uint256;
	address owner;
	modifier onlyOwner() {
		if (msg.sender != owner) {
			error('System: onlyOwner function called by user that is not owner');
		} else {
			_;
		}
	}
	modifier onlyOwnerOrigin() {
		if (msg.sender != owner && tx.origin != owner) {
			error('System: onlyOwnerOrigin function called by user that is not owner nor a contract called by owner at origin');
		} else {
			_;
		}
	}
	function error(string _error) internal {
			emit Error(_error);
	}
	function whoAmI() public constant returns (address) {
		return msg.sender;
	}
	function timestamp() public constant returns (uint256) {
		return block.timestamp;
	}
	function contractBalance() public constant returns (uint256) {
		return address(this).balance;
	}
	constructor() public {
		owner = msg.sender;
		if(owner == 0x0) error('System constructor: Owner address is 0x0'); 
	}
	event Error(string _error);
	event DebugUint256(uint256 _data);
}
contract Haltable is System {
	bool public halted;
	modifier stopInEmergency {
		if (halted) {
			error('Haltable: stopInEmergency function called and contract is halted');
		} else {
			_;
		}
	}
	modifier onlyInEmergency {
		if (!halted) {
			error('Haltable: onlyInEmergency function called and contract is not halted');
		} {
			_;
		}
	}
	function halt() external onlyOwner {
		halted = true;
		emit Halt(true, msg.sender, timestamp()); 
	}
	function unhalt() external onlyOwner onlyInEmergency {
		halted = false;
		emit Halt(false, msg.sender, timestamp()); 
	}
	event Halt(bool _switch, address _halter, uint256 _timestamp);
}
contract Oracles is Haltable {
	struct oracle {
		uint256 oracleId;
		bool oracleAuth;
		address oracleAddress;
	}
	mapping (address => oracle) oracleData;
	mapping (uint256 => address) oracleAddressById; 
	uint256 lastId;
	function isOracle(address _oracle) public constant returns (bool) {
		return (oracleData[_oracle].oracleAuth);
	}
	function newOracle(address _oracle) internal onlyOwner returns (uint256 id) {
		id = ++lastId;
		oracleData[_oracle].oracleId = id;
		oracleData[_oracle].oracleAuth = false;
		oracleData[_oracle].oracleAddress = _oracle;
		oracleAddressById[id] = _oracle;
		emit NewOracle(_oracle, id, timestamp()); 
	}
	function grantOracle(address _oracle) public onlyOwner {
		uint256 id;
		if (oracleData[_oracle].oracleId > 0) {
			id = oracleData[_oracle].oracleId;
		} else {
			id = newOracle(_oracle);
		}
		oracleData[_oracle].oracleAuth = true;
		emit GrantOracle(_oracle, id, timestamp()); 
	}
	function revokeOracle(address _oracle) external onlyOwner {
		oracleData[_oracle].oracleAuth = false;
		emit RevokeOracle(_oracle, timestamp()); 
	}
	function getOracleByAddress(address _oracle) public constant returns (uint256 _oracleId, bool _oracleAuth, address _oracleAddress) {
		return (oracleData[_oracle].oracleId, oracleData[_oracle].oracleAuth, oracleData[_oracle].oracleAddress);
	}
	function getOracleById(uint256 id) public constant returns (uint256 _oracleId, bool _oracleAuth, address _oracleAddress) {
		return (getOracleByAddress(oracleAddressById[id]));
	}
	event NewOracle(address indexed _who, uint256 indexed _id, uint256 _timestamp);
	event GrantOracle(address indexed _who, uint256 indexed _id, uint256 _timestamp);
	event RevokeOracle(address indexed _who, uint256 _timestamp);
}
contract Tellers is Oracles {
	address[] public tellersArray; 
	mapping (address => bytes) public pubKeys;
	bytes[] public pubKeysArray; 
	function grantTeller(address _teller, bytes _pubKey) external onlyOwner {
		if (keccak256(pubKeys[_teller]) != keccak256("")) { 
			error('grantTeller: This teller is already granted');
		}
		tellersArray.push(_teller);
		pubKeys[_teller] = _pubKey;
		pubKeysArray.push(_pubKey);
		grantOracle(_teller); 
		emit GrantTeller(_teller, _pubKey, timestamp()); 
	}
	event GrantTeller(address indexed _who, bytes _pubKey, uint256 _timestamp);
}
contract Voting is Haltable {
	mapping (address => string) votes;
	uint256 public numVotes;
	mapping (address => bool) allowed; 
	address[] votersArray;
	uint256 public numVoters;
	uint256 public deadline;
	eVotingStatus public VotingStatus; 
	enum eVotingStatus { Test, Voting, Closed }
	Oracles public SCOracles; 
	Tellers public SCTellers; 
	mapping (address => bytes) public pubKeys; 
	modifier votingClosed() { if (now >= deadline || VotingStatus == eVotingStatus.Closed) _; }
	modifier votingActive() { if (now < deadline && VotingStatus != eVotingStatus.Closed) _; }
	modifier onlyOracle() {
		if (!SCOracles.isOracle(msg.sender)) {
			error('onlyOracle function called by user that is not an authorized oracle');
		} else {
			_;
		}
	}
	modifier onlyTeller() {
		if (!SCTellers.isOracle(msg.sender)) {
			error('onlyTeller function called by user that is not an authorized teller');
		} else {
			_;
		}
	}
	constructor(address _SCOracles, address _SCTellers) public {
		SCOracles = Oracles(_SCOracles);
		SCTellers = Tellers(_SCTellers);
		deadline = now + 60 days;
		VotingStatus = eVotingStatus.Test;
	}
	function pollStatus() public constant returns (eVotingStatus) {
		if (now >= deadline) {
			return eVotingStatus.Closed;
		}
		return VotingStatus;
	}
	function isACitizen(address _voter) public constant returns (bool) {
		if (allowed[_voter]) {
			return true;
		} else {
			return false;
		}
	}
	function amIACitizen() public constant returns (bool) {
		return (isACitizen(msg.sender));
	}
	function canItVote(address _voter) internal constant returns (bool) {
		if (bytes(votes[_voter]).length == 0) {
			return true;
		} else {
			return false;
		}
	}
	function canIVote() public constant returns (bool) {
		return (canItVote(msg.sender));
	}
	function sendVote(string _vote) votingActive public returns (bool) {
		if (!canIVote()) {
			error('sendVote: sender cannot vote because it has previously casted another vote');
			return false;
		}
		if (bytes(_vote).length < 1) {
			error('sendVote: vote is empty');
			return false;
		}
		votes[msg.sender] = _vote;
		numVotes ++;
		emit SendVote(msg.sender, _vote); 
		return true;
	}
	function getVoter(uint256 _idVoter)  public constant returns (address) {
		return (votersArray[_idVoter]);
	}
	function readVote(address _voter)  public constant returns (string) {
		return (votes[_voter]);
	}
	function _grantVoter(address _voter) onlyOracle public {
		if(!allowed[_voter]) {
			allowed[_voter] = true;
			votersArray.push(_voter);
			numVoters ++;
			emit GrantVoter(_voter); 
		}
	}
	function grantVoter(address _voter, bytes _pubKey) onlyOracle public {
		_grantVoter(_voter);
		pubKeys[_voter] = _pubKey;
	}
	function getVoterPubKey(address _voter) public constant returns (bytes) {
		return (pubKeys[_voter]);
	}
	function closeVoting() onlyTeller public {
		VotingStatus = eVotingStatus.Closed;
		emit CloseVoting(true); 
	}
	function endTesting() onlyTeller public {
		numVotes = 0;
		uint256 l = votersArray.length;
		for(uint256 i = 0;i<l;i++) {
			delete votes[votersArray[i]];
		}
		VotingStatus = eVotingStatus.Voting;
	}
	function () payable public {
		revert();
	}
	event SendVote(address indexed _from, string _vote);
	event GrantVoter(address indexed _voter);
	event CloseVoting(bool _VotingClosed);
}
```

## RQ1_08b082c5c6c5

SHA-256 `182d60e410a15fead5787528a3027edcbfbf0e006983c6b305b2d01d2b8f2b26`

```solidity
pragma solidity ^0.4.24;
contract tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData); }
contract XToken {
  string public constant name = "XTOKEN";
  string public constant symbol = "XTOKEN";
  uint8 public constant decimals = 18;
  string public constant version = '0.15';
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

```

## RQ1_2f73df659ad6

SHA-256 `8c031f78cd28a5453eaf80eec9fb8f313b5c8a69b63c6e3745069e2133b80a08`

```solidity
pragma solidity ^0.4.24;
contract Ownable {
    address public Master;
    function Ownable() public {
        Master = msg.sender;
    }
    modifier onlyMaster() {
        require(msg.sender == Master);
        _;
    }
    function transferOwnership(address newMaster) public onlyMaster {
        if (newMaster != address(0)) {
            Master = newMaster;
        }
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
    modifier whenPaused {
        require(paused);
        _;
    }
    function pause() public onlyMaster whenNotPaused returns (bool) {
        paused = true;
        Pause();
        return true;
    }
    function unpause() public onlyMaster whenPaused returns (bool) {
        paused = false;
        Unpause();
        return true;
    }
}
contract UpgradeInterface {
    function isUpgradeInterface() public pure returns (bool) {
        return true;
    }
    function tryUpgrade(uint32 carID, uint8 upgradeID) public returns (bool);
}
contract EtherRacingCore is Ownable, Pausable {
    uint64 _seed = 0;
    function random(uint64 upper) internal returns (uint64) {
        _seed = uint64(keccak256(keccak256(block.blockhash(block.number), _seed), now));
        return _seed % upper;
    }
    struct CarProduct {
        string name;
        uint32 basePR; 
        uint32 baseTopSpeed; 
        uint32 baseAcceleration; 
        uint32 baseBraking; 
        uint32 baseGrip; 
        uint256 startPrice;
        uint256 currentPrice;
        uint256 earning;
        uint256 createdAt;
        uint32 entityCounter;
        bool sale;
    }
    struct CarEntity {
        uint32 productID;
        address owner;
        address earner;
        bool selling;
        uint256 auctionID;
        uint32 level;
        uint32 exp;
        uint64 genes;
        uint8[8] upgrades;
        uint32 lastCashoutIndex;
    }
    struct AuctionEntity {
        uint32 carID;
        uint256 startPrice;
        uint256 finishPrice;
        uint256 startTime;
        uint256 duration;
    }
    uint32 public newCarID = 1;
    uint32 public newCarProductID = 1;
    uint256 public newAuctionID = 1;
    bool canInit = true;
    mapping(uint32 => CarEntity) cars;
    mapping(uint32 => CarProduct) carProducts;
    mapping(uint256 => AuctionEntity) auctions;
    mapping(address => uint256) balances;
    event EventCashOut (
        address indexed player,
        uint256 amount
    );
    event EventWinReward (
        address indexed player,
        uint256 amount
    );
    event EventUpgradeCar (
        address indexed player,
        uint32 carID,
        uint8 statID,
        uint8 upgradeLevel
    );
    event EventLevelUp (
        uint32 carID,
        uint32 level,
        uint32 exp
    );
    event EventTransfer (
        address indexed player,
        address indexed receiver,
        uint32 carID
    );
    event EventTransferAction (
        address indexed player,
        address indexed receiver,
        uint32 carID,
        uint8 actionType
    );
    event EventAuction (
        address indexed player,
        uint32 carID,
        uint256 startPrice,
        uint256 finishPrice,
        uint256 duration,
        uint256 createdAt
    );
    event EventCancelAuction (
        uint32 carID
    );
    event EventBid (
        address indexed player,
        uint32 carID
    );
    event EventProduct (
        uint32 productID,
        string name,
        uint32 basePR,
        uint32 baseTopSpeed,
        uint32 baseAcceleration,
        uint32 baseBraking,
        uint32 baseGrip,
        uint256 price,
        uint256 earning,
        uint256 createdAt
    );
    event EventProductEndSale (
        uint32 productID
    );
    event EventBuyCar (
        address indexed player,
        uint32 productID,
        uint32 carID
    );
    UpgradeInterface upgradeInterface;
    uint256 public constant upgradePrice = 50 finney;
    uint256 public constant ownerCut = 500;
    function setUpgradeAddress(address _address) external onlyMaster {
        UpgradeInterface c = UpgradeInterface(_address);
        require(c.isUpgradeInterface());
        upgradeInterface = c;
    }
    function EtherRacingCore() public {
        addCarProduct("ER-1", 830,  15500, 530, 11200, 90,  10 finney,   0.1 finney);
        addCarProduct("ER-2", 1910, 17100, 509, 10700, 95,  50 finney,   0.5 finney);
        addCarProduct("ER-3", 2820, 18300, 450, 10500, 100, 100 finney,  1 finney);
        addCarProduct("ER-4", 3020, 17700, 419, 10400, 99,  500 finney,  5 finney);
        addCarProduct("ER-5", 4440, 20500, 379, 10100, 99,  1000 finney, 10 finney);
        addCarProduct("ER-6", 4520, 22000, 350, 10400, 104, 1500 finney, 15 finney);
        addCarProduct("ER-7", 4560, 20500, 340, 10200, 104, 2000 finney, 20 finney);
        addCarProduct("ER-8", 6600, 21700, 290, 9100,  139, 2500 finney, 25 finney);
    }
    function CompleteInit() public onlyMaster {
        canInit = false;
    }
    function cashOut(uint256 _amount) public whenNotPaused {
        require(_amount >= 0);
        require(_amount == uint256(uint128(_amount)));
        require(this.balance >= _amount);
        require(balances[msg.sender] >= _amount);
        if (_amount == 0)
            _amount = balances[msg.sender];
        balances[msg.sender] -= _amount;
        if (!msg.sender.send(_amount))
            balances[msg.sender] += _amount;
        EventCashOut(msg.sender, _amount);
    }
    function cashOutCar(uint32 _carID) public whenNotPaused {
        require(_carID > 0 && _carID < newCarID);
        require(cars[_carID].owner == msg.sender);
        uint256 _amount = getCarEarning(_carID);
        require(this.balance >= _amount);
        require(_amount > 0);
        var car = cars[_carID];
        var lastCashoutIndex = car.lastCashoutIndex;
        var limitCashoutIndex = carProducts[car.productID].entityCounter;
        cars[_carID].lastCashoutIndex = limitCashoutIndex;
        if (!car.owner.send(_amount))
            cars[_carID].lastCashoutIndex = lastCashoutIndex;
        EventCashOut(msg.sender, _amount);
    }
    function upgradeCar(uint32 _carID, uint8 _statID) public payable whenNotPaused {
        require(_carID > 0 && _carID < newCarID);
        require(cars[_carID].owner == msg.sender);
        require(_statID >= 0 && _statID < 8);
        require(cars[_statID].upgrades[_statID] < 20);
        require(msg.value >= upgradePrice);
        require(upgradeInterface != address(0));
        if (upgradeInterface.tryUpgrade(_carID, _statID)) {
            cars[_carID].upgrades[_statID]++;
        }
        balances[msg.sender] += msg.value - upgradePrice;
        balances[Master] += upgradePrice;
        EventUpgradeCar(msg.sender, _carID, _statID, cars[_carID].upgrades[_statID]);
    }
    function levelUpCar(uint32 _carID, uint32 _level, uint32 _exp) public onlyMaster {
        require(_carID > 0 && _carID < newCarID);
        cars[_carID].level = _level;
        cars[_carID].exp = _exp;
        EventLevelUp(_carID, _level, _exp);
    }
    function _transfer(uint32 _carID, address _receiver) public whenNotPaused {
        require(_carID > 0 && _carID < newCarID);
        require(cars[_carID].owner == msg.sender);
        require(msg.sender != _receiver);
        require(cars[_carID].selling == false);
        cars[_carID].owner = _receiver;
        cars[_carID].earner = _receiver;
        EventTransfer(msg.sender, _receiver, _carID);
    }
    function _transferAction(uint32 _carID, address _receiver, uint8 _ActionType) public whenNotPaused {
        require(_carID > 0 && _carID < newCarID);
        require(cars[_carID].owner == msg.sender);
        require(msg.sender != _receiver);
        require(cars[_carID].selling == false);
        cars[_carID].owner = _receiver;
        EventTransferAction(msg.sender, _receiver, _carID, _ActionType);
    }
    function addAuction(uint32 _carID, uint256 _startPrice, uint256 _finishPrice, uint256 _duration) public whenNotPaused {
        require(_carID > 0 && _carID < newCarID);
        require(cars[_carID].owner == msg.sender);
        require(cars[_carID].selling == false);
        require(_startPrice >= _finishPrice);
        require(_startPrice > 0 && _finishPrice >= 0);
        require(_duration > 0);
        require(_startPrice == uint256(uint128(_startPrice)));
        require(_finishPrice == uint256(uint128(_finishPrice)));
        auctions[newAuctionID] = AuctionEntity(_carID, _startPrice, _finishPrice, now, _duration);
        cars[_carID].selling = true;
        cars[_carID].auctionID = newAuctionID++;
        EventAuction(msg.sender, _carID, _startPrice, _finishPrice, _duration, now);
    }
    function bid(uint32 _carID) public payable whenNotPaused {
        require(_carID > 0 && _carID < newCarID);
        require(cars[_carID].selling == true);
        uint256 currentPrice = getCarCurrentPriceAuction(_carID);
        require(currentPrice >= 0);
        require(msg.value >= currentPrice);
        uint256 marketFee = currentPrice * ownerCut / 10000;
        balances[cars[_carID].owner] += currentPrice - marketFee;
        balances[Master] += marketFee;
        balances[msg.sender] += msg.value - currentPrice;
        cars[_carID].owner = msg.sender;
        cars[_carID].selling = false;
        delete auctions[cars[_carID].auctionID];
        cars[_carID].auctionID = 0;
        EventBid(msg.sender, _carID);
    }
    function cancelAuction(uint32 _carID) public whenNotPaused {
        require(_carID > 0 && _carID < newCarID);
        require(cars[_carID].selling == true);
        require(cars[_carID].owner == msg.sender);
        cars[_carID].selling = false;
        delete auctions[cars[_carID].auctionID];
        cars[_carID].auctionID = 0;
        EventCancelAuction(_carID);
    }
    function addCarProduct(string _name, uint32 pr,
        uint32 topSpeed, uint32 acceleration, uint32 braking, uint32 grip, uint256 _price, uint256 _earning) public onlyMaster {
        carProducts[newCarProductID++] = CarProduct(_name,
            pr, topSpeed, acceleration, braking, grip, _price, _price, _earning, now, 0, true);
        EventProduct(newCarProductID - 1, _name,
            pr, topSpeed, acceleration, braking, grip, _price, _earning, now);
    }
    function endSaleCarProduct(uint32 _carProductID) public onlyMaster {
        require(_carProductID > 0 && _carProductID < newCarProductID);
        carProducts[_carProductID].sale = false;
        EventProductEndSale(_carProductID);
    }
    function addCarInit(address owner, uint32 _carProductID, uint32 level, uint32 exp, uint64 genes) public onlyMaster {
        require(canInit == true);
        require(_carProductID > 0 && _carProductID < newCarProductID);
        carProducts[_carProductID].currentPrice += carProducts[_carProductID].earning;
        cars[newCarID++] = CarEntity(_carProductID, owner, owner, false, 0,
            level, exp, genes,
            [0, 0, 0, 0, 0, 0, 0, 0], ++carProducts[_carProductID].entityCounter);
        EventBuyCar(owner, _carProductID, newCarID - 1);
    }
    function buyCar(uint32 _carProductID) public payable {
        require(_carProductID > 0 && _carProductID < newCarProductID);
        require(carProducts[_carProductID].currentPrice > 0 && msg.value > 0);
        require(msg.value >= carProducts[_carProductID].currentPrice);
        require(carProducts[_carProductID].sale);
        if (msg.value > carProducts[_carProductID].currentPrice)
            balances[msg.sender] += msg.value - carProducts[_carProductID].currentPrice;
        carProducts[_carProductID].currentPrice += carProducts[_carProductID].earning;
        cars[newCarID++] = CarEntity(_carProductID, msg.sender, msg.sender, false, 0,
            1, 0, random(~uint64(0)),
            [0, 0, 0, 0, 0, 0, 0, 0], ++carProducts[_carProductID].entityCounter);
        balances[Master] += carProducts[_carProductID].startPrice;
        EventBuyCar(msg.sender, _carProductID, newCarID - 1);
    }
    function getCarProductName(uint32 _id) public constant returns (string) {
        return carProducts[_id].name;
    }
    function getCarProduct(uint32 _id) public constant returns (uint32[6]) {
        var carProduct = carProducts[_id];
        return [carProduct.basePR,
        carProduct.baseTopSpeed,
        carProduct.baseAcceleration,
        carProduct.baseBraking,
        carProduct.baseGrip,
        uint32(carProducts[_id].createdAt)];
    }
    function getCarDetails(uint32 _id) public constant returns (uint64[12]) {
        var car = cars[_id];
        return [uint64(car.productID),
        uint64(car.genes),
        uint64(car.upgrades[0]),
        uint64(car.upgrades[1]),
        uint64(car.upgrades[2]),
        uint64(car.upgrades[3]),
        uint64(car.upgrades[4]),
        uint64(car.upgrades[5]),
        uint64(car.upgrades[6]),
        uint64(car.upgrades[7]),
        uint64(car.level),
        uint64(car.exp)
        ];
    }
    function getCarOwner(uint32 _id) public constant returns (address) {
        return cars[_id].owner;
    }
    function getCarSelling(uint32 _id) public constant returns (bool) {
        return cars[_id].selling;
    }
    function getCarAuctionID(uint32 _id) public constant returns (uint256) {
        return cars[_id].auctionID;
    }
    function getCarEarning(uint32 _id) public constant returns (uint256) {
        var car = cars[_id];
        var carProduct = carProducts[car.productID];
        var limitCashoutIndex = carProduct.entityCounter;
        return carProduct.earning *
            (limitCashoutIndex - car.lastCashoutIndex);
    }
    function getCarCount() public constant returns (uint32) {
        return newCarID-1;
    }
    function getCarCurrentPriceAuction(uint32 _id) public constant returns (uint256) {
        require(getCarSelling(_id));
        var car = cars[_id];
        var currentAuction = auctions[car.auctionID];
        uint256 currentPrice = currentAuction.startPrice
        - (((currentAuction.startPrice - currentAuction.finishPrice) / (currentAuction.duration)) * (now - currentAuction.startTime));
        if (currentPrice < currentAuction.finishPrice)
            currentPrice = currentAuction.finishPrice;
        return currentPrice;
    }
    function getCarProductCurrentPrice(uint32 _id) public constant returns (uint256) {
        return carProducts[_id].currentPrice;
    }
    function getCarProductEarning(uint32 _id) public constant returns (uint256) {
        return carProducts[_id].earning;
    }
    function getCarProductCount() public constant returns (uint32) {
        return newCarProductID-1;
    }
    function getPlayerBalance(address _player) public constant returns (uint256) {
        return balances[_player];
    }
}

```

## RQ1_6505f6beccc4

SHA-256 `2982b781e20bc0f313056f9f5424a22d73eedf1468174468aaafc071073a3238`

```solidity
pragma solidity ^0.4.24;
contract EthRoulette {
    uint256 private secretNumber;
    uint256 public lastPlayed;
    uint256 public betPrice = 0.1 ether;
    address public ownerAddr;
    struct Game {
        address player;
        uint256 number;
    }
    Game[] public gamesPlayed;
    function CryptoRoulette() public {
        ownerAddr = msg.sender;
        shuffle();
    }
    function shuffle() internal {
        secretNumber = uint8(sha3(now, block.blockhash(block.number-1))) % 20 + 1;
    }
    function play(uint256 number) payable public {
        require(msg.value >= betPrice && number <= 10);
        Game game;
        game.player = msg.sender;
        game.number = number;
        gamesPlayed.push(game);
        if (number == secretNumber) {
            msg.sender.transfer(this.balance);
        }
        shuffle();
        lastPlayed = now;
    }
    function kill() public {
        if (msg.sender == ownerAddr && now > lastPlayed + 1 days) {
            suicide(msg.sender);
        }
    }
    function() public payable { }
}
```

## RQ1_da88771c652e

SHA-256 `f37d3ad4fb815cfe90addd6b375bdb66bb9528662c060b1ce33ef4063cc136d7`

```solidity
pragma solidity ^0.4.18;
contract LANDStorage {
  mapping (address => uint) latestPing;
  uint256 constant clearLow = 0xffffffffffffffffffffffffffffffff00000000000000000000000000000000;
  uint256 constant clearHigh = 0x00000000000000000000000000000000ffffffffffffffffffffffffffffffff;
  uint256 constant factor = 0x100000000000000000000000000000000;
}
contract AssetRegistryStorage {
  string internal _name;
  string internal _symbol;
  string internal _description;
  uint256 internal _count;
  mapping(address => uint256[]) internal _assetsOf;
  mapping(uint256 => address) internal _holderOf;
  mapping(uint256 => uint256) internal _indexOfAsset;
  mapping(uint256 => string) internal _assetData;
  mapping(address => mapping(address => bool)) internal _operators;
  bool internal _reentrancy;
}
contract OwnableStorage {
  address public owner;
  function OwnableStorage() internal {
    owner = msg.sender;
  }
}
contract ProxyStorage {
  address currentContract;
}
contract Storage is ProxyStorage, OwnableStorage, AssetRegistryStorage, LANDStorage {
}
contract DelegateProxy {
  function delegatedFwd(address _dst, bytes _calldata) internal {
    require(isContract(_dst));
    assembly {
      let result := delegatecall(sub(gas, 10000), _dst, add(_calldata, 0x20), mload(_calldata), 0, 0)
      let size := returndatasize
      let ptr := mload(0x40)
      returndatacopy(ptr, 0, size)
      switch result case 0 { revert(ptr, size) }
      default { return(ptr, size) }
    }
  }
  function isContract(address _target) constant internal returns (bool) {
    uint256 size;
    assembly { size := extcodesize(_target) }
    return size > 0;
  }
}
contract IApplication {
  function initialize(bytes data) public;
}
contract Proxy is ProxyStorage, DelegateProxy {
  event Upgrade(address indexed newContract, bytes initializedWith);
  function upgrade(IApplication newContract, bytes data) public {
    currentContract = newContract;
    newContract.initialize(data);
    Upgrade(newContract, data);
  }
  function () payable public {
    require(currentContract != 0); 
    delegatedFwd(currentContract, msg.data);
  }
}
contract LANDProxy is Storage, Proxy {
}
```

## RQ1_ff188f5f2d21

SHA-256 `c592448f6a0bb5da6a0d619dbfb9bef651cb13d9e6ab423c3ef683adcd747f72`

```solidity
pragma solidity ^0.4.24;
contract EtherRock {
    struct Rock {
        address owner;
        bool currentlyForSale;
        uint price;
        uint timesSold;
    }
    mapping (uint => Rock) public rocks;
    mapping (address => uint[]) public rockOwners;
    uint public latestNewRockForSale;
    address owner;
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    function EtherRock() {
        rocks[0].price = 10**15;
        rocks[0].currentlyForSale = true;
        owner = msg.sender;
    }
    function getRockInfo (uint rockNumber) returns (address, bool, uint, uint) {
        return (rocks[rockNumber].owner, rocks[rockNumber].currentlyForSale, rocks[rockNumber].price, rocks[rockNumber].timesSold);
    }
    function rockOwningHistory (address _address) returns (uint[]) {
        return rockOwners[_address];
    }
    function buyRock (uint rockNumber) payable {
        require(rocks[rockNumber].currentlyForSale = true);
        require(msg.value == rocks[rockNumber].price);
        rocks[rockNumber].currentlyForSale = false;
        rocks[rockNumber].timesSold++;
        if (rockNumber != latestNewRockForSale) {
            rocks[rockNumber].owner.transfer(rocks[rockNumber].price);
        }
        rocks[rockNumber].owner = msg.sender;
        rockOwners[msg.sender].push(rockNumber);
        if (rockNumber == latestNewRockForSale) {
            if (rockNumber != 99) {
                latestNewRockForSale++;
                rocks[latestNewRockForSale].price = 10**15 + (latestNewRockForSale**2 * 10**15);
                rocks[latestNewRockForSale].currentlyForSale = true;
            }
        }
    }
    function sellRock (uint rockNumber, uint price) {
        require(msg.sender == rocks[rockNumber].owner);
        require(price > 0);
        rocks[rockNumber].price = price;
        rocks[rockNumber].currentlyForSale = true;
    }
    function dontSellRock (uint rockNumber) {
        require(msg.sender == rocks[rockNumber].owner);
        rocks[rockNumber].currentlyForSale = false;
    }
    function giftRock (uint rockNumber, address receiver) {
        require(msg.sender == rocks[rockNumber].owner);
        rocks[rockNumber].owner = receiver;
        rockOwners[receiver].push(rockNumber);
    }
    function() payable {
    }
    function withdraw() onlyOwner {
        owner.transfer(this.balance);
    }
}

```

## RQ1_0f9d3ee5b5c5

SHA-256 `08894ae43738f94377f82677243d5b97b2ae7e9d782cd73864dc29b742ec8685`

```solidity
pragma solidity ^0.4.24;
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public view returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
     function transferFrom(address _from, address _to, uint256 _value) public returns (bool);
}
contract multiowned {
    struct PendingState {
        uint yetNeeded;
        uint ownersDone;
        uint index;
    }
    event Confirmation(address owner, bytes32 operation);
    event Revoke(address owner, bytes32 operation);
    event OwnerChanged(address oldOwner, address newOwner);
    event OwnerAdded(address newOwner);
    event OwnerRemoved(address oldOwner);
    event RequirementChanged(uint newRequirement);
    modifier onlyowner {
        if (isOwner(msg.sender))
            _;
    }
    modifier onlymanyowners(bytes32 _operation) {
        if (confirmAndCheck(_operation))
            _;
    }
    constructor(address[] _owners, uint _required) public {
        m_numOwners = _owners.length;
        for (uint i = 0; i < _owners.length; ++i)
        {
            m_owners[1 + i] = uint(_owners[i]);
            m_ownerIndex[uint(_owners[i])] = 1 + i;
        }
        m_required = _required;
    }
    function revoke(bytes32 _operation) external {
        uint ownerIndex = m_ownerIndex[uint(msg.sender)];
        if (ownerIndex == 0) return;
        uint ownerIndexBit = 2**ownerIndex;
        PendingState storage pending = m_pending[_operation];
        if (pending.ownersDone & ownerIndexBit > 0) {
            pending.yetNeeded++;
            pending.ownersDone -= ownerIndexBit;
            emit Revoke(msg.sender, _operation);
        }
    }
    function changeOwner(address _from, address _to) onlymanyowners(keccak256(abi.encodePacked(msg.data))) external {
        if (isOwner(_to)) return;
        uint ownerIndex = m_ownerIndex[uint(_from)];
        if (ownerIndex == 0) return;
        clearPending();
        m_owners[ownerIndex] = uint(_to);
        m_ownerIndex[uint(_from)] = 0;
        m_ownerIndex[uint(_to)] = ownerIndex;
        emit OwnerChanged(_from, _to);
    }
    function addOwner(address _owner) onlymanyowners(keccak256(abi.encodePacked(msg.data))) external {
        if (isOwner(_owner)) return;
        clearPending();
        if (m_numOwners >= c_maxOwners)
            reorganizeOwners();
        if (m_numOwners >= c_maxOwners)
            return;
        m_numOwners++;
        m_owners[m_numOwners] = uint(_owner);
        m_ownerIndex[uint(_owner)] = m_numOwners;
        emit OwnerAdded(_owner);
    }
    function removeOwner(address _owner) onlymanyowners(keccak256(abi.encodePacked(msg.data))) external {
        uint ownerIndex = m_ownerIndex[uint(_owner)];
        if (ownerIndex == 0) return;
        if (m_required > m_numOwners - 1) return;
        m_owners[ownerIndex] = 0;
        m_ownerIndex[uint(_owner)] = 0;
        clearPending();
        reorganizeOwners(); 
        emit OwnerRemoved(_owner);
    }
    function changeRequirement(uint _newRequired) onlymanyowners(keccak256(abi.encodePacked(msg.data))) external {
        if (_newRequired > m_numOwners) return;
        m_required = _newRequired;
        clearPending();
        emit RequirementChanged(_newRequired);
    }
    function isOwner(address _addr) public view returns (bool) {
        return m_ownerIndex[uint(_addr)] > 0;
    }
    function hasConfirmed(bytes32 _operation, address _owner) public view returns (bool) {
        PendingState storage pending = m_pending[_operation];
        uint ownerIndex = m_ownerIndex[uint(_owner)];
        if (ownerIndex == 0) return false;
        uint ownerIndexBit = 2**ownerIndex;
        if (pending.ownersDone & ownerIndexBit == 0) {
            return false;
        } else {
            return true;
        }
    }
    function confirmAndCheck(bytes32 _operation) internal returns (bool) {
        uint ownerIndex = m_ownerIndex[uint(msg.sender)];
        if (ownerIndex == 0) return;
        PendingState storage pending = m_pending[_operation];
        if (pending.yetNeeded == 0) {
            pending.yetNeeded = m_required;
            pending.ownersDone = 0;
            pending.index = m_pendingIndex.length++;
            m_pendingIndex[pending.index] = _operation;
        }
        uint ownerIndexBit = 2**ownerIndex;
        if (pending.ownersDone & ownerIndexBit == 0) {
            emit Confirmation(msg.sender, _operation);
            if (pending.yetNeeded <= 1) {
                delete m_pendingIndex[m_pending[_operation].index];
                delete m_pending[_operation];
                return true;
            }
            else
            {
                pending.yetNeeded--;
                pending.ownersDone |= ownerIndexBit;
            }
        }
    }
    function reorganizeOwners() private returns (bool) {
        uint free = 1;
        while (free < m_numOwners)
        {
            while (free < m_numOwners && m_owners[free] != 0) free++;
            while (m_numOwners > 1 && m_owners[m_numOwners] == 0) m_numOwners--;
            if (free < m_numOwners && m_owners[m_numOwners] != 0 && m_owners[free] == 0)
            {
                m_owners[free] = m_owners[m_numOwners];
                m_ownerIndex[m_owners[free]] = free;
                m_owners[m_numOwners] = 0;
            }
        }
    }
    function clearPending() internal {
        uint length = m_pendingIndex.length;
        for (uint i = 0; i < length; ++i) {
            if (m_pendingIndex[i] != 0) {
                delete m_pending[m_pendingIndex[i]];
            }
        }
        delete m_pendingIndex;
    }
    uint public m_required;
    uint public m_numOwners;
    uint[256] m_owners;
    uint constant c_maxOwners = 250;
    mapping(uint => uint) m_ownerIndex;
    mapping(bytes32 => PendingState) m_pending;
    bytes32[] m_pendingIndex;
}
contract daylimit is multiowned {
    modifier limitedDaily(uint _value) {
        if (underLimit(_value))
            _;
    }
    constructor(uint _limit) public {
        m_dailyLimit = _limit;
        m_lastDay = today();
    }
    function setDailyLimit(uint _newLimit) onlymanyowners(keccak256(abi.encodePacked(msg.data))) external {
        m_dailyLimit = _newLimit;
    }
    function resetSpentToday() onlymanyowners(keccak256(abi.encodePacked(msg.data))) external {
        m_spentToday = 0;
    }
    function underLimit(uint _value) internal onlyowner returns (bool) {
        if (today() > m_lastDay) {
            m_spentToday = 0;
            m_lastDay = today();
        }
        if (m_spentToday + _value >= m_spentToday && m_spentToday + _value <= m_dailyLimit) {
            m_spentToday += _value;
            return true;
        }
        return false;
    }
    function today() private view returns (uint) { return block.timestamp / 1 days; }
    uint public m_dailyLimit;
    uint public m_spentToday;
    uint public m_lastDay;
}
contract multisig {
    event Deposit(address from, uint value);
    event SingleTransact(address owner, uint value, address to);
    event MultiTransact(address owner, bytes32 operation, uint value, address to);
    event ConfirmationERC20Needed(bytes32 operation, address initiator, uint value, address to, ERC20Basic token);
    event ConfirmationETHNeeded(bytes32 operation, address initiator, uint value, address to);
    function changeOwner(address _from, address _to) external;
}
contract Wallet is multisig, multiowned, daylimit {
    uint public version = 4;
    struct Transaction {
        address to;
        uint value;
        address token;
    }
    ERC20Basic public erc20;
    constructor(address[] _owners, uint _required, uint _daylimit, address _erc20)
            multiowned(_owners, _required) daylimit(_daylimit) public {
            erc20 = ERC20Basic(_erc20);
    }
    function changeERC20(address _erc20) onlymanyowners(keccak256(abi.encodePacked(msg.data))) public {
        erc20 = ERC20Basic(_erc20);
    }
    function kill(address _to) onlymanyowners(keccak256(abi.encodePacked(msg.data))) external {
        selfdestruct(_to);
    }
    function() public payable {
        if (msg.value > 0)
            emit Deposit(msg.sender, msg.value);
    }
    function transferETH(address _to, uint _value) external onlyowner returns (bytes32 _r) {
        if (underLimit(_value)) {
            emit SingleTransact(msg.sender, _value, _to);
            _to.transfer(_value);
            return 0;
        }
        _r = keccak256(abi.encodePacked(msg.data, block.number));
        if (!confirmETH(_r) && m_txs[_r].to == 0) {
            m_txs[_r].to = _to;
            m_txs[_r].value = _value;
            emit ConfirmationETHNeeded(_r, msg.sender, _value, _to);
        }
    }
    function confirmETH(bytes32 _h) onlymanyowners(_h) public returns (bool) {
        if (m_txs[_h].to != 0) {
            m_txs[_h].to.transfer(m_txs[_h].value);
            emit MultiTransact(msg.sender, _h, m_txs[_h].value, m_txs[_h].to);
            delete m_txs[_h];
            return true;
        }
    }
    function transferERC20(address _to, uint _value) external onlyowner returns (bytes32 _r) {
        if (underLimit(_value)) {
            emit SingleTransact(msg.sender, _value, _to);
            erc20.transfer(_to, _value);
            return 0;
        }
        _r = keccak256(abi.encodePacked(msg.data, block.number));
        if (!confirmERC20(_r, address(0)) && m_txs[_r].to == 0) {
            m_txs[_r].to = _to;
            m_txs[_r].value = _value;
            m_txs[_r].token = erc20;
            emit ConfirmationERC20Needed(_r, msg.sender, _value, _to, erc20);
        }
    }
    function confirmERC20(bytes32 _h, address from) onlymanyowners(_h) public returns (bool) {
        if (m_txs[_h].to != 0) {
            ERC20Basic token = ERC20Basic(m_txs[_h].token);
            token.transferFrom(from, m_txs[_h].to, m_txs[_h].value);
            emit MultiTransact(msg.sender, _h, m_txs[_h].value, m_txs[_h].to);
            delete m_txs[_h];
            return true;
        }
    }
    function clearPending() internal {
        uint length = m_pendingIndex.length;
        for (uint i = 0; i < length; ++i)
            delete m_txs[m_pendingIndex[i]];
        super.clearPending();
    }
    mapping (bytes32 => Transaction) m_txs;
}
```

## RQ1_465b9382179b

SHA-256 `bb6c76a711fb52db31137566ed5c28cc2af719aed47c5ab1f270376a719f10ca`

```solidity
pragma solidity 0.4.24;
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
contract ERC20OldBasic {
  function totalSupply() public view returns (uint256);
  function balanceOf(address who) public view returns (uint256);
  function transfer(address to, uint256 value) public;
  event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20Old is ERC20OldBasic {
  function allowance(address owner, address spender) public view returns (uint256);
  function transferFrom(address from, address to, uint256 value) public;
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
contract WrapperLock is BasicToken, Ownable {
    using SafeMath for uint256;
    address public TRANSFER_PROXY_VEFX = 0x7e03d2b8edc3585ecd8a5807661fff0830a0b603;
    address public TRANSFER_PROXY_V2 = 0x2240Dab907db71e64d3E0dbA4800c83B5C502d4E;
    mapping (address => bool) public isSigner;
    bool public erc20old;
    string public name;
    string public symbol;
    uint public decimals;
    address public originalToken;
    mapping (address => uint256) public depositLock;
    mapping (address => uint256) public balances;
    function WrapperLock(address _originalToken, string _name, string _symbol, uint _decimals, bool _erc20old) Ownable() {
        originalToken = _originalToken;
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        isSigner[msg.sender] = true;
        erc20old = _erc20old;
    }
    function deposit(uint _value, uint _forTime) public returns (bool success) {
        require(_forTime >= 1);
        require(now + _forTime * 1 hours >= depositLock[msg.sender]);
        if (erc20old) {
            ERC20Old(originalToken).transferFrom(msg.sender, address(this), _value);
        } else {
            require(ERC20(originalToken).transferFrom(msg.sender, address(this), _value));
        }
        balances[msg.sender] = balances[msg.sender].add(_value);
        totalSupply_ = totalSupply_.add(_value);
        depositLock[msg.sender] = now + _forTime * 1 hours;
        return true;
    }
    function withdraw(
        uint _value,
        uint8 v,
        bytes32 r,
        bytes32 s,
        uint signatureValidUntilBlock
    )
        public
        returns
        (bool success)
    {
        require(balanceOf(msg.sender) >= _value);
        if (now <= depositLock[msg.sender]) {
            require(block.number < signatureValidUntilBlock);
            require(isValidSignature(keccak256(msg.sender, address(this), signatureValidUntilBlock), v, r, s));
        }
        balances[msg.sender] = balances[msg.sender].sub(_value);
        totalSupply_ = totalSupply_.sub(_value);
        depositLock[msg.sender] = 0;
        if (erc20old) {
            ERC20Old(originalToken).transfer(msg.sender, _value);
        } else {
            require(ERC20(originalToken).transfer(msg.sender, _value));
        }
        return true;
    }
    function withdrawBalanceDifference() public onlyOwner returns (bool success) {
        require(ERC20(originalToken).balanceOf(address(this)).sub(totalSupply_) > 0);
        if (erc20old) {
            ERC20Old(originalToken).transfer(msg.sender, ERC20(originalToken).balanceOf(address(this)).sub(totalSupply_));
        } else {
            require(ERC20(originalToken).transfer(msg.sender, ERC20(originalToken).balanceOf(address(this)).sub(totalSupply_)));
        }
        return true;
    }
    function withdrawDifferentToken(address _differentToken, bool _erc20old) public onlyOwner returns (bool) {
        require(_differentToken != originalToken);
        require(ERC20(_differentToken).balanceOf(address(this)) > 0);
        if (_erc20old) {
            ERC20Old(_differentToken).transfer(msg.sender, ERC20(_differentToken).balanceOf(address(this)));
        } else {
            require(ERC20(_differentToken).transfer(msg.sender, ERC20(_differentToken).balanceOf(address(this))));
        }
        return true;
    }
    function transfer(address _to, uint256 _value) public returns (bool) {
        return false;
    }
    function transferFrom(address _from, address _to, uint _value) public {
        require(isSigner[_to] || isSigner[_from]);
        assert(msg.sender == TRANSFER_PROXY_VEFX || msg.sender == TRANSFER_PROXY_V2);
        balances[_to] = balances[_to].add(_value);
        depositLock[_to] = depositLock[_to] > now ? depositLock[_to] : now + 1 hours;
        balances[_from] = balances[_from].sub(_value);
        Transfer(_from, _to, _value);
    }
    function allowance(address _owner, address _spender) public constant returns (uint) {
        if (_spender == TRANSFER_PROXY_VEFX || _spender == TRANSFER_PROXY_V2) {
            return 2**256 - 1;
        }
    }
    function balanceOf(address _owner) public constant returns (uint256) {
        return balances[_owner];
    }
    function isValidSignature(
        bytes32 hash,
        uint8 v,
        bytes32 r,
        bytes32 s
    )
        public
        constant
        returns (bool)
    {
        return isSigner[ecrecover(
            keccak256("\x19Ethereum Signed Message:\n32", hash),
            v,
            r,
            s
        )];
    }
    function addSigner(address _newSigner) public {
        require(isSigner[msg.sender]);
        isSigner[_newSigner] = true;
    }
    function keccak(address _sender, address _wrapper, uint _validTill) public constant returns(bytes32) {
        return keccak256(_sender, _wrapper, _validTill);
    }
}
```

## RQ1_597e2ef1991a

SHA-256 `df01e4e62114c3f5759568f2a132dfafad552260d1333dd3cb6b079515bf9c36`

```solidity
pragma solidity ^0.4.19;
contract ScriniumPresale {
    string public name = "Scrinium";
    string public symbol = "SCR";
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
    function ScriniumPresale() public {
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

## RQ1_3b8914256cc2

SHA-256 `2bb915c9f919cdf9acfb6f4ae1f6cc59a379f50d3b91cd6a5de0a1d9554481cc`

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
contract BLACKCOIN is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "BLACKCOIN";
    string public constant symbol = "BKC";
    uint public constant decimals = 5;
    uint256 public totalSupply = 20000000000e5;
    uint256 public totalDistributed = 12000000000e5;
    uint256 public totalRemaining = totalSupply.sub(totalDistributed);
    uint256 public value = 150000e5;
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
    function  BLACKCOIS() public {
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

## RQ1_74db7b05248a

SHA-256 `18fefaf83bfb6f5b97e40049d5cba44b2d241f8155bc4668f2ab1aa46d06ea3a`

```solidity
pragma solidity ^0.4.22;
contract Auctionify {
    address public beneficiary;
    uint public auctionEnd;
    string public auctionTitle;
    string public auctionDescription;
    uint public minimumBid;
    address public escrowModerator;
    address public highestBidder;
    mapping(address => uint) public bids;
    enum AuctionStates { Started, Ongoing, Ended }
    AuctionStates public auctionState;
    modifier auctionNotEnded()
    {
        require(
            now < auctionEnd, 
            "Auction already ended."
        );
        require(
          auctionState != AuctionStates.Ended,
           "Auction already ended."
          );
        _;
    }
    modifier isMinimumBid()
    {
      require(
          msg.value >= minimumBid,
          "The value is smaller than minimum bid."
      );
      _;
    }
    modifier isHighestBid()
    {
      require(
          msg.value > bids[highestBidder],
          "There already is a higher bid."
      );
      _;
    }
    modifier onlyHighestBidderOrEscrow()
    {
      if ((msg.sender == highestBidder) || (msg.sender == escrowModerator) || (highestBidder == address(0))) {
        _;
      }
      else{
        revert();
      }
    }
    event HighestBidIncreased(address bidder, uint amount);
    event AuctionEnded(address winner, uint amount);
    event CheaterBidder(address cheater, uint amount);
    constructor(
        string _auctionTitle,
        uint _auctionEnd,
        address _beneficiary,
        string _auctionDesc,
        uint _minimumBid,
        bool _escrowEnabled,
        bool _listed
    ) public {
        auctionTitle = _auctionTitle;
        beneficiary = _beneficiary;
        auctionEnd = _auctionEnd;
        auctionDescription = _auctionDesc;
        auctionState = AuctionStates.Started;
        minimumBid = _minimumBid;
        if (_escrowEnabled) {
          escrowModerator = address(0x32cEfb2dC869BBfe636f7547CDa43f561Bf88d5A); 
        }
        if (_listed) {
        }
    }
    function bid() public payable auctionNotEnded isMinimumBid isHighestBid {
        if (highestBidder != address(0)) {
            uint lastBid = bids[highestBidder];
            bids[highestBidder] = 0;
            if(!highestBidder.send(lastBid)) {
                emit CheaterBidder(highestBidder, lastBid);
            }
        }
        highestBidder = msg.sender;
        bids[msg.sender] = msg.value;
        auctionState = AuctionStates.Ongoing;
        emit HighestBidIncreased(msg.sender, msg.value);
    }
    function highestBid() public view returns(uint){
      return (bids[highestBidder]);
    }
    function endAuction() public onlyHighestBidderOrEscrow {
        require(now >= auctionEnd, "Auction not yet ended.");
        require(auctionState != AuctionStates.Ended, "Auction has already ended.");
        auctionState = AuctionStates.Ended;
        emit AuctionEnded(highestBidder, bids[highestBidder]);
        if(!beneficiary.send(bids[highestBidder])) {
        }
    }
  function cleanUpAfterYourself() public {
    require(auctionState == AuctionStates.Ended, "Auction is not ended.");
      if (escrowModerator != address(0)) {
        selfdestruct(escrowModerator);
      } else {
        selfdestruct(beneficiary); 
      }
  }
}
```

## RQ1_2a9fa56d6447

SHA-256 `9b38e255372c88160f20dd7a7ea09c72fc93931300830af440d7528eedcaf50e`

```solidity
pragma solidity ^0.4.24;
contract ERC20Basic {
  function totalSupply() public view returns (uint256);
  function balanceOf(address who) public view returns (uint256);
  function transfer(address to, uint256 value) public returns (bool);
  event Transfer(address indexed from, address indexed to, uint256 value);
}
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
contract Ownable {
  address public owner;
  event OwnershipRenounced(address indexed previousOwner);
  event OwnershipTransferred(
    address indexed previousOwner,
    address indexed newOwner
  );
  constructor() public {
    owner = msg.sender;
  }
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }
  function renounceOwnership() public onlyOwner {
    emit OwnershipRenounced(owner);
    owner = address(0);
  }
  function transferOwnership(address _newOwner) public onlyOwner {
    _transferOwnership(_newOwner);
  }
  function _transferOwnership(address _newOwner) internal {
    require(_newOwner != address(0));
    emit OwnershipTransferred(owner, _newOwner);
    owner = _newOwner;
  }
}
library Roles {
  struct Role {
    mapping (address => bool) bearer;
  }
  function add(Role storage role, address addr)
    internal
  {
    role.bearer[addr] = true;
  }
  function remove(Role storage role, address addr)
    internal
  {
    role.bearer[addr] = false;
  }
  function check(Role storage role, address addr)
    view
    internal
  {
    require(has(role, addr));
  }
  function has(Role storage role, address addr)
    view
    internal
    returns (bool)
  {
    return role.bearer[addr];
  }
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
    emit Transfer(msg.sender, _to, _value);
    return true;
  }
  function balanceOf(address _owner) public view returns (uint256) {
    return balances[_owner];
  }
}
contract MultiSigTransfer is Ownable {
  string public name = "MultiSigTransfer";
  string public symbol = "MST";
  bool public complete = false;
  bool public denied = false;
  uint32 public quantity;
  address public targetAddress;
  address public requesterAddress;
  constructor(
    uint32 _quantity,
    address _targetAddress,
    address _requesterAddress
  ) public {
    quantity = _quantity;
    targetAddress = _targetAddress;
    requesterAddress = _requesterAddress;
  }
  function approveTransfer() public onlyOwner {
    require(denied == false, "cannot approve a denied transfer");
    require(complete == false, "cannot approve a complete transfer");
    complete = true;
  }
  function denyTransfer() public onlyOwner {
    require(denied == false, "cannot deny a transfer that is already denied");
    denied = true;
  }
  function isPending() public view returns (bool) {
    return !complete;
  }
}
contract RBAC {
  using Roles for Roles.Role;
  mapping (string => Roles.Role) private roles;
  event RoleAdded(address indexed operator, string role);
  event RoleRemoved(address indexed operator, string role);
  function checkRole(address _operator, string _role)
    view
    public
  {
    roles[_role].check(_operator);
  }
  function hasRole(address _operator, string _role)
    view
    public
    returns (bool)
  {
    return roles[_role].has(_operator);
  }
  function addRole(address _operator, string _role)
    internal
  {
    roles[_role].add(_operator);
    emit RoleAdded(_operator, _role);
  }
  function removeRole(address _operator, string _role)
    internal
  {
    roles[_role].remove(_operator);
    emit RoleRemoved(_operator, _role);
  }
  modifier onlyRole(string _role)
  {
    checkRole(msg.sender, _role);
    _;
  }
}
contract KinesisVelocityToken is BasicToken, Ownable, RBAC {
  string public name = "KinesisVelocityToken";
  string public symbol = "KVT";
  uint8 public decimals = 0;
  string public constant ADMIN_ROLE = "ADMIN";
  address[] public transfers;
  uint public constant INITIAL_SUPPLY = 300000;
  uint public totalSupply = 0;
  bool public isTransferable = false;
  bool public toggleTransferablePending = false;
  address public transferToggleRequester = address(0);
  constructor() public {
    totalSupply = INITIAL_SUPPLY;
    balances[msg.sender] = INITIAL_SUPPLY;
    addRole(msg.sender, ADMIN_ROLE);
  }
  function isOwner(address _address) public view returns (bool) {
    return owner == _address;
  }
  function getTransfers() public view returns (address[]) {
    return transfers;
  }
  function isAdmin(address _address) public view returns (bool) {
    return hasRole(_address, ADMIN_ROLE);
  }
  function setAdmin(address _newAdmin) public onlyOwner {
    return addRole(_newAdmin, ADMIN_ROLE);
  }
  function removeAdmin(address _oldAdmin) public onlyOwner {
    return removeRole(_oldAdmin, ADMIN_ROLE);
  }
  function setTransferable(bool _toState) public onlyRole(ADMIN_ROLE) {
    require(isTransferable != _toState, "to init a transfer toggle, the toState must change");
    toggleTransferablePending = true;
    transferToggleRequester = msg.sender;
  }
  function approveTransferableToggle() public onlyRole(ADMIN_ROLE) {
    require(toggleTransferablePending == true, "transfer toggle not in pending state");
    require(transferToggleRequester != msg.sender, "the requester cannot approve the transfer toggle");
    isTransferable = !isTransferable;
    toggleTransferablePending = false;
    transferToggleRequester = address(0);
  }
  function _transfer(address _to, address _from, uint256 _value) private returns (bool) {
    require(_value <= balances[_from], "the balance in the from address is smaller than the tx value");
    balances[_from] = balances[_from].sub(_value);
    balances[_to] = balances[_to].add(_value);
    emit Transfer(_from, _to, _value);
    return true;
  }
  function transfer(address _to, uint256 _value) public returns (bool) {
    require(_to != address(0), "cannot transfer to the zero address");
    if (_to != owner && msg.sender != crowdsale) {
      require(isTransferable == true, "kvt is not yet transferable");
    }
    require(msg.sender != owner, "the owner of the kvt contract cannot transfer");
    return _transfer(_to, msg.sender, _value);
  }
  function adminTransfer(address _to, uint32 _quantity) public onlyRole(ADMIN_ROLE) {
    address newTransfer = new MultiSigTransfer(_quantity, _to, msg.sender);
    transfers.push(newTransfer);
  }
  function approveTransfer(address _approvedTransfer) public onlyRole(ADMIN_ROLE) returns (bool) {
    MultiSigTransfer transferToApprove = MultiSigTransfer(_approvedTransfer);
    uint32 transferQuantity = transferToApprove.quantity();
    address deliveryAddress = transferToApprove.targetAddress();
    address requesterAddress = transferToApprove.requesterAddress();
    require(msg.sender != requesterAddress, "a requester cannot approve an admin transfer");
    transferToApprove.approveTransfer();
    return _transfer(deliveryAddress, owner, transferQuantity);
  }
  function denyTransfer(address _approvedTransfer) public onlyRole(ADMIN_ROLE) returns (bool) {
    MultiSigTransfer transferToApprove = MultiSigTransfer(_approvedTransfer);
    transferToApprove.denyTransfer();
  }
  address public crowdsale = address(0);
  function setCrowdsaleAddress(address _crowdsaleAddress) public onlyRole(ADMIN_ROLE) {
    crowdsale = _crowdsaleAddress;
  }
}
```

## RQ1_33c9a3f3758b

SHA-256 `8014d42c02a11a1bf68960a1626c343d6a0888c56f3153f78989b704a8ba6ca7`

```solidity
pragma solidity ^0.4.18;
contract LuckyNumber {
    address owner;
    uint winningNumber = uint(keccak256(now, owner)) % 10;
    function LuckyNumber() public { 
        owner = msg.sender;
    }
    function addBalance() public payable {
    }
    function() public payable {
       msg.sender.transfer(msg.value); 
    }
    function getOwner() view public returns (address)  {
        return owner;
    }
    function getBalance() view public returns (uint) {
        return this.balance;
    }
    function kill() public { 
        if (msg.sender == owner)  
            selfdestruct(owner);       
    }
    function takeAGuess(uint _myGuess) public payable {
        require(msg.value == 0.0001 ether);
        if (_myGuess == winningNumber) {
            msg.sender.transfer((this.balance*9)/10);
            selfdestruct(owner);
        }
    }
}
```

## RQ1_eaefa1b812c4

SHA-256 `0d59acebed46990c4cc22b4e78edabd57c250dba8071bc0679cf7d8b23f4e612`

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
contract HGToken is StandardToken {
   string public name = 'HGToken';
   string public symbol = 'HGT';
   uint public decimals = 8;
   uint public INITIAL_SUPPLY = 1000000000;
   uint public _frozeAmount = 400000000;
   uint _firstUnlockAmmount = 50000000;
   uint _secondUnlockAmmount = 50000000;
   uint _firstUnlockTime;
   uint _secondUnlockTime;
   function HGToken() public {
     totalSupply = 500000000;
     balances[msg.sender] = 500000000;
     _firstUnlockTime  = now + 31536000;
     _secondUnlockTime = now + 63072000;
   }
   function releaseFirstUnlock() public onlyOwner returns (bool success){
        require(now >= _firstUnlockTime);
        require(_firstUnlockAmmount > 0);
        balances[msg.sender] = addSafe(balances[msg.sender], _firstUnlockAmmount);
        _firstUnlockAmmount = 0;
        Transfer(address(0), msg.sender, _firstUnlockAmmount);
        return true;
    }
    function releaseSecondUnlock() public onlyOwner returns (bool success){
        require(now >= _secondUnlockTime);
        require(_secondUnlockAmmount > 0);
        balances[msg.sender] = addSafe(balances[msg.sender], _secondUnlockAmmount);
        _secondUnlockAmmount = 0;
        Transfer(address(0), msg.sender, _secondUnlockAmmount);
        return true;
    }
}
```

## RQ1_8ce69a76eabf

SHA-256 `4c6a6ff7dce3b9b12024311e37fc60e822e7b4c74184f4c4548fabe769712d6e`

```solidity
pragma solidity 0.5.0;
interface IERC165 {
  function supportsInterface(bytes4 interfaceId)
    external
    view
    returns (bool);
}
pragma solidity 0.5.0;
contract IERC721 is IERC165 {
  event Transfer(
    address indexed from,
    address indexed to,
    uint256 indexed tokenId
  );
  event Approval(
    address indexed owner,
    address indexed approved,
    uint256 indexed tokenId
  );
  event ApprovalForAll(
    address indexed owner,
    address indexed operator,
    bool approved
  );
  function balanceOf(address owner) public view returns (uint256 balance);
  function ownerOf(uint256 tokenId) public view returns (address owner);
  function approve(address to, uint256 tokenId) public;
  function getApproved(uint256 tokenId)
    public view returns (address operator);
  function setApprovalForAll(address operator, bool _approved) public;
  function isApprovedForAll(address owner, address operator)
    public view returns (bool);
  function transferFrom(address from, address to, uint256 tokenId) public;
  function safeTransferFrom(address from, address to, uint256 tokenId)
    public;
  function safeTransferFrom(
    address from,
    address to,
    uint256 tokenId,
    bytes memory data
  )
    public;
}
pragma solidity 0.5.0;
contract IERC721Enumerable is IERC721 {
  function totalSupply() public view returns (uint256);
  function tokenOfOwnerByIndex(
    address owner,
    uint256 index
  )
    public
    view
    returns (uint256 tokenId);
  function tokenByIndex(uint256 index) public view returns (uint256);
}
pragma solidity 0.5.0;
contract IERC721Receiver {
  function onERC721Received(
    address operator,
    address from,
    uint256 tokenId,
    bytes memory data
  )
    public
    returns(bytes4);
}
pragma solidity 0.5.0;
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
pragma solidity 0.5.0;
library Address {
  function isContract(address account) internal view returns (bool) {
    uint256 size;
    assembly { size := extcodesize(account) }
    return size > 0;
  }
}
pragma solidity 0.5.0;
contract ERC165 is IERC165 {
  bytes4 private constant _InterfaceId_ERC165 = 0x01ffc9a7;
  mapping(bytes4 => bool) internal _supportedInterfaces;
  constructor()
    public
  {
    _registerInterface(_InterfaceId_ERC165);
  }
  function supportsInterface(bytes4 interfaceId)
    external
    view
    returns (bool)
  {
    return _supportedInterfaces[interfaceId];
  }
  function _registerInterface(bytes4 interfaceId)
    internal
  {
    require(interfaceId != 0xffffffff);
    _supportedInterfaces[interfaceId] = true;
  }
}
pragma solidity 0.5.0;
contract ERC721 is ERC165, IERC721 {
  using SafeMath for uint256;
  using Address for address;
  bytes4 private constant _ERC721_RECEIVED = 0x150b7a02;
  mapping (uint256 => address) private _tokenOwner;
  mapping (uint256 => address) private _tokenApprovals;
  mapping (address => uint256) private _ownedTokensCount;
  mapping (address => mapping (address => bool)) private _operatorApprovals;
  bytes4 private constant _InterfaceId_ERC721 = 0x80ac58cd;
  constructor()
    public
  {
    _registerInterface(_InterfaceId_ERC721);
  }
  function balanceOf(address owner) public view returns (uint256) {
    require(owner != address(0));
    return _ownedTokensCount[owner];
  }
  function ownerOf(uint256 tokenId) public view returns (address) {
    address owner = _tokenOwner[tokenId];
    require(owner != address(0));
    return owner;
  }
  function approve(address to, uint256 tokenId) public {
    address owner = ownerOf(tokenId);
    require(to != owner);
    require(msg.sender == owner || isApprovedForAll(owner, msg.sender));
    _tokenApprovals[tokenId] = to;
    emit Approval(owner, to, tokenId);
  }
  function getApproved(uint256 tokenId) public view returns (address) {
    require(_exists(tokenId));
    return _tokenApprovals[tokenId];
  }
  function setApprovalForAll(address to, bool approved) public {
    require(to != msg.sender);
    _operatorApprovals[msg.sender][to] = approved;
    emit ApprovalForAll(msg.sender, to, approved);
  }
  function isApprovedForAll(
    address owner,
    address operator
  )
    public
    view
    returns (bool)
  {
    return _operatorApprovals[owner][operator];
  }
  function transferFrom(
    address from,
    address to,
    uint256 tokenId
  )
    public
  {
    require(_isApprovedOrOwner(msg.sender, tokenId));
    require(to != address(0));
    _clearApproval(from, tokenId);
    _removeTokenFrom(from, tokenId);
    _addTokenTo(to, tokenId);
    emit Transfer(from, to, tokenId);
  }
  function safeTransferFrom(
    address from,
    address to,
    uint256 tokenId
  )
    public
  {
    safeTransferFrom(from, to, tokenId, "");
  }
  function safeTransferFrom(
    address from,
    address to,
    uint256 tokenId,
    bytes memory _data
  )
    public
  {
    transferFrom(from, to, tokenId);
    require(_checkAndCallSafeTransfer(from, to, tokenId, _data));
  }
  function _exists(uint256 tokenId) internal view returns (bool) {
    address owner = _tokenOwner[tokenId];
    return owner != address(0);
  }
  function _isApprovedOrOwner(
    address spender,
    uint256 tokenId
  )
    internal
    view
    returns (bool)
  {
    address owner = ownerOf(tokenId);
    return (
      spender == owner ||
      getApproved(tokenId) == spender ||
      isApprovedForAll(owner, spender)
    );
  }
  function _mint(address to, uint256 tokenId) internal {
    require(to != address(0));
    _addTokenTo(to, tokenId);
    emit Transfer(address(0), to, tokenId);
  }
  function _burn(address owner, uint256 tokenId) internal {
    _clearApproval(owner, tokenId);
    _removeTokenFrom(owner, tokenId);
    emit Transfer(owner, address(0), tokenId);
  }
  function _clearApproval(address owner, uint256 tokenId) internal {
    require(ownerOf(tokenId) == owner);
    if (_tokenApprovals[tokenId] != address(0)) {
      _tokenApprovals[tokenId] = address(0);
    }
  }
  function _addTokenTo(address to, uint256 tokenId) internal {
    require(_tokenOwner[tokenId] == address(0));
    _tokenOwner[tokenId] = to;
    _ownedTokensCount[to] = _ownedTokensCount[to].add(1);
  }
  function _removeTokenFrom(address from, uint256 tokenId) internal {
    require(ownerOf(tokenId) == from);
    _ownedTokensCount[from] = _ownedTokensCount[from].sub(1);
    _tokenOwner[tokenId] = address(0);
  }
  function _checkAndCallSafeTransfer(
    address from,
    address to,
    uint256 tokenId,
    bytes memory _data
  )
    internal
    returns (bool)
  {
    if (!to.isContract()) {
      return true;
    }
    bytes4 retval = IERC721Receiver(to).onERC721Received(
      msg.sender, from, tokenId, _data);
    return (retval == _ERC721_RECEIVED);
  }
}
pragma solidity 0.5.0;
contract ERC721Enumerable is ERC165, ERC721, IERC721Enumerable {
  mapping(address => uint256[]) private _ownedTokens;
  mapping(uint256 => uint256) private _ownedTokensIndex;
  uint256[] private _allTokens;
  mapping(uint256 => uint256) private _allTokensIndex;
  bytes4 private constant _InterfaceId_ERC721Enumerable = 0x780e9d63;
  constructor() public {
    _registerInterface(_InterfaceId_ERC721Enumerable);
  }
  function tokenOfOwnerByIndex(
    address owner,
    uint256 index
  )
    public
    view
    returns (uint256)
  {
    require(index < balanceOf(owner));
    return _ownedTokens[owner][index];
  }
  function totalSupply() public view returns (uint256) {
    return _allTokens.length;
  }
  function tokenByIndex(uint256 index) public view returns (uint256) {
    require(index < totalSupply());
    return _allTokens[index];
  }
  function _addTokenTo(address to, uint256 tokenId) internal {
    super._addTokenTo(to, tokenId);
    uint256 length = _ownedTokens[to].length;
    _ownedTokens[to].push(tokenId);
    _ownedTokensIndex[tokenId] = length;
  }
  function _removeTokenFrom(address from, uint256 tokenId) internal {
    super._removeTokenFrom(from, tokenId);
    uint256 tokenIndex = _ownedTokensIndex[tokenId];
    uint256 lastTokenIndex = _ownedTokens[from].length.sub(1);
    uint256 lastToken = _ownedTokens[from][lastTokenIndex];
    _ownedTokens[from][tokenIndex] = lastToken;
    _ownedTokens[from].length--;
    _ownedTokensIndex[tokenId] = 0;
    _ownedTokensIndex[lastToken] = tokenIndex;
  }
  function _mint(address to, uint256 tokenId) internal {
    super._mint(to, tokenId);
    _allTokensIndex[tokenId] = _allTokens.length;
    _allTokens.push(tokenId);
  }
  function _burn(address owner, uint256 tokenId) internal {
    super._burn(owner, tokenId);
    uint256 tokenIndex = _allTokensIndex[tokenId];
    uint256 lastTokenIndex = _allTokens.length.sub(1);
    uint256 lastToken = _allTokens[lastTokenIndex];
    _allTokens[tokenIndex] = lastToken;
    _allTokens[lastTokenIndex] = 0;
    _allTokens.length--;
    _allTokensIndex[tokenId] = 0;
    _allTokensIndex[lastToken] = tokenIndex;
  }
}
pragma solidity 0.5.0;
contract IERC721Metadata is IERC721 {
  function name() external view returns (string memory name);
  function symbol() external view returns (string memory symbol);
  function tokenURI(uint256 tokenId) public view returns (string memory uri);
}
pragma solidity 0.5.0;
contract NametagToken  is ERC721Enumerable, IERC721Metadata {
  string internal _name = 'NametagToken';
  string internal _symbol = 'NTT';
  mapping(uint256 => string) private _tokenURIs;
  mapping(uint256 => address) private reservedTokenId;
    bytes4 private constant InterfaceId_ERC721Metadata = 0x5b5e139f;
    constructor( ) public {
      _registerInterface(InterfaceId_ERC721Metadata);
    }
  function reserveToken( address to, uint256 tokenId ) public  returns (bool)
  {
      reservedTokenId[tokenId] = to;
      return true;
  }
  function claimToken( address to,  string memory name  ) public  returns (bool)
  {
    require(containsOnlyLower(name));
    uint256 tokenId = (uint256) (keccak256(abi.encodePacked(name)));
    require( reservedTokenId[tokenId] == address(0x0) || reservedTokenId[tokenId] == to  );
    _mint(to, tokenId);
    _setTokenURI(tokenId, name);
    return true;
  }
  function nameToTokenId(string memory name) public view returns (uint256) {
    string memory lowerName = _toLower(name);
    return  (uint256) (keccak256(abi.encodePacked(lowerName)));
  }
  function containsOnlyAlphaNumerics(string memory str) public view returns (bool) {
      bytes memory bStr = bytes(str);
      for (uint i = 0; i < bStr.length; i++) {
          bytes1  char = bStr[i];
          if ( !( ((char >= 0x30) && (char <= 0x39))
                || ((char >= 0x41) && (char <= 0x5A))
                  || ((char >= 0x61) && (char <= 0x7A)) )   ) {
          return false;
        }
      }
      return true;
    }
    function containsOnlyLower(string memory str) public view returns (bool) {
        bytes memory bStr = bytes(str);
        for (uint i = 0; i < bStr.length; i++) {
            bytes1   char = bStr[i];
            if ( !((char >= 0x61) && (char <= 0x7A))   ) {
            return false;
          }
        }
        return true;
      }
       function _toLower(string memory  _base)
           internal
           pure
           returns (string memory str) {
           bytes memory _baseBytes = bytes(_base);
           for (uint i = 0; i < _baseBytes.length; i++) {
               _baseBytes[i] = _lower(_baseBytes[i]);
           }
           return string(_baseBytes);
       }
   function _lower(bytes1 _b1)
       private
       pure
       returns (bytes1) {
       if (_b1 >= 0x41 && _b1 <= 0x5A) {
           return bytes1(uint8(_b1)+32);
       }
       return _b1;
   }
  function name() external view returns (string memory name) {
    return _name;
  }
   function symbol() external view returns (string memory symbol) {
      return _symbol;
   }
  function tokenURI(uint256 tokenId) public view returns (string memory uti) {
    require(_exists(tokenId));
    return _tokenURIs[tokenId];
  }
  function _setTokenURI(uint256 tokenId, string memory uri) internal {
    require(_exists(tokenId));
    _tokenURIs[tokenId] = uri;
  }
  function _burn(address owner, uint256 tokenId) internal {
    super._burn(owner, tokenId);
    if (bytes(_tokenURIs[tokenId]).length != 0) {
      delete _tokenURIs[tokenId];
    }
  }
}
```

## RQ1_d4c299ba722e

SHA-256 `3131b2de91dba8114b3997eb81d9f0d78e666e7b14ec4547a81741d0b563e8fa`

```solidity
pragma solidity 0.5.7;
interface IHumanityRegistry {
    function isHuman(address who) external view returns (bool);
}
contract Question {
    IHumanityRegistry public registry;
    bytes32 public answerHash = 0x3f071a4c8c4762d45888fda3b7ff73f3d32dac78fd7b374266dec429dfabdfa8;
    constructor(IHumanityRegistry _registry) public payable {
        registry = _registry;
    }
    function answer(string memory response) public {
        require(registry.isHuman(msg.sender), "Question::answer: Only humans can answer");
        if (keccak256(abi.encode(response)) == answerHash) {
            selfdestruct(msg.sender);
        } else {
            revert("Question::answer: Incorrect response");
        }
    }
}
```

## RQ1_e7c2ee23438d

SHA-256 `394223f761ad29a5732de06762b45f07186941dae9569c413d8a8fea53db6242`

```solidity
pragma solidity ^0.4.24;
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
contract Shaycoin is owned {
    string public name;
    string public symbol;
    uint256 public decimals = 18; 
    uint256 public totalSupply;
    uint256 public donations = 0;
    uint256 public price = 200000000000000;
    mapping (address => uint256) public balanceOf;
    mapping (uint256 => address) public depositIndex;
    mapping (address => bool) public depositBool;
    uint256 public indexTracker = 0;
    event Transfer(address indexed from, address indexed to, uint256 value);
    function Shaycoin(
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    ) public {
        totalSupply = initialSupply * 10 ** decimals;  
        balanceOf[this] = totalSupply;                
        name = tokenName;                                   
        symbol = tokenSymbol;                               
    }
    function _transfer(address _from, address _to, uint256 _value) internal {
        require (_to != 0x0);                               
        require (balanceOf[_from] >= _value);               
        require (balanceOf[_to] + _value > balanceOf[_to]); 
        balanceOf[_from] -= _value;                         
        balanceOf[_to] += _value;                           
        if (_to != address(this) && !depositBool[_to]) {
           depositIndex[indexTracker] = _to;
           depositBool[_to] = true;
           indexTracker += 1;
        }
        Transfer(_from, _to, _value);
    }
    function buy() payable public {
        uint256 amount = 10 ** decimals * msg.value / price;               
        if (amount > balanceOf[this]) {
            totalSupply += amount - balanceOf[this];
            balanceOf[this] = amount;
        }
        _transfer(this, msg.sender, amount);                                        
    }
    function sell(uint256 amount) public {
        require(this.balance >= amount * price / 10 ** decimals);      
        _transfer(msg.sender, this, amount);                                    
        msg.sender.transfer(amount * price / 10 ** decimals);          
    }
    function donate() payable public {
        donations += msg.value;
    }
    function collectDonations() onlyOwner public {
        owner.transfer(donations);
        donations = 0;
    }
    function killAndRefund() onlyOwner public {
        for (uint256 i = 0; i < indexTracker; i++) {
            depositIndex[i].transfer(balanceOf[depositIndex[i]] * price / 10 ** decimals);
        }
        selfdestruct(owner);
    }
    function transfer(address _to, uint256 _value) public {
        _transfer(msg.sender, _to, _value);
    }
 }

```

## RQ1_224d9bccba32

SHA-256 `216794f148456bc33214c30c097fed91b9e3137a435c00090eddc402718dc5bf`

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
contract VoipToken is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "VoipToken";
    string public constant symbol = "VOIP";
    uint public constant decimals = 8;
    uint256 public totalSupply = 20000000000e8;
    uint256 public totalDistributed = 0;    
    uint256 public constant MIN_CONTRIBUTION = 1 ether / 100; 
    uint256 public tokensPerEth = 15000000e8;
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
    function VoipTken () public {
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

## RQ1_58a929410f82

SHA-256 `b41d98a1018eb0dd438870af8b0f32644236feea49828cd3ed2d61f600931f43`

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
contract SafeDeposit is TokenVault {
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

## RQ1_3e5b433cf8f3

SHA-256 `f88f3c8505cf34a2e89af4628552f89809de5cc47ea6d722d6adcb4a85afa8dc`

```solidity
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
        if (amount < 1 ether) {
            msg.sender.send(msg.value);
            return false;
        }
        if (amount > 100 ether) {
            msg.sender.send(msg.value - 100 ether);
            amount = 100 ether;
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
            playersAmounts.push(amount / 100 * 150);
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

## RQ1_871c28b72510

SHA-256 `266f447380eabfa48fd2476e87ab6b56ace890e52ffe3122abf921e3a39bce5c`

```solidity
pragma solidity >=0.5.0 <0.6.0;
contract owned {
    address public owner;
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
library SafeMath {
   function mul(uint a, uint b) internal pure returns (uint) {
     if (a == 0) {
        return 0;
      }
      uint c = a * b;
      assert(c / a == b);
      return c;
   }
   function sub(uint a, uint b) internal pure returns (uint) {
      assert(b <= a);
      return a - b;
   }
   function add(uint a, uint b) internal pure returns (uint) {
      uint c = a + b;
      assert(c >= a);
      return c;
   }
  function div(uint a, uint b) internal pure returns (uint256) {
    uint c = a / b;
    assert(a == b * c + a % b); 
    return c;
  }
}
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes calldata _extraData) external; }
contract TokenERC20 {
    using SafeMath for uint256;
    string public name;
    string public symbol;
    uint8 public decimals = 0;
    uint256 public totalSupply;
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Burn(address indexed from, uint256 value);
    constructor(
        uint256 initialSupply,
        string memory tokenName,
        string memory tokenSymbol
    ) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);  
        balanceOf[msg.sender] = totalSupply;                    
        name = tokenName;                                       
        symbol = tokenSymbol;                                   
    }
    function _transfer(address _from, address _to, uint _value) internal {
        require(_to != address(0x0));
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to].add(_value) > balanceOf[_to]);
        uint previousBalances = balanceOf[_from].add(balanceOf[_to]);
        balanceOf[_from] = balanceOf[_from].sub(_value);
        balanceOf[_to] =balanceOf[_to].add(_value);
        emit Transfer(_from, _to, _value);
        assert(balanceOf[_from].add(balanceOf[_to]) == previousBalances);
    }
    function transfer(address _to, uint256 _value) public returns(bool success){
        _transfer(msg.sender, _to, _value);
        return true;
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
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    function approveAndCall(address _spender, uint256 _value, bytes memory _extraData)
        public
        returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        if (approve(_spender, _value)) {
            spender.receiveApproval(msg.sender, _value, address(this), _extraData);
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
        emit Burn(_from, _value);
        return true;
    }
}
contract bitBond1906 is owned, TokenERC20 {
    using SafeMath for uint256;
    mapping (address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
    constructor(
        uint256 initialSupply,
        string memory tokenName,
        string memory tokenSymbol
    ) TokenERC20(initialSupply, tokenName, tokenSymbol) public {}
    function _transfer(address _from, address _to, uint _value) internal {
        require (_to != address(0x0));                               
        require (balanceOf[_from] >= _value);               
        require (balanceOf[_to].add(_value) > balanceOf[_to]); 
        require(!frozenAccount[_from]);                     
        require(!frozenAccount[_to]);                       
        balanceOf[_from] = balanceOf[_from].sub(_value);                         
        balanceOf[_to] = balanceOf[_to].add(_value);                           
        emit Transfer(_from, _to, _value);
    }
    function mintToken(address target, uint256 mintedAmount) onlyOwner public {
        balanceOf[target] = balanceOf[target].add(mintedAmount);
        totalSupply = totalSupply.add(mintedAmount);
        emit Transfer(address(0), address(this), mintedAmount);
        emit Transfer(address(this), target, mintedAmount);
    }
    function freezeAccount(address target, bool freeze) onlyOwner public {
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }
}

```

## RQ1_b9441e3f411e

SHA-256 `4f0a01b7808752895a9c0057df85deab7aa8344229e1fd7b86ca53863cbe2e4f`

```solidity
pragma solidity 		^0.4.25		;	
contract		FORM_2019_01001		{						
	address	owner	;							
	function	NewForm		()	public	{				
		owner	= msg.sender;							
	}									
	modifier	onlyOwner	() {							
		require(msg.sender ==		owner	);					
		_;								
	}									
	string	inData_1	=	"e4ddBDcACBf2AB84eAf0AffeD2eD1E"						;
	function	setData_1	(	string	newData_1	)	public	onlyOwner	{	
		inData_1	=	newData_1	;					
	}									
	function	getData_1	()	public	constant	returns	(	string	)	{
		return	inData_1	;						
	}									
	string	inData_2	=	"356.34299069027500000000"						;
	function	setData_2	(	string	newData_2	)	public	onlyOwner	{	
		inData_2	=	newData_2	;					
	}									
	function	getData_2	()	public	constant	returns	(	string	)	{
		return	inData_2	;						
	}									
	string	inData_3	=	"10.000000000000000000"						;
	function	setData_3	(	string	newData_3	)	public	onlyOwner	{	
		inData_3	=	newData_3	;					
	}									
	function	getData_3	()	public	constant	returns	(	string	)	{
		return	inData_3	;						
	}									
	string	inData_4	=	"0x53da91ae3ffbcf997c1133d0d1b2"						;
	function	setData_4	(	string	newData_4	)	public	onlyOwner	{	
		inData_4	=	newData_4	;					
	}									
	function	getData_4	()	public	constant	returns	(	string	)	{
		return	inData_4	;						
	}									
	string	inData_5	=	"e260825e07cd22a87887850eedc5c9"						;
	function	setData_5	(	string	newData_5	)	public	onlyOwner	{	
		inData_5	=	newData_5	;					
	}									
	function	getData_5	()	public	constant	returns	(	string	)	{
		return	inData_5	;						
	}									
	string	inData_6	=	"3cF0F4401BaAeADdbD9ceaebb4CAaD"						;
	function	setData_6	(	string	newData_6	)	public	onlyOwner	{	
		inData_6	=	newData_6	;					
	}									
	function	getData_6	()	public	constant	returns	(	string	)	{
		return	inData_6	;						
	}									
	string	inData_7	=	"137.02805781747700000000"						;
	function	setData_7	(	string	newData_7	)	public	onlyOwner	{	
		inData_7	=	newData_7	;					
	}									
	function	getData_7	()	public	constant	returns	(	string	)	{
		return	inData_7	;						
	}									
	string	inData_8	=	"10.000000000000000000"						;
	function	setData_8	(	string	newData_8	)	public	onlyOwner	{	
		inData_8	=	newData_8	;					
	}									
	function	getData_8	()	public	constant	returns	(	string	)	{
		return	inData_8	;						
	}									
	string	inData_9	=	"0x53da91ae3ffbcf997c1133d0d1b2"						;
	function	setData_9	(	string	newData_9	)	public	onlyOwner	{	
		inData_9	=	newData_9	;					
	}									
	function	getData_9	()	public	constant	returns	(	string	)	{
		return	inData_9	;						
	}									
	string	inData_10	=	"e260825e07cd22a87887850eedc5c9"						;
	function	setData_10	(	string	newData_10	)	public	onlyOwner	{	
		inData_10	=	newData_10	;					
	}									
	function	getData_10	()	public	constant	returns	(	string	)	{
		return	inData_10	;						
	}									
	string	inData_11	=	"CF07A9f6Eb19891cdbB69Fcd7bF1aB"						;
	function	setData_11	(	string	newData_11	)	public	onlyOwner	{	
		inData_11	=	newData_11	;					
	}									
	function	getData_11	()	public	constant	returns	(	string	)	{
		return	inData_11	;						
	}									
	string	inData_12	=	"34.92521276174280000000"						;
	function	setData_12	(	string	newData_12	)	public	onlyOwner	{	
		inData_12	=	newData_12	;					
	}									
	function	getData_12	()	public	constant	returns	(	string	)	{
		return	inData_12	;						
	}									
	string	inData_13	=	"10.000000000000000000"						;
	function	setData_13	(	string	newData_13	)	public	onlyOwner	{	
		inData_13	=	newData_13	;					
	}									
	function	getData_13	()	public	constant	returns	(	string	)	{
		return	inData_13	;						
	}									
	string	inData_14	=	"0x53da91ae3ffbcf997c1133d0d1b2"						;
	function	setData_14	(	string	newData_14	)	public	onlyOwner	{	
		inData_14	=	newData_14	;					
	}									
	function	getData_14	()	public	constant	returns	(	string	)	{
		return	inData_14	;						
	}									
	string	inData_15	=	"e260825e07cd22a87887850eedc5c9"						;
	function	setData_15	(	string	newData_15	)	public	onlyOwner	{	
		inData_15	=	newData_15	;					
	}									
	function	getData_15	()	public	constant	returns	(	string	)	{
		return	inData_15	;						
	}									
	string	inData_16	=	"0xE38C52BB6Ecdc5CcfBcacf8efbCE"						;
	function	setData_16	(	string	newData_16	)	public	onlyOwner	{	
		inData_16	=	newData_16	;					
	}									
	function	getData_16	()	public	constant	returns	(	string	)	{
		return	inData_16	;						
	}									
	string	inData_17	=	"0.649727402479367"						;
	function	setData_17	(	string	newData_17	)	public	onlyOwner	{	
		inData_17	=	newData_17	;					
	}									
	function	getData_17	()	public	constant	returns	(	string	)	{
		return	inData_17	;						
	}									
	string	inData_18	=	"10.000000000000000000"						;
	function	setData_18	(	string	newData_18	)	public	onlyOwner	{	
		inData_18	=	newData_18	;					
	}									
	function	getData_18	()	public	constant	returns	(	string	)	{
		return	inData_18	;						
	}									
	string	inData_19	=	"0x53da91ae3ffbcf997c1133d0d1b2"						;
	function	setData_19	(	string	newData_19	)	public	onlyOwner	{	
		inData_19	=	newData_19	;					
	}									
	function	getData_19	()	public	constant	returns	(	string	)	{
		return	inData_19	;						
	}									
	string	inData_20	=	"e260825e07cd22a87887850eedc5c9"						;
	function	setData_20	(	string	newData_20	)	public	onlyOwner	{	
		inData_20	=	newData_20	;					
	}									
	function	getData_20	()	public	constant	returns	(	string	)	{
		return	inData_20	;						
	}									
	string	inData_21	=	"F1A4b85faC2c46Ca64DC58bE33d7E3"						;
	function	setData_21	(	string	newData_21	)	public	onlyOwner	{	
		inData_21	=	newData_21	;					
	}									
	function	getData_21	()	public	constant	returns	(	string	)	{
		return	inData_21	;						
	}									
	string	inData_22	=	"28.64382142967830000000"						;
	function	setData_22	(	string	newData_22	)	public	onlyOwner	{	
		inData_22	=	newData_22	;					
	}									
	function	getData_22	()	public	constant	returns	(	string	)	{
		return	inData_22	;						
	}									
	string	inData_23	=	"100.000000000000000000"						;
	function	setData_23	(	string	newData_23	)	public	onlyOwner	{	
		inData_23	=	newData_23	;					
	}									
	function	getData_23	()	public	constant	returns	(	string	)	{
		return	inData_23	;						
	}									
	string	inData_24	=	"0x2d0b1c47e02b21d068b783858d29"						;
	function	setData_24	(	string	newData_24	)	public	onlyOwner	{	
		inData_24	=	newData_24	;					
	}									
	function	getData_24	()	public	constant	returns	(	string	)	{
		return	inData_24	;						
	}									
	string	inData_25	=	"8c152436b26727d6268ee35f785cec"						;
	function	setData_25	(	string	newData_25	)	public	onlyOwner	{	
		inData_25	=	newData_25	;					
	}									
	function	getData_25	()	public	constant	returns	(	string	)	{
		return	inData_25	;						
	}									
	string	inData_26	=	"AdABCE55faC9BfEfCCD3B593dC76cA"						;
	function	setData_26	(	string	newData_26	)	public	onlyOwner	{	
		inData_26	=	newData_26	;					
	}									
	function	getData_26	()	public	constant	returns	(	string	)	{
		return	inData_26	;						
	}									
	string	inData_27	=	"8.46253364746049000000"						;
	function	setData_27	(	string	newData_27	)	public	onlyOwner	{	
		inData_27	=	newData_27	;					
	}									
	function	getData_27	()	public	constant	returns	(	string	)	{
		return	inData_27	;						
	}									
	string	inData_28	=	"100.000000000000000000"						;
	function	setData_28	(	string	newData_28	)	public	onlyOwner	{	
		inData_28	=	newData_28	;					
	}									
	function	getData_28	()	public	constant	returns	(	string	)	{
		return	inData_28	;						
	}									
	string	inData_29	=	"0x2d0b1c47e02b21d068b783858d29"						;
	function	setData_29	(	string	newData_29	)	public	onlyOwner	{	
		inData_29	=	newData_29	;					
	}									
	function	getData_29	()	public	constant	returns	(	string	)	{
		return	inData_29	;						
	}									
	string	inData_30	=	"8c152436b26727d6268ee35f785cec"						;
	function	setData_30	(	string	newData_30	)	public	onlyOwner	{	
		inData_30	=	newData_30	;					
	}									
	function	getData_30	()	public	constant	returns	(	string	)	{
		return	inData_30	;						
	}									
	string	inData_31	=	"2EbDdA77bC3ad8731F89F07EBAc7bD"						;
	function	setData_31	(	string	newData_31	)	public	onlyOwner	{	
		inData_31	=	newData_31	;					
	}									
	function	getData_31	()	public	constant	returns	(	string	)	{
		return	inData_31	;						
	}									
	string	inData_32	=	"1.95755087349616000000"						;
	function	setData_32	(	string	newData_32	)	public	onlyOwner	{	
		inData_32	=	newData_32	;					
	}									
	function	getData_32	()	public	constant	returns	(	string	)	{
		return	inData_32	;						
	}									
	string	inData_33	=	"100.000000000000000000"						;
	function	setData_33	(	string	newData_33	)	public	onlyOwner	{	
		inData_33	=	newData_33	;					
	}									
	function	getData_33	()	public	constant	returns	(	string	)	{
		return	inData_33	;						
	}									
	string	inData_34	=	"0x2d0b1c47e02b21d068b783858d29"						;
	function	setData_34	(	string	newData_34	)	public	onlyOwner	{	
		inData_34	=	newData_34	;					
	}									
	function	getData_34	()	public	constant	returns	(	string	)	{
		return	inData_34	;						
	}									
	string	inData_35	=	"8c152436b26727d6268ee35f785cec"						;
	function	setData_35	(	string	newData_35	)	public	onlyOwner	{	
		inData_35	=	newData_35	;					
	}									
	function	getData_35	()	public	constant	returns	(	string	)	{
		return	inData_35	;						
	}									
	string	inData_36	=	"0xa2baF1B14DFFeDdbD37E3bEDc45c"						;
	function	setData_36	(	string	newData_36	)	public	onlyOwner	{	
		inData_36	=	newData_36	;					
	}									
	function	getData_36	()	public	constant	returns	(	string	)	{
		return	inData_36	;						
	}									
	string	inData_37	=	"0.380368029746767"						;
	function	setData_37	(	string	newData_37	)	public	onlyOwner	{	
		inData_37	=	newData_37	;					
	}									
	function	getData_37	()	public	constant	returns	(	string	)	{
		return	inData_37	;						
	}									
	string	inData_38	=	"100.000000000000000000"						;
	function	setData_38	(	string	newData_38	)	public	onlyOwner	{	
		inData_38	=	newData_38	;					
	}									
	function	getData_38	()	public	constant	returns	(	string	)	{
		return	inData_38	;						
	}									
	string	inData_39	=	"0x2d0b1c47e02b21d068b783858d29"						;
	function	setData_39	(	string	newData_39	)	public	onlyOwner	{	
		inData_39	=	newData_39	;					
	}									
	function	getData_39	()	public	constant	returns	(	string	)	{
		return	inData_39	;						
	}									
	string	inData_40	=	"8c152436b26727d6268ee35f785cec"						;
	function	setData_40	(	string	newData_40	)	public	onlyOwner	{	
		inData_40	=	newData_40	;					
	}									
	function	getData_40	()	public	constant	returns	(	string	)	{
		return	inData_40	;						
	}									
}
```

## RQ1_ce214e96568d

SHA-256 `c12e4e8677a0b6166d2c97d234c3c5d1c556315809f0a3c948da8fcbe61790d5`

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
contract T0XToken is StandardToken {
  string public name = 'T0XToken';
  string public symbol = 'T0X';
  uint public decimals = 8;
  uint256 public createTime         = 1527436800;  
  uint256 public bonusEnds          = 1528646400;  
  uint256 public endDate            = 1529078400;  
  uint256 firstAnnual               = 1559318400;
  uint256 secondAnnual              = 1590940800;
  uint256 thirdAnnual               = 1622476800;
  uint256 public INITIAL_SUPPLY     = 1000000000;
  uint256 public frozenForever      =  400000000;
  uint256 firstAnnualReleasedAmount =  150000000;
  uint256 secondAnnualReleasedAmount=  150000000;
  uint256 thirdAnnualReleasedAmount =  100000000;
  function T0XToken() public {
    totalSupply = 200000000 ; 
    balances[msg.sender] = totalSupply * 10 ** uint256(decimals);
  }
  function releaseSupply() public onlyOwner returns(uint256 _actualRelease) {
    uint256 releaseAmount = getReleaseAmount();
    require(releaseAmount > 0);
    balances[owner] = addSafe(balances[owner], releaseAmount * 10 ** uint256(decimals));
    totalSupply = addSafe(totalSupply, releaseAmount);
    Transfer(address(0), msg.sender, releaseAmount);
    return releaseAmount;
  }
  function getReleaseAmount() internal returns(uint256 _actualRelease) {
        uint256 _amountToRelease;
        if (    now >= firstAnnual
             && now < secondAnnual
             && firstAnnualReleasedAmount > 0) {
            _amountToRelease = firstAnnualReleasedAmount;
            firstAnnualReleasedAmount = 0;
        } else if (    now >= secondAnnual 
                    && now < thirdAnnual
                    && secondAnnualReleasedAmount > 0) {
            _amountToRelease = secondAnnualReleasedAmount;
            secondAnnualReleasedAmount = 0;
        } else if (    now >= thirdAnnual 
                    && thirdAnnualReleasedAmount > 0) {
            _amountToRelease = thirdAnnualReleasedAmount;
            thirdAnnualReleasedAmount = 0;
        } else {
            _amountToRelease = 0;
        }
        return _amountToRelease;
    }
    function () public payable {
        require(now >= createTime && now <= endDate);
        uint tokens;
        if (now <= bonusEnds) {
            tokens = msg.value * 2480;
        } else {
            tokens = msg.value * 2000;
        }
        balances[msg.sender] = addSafe(balances[msg.sender], tokens);
        Transfer(address(0), msg.sender, tokens);
        owner.transfer(msg.value);
    }
}
```

## RQ1_2d78821d8d48

SHA-256 `16d7ec355a58fd9a7ec9bc9d2772f592a6e5bc56ede503ae3dc060c23134c139`

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
contract TOXToken is StandardToken {
  string public name = 'TOXToken';
  string public symbol = 'TOX';
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
  function TOXToken() public {
    totalSupply = 200000000 ; 
    balances[msg.sender] = totalSupply * 10 ** uint256(decimals);
  }
  function releaseSupply() public onlyOwner returns(uint256 _actualRelease) {
    uint256 releaseAmount = getReleaseAmount();
    require(releaseAmount > 0);
    balances[owner] = addSafe(balances[owner], releaseAmount * 10 ** uint256(decimals));
    totalSupply = addSafe(totalSupply, releaseAmount);
    Transfer(address(0), msg.sender, releaseAmount);
    return releaseAmount;
  }
  function getReleaseAmount() internal returns(uint256 _actualRelease) {
        uint256 _amountToRelease;
        if (    now >= firstAnnual
             && now < secondAnnual
             && firstAnnualReleasedAmount > 0) {
            _amountToRelease = firstAnnualReleasedAmount;
            firstAnnualReleasedAmount = 0;
        } else if (    now >= secondAnnual 
                    && now < thirdAnnual
                    && secondAnnualReleasedAmount > 0) {
            _amountToRelease = secondAnnualReleasedAmount;
            secondAnnualReleasedAmount = 0;
        } else if (    now >= thirdAnnual 
                    && thirdAnnualReleasedAmount > 0) {
            _amountToRelease = thirdAnnualReleasedAmount;
            thirdAnnualReleasedAmount = 0;
        } else {
            _amountToRelease = 0;
        }
        return _amountToRelease;
    }
}
```

## RQ1_08756bf2d11a

SHA-256 `e84034ce708b65dafee5eeb73a866aca858ab263417ce35b73a6aba4e958ca8a`

```solidity
contract ICreditBIT {
    function totalSupply() constant returns (uint256 supply) {}
    function mintMigrationTokens(address _reciever, uint _amount) returns (uint error) {}
    function getAccountData(address _owner) constant returns (uint avaliableBalance, uint lockedBalance, uint bondMultiplier, uint lockedUntilBlock, uint lastBlockClaimed) {}
}
contract ICreditIDENTITY {
    function getAddressDescription(address _queryAddress) constant returns (string){}
}
contract ICreditDAOfund {
    function withdrawReward(address _destination) {}
    function setCreditBondContract(address _creditBondAddress) {}
    function setCreditBitContract(address _creditBitAddress) {}
    function setFundsCreditDaoAddress(address _creditDaoAddress) {}
    function claimBondReward() {}
    function setCreditDaoAddress(address _creditDaoAddress) {}
    function lockTokens(uint _multiplier) {}
}
contract CreditDAO {
    struct Election {
        uint startBlock;
        uint endBlock;
        uint totalCrbSupply;
        bool electionsFinished;
        uint nextCandidateIndex;
        mapping(uint => address) candidateIndex;
        mapping(address => uint) candidateAddyToIndexMap;
        mapping(uint => uint) candidateVotes;
        mapping(address => bool) candidates;
        mapping(address => bool) userHasVoted;
        address maxVotes;
        uint numOfMaxVotes;
        uint idProcessed;
    }
    uint public nextElectionIndex;
    mapping(uint => Election) public elections;
    address public creditCEO;
    uint public mandateInBlocks = 927530;
    uint public blocksPerMonth = 76235;
    ICreditBIT creditBitContract = ICreditBIT(0xAef38fBFBF932D1AeF3B808Bc8fBd8Cd8E1f8BC5);
    ICreditDAOfund creditDAOFund;
    modifier onlyCEO {
        require(msg.sender == creditCEO);
        _;
    }
    function CreditDAO() {
        elections[nextElectionIndex].startBlock = block.number;
        elections[nextElectionIndex].endBlock = block.number + blocksPerMonth;
        elections[nextElectionIndex].totalCrbSupply = creditBitContract.totalSupply();
        nextElectionIndex++;
    }
    function createNewElections() {
        require(elections[nextElectionIndex - 1].endBlock + mandateInBlocks < block.number);
        elections[nextElectionIndex].startBlock = block.number;
        elections[nextElectionIndex].endBlock = block.number + blocksPerMonth;
        elections[nextElectionIndex].totalCrbSupply = creditBitContract.totalSupply();
        nextElectionIndex++;
        creditCEO = 0x0;
    }
    function sumbitForElection() {
        require(elections[nextElectionIndex - 1].endBlock > block.number);
        require(!elections[nextElectionIndex - 1].candidates[msg.sender]);
        uint nextCandidateId = elections[nextElectionIndex].nextCandidateIndex;
        elections[nextElectionIndex - 1].candidateIndex[nextCandidateId] = msg.sender;
        elections[nextElectionIndex - 1].candidateAddyToIndexMap[msg.sender] = nextCandidateId;
        elections[nextElectionIndex - 1].nextCandidateIndex++;
        elections[nextElectionIndex - 1].candidates[msg.sender] = true;
    }
    function vote(address _participant) {
        require(elections[nextElectionIndex - 1].endBlock > block.number);
        uint avaliableBalance;
        uint lockedBalance;
        uint bondMultiplier; 
        uint lockedUntilBlock; 
        uint lastBlockClaimed; 
        (avaliableBalance, lockedBalance, bondMultiplier, lockedUntilBlock, lastBlockClaimed) = creditBitContract.getAccountData(msg.sender);
        require(lockedUntilBlock >= elections[nextElectionIndex - 1].endBlock);
        require(!elections[nextElectionIndex - 1].userHasVoted[msg.sender]);
        uint candidateId = elections[nextElectionIndex - 1].candidateAddyToIndexMap[_participant];
        elections[nextElectionIndex - 1].candidateVotes[candidateId] += lockedBalance;
        elections[nextElectionIndex - 1].userHasVoted[msg.sender] = true;
    }
    function finishElections(uint _iterations) {
        require(elections[nextElectionIndex - 1].endBlock < block.number);
        require(!elections[nextElectionIndex - 1].electionsFinished);
        uint curentVotes;
        uint nextCandidateId = elections[nextElectionIndex - 1].idProcessed;
        for (uint cnt = 0; cnt < _iterations; cnt++) {
            curentVotes = elections[nextElectionIndex - 1].candidateVotes[nextCandidateId];
            if (curentVotes > elections[nextElectionIndex - 1].numOfMaxVotes) {
                elections[nextElectionIndex - 1].maxVotes = elections[nextElectionIndex - 1].candidateIndex[nextCandidateId];
                elections[nextElectionIndex - 1].numOfMaxVotes = curentVotes;
            }
            nextCandidateId++;
        }
        elections[nextElectionIndex - 1].idProcessed = nextCandidateId;
        if (elections[nextElectionIndex - 1].candidateIndex[nextCandidateId] == 0x0) {
            creditCEO = elections[nextElectionIndex - 1].maxVotes;
            elections[nextElectionIndex - 1].electionsFinished = true;
            if (elections[nextElectionIndex - 1].numOfMaxVotes == 0) {
                elections[nextElectionIndex].startBlock = block.number;
                elections[nextElectionIndex].endBlock = block.number + blocksPerMonth;
                elections[nextElectionIndex].totalCrbSupply = creditBitContract.totalSupply();
                nextElectionIndex++;
            }
        }
    }
    function claimBondReward() onlyCEO {
		creditDAOFund.claimBondReward();
	}
    function withdrawBondReward(address _addy) onlyCEO {
        creditDAOFund.withdrawReward(_addy);
    }
    function lockTokens(uint _multiplier) onlyCEO {
        creditDAOFund.lockTokens(_multiplier);
    }
    function setCreditBitContract(address _newCreditBitAddress) onlyCEO {
        creditBitContract = ICreditBIT(_newCreditBitAddress);
    }
    function setMandateInBlocks(uint _newMandateInBlocks) onlyCEO {
        mandateInBlocks = _newMandateInBlocks;
    }
    function setblocksPerMonth(uint _newblocksPerMonth) onlyCEO {
        blocksPerMonth = _newblocksPerMonth;
    }
    function setCreditDaoFund(address _newCreditDaoFundAddress) onlyCEO {
        creditDAOFund = ICreditDAOfund(_newCreditDaoFundAddress);
    }
    function setFundsCreditDaoAddress(address _creditDaoAddress) onlyCEO {
	    creditDAOFund.setCreditDaoAddress(_creditDaoAddress);
	}
	function setFundsCreditBitContract(address _creditBitAddress) onlyCEO {
        creditDAOFund.setCreditBitContract(_creditBitAddress);
	}
	function setFundsCreditBondContract(address _creditBondAddress) onlyCEO {
        creditDAOFund.setCreditBondContract(_creditBondAddress);
	}
    function getCreditFundAddress() constant returns (address) {
        return address(creditDAOFund);
    }
    function getCreditBitAddress() constant returns (address) {
        return address(creditBitContract);
    }
}
```

## RQ1_1831d050473c

SHA-256 `984fd962097abd12246cc9d24d5c8578585848794f3a7f4dd1075ff1fa647f8b`

```solidity
pragma solidity ^0.4.18;
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
contract ERC20 is ERC20Basic {
  function allowance(address owner, address spender) public constant returns (uint256);
  function transferFrom(address from, address to, uint256 value) public returns (bool);
  function approve(address spender, uint256 value) public returns (bool);
  event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract BasicToken is ERC20Basic, Ownable {
  using SafeMath for uint256;
  mapping(address => uint256) balances;
  mapping(address => bool) locks;
  function transfer(address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(!locks[msg.sender] && !locks[_to]);
    balances[msg.sender] = balances[msg.sender].sub(_value);
    balances[_to] = balances[_to].add(_value);
    Transfer(msg.sender, _to, _value);
    return true;
  }
  function balanceOf(address _owner) public constant returns (uint256 balance) {
    return balances[_owner];
  }
  function setLock(address _toLock, bool _setTo) onlyOwner {
      locks[_toLock] = _setTo;
  }
  function lockOf(address _owner) public constant returns (bool lock) {
    return locks[_owner];
  }
}
contract StandardToken is ERC20, BasicToken {
  mapping (address => mapping (address => uint256)) internal allowed;
  function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(!locks[_from] && !locks[_to]);
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
contract MintableToken is StandardToken {
  string public constant name = "CryptoTask";
  string public constant symbol = "CTF";
  uint8 public constant decimals = 18; 
  event Mint(address indexed to, uint256 amount);
  event MintFinished();
  bool public mintingFinished = false;
  modifier canMint() {
    require(!mintingFinished);
    _;
  }
  function mint(address _to, uint256 _amount) onlyOwner canMint public returns (bool) {
    require(!locks[_to]);
    totalSupply = totalSupply.add(_amount);
    balances[_to] = balances[_to].add(_amount);
    Mint(_to, _amount);
    Transfer(0x0, _to, _amount);
    return true;
  }
  function finishMinting() onlyOwner public returns (bool) {
    mintingFinished = true;
    MintFinished();
    return true;
  }
}
contract Crowdsale is Ownable {
    using SafeMath for uint;
    uint public fundingGoal = 1000 * 1 ether;
    uint public hardCap;
    uint public amountRaisedPreSale = 0;
    uint public amountRaisedICO = 0;
    uint public contractDeployedTime;
    uint presaleDuration = 30 * 1 days;
    uint countdownDuration = 45 * 1 days;
    uint icoDuration = 20 * 1 days;
    uint public presaleEndTime;
    uint public deadline;
    uint public price = 1000;
    MintableToken public token;
    mapping(address => uint) public balanceOf;
    bool public icoSuccess = false;
    bool public crowdsaleClosed = false;
    address vault1;
    address vault2 = 0xC0776D495f9Ed916C87c8C48f34f08E2B9506342;
    uint public stage = 0;
    uint public against = 0;
    uint public lastVoteTime;
    uint minVoteTime = 180 * 1 days;
    event GoalReached(uint amountRaised);
    event FundTransfer(address backer, uint amount, bool isContribution);
    function Crowdsale() {
        contractDeployedTime = now;
        vault1 = msg.sender;
        token = new MintableToken();
    }
    function () payable {
        require(!token.lockOf(msg.sender) && !crowdsaleClosed && stage<2 && msg.value >= 1 * (1 ether)/10);
        if(stage==1 && (now < presaleEndTime.add(countdownDuration) || amountRaisedPreSale+amountRaisedICO+msg.value > hardCap)) {
            throw;
        }
        uint amount = msg.value;
        balanceOf[msg.sender] += amount;
        if(stage==0) {  
            amountRaisedPreSale += amount;
            token.mint(msg.sender, amount.mul(2) * price);
        } else {
            amountRaisedICO += amount;
            token.mint(msg.sender, amount * price);
        }
        FundTransfer(msg.sender, amount, true);
    }
    function forward(uint amount) internal {
        vault1.transfer(amount.mul(67)/100);
        vault2.transfer(amount.sub(amount.mul(67)/100));
    }
    modifier afterDeadline() { if (stage > 0 && now >= deadline) {_;} }
    function checkGoalReached() afterDeadline {
        require(stage==1 && !crowdsaleClosed);
        if (amountRaisedPreSale+amountRaisedICO >= fundingGoal) {
            uint amount = amountRaisedICO/3;
            if(!icoSuccess) {
                amount += amountRaisedPreSale/3;    
            }
            uint amountToken1 = token.totalSupply().mul(67)/(100*4);
            uint amountToken2 = token.totalSupply().mul(33)/(100*4);
            forward(amount);
            icoSuccess = true;
            token.mint(vault1, amountToken1);    
            token.mint(vault2, amountToken2);    
            stage=2;
            lastVoteTime = now;
            GoalReached(amountRaisedPreSale+amountRaisedICO);
        }
        crowdsaleClosed = true;
        token.finishMinting();
    }
    function closePresale() {
        require((msg.sender == owner || now.sub(contractDeployedTime) > presaleDuration) && stage==0);
        stage = 1;
        presaleEndTime = now;
        deadline = now.add(icoDuration.add(countdownDuration));
        if(amountRaisedPreSale.mul(5) > 10000 * 1 ether) {
            hardCap = amountRaisedPreSale.mul(5);
        } else {
            hardCap = 10000 * 1 ether;
        }
        if(amountRaisedPreSale >= fundingGoal) {
            uint amount = amountRaisedPreSale/3;
            forward(amount);
            icoSuccess = true;
            GoalReached(amountRaisedPreSale);
        }
    }
    function safeWithdrawal() {
        require(crowdsaleClosed && !icoSuccess);
        uint amount;
        if(stage==1) {
            amount = balanceOf[msg.sender];
        } else if(stage==2) {
            amount = balanceOf[msg.sender].mul(2)/3;    
        } else if(stage==3) {
            amount = balanceOf[msg.sender]/3;    
        }
        balanceOf[msg.sender] = 0;
        if (amount > 0) {
            msg.sender.transfer(amount);
            FundTransfer(msg.sender, amount, false);
        }
    }
    function voteAgainst()
    {
        require((stage==2 || stage==3) && !token.lockOf(msg.sender));   
        token.setLock(msg.sender, true);
        uint voteWeight = token.balanceOf(msg.sender);
        against = against.add(voteWeight);
    }
    function voteRelease()
    {
        require((stage==2 || stage==3 || stage==4) && token.lockOf(msg.sender));
        token.setLock(msg.sender, false);
        uint voteWeight = token.balanceOf(msg.sender);
        against = against.sub(voteWeight);
    }
    function countVotes()
    {
        require(icoSuccess && (stage==2 || stage==3) && now.sub(lastVoteTime) > minVoteTime);
        lastVoteTime = now;
        if(against > token.totalSupply()/2) {
            icoSuccess = false;
        } else {
            uint amount = amountRaisedICO/3 + amountRaisedPreSale/3;
            forward(amount);
            stage++;
        }
    }
}
```

## RQ1_053265dda42e

SHA-256 `fd0090415eb98ee048de2fee8083d61743a02237e32ce21967fd34573aa416cf`

```solidity
pragma solidity ^0.4.24;
contract Matthew {
    address owner;
    address whale;
    uint256 blockheight;
    uint256 period = 18; 
    uint constant DELTA = 0.1 ether;
    uint constant WINNERTAX_PRECENT = 10;
    bool mustBeDestroyed = false;
    uint newPeriod = 5;
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
        period;
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

## RQ1_96bf57edc37b

SHA-256 `af80be31f9fc264d6e633841ad30a048475a36a6dfc06f8033bfd7bc87815728`

```solidity
pragma solidity ^0.4.15;
contract BTCRelay {
    function getLastBlockHeight() public returns (int);
    function getBlockchainHead() public returns (int);
    function getFeeAmount(int blockHash) public returns (int);
    function getBlockHeader(int blockHash) public returns (bytes32[5]);
    function storeBlockHeader(bytes blockHeader) public returns (int);
}
contract Escrow {
    function deposit(address recipient) payable;
}
contract AffiliateNetwork {
    function affiliateAddresses(uint code) returns (address);
}
contract EthereumLottery {
    uint constant GAS_LIMIT_DEPOSIT = 300000;
    uint constant GAS_LIMIT_AFFILIATE = 35000;
    struct Lottery {
        uint jackpot;
        int decidingBlock;
        uint numTickets;
        uint numTicketsSold;
        uint ticketPrice;
        uint affiliateCut;
        int winningTicket;
        address winner;
        uint finalizationBlock;
        address finalizer;
        string message;
        mapping (uint => address) tickets;
        int nearestKnownBlock;
        int nearestKnownBlockHash;
    }
    address public owner;
    address public admin;
    address public proposedOwner;
    int public id = -1;
    uint public lastInitTimestamp;
    uint public lastSaleTimestamp;
    uint public recentActivityIdx;
    uint[1000] public recentActivity;
    mapping (int => Lottery) public lotteries;
    address public btcRelay;
    address public escrow;
    address public affiliateNetwork;
    enum Reason { TicketSaleClosed, TicketAlreadySold }
    event PurchaseFailed(address indexed buyer, uint mark, Reason reason);
    event PurchaseSuccessful(address indexed buyer, uint mark);
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    modifier onlyAdminOrOwner {
        require(msg.sender == owner || msg.sender == admin);
        _;
    }
    modifier afterInitialization {
        require(id >= 0);
        _;
    }
    function EthereumLottery(address _btcRelay,
                             address _escrow,
                             address _affiliateNetwork) {
        owner = msg.sender;
        admin = msg.sender;
        btcRelay = _btcRelay;
        escrow = _escrow;
        affiliateNetwork = _affiliateNetwork;
    }
    function needsInitialization() constant returns (bool) {
        return id == -1 || lotteries[id].finalizationBlock > 0;
    }
    function initLottery(uint _jackpot, uint _numTickets, uint _ticketPrice)
             onlyAdminOrOwner {
        require(needsInitialization());
        require(_numTickets * _ticketPrice > _jackpot);
        id += 1;
        lotteries[id].jackpot = _jackpot;
        lotteries[id].decidingBlock = -1;
        lotteries[id].numTickets = _numTickets;
        lotteries[id].ticketPrice = _ticketPrice;
        lotteries[id].winningTicket = -1;
        uint affiliateCut = (_ticketPrice - (_jackpot / _numTickets)) / 2;
        lotteries[id].affiliateCut = affiliateCut;
        lastInitTimestamp = block.timestamp;
        lastSaleTimestamp = 0;
    }
    function buyTickets(uint[] _tickets, uint _mark, uint _affiliate)
             payable afterInitialization {
        if (lotteries[id].numTicketsSold == lotteries[id].numTickets) {
            PurchaseFailed(msg.sender, _mark, Reason.TicketSaleClosed);
            msg.sender.transfer(msg.value);
            return;
        }
        require(_tickets.length > 0);
        require(msg.value == _tickets.length * lotteries[id].ticketPrice);
        for (uint i = 0; i < _tickets.length; i++) {
            uint ticket = _tickets[i];
            require(ticket >= 0);
            require(ticket < lotteries[id].numTickets);
            if (lotteries[id].tickets[ticket] != 0) {
                PurchaseFailed(msg.sender, _mark, Reason.TicketAlreadySold);
                msg.sender.transfer(msg.value);
                return;
            }
        }
        for (i = 0; i < _tickets.length; i++) {
            ticket = _tickets[i];
            lotteries[id].tickets[ticket] = msg.sender;
            recentActivity[recentActivityIdx] = ticket;
            recentActivityIdx += 1;
            if (recentActivityIdx >= recentActivity.length) {
                recentActivityIdx = 0;
            }
        }
        lotteries[id].numTicketsSold += _tickets.length;
        lastSaleTimestamp = block.timestamp;
        address affiliateAddress =
            AffiliateNetwork(affiliateNetwork).affiliateAddresses(_affiliate);
        if (affiliateAddress != 0) {
            uint cut = lotteries[id].affiliateCut * _tickets.length;
            var _ = affiliateAddress.call.gas(GAS_LIMIT_AFFILIATE).value(cut)();
        }
        PurchaseSuccessful(msg.sender, _mark);
    }
    function needsBlockFinalization()
             afterInitialization constant returns (bool) {
        uint btcTimestamp;
        int blockHash = BTCRelay(btcRelay).getBlockchainHead();
        (,btcTimestamp) = getBlockHeader(blockHash);
        uint delta = 0;
        if (btcTimestamp < block.timestamp) {
            delta = block.timestamp - btcTimestamp;
        }
        return delta < 2 * 60 * 60 &&
               lotteries[id].numTicketsSold == lotteries[id].numTickets &&
               lotteries[id].decidingBlock == -1;
    }
    function finalizeBlock()
             afterInitialization {
        require(needsBlockFinalization());
        int blockHeight = BTCRelay(btcRelay).getLastBlockHeight();
        lotteries[id].decidingBlock = blockHeight + 54;
    }
    function needsLotteryFinalization()
             afterInitialization constant returns (bool) {
        int blockHeight = BTCRelay(btcRelay).getLastBlockHeight();
        return lotteries[id].decidingBlock != -1 &&
               blockHeight >= lotteries[id].decidingBlock + 6 &&
               lotteries[id].finalizationBlock == 0;
    }
    function finalizeLottery(uint _steps)
             afterInitialization {
        require(needsLotteryFinalization());
        if (lotteries[id].nearestKnownBlock != lotteries[id].decidingBlock) {
            walkTowardsBlock(_steps);
        } else {
            int winningTicket = lotteries[id].nearestKnownBlockHash %
                                int(lotteries[id].numTickets);
            address winner = lotteries[id].tickets[uint(winningTicket)];
            lotteries[id].winningTicket = winningTicket;
            lotteries[id].winner = winner;
            lotteries[id].finalizationBlock = block.number;
            lotteries[id].finalizer = tx.origin;
            if (winner != 0) {
                uint value = lotteries[id].jackpot;
                bool successful =
                    winner.call.gas(GAS_LIMIT_DEPOSIT).value(value)();
                if (!successful) {
                    Escrow(escrow).deposit.value(value)(winner);
                }
            }
            var _ = admin.call.gas(GAS_LIMIT_DEPOSIT).value(this.balance)();
        }
    }
    function walkTowardsBlock(uint _steps) internal {
        int blockHeight;
        int blockHash;
        if (lotteries[id].nearestKnownBlock == 0) {
            blockHeight = BTCRelay(btcRelay).getLastBlockHeight();
            blockHash = BTCRelay(btcRelay).getBlockchainHead();
        } else {
            blockHeight = lotteries[id].nearestKnownBlock;
            blockHash = lotteries[id].nearestKnownBlockHash;
        }
        for (uint step = 0; step < _steps; step++) {
            blockHeight -= 1;
            (blockHash,) = getBlockHeader(blockHash);
            if (blockHeight == lotteries[id].decidingBlock) { break; }
        }
        lotteries[id].nearestKnownBlock = blockHeight;
        lotteries[id].nearestKnownBlockHash = blockHash;
    }
    function getBlockHeader(int blockHash)
             internal returns (int prevBlockHash, uint timestamp) {
        int fee = BTCRelay(btcRelay).getFeeAmount(blockHash);
        require(fee == 0);
        bytes32[5] memory blockHeader =
            BTCRelay(btcRelay).getBlockHeader(blockHash);
        prevBlockHash = 0;
        for (uint i = 0; i < 32; i++) {
            uint pos = 68 + i;  
            byte data = blockHeader[pos / 32][pos % 32];
            prevBlockHash = prevBlockHash | int(data) * int(0x100 ** i);
        }
        timestamp = 0;
        for (i = 0; i < 4; i++) {
            pos = 132 + i;  
            data = blockHeader[pos / 32][pos % 32];
            timestamp = timestamp | uint(data) * uint(0x100 ** i);
        }
        return (prevBlockHash, timestamp);
    }
    function getMessageLength(string _message) constant returns (uint) {
        return bytes(_message).length;
    }
    function setMessage(int _id, string _message)
             afterInitialization {
        require(lotteries[_id].winner != 0);
        require(lotteries[_id].winner == msg.sender);
        require(getMessageLength(_message) <= 500);
        lotteries[_id].message = _message;
    }
    function getLotteryDetailsA(int _id)
             constant returns (int _actualId, uint _jackpot,
                               int _decidingBlock,
                               uint _numTickets, uint _numTicketsSold,
                               uint _lastSaleTimestamp, uint _ticketPrice) {
        if (_id == -1) {
            _actualId = id;
        } else {
            _actualId = _id;
        }
        _jackpot = lotteries[_actualId].jackpot;
        _decidingBlock = lotteries[_actualId].decidingBlock;
        _numTickets = lotteries[_actualId].numTickets;
        _numTicketsSold = lotteries[_actualId].numTicketsSold;
        _lastSaleTimestamp = lastSaleTimestamp;
        _ticketPrice = lotteries[_actualId].ticketPrice;
    }
    function getLotteryDetailsB(int _id)
             constant returns (int _actualId,
                               int _winningTicket, address _winner,
                               uint _finalizationBlock, address _finalizer,
                               string _message,
                               int _prevLottery, int _nextLottery,
                               int _blockHeight) {
        if (_id == -1) {
            _actualId = id;
        } else {
            _actualId = _id;
        }
        _winningTicket = lotteries[_actualId].winningTicket;
        _winner = lotteries[_actualId].winner;
        _finalizationBlock = lotteries[_actualId].finalizationBlock;
        _finalizer = lotteries[_actualId].finalizer;
        _message = lotteries[_actualId].message;
        if (_actualId == 0) {
            _prevLottery = -1;
        } else {
            _prevLottery = _actualId - 1;
        }
        if (_actualId == id) {
            _nextLottery = -1;
        } else {
            _nextLottery = _actualId + 1;
        }
        _blockHeight = BTCRelay(btcRelay).getLastBlockHeight();
    }
    function getTicketDetails(int _id, uint _offset, uint _n, address _addr)
             constant returns (uint8[] details) {
        require(_offset + _n <= lotteries[_id].numTickets);
        details = new uint8[](_n);
        for (uint i = 0; i < _n; i++) {
            address addr = lotteries[_id].tickets[_offset + i];
            if (addr == _addr && _addr != 0) {
                details[i] = 2;
            } else if (addr != 0) {
                details[i] = 1;
            } else {
                details[i] = 0;
            }
        }
    }
    function getFullTicketDetails(int _id, uint _offset, uint _n)
             constant returns (address[] details) {
        require(_offset + _n <= lotteries[_id].numTickets);
        details = new address[](_n);
        for (uint i = 0; i < _n; i++) {
            details[i] = lotteries[_id].tickets[_offset + i];
        }
    }
    function getTicketOwner(int _id, uint _ticket) constant returns (address) {
        require(_id >= 0);
        return lotteries[_id].tickets[_ticket];
    }
    function getRecentActivity()
             constant returns (int _id, uint _idx, uint[1000] _recentActivity) {
        _id = id;
        _idx = recentActivityIdx;
        for (uint i = 0; i < recentActivity.length; i++) {
            _recentActivity[i] = recentActivity[i];
        }
    }
    function setAdmin(address _admin) onlyOwner {
        admin = _admin;
    }
    function proposeOwner(address _owner) onlyOwner {
        proposedOwner = _owner;
    }
    function acceptOwnership() {
        require(proposedOwner != 0);
        require(msg.sender == proposedOwner);
        owner = proposedOwner;
    }
}
```

## RQ1_4325a2042776

SHA-256 `bf1d847a5e12cfaa4e56300af90f9300da2b6b4983292ce5b6b69ff3daaf560c`

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
contract Ethtex is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "Ethtex";
    string public constant symbol = "EXT";
    uint public constant decimals = 8;
    uint256 public totalSupply = 150000000000e8;
    uint256 public totalDistributed = 0;    
    uint256 public constant MIN_CONTRIBUTION = 1 ether / 50; 
    uint256 public tokensPerEth = 1000000000e8;
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
    function SaveCryptoNetwork () public {
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

## RQ1_c6ae1b699b0e

SHA-256 `1ac1b93175f1dd5a393ca9ef66fda90093c56c965cd2c4a7894439c3d8e4ae18`

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
    string public constant symbol = "VPCx";
    uint public constant decimals = 3;
uint256 public totalSupply = 66000000e3;
uint256 public totalDistributed = 45000000e3;
uint256 public totalRemaining = totalSupply.sub(totalDistributed);
uint256 public value = 150e3;
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
    function VPCx() public {
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
    function withdrawVPCxTokens(address _tokenContract) onlyOwner public returns (bool) {
        VotePumpCoin0xToken token = VotePumpCoin0xToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_fdc16844f97b

SHA-256 `2c131b2e4427a7e3019c4ab065e554002332b688e9c520c2eba52dc514ca6ce3`

```solidity
pragma solidity ^0.4.24;
contract EtherRock {
    struct Rock {
        address owner;
        bool currentlyForSale;
        uint price;
        uint timesSold;
    }
    mapping (uint => Rock) public rocks;
    mapping (address => uint[]) public rockOwners;
    uint public latestNewRockForSale;
    address owner;
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    function EtherRock() {
        latestNewRockForSale = 11;
        rocks[0].owner = 0x789c778b340f17eb046a5a8633e362468aceeff6;
        rocks[0].currentlyForSale = true;
        rocks[0].price = 10000000000000000000;
        rocks[0].timesSold = 2;
        rockOwners[0x789c778b340f17eb046a5a8633e362468aceeff6].push(0);
        rocks[1].owner = 0x9a643a42748243f80243a65666146a2e1bd5c6aa;
        rocks[1].currentlyForSale = false;
        rocks[1].price = 2000000000000000;
        rocks[1].timesSold = 3;
        rockOwners[0x9a643a42748243f80243a65666146a2e1bd5c6aa].push(1);
        rocks[2].owner = 0x5d5d6543d73066e69424ce2756cc34cbfe4c368c;
        rocks[2].currentlyForSale = false;
        rocks[2].price = 5000000000000000;
        rocks[2].timesSold = 1;
        rockOwners[0x5d5d6543d73066e69424ce2756cc34cbfe4c368c].push(2);
        rocks[3].owner = 0xe34501580dc9591211afc7c13f16ddf591c87cde;
        rocks[3].currentlyForSale = true;
        rocks[3].price = 1000000000000000000;
        rocks[3].timesSold = 1;
        rockOwners[0xe34501580dc9591211afc7c13f16ddf591c87cde].push(3);
        rocks[4].owner = 0x93cdb0a93fc36f6a53ed21ecf6305ab80d06beca;
        rocks[4].currentlyForSale = true;
        rocks[4].price = 1000000000000000000;
        rocks[4].timesSold = 1;
        rockOwners[0x93cdb0a93fc36f6a53ed21ecf6305ab80d06beca].push(4);
        rocks[5].owner = 0x9467d05ee1c90010a657e244f626194168596583;
        rocks[5].currentlyForSale = true;
        rocks[5].price = 42000000000000000000;
        rocks[5].timesSold = 1;
        rockOwners[0x9467d05ee1c90010a657e244f626194168596583].push(5);
        rocks[6].owner = 0xb6e2e5e06397dc522db58faa064f74c95322b58e;
        rocks[6].currentlyForSale = true;
        rocks[6].price = 60000000000000000;
        rocks[6].timesSold = 1;
        rockOwners[0xb6e2e5e06397dc522db58faa064f74c95322b58e].push(6);
        rocks[7].owner = 0xbcddcf35880443b6a1f32f07009097e95c327716;
        rocks[7].currentlyForSale = true;
        rocks[7].price = 100000000000000000;
        rocks[7].timesSold = 1;
        rockOwners[0xbcddcf35880443b6a1f32f07009097e95c327716].push(7);
        rocks[8].owner = 0xf7007f39a41d87c669bd9beadc3d5cc2ef5a32be;
        rocks[8].currentlyForSale = false;
        rocks[8].price = 65000000000000000;
        rocks[8].timesSold = 1;
        rockOwners[0xf7007f39a41d87c669bd9beadc3d5cc2ef5a32be].push(8);
        rocks[9].owner = 0xf7007f39a41d87c669bd9beadc3d5cc2ef5a32be;
        rocks[9].currentlyForSale = true;
        rocks[9].price = 10000000000000000000;
        rocks[9].timesSold = 1;
        rockOwners[0xf7007f39a41d87c669bd9beadc3d5cc2ef5a32be].push(9);
        rocks[10].owner = 0xd17e2bfe196470a9fefb567e8f5992214eb42f24;
        rocks[10].currentlyForSale = true;
        rocks[10].price = 200000000000000000;
        rocks[10].timesSold = 1;
        rockOwners[0xd17e2bfe196470a9fefb567e8f5992214eb42f24].push(10);
        rocks[11].currentlyForSale = true;
        rocks[11].price = 122000000000000000;
        owner = msg.sender;
    }
    function getRockInfo (uint rockNumber) returns (address, bool, uint, uint) {
        return (rocks[rockNumber].owner, rocks[rockNumber].currentlyForSale, rocks[rockNumber].price, rocks[rockNumber].timesSold);
    }
    function rockOwningHistory (address _address) returns (uint[]) {
        return rockOwners[_address];
    }
    function buyRock (uint rockNumber) payable {
        require(rocks[rockNumber].currentlyForSale == true);
        require(msg.value == rocks[rockNumber].price);
        rocks[rockNumber].currentlyForSale = false;
        rocks[rockNumber].timesSold++;
        if (rockNumber != latestNewRockForSale) {
            rocks[rockNumber].owner.transfer(rocks[rockNumber].price);
        }
        rocks[rockNumber].owner = msg.sender;
        rockOwners[msg.sender].push(rockNumber);
        if (rockNumber == latestNewRockForSale) {
            if (rockNumber != 99) {
                latestNewRockForSale++;
                rocks[latestNewRockForSale].price = 10**15 + (latestNewRockForSale**2 * 10**15);
                rocks[latestNewRockForSale].currentlyForSale = true;
            }
        }
    }
    function sellRock (uint rockNumber, uint price) {
        require(msg.sender == rocks[rockNumber].owner);
        require(price > 0);
        rocks[rockNumber].price = price;
        rocks[rockNumber].currentlyForSale = true;
    }
    function dontSellRock (uint rockNumber) {
        require(msg.sender == rocks[rockNumber].owner);
        rocks[rockNumber].currentlyForSale = false;
    }
    function giftRock (uint rockNumber, address receiver) {
        require(msg.sender == rocks[rockNumber].owner);
        rocks[rockNumber].owner = receiver;
        rockOwners[receiver].push(rockNumber);
    }
    function() payable {
    }
    function withdraw() onlyOwner {
        owner.transfer(this.balance);
    }
}

```

## RQ1_7e1479cae0bc

SHA-256 `cd16b4f437fe97cdfe206a806573b1bf8bac7f9ff7f9dc2eac07f8a89afb7f93`

```solidity
pragma solidity ^0.4.19;
contract BitDegreeToken {
    string public name = "BitDegree";
    string public symbol = "BDG";
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
    function BitDegreeToken() public {
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
