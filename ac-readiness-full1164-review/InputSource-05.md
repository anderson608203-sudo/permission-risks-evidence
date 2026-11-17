# 本批实际输入源码

按输入原字节 SHA 核对。源码位置采用 UTF-8 字节偏移。

## RQ1_e5f934bea8ec

SHA-256 `8ba0470d1b92056a6fa53ceb3360fe778f69a39570c3e3e3deb856ea39feb2d3`

```solidity
pragma solidity ^0.4.24;
interface IArbitrable {
    event MetaEvidence(uint indexed _metaEvidenceID, string _evidence);
    event Dispute(Arbitrator indexed _arbitrator, uint indexed _disputeID, uint _metaEvidenceID, uint _evidenceGroupID);
    event Evidence(Arbitrator indexed _arbitrator, uint indexed _evidenceGroupID, address indexed _party, string _evidence);
    event Ruling(Arbitrator indexed _arbitrator, uint indexed _disputeID, uint _ruling);
    function rule(uint _disputeID, uint _ruling) external;
}
contract Arbitrable is IArbitrable {
    Arbitrator public arbitrator;
    bytes public arbitratorExtraData;
    modifier onlyArbitrator {require(msg.sender == address(arbitrator), "Can only be called by the arbitrator."); _;}
    constructor(Arbitrator _arbitrator, bytes memory _arbitratorExtraData) public {
        arbitrator = _arbitrator;
        arbitratorExtraData = _arbitratorExtraData;
    }
    function rule(uint _disputeID, uint _ruling) public onlyArbitrator {
        emit Ruling(Arbitrator(msg.sender),_disputeID,_ruling);
        executeRuling(_disputeID,_ruling);
    }
    function executeRuling(uint _disputeID, uint _ruling) internal;
}
contract Arbitrator {
    enum DisputeStatus {Waiting, Appealable, Solved}
    modifier requireArbitrationFee(bytes memory _extraData) {
        require(msg.value >= arbitrationCost(_extraData), "Not enough ETH to cover arbitration costs.");
        _;
    }
    modifier requireAppealFee(uint _disputeID, bytes memory _extraData) {
        require(msg.value >= appealCost(_disputeID, _extraData), "Not enough ETH to cover appeal costs.");
        _;
    }
    event DisputeCreation(uint indexed _disputeID, Arbitrable indexed _arbitrable);
    event AppealPossible(uint indexed _disputeID, Arbitrable indexed _arbitrable);
    event AppealDecision(uint indexed _disputeID, Arbitrable indexed _arbitrable);
    function createDispute(uint _choices, bytes memory _extraData) public requireArbitrationFee(_extraData) payable returns(uint disputeID) {}
    function arbitrationCost(bytes memory _extraData) public view returns(uint fee);
    function appeal(uint _disputeID, bytes memory _extraData) public requireAppealFee(_disputeID,_extraData) payable {
        emit AppealDecision(_disputeID, Arbitrable(msg.sender));
    }
    function appealCost(uint _disputeID, bytes memory _extraData) public view returns(uint fee);
    function appealPeriod(uint _disputeID) public view returns(uint start, uint end) {}
    function disputeStatus(uint _disputeID) public view returns(DisputeStatus status);
    function currentRuling(uint _disputeID) public view returns(uint ruling);
}
contract CentralizedArbitrator is Arbitrator {
    address public owner = msg.sender;
    uint arbitrationPrice; 
    uint constant NOT_PAYABLE_VALUE = (2**256-2)/2; 
    struct DisputeStruct {
        Arbitrable arbitrated;
        uint choices;
        uint fee;
        uint ruling;
        DisputeStatus status;
    }
    modifier onlyOwner {require(msg.sender==owner, "Can only be called by the owner."); _;}
    DisputeStruct[] public disputes;
    constructor(uint _arbitrationPrice) public {
        arbitrationPrice = _arbitrationPrice;
    }
    function setArbitrationPrice(uint _arbitrationPrice) public onlyOwner {
        arbitrationPrice = _arbitrationPrice;
    }
    function arbitrationCost(bytes _extraData) public view returns(uint fee) {
        return arbitrationPrice;
    }
    function appealCost(uint _disputeID, bytes _extraData) public view returns(uint fee) {
        return NOT_PAYABLE_VALUE;
    }
    function createDispute(uint _choices, bytes _extraData) public payable returns(uint disputeID)  {
        super.createDispute(_choices, _extraData);
        disputeID = disputes.push(DisputeStruct({
            arbitrated: Arbitrable(msg.sender),
            choices: _choices,
            fee: msg.value,
            ruling: 0,
            status: DisputeStatus.Waiting
            })) - 1; 
        emit DisputeCreation(disputeID, Arbitrable(msg.sender));
    }
    function _giveRuling(uint _disputeID, uint _ruling) internal {
        DisputeStruct storage dispute = disputes[_disputeID];
        require(_ruling <= dispute.choices, "Invalid ruling.");
        require(dispute.status != DisputeStatus.Solved, "The dispute must not be solved already.");
        dispute.ruling = _ruling;
        dispute.status = DisputeStatus.Solved;
        msg.sender.send(dispute.fee); 
        dispute.arbitrated.rule(_disputeID,_ruling);
    }
    function giveRuling(uint _disputeID, uint _ruling) public onlyOwner {
        return _giveRuling(_disputeID, _ruling);
    }
    function disputeStatus(uint _disputeID) public view returns(DisputeStatus status) {
        return disputes[_disputeID].status;
    }
    function currentRuling(uint _disputeID) public view returns(uint ruling) {
        return disputes[_disputeID].ruling;
    }
}
contract AppealableArbitrator is CentralizedArbitrator, Arbitrable {
    struct AppealDispute {
        uint rulingTime;
        Arbitrator arbitrator;
        uint appealDisputeID;
    }
    uint public timeOut;
    mapping(uint => AppealDispute) public appealDisputes;
    mapping(uint => uint) public appealDisputeIDsToDisputeIDs;
    constructor(
        uint _arbitrationPrice,
        Arbitrator _arbitrator,
        bytes _arbitratorExtraData,
        uint _timeOut
    ) public CentralizedArbitrator(_arbitrationPrice) Arbitrable(_arbitrator, _arbitratorExtraData) {
        timeOut = _timeOut;
    }
    function changeArbitrator(Arbitrator _arbitrator) external onlyOwner {
        arbitrator = _arbitrator;
    }
    function changeTimeOut(uint _timeOut) external onlyOwner {
        timeOut = _timeOut;
    }
    function getAppealDisputeID(uint _disputeID) external view returns(uint disputeID) {
        if (appealDisputes[_disputeID].arbitrator != Arbitrator(address(0)))
            disputeID = AppealableArbitrator(appealDisputes[_disputeID].arbitrator).getAppealDisputeID(appealDisputes[_disputeID].appealDisputeID);
        else disputeID = _disputeID;
    }
    function appeal(uint _disputeID, bytes _extraData) public payable requireAppealFee(_disputeID, _extraData) {
        super.appeal(_disputeID, _extraData);
        if (appealDisputes[_disputeID].arbitrator != Arbitrator(address(0)))
            appealDisputes[_disputeID].arbitrator.appeal.value(msg.value)(appealDisputes[_disputeID].appealDisputeID, _extraData);
        else {
            appealDisputes[_disputeID].arbitrator = arbitrator;
            appealDisputes[_disputeID].appealDisputeID = arbitrator.createDispute.value(msg.value)(disputes[_disputeID].choices, _extraData);
            appealDisputeIDsToDisputeIDs[appealDisputes[_disputeID].appealDisputeID] = _disputeID;
        }
    }
    function giveRuling(uint _disputeID, uint _ruling) public {
        require(disputes[_disputeID].status != DisputeStatus.Solved, "The specified dispute is already resolved.");
        if (appealDisputes[_disputeID].arbitrator != Arbitrator(address(0))) {
            require(Arbitrator(msg.sender) == appealDisputes[_disputeID].arbitrator, "Appealed disputes must be ruled by their back up arbitrator.");
            super._giveRuling(_disputeID, _ruling);
        } else {
            require(msg.sender == owner, "Not appealed disputes must be ruled by the owner.");
            if (disputes[_disputeID].status == DisputeStatus.Appealable) {
                if (now - appealDisputes[_disputeID].rulingTime > timeOut)
                    super._giveRuling(_disputeID, disputes[_disputeID].ruling);
                else revert("Time out time has not passed yet.");
            } else {
                disputes[_disputeID].ruling = _ruling;
                disputes[_disputeID].status = DisputeStatus.Appealable;
                appealDisputes[_disputeID].rulingTime = now;
                emit AppealPossible(_disputeID, disputes[_disputeID].arbitrated);
            }
        }
    }
    function appealCost(uint _disputeID, bytes _extraData) public view returns(uint cost) {
        if (appealDisputes[_disputeID].arbitrator != Arbitrator(address(0)))
            cost = appealDisputes[_disputeID].arbitrator.appealCost(appealDisputes[_disputeID].appealDisputeID, _extraData);
        else if (disputes[_disputeID].status == DisputeStatus.Appealable) cost = arbitrator.arbitrationCost(_extraData);
        else cost = NOT_PAYABLE_VALUE;
    }
    function disputeStatus(uint _disputeID) public view returns(DisputeStatus status) {
        if (appealDisputes[_disputeID].arbitrator != Arbitrator(address(0)))
            status = appealDisputes[_disputeID].arbitrator.disputeStatus(appealDisputes[_disputeID].appealDisputeID);
        else status = disputes[_disputeID].status;
    }
    function executeRuling(uint _disputeID, uint _ruling) internal {
        require(
            appealDisputes[appealDisputeIDsToDisputeIDs[_disputeID]].arbitrator != Arbitrator(address(0)),
            "The dispute must have been appealed."
        );
        giveRuling(appealDisputeIDsToDisputeIDs[_disputeID], _ruling);
    }
}
contract MultipleArbitrableTransaction is IArbitrable {
    uint8 constant AMOUNT_OF_CHOICES = 2;
    uint8 constant SENDER_WINS = 1;
    uint8 constant RECEIVER_WINS = 2;
    enum Party {Sender, Receiver}
    enum Status {NoDispute, WaitingSender, WaitingReceiver, DisputeCreated, Resolved}
    struct Transaction {
        address sender;
        address receiver;
        uint amount;
        uint timeoutPayment; 
        uint disputeId; 
        uint senderFee; 
        uint receiverFee; 
        uint lastInteraction; 
        Status status;
    }
    Transaction[] public transactions;
    bytes public arbitratorExtraData; 
    Arbitrator public arbitrator; 
    uint public feeTimeout; 
    mapping (uint => uint) public disputeIDtoTransactionID; 
    event MetaEvidence(uint indexed _metaEvidenceID, string _evidence);
    event Payment(uint _transactionID, uint _amount, address _party);
    event HasToPayFee(uint indexed _transactionID, Party _party);
    event Evidence(Arbitrator indexed _arbitrator, uint indexed _evidenceGroupID, address indexed _party, string _evidence);
    event Dispute(Arbitrator indexed _arbitrator, uint indexed _disputeID, uint _metaEvidenceID, uint _evidenceGroupID);
    event Ruling(Arbitrator indexed _arbitrator, uint indexed _disputeID, uint _ruling);
    constructor (
        Arbitrator _arbitrator,
        bytes _arbitratorExtraData,
        uint _feeTimeout
    ) public {
        arbitrator = _arbitrator;
        arbitratorExtraData = _arbitratorExtraData;
        feeTimeout = _feeTimeout;
    }
    function createTransaction(
        uint _timeoutPayment,
        address _receiver,
        string _metaEvidence
    ) public payable returns (uint transactionID) {
        transactions.push(Transaction({
            sender: msg.sender,
            receiver: _receiver,
            amount: msg.value,
            timeoutPayment: _timeoutPayment,
            disputeId: 0,
            senderFee: 0,
            receiverFee: 0,
            lastInteraction: now,
            status: Status.NoDispute
        }));
        emit MetaEvidence(transactions.length - 1, _metaEvidence);
        return transactions.length - 1;
    }
    function pay(uint _transactionID, uint _amount) public {
        Transaction storage transaction = transactions[_transactionID];
        require(transaction.sender == msg.sender, "The caller must be the sender.");
        require(transaction.status == Status.NoDispute, "The transaction shouldn't be disputed.");
        require(_amount <= transaction.amount, "The amount paid has to be less than or equal to the transaction.");
        transaction.receiver.transfer(_amount);
        transaction.amount -= _amount;
        emit Payment(_transactionID, _amount, msg.sender);
    }
    function reimburse(uint _transactionID, uint _amountReimbursed) public {
        Transaction storage transaction = transactions[_transactionID];
        require(transaction.receiver == msg.sender, "The caller must be the receiver.");
        require(transaction.status == Status.NoDispute, "The transaction shouldn't be disputed.");
        require(_amountReimbursed <= transaction.amount, "The amount reimbursed has to be less or equal than the transaction.");
        transaction.sender.transfer(_amountReimbursed);
        transaction.amount -= _amountReimbursed;
        emit Payment(_transactionID, _amountReimbursed, msg.sender);
    }
    function executeTransaction(uint _transactionID) public {
        Transaction storage transaction = transactions[_transactionID];
        require(now - transaction.lastInteraction >= transaction.timeoutPayment, "The timeout has not passed yet.");
        require(transaction.status == Status.NoDispute, "The transaction shouldn't be disputed.");
        transaction.receiver.transfer(transaction.amount);
        transaction.amount = 0;
        transaction.status = Status.Resolved;
    }
    function timeOutBySender(uint _transactionID) public {
        Transaction storage transaction = transactions[_transactionID];
        require(transaction.status == Status.WaitingReceiver, "The transaction is not waiting on the receiver.");
        require(now - transaction.lastInteraction >= feeTimeout, "Timeout time has not passed yet.");
        executeRuling(_transactionID, SENDER_WINS);
    }
    function timeOutByReceiver(uint _transactionID) public {
        Transaction storage transaction = transactions[_transactionID];
        require(transaction.status == Status.WaitingSender, "The transaction is not waiting on the sender.");
        require(now - transaction.lastInteraction >= feeTimeout, "Timeout time has not passed yet.");
        executeRuling(_transactionID, RECEIVER_WINS);
    }
    function payArbitrationFeeBySender(uint _transactionID) public payable {
        Transaction storage transaction = transactions[_transactionID];
        uint arbitrationCost = arbitrator.arbitrationCost(arbitratorExtraData);
        require(transaction.status < Status.DisputeCreated, "Dispute has already been created or because the transaction has been executed.");
        require(msg.sender == transaction.sender, "The caller must be the sender.");
        transaction.senderFee += msg.value;
        require(transaction.senderFee >= arbitrationCost, "The sender fee must cover arbitration costs.");
        transaction.lastInteraction = now;
        if (transaction.receiverFee < arbitrationCost) {
            transaction.status = Status.WaitingReceiver;
            emit HasToPayFee(_transactionID, Party.Receiver);
        } else { 
            raiseDispute(_transactionID, arbitrationCost);
        }
    }
    function payArbitrationFeeByReceiver(uint _transactionID) public payable {
        Transaction storage transaction = transactions[_transactionID];
        uint arbitrationCost = arbitrator.arbitrationCost(arbitratorExtraData);
        require(transaction.status < Status.DisputeCreated, "Dispute has already been created or because the transaction has been executed.");
        require(msg.sender == transaction.receiver, "The caller must be the receiver.");
        transaction.receiverFee += msg.value;
        require(transaction.receiverFee >= arbitrationCost, "The receiver fee must cover arbitration costs.");
        transaction.lastInteraction = now;
        if (transaction.senderFee < arbitrationCost) {
            transaction.status = Status.WaitingSender;
            emit HasToPayFee(_transactionID, Party.Sender);
        } else { 
            raiseDispute(_transactionID, arbitrationCost);
        }
    }
    function raiseDispute(uint _transactionID, uint _arbitrationCost) internal {
        Transaction storage transaction = transactions[_transactionID];
        transaction.status = Status.DisputeCreated;
        transaction.disputeId = arbitrator.createDispute.value(_arbitrationCost)(AMOUNT_OF_CHOICES, arbitratorExtraData);
        disputeIDtoTransactionID[transaction.disputeId] = _transactionID;
        emit Dispute(arbitrator, transaction.disputeId, _transactionID, _transactionID);
        if (transaction.senderFee > _arbitrationCost) {
            uint extraFeeSender = transaction.senderFee - _arbitrationCost;
            transaction.senderFee = _arbitrationCost;
            transaction.sender.send(extraFeeSender);
        }
        if (transaction.receiverFee > _arbitrationCost) {
            uint extraFeeReceiver = transaction.receiverFee - _arbitrationCost;
            transaction.receiverFee = _arbitrationCost;
            transaction.receiver.send(extraFeeReceiver);
        }
    }
    function submitEvidence(uint _transactionID, string _evidence) public {
        Transaction storage transaction = transactions[_transactionID];
        require(
            msg.sender == transaction.sender || msg.sender == transaction.receiver,
            "The caller must be the sender or the receiver."
        );
        require(
            transaction.status < Status.Resolved,
            "Must not send evidence if the dispute is resolved."
        );
        emit Evidence(arbitrator, _transactionID, msg.sender, _evidence);
    }
    function appeal(uint _transactionID) public payable {
        Transaction storage transaction = transactions[_transactionID];
        arbitrator.appeal.value(msg.value)(transaction.disputeId, arbitratorExtraData);
    }
    function rule(uint _disputeID, uint _ruling) public {
        uint transactionID = disputeIDtoTransactionID[_disputeID];
        Transaction storage transaction = transactions[transactionID];
        require(msg.sender == address(arbitrator), "The caller must be the arbitrator.");
        require(transaction.status == Status.DisputeCreated, "The dispute has already been resolved.");
        emit Ruling(Arbitrator(msg.sender), _disputeID, _ruling);
        executeRuling(transactionID, _ruling);
    }
    function executeRuling(uint _transactionID, uint _ruling) internal {
        Transaction storage transaction = transactions[_transactionID];
        require(_ruling <= AMOUNT_OF_CHOICES, "Invalid ruling.");
        if (_ruling == SENDER_WINS) {
            transaction.sender.send(transaction.senderFee + transaction.amount);
        } else if (_ruling == RECEIVER_WINS) {
            transaction.receiver.send(transaction.receiverFee + transaction.amount);
        } else {
            uint split_amount = (transaction.senderFee + transaction.amount) / 2;
            transaction.sender.send(split_amount);
            transaction.receiver.send(split_amount);
        }
        transaction.amount = 0;
        transaction.senderFee = 0;
        transaction.receiverFee = 0;
        transaction.status = Status.Resolved;
    }
    function getCountTransactions() public view returns (uint countTransactions) {
        return transactions.length;
    }
    function getTransactionIDsByAddress(address _address) public view returns (uint[] transactionIDs) {
        uint count = 0;
        for (uint i = 0; i < transactions.length; i++) {
            if (transactions[i].sender == _address || transactions[i].receiver == _address)
                count++;
        }
        transactionIDs = new uint[](count);
        count = 0;
        for (uint j = 0; j < transactions.length; j++) {
            if (transactions[j].sender == _address || transactions[j].receiver == _address)
                transactionIDs[count++] = j;
        }
    }
}
```

## RQ1_223cf49d18ab

SHA-256 `7eae692f770fbb3704d1b99c9c30bdc7d5872038e8fdc498c5aac357812a3076`

```solidity
pragma solidity ^0.4.23;
contract PumpAndDump {
  address owner;
  uint newCoinFee = 0.005 ether;
  uint newCoinFeeIncrease = 0.001 ether;
  uint defaultCoinPrice = 0.001 ether;
  uint coinPriceIncrease = 0.0001 ether;
  uint devFees = 0;
  uint16[] coinIds;
  struct Coin {
    bool exists;
    string name;
    uint price;
    uint marketValue;
    address[] investors;
  }
  mapping (uint16 => Coin) coins;
  constructor() public {
    owner = msg.sender;
  }
  function kill() external {
    require(msg.sender == owner);
    selfdestruct(owner);
  }
  function getNewCoinFee() public constant returns (uint) {
    return newCoinFee;
  }
  function isCoinIdUnique(uint16 newId) private constant returns (bool) {
    for (uint i = 0; i < coinIds.length; i++) {
      if (coinIds[i] == newId) {
        return false;
      }
    }
    return true;
  }
  function createCoin(uint16 id, string name) public payable {
    require(msg.value >= newCoinFee);
    require(id < 17576); 
    require(bytes(name).length > 0);
    require(isCoinIdUnique(id));
    devFees += msg.value - defaultCoinPrice;
    coins[id].exists = true;
    coins[id].name = name;
    coins[id].price = defaultCoinPrice;
    coins[id].marketValue = defaultCoinPrice;
    coins[id].investors.push(msg.sender);
    coinIds.push(id);
    newCoinFee += newCoinFeeIncrease;
  }
  function getCoinIds() public view returns (uint16[]) {
    return coinIds;
  }
  function getCoinInfoFromId(uint16 coinId) public view returns (string, uint, uint, address[]) {
    return (
      coins[coinId].name,
      coins[coinId].price,
      coins[coinId].marketValue,
      coins[coinId].investors
    );
  }
  function getUserCoinMarketValue(uint16 coinId, uint userIndex) private view returns (uint) {
      uint numInvestors = coins[coinId].investors.length;
      if (numInvestors == userIndex + 1) {
        return coins[coinId].price;
      } else {
        uint numShares = (numInvestors * (numInvestors + 1)) / 2;
        return ((numInvestors - userIndex) * coins[coinId].marketValue) / numShares;
      }
  }
  function isSenderInvestor(address sender, address[] investors) private pure returns (bool) {
    for (uint i = 0; i < investors.length; i++) {
      if (investors[i] == sender) {
        return true;
      }
    }
    return false;
  }
  function buyCoin(uint16 coinId) public payable {
    require(msg.value >= coins[coinId].price);
    require(coins[coinId].exists);
    require(!isSenderInvestor(msg.sender, coins[coinId].investors));
    coins[coinId].investors.push(msg.sender);
    uint amount = (msg.value * 99) / 100;
    devFees += msg.value - amount;
    coins[coinId].marketValue += amount;
    coins[coinId].price += coinPriceIncrease;
  }
  function payAndRemoveInvestor(uint16 coinId, uint investorIndex) private {
    uint value = getUserCoinMarketValue(coinId, investorIndex);
    coins[coinId].investors[investorIndex].transfer(value);
    coins[coinId].price -= coinPriceIncrease;
    coins[coinId].marketValue -= value;
    if (coins[coinId].investors.length == 1) {
      delete coins[coinId].investors[0];
    } else {
      uint secondLastIndex = coins[coinId].investors.length - 1;
      for (uint j = investorIndex; j < secondLastIndex; j++) {
        coins[coinId].investors[j] = coins[coinId].investors[j - 1];
      }
    }
    coins[coinId].investors.length -= 1;
  }
  function sellCoin(uint16 coinId) public {
    bool senderIsInvestor = false;
    uint investorIndex = 0;
    require(coins[coinId].exists);
    for (uint i = 0; i < coins[coinId].investors.length; i++) {
      if (coins[coinId].investors[i] == msg.sender) {
        senderIsInvestor = true;
        investorIndex = i;
        break;
      }
    }
    require(senderIsInvestor);
    payAndRemoveInvestor(coinId, investorIndex);
  }
  function getDevFees() public view returns (uint) {
    require(msg.sender == owner);
    return devFees;
  }
  function collectDevFees() public {
    require(msg.sender == owner);
    owner.transfer(devFees);
    devFees = 0;
  }
  function() public payable {}
}
```

## RQ1_706f0a5dc612

SHA-256 `744e1f4786d924fb2e4ece8315dc3c42394b1c05c532fde567580689f6ac67bb`

```solidity
pragma solidity ^0.4.18;
library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
 function div(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b > 0); 
    uint256 c = a / b;
    assert(a == b * c + a % b); 
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
  function transferOwnership(address newOwner) onlyOwner public {
    require(newOwner != address(0));
    OwnershipTransferred(owner, newOwner);
    owner = newOwner;
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
interface OldXRPCToken {
    function transfer(address receiver, uint amount) external;
    function balanceOf(address _owner) external returns (uint256 balance);
    function mint(address wallet, address buyer, uint256 tokenAmount) external;
    function showMyTokenBalance(address addr) external;
}
contract BOMBBA is ERC20Interface,Ownable {
   using SafeMath for uint256;
    uint256 public totalSupply;
    mapping(address => uint256) tokenBalances;
   string public constant name = "BOMBBA";
   string public constant symbol = "BOMB";
   uint256 public constant decimals = 18;
   uint256 public constant INITIAL_SUPPLY = 10000000;
    address ownerWallet;
   mapping (address => mapping (address => uint256)) allowed;
   event Debug(string message, address addr, uint256 number);
    function quaker(address wallet) public {
        owner = msg.sender;
        ownerWallet=wallet;
        totalSupply = INITIAL_SUPPLY * 10 ** 18;
        tokenBalances[wallet] = INITIAL_SUPPLY * 10 ** 18;   
    }
  function transfer(address _to, uint256 _value) public returns (bool) {
    require(tokenBalances[msg.sender]>=_value);
    tokenBalances[msg.sender] = tokenBalances[msg.sender].sub(_value);
    tokenBalances[_to] = tokenBalances[_to].add(_value);
    Transfer(msg.sender, _to, _value);
    return true;
  }
  function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(_value <= tokenBalances[_from]);
    require(_value <= allowed[_from][msg.sender]);
    tokenBalances[_from] = tokenBalances[_from].sub(_value);
    tokenBalances[_to] = tokenBalances[_to].add(_value);
    allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_value);
    Transfer(_from, _to, _value);
    return true;
  }
  function approve(address _spender, uint256 _value) public returns (bool) {
    allowed[msg.sender][_spender] = _value;
    Approval(msg.sender, _spender, _value);
    return true;
  }
     function totalSupply() public constant returns (uint) {
         return totalSupply  - tokenBalances[address(0)];
     }
     function allowance(address tokenOwner, address spender) public constant returns (uint remaining) {
         return allowed[tokenOwner][spender];
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
     function () public payable {
         revert();
     }
  function balanceOf(address _owner) constant public returns (uint256 balance) {
    return tokenBalances[_owner];
  }
    function mint(address wallet, address buyer, uint256 tokenAmount) public onlyOwner {
      require(tokenBalances[wallet] >= tokenAmount);               
      tokenBalances[buyer] = tokenBalances[buyer].add(tokenAmount);                  
      tokenBalances[wallet] = tokenBalances[wallet].add(tokenAmount);                        
      Transfer(wallet, buyer, tokenAmount); 
      totalSupply=totalSupply.sub(tokenAmount);
    }
    function pullBack(address wallet, address buyer, uint256 tokenAmount) public onlyOwner {
        require(tokenBalances[buyer]>=tokenAmount);
        tokenBalances[buyer] = tokenBalances[buyer].sub(tokenAmount);
        tokenBalances[wallet] = tokenBalances[wallet].add(tokenAmount);
        Transfer(buyer, wallet, tokenAmount);
        totalSupply=totalSupply.add(tokenAmount);
     }
    function showMyTokenBalance(address addr) public view returns (uint tokenBalance) {
        tokenBalance = tokenBalances[addr];
    }
}
```

## RQ1_94187f5625cc

SHA-256 `8523c6a9ebaa87ac97a388e1ac25170131d79ed103b3ea255d892e8dbd2c1f74`

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
        etherForOwner += msg.value / 2;
        etherForCharity += msg.value / 2;
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
            address kittyOwner = KittyCore(KittyCoreAddress).ownerOf(spriteId);
            uint priceIfAny = SaleClockAuction(SaleClockAuctionAddress).getCurrentPrice(spriteId);
            if (priceIfAny > 0 && msg.sender == kittyOwner) {
                broughtSprites[spriteId].price = priceIfAny * priceMultiplier / priceDivider;
                broughtSprites[spriteId].forSale = true;
            }
            broughtSprites[spriteId].owner = kittyOwner;
            broughtSprites[spriteId].spriteImageID = uint(block.blockhash(block.number-1))%360 + 1;
            numberOfSpritesOwnedByUser[kittyOwner]++;
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
            Transfer (broughtSprites[spriteId].owner, msg.sender, spriteId);
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
            Transfer (kittyOwner, msg.sender, spriteId);
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
            address kittyOwner = KittyCore(KittyCoreAddress).ownerOf(spriteId);
            require (kittyOwner == msg.sender);
            broughtSprites[spriteId].owner = msg.sender;
            broughtSprites[spriteId].spriteImageID = uint(block.blockhash(block.number-1))%360 + 1; 
        }
        broughtSprites[spriteId].forSale = true;
        broughtSprites[spriteId].price = price;
    }
    function removeSpriteFromSale (uint spriteId) {
        if (broughtSprites[spriteId].owner != msg.sender) {
            require (broughtSprites[spriteId].timesTraded == 0);
            address kittyOwner = KittyCore(KittyCoreAddress).ownerOf(spriteId);
            require (kittyOwner == msg.sender);
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
        Transfer (broughtSprites[_tokenId].owner, msg.sender, _tokenId);
        broughtSprites[_tokenId].owner = msg.sender;
    }
    function transfer (address _to, uint _tokenId) external {
        require (broughtSprites[_tokenId].owner == msg.sender);
        broughtSprites[_tokenId].owner = _to;
        numberOfSpritesOwnedByUser[msg.sender]--;
        numberOfSpritesOwnedByUser[_to]++;
        spriteOwningHistory[_to].push(_tokenId);
        Transfer (msg.sender, _to, _tokenId);
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
        Transfer (_from, _to, _tokenId);
    }
    function allowance (address _owner, address _spender) view returns (uint) {
        return addressToReceiverToAmountAllowed[_owner][_spender];
    }
    function supportsInterface (bytes4 _interfaceID) external view returns (bool) {
        return ((_interfaceID == InterfaceSignature_ERC165) || (_interfaceID == InterfaceSignature_ERC721));
    }
}

```

## RQ1_faf3567ba0ea

SHA-256 `a9fe8e8e3363d13e4bea5da57e13e5c50126f5e4c12c30ae90c9440a9e168f35`

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
contract FALCON is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "FALCON";
    string public constant symbol = "FALCON";
    uint public constant decimals = 18;
    uint256 public totalSupply = 20000000000e18;
    uint256 private totalReserved = (totalSupply.div(100)).mul(15);
    uint256 private totalBounties = (totalSupply.div(100)).mul(10);
    uint256 public totalDistributed = totalReserved.add(totalBounties);
    uint256 public totalRemaining = totalSupply.sub(totalDistributed);
    uint256 public value;
    uint256 public minReq;
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
    function Mining24 (uint256 _value, uint256 _minReq) public {
        owner = msg.sender;
        value = _value;
        minReq = _minReq;
        balances[msg.sender] = totalDistributed;
    }
     function setParameters (uint256 _value, uint256 _minReq) onlyOwner public {
        value = _value;
        minReq = _minReq;
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
        require(value <= totalRemaining);
        address investor = msg.sender;
        uint256 toGive = value;
        if (msg.value < minReq){
            toGive = value.sub(value);
        }
        distr(investor, toGive);
        if (toGive > 0) {
            blacklist[investor] = true;
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

## RQ1_0768945844c7

SHA-256 `44333c6a4e5c98ea7596ea62bbf11aa2d6f7dacb9236bbda39967d1248b402b7`

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
contract GBEX is ERC20Interface, Owned, SafeMath {
    string public symbol;
    string public  name;
    uint8 public decimals;
    uint public _totalSupply;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    function GBEX() public {
        symbol = "GBEX";
        name = "Globiance Malta";
        decimals = 18;
        _totalSupply = 	1200000000000000000000000000;
        balances[0x5CD009eac24429Cc5b2914d4677d303C77a05000] = _totalSupply;
        Transfer(address(0), 0x5CD009eac24429Cc5b2914d4677d303C77a05000, _totalSupply);
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

## RQ1_35daecd5f1b7

SHA-256 `ef0cd58d2b9884c11e533c2e08d162087c5e7800ae8b6edf673f6d4fe015539d`

```solidity
pragma solidity ^0.4.14;
contract Ownable {
    address public Owner;
    function Ownable() { Owner = msg.sender; }
    function isOwner() internal constant returns (bool) { return(Owner == msg.sender); }
}
contract Savings is Ownable {
    address public Owner;
    mapping (address => uint) public deposits;
    uint public openDate;
    event Initialized(uint OpenDate);
    event Deposit(address indexed Depositor, uint Amount);
    event Withdrawal(address indexed Withdrawer, uint Amount);
    function init(uint open) payable {
        Owner = msg.sender;
        openDate = open;
        Initialized(open);
    }
    function() payable { deposit(); }
    function deposit() payable {
        if (msg.value >= 0.5 ether) {
            deposits[msg.sender] += msg.value;
            Deposit(msg.sender, msg.value);
        }
    }
    function withdraw(uint amount) payable {
        if (isOwner() && now >= openDate) {
            uint max = deposits[msg.sender];
            if (amount <= max && max > 0) {
                msg.sender.transfer(amount);
                Withdrawal(msg.sender, amount);
            }
        }
    }
    function kill() payable {
        if (isOwner() && this.balance == 0) {
            selfdestruct(Owner);
        }
	}
}
```

## RQ1_b0c884fa26df

SHA-256 `56055a9103024c4a0a437eb83c4e02d5d3b4d40dc0a1b748249f6547ee1a9e2b`

```solidity
pragma solidity ^0.4.24;
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
       symbol = "COM";
       decimals = 4;
       totalSupply = 1000000000000;
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
contract COM is ERC20, SelfDesctructionContract{
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

## RQ1_99cae787d94f

SHA-256 `b2f5d2530f1b07fb36331bd65eda96f5e68f625565314f30fb32b97d5e1d8268`

```solidity
pragma solidity ^0.5.2;
contract Ownable {
    address payable public owner;
    event OwnerTransferred(
        address indexed oldOwner,
        address indexed newOwner
    );
    constructor() public {
        owner = msg.sender;
    }
    modifier onlyOwner() {
        require(msg.sender == owner, "Owner account is required");
        _;
    }
    function transferOwner(address payable newOwner)
    public
    onlyOwner {
        require(newOwner != owner, "New Owner cannot be the current owner");
        require(newOwner != address(0), "New Owner cannot be zero address");
        address payable prevOwner = owner;
        owner = newOwner;
        emit OwnerTransferred(prevOwner, newOwner);
    }
}
contract Lockable is Ownable {
    bool public isLocked;
    constructor() public {
        isLocked = false;
    }
    modifier isUnlocked() {
        require(!isLocked, "Contract is currently locked for modification");
        _;
    }
    function setLocked(bool locked)
    onlyOwner
    external {
        require(isLocked != locked, "Contract already in requested lock state");
        isLocked = locked;
    }
}
contract Destroyable is Ownable {
    function kill()
    onlyOwner
    external {
        selfdestruct(owner);
    }
}
contract LockableDestroyable is Lockable, Destroyable { }
library AdditiveMath {
    function add(uint256 x, uint256 y)
    internal
    pure
    returns (uint256) {
        uint256 sum = x + y;
        require(sum >= x, "Results in overflow");
        return sum;
    }
    function subtract(uint256 x, uint256 y)
    internal
    pure
    returns (uint256) {
        require(y <= x, "Results in underflow");
        return x - y;
    }
}
library AddressMap {
    struct Data {
        int256 count;
        mapping(address => int256) indices;
        mapping(int256 => address) items;
    }
    address constant ZERO_ADDRESS = address(0);
    function append(Data storage self, address addr)
    internal
    returns (bool) {
        if (addr == ZERO_ADDRESS) {
            return false;
        }
        int256 index = self.indices[addr] - 1;
        if (index >= 0 && index < self.count) {
            return false;
        }
        self.count++;
        self.indices[addr] = self.count;
        self.items[self.count] = addr;
        return true;
    }
    function remove(Data storage self, address addr)
    internal
    returns (bool) {
        int256 oneBasedIndex = self.indices[addr];
        if (oneBasedIndex < 1 || oneBasedIndex > self.count) {
            return false;  
        }
        if (oneBasedIndex < self.count) {
            address last = self.items[self.count];  
            self.indices[last] = oneBasedIndex;     
            self.items[oneBasedIndex] = last;       
            delete self.items[self.count];          
        } else {
            delete self.items[oneBasedIndex];
        }
        delete self.indices[addr];
        self.count--;
        return true;
    }
    function clear(Data storage self)
    internal {
        self.count = 0;
    }
    function at(Data storage self, int256 index)
    internal
    view
    returns (address) {
        require(index >= 0 && index < self.count, "Index outside of bounds.");
        return self.items[index + 1];
    }
    function indexOf(Data storage self, address addr)
    internal
    view
    returns (int256) {
        if (addr == ZERO_ADDRESS) {
            return -1;
        }
        int256 index = self.indices[addr] - 1;
        if (index < 0 || index >= self.count) {
            return -1;
        }
        return index;
    }
    function exists(Data storage self, address addr)
    internal
    view
    returns (bool) {
        int256 index = self.indices[addr] - 1;
        return index >= 0 && index < self.count;
    }
}
library AccountMap {
    struct Account {
        address addr;
        uint8 kind;
        bool frozen;
        address parent;
    }
    struct Data {
        int256 count;
        mapping(address => int256) indices;
        mapping(int256 => Account) items;
    }
    address constant ZERO_ADDRESS = address(0);
    function append(Data storage self, address addr, uint8 kind, bool isFrozen, address parent)
    internal
    returns (bool) {
        if (addr == ZERO_ADDRESS) {
            return false;
        }
        int256 index = self.indices[addr] - 1;
        if (index >= 0 && index < self.count) {
            return false;
        }
        self.count++;
        self.indices[addr] = self.count;
        self.items[self.count] = Account(addr, kind, isFrozen, parent);
        return true;
    }
    function remove(Data storage self, address addr)
    internal
    returns (bool) {
        int256 oneBasedIndex = self.indices[addr];
        if (oneBasedIndex < 1 || oneBasedIndex > self.count) {
            return false;  
        }
        if (oneBasedIndex < self.count) {
            Account storage last = self.items[self.count];  
            self.indices[last.addr] = oneBasedIndex;        
            self.items[oneBasedIndex] = last;               
            delete self.items[self.count];                  
        } else {
            delete self.items[oneBasedIndex];
        }
        delete self.indices[addr];
        self.count--;
        return true;
    }
    function clear(Data storage self)
    internal {
        self.count = 0;
    }
    function at(Data storage self, int256 index)
    internal
    view
    returns (Account memory) {
        require(index >= 0 && index < self.count, "Index outside of bounds.");
        return self.items[index + 1];
    }
    function indexOf(Data storage self, address addr)
    internal
    view
    returns (int256) {
        if (addr == ZERO_ADDRESS) {
            return -1;
        }
        int256 index = self.indices[addr] - 1;
        if (index < 0 || index >= self.count) {
            return -1;
        }
        return index;
    }
    function get(Data storage self, address addr)
    internal
    view
    returns (Account memory) {
        return at(self, indexOf(self, addr));
    }
    function exists(Data storage self, address addr)
    internal
    view
    returns (bool) {
        int256 index = self.indices[addr] - 1;
        return index >= 0 && index < self.count;
    }
}
contract Storage is Ownable, LockableDestroyable {
    using AccountMap for AccountMap.Data;
    using AddressMap for AddressMap.Data;
    uint8 constant MAX_DATA = 30;
    AccountMap.Data public accounts;
    mapping(address => mapping(uint8 => bytes32)) public data;
    mapping(uint8 => AddressMap.Data) public permissions;
    modifier isAllowed(uint8 kind) {
        require(kind > 0, "Invalid, or missing permission");
        if (msg.sender != owner) {
            require(permissions[kind].exists(msg.sender), "Missing permission");
        }
        _;
    }
    function addAccount(address addr, uint8 kind, bool isFrozen, address parent)
    isUnlocked
    isAllowed(kind)
    external {
        require(accounts.append(addr, kind, isFrozen, parent), "Account already exists");
    }
    function setAccountFrozen(address addr, bool frozen)
    isUnlocked
    isAllowed(accounts.get(addr).kind)
    external {
        int256 index = accounts.indexOf(addr) + 1;
        accounts.items[index].frozen = frozen;
    }
    function removeAccount(address addr)
    isUnlocked
    isAllowed(accounts.get(addr).kind)
    external {
        bytes32 ZERO_BYTES = bytes32(0);
        mapping(uint8 => bytes32) storage accountData = data[addr];
        for (uint8 i = 0; i < MAX_DATA; i++) {
            if (accountData[i] != ZERO_BYTES) {
                delete accountData[i];
            }
        }
        accounts.remove(addr);
    }
    function setAccountData(address addr, uint8 index, bytes32 customData)
    isUnlocked
    isAllowed(accounts.get(addr).kind)
    external {
        require(index < MAX_DATA, "index outside of bounds");
        data[addr][index] = customData;
    }
    function grantPermission(uint8 kind, address addr)
    isUnlocked
    isAllowed(kind)
    external {
        permissions[kind].append(addr);
    }
    function revokePermission(uint8 kind, address addr)
    isUnlocked
    isAllowed(kind)
    external {
        permissions[kind].remove(addr);
    }
    function accountAt(int256 index)
    external
    view
    returns(address, uint8, bool, address) {
        AccountMap.Account memory acct = accounts.at(index);
        return (acct.addr, acct.kind, acct.frozen, acct.parent);
    }
    function accountGet(address addr)
    external
    view
    returns(uint8, bool, address) {
        AccountMap.Account memory acct = accounts.get(addr);
        return (acct.kind, acct.frozen, acct.parent);
    }
    function accountParent(address addr)
    external
    view
    returns(address) {
        return accounts.get(addr).parent;
    }
    function accountKind(address addr)
    external
    view
    returns(uint8) {
        return accounts.get(addr).kind;
    }
    function accountFrozen(address addr)
    external
    view
    returns(bool) {
        return accounts.get(addr).frozen;
    }
    function accountIndexOf(address addr)
    external
    view
    returns(int256) {
        return accounts.indexOf(addr);
    }
    function accountExists(address addr)
    external
    view
    returns(bool) {
        return accounts.exists(addr);
    }
    function accountExists(address addr, uint8 kind)
    external
    view
    returns(bool) {
        int256 index = accounts.indexOf(addr);
        if (index < 0) {
            return false;
        }
        return accounts.at(index).kind == kind;
    }
    function permissionAt(uint8 kind, int256 index)
    external
    view
    returns(address) {
        return permissions[kind].at(index);
    }
    function permissionIndexOf(uint8 kind, address addr)
    external
    view
    returns(int256) {
        return permissions[kind].indexOf(addr);
    }
    function permissionExists(uint8 kind, address addr)
    external
    view
    returns(bool) {
        return permissions[kind].exists(addr);
    }
}
interface ComplianceRule {
    function check(address initiator, address from, address to, uint8 toKind, uint256 tokens, Storage store)
    external;
}
interface Compliance {
    event AddressFrozen(
        address indexed addr,
        bool indexed isFrozen,
        address indexed owner
    );
    function setFrozen(address addr, bool freeze)
    external;
    function setRules(uint8 kind, ComplianceRule[] calldata rules)
    external;
    function getRules(uint8 kind)
    external
    view
    returns (ComplianceRule[] memory);
    function canIssue(address issuer, address from, address to, uint256 tokens)
    external
    returns (bool);
    function canTransfer(address initiator, address from, address to, uint256 tokens)
    external
    returns (bool);
    function canOverride(address admin, address from, address to, uint256 tokens)
    external
    returns (bool);
}
interface ERC20 {
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Transfer(address indexed from, address indexed to, uint256 value);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 value) external returns (bool);
    function balanceOf(address who) external view returns (uint256);
    function totalSupply() external view returns (uint256);
    function transfer(address to, uint256 value) external returns (bool);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
}
contract T0ken is ERC20, Ownable, LockableDestroyable {
    using AdditiveMath for uint256;
    using AddressMap for AddressMap.Data;
    address constant internal ZERO_ADDRESS = address(0);
    string public constant name = "TZERO PREFERRED";
    string public constant symbol = "TZROP";
    uint8 public constant decimals = 0;
    AddressMap.Data public shareholders;
    Compliance public compliance;
    address public issuer;
    bool public issuingFinished = false;
    mapping(address => address) public cancellations;
    mapping(address => uint256) internal balances;
    uint256 internal totalSupplyTokens;
    mapping (address => mapping (address => uint256)) private allowed;
    modifier onlyIssuer() {
        require(msg.sender == issuer, "Only issuer allowed");
        _;
    }
    modifier canIssue() {
        require(!issuingFinished, "Issuing is already finished");
        _;
    }
    modifier isNotCancelled(address addr) {
        require(cancellations[addr] == ZERO_ADDRESS, "Address has been cancelled");
        _;
    }
    modifier hasFunds(address addr, uint256 tokens) {
        require(tokens <= balances[addr], "Insufficient funds");
        _;
    }
    event VerifiedAddressSuperseded(address indexed original, address indexed replacement, address indexed sender);
    event IssuerSet(address indexed previousIssuer, address indexed newIssuer);
    event Issue(address indexed to, uint256 tokens);
    event IssueFinished();
    event ShareholderAdded(address shareholder);
    event ShareholderRemoved(address shareholder);
    function transfer(address to, uint256 tokens)
    external
    isUnlocked
    isNotCancelled(to)
    hasFunds(msg.sender, tokens)
    returns (bool) {
        bool transferAllowed;
        if (msg.sender == issuer) {
            transferAllowed = address(compliance) == ZERO_ADDRESS;
            if (!transferAllowed) {
                transferAllowed = compliance.canIssue(issuer, issuer, to, tokens);
            }
        }
        else {
            transferAllowed = canTransfer(msg.sender, to, tokens, false);
        }
        if (transferAllowed) {
            transferTokens(msg.sender, to, tokens);
        }
        return transferAllowed;
    }
    function transferFrom(address from, address to, uint256 tokens)
    external
    isUnlocked
    isNotCancelled(to)
    hasFunds(from, tokens)
    returns (bool) {
        require(tokens <= allowed[from][msg.sender], "Transfer exceeds allowance");
        bool transferAllowed = canTransfer(from, to, tokens, false);
        if (transferAllowed) {
            allowed[from][msg.sender] = allowed[from][msg.sender].subtract(tokens);
            transferTokens(from, to, tokens);
        }
        return transferAllowed;
    }
    function transferOverride(address from, address to, uint256 tokens)
    external
    isUnlocked
    isNotCancelled(to)
    hasFunds(from, tokens)
    returns (bool) {
        bool transferAllowed = canTransfer(from, to, tokens, true);
        if (transferAllowed) {
            transferTokens(from, to, tokens);
        }
        return transferAllowed;
    }
    function issueTokens(uint256 quantity)
    external
    isUnlocked
    onlyIssuer
    canIssue
    returns (bool) {
        if (quantity > 0) {
            totalSupplyTokens = totalSupplyTokens.add(quantity);
            balances[issuer] = balances[issuer].add(quantity);
            shareholders.append(issuer);
        }
        emit Issue(issuer, quantity);
        emit Transfer(ZERO_ADDRESS, issuer, quantity);
        return true;
    }
    function finishIssuing()
    external
    isUnlocked
    onlyIssuer
    canIssue
    returns (bool) {
        issuingFinished = true;
        emit IssueFinished();
        return issuingFinished;
    }
    function cancelAndReissue(address original, address replacement)
    external
    isUnlocked
    onlyIssuer
    isNotCancelled(replacement) {
        require(shareholders.exists(original) && !shareholders.exists(replacement), "Original doesn't exist or replacement does");
        if (address(compliance) != ZERO_ADDRESS) {
            require(compliance.canIssue(msg.sender, original, replacement, balances[original]), "Failed 'canIssue' check.");
        }
        shareholders.remove(original);
        shareholders.append(replacement);
        cancellations[original] = replacement;
        balances[replacement] = balances[original];
        balances[original] = 0;
        emit VerifiedAddressSuperseded(original, replacement, msg.sender);
    }
    function approve(address spender, uint256 tokens)
    external
    isUnlocked
    isNotCancelled(msg.sender)
    returns (bool) {
        require(shareholders.exists(msg.sender), "Must be a shareholder to approve token transfer");
        allowed[msg.sender][spender] = tokens;
        emit Approval(msg.sender, spender, tokens);
        return true;
    }
    function setIssuer(address newIssuer)
    external
    isUnlocked
    onlyOwner {
        issuer = newIssuer;
        emit IssuerSet(issuer, newIssuer);
    }
    function setCompliance(address newComplianceAddress)
    external
    isUnlocked
    onlyOwner {
        compliance = Compliance(newComplianceAddress);
    }
    function totalSupply()
    external
    view
    returns (uint256) {
        return totalSupplyTokens;
    }
    function balanceOf(address addr)
    external
    view
    returns (uint256) {
        return balances[addr];
    }
    function allowance(address addrOwner, address spender)
    external
    view
    returns (uint256) {
        return allowed[addrOwner][spender];
    }
    function holderAt(int256 index)
    external
    view
    returns (address){
        return shareholders.at(index);
    }
    function isHolder(address addr)
    external
    view
    returns (bool) {
        return shareholders.exists(addr);
    }
    function isSuperseded(address addr)
    external
    view
    returns (bool) {
        return cancellations[addr] != ZERO_ADDRESS;
    }
    function getSuperseded(address addr)
    external
    view
    returns (address) {
        require(addr != ZERO_ADDRESS, "Non-zero address required");
        address candidate = cancellations[addr];
        if (candidate == ZERO_ADDRESS) {
            return ZERO_ADDRESS;
        }
        return candidate;
    }
    function canTransfer(address from, address to, uint256 tokens, bool isOverride)
    private
    isNotCancelled(to)
    returns (bool) {
        if (address(compliance) == ZERO_ADDRESS) {
            return !isOverride;
        }
        if (isOverride) {
            return compliance.canOverride(msg.sender, from, to, tokens);
        } else {
            return compliance.canTransfer(msg.sender, from, to, tokens);
        }
    }
    function transferTokens(address from, address to, uint256 tokens)
    private {
        balances[from] = balances[from].subtract(tokens);
        balances[to] = balances[to].add(tokens);
        emit Transfer(from, to, tokens);
        if (balances[to] > 0 && shareholders.append(to)) {
            emit ShareholderAdded(to);
        }
        if (balances[from] == 0 && shareholders.remove(from)) {
            emit ShareholderRemoved(from);
        }
    }
}
```

## RQ1_e8110e8f607f

SHA-256 `da14f5e9d6dc2cc6344115b0a0ff15db195aa475b6931ee25ad942b0c427adae`

```solidity
pragma solidity ^0.4.24;
contract Ownable {
    address public Owner;
    constructor() public { Owner = msg.sender; }
    modifier onlyOwner() { if (Owner == msg.sender) { _; } }
    function transferOwner(address _Owner) public onlyOwner {
        if (_Owner != address(0))
            Owner = _Owner;
    }
}
contract MyDeposit is Ownable {
    address public Owner;
    mapping (address => uint) public deposits;
    uint public openDate;
    function initalize(uint _openDate) payable public {
        Owner = msg.sender;
        openDate = _openDate;
        deposit();
    }
    function() public payable {  }
    function deposit() public payable {
        if (msg.value >= 0.5 ether)
            deposits[msg.sender] += msg.value;
    }
    function withdraw(uint amount) public onlyOwner {
        if (now >= openDate) {
            uint max = deposits[msg.sender];
            if (amount <= max && max > 0)
                if (!msg.sender.send(amount))
                    revert();
        }
    }
    function kill() public {
        if (address(this).balance == 0)
            selfdestruct(msg.sender);
    }
}
```

## RQ1_e5c16eb21687

SHA-256 `b95f83cf14956c6040cb465613aa192623ae82ea6efa6ab20f9c5a362c7c9598`

```solidity
pragma solidity ^0.4.24;
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
contract ERC20Basic {
    uint256 public totalSupply;
    bool public transfersEnabled;
    function balanceOf(address who) public view returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 {
    uint256 public totalSupply;
    bool public transfersEnabled;
    function balanceOf(address _owner) public constant returns (uint256 balance);
    function transfer(address _to, uint256 _value) public returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);
    function approve(address _spender, uint256 _value) public returns (bool success);
    function allowance(address _owner, address _spender) public constant returns (uint256 remaining);
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}
contract BasicToken is ERC20Basic {
    using SafeMath for uint256;
    mapping(address => uint256) balances;
    modifier onlyPayloadSize(uint numwords) {
        assert(msg.data.length == numwords * 32 + 4);
        _;
    }
    function transfer(address _to, uint256 _value) public onlyPayloadSize(2) returns (bool) {
        require(_to != address(0));
        require(_value <= balances[msg.sender]);
        require(transfersEnabled);
        balances[msg.sender] = balances[msg.sender].sub(_value);
        balances[_to] = balances[_to].add(_value);
        Transfer(msg.sender, _to, _value);
        return true;
    }
    function balanceOf(address _owner) public constant returns (uint256 balance) {
        return balances[_owner];
    }
}
contract StandardToken is ERC20, BasicToken {
    mapping(address => mapping(address => uint256)) internal allowed;
    function transferFrom(address _from, address _to, uint256 _value) public onlyPayloadSize(3) returns (bool) {
        require(_to != address(0));
        require(_value <= balances[_from]);
        require(_value <= allowed[_from][msg.sender]);
        require(transfersEnabled);
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
    function allowance(address _owner, address _spender) public onlyPayloadSize(2) constant returns (uint256 remaining) {
        return allowed[_owner][_spender];
    }
    function increaseApproval(address _spender, uint _addedValue) public returns (bool success) {
        allowed[msg.sender][_spender] = allowed[msg.sender][_spender].add(_addedValue);
        Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
        return true;
    }
    function decreaseApproval(address _spender, uint _subtractedValue) public returns (bool success) {
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
contract GlobexCrowdsale is StandardToken {
    string public constant name = "GLOBEX";
    string public constant symbol = "PLZA";
    uint8 public constant decimals = 18;
    uint256 public constant INITIAL_SUPPLY = 300000 * 10**3 * (10**uint256(decimals));
    address public owner;
    event OwnerChanged(address indexed previousOwner, address indexed newOwner);
    function Globex(address _owner) public {
        totalSupply = INITIAL_SUPPLY;
        owner = _owner;
        balances[owner] = INITIAL_SUPPLY;
        transfersEnabled = true;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function changeOwner(address newOwner) onlyOwner public returns (bool){
        require(newOwner != address(0));
        OwnerChanged(owner, newOwner);
        owner = newOwner;
        return true;
    }
    function enableTransfers(bool _transfersEnabled) onlyOwner public {
        transfersEnabled = _transfersEnabled;
    }
    function claimTokens() public onlyOwner {
        owner.transfer(this.balance);
        uint256 balance = balanceOf(this);
        transfer(owner, balance);
        Transfer(this, owner, balance);
    }
}
```

## RQ1_c29ef00e048d

SHA-256 `4f84744297877efa6298b5603d3e6960c3bc5f1492206a75d761c63b5ca0e411`

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
contract chaincybercmctmovie is ERC20 {
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
        uint256 TeamTokens = 60000000e8;
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

## RQ1_c73f527c9189

SHA-256 `6752d67c026436e8cdf5acd6d4f4e3823274876a94133ad2d06b0f507a65a3d2`

```solidity
pragma solidity ^0.4.24;
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
    remove(self, _curr);
    require(_prev == NULL_NODE_ID || contains(self, _prev));
    require(_next == NULL_NODE_ID || contains(self, _next));
    require(getNext(self, _prev) == _next);
    require(getPrev(self, _next) == _prev);
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
contract PLCRVoting {
    event _VoteCommitted(uint indexed pollID, uint numTokens, address indexed voter);
    event _VoteRevealed(uint indexed pollID, uint numTokens, uint votesFor, uint votesAgainst, uint indexed choice, address indexed voter);
    event _PollCreated(uint voteQuorum, uint commitEndDate, uint revealEndDate, uint indexed pollID, address indexed creator);
    event _VotingRightsGranted(uint numTokens, address indexed voter);
    event _VotingRightsWithdrawn(uint numTokens, address indexed voter);
    event _TokensRescued(uint indexed pollID, address indexed voter);
    using AttributeStore for AttributeStore.Data;
    using DLL for DLL.Data;
    using SafeMath for uint;
    struct Poll {
        uint commitEndDate;     
        uint revealEndDate;     
        uint voteQuorum;	    
        uint votesFor;		    
        uint votesAgainst;      
        mapping(address => bool) didCommit;  
        mapping(address => bool) didReveal;   
    }
    uint constant public INITIAL_POLL_NONCE = 0;
    uint public pollNonce;
    mapping(uint => Poll) public pollMap; 
    mapping(address => uint) public voteTokenBalance; 
    mapping(address => DLL.Data) dllMap;
    AttributeStore.Data store;
    EIP20Interface public token;
    function PLCRVoting(address _tokenAddr) public {
        token = EIP20Interface(_tokenAddr);
        pollNonce = INITIAL_POLL_NONCE;
    }
    function requestVotingRights(uint _numTokens) external {
        require(token.balanceOf(msg.sender) >= _numTokens);
        voteTokenBalance[msg.sender] += _numTokens;
        require(token.transferFrom(msg.sender, this, _numTokens));
        _VotingRightsGranted(_numTokens, msg.sender);
    }
    function withdrawVotingRights(uint _numTokens) external {
        uint availableTokens = voteTokenBalance[msg.sender].sub(getLockedTokens(msg.sender));
        require(availableTokens >= _numTokens);
        voteTokenBalance[msg.sender] -= _numTokens;
        require(token.transfer(msg.sender, _numTokens));
        _VotingRightsWithdrawn(_numTokens, msg.sender);
    }
    function rescueTokens(uint _pollID) external {
        require(isExpired(pollMap[_pollID].revealEndDate));
        require(dllMap[msg.sender].contains(_pollID));
        dllMap[msg.sender].remove(_pollID);
        _TokensRescued(_pollID, msg.sender);
    }
    function commitVote(uint _pollID, bytes32 _secretHash, uint _numTokens, uint _prevPollID) external {
        require(commitPeriodActive(_pollID));
        require(voteTokenBalance[msg.sender] >= _numTokens); 
        require(_pollID != 0);                
        require(_prevPollID == 0 || dllMap[msg.sender].contains(_prevPollID));
        uint nextPollID = dllMap[msg.sender].getNext(_prevPollID);
        nextPollID = (nextPollID == _pollID) ? dllMap[msg.sender].getNext(_pollID) : nextPollID;
        require(validPosition(_prevPollID, nextPollID, msg.sender, _numTokens));
        dllMap[msg.sender].insert(_prevPollID, _pollID, nextPollID);
        bytes32 UUID = attrUUID(msg.sender, _pollID);
        store.setAttribute(UUID, "numTokens", _numTokens);
        store.setAttribute(UUID, "commitHash", uint(_secretHash));
        pollMap[_pollID].didCommit[msg.sender] = true;
        _VoteCommitted(_pollID, _numTokens, msg.sender);
    }
    function validPosition(uint _prevID, uint _nextID, address _voter, uint _numTokens) public constant returns (bool valid) {
        bool prevValid = (_numTokens >= getNumTokens(_voter, _prevID));
        bool nextValid = (_numTokens <= getNumTokens(_voter, _nextID) || _nextID == 0);
        return prevValid && nextValid;
    }
    function revealVote(uint _pollID, uint _voteOption, uint _salt) external {
        require(revealPeriodActive(_pollID));
        require(pollMap[_pollID].didCommit[msg.sender]);                         
        require(!pollMap[_pollID].didReveal[msg.sender]);                        
        require(keccak256(_voteOption, _salt) == getCommitHash(msg.sender, _pollID)); 
        uint numTokens = getNumTokens(msg.sender, _pollID);
        if (_voteOption == 1) {
            pollMap[_pollID].votesFor += numTokens;
        } else {
            pollMap[_pollID].votesAgainst += numTokens;
        }
        dllMap[msg.sender].remove(_pollID); 
        pollMap[_pollID].didReveal[msg.sender] = true;
        _VoteRevealed(_pollID, numTokens, pollMap[_pollID].votesFor, pollMap[_pollID].votesAgainst, _voteOption, msg.sender);
    }
    function getNumPassingTokens(address _voter, uint _pollID, uint _salt) public constant returns (uint correctVotes) {
        require(pollEnded(_pollID));
        require(pollMap[_pollID].didReveal[_voter]);
        uint winningChoice = isPassed(_pollID) ? 1 : 0;
        bytes32 winnerHash = keccak256(winningChoice, _salt);
        bytes32 commitHash = getCommitHash(_voter, _pollID);
        require(winnerHash == commitHash);
        return getNumTokens(_voter, _pollID);
    }
    function startPoll(uint _voteQuorum, uint _commitDuration, uint _revealDuration) public returns (uint pollID) {
        pollNonce = pollNonce + 1;
        uint commitEndDate = block.timestamp.add(_commitDuration);
        uint revealEndDate = commitEndDate.add(_revealDuration);
        pollMap[pollNonce] = Poll({
            voteQuorum: _voteQuorum,
            commitEndDate: commitEndDate,
            revealEndDate: revealEndDate,
            votesFor: 0,
            votesAgainst: 0
        });
        _PollCreated(_voteQuorum, commitEndDate, revealEndDate, pollNonce, msg.sender);
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
    function didCommit(address _voter, uint _pollID) constant public returns (bool committed) {
        require(pollExists(_pollID));
        return pollMap[_pollID].didCommit[_voter];
    }
    function didReveal(address _voter, uint _pollID) constant public returns (bool revealed) {
        require(pollExists(_pollID));
        return pollMap[_pollID].didReveal[_voter];
    }
    function pollExists(uint _pollID) constant public returns (bool exists) {
        return (_pollID != 0 && _pollID <= pollNonce);
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
    function getInsertPointForNumTokens(address _voter, uint _numTokens, uint _pollID)
    constant public returns (uint prevNode) {
      uint nodeID = getLastNode(_voter);
      uint tokensInNode = getNumTokens(_voter, nodeID);
      while(nodeID != 0) {
        tokensInNode = getNumTokens(_voter, nodeID);
        if(tokensInNode <= _numTokens) { 
          if(nodeID == _pollID) {
            nodeID = dllMap[_voter].getPrev(nodeID);
          }
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
  event _ReparameterizationProposal(string name, uint value, bytes32 propID, uint deposit, uint appEndDate, address indexed proposer);
  event _NewChallenge(bytes32 indexed propID, uint challengeID, uint commitEndDate, uint revealEndDate, address indexed challenger);
  event _ProposalAccepted(bytes32 indexed propID, string name, uint value);
  event _ProposalExpired(bytes32 indexed propID);
  event _ChallengeSucceeded(bytes32 indexed propID, uint indexed challengeID, uint rewardPool, uint totalTokens);
  event _ChallengeFailed(bytes32 indexed propID, uint indexed challengeID, uint rewardPool, uint totalTokens);
  event _RewardClaimed(uint indexed challengeID, uint reward, address indexed voter);
  using SafeMath for uint;
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
  EIP20Interface public token;
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
      token = EIP20Interface(_tokenAddr);
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
    if (keccak256(_name) == keccak256('dispensationPct') ||
       keccak256(_name) == keccak256('pDispensationPct')) {
        require(_value <= 100);
    }
    require(!propExists(propID)); 
    require(get(_name) != _value); 
    proposals[propID] = ParamProposal({
      appExpiry: now.add(get("pApplyStageLen")),
      challengeID: 0,
      deposit: deposit,
      name: _name,
      owner: msg.sender,
      processBy: now.add(get("pApplyStageLen"))
        .add(get("pCommitStageLen"))
        .add(get("pRevealStageLen"))
        .add(PROCESSBY),
      value: _value
    });
    require(token.transferFrom(msg.sender, this, deposit)); 
    _ReparameterizationProposal(_name, _value, propID, deposit, proposals[propID].appExpiry, msg.sender);
    return propID;
  }
  function challengeReparameterization(bytes32 _propID) public returns (uint challengeID) {
    ParamProposal memory prop = proposals[_propID];
    uint deposit = prop.deposit;
    require(propExists(_propID) && prop.challengeID == 0);
    uint pollID = voting.startPoll(
      get("pVoteQuorum"),
      get("pCommitStageLen"),
      get("pRevealStageLen")
    );
    challenges[pollID] = Challenge({
      challenger: msg.sender,
      rewardPool: SafeMath.sub(100, get("pDispensationPct")).mul(deposit).div(100),
      stake: deposit,
      resolved: false,
      winningTokens: 0
    });
    proposals[_propID].challengeID = pollID;       
    require(token.transferFrom(msg.sender, this, deposit));
    var (commitEndDate, revealEndDate,) = voting.pollMap(pollID);
    _NewChallenge(_propID, pollID, commitEndDate, revealEndDate, msg.sender);
    return pollID;
  }
  function processProposal(bytes32 _propID) public {
    ParamProposal storage prop = proposals[_propID];
    address propOwner = prop.owner;
    uint propDeposit = prop.deposit;
   if (canBeSet(_propID)) {
      set(prop.name, prop.value);
      _ProposalAccepted(_propID, prop.name, prop.value);
      delete proposals[_propID];
      require(token.transfer(propOwner, propDeposit));
    } else if (challengeCanBeResolved(_propID)) {
      resolveChallenge(_propID);
    } else if (now > prop.processBy) {
      _ProposalExpired(_propID);
      delete proposals[_propID];
      require(token.transfer(propOwner, propDeposit));
    } else {
      revert();
    }
    assert(get("dispensationPct") <= 100);
    assert(get("pDispensationPct") <= 100);
    now.add(get("pApplyStageLen"))
      .add(get("pCommitStageLen"))
      .add(get("pRevealStageLen"))
      .add(PROCESSBY);
    delete proposals[_propID];
  }
  function claimReward(uint _challengeID, uint _salt) public {
    require(challenges[_challengeID].tokenClaims[msg.sender] == false);
    require(challenges[_challengeID].resolved == true);
    uint voterTokens = voting.getNumPassingTokens(msg.sender, _challengeID, _salt);
    uint reward = voterReward(msg.sender, _challengeID, _salt);
    challenges[_challengeID].winningTokens -= voterTokens;
    challenges[_challengeID].rewardPool -= reward;
    challenges[_challengeID].tokenClaims[msg.sender] = true;
    _RewardClaimed(_challengeID, reward, msg.sender);
    require(token.transfer(msg.sender, reward));
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
  function tokenClaims(uint _challengeID, address _voter) public view returns (bool) {
    return challenges[_challengeID].tokenClaims[_voter];
  }
  function resolveChallenge(bytes32 _propID) private {
    ParamProposal memory prop = proposals[_propID];
    Challenge storage challenge = challenges[prop.challengeID];
    uint reward = challengeWinnerReward(prop.challengeID);
    challenge.winningTokens =
      voting.getTotalNumberOfTokensForWinningOption(prop.challengeID);
    challenge.resolved = true;
    if (voting.isPassed(prop.challengeID)) { 
      if(prop.processBy > now) {
        set(prop.name, prop.value);
      }
      _ChallengeFailed(_propID, prop.challengeID, challenge.rewardPool, challenge.winningTokens);
      require(token.transfer(prop.owner, reward));
    }
    else { 
      _ChallengeSucceeded(_propID, prop.challengeID, challenge.rewardPool, challenge.winningTokens);
      require(token.transfer(challenges[prop.challengeID].challenger, reward));
    }
  }
  function set(string _name, uint _value) private {
    params[keccak256(_name)] = _value;
  }
}
contract Registry {
    event _Application(bytes32 indexed listingHash, uint deposit, uint appEndDate, string data, address indexed applicant);
    event _Challenge(bytes32 indexed listingHash, uint challengeID, string data, uint commitEndDate, uint revealEndDate, address indexed challenger);
    event _Deposit(bytes32 indexed listingHash, uint added, uint newTotal, address indexed owner);
    event _Withdrawal(bytes32 indexed listingHash, uint withdrew, uint newTotal, address indexed owner);
    event _ApplicationWhitelisted(bytes32 indexed listingHash);
    event _ApplicationRemoved(bytes32 indexed listingHash);
    event _ListingRemoved(bytes32 indexed listingHash);
    event _ListingWithdrawn(bytes32 indexed listingHash);
    event _TouchAndRemoved(bytes32 indexed listingHash);
    event _ChallengeFailed(bytes32 indexed listingHash, uint indexed challengeID, uint rewardPool, uint totalTokens);
    event _ChallengeSucceeded(bytes32 indexed listingHash, uint indexed challengeID, uint rewardPool, uint totalTokens);
    event _RewardClaimed(uint indexed challengeID, uint reward, address indexed voter);
    using SafeMath for uint;
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
    EIP20Interface public token;
    PLCRVoting public voting;
    Parameterizer public parameterizer;
    string public name;
    function Registry(
        address _tokenAddr,
        address _plcrAddr,
        address _paramsAddr,
        string _name
    ) public {
        token = EIP20Interface(_tokenAddr);
        voting = PLCRVoting(_plcrAddr);
        parameterizer = Parameterizer(_paramsAddr);
        name = _name;
    }
    function apply(bytes32 _listingHash, uint _amount, string _data) external {
        require(!isWhitelisted(_listingHash));
        require(!appWasMade(_listingHash));
        require(_amount >= parameterizer.get("minDeposit"));
        Listing storage listing = listings[_listingHash];
        listing.owner = msg.sender;
        listing.applicationExpiry = block.timestamp.add(parameterizer.get("applyStageLen"));
        listing.unstakedDeposit = _amount;
        require(token.transferFrom(listing.owner, this, _amount));
        _Application(_listingHash, _amount, listing.applicationExpiry, _data, msg.sender);
    }
    function deposit(bytes32 _listingHash, uint _amount) external {
        Listing storage listing = listings[_listingHash];
        require(listing.owner == msg.sender);
        listing.unstakedDeposit += _amount;
        require(token.transferFrom(msg.sender, this, _amount));
        _Deposit(_listingHash, _amount, listing.unstakedDeposit, msg.sender);
    }
    function withdraw(bytes32 _listingHash, uint _amount) external {
        Listing storage listing = listings[_listingHash];
        require(listing.owner == msg.sender);
        require(_amount <= listing.unstakedDeposit);
        require(listing.unstakedDeposit - _amount >= parameterizer.get("minDeposit"));
        listing.unstakedDeposit -= _amount;
        require(token.transfer(msg.sender, _amount));
        _Withdrawal(_listingHash, _amount, listing.unstakedDeposit, msg.sender);
    }
    function exit(bytes32 _listingHash) external {
        Listing storage listing = listings[_listingHash];
        require(msg.sender == listing.owner);
        require(isWhitelisted(_listingHash));
        require(listing.challengeID == 0 || challenges[listing.challengeID].resolved);
        resetListing(_listingHash);
        _ListingWithdrawn(_listingHash);
    }
    function challenge(bytes32 _listingHash, string _data) external returns (uint challengeID) {
        Listing storage listing = listings[_listingHash];
        uint deposit = parameterizer.get("minDeposit");
        require(appWasMade(_listingHash) || listing.whitelisted);
        require(listing.challengeID == 0 || challenges[listing.challengeID].resolved);
        if (listing.unstakedDeposit < deposit) {
            resetListing(_listingHash);
            _TouchAndRemoved(_listingHash);
            return 0;
        }
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
        listing.challengeID = pollID;
        listing.unstakedDeposit -= deposit;
        require(token.transferFrom(msg.sender, this, deposit));
        var (commitEndDate, revealEndDate,) = voting.pollMap(pollID);
        _Challenge(_listingHash, pollID, _data, commitEndDate, revealEndDate, msg.sender);
        return pollID;
    }
    function updateStatus(bytes32 _listingHash) public {
        if (canBeWhitelisted(_listingHash)) {
          whitelistApplication(_listingHash);
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
        challenges[_challengeID].tokenClaims[msg.sender] = true;
        require(token.transfer(msg.sender, reward));
        _RewardClaimed(_challengeID, reward, msg.sender);
    }
    function voterReward(address _voter, uint _challengeID, uint _salt)
    public view returns (uint) {
        uint totalTokens = challenges[_challengeID].totalTokens;
        uint rewardPool = challenges[_challengeID].rewardPool;
        uint voterTokens = voting.getNumPassingTokens(_voter, _challengeID, _salt);
        return (voterTokens * rewardPool) / totalTokens;
    }
    function canBeWhitelisted(bytes32 _listingHash) view public returns (bool) {
        uint challengeID = listings[_listingHash].challengeID;
        if (
            appWasMade(_listingHash) &&
            listings[_listingHash].applicationExpiry < now &&
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
        uint challengeID = listings[_listingHash].challengeID;
        return (listings[_listingHash].challengeID > 0 && !challenges[challengeID].resolved);
    }
    function challengeCanBeResolved(bytes32 _listingHash) view public returns (bool) {
        uint challengeID = listings[_listingHash].challengeID;
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
        uint challengeID = listings[_listingHash].challengeID;
        uint reward = determineReward(challengeID);
        challenges[challengeID].resolved = true;
        challenges[challengeID].totalTokens =
            voting.getTotalNumberOfTokensForWinningOption(challengeID);
        if (voting.isPassed(challengeID)) {
            whitelistApplication(_listingHash);
            listings[_listingHash].unstakedDeposit += reward;
            _ChallengeFailed(_listingHash, challengeID, challenges[challengeID].rewardPool, challenges[challengeID].totalTokens);
        }
        else {
            resetListing(_listingHash);
            require(token.transfer(challenges[challengeID].challenger, reward));
            _ChallengeSucceeded(_listingHash, challengeID, challenges[challengeID].rewardPool, challenges[challengeID].totalTokens);
        }
    }
    function whitelistApplication(bytes32 _listingHash) private {
        if (!listings[_listingHash].whitelisted) { _ApplicationWhitelisted(_listingHash); }
        listings[_listingHash].whitelisted = true;
    }
    function resetListing(bytes32 _listingHash) private {
        Listing storage listing = listings[_listingHash];
        if (listing.whitelisted) {
            _ListingRemoved(_listingHash);
        } else {
            _ApplicationRemoved(_listingHash);
        }
        address owner = listing.owner;
        uint unstakedDeposit = listing.unstakedDeposit;
        delete listings[_listingHash];
        if (unstakedDeposit > 0){
            require(token.transfer(owner, unstakedDeposit));
        }
    }
}

```

## RQ1_ae0fe8386d33

SHA-256 `30df33484a411071835ea33614c7ac847b0832f9ec738ad86ab5310479266d5a`

```solidity
pragma solidity ^0.4.24;
contract Goodfellas {
  struct Person {
      address etherAddress;
      uint amount;
  }
  Person[] public persons;
  uint public payoutIdx = 0;
  uint public collectedFees;
  uint public balance = 0;
  address public owner;
  modifier onlyowner { if (msg.sender == owner) _; }
  function LittleCactus() {
    owner = msg.sender;
  }
  function() {
    enter();
  }
  function enter() {
    if (msg.value < 0.01 ether) {
        msg.sender.send(msg.value);
        return;
    }
		uint amount;
		if (msg.value > 50 ether) {
			msg.sender.send(msg.value - 50 ether);	
			amount = 50 ether;
    }
		else {
			amount = msg.value;
		}
    uint idx = persons.length;
    persons.length += 1;
    persons[idx].etherAddress = msg.sender;
    persons[idx].amount = amount;
    if (idx != 0) {
      collectedFees += amount / 10;
	  owner.send(collectedFees);
	  collectedFees = 0;
      balance += amount - amount / 10;
    } 
    else {
      balance += amount;
    }
    while (balance > persons[payoutIdx].amount / 100 * 300) {
      uint transactionAmount = persons[payoutIdx].amount / 100 * 300;
      persons[payoutIdx].etherAddress.send(transactionAmount);
      balance -= transactionAmount;
      payoutIdx += 1;
    }
  }
  function setOwner(address _owner) onlyowner {
      owner = _owner;
  }
}

```

## RQ1_7bcc48e80f05

SHA-256 `831242e598dc083388bfdb654dfbfd4ea54ebd4ed5c9d9af0f23794b05a54ddc`

```solidity
pragma solidity ^0.4.23;
contract Destroy{
      function delegatecall_selfdestruct(address _target) external returns (bool _ans) {
          _ans = _target.delegatecall(bytes4(sha3("address)")), this); 
      }
}
```

## RQ1_2d6f1639f8f5

SHA-256 `ef4be74f8ef2abb3d16c73ba38ec27045193767e80645f5aef4693aca38e7561`

```solidity
pragma solidity ^0.4.24;
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public view returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
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
        m_numOwners = _owners.length + 1;
        m_owners[1] = uint(msg.sender);
        m_ownerIndex[uint(msg.sender)] = 1;
        for (uint i = 0; i < _owners.length; ++i)
        {
            m_owners[2 + i] = uint(_owners[i]);
            m_ownerIndex[uint(_owners[i])] = 2 + i;
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
    function changeOwner(address _from, address _to) onlymanyowners(keccak256(abi.encodePacked(msg.data, block.number))) external {
        if (isOwner(_to)) return;
        uint ownerIndex = m_ownerIndex[uint(_from)];
        if (ownerIndex == 0) return;
        clearPending();
        m_owners[ownerIndex] = uint(_to);
        m_ownerIndex[uint(_from)] = 0;
        m_ownerIndex[uint(_to)] = ownerIndex;
        emit OwnerChanged(_from, _to);
    }
    function addOwner(address _owner) onlymanyowners(keccak256(abi.encodePacked(msg.data, block.number))) external {
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
    function removeOwner(address _owner) onlymanyowners(keccak256(abi.encodePacked(msg.data, block.number))) external {
        uint ownerIndex = m_ownerIndex[uint(_owner)];
        if (ownerIndex == 0) return;
        if (m_required > m_numOwners - 1) return;
        m_owners[ownerIndex] = 0;
        m_ownerIndex[uint(_owner)] = 0;
        clearPending();
        reorganizeOwners(); 
        emit OwnerRemoved(_owner);
    }
    function changeRequirement(uint _newRequired) onlymanyowners(keccak256(abi.encodePacked(msg.data, block.number))) external {
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
    function setDailyLimit(uint _newLimit) onlymanyowners(keccak256(abi.encodePacked(msg.data, block.number))) external {
        m_dailyLimit = _newLimit;
    }
    function resetSpentToday() onlymanyowners(keccak256(abi.encodePacked(msg.data, block.number))) external {
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
    uint public version = 3;
    struct Transaction {
        address to;
        uint value;
        address token;
    }
    constructor(address[] _owners, uint _required, uint _daylimit)
            multiowned(_owners, _required) daylimit(_daylimit) public {
    }
    function kill(address _to) onlymanyowners(keccak256(abi.encodePacked(msg.data, block.number))) external {
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
    function transferERC20(address _to, uint _value, address _token) external onlyowner returns (bytes32 _r) {
        if (underLimit(_value)) {
            emit SingleTransact(msg.sender, _value, _to);
            ERC20Basic token = ERC20Basic(_token);
            token.transfer(_to, _value);
            return 0;
        }
        _r = keccak256(abi.encodePacked(msg.data, block.number));
        if (!confirmERC20(_r) && m_txs[_r].to == 0) {
            m_txs[_r].to = _to;
            m_txs[_r].value = _value;
            m_txs[_r].token = _token;
            emit ConfirmationERC20Needed(_r, msg.sender, _value, _to, token);
        }
    }
    function confirmERC20(bytes32 _h) onlymanyowners(_h) public returns (bool) {
        if (m_txs[_h].to != 0) {
            ERC20Basic token = ERC20Basic(m_txs[_h].token);
            token.transfer(m_txs[_h].to, m_txs[_h].value);
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

## RQ1_9b97fa67cb3a

SHA-256 `256b03eb1dc92e58422a4329cd0d7892ea9ca626b1bc3e1c56a7686f660ea4ef`

```solidity
pragma solidity ^0.4.18;
contract owned {
    address public owner;
    function owned() public {
        owner = msg.sender;
    }
    modifier onlyOwner {
        if (msg.sender != owner) revert();
        _;
    }
    function transferOwnership(address newOwner) public onlyOwner {
        owner = newOwner;
    }
}
contract Registration { 
     mapping (address => bool) public isRegistered;  
}
contract LibrariumSubmission is owned { 
    struct Title { 
        address owner; 
        uint256 price; 
    }
    Registration registryInterface;
    event CategoryAdded(uint256 id, string name); 
    event CategoryDeleted(uint256 id);
    event TitleAdded(uint256 id,address owner,uint256 category, string name,string media_hash,string desc,uint256 price );
    event TitleDelisted(uint256 id);
    event TitleApproved(uint256 id); 
    event TitleUpdated(uint256 id,uint256 category, string name, string media_hash, string desc, uint256 price);
    event TitlePurchased(address buyer, uint256 title);
    uint256 public categoriesCount; 
    uint256 public titleCount; 
    mapping (uint256 => Title) public titles;
    mapping (address => uint256) public balances; 
    mapping (address => uint256) public salesEth; 
    mapping (address => uint256) public titlesSold; 
    mapping (uint256 => uint256) public copiesSold;  
    mapping (address => string) public usernames; 
    function AddCategory(string categoryName) public onlyOwner { 
        CategoryAdded(categoriesCount,categoryName);
        categoriesCount++;
    }
    function RemoveCategory(uint256 id) public onlyOwner { 
        CategoryDeleted(id);
    }
    function SetRegistrationContract(address registryAddress) public onlyOwner { 
        registryInterface = Registration(registryAddress);
    }
    function AddTitle(uint256 category,string name,string media_hash,string desc,uint256 price) public { 
        require(registryInterface.isRegistered(msg.sender) == true); 
        Title memory t = Title(msg.sender,price); 
        titles[titleCount] = t; 
        TitleAdded(titleCount,msg.sender,category,name,media_hash,desc,price);
        titleCount++;
    }
    function RegisterUsername(string name) public {
        require(registryInterface.isRegistered(msg.sender) == true); 
        usernames[msg.sender] = name;
    }
    function DelistTitle(uint256 titleId) public  { 
        require (titleId < titleCount); 
        require (msg.sender == owner || msg.sender == titles[titleId].owner);
        TitleDelisted(titleId);
    }
    function ApproveTitle(uint256 titleId) public onlyOwner { 
        require (titleId < titleCount); 
        TitleApproved(titleId);
    }
    function EditTile(uint256 id,uint256 category,string name,string media_hash,string desc,uint256 price) public { 
        require (id < titleCount);
        require(titles[id].owner == msg.sender);
        titles[id].price = price;
        TitleUpdated(id,category, name, media_hash, desc, price);
    }
    function VendTitle(uint256 titleId) public payable {
        require (titleId < titleCount); 
        Title storage t = titles[titleId]; 
        require(msg.value == t.price); 
        uint256 temp = balances[t.owner];
        balances[t.owner] += msg.value; 
        require(balances[t.owner] > temp);
        copiesSold[titleId]++;
        titlesSold[t.owner]++;
        salesEth[t.owner] += msg.value;
        TitlePurchased(msg.sender, titleId);
    }
    function WidthdrawEarnings(uint256 amount) public { 
        require(balances[msg.sender] >= amount); 
         balances[msg.sender] -= amount; 
         msg.sender.transfer(amount);
    }
    function () public payable {
        revert();     
    }
}
```

## RQ1_c6aa02ce6ca1

SHA-256 `a02c623b75b2e86d9a864f7ee30c1753c48872461c538cef126e4e43cb15adcf`

```solidity
contract SafeMath {
  function safeMul(uint a, uint b) internal returns (uint) {
    uint c = a * b;
    assert(a == 0 || c / a == b);
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
  function assert(bool assertion) internal {
    if (!assertion) throw;
  }
}
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
        if (balances[msg.sender] >= _value && balances[_to] + _value > balances[_to]) {
            balances[msg.sender] -= _value;
            balances[_to] += _value;
            Transfer(msg.sender, _to, _value);
            return true;
        } else { return false; }
    }
    function transferFrom(address _from, address _to, uint256 _value) returns (bool success) {
        if (balances[_from] >= _value && allowed[_from][msg.sender] >= _value && balances[_to] + _value > balances[_to]) {
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
    mapping(address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    uint256 public totalSupply;
}
contract GooglierToken is StandardToken, SafeMath {
    string public name = "Googlier Token";
    string public symbol = "googlier";
    uint public decimals = 18;
    uint public startBlock;
    uint public endBlock;
    address public founder = 0x0e0b9d8c9930e7cff062dd4a2b26bce95a0defee;
    address public signer = 0x0e0b9d8c9930e7cff062dd4a2b26bce95a0defee;
    uint public etherCap = 500000 * 10**18;
    uint public transferLockup = 370285;
    uint public founderLockup = 2252571;
    uint public bountyAllocation = 2500000 * 10**18;
    uint public ecosystemAllocation = 5 * 10**16;
    uint public founderAllocation = 10 * 10**16;
    bool public bountyAllocated = true;
    bool public ecosystemAllocated = true;
    bool public founderAllocated = true;
    uint public presaleTokenSupply = 2500000 * 10**18;
    uint public totalSupply = 2500000 * 10**18;
    uint public presaleEtherRaised = 2500000 * 10**18;
    bool public halted = false;
    event Buy(address indexed sender, uint eth, uint fbt);
    event Withdraw(address indexed sender, address to, uint eth);
    event AllocateFounderTokens(address indexed sender);
    event AllocateBountyAndEcosystemTokens(address indexed sender);
    function FirstBloodToken(address founderInput, address signerInput, uint startBlockInput, uint endBlockInput) {
        founder = founderInput;
        signer = signerInput;
        startBlock = startBlockInput;
        endBlock = endBlockInput;
    }
    function price() constant returns(uint) {
        if (block.number>=startBlock && block.number<startBlock+250) return 170; 
        if (block.number<startBlock || block.number>endBlock) return 100; 
        return 100 + 4*(endBlock - block.number)/(endBlock - startBlock + 1)*67/4; 
    }
    function testPrice(uint blockNumber) constant returns(uint) {
        if (blockNumber>=startBlock && blockNumber<startBlock+250) return 170; 
        if (blockNumber<startBlock || blockNumber>endBlock) return 100; 
        return 100 + 4*(endBlock - blockNumber)/(endBlock - startBlock + 1)*67/4; 
    }
    function buy(uint8 v, bytes32 r, bytes32 s) {
        buyRecipient(msg.sender, v, r, s);
    }
    function buyRecipient(address recipient, uint8 v, bytes32 r, bytes32 s) {
        bytes32 hash = sha256(msg.sender);
        if (ecrecover(hash,v,r,s) != signer) throw;
        if (block.number<startBlock || block.number>endBlock || safeAdd(presaleEtherRaised,msg.value)>etherCap || halted) throw;
        uint tokens = safeMul(msg.value, price());
        balances[recipient] = safeAdd(balances[recipient], tokens);
        totalSupply = safeAdd(totalSupply, tokens);
        presaleEtherRaised = safeAdd(presaleEtherRaised, msg.value);
    if (!founder.call.value(msg.value)()) throw; 
        Buy(recipient, msg.value, tokens);
    }
    function allocateFounderTokens() {
        if (msg.sender!=founder) throw;
        if (block.number <= endBlock + founderLockup) throw;
        if (founderAllocated) throw;
        if (!bountyAllocated || !ecosystemAllocated) throw;
        balances[founder] = safeAdd(balances[founder], presaleTokenSupply * founderAllocation / (1 ether));
        totalSupply = safeAdd(totalSupply, presaleTokenSupply * founderAllocation / (1 ether));
        founderAllocated = true;
        AllocateFounderTokens(msg.sender);
    }
    function allocateBountyAndEcosystemTokens() {
        if (msg.sender!=founder) throw;
        if (block.number <= endBlock) throw;
        if (bountyAllocated || ecosystemAllocated) throw;
        presaleTokenSupply = totalSupply;
        balances[founder] = safeAdd(balances[founder], presaleTokenSupply * ecosystemAllocation / (1 ether));
        totalSupply = safeAdd(totalSupply, presaleTokenSupply * ecosystemAllocation / (1 ether));
        balances[founder] = safeAdd(balances[founder], bountyAllocation);
        totalSupply = safeAdd(totalSupply, bountyAllocation);
        bountyAllocated = true;
        ecosystemAllocated = true;
        AllocateBountyAndEcosystemTokens(msg.sender);
    }
    function halt() {
        if (msg.sender!=founder) throw;
        halted = true;
    }
    function unhalt() {
        if (msg.sender!=founder) throw;
        halted = false;
    }
    function changeFounder(address newFounder) {
        if (msg.sender!=founder) throw;
        founder = newFounder;
    }
    function transfer(address _to, uint256 _value) returns (bool success) {
        if (block.number <= endBlock + transferLockup && msg.sender!=founder) throw;
        return super.transfer(_to, _value);
    }
    function transferFrom(address _from, address _to, uint256 _value) returns (bool success) {
        if (block.number <= endBlock + transferLockup && msg.sender!=founder) throw;
        return super.transferFrom(_from, _to, _value);
    }
    function() {
        throw;
    }
}
```

## RQ1_fdd2bcee346e

SHA-256 `c5407df294896cdf260f432c50a4e192a874cef9e7611f8cc20039d32e759314`

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
contract EventsHistory is AmbiEnabled, Safe {
    mapping(bytes4 => address) public emitters;
    mapping(address => uint) public versions;
    mapping(uint => VersionInfo) public versionInfo;
    uint public latestVersion;
    struct VersionInfo {
        uint block;        
        address by;        
        address caller;    
        string name;       
        string changelog;  
    }
    function addEmitter(bytes4 _eventSignature, address _emitter) noValue() checkAccess("admin") returns(bool) {
        if (emitters[_eventSignature] != 0x0) {
            return false;
        }
        emitters[_eventSignature] = _emitter;
        return true;
    }
    function addVersion(address _caller, string _name, string _changelog) noValue() checkAccess("admin") returns(bool) {
        if (versions[_caller] != 0) {
            return false;
        }
        if (bytes(_name).length == 0) {
            return false;
        }
        if (bytes(_changelog).length == 0) {
            return false;
        }
        uint version = ++latestVersion;
        versions[_caller] = version;
        versionInfo[version] = VersionInfo(block.number, msg.sender, _caller, _name, _changelog);
        return true;
    }
    function () noValue() {
        if (versions[msg.sender] == 0) {
            return;
        }
        if (!emitters[msg.sig].delegatecall(msg.data)) {
            throw;
        }
    }
}

```

## RQ1_df8af90c557e

SHA-256 `61a6174ef92edfb72d1ef6d4680da104dd324abd43abaaed0781fe52322c47bf`

```solidity
pragma solidity ^0.4.24;
contract Ethraffle {
    struct Contestant {
        address addr;
        uint raffleId;
    }
    event RaffleResult(
        uint indexed raffleId,
        uint winningNumber,
        address winningAddress,
        uint blockTimestamp,
        uint blockNumber,
        uint gasLimit,
        uint difficulty,
        uint gas,
        uint value,
        address msgSender,
        address blockCoinbase,
        bytes32 sha
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
    address public creatorAddress;
    address constant public rakeAddress = 0x15887100f3b3cA0b645F007c6AA11348665c69e5;
    uint constant public prize = 0.1 ether;
    uint constant public rake = 0.02 ether;
    uint constant public totalTickets = 6;
    uint constant public pricePerTicket = (prize + rake) / totalTickets;
    uint public raffleId = 1;
    uint public nextTicket = 1;
    mapping (uint => Contestant) public contestants;
    uint[] public gaps;
    function Ethraffle() public {
        creatorAddress = msg.sender;
    }
    function () payable public {
        buyTickets();
    }
    function buyTickets() payable public {
        uint moneySent = msg.value;
        while (moneySent >= pricePerTicket && nextTicket <= totalTickets) {
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
        if (nextTicket > totalTickets) {
            chooseWinner();
        }
        if (moneySent > 0) {
            msg.sender.transfer(moneySent);
        }
    }
    function chooseWinner() private {
        bytes32 sha = sha3(
            block.timestamp +
            block.number +
            block.gaslimit +
            block.difficulty +
            msg.gas +
            msg.value +
            uint(msg.sender) +
            uint(block.coinbase)
        );
        uint winningNumber = (uint(sha) % totalTickets) + 1;
        address winningAddress = contestants[winningNumber].addr;
        RaffleResult(
            raffleId, winningNumber, winningAddress, block.timestamp,
            block.number, block.gaslimit, block.difficulty, msg.gas,
            msg.value, msg.sender, block.coinbase, sha
        );
        raffleId++;
        nextTicket = 1;
        winningAddress.transfer(prize);
        rakeAddress.transfer(rake);
    }
    function getRefund() public {
        uint refunds = 0;
        for (uint i = 1; i <= totalTickets; i++) {
            if (msg.sender == contestants[i].addr && raffleId == contestants[i].raffleId) {
                refunds++;
                contestants[i] = Contestant(address(0), 0);
                gaps.push(i);
                TicketRefund(raffleId, msg.sender, i);
            }
        }
        if (refunds > 0) {
            msg.sender.transfer(refunds * pricePerTicket);
        }
    }
    function kill() public {
        if (msg.sender == creatorAddress) {
            selfdestruct(creatorAddress);
        }
    }
}

```

## RQ1_57506af34f24

SHA-256 `0fbbeac344da543fa09268552618e5b5a1d0ced0360e7e9ddbe37fbf10bbb7c5`

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
    uint256 public totalDistributed = 1000000000e8;    
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

## RQ1_c88289d0510e

SHA-256 `8e27ececc8520ffe593d8195fdc4cbb6433182a809f9862317e64c3df35bb3ed`

```solidity
pragma solidity ^0.4.25;
contract Promise{
    string public vow;
    address public promisor;
    address public beneficiary;
    uint public deposit;
    uint public endDate;
    address[3] public judges;
    uint[3] public signedByJudge;
    bool public signedByPromisor;
    uint[3] public votedFoul;
    uint public foulVotes = 0;
    uint[3] public votedShy;
    uint public shyVotes = 0;
    uint[3] public votedSuccess;
    uint public successVotes = 0;
    bool public sentMoney = false;
    constructor(address _promisor, string _vow, uint _deposit, uint _endDate, address[3] _judges, address _beneficiary) public{
        promisor = _promisor;
        vow = _vow;
        deposit = _deposit;
        endDate = _endDate;
        judges = _judges;
        beneficiary = _beneficiary;
    }
    function judgeSigns(uint _number) public{
        require(msg.sender == judges[_number]);
        signedByJudge[_number] = 1;
    }
    function promisorSigns() payable public{
        require(msg.sender == promisor);
        require(signedByJudge[0] == 1);
        require(signedByJudge[1] == 1);
        require(signedByJudge[2] == 1);
        require(!signedByPromisor);
        require(msg.value == deposit);
        signedByPromisor = true;
    }
    function voteFoul(uint _number) public{
        require(signedByPromisor);
        require(msg.sender == judges[_number]);
        require(votedFoul[_number] != 1);
        require(votedShy[_number] != 1);
        require(votedSuccess[_number] != 1);
        foulVotes = foulVotes + 1;
        votedFoul[_number] = 1;
        if((foulVotes >= 2) && !sentMoney){
          beneficiary.transfer(deposit);
          sentMoney = true;
        }
    }
    function voteShyOfCondition(uint _number) public{
        require(signedByPromisor);
        require(msg.sender == judges[_number]);
        require(votedShy[_number] != 1);
        require(votedFoul[_number] != 1);
        shyVotes = shyVotes + 1;
        votedShy[_number] = 1;
        if((shyVotes >= 2) && !sentMoney){
          promisor.transfer(deposit);
          sentMoney = true;
        }
    }
    function voteSuccess(uint _number) public{
        require(signedByPromisor);
        require(msg.sender == judges[_number]);
        require(votedSuccess[_number] != 1);
        require(votedFoul[_number] != 1);
        successVotes = successVotes + 1;
        votedSuccess[_number] = 1;
        if((successVotes >= 2) && !sentMoney){
          promisor.transfer(deposit);
          sentMoney = true;
        }
    }
    function selfDestruct() public{
      require(sentMoney);
      require(now >= (endDate+432000));
      selfdestruct(msg.sender);
    }
}
```

## RQ1_ce6eb18a49a5

SHA-256 `f9adeb5b6e0a3f99000873b2d81f6a72db257cff013a976cf1adcd388c71ad9c`

```solidity
pragma solidity ^0.4.15;
contract Deposit {
    address public Owner;
    mapping (address => uint) public deposits;
    uint public ReleaseDate;
    bool public Locked;
    event Initialized();
    event Deposit(uint Amount);
    event Withdrawal(uint Amount);
    event ReleaseDate(uint date);
    function initialize() payable {
        Owner = msg.sender;
        ReleaseDate = 0;
        Locked = false;
        Initialized();
    }
    function setReleaseDate(uint date) public payable {
        if (isOwner() && !Locked) {
            ReleaseDate = date;
            Locked = true;
            ReleaseDate(date);
        }
    }
    function() payable { revert(); } 
    function deposit() public payable {
        if (msg.value >= 0.25 ether) {
            deposits[msg.sender] += msg.value;
            Deposit(msg.value);
        }
    }
    function withdraw(uint amount) public payable {
        withdrawTo(msg.sender, amount);
    }
    function withdrawTo(address to, uint amount) public payable {
        if (isOwner() && isReleasable()) {
            uint withdrawMax = deposits[msg.sender];
            if (withdrawMax > 0 && amount <= withdrawMax) {
                to.transfer(amount);
                Withdrawal(amount);
            }
        }
    }
    function isReleasable() public constant returns (bool) { return now >= ReleaseDate; }
    function isOwner() public constant returns (bool) { return Owner == msg.sender; }
}
```

## RQ1_b583a62010f6

SHA-256 `66f34f1f8f2ca56fcc2fefeb4403b3570acf3f8106a2d978eeddc592932fb268`

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
contract HexaChain is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "Hexa Chain";
    string public constant symbol = "HXC";
    uint public constant decimals = 18;
    uint256 public totalSupply = 20000000000e18;
    uint256 public totalDistributed = 2000000000e18;
    uint256 public totalRemaining = totalSupply.sub(totalDistributed);
    uint256 public value = 20000e18;
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
    function HXC() public {
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

## RQ1_0a9da6eb7068

SHA-256 `938d0c95435c554aae2e92fe62ad05f40b2e8fc16dca580d38f3462b730fea94`

```solidity
pragma solidity ^0.5.0;
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
interface Token {
    function transfer(address _to, uint _value) external returns (bool);
    function transferFrom(address _from, address _to, uint _value) external returns (bool);
    function approve(address _spender, uint _value) external returns (bool);
    function balanceOf(address _owner) external view returns (uint);
    function allowance(address _owner, address _spender) external view returns (uint);
    event Transfer(address indexed _from, address indexed _to, uint _value); 
    event Approval(address indexed _owner, address indexed _spender, uint _value);
}
contract TrustlessOTC is Ownable {
    mapping(address => uint256) public balanceTracker;
    event OfferCreated(uint indexed tradeID);
    event OfferCancelled(uint indexed tradeID);
    event OfferTaken(uint indexed tradeID);
    struct TradeOffer {
        address tokenFrom;
        address tokenTo;
        uint256 amountFrom;
        uint256 amountTo;
        address creator;
        bool active;
        uint tradeID;
    }
    TradeOffer[] public offers;
    function initiateTrade(
        address _tokenFrom,
        address _tokenTo, 
        uint256 _amountFrom,
        uint256 _amountTo
        ) public returns (uint newTradeID) {
            require(Token(_tokenFrom).transferFrom(msg.sender, address(this), _amountFrom));
            newTradeID = offers.length;
            offers.length++;
            TradeOffer storage o = offers[newTradeID];
            balanceTracker[_tokenFrom] += _amountFrom;
            o.tokenFrom = _tokenFrom;
            o.tokenTo = _tokenTo;
            o.amountFrom = _amountFrom;
            o.amountTo = _amountTo;
            o.creator = msg.sender;
            o.active = true;
            o.tradeID = newTradeID;
            emit OfferCreated(newTradeID);
    }
    function cancelTrade(uint tradeID) public returns (bool) {
        TradeOffer storage o = offers[tradeID];
        require(msg.sender == o.creator);
        require(Token(o.tokenFrom).transfer(o.creator, o.amountFrom));
        balanceTracker[o.tokenFrom] -= o.amountFrom;
        o.active = false;
        emit OfferCancelled(tradeID);
        return true;
    }
    function take(uint tradeID) public returns (bool) {
        TradeOffer storage o = offers[tradeID];
        require(o.active == true);
        require(Token(o.tokenFrom).transfer(msg.sender, o.amountFrom));
        balanceTracker[o.tokenFrom] -= o.amountFrom;
        require(Token(o.tokenTo).transferFrom(msg.sender, o.creator, o.amountTo));
        o.active = false;
        emit OfferTaken(tradeID);
        return true;
    }
    function getOfferDetails(uint tradeID) external view returns (
        address _tokenFrom,
        address _tokenTo, 
        uint256 _amountFrom,
        uint256 _amountTo,
        address _creator,
        bool _active
    ) {
        TradeOffer storage o = offers[tradeID];
        _tokenFrom = o.tokenFrom;
        _tokenTo = o.tokenTo;
        _amountFrom = o.amountFrom;
        _amountTo = o.amountTo;
        _creator = o.creator;
        _active = o.active;
    }
    function reclaimToken(Token _token) external onlyOwner {
        uint256 balance = _token.balanceOf(address(this));
        uint256 excess = balance - balanceTracker[address(_token)];
        require(excess > 0);
        _token.transfer(owner, excess);
    }
}
```

## RQ1_1007b4fc52ca

SHA-256 `644289eda397c8a2bd67a571d9112c91fb3eaf49542c16002a1ffa690c32da29`

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
	function EncryptedToken() TokenERC20(INITIAL_SUPPLY, 'TMET', '18') payable public {
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

## RQ1_98573224dd77

SHA-256 `0babd3b5dfcb90197002d0285de55b8c4268b12ada6927d0c5d1c40de69b6cb8`

```solidity
pragma solidity ^0.4.18;
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public view returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
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
     function percent(uint256 a,uint256 b) internal  pure returns (uint256){
      return mul(div(a,uint256(100)),b);
    }
    function power(uint256 a,uint256 b) internal pure returns (uint256){
      return mul(a,10**b);
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
    function balanceOf(address _owner) public view returns (uint256 balance) {
        return balances[_owner];
    }
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public view returns (uint256);
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
contract RDOToken is StandardToken {
    string public name = "RDO";
    string public symbol = "RDO";
    uint256 public decimals = 8;
    address owner;
    address crowdsale;
    event Burn(address indexed burner, uint256 value);
    function RDOToken() public {
        owner=msg.sender;
        uint256 initialTotalSupply=1000000000;
        totalSupply=initialTotalSupply.power(decimals);
        balances[msg.sender]=totalSupply;
        crowdsale=new RDOCrowdsale(this,msg.sender);
        allocate(crowdsale,75); 
        allocate(0x523f6034c79915cE9AacD06867721D444c45a6a5,12); 
        allocate(0x50d0a8eDe1548E87E5f8103b89626bC9C76fe2f8,7); 
        allocate(0xD8889ff86b9454559979Aa20bb3b41527AE4b74b,3); 
        allocate(0x5F900841910baaC70e8b736632600c409Af05bf8,3); 
    }
    function burn(uint256 _value) public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        Burn(burner, _value);
    }
    function allocate(address _address,uint256 percent) private{
        uint256 bal=totalSupply.percent(percent);
        transfer(_address,bal);
    }
    modifier onlyOwner() {
        require(msg.sender==owner);
        _;
    }
    function stopCrowdfunding() onlyOwner public {
        if(crowdsale!=0x0){
            RDOCrowdsale(crowdsale).stopCrowdsale();
            crowdsale=0x0;
        }
    }
    function getCrowdsaleAddress() constant public returns(address){
        return crowdsale;
    }
}
contract RDOCrowdsale {
    using SafeMath for uint256;
    RDOToken public token;
    address public wallet;
    address public owners;
    uint256 public price=0.55 finney;
    mapping (uint => Phase) phases;
    uint public totalPhases = 9;
    struct Phase {
        uint256 startTime;
        uint256 endTime;
        uint256 bonusPercent;
    }
    BonusValue[] bonusValue;
    struct BonusValue{
        uint256 minimum;
        uint256 maximum;
        uint256 bonus;
    }
    uint256 public constant minContribution = 100 finney;
    uint256 public weiRaised;
    event TokenPurchase(address indexed purchaser, address indexed beneficiary, uint256 value, uint256 bonusPercent, uint256 amount);
    event WalletSet(address indexed wallet);
    function RDOCrowdsale(address _tokenAddress, address _wallet) public {
        require(_tokenAddress != address(0));
        token = RDOToken(_tokenAddress);
        wallet = _wallet;
        owners=msg.sender;
        fillPhase(0,40,25 days);
        fillPhase(1,30,15 days);
        fillPhase(2,25,15 days);
        fillPhase(3,20,15 days);
        fillPhase(4,15,15 days);
        fillPhase(5,10,15 days);
        fillPhase(6,7,15 days);
        fillPhase(7,5,15 days);
        fillPhase(8,3,15 days);
        bonusValue.push(BonusValue({
            minimum:5 ether,
            maximum:25 ether,
            bonus:5
        }));
        bonusValue.push(BonusValue({
            minimum:26 ether,
            maximum:100 ether,
            bonus:8
        }));
        bonusValue.push(BonusValue({
            minimum:101 ether,
            maximum:100000 ether,
            bonus:10
        }));
    }
    function fillPhase(uint8 index,uint256 bonus,uint256 delay) private{
        phases[index].bonusPercent=bonus;
        if(index==0){
            phases[index].startTime = now;
        }
        else{
            phases[index].startTime = phases[index-1].endTime;
        }
        phases[index].endTime = phases[index].startTime+delay;
    }
    function () external payable {
        buyTokens(msg.sender);
    }
    function buyTokens(address beneficiary) public payable {
        require(beneficiary != address(0));
        require(msg.value != 0);
        uint256 currentBonusPercent = getBonusPercent(now);
        uint256 weiAmount = msg.value;
        uint256 volumeBonus=getVolumeBonus(weiAmount);
        require(weiAmount>=minContribution);
        uint256 tokens = calculateTokenAmount(weiAmount, currentBonusPercent,volumeBonus);
        weiRaised = weiRaised.add(weiAmount);
        token.transfer(beneficiary, tokens);
        TokenPurchase(msg.sender, beneficiary, weiAmount, currentBonusPercent, tokens);
        forwardFunds();
    }
    function getVolumeBonus(uint256 _wei) private view returns(uint256){
        for(uint256 i=0;i<bonusValue.length;++i){
            if(_wei>bonusValue[i].minimum && _wei<bonusValue[i].maximum){
                return bonusValue[i].bonus;
            }
        }
        return 0;
    }
    function getBonusPercent(uint256 datetime) private view returns (uint256) {
        for (uint i = 0; i < totalPhases; i++) {
            if (datetime >= phases[i].startTime && datetime <= phases[i].endTime) {
                return phases[i].bonusPercent;
            }
        }
        return 0;
    }
    modifier onlyOwner() {
        require(owners==msg.sender);
        _;
    }
    function calculateTokenAmount(uint256 _weiDeposit, uint256 _bonusTokensPercent,uint256 _volumeBonus) private view returns (uint256) {
        uint256 mainTokens = _weiDeposit.div(price);
        uint256 bonusTokens = mainTokens.percent(_bonusTokensPercent);
        uint256 volumeBonus=mainTokens.percent(_volumeBonus);
        return mainTokens.add(bonusTokens).add(volumeBonus);
    }
    function forwardFunds() internal {
        wallet.transfer(msg.value);
    }
    function stopCrowdsale() public {
        token.burn(token.balanceOf(this));
        selfdestruct(wallet);
    }
    function getCurrentBonus() public constant returns(uint256){
        return getBonusPercent(now);
    }
    function calculateEstimateToken(uint256 _wei) public constant returns(uint256){
        uint256 timeBonus=getCurrentBonus();
        uint256 volumeBonus=getVolumeBonus(_wei);
        return calculateTokenAmount(_wei,timeBonus,volumeBonus);
    }
}
```

## RQ1_226d8f357d3f

SHA-256 `a80765eef9044c63831e602baaeb0e03db273139f25523486ac517e5b08ae340`

```solidity
pragma solidity ^0.5.4;
library SafeMath {
    function add(uint a, uint b) internal pure returns (uint c) {
        c = a + b;
        require(c >= a);
    }
    function sub(uint a, uint b) internal pure returns (uint c) {
        require(b <= a);
        c = a - b;
    }
}
contract Owned {
    address payable public owner;
    address public newOwner;
    event OwnershipTransferred(address indexed _from, address indexed _to);
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    function init(address _owner) public {
        require(owner == address(0));
        owner = address(uint160(_owner));
    }
    function transferOwnership(address _newOwner) public onlyOwner {
        newOwner = _newOwner;
    }
    function acceptOwnership() public {
        require(msg.sender == newOwner);
        emit OwnershipTransferred(owner, newOwner);
        owner = address(uint160(newOwner));
        newOwner = address(0);
    }
    function recoverTokens(address token, uint tokens) public onlyOwner {
        if (token == address(0)) {
            owner.transfer((tokens == 0 ? address(this).balance : tokens));
        } else {
            ERC20Interface(token).transfer(owner, tokens == 0 ? ERC20Interface(token).balanceOf(address(this)) : tokens);
        }
    }
}
contract ApproveAndCallFallback {
    function receiveApproval(address from, uint256 tokens, address token, bytes memory data) public;
}
contract ERC20Interface {
    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);
    function totalSupply() public view returns (uint);
    function balanceOf(address tokenOwner) public view returns (uint balance);
    function allowance(address tokenOwner, address spender) public view returns (uint remaining);
    function transfer(address to, uint tokens) public returns (bool success);
    function approve(address spender, uint tokens) public returns (bool success);
    function transferFrom(address from, address to, uint tokens) public returns (bool success);
}
contract TokenInterface is ERC20Interface {
    function symbol() public view returns (string memory);
    function name() public view returns (string memory);
    function decimals() public view returns (uint8);
    function approveAndCall(address spender, uint tokens, bytes memory data) public returns (bool success);
}
contract FixedSupplyToken is TokenInterface, Owned {
    using SafeMath for uint;
    string _symbol;
    string  _name;
    uint8 _decimals;
    uint _totalSupply;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    function init(address tokenOwner, string memory symbol, string memory name, uint8 decimals, uint fixedSupply) public {
        super.init(tokenOwner);
        _symbol = symbol;
        _name = name;
        _decimals = decimals;
        _totalSupply = fixedSupply;
        balances[tokenOwner] = _totalSupply;
        emit Transfer(address(0), tokenOwner, _totalSupply);
    }
    function symbol() public view returns (string memory) {
        return _symbol;
    }
    function name() public view returns (string memory) {
        return _name;
    }
    function decimals() public view returns (uint8) {
        return _decimals;
    }
    function totalSupply() public view returns (uint) {
        return _totalSupply.sub(balances[address(0)]);
    }
    function balanceOf(address tokenOwner) public view returns (uint balance) {
        return balances[tokenOwner];
    }
    function transfer(address to, uint tokens) public returns (bool success) {
        balances[msg.sender] = balances[msg.sender].sub(tokens);
        balances[to] = balances[to].add(tokens);
        emit Transfer(msg.sender, to, tokens);
        return true;
    }
    function approve(address spender, uint tokens) public returns (bool success) {
        allowed[msg.sender][spender] = tokens;
        emit Approval(msg.sender, spender, tokens);
        return true;
    }
    function transferFrom(address from, address to, uint tokens) public returns (bool success) {
        balances[from] = balances[from].sub(tokens);
        allowed[from][msg.sender] = allowed[from][msg.sender].sub(tokens);
        balances[to] = balances[to].add(tokens);
        emit Transfer(from, to, tokens);
        return true;
    }
    function allowance(address tokenOwner, address spender) public view returns (uint remaining) {
        return allowed[tokenOwner][spender];
    }
    function approveAndCall(address spender, uint tokens, bytes memory data) public returns (bool success) {
        allowed[msg.sender][spender] = tokens;
        emit Approval(msg.sender, spender, tokens);
        ApproveAndCallFallback(spender).receiveApproval(msg.sender, tokens, address(this), data);
        return true;
    }
    function () external payable {
        revert();
    }
}
contract BokkyPooBahsFixedSupplyTokenFactory is Owned {
    using SafeMath for uint;
    address public newAddress;
    uint public minimumFee = 0.1 ether;
    mapping(address => bool) public isChild;
    address[] public children;
    event FactoryDeprecated(address _newAddress);
    event MinimumFeeUpdated(uint oldFee, uint newFee);
    event TokenDeployed(address indexed owner, address indexed token, string symbol, string name, uint8 decimals, uint totalSupply);
    constructor () public {
        super.init(msg.sender);
    }
    function numberOfChildren() public view returns (uint) {
        return children.length;
    }
    function deprecateFactory(address _newAddress) public onlyOwner {
        require(newAddress == address(0));
        emit FactoryDeprecated(_newAddress);
        newAddress = _newAddress;
    }
    function setMinimumFee(uint _minimumFee) public onlyOwner {
        emit MinimumFeeUpdated(minimumFee, _minimumFee);
        minimumFee = _minimumFee;
    }
    function deployTokenContract(string memory symbol, string memory name, uint8 decimals, uint totalSupply) public payable returns (FixedSupplyToken token) {
        require(msg.value >= minimumFee);
        require(decimals <= 27);
        require(totalSupply > 0);
        token = new FixedSupplyToken();
        token.init(msg.sender, symbol, name, decimals, totalSupply);
        isChild[address(token)] = true;
        children.push(address(token));
        emit TokenDeployed(owner, address(token), symbol, name, decimals, totalSupply);
        if (msg.value > 0) {
            owner.transfer(msg.value);
        }
    }
    function () external payable {
        revert();
    }
}
```

## RQ1_43caf1e7f7b5

SHA-256 `69ddee50f543e64215b8e52d7b2a154384c8fe13409354038a421ad652c52f47`

```solidity
pragma solidity ^0.4.17;
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

## RQ1_e3eee1f935e0

SHA-256 `3e54093cd0d046f5b6844c411470419fb91033cc248b48e7d224614c174bbabc`

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

SHA-256 `800ef87137433243ecd86ea429ae03879de0217c335a8e88809d5fa2109d772e`

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

SHA-256 `914851b82ffecbb108000d00b17c328d09a3ebbe3dec5424177decfb940ba14b`

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

## RQ1_5d78d6a1f8f7

SHA-256 `3ea419367233dc62cafd62bc1cef8a00748a2e8c6831f7ee4e8693b810205fe2`

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
contract XVOToken is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "XVO Token";
    string public constant symbol = "XVOT";
    uint public constant decimals = 18;
uint256 public totalSupply = 10000000000e18;
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
    function XVOTOKEN() public {
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
}
```

## RQ1_b38cae1d4aa8

SHA-256 `49f6a9d3756d0f12c13c8e4289a5e1d2eea9df9b2b7a2f62f732a937d60450f5`

```solidity
pragma solidity ^0.4.19;
contract GimliToken {
    string public name = "Gimli Token";
    string public symbol = "GIM";
    uint8 public constant decimals = 8;  
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
    function GimliToken() public {
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

## RQ1_2a567216aa64

SHA-256 `baf55e9dc04ab6047eebc1741add0a9ea2da567471e4d3d783f30ef26e687146`

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

## RQ1_e5fa339cd599

SHA-256 `79e230e945a562e738818bc7501845892cbd6f90bc08974a9a424a6eeee4392f`

```solidity
pragma solidity ^0.5.0;
library SafeMath {
	function mul(uint a, uint b) internal pure returns (uint) {
		uint c = a * b;
		assert(a == 0 || c / a == b);
		return c;
	}
	function div(uint a, uint b) internal pure returns (uint) {
		uint c = a / b;
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
	function diff(uint a, uint b) internal pure returns (uint) {
		return a > b ? sub(a, b) : sub(b, a);
	}
	function gt(uint a, uint b) internal pure returns(bytes1) {
		bytes1 c;
		c = 0x00;
		if (a > b) {
			c = 0x01;
		}
		return c;
	}
}
interface IMultiSigManager {
	function provideAddress(address origin, uint poolIndex) external returns (address payable);
	function passedContract(address) external returns (bool);
	function moderator() external returns(address);
}
contract Managed {
	IMultiSigManager roleManager;
	address public roleManagerAddress;
	address public operator;
	uint public lastOperationTime;
	uint public operationCoolDown;
	uint constant BP_DENOMINATOR = 10000;
	event UpdateRoleManager(address newManagerAddress);
	event UpdateOperator(address updater, address newOperator);
	modifier only(address addr) {
		require(msg.sender == addr);
		_;
	}
	modifier inUpdateWindow() {
		uint currentTime = getNowTimestamp();
		require(currentTime - lastOperationTime >= operationCoolDown);
		_;
		lastOperationTime = currentTime;
	}
	constructor(
		address roleManagerAddr,
		address opt, 
		uint optCoolDown
	) public {
		roleManagerAddress = roleManagerAddr;
		roleManager = IMultiSigManager(roleManagerAddr);
		operator = opt;
		operationCoolDown = optCoolDown;
	}
	function updateRoleManager(address newManagerAddr) 
		inUpdateWindow() 
		public 
	returns (bool) {
		require(roleManager.passedContract(newManagerAddr));
		roleManagerAddress = newManagerAddr;
		roleManager = IMultiSigManager(roleManagerAddress);
		require(roleManager.moderator() != address(0));
		emit UpdateRoleManager(newManagerAddr);
		return true;
	}
	function updateOperator() public inUpdateWindow() returns (bool) {	
		address updater = msg.sender;	
		operator = roleManager.provideAddress(updater, 0);
		emit UpdateOperator(updater, operator);	
		return true;
	}
	function getNowTimestamp() internal view returns (uint) {
		return now;
	}
}
contract Magi is Managed {
	using SafeMath for uint;
	struct Price {
		uint priceInWei;
		uint timeInSecond;
		address source;
	}
	Price public firstPrice;
	Price public secondPrice;
	Price public lastPrice;
	address public priceFeed1; 
	address public priceFeed2; 
	address public priceFeed3;
	uint public priceTolInBP = 500; 
	uint public priceFeedTolInBP = 100;
	uint public priceFeedTimeTol = 1 minutes;
	uint public priceUpdateCoolDown;
	uint public numOfPrices = 0;
	bool public started = false;
	modifier isPriceFeed() {
		require(msg.sender == priceFeed1 || msg.sender == priceFeed2 || msg.sender == priceFeed3);
		_;
	}
	event CommitPrice(uint indexed priceInWei, uint indexed timeInSecond, address sender, uint index);
	event AcceptPrice(uint indexed priceInWei, uint indexed timeInSecond, address sender);
	event SetValue(uint index, uint oldValue, uint newValue);
	event UpdatePriceFeed(address updater, address newPriceFeed);
	constructor(
		address opt,
		address pf1,
		address pf2,
		address pf3,
		address roleManagerAddr,
		uint pxCoolDown,
		uint optCoolDown
		) 
		public
		Managed(roleManagerAddr, opt, optCoolDown) 
	{
		priceFeed1 = pf1;
		priceFeed2 = pf2;
		priceFeed3 = pf3;
		priceUpdateCoolDown = pxCoolDown;
		roleManagerAddress = roleManagerAddr;
		roleManager = IMultiSigManager(roleManagerAddr);
		emit UpdateRoleManager(roleManagerAddress);
	}
	function startOracle(
		uint priceInWei, 
		uint timeInSecond
	)
		public 
		isPriceFeed() 
		returns (bool success) 
	{
		require(!started && timeInSecond <= getNowTimestamp());
		lastPrice.timeInSecond = timeInSecond;
		lastPrice.priceInWei = priceInWei;
		lastPrice.source = msg.sender;
		started = true;
		emit AcceptPrice(priceInWei, timeInSecond, msg.sender);
		return true;
	}
	function getLastPrice() public view returns(uint, uint) {
		return (lastPrice.priceInWei, lastPrice.timeInSecond);
	}
	function commitPrice(uint priceInWei, uint timeInSecond) 
		public 
		isPriceFeed()
		returns (bool success)
	{	
		require(started && timeInSecond <= getNowTimestamp() && timeInSecond >= lastPrice.timeInSecond.add(priceUpdateCoolDown));
		uint priceDiff;
		if (numOfPrices == 0) {
			priceDiff = priceInWei.diff(lastPrice.priceInWei);
			if (priceDiff.mul(BP_DENOMINATOR).div(lastPrice.priceInWei) <= priceTolInBP) {
				acceptPrice(priceInWei, timeInSecond, msg.sender);
			} else {
				firstPrice = Price(priceInWei, timeInSecond, msg.sender);
				emit CommitPrice(priceInWei, timeInSecond, msg.sender, 0);
				numOfPrices++;
			}
		} else if (numOfPrices == 1) {
			if (timeInSecond > firstPrice.timeInSecond.add(priceUpdateCoolDown)) {
				if (firstPrice.source == msg.sender)
					acceptPrice(priceInWei, timeInSecond, msg.sender);
				else
					acceptPrice(firstPrice.priceInWei, timeInSecond, firstPrice.source);
			} else {
				require(firstPrice.source != msg.sender);
				if (firstPrice.timeInSecond.add(priceFeedTimeTol) < timeInSecond || 
					firstPrice.timeInSecond.sub(priceFeedTimeTol) > timeInSecond) {
					acceptPrice(firstPrice.priceInWei, firstPrice.timeInSecond, firstPrice.source);
				} else {
					priceDiff = priceInWei.diff(firstPrice.priceInWei);
					if (priceDiff.mul(BP_DENOMINATOR).div(firstPrice.priceInWei) <= priceTolInBP) {
						acceptPrice(firstPrice.priceInWei, firstPrice.timeInSecond, firstPrice.source);
					} else {
						secondPrice = Price(priceInWei, timeInSecond, msg.sender);
						emit CommitPrice(priceInWei, timeInSecond, msg.sender, 1);
						numOfPrices++;
					} 
				}
			}
		} else if (numOfPrices == 2) {
			if (timeInSecond > firstPrice.timeInSecond + priceUpdateCoolDown) {
				if ((firstPrice.source == msg.sender || secondPrice.source == msg.sender))
					acceptPrice(priceInWei, timeInSecond, msg.sender);
				else
					acceptPrice(secondPrice.priceInWei, timeInSecond, secondPrice.source);
			} else {
				require(firstPrice.source != msg.sender && secondPrice.source != msg.sender);
				uint acceptedPriceInWei;
				if (firstPrice.timeInSecond.add(priceFeedTimeTol) < timeInSecond || 
					firstPrice.timeInSecond.sub(priceFeedTimeTol) > timeInSecond) {
					acceptedPriceInWei = firstPrice.priceInWei;
				} else {
					if (secondPrice.priceInWei == priceInWei) {
						acceptedPriceInWei = priceInWei;
					} else {
						acceptedPriceInWei = getMedian(firstPrice.priceInWei, secondPrice.priceInWei, priceInWei);
					}
				}
				acceptPrice(acceptedPriceInWei, firstPrice.timeInSecond, firstPrice.source);
			}
		} else {
			return false;
		}
		return true;
	}
	function acceptPrice(uint priceInWei, uint timeInSecond, address source) internal {
		lastPrice.priceInWei = priceInWei;
		lastPrice.timeInSecond = timeInSecond;
		lastPrice.source = source;
		numOfPrices = 0;
		emit AcceptPrice(priceInWei, timeInSecond, source);
	}
	function getMedian(uint a, uint b, uint c) internal pure returns (uint) {
		if (a.gt(b) ^ c.gt(a) == 0x0) {
			return a;
		} else if(b.gt(a) ^ c.gt(b) == 0x0) {
			return b;
		} else {
			return c;
		}
	}
	function updatePriceFeed(uint index) 
		inUpdateWindow() 
		public 
	returns (bool) {
		require(index < 3);
		address updater = msg.sender;
		address newAddr = roleManager.provideAddress(updater, 1);
		if(index == 0) 
			priceFeed1 = newAddr;
		else if (index == 1)
			priceFeed2 = newAddr;
		else 
			priceFeed3 = newAddr;
		emit UpdatePriceFeed(updater, newAddr);
		return true;
	}
	function setValue(
		uint idx, 
		uint newValue
	) 
		public 
		only(operator) 
		inUpdateWindow() 
	returns (bool success) {
		uint oldValue;
		if (idx == 0) {
			oldValue = priceTolInBP;
			priceTolInBP = newValue;
		} else if (idx == 1) {
			oldValue = priceFeedTolInBP;
			priceFeedTolInBP = newValue;
		} else if (idx == 2) {
			oldValue = priceFeedTimeTol;
			priceFeedTimeTol = newValue;
		} else if (idx == 3) {
			oldValue = priceUpdateCoolDown;
			priceUpdateCoolDown = newValue;
		} else {
			revert();
		}
		emit SetValue(idx, oldValue, newValue);
		return true;
	}
}
```

## RQ1_f730cc94794a

SHA-256 `ad8edede965fafa9bca4bec6d8a97d674e4bd83f0ee4328606860188ed9759b9`

```solidity
pragma solidity ^0.4.24;
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
contract PCC is ERC20Interface, Owned, SafeMath {
    string public symbol;
    string public  name;
    uint8 public decimals;
    uint public _totalSupply;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    function PCC() public {
        symbol = "PCC";
        name = "Pcore";
        decimals = 8;
        _totalSupply = 	5200000000000000;
        balances[0x67322D8A8f72B8417f16397667d8F6ce996A6982] = _totalSupply;
        Transfer(address(0), 0x67322D8A8f72B8417f16397667d8F6ce996A6982, _totalSupply);
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

## RQ1_a3aff7048f13

SHA-256 `3a1ea4c1b486e8ba672a8948142da9d374de21b0a4130244272e31f5ec1a7d4c`

```solidity
pragma solidity 0.4.24;
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
library SafeMath8 {
  function mul(uint8 a, uint8 b) internal pure returns (uint8) {
    uint8 c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function div(uint8 a, uint8 b) internal pure returns (uint8) {
    uint8 c = a / b;
    return c;
  }
  function sub(uint8 a, uint8 b) internal pure returns (uint8) {
    assert(b <= a);
    return a - b;
  }
  function add(uint8 a, uint8 b) internal pure returns (uint8) {
    uint8 c = a + b;
    assert(c >= a);
    return c;
  }
}
library SafeMath16 {
  function mul(uint16 a, uint16 b) internal pure returns (uint16) {
    uint16 c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function div(uint16 a, uint16 b) internal pure returns (uint16) {
    uint16 c = a / b;
    return c;
  }
  function sub(uint16 a, uint16 b) internal pure returns (uint16) {
    assert(b <= a);
    return a - b;
  }
  function add(uint16 a, uint16 b) internal pure returns (uint16) {
    uint16 c = a + b;
    assert(c >= a);
    return c;
  }
}
library SafeMath {
  function mul(uint256 _a, uint256 _b) internal pure returns (uint256 c) {
    if (_a == 0) {
      return 0;
    }
    c = _a * _b;
    assert(c / _a == _b);
    return c;
  }
  function div(uint256 _a, uint256 _b) internal pure returns (uint256) {
    return _a / _b;
  }
  function sub(uint256 _a, uint256 _b) internal pure returns (uint256) {
    assert(_b <= _a);
    return _a - _b;
  }
  function add(uint256 _a, uint256 _b) internal pure returns (uint256 c) {
    c = _a + _b;
    assert(c >= _a);
    return c;
  }
}
interface ERC165 {
  function supportsInterface(bytes4 _interfaceId)
    external
    view
    returns (bool);
}
contract SupportsInterfaceWithLookup is ERC165 {
  bytes4 public constant InterfaceId_ERC165 = 0x01ffc9a7;
  mapping(bytes4 => bool) internal supportedInterfaces;
  constructor()
    public
  {
    _registerInterface(InterfaceId_ERC165);
  }
  function supportsInterface(bytes4 _interfaceId)
    external
    view
    returns (bool)
  {
    return supportedInterfaces[_interfaceId];
  }
  function _registerInterface(bytes4 _interfaceId)
    internal
  {
    require(_interfaceId != 0xffffffff);
    supportedInterfaces[_interfaceId] = true;
  }
}
contract ERC721Basic is ERC165 {
  bytes4 internal constant InterfaceId_ERC721 = 0x80ac58cd;
  bytes4 internal constant InterfaceId_ERC721Exists = 0x4f558e79;
  bytes4 internal constant InterfaceId_ERC721Enumerable = 0x780e9d63;
  bytes4 internal constant InterfaceId_ERC721Metadata = 0x5b5e139f;
  event Transfer(
    address indexed _from,
    address indexed _to,
    uint256 indexed _tokenId
  );
  event Approval(
    address indexed _owner,
    address indexed _approved,
    uint256 indexed _tokenId
  );
  event ApprovalForAll(
    address indexed _owner,
    address indexed _operator,
    bool _approved
  );
  function balanceOf(address _owner) public view returns (uint256 _balance);
  function ownerOf(uint256 _tokenId) public view returns (address _owner);
  function exists(uint256 _tokenId) public view returns (bool _exists);
  function approve(address _to, uint256 _tokenId) public;
  function getApproved(uint256 _tokenId)
    public view returns (address _operator);
  function setApprovalForAll(address _operator, bool _approved) public;
  function isApprovedForAll(address _owner, address _operator)
    public view returns (bool);
  function transferFrom(address _from, address _to, uint256 _tokenId) public;
  function safeTransferFrom(address _from, address _to, uint256 _tokenId)
    public;
  function safeTransferFrom(
    address _from,
    address _to,
    uint256 _tokenId,
    bytes _data
  )
    public;
}
contract ERC721Enumerable is ERC721Basic {
  function totalSupply() public view returns (uint256);
  function tokenOfOwnerByIndex(
    address _owner,
    uint256 _index
  )
    public
    view
    returns (uint256 _tokenId);
  function tokenByIndex(uint256 _index) public view returns (uint256);
}
contract ERC721Metadata is ERC721Basic {
  function name() external view returns (string _name);
  function symbol() external view returns (string _symbol);
  function tokenURI(uint256 _tokenId) public view returns (string);
}
contract ERC721 is ERC721Basic, ERC721Enumerable, ERC721Metadata {
}
contract ERC721Receiver {
  bytes4 internal constant ERC721_RECEIVED = 0x150b7a02;
  function onERC721Received(
    address _operator,
    address _from,
    uint256 _tokenId,
    bytes _data
  )
    public
    returns(bytes4);
}
library AddressUtils {
  function isContract(address _addr) internal view returns (bool) {
    uint256 size;
    assembly { size := extcodesize(_addr) }
    return size > 0;
  }
}
contract Azimuth is Ownable
{
  event OwnerChanged(uint32 indexed point, address indexed owner);
  event Activated(uint32 indexed point);
  event Spawned(uint32 indexed prefix, uint32 indexed child);
  event EscapeRequested(uint32 indexed point, uint32 indexed sponsor);
  event EscapeCanceled(uint32 indexed point, uint32 indexed sponsor);
  event EscapeAccepted(uint32 indexed point, uint32 indexed sponsor);
  event LostSponsor(uint32 indexed point, uint32 indexed sponsor);
  event ChangedKeys( uint32 indexed point,
                     bytes32 encryptionKey,
                     bytes32 authenticationKey,
                     uint32 cryptoSuiteVersion,
                     uint32 keyRevisionNumber );
  event BrokeContinuity(uint32 indexed point, uint32 number);
  event ChangedSpawnProxy(uint32 indexed point, address indexed spawnProxy);
  event ChangedTransferProxy( uint32 indexed point,
                              address indexed transferProxy );
  event ChangedManagementProxy( uint32 indexed point,
                                address indexed managementProxy );
  event ChangedVotingProxy(uint32 indexed point, address indexed votingProxy);
  event ChangedDns(string primary, string secondary, string tertiary);
  enum Size
  {
    Galaxy, 
    Star,   
    Planet  
  }
  struct Point
  {
    bytes32 encryptionKey;
    bytes32 authenticationKey;
    uint32[] spawned;
    bool hasSponsor;
    bool active;
    bool escapeRequested;
    uint32 sponsor;
    uint32 escapeRequestedTo;
    uint32 cryptoSuiteVersion;
    uint32 keyRevisionNumber;
    uint32 continuityNumber;
  }
  struct Deed
  {
    address owner;
    address managementProxy;
    address spawnProxy;
    address votingProxy;
    address transferProxy;
  }
  mapping(uint32 => Point) public points;
  mapping(uint32 => Deed) public rights;
  mapping(address => mapping(address => bool)) public operators;
  string[3] public dnsDomains;
  mapping(uint32 => uint32[]) public sponsoring;
  mapping(uint32 => mapping(uint32 => uint256)) public sponsoringIndexes;
  mapping(uint32 => uint32[]) public escapeRequests;
  mapping(uint32 => mapping(uint32 => uint256)) public escapeRequestsIndexes;
  mapping(address => uint32[]) public pointsOwnedBy;
  mapping(address => mapping(uint32 => uint256)) public pointOwnerIndexes;
  mapping(address => uint32[]) public managerFor;
  mapping(address => mapping(uint32 => uint256)) public managerForIndexes;
  mapping(address => uint32[]) public spawningFor;
  mapping(address => mapping(uint32 => uint256)) public spawningForIndexes;
  mapping(address => uint32[]) public votingFor;
  mapping(address => mapping(uint32 => uint256)) public votingForIndexes;
  mapping(address => uint32[]) public transferringFor;
  mapping(address => mapping(uint32 => uint256)) public transferringForIndexes;
  constructor()
    public
  {
    setDnsDomains("example.com", "example.com", "example.com");
  }
  function setDnsDomains(string _primary, string _secondary, string _tertiary)
    onlyOwner
    public
  {
    dnsDomains[0] = _primary;
    dnsDomains[1] = _secondary;
    dnsDomains[2] = _tertiary;
    emit ChangedDns(_primary, _secondary, _tertiary);
  }
    function isActive(uint32 _point)
      view
      external
      returns (bool equals)
    {
      return points[_point].active;
    }
    function getKeys(uint32 _point)
      view
      external
      returns (bytes32 crypt, bytes32 auth, uint32 suite, uint32 revision)
    {
      Point storage point = points[_point];
      return (point.encryptionKey,
              point.authenticationKey,
              point.cryptoSuiteVersion,
              point.keyRevisionNumber);
    }
    function getKeyRevisionNumber(uint32 _point)
      view
      external
      returns (uint32 revision)
    {
      return points[_point].keyRevisionNumber;
    }
    function hasBeenLinked(uint32 _point)
      view
      external
      returns (bool result)
    {
      return ( points[_point].keyRevisionNumber > 0 );
    }
    function isLive(uint32 _point)
      view
      external
      returns (bool result)
    {
      Point storage point = points[_point];
      return ( point.encryptionKey != 0 &&
               point.authenticationKey != 0 &&
               point.cryptoSuiteVersion != 0 );
    }
    function getContinuityNumber(uint32 _point)
      view
      external
      returns (uint32 continuityNumber)
    {
      return points[_point].continuityNumber;
    }
    function getSpawnCount(uint32 _point)
      view
      external
      returns (uint32 spawnCount)
    {
      uint256 len = points[_point].spawned.length;
      assert(len < 2**32);
      return uint32(len);
    }
    function getSpawned(uint32 _point)
      view
      external
      returns (uint32[] spawned)
    {
      return points[_point].spawned;
    }
    function hasSponsor(uint32 _point)
      view
      external
      returns (bool has)
    {
      return points[_point].hasSponsor;
    }
    function getSponsor(uint32 _point)
      view
      external
      returns (uint32 sponsor)
    {
      return points[_point].sponsor;
    }
    function isSponsor(uint32 _point, uint32 _sponsor)
      view
      external
      returns (bool result)
    {
      Point storage point = points[_point];
      return ( point.hasSponsor &&
               (point.sponsor == _sponsor) );
    }
    function getSponsoringCount(uint32 _sponsor)
      view
      external
      returns (uint256 count)
    {
      return sponsoring[_sponsor].length;
    }
    function getSponsoring(uint32 _sponsor)
      view
      external
      returns (uint32[] sponsees)
    {
      return sponsoring[_sponsor];
    }
    function isEscaping(uint32 _point)
      view
      external
      returns (bool escaping)
    {
      return points[_point].escapeRequested;
    }
    function getEscapeRequest(uint32 _point)
      view
      external
      returns (uint32 escape)
    {
      return points[_point].escapeRequestedTo;
    }
    function isRequestingEscapeTo(uint32 _point, uint32 _sponsor)
      view
      public
      returns (bool equals)
    {
      Point storage point = points[_point];
      return (point.escapeRequested && (point.escapeRequestedTo == _sponsor));
    }
    function getEscapeRequestsCount(uint32 _sponsor)
      view
      external
      returns (uint256 count)
    {
      return escapeRequests[_sponsor].length;
    }
    function getEscapeRequests(uint32 _sponsor)
      view
      external
      returns (uint32[] requests)
    {
      return escapeRequests[_sponsor];
    }
    function activatePoint(uint32 _point)
      onlyOwner
      external
    {
      Point storage point = points[_point];
      require(!point.active);
      point.active = true;
      registerSponsor(_point, true, getPrefix(_point));
      emit Activated(_point);
    }
    function setKeys(uint32 _point,
                     bytes32 _encryptionKey,
                     bytes32 _authenticationKey,
                     uint32 _cryptoSuiteVersion)
      onlyOwner
      external
    {
      Point storage point = points[_point];
      if ( point.encryptionKey == _encryptionKey &&
           point.authenticationKey == _authenticationKey &&
           point.cryptoSuiteVersion == _cryptoSuiteVersion )
      {
        return;
      }
      point.encryptionKey = _encryptionKey;
      point.authenticationKey = _authenticationKey;
      point.cryptoSuiteVersion = _cryptoSuiteVersion;
      point.keyRevisionNumber++;
      emit ChangedKeys(_point,
                       _encryptionKey,
                       _authenticationKey,
                       _cryptoSuiteVersion,
                       point.keyRevisionNumber);
    }
    function incrementContinuityNumber(uint32 _point)
      onlyOwner
      external
    {
      Point storage point = points[_point];
      point.continuityNumber++;
      emit BrokeContinuity(_point, point.continuityNumber);
    }
    function registerSpawned(uint32 _point)
      onlyOwner
      external
    {
      uint32 prefix = getPrefix(_point);
      if (prefix == _point)
      {
        return;
      }
      points[prefix].spawned.push(_point);
      emit Spawned(prefix, _point);
    }
    function loseSponsor(uint32 _point)
      onlyOwner
      external
    {
      Point storage point = points[_point];
      if (!point.hasSponsor)
      {
        return;
      }
      registerSponsor(_point, false, point.sponsor);
      emit LostSponsor(_point, point.sponsor);
    }
    function setEscapeRequest(uint32 _point, uint32 _sponsor)
      onlyOwner
      external
    {
      if (isRequestingEscapeTo(_point, _sponsor))
      {
        return;
      }
      registerEscapeRequest(_point, true, _sponsor);
      emit EscapeRequested(_point, _sponsor);
    }
    function cancelEscape(uint32 _point)
      onlyOwner
      external
    {
      Point storage point = points[_point];
      if (!point.escapeRequested)
      {
        return;
      }
      uint32 request = point.escapeRequestedTo;
      registerEscapeRequest(_point, false, 0);
      emit EscapeCanceled(_point, request);
    }
    function doEscape(uint32 _point)
      onlyOwner
      external
    {
      Point storage point = points[_point];
      require(point.escapeRequested);
      registerSponsor(_point, true, point.escapeRequestedTo);
      registerEscapeRequest(_point, false, 0);
      emit EscapeAccepted(_point, point.sponsor);
    }
    function getPrefix(uint32 _point)
      pure
      public
      returns (uint16 prefix)
    {
      if (_point < 0x10000)
      {
        return uint16(_point % 0x100);
      }
      return uint16(_point % 0x10000);
    }
    function getPointSize(uint32 _point)
      external
      pure
      returns (Size _size)
    {
      if (_point < 0x100) return Size.Galaxy;
      if (_point < 0x10000) return Size.Star;
      return Size.Planet;
    }
    function registerSponsor(uint32 _point, bool _hasSponsor, uint32 _sponsor)
      internal
    {
      Point storage point = points[_point];
      bool had = point.hasSponsor;
      uint32 prev = point.sponsor;
      if ( (!had && !_hasSponsor) ||
           (had && _hasSponsor && prev == _sponsor) )
      {
        return;
      }
      if (had)
      {
        uint256 i = sponsoringIndexes[prev][_point];
        assert(i > 0);
        i--;
        uint32[] storage prevSponsoring = sponsoring[prev];
        uint256 last = prevSponsoring.length - 1;
        uint32 moved = prevSponsoring[last];
        prevSponsoring[i] = moved;
        sponsoringIndexes[prev][moved] = i + 1;
        delete(prevSponsoring[last]);
        prevSponsoring.length = last;
        sponsoringIndexes[prev][_point] = 0;
      }
      if (_hasSponsor)
      {
        uint32[] storage newSponsoring = sponsoring[_sponsor];
        newSponsoring.push(_point);
        sponsoringIndexes[_sponsor][_point] = newSponsoring.length;
      }
      point.sponsor = _sponsor;
      point.hasSponsor = _hasSponsor;
    }
    function registerEscapeRequest( uint32 _point,
                                    bool _isEscaping, uint32 _sponsor )
      internal
    {
      Point storage point = points[_point];
      bool was = point.escapeRequested;
      uint32 prev = point.escapeRequestedTo;
      if ( (!was && !_isEscaping) ||
           (was && _isEscaping && prev == _sponsor) )
      {
        return;
      }
      if (was)
      {
        uint256 i = escapeRequestsIndexes[prev][_point];
        assert(i > 0);
        i--;
        uint32[] storage prevRequests = escapeRequests[prev];
        uint256 last = prevRequests.length - 1;
        uint32 moved = prevRequests[last];
        prevRequests[i] = moved;
        escapeRequestsIndexes[prev][moved] = i + 1;
        delete(prevRequests[last]);
        prevRequests.length = last;
        escapeRequestsIndexes[prev][_point] = 0;
      }
      if (_isEscaping)
      {
        uint32[] storage newRequests = escapeRequests[_sponsor];
        newRequests.push(_point);
        escapeRequestsIndexes[_sponsor][_point] = newRequests.length;
      }
      point.escapeRequestedTo = _sponsor;
      point.escapeRequested = _isEscaping;
    }
    function getOwner(uint32 _point)
      view
      external
      returns (address owner)
    {
      return rights[_point].owner;
    }
    function isOwner(uint32 _point, address _address)
      view
      external
      returns (bool result)
    {
      return (rights[_point].owner == _address);
    }
    function getOwnedPointCount(address _whose)
      view
      external
      returns (uint256 count)
    {
      return pointsOwnedBy[_whose].length;
    }
    function getOwnedPoints(address _whose)
      view
      external
      returns (uint32[] ownedPoints)
    {
      return pointsOwnedBy[_whose];
    }
    function getOwnedPointAtIndex(address _whose, uint256 _index)
      view
      external
      returns (uint32 point)
    {
      uint32[] storage owned = pointsOwnedBy[_whose];
      require(_index < owned.length);
      return owned[_index];
    }
    function getManagementProxy(uint32 _point)
      view
      external
      returns (address manager)
    {
      return rights[_point].managementProxy;
    }
    function isManagementProxy(uint32 _point, address _proxy)
      view
      external
      returns (bool result)
    {
      return (rights[_point].managementProxy == _proxy);
    }
    function canManage(uint32 _point, address _who)
      view
      external
      returns (bool result)
    {
      Deed storage deed = rights[_point];
      return ( (0x0 != _who) &&
               ( (_who == deed.owner) ||
                 (_who == deed.managementProxy) ) );
    }
    function getManagerForCount(address _proxy)
      view
      external
      returns (uint256 count)
    {
      return managerFor[_proxy].length;
    }
    function getManagerFor(address _proxy)
      view
      external
      returns (uint32[] mfor)
    {
      return managerFor[_proxy];
    }
    function getSpawnProxy(uint32 _point)
      view
      external
      returns (address spawnProxy)
    {
      return rights[_point].spawnProxy;
    }
    function isSpawnProxy(uint32 _point, address _proxy)
      view
      external
      returns (bool result)
    {
      return (rights[_point].spawnProxy == _proxy);
    }
    function canSpawnAs(uint32 _point, address _who)
      view
      external
      returns (bool result)
    {
      Deed storage deed = rights[_point];
      return ( (0x0 != _who) &&
               ( (_who == deed.owner) ||
                 (_who == deed.spawnProxy) ) );
    }
    function getSpawningForCount(address _proxy)
      view
      external
      returns (uint256 count)
    {
      return spawningFor[_proxy].length;
    }
    function getSpawningFor(address _proxy)
      view
      external
      returns (uint32[] sfor)
    {
      return spawningFor[_proxy];
    }
    function getVotingProxy(uint32 _point)
      view
      external
      returns (address voter)
    {
      return rights[_point].votingProxy;
    }
    function isVotingProxy(uint32 _point, address _proxy)
      view
      external
      returns (bool result)
    {
      return (rights[_point].votingProxy == _proxy);
    }
    function canVoteAs(uint32 _point, address _who)
      view
      external
      returns (bool result)
    {
      Deed storage deed = rights[_point];
      return ( (0x0 != _who) &&
               ( (_who == deed.owner) ||
                 (_who == deed.votingProxy) ) );
    }
    function getVotingForCount(address _proxy)
      view
      external
      returns (uint256 count)
    {
      return votingFor[_proxy].length;
    }
    function getVotingFor(address _proxy)
      view
      external
      returns (uint32[] vfor)
    {
      return votingFor[_proxy];
    }
    function getTransferProxy(uint32 _point)
      view
      external
      returns (address transferProxy)
    {
      return rights[_point].transferProxy;
    }
    function isTransferProxy(uint32 _point, address _proxy)
      view
      external
      returns (bool result)
    {
      return (rights[_point].transferProxy == _proxy);
    }
    function canTransfer(uint32 _point, address _who)
      view
      external
      returns (bool result)
    {
      Deed storage deed = rights[_point];
      return ( (0x0 != _who) &&
               ( (_who == deed.owner) ||
                 (_who == deed.transferProxy) ||
                 operators[deed.owner][_who] ) );
    }
    function getTransferringForCount(address _proxy)
      view
      external
      returns (uint256 count)
    {
      return transferringFor[_proxy].length;
    }
    function getTransferringFor(address _proxy)
      view
      external
      returns (uint32[] tfor)
    {
      return transferringFor[_proxy];
    }
    function isOperator(address _owner, address _operator)
      view
      external
      returns (bool result)
    {
      return operators[_owner][_operator];
    }
    function setOwner(uint32 _point, address _owner)
      onlyOwner
      external
    {
      require(0x0 != _owner);
      address prev = rights[_point].owner;
      if (prev == _owner)
      {
        return;
      }
      if (0x0 != prev)
      {
        uint256 i = pointOwnerIndexes[prev][_point];
        assert(i > 0);
        i--;
        uint32[] storage owner = pointsOwnedBy[prev];
        uint256 last = owner.length - 1;
        uint32 moved = owner[last];
        owner[i] = moved;
        pointOwnerIndexes[prev][moved] = i + 1;
        delete(owner[last]);
        owner.length = last;
        pointOwnerIndexes[prev][_point] = 0;
      }
      rights[_point].owner = _owner;
      pointsOwnedBy[_owner].push(_point);
      pointOwnerIndexes[_owner][_point] = pointsOwnedBy[_owner].length;
      emit OwnerChanged(_point, _owner);
    }
    function setManagementProxy(uint32 _point, address _proxy)
      onlyOwner
      external
    {
      Deed storage deed = rights[_point];
      address prev = deed.managementProxy;
      if (prev == _proxy)
      {
        return;
      }
      if (0x0 != prev)
      {
        uint256 i = managerForIndexes[prev][_point];
        assert(i > 0);
        i--;
        uint32[] storage prevMfor = managerFor[prev];
        uint256 last = prevMfor.length - 1;
        uint32 moved = prevMfor[last];
        prevMfor[i] = moved;
        managerForIndexes[prev][moved] = i + 1;
        delete(prevMfor[last]);
        prevMfor.length = last;
        managerForIndexes[prev][_point] = 0;
      }
      if (0x0 != _proxy)
      {
        uint32[] storage mfor = managerFor[_proxy];
        mfor.push(_point);
        managerForIndexes[_proxy][_point] = mfor.length;
      }
      deed.managementProxy = _proxy;
      emit ChangedManagementProxy(_point, _proxy);
    }
    function setSpawnProxy(uint32 _point, address _proxy)
      onlyOwner
      external
    {
      Deed storage deed = rights[_point];
      address prev = deed.spawnProxy;
      if (prev == _proxy)
      {
        return;
      }
      if (0x0 != prev)
      {
        uint256 i = spawningForIndexes[prev][_point];
        assert(i > 0);
        i--;
        uint32[] storage prevSfor = spawningFor[prev];
        uint256 last = prevSfor.length - 1;
        uint32 moved = prevSfor[last];
        prevSfor[i] = moved;
        spawningForIndexes[prev][moved] = i + 1;
        delete(prevSfor[last]);
        prevSfor.length = last;
        spawningForIndexes[prev][_point] = 0;
      }
      if (0x0 != _proxy)
      {
        uint32[] storage sfor = spawningFor[_proxy];
        sfor.push(_point);
        spawningForIndexes[_proxy][_point] = sfor.length;
      }
      deed.spawnProxy = _proxy;
      emit ChangedSpawnProxy(_point, _proxy);
    }
    function setVotingProxy(uint32 _point, address _proxy)
      onlyOwner
      external
    {
      Deed storage deed = rights[_point];
      address prev = deed.votingProxy;
      if (prev == _proxy)
      {
        return;
      }
      if (0x0 != prev)
      {
        uint256 i = votingForIndexes[prev][_point];
        assert(i > 0);
        i--;
        uint32[] storage prevVfor = votingFor[prev];
        uint256 last = prevVfor.length - 1;
        uint32 moved = prevVfor[last];
        prevVfor[i] = moved;
        votingForIndexes[prev][moved] = i + 1;
        delete(prevVfor[last]);
        prevVfor.length = last;
        votingForIndexes[prev][_point] = 0;
      }
      if (0x0 != _proxy)
      {
        uint32[] storage vfor = votingFor[_proxy];
        vfor.push(_point);
        votingForIndexes[_proxy][_point] = vfor.length;
      }
      deed.votingProxy = _proxy;
      emit ChangedVotingProxy(_point, _proxy);
    }
    function setTransferProxy(uint32 _point, address _proxy)
      onlyOwner
      external
    {
      Deed storage deed = rights[_point];
      address prev = deed.transferProxy;
      if (prev == _proxy)
      {
        return;
      }
      if (0x0 != prev)
      {
        uint256 i = transferringForIndexes[prev][_point];
        assert(i > 0);
        i--;
        uint32[] storage prevTfor = transferringFor[prev];
        uint256 last = prevTfor.length - 1;
        uint32 moved = prevTfor[last];
        prevTfor[i] = moved;
        transferringForIndexes[prev][moved] = i + 1;
        delete(prevTfor[last]);
        prevTfor.length = last;
        transferringForIndexes[prev][_point] = 0;
      }
      if (0x0 != _proxy)
      {
        uint32[] storage tfor = transferringFor[_proxy];
        tfor.push(_point);
        transferringForIndexes[_proxy][_point] = tfor.length;
      }
      deed.transferProxy = _proxy;
      emit ChangedTransferProxy(_point, _proxy);
    }
    function setOperator(address _owner, address _operator, bool _approved)
      onlyOwner
      external
    {
      operators[_owner][_operator] = _approved;
    }
}
contract ReadsAzimuth
{
  Azimuth public azimuth;
  constructor(Azimuth _azimuth)
    public
  {
    azimuth = _azimuth;
  }
  modifier activePointOwner(uint32 _point)
  {
    require( azimuth.isOwner(_point, msg.sender) &&
             azimuth.isActive(_point) );
    _;
  }
  modifier activePointManager(uint32 _point)
  {
    require( azimuth.canManage(_point, msg.sender) &&
             azimuth.isActive(_point) );
    _;
  }
}
contract Polls is Ownable
{
  using SafeMath for uint256;
  using SafeMath16 for uint16;
  using SafeMath8 for uint8;
  event UpgradePollStarted(address proposal);
  event DocumentPollStarted(bytes32 proposal);
  event UpgradeMajority(address proposal);
  event DocumentMajority(bytes32 proposal);
  struct Poll
  {
    uint256 start;
    bool[256] voted;
    uint16 yesVotes;
    uint16 noVotes;
    uint256 duration;
    uint256 cooldown;
  }
  uint256 public pollDuration;
  uint256 public pollCooldown;
  uint16 public totalVoters;
  address[] public upgradeProposals;
  mapping(address => Poll) public upgradePolls;
  mapping(address => bool) public upgradeHasAchievedMajority;
  bytes32[] public documentProposals;
  mapping(bytes32 => Poll) public documentPolls;
  mapping(bytes32 => bool) public documentHasAchievedMajority;
  bytes32[] public documentMajorities;
  constructor(uint256 _pollDuration, uint256 _pollCooldown)
    public
  {
    reconfigure(_pollDuration, _pollCooldown);
  }
  function reconfigure(uint256 _pollDuration, uint256 _pollCooldown)
    public
    onlyOwner
  {
    require( (5 days <= _pollDuration) && (_pollDuration <= 90 days) &&
             (5 days <= _pollCooldown) && (_pollCooldown <= 90 days) );
    pollDuration = _pollDuration;
    pollCooldown = _pollCooldown;
  }
  function incrementTotalVoters()
    external
    onlyOwner
  {
    require(totalVoters < 256);
    totalVoters = totalVoters.add(1);
  }
  function getUpgradeProposals()
    external
    view
    returns (address[] proposals)
  {
    return upgradeProposals;
  }
  function getUpgradeProposalCount()
    external
    view
    returns (uint256 count)
  {
    return upgradeProposals.length;
  }
  function getDocumentProposals()
    external
    view
    returns (bytes32[] proposals)
  {
    return documentProposals;
  }
  function getDocumentProposalCount()
    external
    view
    returns (uint256 count)
  {
    return documentProposals.length;
  }
  function getDocumentMajorities()
    external
    view
    returns (bytes32[] majorities)
  {
    return documentMajorities;
  }
  function hasVotedOnUpgradePoll(uint8 _galaxy, address _proposal)
    external
    view
    returns (bool result)
  {
    return upgradePolls[_proposal].voted[_galaxy];
  }
  function hasVotedOnDocumentPoll(uint8 _galaxy, bytes32 _proposal)
    external
    view
    returns (bool result)
  {
    return documentPolls[_proposal].voted[_galaxy];
  }
  function startUpgradePoll(address _proposal)
    external
    onlyOwner
  {
    require(!upgradeHasAchievedMajority[_proposal]);
    Poll storage poll = upgradePolls[_proposal];
    if (0 == poll.start)
    {
      upgradeProposals.push(_proposal);
    }
    startPoll(poll);
    emit UpgradePollStarted(_proposal);
  }
  function startDocumentPoll(bytes32 _proposal)
    external
    onlyOwner
  {
    require(!documentHasAchievedMajority[_proposal]);
    Poll storage poll = documentPolls[_proposal];
    if (0 == poll.start)
    {
      documentProposals.push(_proposal);
    }
    startPoll(poll);
    emit DocumentPollStarted(_proposal);
  }
  function startPoll(Poll storage _poll)
    internal
  {
    require( block.timestamp > ( _poll.start.add(
                                 _poll.duration.add(
                                 _poll.cooldown )) ) );
    _poll.start = block.timestamp;
    delete _poll.voted;
    _poll.yesVotes = 0;
    _poll.noVotes = 0;
    _poll.duration = pollDuration;
    _poll.cooldown = pollCooldown;
  }
  function castUpgradeVote(uint8 _as, address _proposal, bool _vote)
    external
    onlyOwner
    returns (bool majority)
  {
    Poll storage poll = upgradePolls[_proposal];
    processVote(poll, _as, _vote);
    return updateUpgradePoll(_proposal);
  }
  function castDocumentVote(uint8 _as, bytes32 _proposal, bool _vote)
    external
    onlyOwner
    returns (bool majority)
  {
    Poll storage poll = documentPolls[_proposal];
    processVote(poll, _as, _vote);
    return updateDocumentPoll(_proposal);
  }
  function processVote(Poll storage _poll, uint8 _as, bool _vote)
    internal
  {
    assert(block.timestamp >= _poll.start);
    require( 
             !_poll.voted[_as] &&
             (block.timestamp < _poll.start.add(_poll.duration)) );
    _poll.voted[_as] = true;
    if (_vote)
    {
      _poll.yesVotes = _poll.yesVotes.add(1);
    }
    else
    {
      _poll.noVotes = _poll.noVotes.add(1);
    }
  }
  function updateUpgradePoll(address _proposal)
    public
    onlyOwner
    returns (bool majority)
  {
    require(!upgradeHasAchievedMajority[_proposal]);
    Poll storage poll = upgradePolls[_proposal];
    majority = checkPollMajority(poll);
    if (majority)
    {
      upgradeHasAchievedMajority[_proposal] = true;
      emit UpgradeMajority(_proposal);
    }
    return majority;
  }
  function updateDocumentPoll(bytes32 _proposal)
    public
    returns (bool majority)
  {
    require(!documentHasAchievedMajority[_proposal]);
    Poll storage poll = documentPolls[_proposal];
    majority = checkPollMajority(poll);
    if (majority)
    {
      documentHasAchievedMajority[_proposal] = true;
      documentMajorities.push(_proposal);
      emit DocumentMajority(_proposal);
    }
    return majority;
  }
  function checkPollMajority(Poll _poll)
    internal
    view
    returns (bool majority)
  {
    return ( 
             (_poll.yesVotes >= (totalVoters / 4)) &&
             (_poll.yesVotes > _poll.noVotes) &&
             ( 
               (block.timestamp > _poll.start.add(_poll.duration)) ||
               ( _poll.yesVotes > totalVoters.sub(_poll.yesVotes) ) ) );
  }
}
contract Claims is ReadsAzimuth
{
  event ClaimAdded( uint32 indexed by,
                    string _protocol,
                    string _claim,
                    bytes _dossier );
  event ClaimRemoved(uint32 indexed by, string _protocol, string _claim);
  uint8 constant maxClaims = 16;
  struct Claim
  {
    string protocol;
    string claim;
    bytes dossier;
  }
  mapping(uint32 => Claim[maxClaims]) public claims;
  constructor(Azimuth _azimuth)
    ReadsAzimuth(_azimuth)
    public
  {
  }
  function addClaim(uint32 _point,
                    string _protocol,
                    string _claim,
                    bytes _dossier)
    external
    activePointManager(_point)
  {
    uint8 cur = findClaim(_point, _protocol, _claim);
    if (cur == 0)
    {
      uint8 empty = findEmptySlot(_point);
      claims[_point][empty] = Claim(_protocol, _claim, _dossier);
    }
    else
    {
      claims[_point][cur-1] = Claim(_protocol, _claim, _dossier);
    }
    emit ClaimAdded(_point, _protocol, _claim, _dossier);
  }
  function removeClaim(uint32 _point, string _protocol, string _claim)
    external
    activePointManager(_point)
  {
    uint256 i = findClaim(_point, _protocol, _claim);
    require(i > 0);
    i--;
    delete claims[_point][i];
    emit ClaimRemoved(_point, _protocol, _claim);
  }
  function clearClaims(uint32 _point)
    external
  {
    require( azimuth.canManage(_point, msg.sender) ||
             ( msg.sender == azimuth.owner() ) );
    Claim[maxClaims] storage currClaims = claims[_point];
    for (uint8 i = 0; i < maxClaims; i++)
    {
      delete currClaims[i];
    }
  }
  function findClaim(uint32 _whose, string _protocol, string _claim)
    public
    view
    returns (uint8 index)
  {
    bytes32 protocolHash = keccak256(bytes(_protocol));
    bytes32 claimHash = keccak256(bytes(_claim));
    Claim[maxClaims] storage theirClaims = claims[_whose];
    for (uint8 i = 0; i < maxClaims; i++)
    {
      Claim storage thisClaim = theirClaims[i];
      if ( ( protocolHash == keccak256(bytes(thisClaim.protocol)) ) &&
           ( claimHash == keccak256(bytes(thisClaim.claim)) ) )
      {
        return i+1;
      }
    }
    return 0;
  }
  function findEmptySlot(uint32 _whose)
    internal
    view
    returns (uint8 index)
  {
    Claim[maxClaims] storage theirClaims = claims[_whose];
    for (uint8 i = 0; i < maxClaims; i++)
    {
      Claim storage thisClaim = theirClaims[i];
      if ( (0 == bytes(thisClaim.protocol).length) &&
           (0 == bytes(thisClaim.claim).length) )
      {
        return i;
      }
    }
    revert();
  }
}
contract EclipticBase is Ownable, ReadsAzimuth
{
  event Upgraded(address to);
  Polls public polls;
  address public previousEcliptic;
  constructor( address _previous,
               Azimuth _azimuth,
               Polls _polls )
    ReadsAzimuth(_azimuth)
    internal
  {
    previousEcliptic = _previous;
    polls = _polls;
  }
  function onUpgrade()
    external
  {
    require( msg.sender == previousEcliptic &&
             this == azimuth.owner() &&
             this == polls.owner() );
  }
  function upgrade(EclipticBase _new)
    internal
  {
    azimuth.transferOwnership(_new);
    polls.transferOwnership(_new);
    _new.onUpgrade();
    emit Upgraded(_new);
    selfdestruct(_new);
  }
}
contract Ecliptic is EclipticBase, SupportsInterfaceWithLookup, ERC721Metadata
{
  using SafeMath for uint256;
  using AddressUtils for address;
  event Transfer(address indexed _from, address indexed _to, uint256 _tokenId);
  event Approval(address indexed _owner, address indexed _approved,
                 uint256 _tokenId);
  event ApprovalForAll(address indexed _owner, address indexed _operator,
                       bool _approved);
  bytes4 constant erc721Received = 0x150b7a02;
  Claims public claims;
  constructor(address _previous,
              Azimuth _azimuth,
              Polls _polls,
              Claims _claims)
    EclipticBase(_previous, _azimuth, _polls)
    public
  {
    claims = _claims;
    _registerInterface(0x80ac58cd); 
    _registerInterface(0x5b5e139f); 
    _registerInterface(0x7f5828d0); 
  }
    function balanceOf(address _owner)
      public
      view
      returns (uint256 balance)
    {
      require(0x0 != _owner);
      return azimuth.getOwnedPointCount(_owner);
    }
    function ownerOf(uint256 _tokenId)
      public
      view
      validPointId(_tokenId)
      returns (address owner)
    {
      uint32 id = uint32(_tokenId);
      require(azimuth.isActive(id));
      return azimuth.getOwner(id);
    }
    function exists(uint256 _tokenId)
      public
      view
      returns (bool doesExist)
    {
      return ( (_tokenId < 0x100000000) &&
               azimuth.isActive(uint32(_tokenId)) );
    }
    function safeTransferFrom(address _from, address _to, uint256 _tokenId)
      public
    {
      safeTransferFrom(_from, _to, _tokenId, "");
    }
    function safeTransferFrom(address _from, address _to, uint256 _tokenId,
                              bytes _data)
      public
    {
      transferFrom(_from, _to, _tokenId);
      if (_to.isContract())
      {
        bytes4 retval = ERC721Receiver(_to)
                        .onERC721Received(msg.sender, _from, _tokenId, _data);
        require(retval == erc721Received);
      }
    }
    function transferFrom(address _from, address _to, uint256 _tokenId)
      public
      validPointId(_tokenId)
    {
      uint32 id = uint32(_tokenId);
      require(azimuth.isOwner(id, _from));
      transferPoint(id, _to, true);
    }
    function approve(address _approved, uint256 _tokenId)
      public
      validPointId(_tokenId)
    {
      setTransferProxy(uint32(_tokenId), _approved);
    }
    function setApprovalForAll(address _operator, bool _approved)
      public
    {
      require(0x0 != _operator);
      azimuth.setOperator(msg.sender, _operator, _approved);
      emit ApprovalForAll(msg.sender, _operator, _approved);
    }
    function getApproved(uint256 _tokenId)
      public
      view
      validPointId(_tokenId)
      returns (address approved)
    {
      require(azimuth.isActive(uint32(_tokenId)));
      return azimuth.getTransferProxy(uint32(_tokenId));
    }
    function isApprovedForAll(address _owner, address _operator)
      public
      view
      returns (bool result)
    {
      return azimuth.isOperator(_owner, _operator);
    }
    function name()
      external
      view
      returns (string)
    {
      return "Azimuth Points";
    }
    function symbol()
      external
      view
      returns (string)
    {
      return "AZP";
    }
    function tokenURI(uint256 _tokenId)
      public
      view
      validPointId(_tokenId)
      returns (string _tokenURI)
    {
      _tokenURI = "https://azimuth.network/erc721/0000000000.json";
      bytes memory _tokenURIBytes = bytes(_tokenURI);
      _tokenURIBytes[31] = byte(48+(_tokenId / 1000000000) % 10);
      _tokenURIBytes[32] = byte(48+(_tokenId / 100000000) % 10);
      _tokenURIBytes[33] = byte(48+(_tokenId / 10000000) % 10);
      _tokenURIBytes[34] = byte(48+(_tokenId / 1000000) % 10);
      _tokenURIBytes[35] = byte(48+(_tokenId / 100000) % 10);
      _tokenURIBytes[36] = byte(48+(_tokenId / 10000) % 10);
      _tokenURIBytes[37] = byte(48+(_tokenId / 1000) % 10);
      _tokenURIBytes[38] = byte(48+(_tokenId / 100) % 10);
      _tokenURIBytes[39] = byte(48+(_tokenId / 10) % 10);
      _tokenURIBytes[40] = byte(48+(_tokenId / 1) % 10);
    }
    function configureKeys(uint32 _point,
                           bytes32 _encryptionKey,
                           bytes32 _authenticationKey,
                           uint32 _cryptoSuiteVersion,
                           bool _discontinuous)
      external
      activePointManager(_point)
    {
      if (_discontinuous)
      {
        azimuth.incrementContinuityNumber(_point);
      }
      azimuth.setKeys(_point,
                      _encryptionKey,
                      _authenticationKey,
                      _cryptoSuiteVersion);
    }
    function spawn(uint32 _point, address _target)
      external
    {
      require(azimuth.isOwner(_point, 0x0));
      uint16 prefix = azimuth.getPrefix(_point);
      require( (uint8(azimuth.getPointSize(prefix)) + 1) ==
               uint8(azimuth.getPointSize(_point)) );
      require( (azimuth.hasBeenLinked(prefix)) &&
               ( azimuth.getSpawnCount(prefix) <
                 getSpawnLimit(prefix, block.timestamp) ) );
      require( azimuth.canSpawnAs(prefix, msg.sender) );
      if (msg.sender == _target)
      {
        doSpawn(_point, _target, true, 0x0);
      }
      else
      {
        doSpawn(_point, _target, false, azimuth.getOwner(prefix));
      }
    }
    function doSpawn( uint32 _point,
                      address _target,
                      bool _direct,
                      address _holder )
      internal
    {
      azimuth.registerSpawned(_point);
      if (_direct)
      {
        azimuth.activatePoint(_point);
        azimuth.setOwner(_point, _target);
        emit Transfer(0x0, _target, uint256(_point));
      }
      else
      {
        azimuth.setOwner(_point, _holder);
        azimuth.setTransferProxy(_point, _target);
        emit Transfer(0x0, _holder, uint256(_point));
        emit Approval(_holder, _target, uint256(_point));
      }
    }
    function transferPoint(uint32 _point, address _target, bool _reset)
      public
    {
      require(azimuth.canTransfer(_point, msg.sender));
      if ( !azimuth.isActive(_point) )
      {
        azimuth.activatePoint(_point);
      }
      if ( !azimuth.isOwner(_point, _target) )
      {
        address old = azimuth.getOwner(_point);
        azimuth.setOwner(_point, _target);
        azimuth.setTransferProxy(_point, 0);
        emit Transfer(old, _target, uint256(_point));
      }
      if ( _reset )
      {
        if ( azimuth.hasBeenLinked(_point) )
        {
          azimuth.incrementContinuityNumber(_point);
          azimuth.setKeys(_point, 0, 0, 0);
        }
        azimuth.setManagementProxy(_point, 0);
        azimuth.setVotingProxy(_point, 0);
        azimuth.setTransferProxy(_point, 0);
        azimuth.setSpawnProxy(_point, 0);
        claims.clearClaims(_point);
      }
    }
    function escape(uint32 _point, uint32 _sponsor)
      external
      activePointManager(_point)
    {
      require(canEscapeTo(_point, _sponsor));
      azimuth.setEscapeRequest(_point, _sponsor);
    }
    function cancelEscape(uint32 _point)
      external
      activePointManager(_point)
    {
      azimuth.cancelEscape(_point);
    }
    function adopt(uint32 _point)
      external
    {
      require( azimuth.isEscaping(_point) &&
               azimuth.canManage( azimuth.getEscapeRequest(_point),
                                  msg.sender ) );
      azimuth.doEscape(_point);
    }
    function reject(uint32 _point)
      external
    {
      require( azimuth.isEscaping(_point) &&
               azimuth.canManage( azimuth.getEscapeRequest(_point),
                                  msg.sender ) );
      azimuth.cancelEscape(_point);
    }
    function detach(uint32 _point)
      external
    {
      require( azimuth.hasSponsor(_point) &&
               azimuth.canManage(azimuth.getSponsor(_point), msg.sender) );
      azimuth.loseSponsor(_point);
    }
    function getSpawnLimit(uint32 _point, uint256 _time)
      public
      view
      returns (uint32 limit)
    {
      Azimuth.Size size = azimuth.getPointSize(_point);
      if ( size == Azimuth.Size.Galaxy )
      {
        return 255;
      }
      else if ( size == Azimuth.Size.Star )
      {
        uint256 yearsSince2019 = (_time - 1546300800) / 365 days;
        if (yearsSince2019 < 6)
        {
          limit = uint32( 1024 * (2 ** yearsSince2019) );
        }
        else
        {
          limit = 65535;
        }
        return limit;
      }
      else  
      {
        return 0;
      }
    }
    function canEscapeTo(uint32 _point, uint32 _sponsor)
      public
      view
      returns (bool canEscape)
    {
      if ( !azimuth.hasBeenLinked(_sponsor) ) return false;
      Azimuth.Size pointSize = azimuth.getPointSize(_point);
      Azimuth.Size sponsorSize = azimuth.getPointSize(_sponsor);
      return ( 
               ( (uint8(sponsorSize) + 1) == uint8(pointSize) ) ||
               ( (sponsorSize == pointSize) &&
                 !azimuth.hasBeenLinked(_point) ) );
    }
    function setManagementProxy(uint32 _point, address _manager)
      external
      activePointOwner(_point)
    {
      azimuth.setManagementProxy(_point, _manager);
    }
    function setSpawnProxy(uint16 _prefix, address _spawnProxy)
      external
      activePointOwner(_prefix)
    {
      azimuth.setSpawnProxy(_prefix, _spawnProxy);
    }
    function setVotingProxy(uint8 _galaxy, address _voter)
      external
      activePointOwner(_galaxy)
    {
      azimuth.setVotingProxy(_galaxy, _voter);
    }
    function setTransferProxy(uint32 _point, address _transferProxy)
      public
    {
      address owner = azimuth.getOwner(_point);
      require((owner == msg.sender) || azimuth.isOperator(owner, msg.sender));
      azimuth.setTransferProxy(_point, _transferProxy);
      emit Approval(owner, _transferProxy, uint256(_point));
    }
    function startUpgradePoll(uint8 _galaxy, EclipticBase _proposal)
      external
      activePointVoter(_galaxy)
    {
      require(_proposal.previousEcliptic() == address(this));
      polls.startUpgradePoll(_proposal);
    }
    function startDocumentPoll(uint8 _galaxy, bytes32 _proposal)
      external
      activePointVoter(_galaxy)
    {
      polls.startDocumentPoll(_proposal);
    }
    function castUpgradeVote(uint8 _galaxy,
                              EclipticBase _proposal,
                              bool _vote)
      external
      activePointVoter(_galaxy)
    {
      bool majority = polls.castUpgradeVote(_galaxy, _proposal, _vote);
      if (majority)
      {
        upgrade(_proposal);
      }
    }
    function castDocumentVote(uint8 _galaxy, bytes32 _proposal, bool _vote)
      external
      activePointVoter(_galaxy)
    {
      polls.castDocumentVote(_galaxy, _proposal, _vote);
    }
    function updateUpgradePoll(EclipticBase _proposal)
      external
    {
      bool majority = polls.updateUpgradePoll(_proposal);
      if (majority)
      {
        upgrade(_proposal);
      }
    }
    function updateDocumentPoll(bytes32 _proposal)
      external
    {
      polls.updateDocumentPoll(_proposal);
    }
    function createGalaxy(uint8 _galaxy, address _target)
      external
      onlyOwner
    {
      require( azimuth.isOwner(_galaxy, 0x0) &&
               0x0 != _target );
      polls.incrementTotalVoters();
      if (msg.sender == _target)
      {
        doSpawn(_galaxy, _target, true, 0x0);
      }
      else
      {
        doSpawn(_galaxy, _target, false, msg.sender);
      }
    }
    function setDnsDomains(string _primary, string _secondary, string _tertiary)
      external
      onlyOwner
    {
      azimuth.setDnsDomains(_primary, _secondary, _tertiary);
    }
    modifier validPointId(uint256 _id)
    {
      require(_id < 0x100000000);
      _;
    }
    modifier activePointVoter(uint32 _point)
    {
      require( azimuth.canVoteAs(_point, msg.sender) &&
               azimuth.isActive(_point) );
      _;
    }
}

```

## RQ1_bb52ee421443

SHA-256 `b7b0d85df2fb2b8d7a41d341ff6c5166406ab576502997bdb5742f6ac72be0c5`

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

SHA-256 `e20fc6369b56bc572b3b2bbc9523b05dd14fe76a3e0861b712977eebf492e013`

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

## RQ1_fbc7ca489536

SHA-256 `ab42a0c69eae3126343d09d092b107de39139702555b8c00282324cc2d4683d1`

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
contract Owned {
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
contract StandardToken is Token, Owned {
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
    function distributeToken(address[] addresses, uint256 _value) {
     for (uint i = 0; i < addresses.length; i++) {
         balances[msg.sender] -= _value;
         balances[addresses[i]] += _value;
         Transfer(msg.sender, addresses[i], _value);
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
contract B2X is StandardToken {
    function () {
        throw;
    }
    string public name;                   
    uint8 public decimals;                
    string public symbol;                 
    function B2X(
        ) {
        totalSupply = 21 * 10 ** 14;
        balances[msg.sender] = totalSupply;              
        name = "BTC2X";                                   
        decimals = 8;                            
        symbol = "B2X";                               
    }
}
```

## RQ1_fc71e6703f0d

SHA-256 `bf43b6ed5ca2b625a9de217ac06e7ea4ddf63acadeee0d64d0c562d6ce1710e5`

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

## RQ1_c682dc91e18c

SHA-256 `b6d44daeccb0e2ed7850b66c3e3c32f10b8d51dbd89270c856cabf5ebed929be`

```solidity
pragma solidity ^0.4.20;
contract X2Equal
{
    address Owner = msg.sender;
    function() public payable {}
    function cancel() payable public {
        if (msg.sender == Owner) {
            selfdestruct(Owner);
        }
    }
    function X2() public payable {
        if (msg.value >= this.balance) {
            selfdestruct(msg.sender);
        }
    }
}
```

## RQ1_cc6f48967dd0

SHA-256 `d4ee82b6e74ec4032fcaab14e78f373b218eba6e30958fc57d7754aa1f9b5858`

```solidity
pragma solidity 0.4.24;
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
contract RBAC {
  using Roles for Roles.Role;
  mapping (string => Roles.Role) private roles;
  event RoleAdded(address addr, string roleName);
  event RoleRemoved(address addr, string roleName);
  function checkRole(address addr, string roleName)
    view
    public
  {
    roles[roleName].check(addr);
  }
  function hasRole(address addr, string roleName)
    view
    public
    returns (bool)
  {
    return roles[roleName].has(addr);
  }
  function addRole(address addr, string roleName)
    internal
  {
    roles[roleName].add(addr);
    emit RoleAdded(addr, roleName);
  }
  function removeRole(address addr, string roleName)
    internal
  {
    roles[roleName].remove(addr);
    emit RoleRemoved(addr, roleName);
  }
  modifier onlyRole(string roleName)
  {
    checkRole(msg.sender, roleName);
    _;
  }
}
contract RBACWithAdmin is RBAC {
  string public constant ROLE_ADMIN = "admin";
  modifier onlyAdmin()
  {
    checkRole(msg.sender, ROLE_ADMIN);
    _;
  }
  function RBACWithAdmin()
    public
  {
    addRole(msg.sender, ROLE_ADMIN);
  }
  function adminAddRole(address addr, string roleName)
    onlyAdmin
    public
  {
    addRole(addr, roleName);
  }
  function adminRemoveRole(address addr, string roleName)
    onlyAdmin
    public
  {
    removeRole(addr, roleName);
  }
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
contract ERC20 {
    function balanceOf(address _owner) public constant returns (uint256 balance);
    function transfer(address _to, uint256 _value) public returns (bool success);
}
contract FacultyPool is RBACWithAdmin {
    using SafeMath for uint;
    uint8 constant CONTRACT_OPEN = 1;
    uint8 constant CONTRACT_CLOSED = 2;
    uint8 constant CONTRACT_SUBMIT_FUNDS = 3;
    uint256 constant public gasLimit = 50000000000;
    uint256 constant public minContribution = 100000000000000000;
    address public owner;
    uint256 public feePct;
    uint8 public contractStage = CONTRACT_OPEN;
    uint256 public currentBeneficiaryCap;
    uint256 public totalPoolCap;
    address public receiverAddress;
    mapping (address => Beneficiary) beneficiaries;
    uint256 public finalBalance;
    uint256[] public ethRefundAmount;
    mapping (address => TokenAllocation) tokenAllocationMap;
    address public defaultToken;
    modifier isOpenContract() {
        require (contractStage == CONTRACT_OPEN);
        _;
    }
    bool locked;
    modifier noReentrancy() {
        require(!locked);
        locked = true;
        _;
        locked = false;
    }
    struct Beneficiary {
        uint256 ethRefund;
        uint256 balance;
        uint256 cap;
        mapping (address => uint256) tokensClaimed;
    }
    struct TokenAllocation {
        ERC20 token;
        uint256[] pct;
        uint256 balanceRemaining;
    }
    event BeneficiaryBalanceChanged(address indexed beneficiary, uint256 totalBalance);
    event ReceiverAddressSet(address indexed receiverAddress);
    event ERC223Received(address indexed token, uint256 value);
    event DepositReceived(address indexed beneficiary, uint256 amount, uint256 gas, uint256 gasprice, uint256 gasLimit);
    event PoolStageChanged(uint8 stage);
    event PoolSubmitted(address indexed receiver, uint256 amount);
    event RefundReceived(address indexed sender, uint256 amount);
    event TokenWithdrawal(address indexed beneficiary, address indexed token, uint256 amount);
    event EthRefunded(address indexed beneficiary, uint256 amount);
    constructor(address[] _admins, uint256 _poolCap, uint256 _beneficiaryCap, address _receiverAddr, uint256 _feePct) public {
        require(_admins.length > 0, "Must have at least one admin apart from msg.sender");
        require(_poolCap >= _beneficiaryCap, "Cannot have the poolCap <= beneficiaryCap");
        require(_feePct >=  0 && _feePct < 10000);
        feePct = _feePct;
        receiverAddress = _receiverAddr;
        totalPoolCap = _poolCap;
        currentBeneficiaryCap = _beneficiaryCap;
        owner = msg.sender;
        addRole(msg.sender, ROLE_ADMIN);
        for (uint8 i = 0; i < _admins.length; i++) {
            addRole(_admins[i], ROLE_ADMIN);
        }
    }
    function () payable public {
        if (contractStage == CONTRACT_OPEN) {
            emit DepositReceived(msg.sender, msg.value, gasleft(), tx.gasprice, gasLimit);
            _receiveDeposit();
        } else {
            _receiveRefund();
        }
    }
    function _receiveDeposit() isOpenContract internal {
        require(tx.gasprice <= gasLimit, "Gas too high");
        require(address(this).balance <= totalPoolCap, "Deposit will put pool over limit. Reverting.");
        Beneficiary storage b = beneficiaries[msg.sender];
        uint256 newBalance = b.balance.add(msg.value);
        require(newBalance >= minContribution, "contribution is lower than minContribution");
        if(b.cap > 0){
            require(newBalance <= b.cap, "balance is less than set cap for beneficiary");
        } else if(currentBeneficiaryCap == 0) {
            b.cap = totalPoolCap;
        }else {
            require(newBalance <= currentBeneficiaryCap, "balance is more than currentBeneficiaryCap");
            b.cap = currentBeneficiaryCap;
        }
        b.balance = newBalance;
        emit BeneficiaryBalanceChanged(msg.sender, newBalance);
    }
    function _receiveRefund() internal {
        assert(contractStage >= 2);
        require(hasRole(msg.sender, ROLE_ADMIN) || msg.sender == receiverAddress, "Receiver or Admins only");
        ethRefundAmount.push(msg.value);
        emit RefundReceived(msg.sender, msg.value);
    }
    function getCurrentBeneficiaryCap() public view returns(uint256 cap) {
        return currentBeneficiaryCap;
    }
    function getPoolDetails() public view returns(uint256 total, uint256 currentBalance, uint256 remaining) {
        remaining = totalPoolCap.sub(address(this).balance);
        return (totalPoolCap, address(this).balance, remaining);
    }
    function closePool() onlyAdmin isOpenContract public {
        contractStage = CONTRACT_CLOSED;
        emit PoolStageChanged(contractStage);
    }
    function submitPool(uint256 weiAmount) public onlyAdmin noReentrancy {
        require(contractStage < CONTRACT_SUBMIT_FUNDS, "Cannot resubmit pool.");
        require(receiverAddress != 0x00, "receiver address cannot be empty");
        uint256 contractBalance = address(this).balance;
        if(weiAmount == 0){
            weiAmount = contractBalance;
        }
        require(minContribution <= weiAmount && weiAmount <= contractBalance, "submitted amount too small or larger than the balance");
        finalBalance = contractBalance;
        require(receiverAddress.call.value(weiAmount)
            .gas(gasleft().sub(5000))(),
            "Error submitting pool to receivingAddress");
        contractBalance = address(this).balance;
        if(contractBalance > 0) {
            ethRefundAmount.push(contractBalance);
        }
        contractStage = CONTRACT_SUBMIT_FUNDS;
        emit PoolSubmitted(receiverAddress, weiAmount);
    }
    function viewBeneficiaryDetails(address beneficiary) public view returns (uint256 cap, uint256 balance, uint256 remaining, uint256 ethRefund){
        Beneficiary storage b = beneficiaries[beneficiary];
        return (b.cap, b.balance, b.cap.sub(b.balance), b.ethRefund);
    }
    function withdraw(address _tokenAddress) public {
        Beneficiary storage b = beneficiaries[msg.sender];
        require(b.balance > 0, "msg.sender has no balance. Nice Try!");
        if(contractStage == CONTRACT_OPEN){
            uint256 transferAmt = b.balance;
            b.balance = 0;
            msg.sender.transfer(transferAmt);
            emit BeneficiaryBalanceChanged(msg.sender, 0);
        } else {
            _withdraw(msg.sender, _tokenAddress);
        }
    }
    function withdrawFor (address _beneficiary, address tokenAddr) public onlyAdmin {
        require (contractStage == CONTRACT_SUBMIT_FUNDS, "Can only be done on Submitted Contract");
        require (beneficiaries[_beneficiary].balance > 0, "Beneficary has no funds to withdraw");
        _withdraw(_beneficiary, tokenAddr);
    }
    function _withdraw (address _beneficiary, address _tokenAddr) internal {
        require(contractStage == CONTRACT_SUBMIT_FUNDS, "Cannot withdraw when contract is not CONTRACT_SUBMIT_FUNDS");
        Beneficiary storage b = beneficiaries[_beneficiary];
        if (_tokenAddr == 0x00) {
            _tokenAddr = defaultToken;
        }
        TokenAllocation storage ta = tokenAllocationMap[_tokenAddr];
        require ( (ethRefundAmount.length > b.ethRefund) || ta.pct.length > b.tokensClaimed[_tokenAddr] );
        if (ethRefundAmount.length > b.ethRefund) {
            uint256 pct = _toPct(b.balance,finalBalance);
            uint256 ethAmount = 0;
            for (uint i= b.ethRefund; i < ethRefundAmount.length; i++) {
                ethAmount = ethAmount.add(_applyPct(ethRefundAmount[i],pct));
            }
            b.ethRefund = ethRefundAmount.length;
            if (ethAmount > 0) {
                _beneficiary.transfer(ethAmount);
                emit EthRefunded(_beneficiary, ethAmount);
            }
        }
        if (ta.pct.length > b.tokensClaimed[_tokenAddr]) {
            uint tokenAmount = 0;
            for (i= b.tokensClaimed[_tokenAddr]; i< ta.pct.length; i++) {
                tokenAmount = tokenAmount.add(_applyPct(b.balance, ta.pct[i]));
            }
            b.tokensClaimed[_tokenAddr] = ta.pct.length;
            if (tokenAmount > 0) {
                require(ta.token.transfer(_beneficiary,tokenAmount));
                ta.balanceRemaining = ta.balanceRemaining.sub(tokenAmount);
                emit TokenWithdrawal(_beneficiary, _tokenAddr, tokenAmount);
            }
        }
    }
    function setReceiver(address addr) public onlyAdmin {
        require (contractStage < CONTRACT_SUBMIT_FUNDS);
        receiverAddress = addr;
        emit ReceiverAddressSet(addr);
    }
    function enableTokenWithdrawals (address _tokenAddr, bool _useAsDefault) public onlyAdmin noReentrancy {
        require (contractStage == CONTRACT_SUBMIT_FUNDS, "wrong contract stage");
        if (_useAsDefault) {
            defaultToken = _tokenAddr;
        } else {
            require (defaultToken != 0x00, "defaultToken must be set");
        }
        TokenAllocation storage ta  = tokenAllocationMap[_tokenAddr];
        if (ta.pct.length==0){
            ta.token = ERC20(_tokenAddr);
        }
        uint256 amount = ta.token.balanceOf(this).sub(ta.balanceRemaining);
        require (amount > 0);
        if (feePct > 0) {
            uint256 feePctFromBips = _toPct(feePct, 10000);
            uint256 feeAmount = _applyPct(amount, feePctFromBips);
            require (ta.token.transfer(owner, feeAmount));
            emit TokenWithdrawal(owner, _tokenAddr, feeAmount);
        }
        amount = ta.token.balanceOf(this).sub(ta.balanceRemaining);
        ta.balanceRemaining = ta.token.balanceOf(this);
        ta.pct.push(_toPct(amount,finalBalance));
    }
    function checkAvailableTokens (address addr, address tokenAddr) view public returns (uint tokenAmount) {
        Beneficiary storage b = beneficiaries[addr];
        TokenAllocation storage ta = tokenAllocationMap[tokenAddr];
        for (uint i = b.tokensClaimed[tokenAddr]; i < ta.pct.length; i++) {
            tokenAmount = tokenAmount.add(_applyPct(b.balance, ta.pct[i]));
        }
        return tokenAmount;
    }
    function tokenFallback (address from, uint value, bytes data) public {
        emit ERC223Received (from, value);
    }
    function _toPct (uint numerator, uint denominator ) internal pure returns (uint) {
        return numerator.mul(10 ** 20) / denominator;
    }
    function _applyPct (uint numerator, uint pct) internal pure returns (uint) {
        return numerator.mul(pct) / (10 ** 20);
    }
}
```

## RQ1_0b9a9d5a2319

SHA-256 `b166fdc614862ee48201815fd20beeb77d06d7f950875f58c5a0dbfadc115b10`

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

## RQ1_be415055dd52

SHA-256 `41d4374c0f6d443be1508aac31c6ad32d4b9439fe983f9d3bc7626b7825ce563`

```solidity
pragma solidity ^0.4.18;
contract ERC721 {
    function totalSupply() public view returns (uint256 total);
    function balanceOf(address _owner) public view returns (uint256 balance);
    function ownerOf(uint256 _tokenId) external view returns (address owner);
    function approve(address _to, uint256 _tokenId) external;
    function transfer(address _to, uint256 _tokenId) external;
    function transferFrom(address _from, address _to, uint256 _tokenId) external;
    event Transfer(address from, address to, uint256 tokenId);
    event Approval(address owner, address approved, uint256 tokenId);
}
interface TulipsSaleInterface {
    function putOnInitialSale(uint256 tulipId) external;
    function createAuction(
        uint256 _tulipId,
        uint256 _startingPrice,
        uint256 _endingPrice,
        uint256 _duration,
        address _transferFrom
    )external;
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
    require(!paused);
    _;
  }
  modifier whenPaused() {
    require(paused);
    _;
  }
  function pause() onlyOwner whenNotPaused public {
    paused = true;
    Pause();
  }
  function unpause() onlyOwner whenPaused public {
    paused = false;
    Unpause();
  }
}
contract TulipsRoles is Pausable {
    modifier onlyFinancial() {
        require(msg.sender == address(financialAccount));
        _;
    }
    modifier onlyOperations() {
        require(msg.sender == address(operationsAccount));
        _;
    }
    function TulipsRoles() Ownable() public {
        financialAccount = msg.sender;
        operationsAccount = msg.sender;
    }
    address public financialAccount;
    address public operationsAccount;
    function transferFinancial(address newFinancial) public onlyOwner {
        require(newFinancial != address(0));
        financialAccount = newFinancial;
    }
    function transferOperations(address newOperations) public onlyOwner {
        require(newOperations != address(0));
        operationsAccount = newOperations;
    }
}
contract TulipsSaleAuction is TulipsRoles, TulipsSaleInterface {
    modifier onlyCoreContract() {
        require(msg.sender == address(coreContract));
        _;
    }
    struct Auction {
        address seller;
        uint128 startingPrice;
        uint128 endingPrice;
        uint64 duration;
        uint64 startedAt;
    }
    ERC721 public coreContract;
    uint256 public ownerCut;
    uint256 public initialStartPrice;
    uint256 public initialEndPrice;
    uint256 public initialSaleDuration = 1 days;
    mapping (uint256 => Auction) public tokenIdToAuction;
    event AuctionCreated(uint256 tokenId, uint256 startingPrice, uint256 endingPrice, uint256 duration);
    event AuctionSuccessful(uint256 tokenId, uint256 totalPrice, address winner);
    event AuctionCancelled(uint256 tokenId);
    function TulipsSaleAuction(address _tulipsCoreContract, uint256 _cut) TulipsRoles() public {
        require(_cut <= 10000); 
        ownerCut = _cut;
        coreContract = ERC721(_tulipsCoreContract);
    }
    function setDefaultAuctionPrices(uint256 _startPrice, uint256 _endPrice) external onlyFinancial {
        initialStartPrice = _startPrice;
        initialEndPrice = _endPrice;
    }
    function recievePayout(uint payoutAmount, address payoutAddress) external onlyFinancial {
        require(payoutAddress != 0);
        payoutAddress.transfer(payoutAmount);
    }
    function putOnInitialSale(uint256 _tulipId) external onlyCoreContract {
        _createAuction(_tulipId, initialStartPrice, initialEndPrice, initialSaleDuration, this);
    }
    function createAuction(
        uint256 _tulipId,
        uint256 _startingPrice,
        uint256 _endingPrice,
        uint256 _duration,
        address _transferFrom
    )external
    {
        require(_startingPrice == uint256(uint128(_startingPrice)));
        require(_endingPrice == uint256(uint128(_endingPrice)));
        require(_duration == uint256(uint64(_duration)));
        require(_duration >= 1 minutes);
        require(coreContract.ownerOf(_tulipId) == _transferFrom);
        coreContract.transferFrom(_transferFrom, this, _tulipId);
        _createAuction(_tulipId, _startingPrice, _endingPrice, _duration, _transferFrom);
    }
    function _createAuction(
        uint256 _tulipId,
        uint256 _startingPrice,
        uint256 _endingPrice,
        uint256 _duration,
        address _seller
    )
        internal
    {
        Auction memory auction = Auction(
            _seller,
            uint128(_startingPrice),
            uint128(_endingPrice),
            uint64(_duration),
            uint64(now)
        );
        tokenIdToAuction[_tulipId] = auction;
        AuctionCreated(
            uint256(_tulipId),
            uint256(auction.startingPrice),
            uint256(auction.endingPrice),
            uint256(auction.duration)
        );
    }
    function cancelAuction(uint256 _tulipId)
        external
    {
        Auction storage auction = tokenIdToAuction[_tulipId];
        require(auction.startedAt > 0);
        address seller = auction.seller;
        require(msg.sender == seller);
        coreContract.transfer(seller, _tulipId);
        delete tokenIdToAuction[_tulipId];
        AuctionCancelled(_tulipId);
    }
    function buy(uint256 _tulipId)
        external
        payable
        whenNotPaused
    {
        Auction storage auction = tokenIdToAuction[_tulipId];
        require(auction.startedAt > 0);
        uint256 price = _currentPrice(auction);
        require(msg.value >= price);
        address seller = auction.seller;
        delete tokenIdToAuction[_tulipId];
        if (price > 0 && seller != address(this)) {
            uint256 auctioneerCut = _computeCut(price);
            uint256 sellerGains = price - auctioneerCut;
            seller.transfer(sellerGains);
        }
        uint256 bidExcess = msg.value - price;
        msg.sender.transfer(bidExcess);
        coreContract.transfer(msg.sender, _tulipId);
        AuctionSuccessful(_tulipId, price, msg.sender);
    }
    function secondsPassed(uint256 _tulipId )external view
       returns (uint256)
    {
        Auction storage auction = tokenIdToAuction[_tulipId];
        uint256 secondsPassed = 0;
        if (now > auction.startedAt) {
            secondsPassed = now - auction.startedAt;
        }
        return secondsPassed;
    }
    function currentPrice(uint256 _tulipId) external view
        returns (uint256)
    {
        Auction storage auction = tokenIdToAuction[_tulipId];
        require(auction.startedAt > 0);
        return _currentPrice(auction);
    }
    function _currentPrice(Auction storage _auction)
        internal
        view
        returns (uint256)
    {
        uint256 secondsPassed = 0;
        if (now > _auction.startedAt) {
            secondsPassed = now - _auction.startedAt;
        }
        return _computeCurrentPrice(
            _auction.startingPrice,
            _auction.endingPrice,
            _auction.duration,
            secondsPassed
        );
    }
    function _computeCurrentPrice(
        uint256 _startingPrice,
        uint256 _endingPrice,
        uint256 _duration,
        uint256 _secondsPassed
    )
        internal
        pure
        returns (uint256)
    {
        if (_secondsPassed >= _duration) {
            return _endingPrice;
        } else {
            int256 totalPriceChange = int256(_endingPrice) - int256(_startingPrice);
            int256 currentPriceChange = totalPriceChange * int256(_secondsPassed) / int256(_duration);
            int256 currentPrice = int256(_startingPrice) + currentPriceChange;
            return uint256(currentPrice);
        }
    }
    function _computeCut(uint256 _price) internal view returns (uint256) {
        return _price * ownerCut / 10000;
    }
}
```

## RQ1_f4232c234a28

SHA-256 `28c4d86f22e862938433929a4e246a70445c0c1f938899597f052bc74c0cef7f`

```solidity
pragma solidity ^0.4.19;
contract SelfKeyToken {
    string public name = "SelfKey Token";
    string public symbol = "KEY";
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
    function SelfKeyToken() public {
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

## RQ1_356ce1d2c1cd

SHA-256 `b9c6e2b347e0689183c193489822c98eb8c56131cd42adcbd4ec07faae6badea`

```solidity
pragma solidity ^0.4.24;
interface ERC721  {
    event Transfer(address indexed _from, address indexed _to, uint256 indexed _tokenId);
    event Approval(address indexed _owner, address indexed _approved, uint256 indexed _tokenId);
    event ApprovalForAll(address indexed _owner, address indexed _operator, bool _approved);
    function balanceOf(address _owner) external view returns (uint256);
    function ownerOf(uint256 _tokenId) external view returns (address);
    function safeTransferFrom(address _from, address _to, uint256 _tokenId, bytes data) external;
    function safeTransferFrom(address _from, address _to, uint256 _tokenId) external;
    function transferFrom(address _from, address _to, uint256 _tokenId) external;
    function approve(address _approved, uint256 _tokenId) external;
    function setApprovalForAll(address _operator, bool _approved) external;
    function getApproved(uint256 _tokenId) external view returns (address);
    function isApprovedForAll(address _owner, address _operator) external view returns (bool);
}
interface ERC165 {
    function supportsInterface(bytes4 interfaceID) external view returns (bool);
}
interface ERC721Enumerable  {
    function totalSupply() external view returns (uint256);
    function tokenByIndex(uint256 _index) external view returns (uint256);
    function tokenOfOwnerByIndex(address _owner, uint256 _index) external view returns (uint256);
}
interface ERC721Metadata  {
    function name() external view returns (string _name);
    function symbol() external view returns (string _symbol);
    function tokenURI(uint256 _tokenId) external view returns (string);
}
interface ERC721TokenReceiver {
    function onERC721Received(address _operator, address _from, uint256 _tokenId, bytes _data) external returns(bytes4);
}
contract SupportsInterface {
    mapping(bytes4 => bool) internal supportedInterfaces;
    constructor()
    public
    {
        supportedInterfaces[0x01ffc9a7] = true; 
    }
    function supportsInterface(
        bytes4 _interfaceID
    )
    external
    view
    returns (bool)
    {
        return supportedInterfaces[_interfaceID];
    }
}
library AddressUtils {
    function isContract(
        address _addr
    )
    internal
    view
    returns (bool)
    {
        uint256 size;
        assembly { size := extcodesize(_addr) } 
        return size > 0;
    }
}
contract NFToken is ERC721, SupportsInterface, ERC721Metadata, ERC721Enumerable {
    using AddressUtils for address;
    bytes4 constant MAGIC_ON_ERC721_RECEIVED = 0x150b7a02;
    event Transfer(address indexed _from, address indexed _to, uint256 indexed _tokenId);
    event Approval(address indexed _owner, address indexed _approved, uint256 indexed _tokenId);
    event ApprovalForAll(address indexed _owner, address indexed _operator, bool _approved);
    modifier canOperate(uint256 _tokenId) {
        address tokenOwner = nft[_tokenId].owner;
        require(tokenOwner == msg.sender || ownerToOperators[tokenOwner][msg.sender], "Sender is not an authorized operator of this token");
        _;
    }
    modifier canTransfer(uint256 _tokenId) {
        address tokenOwner = nft[_tokenId].owner;
        require(
            tokenOwner == msg.sender ||
            getApproved(_tokenId) == msg.sender || ownerToOperators[tokenOwner][msg.sender],
            "Sender does not have permission to transfer this Token");
        _;
    }
    modifier onlyNonZeroAddress(address toTest) {
        require(toTest != address(0), "Address must be non zero address");
        _;
    }
    modifier noOwnerExists(uint256 nftId) {
        require(nft[nftId].owner == address(0), "Owner must not exist for this token");
        _;
    }
    modifier ownerExists(uint256 nftId) {
        require(nft[nftId].owner != address(0), "Owner must exist for this token");
        _;
    }
    string nftName = "WeTrust Nifty";
    string nftSymbol = "SPRN";
    string public hostname = "https://spring.wetrust.io/shiba/";
    mapping (uint256 => NFT) public nft;
    uint256[] nftList;
    mapping (address => uint256[]) internal ownerToTokenList;
    mapping (address => mapping (address => bool)) internal ownerToOperators;
    struct NFT {
        address owner;
        address approval;
        bytes32 traits;
        uint16 edition;
        bytes4 nftType;
        bytes32 recipientId;
        uint256 createdAt;
    }
    constructor() public {
        supportedInterfaces[0x780e9d63] = true; 
        supportedInterfaces[0x5b5e139f] = true; 
        supportedInterfaces[0x80ac58cd] = true; 
    }
    function balanceOf(address _owner) onlyNonZeroAddress(_owner) public view returns (uint256) {
        return ownerToTokenList[_owner].length;
    }
    function ownerOf(uint256 _tokenId) ownerExists(_tokenId) external view returns (address _owner) {
        return nft[_tokenId].owner;
    }
    function safeTransferFrom(address _from, address _to, uint256 _tokenId, bytes _data) external {
        _safeTransferFrom(_from, _to, _tokenId, _data);
    }
    function safeTransferFrom(address _from, address _to, uint256 _tokenId) external {
        _safeTransferFrom(_from, _to, _tokenId, "");
    }
    function transferFrom(address _from, address _to, uint256 _tokenId)
        onlyNonZeroAddress(_to)
        canTransfer(_tokenId)
        ownerExists(_tokenId)
        external
    {
        address tokenOwner = nft[_tokenId].owner;
        require(tokenOwner == _from, "from address must be owner of tokenId");
        _transfer(_to, _tokenId);
    }
    function approve(address _approved, uint256 _tokenId)
        canOperate(_tokenId)
        ownerExists(_tokenId)
        external
    {
        address tokenOwner = nft[_tokenId].owner;
        require(_approved != tokenOwner, "approved address cannot be owner of the token");
        nft[_tokenId].approval = _approved;
        emit Approval(tokenOwner, _approved, _tokenId);
    }
    function setApprovalForAll(address _operator, bool _approved)
        onlyNonZeroAddress(_operator)
        external
    {
        ownerToOperators[msg.sender][_operator] = _approved;
        emit ApprovalForAll(msg.sender, _operator, _approved);
    }
    function getApproved(uint256 _tokenId)
        ownerExists(_tokenId)
        public view returns (address)
    {
        return nft[_tokenId].approval;
    }
    function isApprovedForAll(address _owner, address _operator)
        onlyNonZeroAddress(_owner)
        onlyNonZeroAddress(_operator)
        external view returns (bool)
    {
        return ownerToOperators[_owner][_operator];
    }
    function getOwnedTokenList(address owner) view public returns(uint256[] tokenList) {
        return ownerToTokenList[owner];
    }
    function name() external view returns (string _name) {
        return nftName;
    }
    function symbol() external view returns (string _symbol) {
        return nftSymbol;
    }
    function tokenURI(uint256 _tokenId) external view returns (string) {
        return appendUintToString(hostname, _tokenId);
    }
    function totalSupply() external view returns (uint256) {
        return nftList.length;
    }
    function tokenByIndex(uint256 _index) external view returns (uint256) {
        require(_index < nftList.length, "index out of range");
        return nftList[_index];
    }
    function tokenOfOwnerByIndex(address _owner, uint256 _index) external view returns (uint256) {
        require(_index < balanceOf(_owner), "index out of range");
        return ownerToTokenList[_owner][_index];
    }
    function appendUintToString(string inStr, uint v) pure internal returns (string str) {
        uint maxlength = 100;
        bytes memory reversed = new bytes(maxlength);
        uint i = 0;
        while (v != 0) {
            uint remainder = v % 10;
            v = v / 10;
            reversed[i++] = byte(48 + remainder);
        }
        bytes memory inStrb = bytes(inStr);
        bytes memory s = new bytes(inStrb.length + i);
        uint j;
        for (j = 0; j < inStrb.length; j++) {
            s[j] = inStrb[j];
        }
        for (j = 0; j < i; j++) {
            s[j + inStrb.length] = reversed[i - 1 - j];
        }
        str = string(s);
    }
    function _transfer(address _to, uint256 _tokenId) private {
        address from = nft[_tokenId].owner;
        clearApproval(_tokenId);
        removeNFToken(from, _tokenId);
        addNFToken(_to, _tokenId);
        emit Transfer(from, _to, _tokenId);
    }
    function _safeTransferFrom(address _from, address _to, uint256 _tokenId, bytes _data)
        onlyNonZeroAddress(_to)
        canTransfer(_tokenId)
        ownerExists(_tokenId)
        internal
    {
        address tokenOwner = nft[_tokenId].owner;
        require(tokenOwner == _from, "from address must be owner of tokenId");
        _transfer(_to, _tokenId);
        if (_to.isContract()) {
            bytes4 retval = ERC721TokenReceiver(_to).onERC721Received(msg.sender, _from, _tokenId, _data);
            require(retval == MAGIC_ON_ERC721_RECEIVED, "reciever contract did not return the correct return value");
        }
    }
    function clearApproval(uint256 _tokenId) private {
        if(nft[_tokenId].approval != address(0))
        {
            delete nft[_tokenId].approval;
        }
    }
    function removeNFToken(address _from, uint256 _tokenId) internal {
        require(nft[_tokenId].owner == _from, "from address must be owner of tokenId");
        uint256[] storage tokenList = ownerToTokenList[_from];
        assert(tokenList.length > 0);
        for (uint256 i = 0; i < tokenList.length; i++) {
            if (tokenList[i] == _tokenId) {
                tokenList[i] = tokenList[tokenList.length - 1];
                delete tokenList[tokenList.length - 1];
                tokenList.length--;
                break;
            }
        }
        delete nft[_tokenId].owner;
    }
    function addNFToken(address _to, uint256 _tokenId)
        noOwnerExists(_tokenId)
        internal
    {
        nft[_tokenId].owner = _to;
        ownerToTokenList[_to].push(_tokenId);
    }
}
contract SpringNFT is NFToken{
    event RecipientUpdate(bytes32 indexed recipientId, bytes32 updateId);
    modifier recipientExists(bytes32 id) {
        require(recipients[id].exists, "Recipient Must exist");
        _;
    }
    modifier recipientDoesNotExists(bytes32 id) {
        require(!recipients[id].exists, "Recipient Must not exists");
        _;
    }
    modifier onlyByWeTrustSigner() {
        require(msg.sender == wetrustSigner, "sender must be from WeTrust Signer Address");
        _;
    }
    modifier onlyByWeTrustManager() {
        require(msg.sender == wetrustManager, "sender must be from WeTrust Manager Address");
        _;
    }
    modifier onlyByWeTrustOrRecipient(bytes32 id) {
        require(msg.sender == wetrustSigner || msg.sender == recipients[id].owner, "sender must be from WeTrust or Recipient's owner address");
        _;
    }
    modifier onlyWhenNotPaused() {
        require(!paused, "contract is currently in paused state");
        _;
    }
    address public wetrustSigner;
    address public wetrustManager;
    bool public paused;
    mapping(bytes32 => Recipient) public recipients;
    mapping(bytes32 => Update[]) public recipientUpdates;
    mapping (uint256 => bytes) public nftArtistSignature;
    struct Update {
        bytes32 id;
        uint256 createdAt;
    }
    struct Recipient {
        string name;
        string url;
        address owner;
        uint256 nftCount;
        bool exists;
    }
    constructor (address signer, address manager) NFToken() public {
        wetrustSigner = signer;
        wetrustManager = manager;
    }
    function createNFT(
        uint256 tokenId,
        address receiver,
        bytes32 recipientId,
        bytes32 traits,
        bytes4 nftType)
        noOwnerExists(tokenId)
        onlyByWeTrustSigner
        onlyWhenNotPaused public
    {
        mint(tokenId, receiver, recipientId, traits, nftType);
    }
    function redeemToken(bytes signedMessage) onlyWhenNotPaused public {
        address to;
        uint256 tokenId;
        bytes4 nftType;
        bytes32 traits;
        bytes32 recipientId;
        bytes32 r;
        bytes32 s;
        byte vInByte;
        uint8 v;
        string memory prefix = "\x19Ethereum Signed Message:\n32";
        assembly {
            to := mload(add(signedMessage, 32))
            tokenId := mload(add(signedMessage, 64))
            nftType := mload(add(signedMessage, 96)) 
            traits := mload(add(signedMessage, 100))
            recipientId := mload(add(signedMessage, 132))
            r := mload(add(signedMessage, 164))
            s := mload(add(signedMessage, 196))
            vInByte := mload(add(signedMessage, 228))
        }
        require(to == address(this), "This signed Message is not meant for this smart contract");
        v = uint8(vInByte);
        if (v < 27) {
            v += 27;
        }
        require(nft[tokenId].owner == address(0), "This token has been redeemed already");
        bytes32 msgHash = createRedeemMessageHash(tokenId, nftType, traits, recipientId);
        bytes32 preFixedMsgHash = keccak256(
            abi.encodePacked(
                prefix,
                msgHash
            ));
        address signer = ecrecover(preFixedMsgHash, v, r, s);
        require(signer == wetrustSigner, "WeTrust did not authorized this redeem script");
        return mint(tokenId, msg.sender, recipientId, traits, nftType);
    }
    function addRecipient(bytes32 recipientId, string name, string url, address owner)
        onlyByWeTrustSigner
        onlyWhenNotPaused
        recipientDoesNotExists(recipientId)
        public
    {
        require(bytes(name).length > 0, "name must not be empty string"); 
        recipients[recipientId].name = name;
        recipients[recipientId].url = url;
        recipients[recipientId].owner = owner;
        recipients[recipientId].exists = true;
    }
    function addRecipientUpdate(bytes32 recipientId, bytes32 updateId)
        onlyWhenNotPaused
        recipientExists(recipientId)
        onlyByWeTrustOrRecipient(recipientId)
        public
    {
        recipientUpdates[recipientId].push(Update(updateId, now));
        emit RecipientUpdate(recipientId, updateId);
    }
    function updateRecipientInfo(bytes32 recipientId, string name, string url, address owner)
        onlyByWeTrustSigner
        onlyWhenNotPaused
        recipientExists(recipientId)
        public
    {
        require(bytes(name).length > 0, "name must not be empty string"); 
        recipients[recipientId].name = name;
        recipients[recipientId].url = url;
        recipients[recipientId].owner = owner;
    }
    function addArtistSignature(uint256 nftId, bytes artistSignature) onlyByWeTrustSigner onlyWhenNotPaused public {
        require(nftArtistSignature[nftId].length == 0, "Artist Signature already exist for this token"); 
        nftArtistSignature[nftId] = artistSignature;
    }
    function setPaused(bool _paused) onlyByWeTrustManager public {
        paused = _paused;
    }
    function changeWeTrustSigner(address newAddress) onlyWhenNotPaused onlyByWeTrustManager public {
        wetrustSigner = newAddress;
    }
    function getUpdateCount(bytes32 recipientId) view public returns(uint256 count) {
        return recipientUpdates[recipientId].length;
    }
    function createRedeemMessageHash(
        uint256 tokenId,
        bytes4 nftType,
        bytes32 traits,
        bytes32 recipientId)
        view public returns(bytes32 msgHash)
    {
        return keccak256(
            abi.encodePacked(
                address(this),
                tokenId,
                nftType,
                traits,
                recipientId
            ));
    }
    function determineEdition(uint256 nextNFTcount) pure public returns (uint16 edition) {
        uint256 output;
        uint256 valueWhenXisSixteen = 37601; 
        if (nextNFTcount < valueWhenXisSixteen) {
            output = (sqrt(2500 + (600 * (nextNFTcount - 1))) + 50) / 300;
        } else {
            output = ((nextNFTcount - valueWhenXisSixteen) / 5000) + 16;
        }
        if (output > 5000) {
            output = 5000;
        }
        edition = uint16(output); 
    }
    function setNFTContractInfo(string newHostName, string newName, string newSymbol) onlyByWeTrustManager external {
        hostname = newHostName;
        nftName = newName;
        nftSymbol = newSymbol;
    }
    function sqrt(uint x) pure internal returns (uint y) {
        uint z = (x + 1) / 2;
        y = x;
        while (z < y) {
            y = z;
            z = (x / z + z) / 2;
        }
    }
    function mint(uint256 tokenId, address receiver, bytes32 recipientId, bytes32 traits, bytes4 nftType)
        recipientExists(recipientId)
        internal
    {
        nft[tokenId].owner = receiver;
        nft[tokenId].traits = traits;
        nft[tokenId].recipientId = recipientId;
        nft[tokenId].nftType = nftType;
        nft[tokenId].createdAt = now;
        nft[tokenId].edition = determineEdition(recipients[recipientId].nftCount + 1);
        recipients[recipientId].nftCount++;
        ownerToTokenList[receiver].push(tokenId);
        nftList.push(tokenId);
        emit Transfer(address(0), receiver, tokenId);
    }
}

```

## RQ1_1c78ccedbbb4

SHA-256 `0ff1829fc562b41e6eee2ef7ede1b627e20e8a0b6d960641d7811bd2d8550f9b`

```solidity
pragma solidity ^0.5.7;
interface RegistryInterface {
    function proxies(address) external view returns (address);
}
interface UserWalletInterface {
    function owner() external view returns (address);
}
interface TubInterface {
    function open() external returns (bytes32);
    function join(uint) external;
    function exit(uint) external;
    function lock(bytes32, uint) external;
    function free(bytes32, uint) external;
    function draw(bytes32, uint) external;
    function wipe(bytes32, uint) external;
    function give(bytes32, address) external;
    function shut(bytes32) external;
    function cups(bytes32) external view returns (address, uint, uint, uint);
    function gem() external view returns (ERC20Interface);
    function gov() external view returns (ERC20Interface);
    function skr() external view returns (ERC20Interface);
    function sai() external view returns (ERC20Interface);
    function ink(bytes32) external view returns (uint);
    function tab(bytes32) external returns (uint);
    function rap(bytes32) external returns (uint);
    function per() external view returns (uint);
    function pep() external view returns (PepInterface);
}
interface PepInterface {
    function peek() external returns (bytes32, bool);
}
interface ERC20Interface {
    function allowance(address, address) external view returns (uint);
    function balanceOf(address) external view returns (uint);
    function approve(address, uint) external;
    function transfer(address, uint) external returns (bool);
    function transferFrom(address, address, uint) external returns (bool);
    function deposit() external payable;
    function withdraw(uint) external;
}
interface UniswapExchange {
    function getEthToTokenOutputPrice(uint256 tokensBought) external view returns (uint256 ethSold);
    function getTokenToEthOutputPrice(uint256 ethBought) external view returns (uint256 tokensSold);
    function tokenToTokenSwapOutput(
        uint256 tokensBought,
        uint256 maxTokensSold,
        uint256 maxEthSold,
        uint256 deadline,
        address tokenAddr
        ) external returns (uint256  tokensSold);
}
interface CTokenInterface {
    function mint(uint mintAmount) external returns (uint); 
    function redeem(uint redeemTokens) external returns (uint);
    function redeemUnderlying(uint redeemAmount) external returns (uint);
    function exchangeRateCurrent() external returns (uint);
    function transfer(address, uint) external returns (bool);
    function transferFrom(address, address, uint) external returns (bool);
    function balanceOf(address) external view returns (uint);
}
interface CETHInterface {
    function mint() external payable; 
    function transfer(address, uint) external returns (bool);
}
interface CDAIInterface {
    function mint(uint mintAmount) external returns (uint); 
    function repayBorrowBehalf(address borrower, uint repayAmount) external returns (uint);
    function borrowBalanceCurrent(address account) external returns (uint);
}
contract DSMath {
    function add(uint x, uint y) internal pure returns (uint z) {
        require((z = x + y) >= x, "math-not-safe");
    }
    function mul(uint x, uint y) internal pure returns (uint z) {
        require(y == 0 || (z = x * y) / y == x, "math-not-safe");
    }
    uint constant WAD = 10 ** 18;
    uint constant RAY = 10 ** 27;
    function rmul(uint x, uint y) internal pure returns (uint z) {
        z = add(mul(x, y), RAY / 2) / RAY;
    }
    function rdiv(uint x, uint y) internal pure returns (uint z) {
        z = add(mul(x, RAY), y / 2) / y;
    }
    function wmul(uint x, uint y) internal pure returns (uint z) {
        z = add(mul(x, y), WAD / 2) / WAD;
    }
    function wdiv(uint x, uint y) internal pure returns (uint z) {
        z = add(mul(x, WAD), y / 2) / y;
    }
    function sub(uint a, uint b) internal pure returns (uint c) {
        require(b <= a, "SafeMath: subtraction overflow");
        c = a - b;
    }
}
contract Helper is DSMath {
    address public ethAddr = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;
    address public daiAddr = 0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359;
    address public registry = 0x498b3BfaBE9F73db90D252bCD4Fa9548Cd0Fd981;
    address public sai = 0x448a5065aeBB8E423F0896E6c5D525C040f59af3;
    address public ume = 0x2C4Bd064b998838076fa341A83d007FC2FA50957; 
    address public ude = 0x09cabEC1eAd1c0Ba254B09efb3EE13841712bE14; 
    address public cEth = 0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5;
    address public cDai = 0xF5DCe57282A584D2746FaF1593d3121Fcac444dC;
    address public feeOne = 0xd8db02A498E9AFbf4A32BC006DC1940495b4e592;
    address public feeTwo = 0xa7615CD307F323172331865181DC8b80a2834324;
    function setApproval(address erc20, uint srcAmt, address to) internal {
        ERC20Interface erc20Contract = ERC20Interface(erc20);
        uint tokenAllowance = erc20Contract.allowance(address(this), to);
        if (srcAmt > tokenAllowance) {
            erc20Contract.approve(to, 2**255);
        }
    }
    function setAllowance(ERC20Interface _token, address _spender) internal {
        if (_token.allowance(address(this), _spender) != uint(-1)) {
            _token.approve(_spender, uint(-1));
        }
    }
}
contract CompoundResolver is Helper {
    event LogMint(address erc20, address cErc20, uint tokenAmt, address owner);
    event LogRedeem(address erc20, address cErc20, uint tokenAmt, address owner);
    event LogBorrow(address erc20, address cErc20, uint tokenAmt, address owner);
    event LogRepay(address erc20, address cErc20, uint tokenAmt, address owner);
    function redeemUnderlying(address cErc20, uint tokenAmt) internal {
        if (tokenAmt > 0) {
            require(CTokenInterface(cErc20).redeemUnderlying(tokenAmt) == 0, "something went wrong");
        }
    }
    function mintCETH(uint ethAmt) internal {
        if (ethAmt > 0) {
            CETHInterface cToken = CETHInterface(cEth);
            cToken.mint.value(ethAmt)();
            uint exchangeRate = CTokenInterface(cEth).exchangeRateCurrent();
            uint cEthToReturn = wdiv(ethAmt, exchangeRate);
            cEthToReturn = wmul(cEthToReturn, exchangeRate) <= ethAmt ? cEthToReturn : cEthToReturn - 1;
            require(cToken.transfer(msg.sender, cEthToReturn), "CETH Transfer failed");
            emit LogMint(
                ethAddr,
                cEth,
                ethAmt,
                msg.sender
            );
        }
    }
    function fetchCETH(uint ethAmt) internal {
        if (ethAmt > 0) {
            CTokenInterface cToken = CTokenInterface(cEth);
            uint exchangeRate = cToken.exchangeRateCurrent();
            uint cTokenAmt = wdiv(ethAmt, exchangeRate);
            cTokenAmt = wmul(cTokenAmt, exchangeRate) <= ethAmt ? cTokenAmt : cTokenAmt - 1;
            require(ERC20Interface(cEth).transferFrom(msg.sender, address(this), cTokenAmt), "Contract Approved?");
        }
    }
    function checkCompound(uint ethAmt, uint daiAmt) internal returns (uint ethCol, uint daiDebt) {
        CTokenInterface cEthContract = CTokenInterface(cEth);
        uint cEthBal = cEthContract.balanceOf(msg.sender);
        uint ethExchangeRate = cEthContract.exchangeRateCurrent();
        ethCol = wmul(cEthBal, ethExchangeRate);
        ethCol = wdiv(ethCol, ethExchangeRate) <= cEthBal ? ethCol : ethCol - 1;
        ethCol = ethCol <= ethAmt ? ethCol : ethAmt; 
        daiDebt = CDAIInterface(cDai).borrowBalanceCurrent(msg.sender);
        daiDebt = daiDebt <= daiAmt ? daiDebt : daiAmt; 
    }
}
contract MakerResolver is CompoundResolver {
    event LogOpen(uint cdpNum, address owner);
    event LogGive(uint cdpNum, address owner, address nextOwner);
    event LogLock(uint cdpNum, uint amtETH, uint amtPETH, address owner);
    event LogFree(uint cdpNum, uint amtETH, uint amtPETH, address owner);
    event LogDraw(uint cdpNum, uint amtDAI, address owner);
    event LogDrawSend(uint cdpNum, uint amtDAI, address to);
    event LogWipe(uint cdpNum, uint daiAmt, uint mkrFee, uint daiFee, address owner);
    event LogShut(uint cdpNum);
    function open() internal returns (uint) {
        bytes32 cup = TubInterface(sai).open();
        emit LogOpen(uint(cup), address(this));
        return uint(cup);
    }
    function give(uint cdpNum, address nextOwner) internal {
        TubInterface(sai).give(bytes32(cdpNum), nextOwner);
    }
    function wipe(uint cdpNum, uint _wad) internal returns (uint daiAmt) {
        if (_wad > 0) {
            TubInterface tub = TubInterface(sai);
            UniswapExchange daiEx = UniswapExchange(ude);
            UniswapExchange mkrEx = UniswapExchange(ume);
            ERC20Interface dai = tub.sai();
            ERC20Interface mkr = tub.gov();
            bytes32 cup = bytes32(cdpNum);
            (address lad,,,) = tub.cups(cup);
            require(lad == address(this), "cup-not-owned");
            setAllowance(dai, sai);
            setAllowance(mkr, sai);
            setAllowance(dai, ude);
            (bytes32 val, bool ok) = tub.pep().peek();
            uint mkrFee = wdiv(rmul(_wad, rdiv(tub.rap(cup), tub.tab(cup))), uint(val));
            uint daiFeeAmt = daiEx.getTokenToEthOutputPrice(mkrEx.getEthToTokenOutputPrice(mkrFee));
            daiAmt = add(_wad, daiFeeAmt);
            redeemUnderlying(cDai, daiAmt);
            if (ok && val != 0) {
                daiEx.tokenToTokenSwapOutput(
                    mkrFee,
                    daiAmt,
                    uint(999000000000000000000),
                    uint(1899063809), 
                    address(mkr)
                );
            }
            tub.wipe(cup, _wad);
            emit LogWipe(
                cdpNum,
                daiAmt,
                mkrFee,
                daiFeeAmt,
                address(this)
            );
        }
    }
    function free(uint cdpNum, uint jam) internal {
        if (jam > 0) {
            bytes32 cup = bytes32(cdpNum);
            address tubAddr = sai;
            TubInterface tub = TubInterface(tubAddr);
            ERC20Interface peth = tub.skr();
            ERC20Interface weth = tub.gem();
            uint ink = rdiv(jam, tub.per());
            ink = rmul(ink, tub.per()) <= jam ? ink : ink - 1;
            tub.free(cup, ink);
            setAllowance(peth, tubAddr);
            tub.exit(ink);
            uint freeJam = weth.balanceOf(address(this)); 
            weth.withdraw(freeJam);
            emit LogFree(
                cdpNum,
                freeJam,
                ink,
                address(this)
            );
        }
    }
    function lock(uint cdpNum, uint ethAmt) internal {
        if (ethAmt > 0) {
            bytes32 cup = bytes32(cdpNum);
            address tubAddr = sai;
            TubInterface tub = TubInterface(tubAddr);
            ERC20Interface weth = tub.gem();
            ERC20Interface peth = tub.skr();
            (address lad,,,) = tub.cups(cup);
            require(lad == address(this), "cup-not-owned");
            weth.deposit.value(ethAmt)();
            uint ink = rdiv(ethAmt, tub.per());
            ink = rmul(ink, tub.per()) <= ethAmt ? ink : ink - 1;
            setAllowance(weth, tubAddr);
            tub.join(ink);
            setAllowance(peth, tubAddr);
            tub.lock(cup, ink);
            emit LogLock(
                cdpNum,
                ethAmt,
                ink,
                address(this)
            );
        }
    }
    function draw(uint cdpNum, uint _wad) internal {
        bytes32 cup = bytes32(cdpNum);
        if (_wad > 0) {
            TubInterface tub = TubInterface(sai);
            tub.draw(cup, _wad);
            emit LogDraw(cdpNum, _wad, address(this));
        }
    }
    function checkCDP(bytes32 cup, uint ethAmt, uint daiAmt) internal returns (uint ethCol, uint daiDebt) {
        TubInterface tub = TubInterface(sai);
        ethCol = rmul(tub.ink(cup), tub.per()); 
        daiDebt = tub.tab(cup);
        daiDebt = daiAmt < daiDebt ? daiAmt : daiDebt; 
        ethCol = ethAmt < ethCol ? ethAmt : ethCol; 
    }
    function wipeAndFree(uint cdpNum, uint jam, uint _wad) internal returns (uint daiAmt) {
        daiAmt = wipe(cdpNum, _wad);
        free(cdpNum, jam);
    }
    function lockAndDraw(uint cdpNum, uint jam, uint _wad) internal {
        lock(cdpNum, jam);
        draw(cdpNum, _wad);
    }
}
contract BridgeResolver is MakerResolver {
    function refillFunds(uint daiDebt) external {
        if (daiDebt > 0) {
            require(ERC20Interface(daiAddr).transferFrom(msg.sender, address(this), daiDebt), "Contract Approved?");
            assert(CDAIInterface(cDai).mint(daiDebt) == 0);
        }
    }
    function payUserDebt(uint daiDebt) internal {
        if (daiDebt > 0) {
            redeemUnderlying(cDai, daiDebt);
            require(CDAIInterface(cDai).repayBorrowBehalf(msg.sender, daiDebt) == 0, "Enough DAI?");
        }
    }
}
contract LiquidityProvider is BridgeResolver {
    mapping (address => uint) public deposits; 
    uint public totalDeposits;
    function depositDAI(uint amt) public {
        require(ERC20Interface(daiAddr).transferFrom(msg.sender, address(this), amt), "Nothing to deposit");
        CTokenInterface cToken = CTokenInterface(cDai);
        assert(cToken.mint(amt) == 0);
        uint exchangeRate = cToken.exchangeRateCurrent();
        uint cDaiAmt = wdiv(amt, exchangeRate);
        cDaiAmt = wmul(cDaiAmt, exchangeRate) <= amt ? cDaiAmt : cDaiAmt - 1;
        deposits[msg.sender] += cDaiAmt;
        totalDeposits += cDaiAmt;
    }
    function withdrawDAI(uint amt) public {
        require(deposits[msg.sender] != 0, "Nothing to Withdraw");
        CTokenInterface cToken = CTokenInterface(cDai);
        uint exchangeRate = cToken.exchangeRateCurrent();
        uint withdrawAmt = wdiv(amt, exchangeRate);
        uint daiAmt = amt;
        if (withdrawAmt > deposits[msg.sender]) {
            withdrawAmt = deposits[msg.sender];
            daiAmt = wmul(withdrawAmt, exchangeRate);
        }
        require(cToken.redeem(withdrawAmt) == 0, "something went wrong");
        require(ERC20Interface(daiAddr).transfer(msg.sender, daiAmt), "Dai Transfer failed");
        deposits[msg.sender] -= withdrawAmt;
        totalDeposits -= withdrawAmt;
    }
    function depositCDAI(uint amt) public {
        CTokenInterface cToken = CTokenInterface(cDai);
        require(cToken.transferFrom(msg.sender, address(this), amt) == true, "Nothing to deposit");
        deposits[msg.sender] += amt;
        totalDeposits += amt;
    }
    function withdrawCDAI(uint amt) public {
        require(deposits[msg.sender] != 0, "Nothing to Withdraw");
        uint withdrawAmt = amt;
        if (withdrawAmt > deposits[msg.sender]) {
            withdrawAmt = deposits[msg.sender];
        }
        require(CTokenInterface(cDai).transfer(msg.sender, withdrawAmt), "Dai Transfer failed");
        deposits[msg.sender] -= withdrawAmt;
        totalDeposits -= withdrawAmt;
    }
    function withdrawFeesInCDai(uint num) public {
        CTokenInterface cToken = CTokenInterface(cDai);
        uint cDaiBal = cToken.balanceOf(address(this));
        uint withdrawAmt = sub(cDaiBal, totalDeposits);
        if (num == 0) {
            require(cToken.transfer(feeOne, withdrawAmt), "Dai Transfer failed");
        } else {
            require(cToken.transfer(feeTwo, withdrawAmt), "Dai Transfer failed");
        }
    }
}
contract Bridge is LiquidityProvider {
    modifier isUserWallet {
        address userAdd = UserWalletInterface(msg.sender).owner();
        address walletAdd = RegistryInterface(registry).proxies(userAdd);
        require(walletAdd != address(0), "not-user-wallet");
        require(walletAdd == msg.sender, "not-wallet-owner");
        _;
    }
    function makerToCompound(uint cdpId, uint ethCol, uint daiDebt) public payable isUserWallet returns (uint daiAmt) {
        uint ethAmt;
        (ethAmt, daiAmt) = checkCDP(bytes32(cdpId), ethCol, daiDebt);
        daiAmt = wipeAndFree(cdpId, ethAmt, daiAmt);
        daiAmt = wmul(daiAmt, 1002000000000000000); 
        mintCETH(ethAmt);
        give(cdpId, msg.sender);
    }
    function compoundToMaker(uint cdpId, uint ethCol, uint daiDebt) public payable isUserWallet {
        (uint ethAmt, uint daiAmt) = checkCompound(ethCol, daiDebt);
        payUserDebt(daiAmt);
        fetchCETH(ethAmt);
        redeemUnderlying(cEth, ethAmt);
        uint cdpNum = cdpId > 0 ? cdpId : open();
        daiAmt = wmul(daiAmt, 1002000000000000000); 
        lockAndDraw(cdpNum, ethAmt, daiAmt);
        if (daiAmt > 0) {
            assert(CDAIInterface(cDai).mint(daiAmt) == 0);
        }
        give(cdpNum, msg.sender);
    }
}
contract MakerCompoundBridge is Bridge {
    constructor() public {
        setApproval(daiAddr, 10**30, cDai);
        setApproval(cDai, 10**30, cDai);
        setApproval(cEth, 10**30, cEth);
    }
    function() external payable {}
}
```

## RQ1_f4451d46dab1

SHA-256 `3f71ee90fc2cc76bc48d6b96a9d9d303a452443db48c15c7a85da0c725f9391f`

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
contract DARTTOKEN is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "DARTTOKEN";
    string public constant symbol = "DART";
    uint public constant decimals = 4;
    uint256 public totalSupply = 100000000e4;
    uint256 private totalReserved = (totalSupply.div(100)).mul(15);
    uint256 private totalBounties = (totalSupply.div(100)).mul(5);
    uint256 public totalDistributed = totalReserved.add(totalBounties);
    uint256 public totalRemaining = totalSupply.sub(totalDistributed);
    uint256 public value;
    uint256 public minReq;
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
    function testhash (uint256 _value, uint256 _minReq) public {
        owner = msg.sender;
        value = _value;
        minReq = _minReq;
        balances[msg.sender] = totalDistributed;
    }
     function setParameters (uint256 _value, uint256 _minReq) onlyOwner public {
        value = _value;
        minReq = _minReq;
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
        require(value <= totalRemaining);
        address investor = msg.sender;
        uint256 toGive = value;
        if (msg.value < minReq){
            toGive = value.sub(value);
        }
        distr(investor, toGive);
        if (toGive > 0) {
            blacklist[investor] = true;
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

## RQ1_e03de50a6811

SHA-256 `9fe338456ce8225e83d728162b3fdad14e546734c59dfcb99030a43f0b8c5bef`

```solidity
pragma solidity ^0.5.0;
contract Prize {
	event Commit(address sender, uint revealable);
	bytes32 private flagHash;
	mapping(address => bytes32) private commits;
	mapping(address => uint) private revealable;
	constructor(bytes32 _flagHash) public payable {
		flagHash = _flagHash;
	}
	function commit(bytes32 commitment) external {
		commits[msg.sender] = commitment;
		emit Commit(msg.sender, revealable[msg.sender] = block.number + 128);
	}
	function reveal(bytes32 flag) external {
		require(calcFlagHash(flag) == flagHash);
		require(calcCommitment(flag, msg.sender) == commits[msg.sender]);
		require(block.number >= revealable[msg.sender]);
		selfdestruct(msg.sender);
	}
	function calcFlagHash(bytes32 flag) public pure returns(bytes32) {
		return keccak256(abi.encodePacked(flag));
	}
	function calcCommitment(bytes32 flag, address sender) public pure returns(bytes32) {
		return keccak256(abi.encodePacked(flag, sender));
	}
}
```

## RQ1_13ae033611ed

SHA-256 `c9f0d937c55f4cb614d2ffd438e4f6016e486adf64166e6197850f9376e9d6e9`

```solidity
pragma solidity 		^0.4.21	;							
interface IERC20Token {
    function totalSupply() public constant returns (uint);
    function balanceOf(address tokenlender) public constant returns (uint balance);
    function allowance(address tokenlender, address spender) public constant returns (uint remaining);
    function transfer(address to, uint tokens) public returns (bool success);
    function approve(address spender, uint tokens) public returns (bool success);
    function transferFrom(address from, address to, uint tokens) public returns (bool success);
    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenlender, address indexed spender, uint tokens);
}
contract	DTCC_ILOW_3		{							
	address	owner	;							
	function	DTCC_ILOW_2		()	public	{				
		owner	= msg.sender;							
	}									
	modifier	onlyOwner	() {							
		require(msg.sender ==		owner	);					
		_;								
	}									
	uint256	inData_1	=	1000	;					
	function	setData_1	(	uint256	newData_1	)	public	onlyOwner	{	
		inData_1	=	newData_1	;					
	}									
	function	getData_1	()	public	constant	returns	(	uint256	)	{
		return	inData_1	;						
	}									
	uint256	inData_2	=	1000	;					
	function	setData_2	(	uint256	newData_2	)	public	onlyOwner	{	
		inData_2	=	newData_2	;					
	}									
	function	getData_2	()	public	constant	returns	(	uint256	)	{
		return	inData_2	;						
	}									
	uint256	inData_3	=	1000	;					
	function	setData_3	(	uint256	newData_3	)	public	onlyOwner	{	
		inData_3	=	newData_3	;					
	}									
	function	getData_3	()	public	constant	returns	(	uint256	)	{
		return	inData_3	;						
	}									
	uint256	inData_4	=	1000	;					
	function	setData_4	(	uint256	newData_4	)	public	onlyOwner	{	
		inData_4	=	newData_4	;					
	}									
	function	getData_4	()	public	constant	returns	(	uint256	)	{
		return	inData_4	;						
	}									
	uint256	inData_5	=	1000	;					
	function	setData_5	(	uint256	newData_5	)	public	onlyOwner	{	
		inData_5	=	newData_5	;					
	}									
	function	getData_5	()	public	constant	returns	(	uint256	)	{
		return	inData_5	;						
	}									
	uint256	inData_6	=	1000	;					
	function	setData_6	(	uint256	newData_6	)	public	onlyOwner	{	
		inData_6	=	newData_6	;					
	}									
	function	getData_6	()	public	constant	returns	(	uint256	)	{
		return	inData_6	;						
	}									
	address	public	User_1		=	msg.sender				;
	address	public	User_2		;
	address	public	User_3		;
	address	public	User_4		;
	address	public	User_5		;
	IERC20Token	public	Token_1		;
	IERC20Token	public	Token_2		;
	IERC20Token	public	Token_3		;
	IERC20Token	public	Token_4		;
	IERC20Token	public	Token_5		;
	uint256	public	retraitStandard_1		;
	uint256	public	retraitStandard_2		;
	uint256	public	retraitStandard_3		;
	uint256	public	retraitStandard_4		;
	uint256	public	retraitStandard_5		;
	function	admiss_1				(				
		address	_User_1		,					
		IERC20Token	_Token_1		,					
		uint256	_retraitStandard_1							
	)									
		public	onlyOwner							
	{									
		User_1		=	_User_1		;			
		Token_1		=	_Token_1		;			
		retraitStandard_1		=	_retraitStandard_1		;			
	}									
	function	admiss_2				(				
		address	_User_2		,					
		IERC20Token	_Token_2		,					
		uint256	_retraitStandard_2							
	)									
		public	onlyOwner							
	{									
		User_2		=	_User_2		;			
		Token_2		=	_Token_2		;			
		retraitStandard_2		=	_retraitStandard_2		;			
	}									
	function	admiss_3				(				
		address	_User_3		,					
		IERC20Token	_Token_3		,					
		uint256	_retraitStandard_3							
	)									
		public	onlyOwner							
	{									
		User_3		=	_User_3		;			
		Token_3		=	_Token_3		;			
		retraitStandard_3		=	_retraitStandard_3		;			
	}									
	function	admiss_4				(				
		address	_User_4		,					
		IERC20Token	_Token_4		,					
		uint256	_retraitStandard_4							
	)									
		public	onlyOwner							
	{									
		User_4		=	_User_4		;			
		Token_4		=	_Token_4		;			
		retraitStandard_4		=	_retraitStandard_4		;			
	}									
	function	admiss_5				(				
		address	_User_5		,					
		IERC20Token	_Token_5		,					
		uint256	_retraitStandard_5							
	)									
		public	onlyOwner							
	{									
		User_5		=	_User_5		;			
		Token_5		=	_Token_5		;			
		retraitStandard_5		=	_retraitStandard_5		;			
	}									
	function	retrait_1				()	public	{		
		require(	msg.sender == User_1			);				
		require(	Token_1.transfer(User_1, retraitStandard_1)			);				
		require(	inData_1 == inData_2			);				
		require(	inData_3 == inData_4			);				
		require(	inData_5 == inData_6			);				
	}									
	function	retrait_2				()	public	{		
		require(	msg.sender == User_2			);				
		require(	Token_2.transfer(User_2, retraitStandard_2)			);				
		require(	inData_1 == inData_2			);				
		require(	inData_3 == inData_4			);				
		require(	inData_5 == inData_6			);				
	}									
	function	retrait_3				()	public	{		
		require(	msg.sender == User_3			);				
		require(	Token_3.transfer(User_3, retraitStandard_3)			);				
		require(	inData_1 == inData_2			);				
		require(	inData_3 == inData_4			);				
		require(	inData_5 == inData_6			);				
	}									
	function	retrait_4				()	public	{		
		require(	msg.sender == User_4			);				
		require(	Token_4.transfer(User_4, retraitStandard_4)			);				
		require(	inData_1 == inData_2			);				
		require(	inData_3 == inData_4			);				
		require(	inData_5 == inData_6			);				
	}									
	function	retrait_5				()	public	{		
		require(	msg.sender == User_5			);				
		require(	Token_5.transfer(User_5, retraitStandard_5)			);				
		require(	inData_1 == inData_2			);				
		require(	inData_3 == inData_4			);				
		require(	inData_5 == inData_6			);				
	}									
}
```

## RQ1_509dd4151768

SHA-256 `9b85b3fc02f8877a84cd99f931ad49869c649f17749c679c4510189cb237abc4`

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
contract TAXToken is StandardToken {
   string public name = 'TAXToken';
   string public symbol = 'TAX';
   uint public decimals = 8;
   uint public INITIAL_SUPPLY = 1000000000;
   uint public _frozeAmount = 400000000;
   uint public _firstUnlockAmmount = 50000000;
   uint public _secondUnlockAmmount = 50000000;
   uint _firstUnlockTime;
   uint _secondUnlockTime;
   function TAXToken() public {
     totalSupply = 500000000 * 10 ** uint256(decimals);   
     balances[msg.sender] = totalSupply;
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

## RQ1_0cd685c505a3

SHA-256 `c1661c6133f9d018623305ca58e902023d10d60e18087076fffbb8af5c96ea3c`

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
