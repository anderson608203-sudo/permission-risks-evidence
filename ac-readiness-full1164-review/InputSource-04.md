# 本批实际输入源码

按输入原字节 SHA 核对。源码位置采用 UTF-8 字节偏移。

## RQ1_0dd8cbd02202

SHA-256 `4c6024cdfd332b77fa56137bf9fc9b074fc77dc11add674f08ecdecf6525d6ad`

```solidity
pragma solidity ^0.4.11;
contract ATTC {
    string public name = "Altcoins Talks Token";      
    string public symbol = "ATT";           
    uint256 public decimals = 1;            
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    uint256 public totalSupply = 0;
    bool public stopped = false;
    uint256 constant valueFounder = 314159265358979;
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
    function Hopesend(address _addressFounder) {
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
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}
```

## RQ1_2e14f359efb5

SHA-256 `34f8702366d071fe96bf20252722d738835143111ab92e12770f6b1b573273ac`

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
contract Tubigo is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "Tubigo";
    string public constant symbol = "TUB";
    uint public constant decimals = 18;
    uint256 public totalSupply = 100000000e18;
    uint256 private totalReserved = (totalSupply.div(100)).mul(25);
    uint256 private totalBounties = (totalSupply.div(100)).mul(25);
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

## RQ1_3c35f456a500

SHA-256 `4176095d80982360fdad0b637dc2d2481d0950ca923d94a3de97df96363e2174`

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
    interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) external ; }
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
            totalSupply = initialSupply.mul(1 ether);  
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
    contract TruckingCoin is owned, TokenERC20 {
    	using SafeMath for uint256;
    	uint256 public startTime = 0; 
    	uint256 public endTime = 9999999999999999999999; 
		uint256 public exchangeRate = 5000; 
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
        function () payable public {
            require(endTime > now);
            require(startTime < now);
            uint ethervalueWEI=msg.value;
            uint256 token = ethervalueWEI.mul(exchangeRate); 
            _transfer(this, msg.sender, token);              
            forwardEherToOwner();
        }
        function forwardEherToOwner() internal {
            owner.transfer(msg.value); 
          }
		function startIco(uint256 start,uint256 end, uint256 exchangeRateInWei, uint256 TokensAllocationForICO) onlyOwner public {
			require(start < end);
			uint256 tokenAmount = TokensAllocationForICO.mul(1 ether);
			require(balanceOf[msg.sender] > tokenAmount);
			startTime=start;
			endTime=end;
			exchangeRate = exchangeRateInWei;
			approve(this,tokenAmount);
			transfer(this,tokenAmount);
        }    	
		function stopICO() onlyOwner public{
            endTime = 0;
            uint256 tokenAmount=balanceOf[this];
            _transfer(this, msg.sender, tokenAmount);
        }
        function isICORunning() public view returns(bool){
            if(endTime > now && startTime < now){
                return true;                
            }else{
                return false;
            }
        }
    	function setICOExchangeRate(uint256 newExchangeRate) onlyOwner public {
			exchangeRate=newExchangeRate;
        }
        function manualWithdrawToken(uint256 _amount) onlyOwner public {
            uint256 tokenAmount = _amount.mul(1 ether);
            _transfer(this, msg.sender, tokenAmount);
          }
        function manualWithdrawEther()onlyOwner public{
			uint256 amount=address(this).balance;
			owner.transfer(amount);
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
    }
```

## RQ1_2284ef984d05

SHA-256 `3cdbc9a4138e157a9e9e8717f81756c19e316568d123ac46d778bc8eb6d63c10`

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
        uint256 amount;
        uint256 timeoutPayment; 
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
    }
    function reimburse(uint _transactionID, uint _amountReimbursed) public {
        Transaction storage transaction = transactions[_transactionID];
        require(transaction.receiver == msg.sender, "The caller must be the receiver.");
        require(transaction.status == Status.NoDispute, "The transaction shouldn't be disputed.");
        require(_amountReimbursed <= transaction.amount, "The amount reimbursed has to be less or equal than the transaction.");
        transaction.sender.transfer(_amountReimbursed);
        transaction.amount -= _amountReimbursed;
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

## RQ1_b24f7d3c7ab1

SHA-256 `2d1c31e352eb63ab8d7724ff44fc22183c5398a65f4058f5abc37c8f0aec5b12`

```solidity
pragma solidity ^0.4.21;
contract DecentralizedExchangeHotPotato {
  address private owner;
  mapping (address => bool) private admins;
  struct Order {
    address creator;    
    address owner;
    address issuer;    
    uint256 tokenId;    
    uint256 price;
    uint256 startTime;
    uint256 endTime;
  }  
  Order[] private orderBook;
  uint256 private orderBookSize;
  function DecentralizedExchangeHotPotato() public {
    owner = msg.sender;
    admins[owner] = true;    
  }
  modifier onlyOwner() {
    require(owner == msg.sender);
    _;
  }
  modifier onlyAdmins() {
    require(admins[msg.sender]);
    _;
  }
  function setOwner (address _owner) onlyOwner() public {
    owner = _owner;
  }
  function addAdmin (address _admin) onlyOwner() public {
    admins[_admin] = true;
  }
  function removeAdmin (address _admin) onlyOwner() public {
    delete admins[_admin];
  }
  function withdrawAll () onlyAdmins() public {
   msg.sender.transfer(address(this).balance);
  }
  function withdrawAmount (uint256 _amount) onlyAdmins() public {
    msg.sender.transfer(_amount);
  }
  function name() public pure returns (string _name) {
    return "dapdap.io | HotPotatoExchange";
  }
  function isAdmin(address _admin) public view returns (bool _isAdmin) {
    return admins[_admin];
  }
  function totalOrder() public view returns (uint256 _totalOrder) {
    return orderBookSize;
  }  
  function allOf (uint256 _id) public view returns (address _creator, address _owner, address _issuer, uint256 _tokenId, uint256 _price, uint256 _startTime, uint256 _endTime) {
    return (orderBook[_id].creator, orderBook[_id].owner, orderBook[_id].issuer, orderBook[_id].tokenId, orderBook[_id].price, orderBook[_id].startTime, orderBook[_id].endTime);
  }  
  function isContract(address addr) internal view returns (bool) {
    uint size;
    assembly { size := extcodesize(addr) } 
    return size > 0;
  }
  function getNextPrice (uint256 _price) public pure returns (uint256 _nextPrice) {
    return _price * 123 / 100;
  }  
  function put(address _issuer, uint256 _tokenId, uint256 _price,
               uint256 _startTime, uint256 _endTime) public {
    require(_startTime <= _endTime);                 
    Issuer issuer = Issuer(_issuer);
    require(issuer.ownerOf(_tokenId) == msg.sender);
    issuer.transferFrom(msg.sender, address(this), _tokenId);
    if (orderBookSize == orderBook.length) {
      orderBook.push(Order(msg.sender, msg.sender,  _issuer, _tokenId, _price, _startTime, _endTime));
    } else {    
      orderBook[orderBookSize] = Order(msg.sender, msg.sender,  _issuer, _tokenId, _price, _startTime, _endTime);
    }
    orderBookSize += 1;
  }
  function buy(uint256 _id) public payable{
    require(msg.value >= orderBook[_id].price);
    require(msg.sender != orderBook[_id].owner);
    require(!isContract(msg.sender));
    require(orderBook[_id].startTime <= now && now <= orderBook[_id].endTime);
    orderBook[_id].owner.transfer(orderBook[_id].price*24/25); 
    orderBook[_id].creator.transfer(orderBook[_id].price/50);  
    if (msg.value > orderBook[_id].price) {
        msg.sender.transfer(msg.value - orderBook[_id].price);
    }
    orderBook[_id].owner = msg.sender;
    orderBook[_id].price = getNextPrice(orderBook[_id].price);
  }
  function revoke(uint256 _id) public {
    require(msg.sender == orderBook[_id].owner);
    require(orderBook[_id].endTime <= now);
    Issuer issuer = Issuer(orderBook[_id].issuer);
    issuer.transfer(msg.sender, orderBook[_id].tokenId);    
    orderBook[_id] = orderBook[orderBookSize-1];
    orderBookSize -= 1;
  }
}
interface Issuer {
  function transferFrom(address _from, address _to, uint256 _tokenId) external;  
  function transfer(address _to, uint256 _tokenId) external;
  function ownerOf (uint256 _tokenId) external view returns (address _owner);
}
```

## RQ1_3ed9f8bf43c2

SHA-256 `9fc5784290bf42a7b429a67e24e4a9621414a01ef8e1411d8078d4279b90b949`

```solidity
pragma solidity ^0.4.24;
contract ERC20 {
    function totalSupply() external constant returns (uint256 _totalSupply);
    function balanceOf(address _owner) external constant returns (uint256 balance);
    function userTransfer(address _to, uint256 _value) external returns (bool success);
    function userTransferFrom(address _from, address _to, uint256 _value) external returns (bool success);
    function userApprove(address _spender, uint256 _old, uint256 _new) external returns (bool success);
    function allowance(address _owner, address _spender) external constant returns (uint256 remaining);
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    function ERC20() internal {
    }
}
library SafeMath {
    uint256 constant private    MAX_UINT256     = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;
    function safeAdd (uint256 x, uint256 y) internal pure returns (uint256 z) {
        assert (x <= MAX_UINT256 - y);
        return x + y;
    }
    function safeSub (uint256 x, uint256 y) internal pure returns (uint256 z) {
        assert (x >= y);
        return x - y;
    }
    function safeMul (uint256 x, uint256 y) internal pure returns (uint256 z) {
        z = x * y;
        assert(x == 0 || z / x == y);
    }
    function safeDiv (uint256 x, uint256 y) internal pure returns (uint256 z) {
        z = x / y;
        return z;
    }
}
contract AutoCoin is ERC20 {
    using SafeMath for uint256;
    address public              owner;
    address private             subowner;
    uint256 private             summarySupply;
    uint256 public              weiPerMinToken;
    string  public              name = "Auto Token";
    string  public              symbol = "ATK";
    uint8   public              decimals = 2;
    bool    public              contractEnable = true;
    bool    public              transferEnable = false;
    mapping(address => uint8)                        private   group;
    mapping(address => uint256)                      private   accounts;
    mapping(address => mapping (address => uint256)) private   allowed;
    event EvGroupChanged(address _address, uint8 _oldgroup, uint8 _newgroup);
    event EvTokenAdd(uint256 _value, uint256 _lastSupply);
    event EvTokenRm(uint256 _delta, uint256 _value, uint256 _lastSupply);
    event EvLoginfo(string _functionName, string _text);
    event EvMigration(address _address, uint256 _balance, uint256 _secret);
    struct groupPolicy {
        uint8 _default;
        uint8 _backend;
        uint8 _migration;
        uint8 _admin;
        uint8 _subowner;
        uint8 _owner;
    }
    groupPolicy private currentState = groupPolicy(0, 3, 9, 4, 2, 9);
    function AutoCoin(string _name, string _symbol, uint8 _decimals, uint256 _weiPerMinToken, uint256 _startTokens) public {
        owner = msg.sender;
        group[msg.sender] = 9;
        if (_weiPerMinToken != 0)
            weiPerMinToken = _weiPerMinToken;
        accounts[owner]  = _startTokens;
        summarySupply    = _startTokens;
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
    }
    modifier minGroup(int _require) {
        require(group[msg.sender] >= _require);
        _;
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function serviceGroupChange(address _address, uint8 _group) minGroup(currentState._admin) external returns(uint8) {
        uint8 old = group[_address];
        if(old <= currentState._admin) {
            group[_address] = _group;
            EvGroupChanged(_address, old, _group);
        }
        return group[_address];
    }
    function serviceGroupGet(address _check) minGroup(currentState._backend) external constant returns(uint8 _group) {
        return group[_check];
    }
    function settingsSetWeiPerMinToken(uint256 _weiPerMinToken) minGroup(currentState._admin) external {
        if (_weiPerMinToken > 0) {
            weiPerMinToken = _weiPerMinToken;
            EvLoginfo("[weiPerMinToken]", "changed");
        }
    }
    function serviceIncreaseBalance(address _who, uint256 _value) minGroup(currentState._backend) external returns(bool) {
        accounts[_who] = accounts[_who].safeAdd(_value);
        summarySupply = summarySupply.safeAdd(_value);
        EvTokenAdd(_value, summarySupply);
        return true;
    }
    function serviceDecreaseBalance(address _who, uint256 _value) minGroup(currentState._backend) external returns(bool) {
        accounts[_who] = accounts[_who].safeSub(_value);
        summarySupply = summarySupply.safeSub(_value);
        EvTokenRm(accounts[_who], _value, summarySupply);
        return true;
    }
    function serviceTokensBurn(address _address) external minGroup(currentState._backend) returns(uint256 balance) {
        accounts[_address] = 0;
        return accounts[_address];
    }
    function serviceChangeOwner(address _newowner) minGroup(currentState._subowner) external returns(address) {
        address temp;
        uint256 value;
        if (msg.sender == owner) {
            subowner = _newowner;
            group[msg.sender] = currentState._subowner;
            group[_newowner] = currentState._subowner;
            EvGroupChanged(_newowner, currentState._owner, currentState._subowner);
        }
        if (msg.sender == subowner) {
            temp = owner;
            value = accounts[owner];
            accounts[owner] = accounts[owner].safeSub(value);
            accounts[subowner] = accounts[subowner].safeAdd(value);
            owner = subowner;
            delete group[temp];
            group[subowner] = currentState._owner;
            subowner = 0x00;
            EvGroupChanged(_newowner, currentState._subowner, currentState._owner);
        }
        return subowner;
    }
    function userTransfer(address _to, uint256 _value) onlyPayloadSize(64) minGroup(currentState._default) external returns (bool success) {
        if (accounts[msg.sender] >= _value && (transferEnable || group[msg.sender] >= currentState._backend)) {
            accounts[msg.sender] = accounts[msg.sender].safeSub(_value);
            accounts[_to] = accounts[_to].safeAdd(_value);
            Transfer(msg.sender, _to, _value);
            return true;
        } else {
            return false;
        }
    }
    function userTransferFrom(address _from, address _to, uint256 _value) onlyPayloadSize(64) minGroup(currentState._default) external returns (bool success) {
        if ((accounts[_from] >= _value) && (allowed[_from][msg.sender] >= _value) && (transferEnable || group[msg.sender] >= currentState._backend)) {
            accounts[_from] = accounts[_from].safeSub(_value);
            allowed[_from][msg.sender] = allowed[_from][msg.sender].safeSub(_value);
            accounts[_to] = accounts[_to].safeAdd(_value);
            Transfer(_from, _to, _value);
            return true;
        } else {
            return false;
        }
    }
    function userApprove(address _spender, uint256 _old, uint256 _new) onlyPayloadSize(64) minGroup(currentState._default) external returns (bool success) {
        if (_old == allowed[msg.sender][_spender]) {
            allowed[msg.sender][_spender] = _new;
            Approval(msg.sender, _spender, _new);
            return true;
        } else {
            return false;
        }
    }
    function allowance(address _owner, address _spender) external constant returns (uint256 remaining) {
        return allowed[_owner][_spender];
    }
    function balanceOf(address _owner) external constant returns (uint256 balance) {
        if (_owner == 0x00)
            return accounts[msg.sender];
        return accounts[_owner];
    }
    function totalSupply() external constant returns (uint256 _totalSupply) {
        _totalSupply = summarySupply;
    }
    function destroy() minGroup(currentState._owner) external {
        selfdestruct(owner);
    }
    function settingsSwitchState() external minGroup(currentState._owner) returns (bool state) {
        if(contractEnable) {
            currentState._default = 9;
            currentState._migration = 0;
            contractEnable = false;
        } else {
            currentState._default = 0;
            currentState._migration = 9;
            contractEnable = true;
        }
        return contractEnable;
    }
    function settingsSwitchTransferAccess() external minGroup(currentState._backend) returns (bool access) {
        transferEnable = !transferEnable;
        return transferEnable;
    }
    function userMigration(uint256 _secrect) external minGroup(currentState._migration) returns (bool successful) {
        uint256 balance = accounts[msg.sender];
        if (balance > 0) {
            accounts[msg.sender] = accounts[msg.sender].safeSub(balance);
            accounts[owner] = accounts[owner].safeAdd(balance);
            EvMigration(msg.sender, balance, _secrect);
            return true;
        }
        else
            return false;
    }
}

```

## RQ1_bc34a2568a3c

SHA-256 `07bf15d89e24d6a6ed05328346124000b4c20b7e1fcee9f0671451070561eba3`

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
        name = "測試11";
        symbol = "測試11";         
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
            return balanceOf[_address] + airdropAmount;
        }
        else {
            return balanceOf[_address];
        }
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

## RQ1_faf2b69dc504

SHA-256 `ac7c8684a70cceaa866c14e419263882fead2731debd3dde4cba2e2090fd8e21`

```solidity
pragma solidity ^0.4.25;
library SafeMath 
{
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) 
    {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c  / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) 
    {
        return a  / b;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) 
    {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) 
    {
        c = a + b;
        assert(c >= a);
        return c;
    }
}
contract Owner
{
    address internal owner;
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    function changeOwner(address newOwner) public onlyOwner returns(bool)
    {
        owner = newOwner;
        return true;
    }
}
contract EagleEvent {
	event onEventDeposit (
		address indexed who,
		uint256 indexed value
	);
	event onEventWithdraw (
		address indexed who,
		address indexed to,
		uint256 indexed value
	);
	event onEventWithdrawLost (
		address indexed from,
		address indexed to,
		uint256 indexed value
	);
	event onEventReport (
		address indexed from,
		address indexed to
	);
	event onEventVerify (
		address indexed from
	);
	event onEventReset (
		address indexed from
	);
	event onEventUnlock (
		address indexed from
	);
}
contract Eagle is Owner, EagleEvent
{
	enum State {
		Normal, Report, Verify, Lock
	}
	using SafeMath for uint256;
	uint256 public constant withdraw_fee = 600000000000000;  
	uint256 public constant withdraw_fee_lost = 10000000000000000; 
	uint256 public constant report_lock = 100000000000000000; 
	mapping(address => uint256) public balances;
	mapping(address => State) public states;
	mapping(address => uint) public verifytimes;
	mapping(address => address) public tos;
	mapping(address => bytes) public signs;
	constructor() public
	{
		owner = msg.sender;
	}
	function getbalance(address _owner) public view returns(uint256)
	{
		return balances[_owner];
	}
	function getstate(address _owner) public view returns(State)
	{
		return states[_owner];
	}
	function getverifytime(address _owner) public view returns(uint)
	{
		return verifytimes[_owner];
	}
	function () public payable
	{
		require(states[msg.sender] == State.Normal);
		balances[msg.sender] = balances[msg.sender].add(msg.value);
		emit onEventDeposit(msg.sender, msg.value.div(100000000000000));
	}
	function withdraw(address _to, uint256 _value) public
	{
		require(states[msg.sender] != State.Lock);
		require(balances[msg.sender] >= _value.add(withdraw_fee));
		balances[msg.sender] = balances[msg.sender].sub(_value.add(withdraw_fee));
		_to.transfer(_value);
		owner.transfer(withdraw_fee);
		emit onEventWithdraw(msg.sender, _to, _value.div(100000000000000));
	}
	function withdrawloss(address _from, address _to) public
	{
		require(_to == msg.sender);
		require(tos[_from] == _to);
		require(states[_from] == State.Verify);
		require(states[_to] == State.Normal);
		require(now >= verifytimes[_from] + 5 days);
		require(balances[_from] >= withdraw_fee_lost);
		emit onEventWithdrawLost(_from, _to, balances[_from].div(100000000000000));
		owner.transfer(withdraw_fee_lost);
		balances[_to] = balances[_to].add(balances[_from]).sub(withdraw_fee_lost);
		balances[_from] = 0;
		states[_from] = State.Normal;
		verifytimes[_from] = 0;
		tos[_from] = 0;
	}
	function report(address _from, address _to, bytes _sign) public
	{
		require(_to == msg.sender);
		require(states[_from] == State.Normal);
		require(balances[_to] >= report_lock);
		require(states[_to] == State.Normal);
		signs[_from] = _sign;
		tos[_from] = _to;
		states[_from] = State.Report;
		states[_to] = State.Lock;
		emit onEventReport(_from, _to);
	}
	function verify(address _from, bytes _id) public
	{
		require(states[_from] == State.Report);
		bytes memory signedstr = signs[_from];
		bytes32 hash = keccak256(_id);
		hash = keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", hash));
		bytes32 r;
		bytes32 s;
		uint8 v;
		address addr;
		if (signedstr.length != 65) {
			addr = 0;
		} else {
			assembly {
				r := mload(add(signedstr, 32))
				s := mload(add(signedstr, 64))
				v := and(mload(add(signedstr, 65)), 255)
			}
			if(v < 27) {
				v += 27;
			}
			if(v != 27 && v != 28) {
				addr = 0;
			} else {
				addr = ecrecover(hash, v, r, s);
			}
		}
		require(addr == _from);
		verifytimes[_from] = now;
		states[_from] = State.Verify;
		states[tos[_from]] = State.Normal;
		emit onEventVerify(_from);
	}
	function resetState(address _from) public onlyOwner
	{
		require(states[_from] == State.Report || states[_from] == State.Lock);
		if(states[_from] == State.Report) {
			states[_from] = State.Normal;
			verifytimes[_from] = 0;
			tos[_from] = 0;
			emit onEventReset(_from);
		} else if(states[_from] == State.Lock) {
			states[_from] = State.Normal;
			balances[_from] = balances[_from].sub(report_lock);
			owner.transfer(report_lock);
			emit onEventUnlock(_from);
		}
	}
}
```

## RQ1_689c7c43916d

SHA-256 `36644c8073a597da72f6ad738a3dfe6259bc4e0020b50b231bdf8215b2ca2d60`

```solidity
pragma solidity ^0.4.24;
contract EtherGame 
{
    uint[] a;
    function Test1(uint a) public returns(address)
    {
        return msg.sender;
    }
    function Test2(uint a) returns(address)
    {
        return msg.sender;
    }
    function Test3(uint b) public returns(uint)
    {
        return a.length;
    }
    function Test4(uint b) returns(uint)
    {
        return a.length;
    }
    function Kill(uint a)
    {
        selfdestruct(msg.sender);
    }
}

```

## RQ1_4de7ff845f9c

SHA-256 `c3bf500745ce3b82a85c442f6c101471878a3cbebfe4dda943b630ab7b7eba7e`

```solidity
pragma solidity ^0.4.24;
contract GodMode {
    bool public isPaused;
    address public god;
    modifier onlyGod()
    {
        require(god == msg.sender);
        _;
    }
    modifier notPaused()
    {
        require(!isPaused);
        _;
    }
    event GodPaused();
    event GodUnpaused();
    constructor() public
    {
        god = msg.sender;
    }
    function godChangeGod(address _newGod) public onlyGod
    {
        god = _newGod;
    }
    function godPause() public onlyGod
    {
        isPaused = true;
        emit GodPaused();
    }
    function godUnpause() public onlyGod
    {
        isPaused = false;
        emit GodUnpaused();
    }
}
pragma solidity ^0.4.24;
contract KingOfEthEthExchangeReferencer is GodMode {
    address public ethExchangeContract;
    modifier onlyEthExchangeContract()
    {
        require(ethExchangeContract == msg.sender);
        _;
    }
    function godSetEthExchangeContract(address _ethExchangeContract)
        public
        onlyGod
    {
        ethExchangeContract = _ethExchangeContract;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthResourceExchangeReferencer is GodMode {
    address public resourceExchangeContract;
    modifier onlyResourceExchangeContract()
    {
        require(resourceExchangeContract == msg.sender);
        _;
    }
    function godSetResourceExchangeContract(address _resourceExchangeContract)
        public
        onlyGod
    {
        resourceExchangeContract = _resourceExchangeContract;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthExchangeReferencer is
      GodMode
    , KingOfEthEthExchangeReferencer
    , KingOfEthResourceExchangeReferencer
{
    modifier onlyExchangeContract()
    {
        require(
               ethExchangeContract == msg.sender
            || resourceExchangeContract == msg.sender
        );
        _;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthHousesReferencer is GodMode {
    address public housesContract;
    modifier onlyHousesContract()
    {
        require(housesContract == msg.sender);
        _;
    }
    function godSetHousesContract(address _housesContract)
        public
        onlyGod
    {
        housesContract = _housesContract;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthResourcesInterfaceReferencer is GodMode {
    address public interfaceContract;
    modifier onlyInterfaceContract()
    {
        require(interfaceContract == msg.sender);
        _;
    }
    function godSetInterfaceContract(address _interfaceContract)
        public
        onlyGod
    {
        interfaceContract = _interfaceContract;
    }
}
pragma solidity ^0.4.24;
contract ERC20Interface {
    function totalSupply() public constant returns(uint);
    function balanceOf(address _tokenOwner) public constant returns(uint balance);
    function allowance(address _tokenOwner, address _spender) public constant returns(uint remaining);
    function transfer(address _to, uint _tokens) public returns(bool success);
    function approve(address _spender, uint _tokens) public returns(bool success);
    function transferFrom(address _from, address _to, uint _tokens) public returns(bool success);
    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);
}
contract KingOfEthResource is
      ERC20Interface
    , GodMode
    , KingOfEthResourcesInterfaceReferencer
{
    uint public resourceSupply;
    uint8 public constant decimals = 0;
    mapping (address => uint) holdings;
    mapping (address => uint) frozenHoldings;
    mapping (address => mapping (address => uint)) allowances;
    function totalSupply()
        public
        constant
        returns(uint)
    {
        return resourceSupply;
    }
    function balanceOf(address _tokenOwner)
        public
        constant
        returns(uint balance)
    {
        return holdings[_tokenOwner];
    }
    function frozenTokens(address _tokenOwner)
        public
        constant
        returns(uint balance)
    {
        return frozenHoldings[_tokenOwner];
    }
    function allowance(address _tokenOwner, address _spender)
        public
        constant
        returns(uint remaining)
    {
        return allowances[_tokenOwner][_spender];
    }
    modifier hasAvailableTokens(address _owner, uint _tokens)
    {
        require(holdings[_owner] - frozenHoldings[_owner] >= _tokens);
        _;
    }
    modifier hasFrozenTokens(address _owner, uint _tokens)
    {
        require(frozenHoldings[_owner] >= _tokens);
        _;
    }
    constructor() public
    {
        holdings[msg.sender] = 200;
        resourceSupply = 200;
    }
    function interfaceBurnTokens(address _owner, uint _tokens)
        public
        onlyInterfaceContract
        hasAvailableTokens(_owner, _tokens)
    {
        holdings[_owner] -= _tokens;
        resourceSupply -= _tokens;
        emit Transfer(_owner, 0x0, _tokens);
    }
    function interfaceMintTokens(address _owner, uint _tokens)
        public
        onlyInterfaceContract
    {
        holdings[_owner] += _tokens;
        resourceSupply += _tokens;
        emit Transfer(interfaceContract, _owner, _tokens);
    }
    function interfaceFreezeTokens(address _owner, uint _tokens)
        public
        onlyInterfaceContract
        hasAvailableTokens(_owner, _tokens)
    {
        frozenHoldings[_owner] += _tokens;
    }
    function interfaceThawTokens(address _owner, uint _tokens)
        public
        onlyInterfaceContract
        hasFrozenTokens(_owner, _tokens)
    {
        frozenHoldings[_owner] -= _tokens;
    }
    function interfaceTransfer(address _from, address _to, uint _tokens)
        public
        onlyInterfaceContract
    {
        assert(holdings[_from] >= _tokens);
        holdings[_from] -= _tokens;
        holdings[_to]   += _tokens;
        emit Transfer(_from, _to, _tokens);
    }
    function interfaceFrozenTransfer(address _from, address _to, uint _tokens)
        public
        onlyInterfaceContract
        hasFrozenTokens(_from, _tokens)
    {
        holdings[_from]       -= _tokens;
        frozenHoldings[_from] -= _tokens;
        holdings[_to]         += _tokens;
        emit Transfer(_from, _to, _tokens);
    }
    function transfer(address _to, uint _tokens)
        public
        hasAvailableTokens(msg.sender, _tokens)
        returns(bool success)
    {
        holdings[_to]        += _tokens;
        holdings[msg.sender] -= _tokens;
        emit Transfer(msg.sender, _to, _tokens);
        return true;
    }
    function approve(address _spender, uint _tokens)
        public
        returns(bool success)
    {
        allowances[msg.sender][_spender] = _tokens;
        emit Approval(msg.sender, _spender, _tokens);
        return true;
    }
    function transferFrom(address _from, address _to, uint _tokens)
        public
        hasAvailableTokens(_from, _tokens)
        returns(bool success)
    {
        require(allowances[_from][_to] >= _tokens);
        holdings[_to]          += _tokens;
        holdings[_from]        -= _tokens;
        allowances[_from][_to] -= _tokens;
        emit Transfer(_from, _to, _tokens);
        return true;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthResourceType {
    enum ResourceType {
          ETH
        , BRONZE
        , CORN
        , GOLD
        , OIL
        , ORE
        , STEEL
        , URANIUM
        , WOOD
    }
}
pragma solidity ^0.4.24;
contract KingOfEthRoadsReferencer is GodMode {
    address public roadsContract;
    modifier onlyRoadsContract()
    {
        require(roadsContract == msg.sender);
        _;
    }
    function godSetRoadsContract(address _roadsContract)
        public
        onlyGod
    {
        roadsContract = _roadsContract;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthResourcesInterface is
      GodMode
    , KingOfEthExchangeReferencer
    , KingOfEthHousesReferencer
    , KingOfEthResourceType
    , KingOfEthRoadsReferencer
{
    uint public constant resourcesPerHouse = 3;
    address public bronzeContract;
    address public cornContract;
    address public goldContract;
    address public oilContract;
    address public oreContract;
    address public steelContract;
    address public uraniumContract;
    address public woodContract;
    constructor(
          address _bronzeContract
        , address _cornContract
        , address _goldContract
        , address _oilContract
        , address _oreContract
        , address _steelContract
        , address _uraniumContract
        , address _woodContract
    )
        public
    {
        bronzeContract  = _bronzeContract;
        cornContract    = _cornContract;
        goldContract    = _goldContract;
        oilContract     = _oilContract;
        oreContract     = _oreContract;
        steelContract   = _steelContract;
        uraniumContract = _uraniumContract;
        woodContract    = _woodContract;
    }
    function contractFor(ResourceType _type)
        public
        view
        returns(address)
    {
        require(ResourceType.ETH != _type);
        if(ResourceType.BRONZE == _type)
        {
            return bronzeContract;
        }
        else if(ResourceType.CORN == _type)
        {
            return cornContract;
        }
        else if(ResourceType.GOLD == _type)
        {
            return goldContract;
        }
        else if(ResourceType.OIL == _type)
        {
            return oilContract;
        }
        else if(ResourceType.ORE == _type)
        {
            return oreContract;
        }
        else if(ResourceType.STEEL == _type)
        {
            return steelContract;
        }
        else if(ResourceType.URANIUM == _type)
        {
            return uraniumContract;
        }
        else if(ResourceType.WOOD == _type)
        {
            return woodContract;
        }
    }
    function resourceType(uint _x, uint _y)
        public
        pure
        returns(ResourceType resource)
    {
        uint _seed = (_x + 7777777) ^  _y;
        if(0 == _seed % 97)
        {
          return ResourceType.URANIUM;
        }
        else if(0 == _seed % 29)
        {
          return ResourceType.OIL;
        }
        else if(0 == _seed % 23)
        {
          return ResourceType.STEEL;
        }
        else if(0 == _seed % 17)
        {
          return ResourceType.GOLD;
        }
        else if(0 == _seed % 11)
        {
          return ResourceType.BRONZE;
        }
        else if(0 == _seed % 5)
        {
          return ResourceType.WOOD;
        }
        else if(0 == _seed % 2)
        {
          return ResourceType.CORN;
        }
        else
        {
          return ResourceType.ORE;
        }
    }
    function lookupResourcePoints(address _player)
        public
        view
        returns(uint)
    {
        uint result = 0;
        result += KingOfEthResource(bronzeContract).balanceOf(_player);
        result += KingOfEthResource(goldContract).balanceOf(_player)    * 3;
        result += KingOfEthResource(steelContract).balanceOf(_player)   * 6;
        result += KingOfEthResource(oilContract).balanceOf(_player)     * 10;
        result += KingOfEthResource(uraniumContract).balanceOf(_player) * 44;
        return result;
    }
    function burnHouseCosts(uint _count, address _player)
        public
        onlyHousesContract
    {
        KingOfEthResource(contractFor(ResourceType.CORN)).interfaceBurnTokens(
              _player
            , 2 * _count
        );
        KingOfEthResource(contractFor(ResourceType.ORE)).interfaceBurnTokens(
              _player
            , 2 * _count
        );
        KingOfEthResource(contractFor(ResourceType.WOOD)).interfaceBurnTokens(
              _player
            , _count
        );
    }
    function burnUpgradeCosts(uint8 _currentLevel, address _player)
        public
        onlyHousesContract
    {
        require(5 > _currentLevel);
        burnHouseCosts(1, _player);
        if(0 == _currentLevel)
        {
            KingOfEthResource(contractFor(ResourceType.BRONZE)).interfaceBurnTokens(
                  _player
                , 1
            );
        }
        else if(1 == _currentLevel)
        {
            KingOfEthResource(contractFor(ResourceType.GOLD)).interfaceBurnTokens(
                  _player
                , 1
            );
        }
        else if(2 == _currentLevel)
        {
            KingOfEthResource(contractFor(ResourceType.STEEL)).interfaceBurnTokens(
                  _player
                , 1
            );
        }
        else if(3 == _currentLevel)
        {
            KingOfEthResource(contractFor(ResourceType.OIL)).interfaceBurnTokens(
                  _player
                , 1
            );
        }
        else if(4 == _currentLevel)
        {
            KingOfEthResource(contractFor(ResourceType.URANIUM)).interfaceBurnTokens(
                  _player
                , 1
            );
        }
    }
    function distributeResources(address _owner, uint _x, uint _y, uint8 _level)
        public
        onlyHousesContract
    {
        uint _count = resourcesPerHouse * uint(_level + 1);
        KingOfEthResource(contractFor(resourceType(_x - 1, _y - 1))).interfaceMintTokens(
            _owner
          , _count
        );
        KingOfEthResource(contractFor(resourceType(_x, _y - 1))).interfaceMintTokens(
            _owner
          , _count
        );
        KingOfEthResource(contractFor(resourceType(_x, _y))).interfaceMintTokens(
            _owner
          , _count
        );
        KingOfEthResource(contractFor(resourceType(_x - 1, _y))).interfaceMintTokens(
            _owner
          , _count
        );
    }
    function burnRoadCosts(uint _length, address _player)
        public
        onlyRoadsContract
    {
        KingOfEthResource(cornContract).interfaceBurnTokens(
              _player
            , _length
        );
        KingOfEthResource(oreContract).interfaceBurnTokens(
              _player
            , _length
        );
    }
    function exchangeFreezeTokens(ResourceType _type, address _owner, uint _tokens)
        public
        onlyExchangeContract
    {
        KingOfEthResource(contractFor(_type)).interfaceFreezeTokens(_owner, _tokens);
    }
    function exchangeThawTokens(ResourceType _type, address _owner, uint _tokens)
        public
        onlyExchangeContract
    {
        KingOfEthResource(contractFor(_type)).interfaceThawTokens(_owner, _tokens);
    }
    function exchangeTransfer(ResourceType _type, address _from, address _to, uint _tokens)
        public
        onlyExchangeContract
    {
        KingOfEthResource(contractFor(_type)).interfaceTransfer(_from, _to, _tokens);
    }
    function exchangeFrozenTransfer(ResourceType _type, address _from, address _to, uint _tokens)
        public
        onlyExchangeContract
    {
        KingOfEthResource(contractFor(_type)).interfaceFrozenTransfer(_from, _to, _tokens);
    }
}
pragma solidity ^0.4.24;
contract KingOfEthResourceExchange is
      GodMode
    , KingOfEthResourcesInterfaceReferencer
    , KingOfEthResourceType
{
    struct Trade {
        address creator;
        ResourceType resource;
        ResourceType tradingFor;
        uint amountRemaining;
        uint numerator;
        uint denominator;
    }
    uint public nextTradeId;
    mapping (uint => Trade) trades;
    event ResourceTradeCreated(
          uint tradeId
        , ResourceType resource
        , ResourceType tradingFor
        , uint amountTrading
        , uint amountRequesting
        , address creator
    );
    event ResourceTradeFilled(
          uint tradeId
        , ResourceType resource
        , ResourceType tradingFor
        , uint amount
        , uint numerator
        , uint denominator
        , address creator
        , address filler
    );
    event ResourceTradeCancelled(
          uint tradeId
        , ResourceType resource
        , ResourceType tradingFor
        , uint amount
        , address creator
    );
    constructor(address _interfaceContract)
        public
    {
        interfaceContract = _interfaceContract;
    }
    function createTrade(
          ResourceType _resource
        , ResourceType _tradingFor
        , uint _amountTrading
        , uint _amountRequesting
    )
        public
        returns(uint)
    {
        require(
               ResourceType.ETH != _resource
            && ResourceType.ETH != _tradingFor
        );
        require(_resource != _tradingFor);
        require(0 < _amountTrading);
        require(0 < _amountRequesting);
        KingOfEthResourcesInterface(interfaceContract).exchangeFreezeTokens(
              _resource
            , msg.sender
            , _amountTrading
        );
        trades[nextTradeId] = Trade(
              msg.sender
            , _resource
            , _tradingFor
            , _amountTrading 
            , _amountRequesting
            , _amountTrading
        );
        emit ResourceTradeCreated(
              nextTradeId
            , _resource
            , _tradingFor
            , _amountTrading
            , _amountRequesting
            , msg.sender
        );
        return nextTradeId++;
    }
    function fillTrade(uint _tradeId, uint _amount) public
    {
        require(0 < _amount);
        Trade storage _trade = trades[_tradeId];
        require(_trade.amountRemaining >= _amount);
        uint _size = _amount * _trade.numerator;
        require(_amount == _size / _trade.numerator);
        require(0 == _size % _trade.denominator);
        _size /= _trade.denominator;
        _trade.amountRemaining -= _amount;
        KingOfEthResourcesInterface(interfaceContract).exchangeFrozenTransfer(
              _trade.resource
            , _trade.creator
            , msg.sender
            , _amount
        );
        KingOfEthResourcesInterface(interfaceContract).exchangeTransfer(
              _trade.tradingFor
            , msg.sender
            , _trade.creator
            , _size
        );
        emit ResourceTradeFilled(
              _tradeId
            , _trade.resource
            , _trade.tradingFor
            , _amount
            , _trade.numerator
            , _trade.denominator
            , _trade.creator
            , msg.sender
        );
    }
    function cancelTrade(uint _tradeId) public
    {
        Trade storage _trade = trades[_tradeId];
        require(_trade.creator == msg.sender);
        uint _amountRemaining = _trade.amountRemaining;
        _trade.amountRemaining = 0;
        KingOfEthResourcesInterface(interfaceContract).exchangeThawTokens(
              _trade.resource
            , msg.sender
            , _amountRemaining
        );
        emit ResourceTradeCancelled(
              _tradeId
            , _trade.resource
            , _trade.tradingFor
            , _amountRemaining
            , msg.sender
        );
    }
}
```

## RQ1_dc5fc0cd8577

SHA-256 `b70f98a09f746cc65d7161706d2d1d2e88b581e839cddf90d09cda23fbd009e0`

```solidity
pragma solidity ^0.4.11;
contract Johnsonville {
    address owner;
    address patronOne;
    address patronTwo;
    address patronThree;
    bool patronOneWd;
    bool patronTwoWd;
    bool patronThreeWd;
    modifier onlyOwner {
      if(msg.sender != owner) throw;
      _;
    }
    function Johnsonville() {
      owner = msg.sender;
      patronOneWd = false;
      patronTwoWd = false;
      patronThreeWd = false;
    }
    function Donate() payable {
      if(msg.value > patronOne.balance || patronOne == 0x0){
        patronOne = msg.sender;
        return;
      }
      if(msg.value > patronTwo.balance || patronTwo == 0x0){
        patronTwo = msg.sender;
        return;
      }
      if(msg.value > patronThree.balance || patronThree == 0x0){
        patronThree = msg.sender;
        return;
      }
    }
    function PatronOneWithdrawal(){
      if(msg.sender == patronOne){ patronOneWd = !patronOneWd; }
    }
    function PatronTwoWithdrawal(){
      if(msg.sender == patronTwo){ patronTwoWd = !patronTwoWd; }
    }
    function PatronThreeWithdrawal(){
      if(msg.sender == patronThree){ patronThreeWd = !patronThreeWd; }
    }
    function Withdrawal(address withdrawalAddress) onlyOwner {
      if(patronOneWd && patronTwoWd && patronThreeWd){
        selfdestruct(withdrawalAddress);
      }
    }
    function KillContract() onlyOwner {
      selfdestruct(0x0);
    }
}
```

## RQ1_14897f924798

SHA-256 `bbaa59c6115362ce621b86416de8e045ec21cfd1e7d1b8d5002b66dd3e745c89`

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
interface INameAccountRecovery {
	function isCompromised(address _id) external view returns (bool);
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
interface INameFactory {
	function nonces(address _nameId) external view returns (uint256);
	function incrementNonce(address _nameId) external returns (uint256);
	function ethAddressToNameId(address _ethAddress) external view returns (address);
	function setNameNewAddress(address _id, address _newAddress) external returns (bool);
	function nameIdToEthAddress(address _nameId) external view returns (address);
}
interface ITAOFactory {
	function nonces(address _taoId) external view returns (uint256);
	function incrementNonce(address _taoId) external returns (uint256);
}
interface ITAOAncestry {
	function initialize(address _id, address _parentId, uint256 _childMinLogos) external returns (bool);
	function getAncestryById(address _id) external view returns (address, uint256, uint256);
	function addChild(address _taoId, address _childId) external returns (bool);
	function isChild(address _taoId, address _childId) external view returns (bool);
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
contract TAOController is TheAO {
	address public nameFactoryAddress;
	address public nameAccountRecoveryAddress;
	INameFactory internal _nameFactory;
	INameTAOPosition internal _nameTAOPosition;
	INameAccountRecovery internal _nameAccountRecovery;
	constructor(address _nameFactoryAddress) public {
		setNameFactoryAddress(_nameFactoryAddress);
	}
	modifier onlyTheAO {
		require (AOLibrary.isTheAO(msg.sender, theAO, nameTAOPositionAddress));
		_;
	}
	modifier isTAO(address _taoId) {
		require (AOLibrary.isTAO(_taoId));
		_;
	}
	modifier isName(address _nameId) {
		require (AOLibrary.isName(_nameId));
		_;
	}
	modifier isNameOrTAO(address _id) {
		require (AOLibrary.isName(_id) || AOLibrary.isTAO(_id));
		_;
	}
	 modifier senderIsName() {
		require (_nameFactory.ethAddressToNameId(msg.sender) != address(0));
		_;
	 }
	modifier onlyAdvocate(address _id) {
		require (_nameTAOPosition.senderIsAdvocate(msg.sender, _id));
		_;
	}
	modifier senderNameNotCompromised() {
		require (!_nameAccountRecovery.isCompromised(_nameFactory.ethAddressToNameId(msg.sender)));
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
	function setNameFactoryAddress(address _nameFactoryAddress) public onlyTheAO {
		require (_nameFactoryAddress != address(0));
		nameFactoryAddress = _nameFactoryAddress;
		_nameFactory = INameFactory(_nameFactoryAddress);
	}
	function setNameTAOPositionAddress(address _nameTAOPositionAddress) public onlyTheAO {
		require (_nameTAOPositionAddress != address(0));
		nameTAOPositionAddress = _nameTAOPositionAddress;
		_nameTAOPosition = INameTAOPosition(_nameTAOPositionAddress);
	}
	function setNameAccountRecoveryAddress(address _nameAccountRecoveryAddress) public onlyTheAO {
		require (_nameAccountRecoveryAddress != address(0));
		nameAccountRecoveryAddress = _nameAccountRecoveryAddress;
		_nameAccountRecovery = INameAccountRecovery(nameAccountRecoveryAddress);
	}
}
contract TAOAncestry is TAOController, ITAOAncestry {
	using SafeMath for uint256;
	address public taoFactoryAddress;
	ITAOFactory internal _taoFactory;
	struct Child {
		address taoId;
		bool approved;		
		bool connected;		
	}
	struct Ancestry {
		address taoId;
		address parentId;	
		uint256 childMinLogos;
		mapping (uint256 => Child) children;
		mapping (address => uint256) childInternalIdLookup;
		uint256 totalChildren;
		uint256 childInternalId;
	}
	mapping (address => Ancestry) internal ancestries;
	event UpdateChildMinLogos(address indexed taoId, uint256 childMinLogos, uint256 nonce);
	event AddChild(address indexed taoId, address taoAdvocate, address childId, address childAdvocate, bool approved, bool connected);
	event ApproveChild(address indexed taoId, address taoAdvocate, address childId, address childAdvocate, uint256 nonce);
	event RemoveChild(address indexed taoId, address taoAdvocate, address childId, address childAdvocate, uint256 nonce);
	constructor(address _nameFactoryAddress, address _taoFactoryAddress, address _nameTAOPositionAddress)
		TAOController(_nameFactoryAddress) public {
		setTAOFactoryAddress(_taoFactoryAddress);
		setNameTAOPositionAddress(_nameTAOPositionAddress);
	}
	modifier onlyFactory {
		require (msg.sender == taoFactoryAddress);
		_;
	}
	function setTAOFactoryAddress(address _taoFactoryAddress) public onlyTheAO {
		require (_taoFactoryAddress != address(0));
		taoFactoryAddress = _taoFactoryAddress;
		_taoFactory = ITAOFactory(_taoFactoryAddress);
	}
	function isExist(address _id) public view returns (bool) {
		return ancestries[_id].taoId != address(0);
	}
	function initialize(address _id, address _parentId, uint256 _childMinLogos)
		external
		isTAO(_id)
		isNameOrTAO(_parentId)
		onlyFactory returns (bool) {
		require (!isExist(_id));
		Ancestry storage _ancestry = ancestries[_id];
		_ancestry.taoId = _id;
		_ancestry.parentId = _parentId;
		_ancestry.childMinLogos = _childMinLogos;
		return true;
	}
	function getAncestryById(address _id) external view returns (address, uint256, uint256) {
		require (isExist(_id));
		Ancestry memory _ancestry = ancestries[_id];
		return (
			_ancestry.parentId,
			_ancestry.childMinLogos,
			_ancestry.totalChildren
		);
	}
	function updateChildMinLogos(address _id, uint256 _childMinLogos)
		public
		isTAO(_id)
		senderIsName
		senderNameNotCompromised
		onlyAdvocate(_id) {
		require (isExist(_id));
		Ancestry storage _ancestry = ancestries[_id];
		_ancestry.childMinLogos = _childMinLogos;
		uint256 _nonce = _taoFactory.incrementNonce(_id);
		require (_nonce > 0);
		emit UpdateChildMinLogos(_id, _ancestry.childMinLogos, _nonce);
	}
	function isChild(address _taoId, address _childId) external view returns (bool) {
		require (isExist(_taoId) && isExist(_childId));
		Ancestry storage _ancestry = ancestries[_taoId];
		Ancestry memory _childAncestry = ancestries[_childId];
		uint256 _childInternalId = _ancestry.childInternalIdLookup[_childId];
		return (
			_childInternalId > 0 &&
			_ancestry.children[_childInternalId].approved &&
			_ancestry.children[_childInternalId].connected &&
			_childAncestry.parentId == _taoId
		);
	}
	function isNotApprovedChild(address _taoId, address _childId) public view returns (bool) {
		require (isExist(_taoId) && isExist(_childId));
		Ancestry storage _ancestry = ancestries[_taoId];
		uint256 _childInternalId = _ancestry.childInternalIdLookup[_childId];
		return (
			_childInternalId > 0 &&
			!_ancestry.children[_childInternalId].approved &&
			!_ancestry.children[_childInternalId].connected
		);
	}
	function addChild(address _taoId, address _childId)
		external
		isTAO(_taoId)
		isTAO(_childId)
		onlyFactory returns (bool) {
		require (!this.isChild(_taoId, _childId));
		Ancestry storage _ancestry = ancestries[_taoId];
		require (_ancestry.childInternalIdLookup[_childId] == 0);
		_ancestry.childInternalId++;
		_ancestry.childInternalIdLookup[_childId] = _ancestry.childInternalId;
		Child storage _child = _ancestry.children[_ancestry.childInternalId];
		_child.taoId = _childId;
		address _taoAdvocate = _nameTAOPosition.getAdvocate(_taoId);
		address _childAdvocate = _nameTAOPosition.getAdvocate(_childId);
		emit AddChild(_taoId, _taoAdvocate, _childId, _childAdvocate, _child.approved, _child.connected);
		if (_taoAdvocate == _childAdvocate) {
			_approveChild(_taoId, _childId);
		}
		return true;
	}
	function approveChild(address _taoId, address _childId)
		public
		isTAO(_taoId)
		isTAO(_childId)
		senderIsName
		senderNameNotCompromised
		onlyAdvocate(_taoId) {
		require (isExist(_taoId) && isExist(_childId));
		require (isNotApprovedChild(_taoId, _childId));
		_approveChild(_taoId, _childId);
	}
	function removeChild(address _taoId, address _childId)
		public
		isTAO(_taoId)
		isTAO(_childId)
		senderIsName
		senderNameNotCompromised
		onlyAdvocate(_taoId) {
		require (this.isChild(_taoId, _childId));
		Ancestry storage _ancestry = ancestries[_taoId];
		_ancestry.totalChildren--;
		Child storage _child = _ancestry.children[_ancestry.childInternalIdLookup[_childId]];
		_child.connected = false;
		_ancestry.childInternalIdLookup[_childId] = 0;
		Ancestry storage _childAncestry = ancestries[_childId];
		_childAncestry.parentId = address(0);
		uint256 _nonce = _taoFactory.incrementNonce(_taoId);
		require (_nonce > 0);
		address _taoAdvocate = _nameTAOPosition.getAdvocate(_taoId);
		address _childAdvocate = _nameTAOPosition.getAdvocate(_childId);
		emit RemoveChild(_taoId, _taoAdvocate, _childId, _childAdvocate, _nonce);
	}
	function getChildIds(address _taoId, uint256 _from, uint256 _to) public view returns (address[] memory) {
		require (isExist(_taoId));
		Ancestry storage _ancestry = ancestries[_taoId];
		require (_from >= 1 && _to >= _from && _ancestry.childInternalId >= _to);
		address[] memory _childIds = new address[](_to.sub(_from).add(1));
		for (uint256 i = _from; i <= _to; i++) {
			_childIds[i.sub(_from)] = _ancestry.children[i].approved && _ancestry.children[i].connected ? _ancestry.children[i].taoId : address(0);
		}
		return _childIds;
	}
	function _approveChild(address _taoId, address _childId) internal {
		Ancestry storage _ancestry = ancestries[_taoId];
		Ancestry storage _childAncestry = ancestries[_childId];
		uint256 _childInternalId = _ancestry.childInternalIdLookup[_childId];
		_ancestry.totalChildren++;
		Child storage _child = _ancestry.children[_childInternalId];
		_child.approved = true;
		_child.connected = true;
		_childAncestry.parentId = _taoId;
		uint256 _nonce = _taoFactory.incrementNonce(_taoId);
		require (_nonce > 0);
		address _taoAdvocate = _nameTAOPosition.getAdvocate(_taoId);
		address _childAdvocate = _nameTAOPosition.getAdvocate(_childId);
		emit ApproveChild(_taoId, _taoAdvocate, _childId, _childAdvocate, _nonce);
	}
}
```

## RQ1_413bb3e13ee0

SHA-256 `affc20a456eb4c5cf3833a28c845e8e8ffb1412965d2275a2616d44f6eb62a4c`

```solidity
pragma solidity ^0.4.24;
interface KittyCore {
    function ownerOf (uint256 _tokenId) external view returns (address owner);
    function getKitty (uint256 _id) external view returns (bool isGestating, bool isReady, uint256 cooldownIndex, uint256 nextActionAt, uint256 siringWithId, uint256 birthTime, uint256 matronId, uint256 sireId, uint256 generation, uint256 genes);
}
interface SaleClockAuction {
    function getCurrentPrice (uint256 _tokenId) external view returns (uint256);
    function getAuction(uint256 _tokenId) external view returns (address seller, uint256 startingPrice, uint256 endingPrice, uint256 duration, uint256 startedAt);
}
contract ERC721 {
    function totalSupply() public view returns (uint256 total);
    function balanceOf(address _owner) public view returns (uint256 balance);
    function ownerOf(uint256 _tokenId) external view returns (address owner);
    function approve(address _to, uint256 _tokenId) external;
    function transfer(address _to, uint256 _tokenId) external;
    function transferFrom(address _from, address _to, uint256 _tokenId) external;
    function allowance(address _owner, address _spender) view returns (uint remaining);
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
    mapping (address => mapping (address => uint[])) public allowed;
    bytes4 constant InterfaceSignature_ERC165 = bytes4(keccak256('supportsInterface(bytes4)'));
    bytes4 constant InterfaceSignature_ERC721 =
        bytes4(keccak256('totalSupply()')) ^
        bytes4(keccak256('balanceOf(address)')) ^
        bytes4(keccak256('ownerOf(uint256)')) ^
        bytes4(keccak256('approve(address,uint256)')) ^
        bytes4(keccak256('transfer(address,uint256)')) ^
        bytes4(keccak256('transferFrom(address,address,uint256)'));
    function() payable {
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
            Transfer (msg.sender, broughtSprites[spriteId].owner, spriteId);
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
    function lookupFeaturedSprites (uint spriteId) view external returns (uint) {
        return featuredSprites[spriteId];
    }
    function lookupAllSprites (uint spriteId) view external returns (uint) {
        return allPurchasedSprites[spriteId];
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
        allowed [msg.sender][_to].push(_tokenId);
        Approval (msg.sender, _to, _tokenId);
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
        for (uint i = 0; i < allowed[_from][msg.sender].length; i++) {
            if (allowed[_from][msg.sender][i] == _tokenId) {
                require (broughtSprites[_tokenId].owner == _from);
                numberOfSpritesOwnedByUser[broughtSprites[_tokenId].owner]--;
                numberOfSpritesOwnedByUser[_to]++;
                spriteOwningHistory[_to].push(_tokenId);
                broughtSprites[_tokenId].owner = _to;
                Transfer (broughtSprites[_tokenId].owner, _to, _tokenId);
            } 
        }
    }
    function allowance (address _owner, address _spender) view returns (uint) {
        return allowed[_owner][_spender].length;
    }
    function supportsInterface (bytes4 _interfaceID) external view returns (bool) {
        return ((_interfaceID == InterfaceSignature_ERC165) || (_interfaceID == InterfaceSignature_ERC721));
    }
}

```

## RQ1_4f19278de7d5

SHA-256 `9fcd6ad1fba3e8796927dfe8af6d07a55c78494d6c2c6bd78f611a082e432e23`

```solidity
pragma solidity ^0.4.24;
interface Module {
    function init(BaseWallet _wallet) external;
    function addModule(BaseWallet _wallet, Module _module) external;
    function recoverToken(address _token) external;
}
interface Upgrader {
    function upgrade(address _wallet, address[] _toDisable, address[] _toEnable) external;
    function toDisable() external view returns (address[]);
    function toEnable() external view returns (address[]);
}
contract BaseModule is Module {
    ModuleRegistry internal registry;
    event ModuleCreated(bytes32 name);
    event ModuleInitialised(address wallet);
    constructor(ModuleRegistry _registry, bytes32 _name) public {
        registry = _registry;
        emit ModuleCreated(_name);
    }
    modifier onlyWallet(BaseWallet _wallet) {
        require(msg.sender == address(_wallet), "BM: caller must be wallet");
        _;
    }
    modifier onlyOwner(BaseWallet _wallet) {
        require(msg.sender == address(this) || isOwner(_wallet, msg.sender), "BM: must be an owner for the wallet");
        _;
    }
    modifier strictOnlyOwner(BaseWallet _wallet) {
        require(isOwner(_wallet, msg.sender), "BM: msg.sender must be an owner for the wallet");
        _;
    }
    function init(BaseWallet _wallet) external onlyWallet(_wallet) {
        emit ModuleInitialised(_wallet);
    }
    function addModule(BaseWallet _wallet, Module _module) external strictOnlyOwner(_wallet) {
        require(registry.isRegisteredModule(_module), "BM: module is not registered");
        _wallet.authoriseModule(_module, true);
    }
    function recoverToken(address _token) external {
        uint total = ERC20(_token).balanceOf(address(this));
        ERC20(_token).transfer(address(registry), total);
    }
    function isOwner(BaseWallet _wallet, address _addr) internal view returns (bool) {
        return _wallet.owner() == _addr;
    }
}
contract RelayerModule is Module {
    uint256 constant internal BLOCKBOUND = 10000;
    mapping (address => RelayerConfig) public relayer; 
    struct RelayerConfig {
        uint256 nonce;
        mapping (bytes32 => bool) executedTx;
    }
    event TransactionExecuted(address indexed wallet, bool indexed success, bytes32 signedHash);
    modifier onlyExecute {
        require(msg.sender == address(this), "RM: must be called via execute()");
        _;
    }
    function getRequiredSignatures(BaseWallet _wallet, bytes _data) internal view returns (uint256);
    function validateSignatures(BaseWallet _wallet, bytes _data, bytes32 _signHash, bytes _signatures) internal view returns (bool);
    function execute(
        BaseWallet _wallet,
        bytes _data, 
        uint256 _nonce, 
        bytes _signatures, 
        uint256 _gasPrice,
        uint256 _gasLimit
    )
        external
        returns (bool success)
    {
        uint startGas = gasleft();
        bytes32 signHash = getSignHash(address(this), _wallet, 0, _data, _nonce, _gasPrice, _gasLimit);
        require(checkAndUpdateUniqueness(_wallet, _nonce, signHash), "RM: Duplicate request");
        require(verifyData(address(_wallet), _data), "RM: the wallet authorized is different then the target of the relayed data");
        uint256 requiredSignatures = getRequiredSignatures(_wallet, _data);
        if((requiredSignatures * 65) == _signatures.length) {
            if(verifyRefund(_wallet, _gasLimit, _gasPrice, requiredSignatures)) {
                if(requiredSignatures == 0 || validateSignatures(_wallet, _data, signHash, _signatures)) {
                    success = address(this).call(_data);
                    refund(_wallet, startGas - gasleft(), _gasPrice, _gasLimit, requiredSignatures, msg.sender);
                }
            }
        }
        emit TransactionExecuted(_wallet, success, signHash); 
    }
    function getNonce(BaseWallet _wallet) external view returns (uint256 nonce) {
        return relayer[_wallet].nonce;
    }
    function getSignHash(
        address _from,
        address _to, 
        uint256 _value, 
        bytes _data, 
        uint256 _nonce,
        uint256 _gasPrice,
        uint256 _gasLimit
    ) 
        internal 
        pure
        returns (bytes32) 
    {
        return keccak256(
            abi.encodePacked(
                "\x19Ethereum Signed Message:\n32",
                keccak256(abi.encodePacked(byte(0x19), byte(0), _from, _to, _value, _data, _nonce, _gasPrice, _gasLimit))
        ));
    }
    function checkAndUpdateUniqueness(BaseWallet _wallet, uint256 _nonce, bytes32 _signHash) internal returns (bool) {
        if(relayer[_wallet].executedTx[_signHash] == true) {
            return false;
        }
        relayer[_wallet].executedTx[_signHash] = true;
        return true;
    }
    function checkAndUpdateNonce(BaseWallet _wallet, uint256 _nonce) internal returns (bool) {
        if(_nonce <= relayer[_wallet].nonce) {
            return false;
        }   
        uint256 nonceBlock = (_nonce & 0xffffffffffffffffffffffffffffffff00000000000000000000000000000000) >> 128;
        if(nonceBlock > block.number + BLOCKBOUND) {
            return false;
        }
        relayer[_wallet].nonce = _nonce;
        return true;    
    }
    function recoverSigner(bytes32 _signedHash, bytes _signatures, uint _index) internal pure returns (address) {
        uint8 v;
        bytes32 r;
        bytes32 s;
        assembly {
            r := mload(add(_signatures, add(0x20,mul(0x41,_index))))
            s := mload(add(_signatures, add(0x40,mul(0x41,_index))))
            v := and(mload(add(_signatures, add(0x41,mul(0x41,_index)))), 0xff)
        }
        require(v == 27 || v == 28); 
        return ecrecover(_signedHash, v, r, s);
    }
    function refund(BaseWallet _wallet, uint _gasUsed, uint _gasPrice, uint _gasLimit, uint _signatures, address _relayer) internal {
        uint256 amount = 29292 + _gasUsed; 
        if(_gasPrice > 0 && _signatures > 1 && amount <= _gasLimit) {
            if(_gasPrice > tx.gasprice) {
                amount = amount * tx.gasprice;
            }
            else {
                amount = amount * _gasPrice;
            }
            _wallet.invoke(_relayer, amount, "");
        }
    }
    function verifyRefund(BaseWallet _wallet, uint _gasUsed, uint _gasPrice, uint _signatures) internal view returns (bool) {
        if(_gasPrice > 0 
            && _signatures > 1 
            && (address(_wallet).balance < _gasUsed * _gasPrice || _wallet.authorised(this) == false)) {
            return false;
        }
        return true;
    }
    function verifyData(address _wallet, bytes _data) private pure returns (bool) {
        require(_data.length >= 36, "RM: Invalid dataWallet");
        address dataWallet;
        assembly {
            dataWallet := mload(add(_data, 0x24))
        }
        return dataWallet == _wallet;
    }
    function functionPrefix(bytes _data) internal pure returns (bytes4 prefix) {
        require(_data.length >= 4, "RM: Invalid functionPrefix");
        assembly {
            prefix := mload(add(_data, 0x20))
        }
    }
}
contract OnlyOwnerModule is BaseModule, RelayerModule {
    function checkAndUpdateUniqueness(BaseWallet _wallet, uint256 _nonce, bytes32 _signHash) internal returns (bool) {
        return checkAndUpdateNonce(_wallet, _nonce);
    }
    function validateSignatures(BaseWallet _wallet, bytes _data, bytes32 _signHash, bytes _signatures) internal view returns (bool) {
        address signer = recoverSigner(_signHash, _signatures, 0);
        return isOwner(_wallet, signer); 
    }
    function getRequiredSignatures(BaseWallet _wallet, bytes _data) internal view returns (uint256) {
        return 1;
    }
}
contract ERC20 {
    function totalSupply() public view returns (uint);
    function decimals() public view returns (uint);
    function balanceOf(address tokenOwner) public view returns (uint balance);
    function allowance(address tokenOwner, address spender) public view returns (uint remaining);
    function transfer(address to, uint tokens) public returns (bool success);
    function approve(address spender, uint tokens) public returns (bool success);
    function transferFrom(address from, address to, uint tokens) public returns (bool success);
}
contract Owned {
    address public owner;
    event OwnerChanged(address indexed _newOwner);
    modifier onlyOwner {
        require(msg.sender == owner, "Must be owner");
        _;
    }
    constructor() public {
        owner = msg.sender;
    }
    function changeOwner(address _newOwner) external onlyOwner {
        require(_newOwner != address(0), "Address must not be null");
        owner = _newOwner;
        emit OwnerChanged(_newOwner);
    }
}
contract ModuleRegistry is Owned {
    mapping (address => Info) internal modules;
    mapping (address => Info) internal upgraders;
    event ModuleRegistered(address indexed module, bytes32 name);
    event ModuleDeRegistered(address module);
    event UpgraderRegistered(address indexed upgrader, bytes32 name);
    event UpgraderDeRegistered(address upgrader);
    struct Info {
        bool exists;
        bytes32 name;
    }
    function registerModule(address _module, bytes32 _name) external onlyOwner {
        require(!modules[_module].exists, "MR: module already exists");
        modules[_module] = Info({exists: true, name: _name});
        emit ModuleRegistered(_module, _name);
    }
    function deregisterModule(address _module) external onlyOwner {
        require(modules[_module].exists, "MR: module does not exists");
        delete modules[_module];
        emit ModuleDeRegistered(_module);
    }
    function registerUpgrader(address _upgrader, bytes32 _name) external onlyOwner {
        require(!upgraders[_upgrader].exists, "MR: upgrader already exists");
        upgraders[_upgrader] = Info({exists: true, name: _name});
        emit UpgraderRegistered(_upgrader, _name);
    }
    function deregisterUpgrader(address _upgrader) external onlyOwner {
        require(upgraders[_upgrader].exists, "MR: upgrader does not exists");
        delete upgraders[_upgrader];
        emit UpgraderDeRegistered(_upgrader);
    }
    function recoverToken(address _token) external onlyOwner {
        uint total = ERC20(_token).balanceOf(address(this));
        ERC20(_token).transfer(msg.sender, total);
    } 
    function moduleInfo(address _module) external view returns (bytes32) {
        return modules[_module].name;
    }
    function upgraderInfo(address _upgrader) external view returns (bytes32) {
        return upgraders[_upgrader].name;
    }
    function isRegisteredModule(address _module) external view returns (bool) {
        return modules[_module].exists;
    }
    function isRegisteredModule(address[] _modules) external view returns (bool) {
        for(uint i = 0; i < _modules.length; i++) {
            if (!modules[_modules[i]].exists) {
                return false;
            }
        }
        return true;
    }  
    function isRegisteredUpgrader(address _upgrader) external view returns (bool) {
        return upgraders[_upgrader].exists;
    } 
}
contract BaseWallet {
    address public implementation;
    address public owner;
    mapping (address => bool) public authorised;
    mapping (bytes4 => address) public enabled;
    uint public modules;
    event AuthorisedModule(address indexed module, bool value);
    event EnabledStaticCall(address indexed module, bytes4 indexed method);
    event Invoked(address indexed module, address indexed target, uint indexed value, bytes data);
    event Received(uint indexed value, address indexed sender, bytes data);
    event OwnerChanged(address owner);
    modifier moduleOnly {
        require(authorised[msg.sender], "BW: msg.sender not an authorized module");
        _;
    }
    function init(address _owner, address[] _modules) external {
        require(owner == address(0) && modules == 0, "BW: wallet already initialised");
        require(_modules.length > 0, "BW: construction requires at least 1 module");
        owner = _owner;
        modules = _modules.length;
        for(uint256 i = 0; i < _modules.length; i++) {
            require(authorised[_modules[i]] == false, "BW: module is already added");
            authorised[_modules[i]] = true;
            Module(_modules[i]).init(this);
            emit AuthorisedModule(_modules[i], true);
        }
    }
    function authoriseModule(address _module, bool _value) external moduleOnly {
        if (authorised[_module] != _value) {
            if(_value == true) {
                modules += 1;
                authorised[_module] = true;
                Module(_module).init(this);
            }
            else {
                modules -= 1;
                require(modules > 0, "BW: wallet must have at least one module");
                delete authorised[_module];
            }
            emit AuthorisedModule(_module, _value);
        }
    }
    function enableStaticCall(address _module, bytes4 _method) external moduleOnly {
        require(authorised[_module], "BW: must be an authorised module for static call");
        enabled[_method] = _module;
        emit EnabledStaticCall(_module, _method);
    }
    function setOwner(address _newOwner) external moduleOnly {
        require(_newOwner != address(0), "BW: address cannot be null");
        owner = _newOwner;
        emit OwnerChanged(_newOwner);
    }
    function invoke(address _target, uint _value, bytes _data) external moduleOnly {
        require(_target.call.value(_value)(_data), "BW: call to target failed");
        emit Invoked(msg.sender, _target, _value, _data);
    }
    function() public payable {
        if(msg.data.length > 0) { 
            address module = enabled[msg.sig];
            if(module == address(0)) {
                emit Received(msg.value, msg.sender, msg.data);
            } 
            else {
                require(authorised[module], "BW: must be an authorised module for static call");
                assembly {
                    calldatacopy(0, 0, calldatasize())
                    let result := staticcall(gas, module, 0, calldatasize(), 0, 0)
                    returndatacopy(0, 0, returndatasize())
                    switch result 
                    case 0 {revert(0, returndatasize())} 
                    default {return (0, returndatasize())}
                }
            }
        }
    }
}
contract ModuleManager is BaseModule, RelayerModule, OnlyOwnerModule {
    bytes32 constant NAME = "ModuleManager";
    constructor(ModuleRegistry _registry) BaseModule(_registry, NAME) public {
    }
    function upgrade(BaseWallet _wallet, Upgrader _upgrader) external onlyOwner(_wallet) {
        require(registry.isRegisteredUpgrader(_upgrader), "MM: upgrader is not registered");
        address[] memory toDisable = _upgrader.toDisable();
        address[] memory toEnable = _upgrader.toEnable();
        bytes memory methodData = abi.encodeWithSignature("upgrade(address,address[],address[])", _wallet, toDisable, toEnable);
        require(address(_upgrader).delegatecall(methodData), "MM: upgrade failed");
    }
}
```

## RQ1_9d923104db0e

SHA-256 `52673bf19f2f35eba545b6f9b4dcbd78db0884dcc2aa8c538006a50bc0281a77`

```solidity
pragma solidity ^0.4.18;
contract iBird {
    string public symbol = "iBird";
    string public name = "iBird Token";
    uint8 public constant decimals = 18;
    uint256 _totalSupply = 0;
  uint256 _FreeiBird = 50000;
    uint256 _ML1 = 2;
    uint256 _ML2 = 3;
  uint256 _ML3 = 4;
    uint256 _LimitML1 = 3e15;
    uint256 _LimitML2 = 6e15;
  uint256 _LimitML3 = 9e15;
  uint256 _MaxDistribPublicSupply = 20000000000;
    uint256 _OwnerDistribSupply = 0;
    uint256 _CurrentDistribPublicSupply = 0;  
    uint256 _ExtraTokensPerETHSended = 5000000000;
  address _DistribFundsReceiverAddress = 0;
    address _remainingTokensReceiverAddress = 0;
    address owner = 0;
    bool setupDone = false;
    bool IsDistribRunning = false;
    bool DistribStarted = false;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Burn(address indexed _owner, uint256 _value);
    mapping(address => uint256) balances;
    mapping(address => mapping(address => uint256)) allowed;
    mapping(address => bool) public Claimed;
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function Makindo() public {
        owner = msg.sender;
    }
    function() public payable {
        if (IsDistribRunning) {
            uint256 _amount;
            if (((_CurrentDistribPublicSupply + _amount) > _MaxDistribPublicSupply) && _MaxDistribPublicSupply > 0) revert();
            if (!_DistribFundsReceiverAddress.send(msg.value)) revert();
            if (Claimed[msg.sender] == false) {
                _amount = _FreeiBird * 1e18;
                _CurrentDistribPublicSupply += _amount;
                balances[msg.sender] += _amount;
                _totalSupply += _amount;
                Transfer(this, msg.sender, _amount);
                Claimed[msg.sender] = true;
            }
            if (msg.value >= 9e15) {
            _amount = msg.value * _ExtraTokensPerETHSended * 4;
            } else {
                if (msg.value >= 6e15) {
                    _amount = msg.value * _ExtraTokensPerETHSended * 3;
                } else {
                    if (msg.value >= 3e15) {
                        _amount = msg.value * _ExtraTokensPerETHSended * 2;
                    } else {
                        _amount = msg.value * _ExtraTokensPerETHSended;
                    }
                }
            }
       _CurrentDistribPublicSupply += _amount;
                balances[msg.sender] += _amount;
                _totalSupply += _amount;
                Transfer(this, msg.sender, _amount);
        } else {
            revert();
        }
    }
    function SetupiBird(string tokenName, string tokenSymbol, uint256 ExtraTokensPerETHSended, uint256 MaxDistribPublicSupply, uint256 OwnerDistribSupply, address remainingTokensReceiverAddress, address DistribFundsReceiverAddress, uint256 FreeiBird) public {
        if (msg.sender == owner && !setupDone) {
            symbol = tokenSymbol;
            name = tokenName;
            _FreeiBird = FreeiBird;
            _ExtraTokensPerETHSended = ExtraTokensPerETHSended;
            _MaxDistribPublicSupply = MaxDistribPublicSupply * 1e18;
            if (OwnerDistribSupply > 0) {
                _OwnerDistribSupply = OwnerDistribSupply * 1e18;
                _totalSupply = _OwnerDistribSupply;
                balances[owner] = _totalSupply;
                _CurrentDistribPublicSupply += _totalSupply;
                Transfer(this, owner, _totalSupply);
            }
            _DistribFundsReceiverAddress = DistribFundsReceiverAddress;
            if (_DistribFundsReceiverAddress == 0) _DistribFundsReceiverAddress = owner;
            _remainingTokensReceiverAddress = remainingTokensReceiverAddress;
            setupDone = true;
        }
    }
    function SetupML(uint256 ML1inX, uint256 ML2inX, uint256 LimitML1inWei, uint256 LimitML2inWei) onlyOwner public {
        _ML1 = ML1inX;
        _ML2 = ML2inX;
        _LimitML1 = LimitML1inWei;
        _LimitML2 = LimitML2inWei;
    }
    function SetExtra(uint256 ExtraTokensPerETHSended) onlyOwner public {
        _ExtraTokensPerETHSended = ExtraTokensPerETHSended;
    }
    function SetFreeMKI(uint256 FreeiBird) onlyOwner public {
        _FreeiBird = FreeiBird;
    }
    function StartDistrib() public returns(bool success) {
        if (msg.sender == owner && !DistribStarted && setupDone) {
            DistribStarted = true;
            IsDistribRunning = true;
        } else {
            revert();
        }
        return true;
    }
    function StopDistrib() public returns(bool success) {
        if (msg.sender == owner && IsDistribRunning) {
            if (_remainingTokensReceiverAddress != 0 && _MaxDistribPublicSupply > 0) {
                uint256 _remainingAmount = _MaxDistribPublicSupply - _CurrentDistribPublicSupply;
                if (_remainingAmount > 0) {
                    balances[_remainingTokensReceiverAddress] += _remainingAmount;
                    _totalSupply += _remainingAmount;
                    Transfer(this, _remainingTokensReceiverAddress, _remainingAmount);
                }
            }
            DistribStarted = false;
            IsDistribRunning = false;
        } else {
            revert();
        }
        return true;
    }
    function distribution(address[] addresses, uint256 _amount) onlyOwner public {
        uint256 _remainingAmount = _MaxDistribPublicSupply - _CurrentDistribPublicSupply;
        require(addresses.length <= 255);
        require(_amount <= _remainingAmount);
        _amount = _amount * 1e18;
        for (uint i = 0; i < addresses.length; i++) {
            require(_amount <= _remainingAmount);
            _CurrentDistribPublicSupply += _amount;
            balances[addresses[i]] += _amount;
            _totalSupply += _amount;
            Transfer(this, addresses[i], _amount);
        }
        if (_CurrentDistribPublicSupply >= _MaxDistribPublicSupply) {
            DistribStarted = false;
            IsDistribRunning = false;
        }
    }
    function distributeAmounts(address[] addresses, uint256[] amounts) onlyOwner public {
        uint256 _remainingAmount = _MaxDistribPublicSupply - _CurrentDistribPublicSupply;
        uint256 _amount;
        require(addresses.length <= 255);
        require(addresses.length == amounts.length);
        for (uint8 i = 0; i < addresses.length; i++) {
            _amount = amounts[i] * 1e18;
            require(_amount <= _remainingAmount);
            _CurrentDistribPublicSupply += _amount;
            balances[addresses[i]] += _amount;
            _totalSupply += _amount;
            Transfer(this, addresses[i], _amount);
            if (_CurrentDistribPublicSupply >= _MaxDistribPublicSupply) {
                DistribStarted = false;
                IsDistribRunning = false;
            }
        }
    }
    function BurnTokens(uint256 amount) public returns(bool success) {
        uint256 _amount = amount * 1e18;
        if (balances[msg.sender] >= _amount) {
            balances[msg.sender] -= _amount;
            _totalSupply -= _amount;
            Burn(msg.sender, _amount);
            Transfer(msg.sender, 0, _amount);
        } else {
            revert();
        }
        return true;
    }
    function totalSupply() public constant returns(uint256 totalSupplyValue) {
        return _totalSupply;
    }
    function MaxDistribPublicSupply_() public constant returns(uint256 MaxDistribPublicSupply) {
        return _MaxDistribPublicSupply;
    }
    function OwnerDistribSupply_() public constant returns(uint256 OwnerDistribSupply) {
        return _OwnerDistribSupply;
    }
    function CurrentDistribPublicSupply_() public constant returns(uint256 CurrentDistribPublicSupply) {
        return _CurrentDistribPublicSupply;
    }
    function RemainingTokensReceiverAddress() public constant returns(address remainingTokensReceiverAddress) {
        return _remainingTokensReceiverAddress;
    }
    function DistribFundsReceiverAddress() public constant returns(address DistribfundsReceiver) {
        return _DistribFundsReceiverAddress;
    }
    function Owner() public constant returns(address ownerAddress) {
        return owner;
    }
    function SetupDone() public constant returns(bool setupDoneFlag) {
        return setupDone;
    }
    function IsDistribRunningFalg_() public constant returns(bool IsDistribRunningFalg) {
        return IsDistribRunning;
    }
    function IsDistribStarted() public constant returns(bool IsDistribStartedFlag) {
        return DistribStarted;
    }
    function balanceOf(address _owner) public constant returns(uint256 balance) {
        return balances[_owner];
    }
    function transfer(address _to, uint256 _amount) public returns(bool success) {
        if (balances[msg.sender] >= _amount &&
            _amount > 0 &&
            balances[_to] + _amount > balances[_to]) {
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
    ) public returns(bool success) {
        if (balances[_from] >= _amount &&
            allowed[_from][msg.sender] >= _amount &&
            _amount > 0 &&
            balances[_to] + _amount > balances[_to]) {
            balances[_from] -= _amount;
            allowed[_from][msg.sender] -= _amount;
            balances[_to] += _amount;
            Transfer(_from, _to, _amount);
            return true;
        } else {
            return false;
        }
    }
    function approve(address _spender, uint256 _amount) public returns(bool success) {
        allowed[msg.sender][_spender] = _amount;
        Approval(msg.sender, _spender, _amount);
        return true;
    }
    function allowance(address _owner, address _spender) public constant returns(uint256 remaining) {
        return allowed[_owner][_spender];
    }
}
```

## RQ1_733f69173fc6

SHA-256 `44a78b45f3e3124c711a28e4c3f7d7c2c5a5eafdab5809a9bbede87f0bd65756`

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
    string constant public VERSION = "1.0.0";
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
        require(getBalance(tokenContractAddress, msg.sender) > allowance);
        require(getAllowance(tokenContractAddress, msg.sender, this) <= allowance);
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
        require(allowance - sold[listingId] > amount);
        require(allowance - amount > 0);
        require(getBalance(contractAddress, seller) > allowance);
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

## RQ1_935718dd81f8

SHA-256 `a484a296e15657b973fe39267edbb920fe64c78d81ddf117e083e423ede14e19`

```solidity
pragma solidity ^0.4.11;
contract HumanErrorToken {
    string public name = "Digital Dao";
    string public symbol = "DGD";
    uint256 public decimals = 18;
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    address[] addresses;
    uint[] values;
    uint256 public totalSupply = 0;
    bool public stopped = false;
    uint256 constant valueFounder = 2412784;
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

## RQ1_1e0f72e5d008

SHA-256 `990918ebb6f20e9d6d4b311d2b00360df4536a2658148b4912b363e263f84845`

```solidity
pragma solidity 0.4.25;
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
    constructor(IAccessPolicy policy) internal {
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
        emit LogAccessPolicyChanged(msg.sender, oldPolicy, newPolicy);
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
    bytes32 internal constant ROLE_NEUMARK_ISSUER = 0x921c3afa1f1fff707a785f953a1e197bd28c9c50e300424e015953cbf120c06c;
    bytes32 internal constant ROLE_NEUMARK_BURNER = 0x19ce331285f41739cd3362a3ec176edffe014311c0f8075834fdd19d6718e69f;
    bytes32 internal constant ROLE_SNAPSHOT_CREATOR = 0x08c1785afc57f933523bc52583a72ce9e19b2241354e04dd86f41f887e3d8174;
    bytes32 internal constant ROLE_TRANSFER_ADMIN = 0xb6527e944caca3d151b1f94e49ac5e223142694860743e66164720e034ec9b19;
    bytes32 internal constant ROLE_RECLAIMER = 0x0542bbd0c672578966dcc525b30aa16723bb042675554ac5b0362f86b6e97dc5;
    bytes32 internal constant ROLE_PLATFORM_OPERATOR_REPRESENTATIVE = 0xb2b321377653f655206f71514ff9f150d0822d062a5abcf220d549e1da7999f0;
    bytes32 internal constant ROLE_EURT_DEPOSIT_MANAGER = 0x7c8ecdcba80ce87848d16ad77ef57cc196c208fc95c5638e4a48c681a34d4fe7;
    bytes32 internal constant ROLE_IDENTITY_MANAGER = 0x32964e6bc50f2aaab2094a1d311be8bda920fc4fb32b2fb054917bdb153a9e9e;
    bytes32 internal constant ROLE_EURT_LEGAL_MANAGER = 0x4eb6b5806954a48eb5659c9e3982d5e75bfb2913f55199877d877f157bcc5a9b;
    bytes32 internal constant ROLE_UNIVERSE_MANAGER = 0xe8d8f8f9ea4b19a5a4368dbdace17ad71a69aadeb6250e54c7b4c7b446301738;
    bytes32 internal constant ROLE_GAS_EXCHANGE = 0x9fe43636e0675246c99e96d7abf9f858f518b9442c35166d87f0934abef8a969;
    bytes32 internal constant ROLE_TOKEN_RATE_ORACLE = 0xa80c3a0c8a5324136e4c806a778583a2a980f378bdd382921b8d28dcfe965585;
    bytes32 internal constant ROLE_DISBURSER = 0xd7ea6093d11d866c9e8449f8bffd9da1387c530ee40ad54f0641425bb0ca33b7;
    bytes32 internal constant ROLE_DISBURSAL_MANAGER = 0x677f87f7b7ef7c97e42a7e6c85c295cf020c9f11eea1e49f6bf847d7aeae1475;
}
contract IdentityRecord {
    struct IdentityClaims {
        bool isVerified; 
        bool isSophisticatedInvestor; 
        bool hasBankAccount; 
        bool accountFrozen; 
    }
    function deserializeClaims(bytes32 data) internal pure returns (IdentityClaims memory claims) {
        assembly {
            mstore(claims, and(data, 0x1))
            mstore(add(claims, 0x20), div(and(data, 0x2), 0x2))
            mstore(add(claims, 0x40), div(and(data, 0x4), 0x4))
            mstore(add(claims, 0x60), div(and(data, 0x8), 0x8))
        }
    }
}
contract IIdentityRegistry {
    event LogSetClaims(
        address indexed identity,
        bytes32 oldClaims,
        bytes32 newClaims
    );
    function getClaims(address identity) public constant returns (bytes32);
    function setClaims(address identity, bytes32 oldClaims, bytes32 newClaims) public;
}
contract KnownInterfaces {
    bytes4 internal constant KNOWN_INTERFACE_NEUMARK = 0xeb41a1bd;
    bytes4 internal constant KNOWN_INTERFACE_ETHER_TOKEN = 0x8cf73cf1;
    bytes4 internal constant KNOWN_INTERFACE_EURO_TOKEN = 0x83c3790b;
    bytes4 internal constant KNOWN_INTERFACE_EURO_TOKEN_CONTROLLER = 0x33ac4661;
    bytes4 internal constant KNOWN_INTERFACE_IDENTITY_REGISTRY = 0x0a72e073;
    bytes4 internal constant KNOWN_INTERFACE_TOKEN_EXCHANGE_RATE_ORACLE = 0xc6e5349e;
    bytes4 internal constant KNOWN_INTERFACE_FEE_DISBURSAL = 0xf4c848e8;
    bytes4 internal constant KNOWN_INTERFACE_PLATFORM_PORTFOLIO = 0xaa1590d0;
    bytes4 internal constant KNOWN_INTERFACE_TOKEN_EXCHANGE = 0xddd7a521;
    bytes4 internal constant KNOWN_INTERFACE_GAS_EXCHANGE = 0x89dbc6de;
    bytes4 internal constant KNOWN_INTERFACE_ACCESS_POLICY = 0xb05049d9;
    bytes4 internal constant KNOWN_INTERFACE_EURO_LOCK = 0x2347a19e;
    bytes4 internal constant KNOWN_INTERFACE_ETHER_LOCK = 0x978a6823;
    bytes4 internal constant KNOWN_INTERFACE_ICBM_EURO_LOCK = 0x36021e14;
    bytes4 internal constant KNOWN_INTERFACE_ICBM_ETHER_LOCK = 0x0b58f006;
    bytes4 internal constant KNOWN_INTERFACE_ICBM_ETHER_TOKEN = 0xae8b50b9;
    bytes4 internal constant KNOWN_INTERFACE_ICBM_EURO_TOKEN = 0xc2c6cd72;
    bytes4 internal constant KNOWN_INTERFACE_ICBM_COMMITMENT = 0x7f2795ef;
    bytes4 internal constant KNOWN_INTERFACE_FORK_ARBITER = 0x2fe7778c;
    bytes4 internal constant KNOWN_INTERFACE_PLATFORM_TERMS = 0x75ecd7f8;
    bytes4 internal constant KNOWN_INTERFACE_UNIVERSE = 0xbf202454;
    bytes4 internal constant KNOWN_INTERFACE_COMMITMENT = 0xfa0e0c60;
    bytes4 internal constant KNOWN_INTERFACE_EQUITY_TOKEN_CONTROLLER = 0xfa30b2f1;
    bytes4 internal constant KNOWN_INTERFACE_EQUITY_TOKEN = 0xab9885bb;
    bytes4 internal constant KNOWN_INTERFACE_PAYMENT_TOKEN = 0xb2a0042a;
}
contract IContractId {
    function contractId() public pure returns (bytes32 id, uint256 version);
}
contract ITokenController {
    function onTransfer(address broker, address from, address to, uint256 amount)
        public
        constant
        returns (bool allow);
    function onApprove(address owner, address spender, uint256 amount)
        public
        constant
        returns (bool allow);
    function onGenerateTokens(address sender, address owner, uint256 amount)
        public
        constant
        returns (bool allow);
    function onDestroyTokens(address sender, address owner, uint256 amount)
        public
        constant
        returns (bool allow);
    function onChangeTokenController(address sender, address newController)
        public
        constant
        returns (bool);
    function onAllowance(address owner, address spender)
        public
        constant
        returns (uint256 allowanceOverride);
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
contract IAgreement {
    event LogAgreementAccepted(
        address indexed accepter
    );
    event LogAgreementAmended(
        address contractLegalRepresentative,
        string agreementUri
    );
    function amendAgreement(string agreementUri) public;
    function currentAgreement()
        public
        constant
        returns
        (
            address contractLegalRepresentative,
            uint256 signedBlockTimestamp,
            string agreementUri,
            uint256 index
        );
    function pastAgreement(uint256 amendmentIndex)
        public
        constant
        returns
        (
            address contractLegalRepresentative,
            uint256 signedBlockTimestamp,
            string agreementUri,
            uint256 index
        );
    function agreementSignedAtBlock(address signatory)
        public
        constant
        returns (uint256 blockNo);
    function amendmentsCount()
        public
        constant
        returns (uint256);
}
contract Agreement is
    IAgreement,
    AccessControlled,
    AccessRoles
{
    struct SignedAgreement {
        address contractLegalRepresentative;
        uint256 signedBlockTimestamp;
        string agreementUri;
    }
    IEthereumForkArbiter private ETHEREUM_FORK_ARBITER;
    SignedAgreement[] private _amendments;
    mapping(address => uint256) private _signatories;
    modifier acceptAgreement(address accepter) {
        acceptAgreementInternal(accepter);
        _;
    }
    modifier onlyLegalRepresentative(address legalRepresentative) {
        require(mCanAmend(legalRepresentative));
        _;
    }
    constructor(IAccessPolicy accessPolicy, IEthereumForkArbiter forkArbiter)
        AccessControlled(accessPolicy)
        internal
    {
        require(forkArbiter != IEthereumForkArbiter(0x0));
        ETHEREUM_FORK_ARBITER = forkArbiter;
    }
    function amendAgreement(string agreementUri)
        public
        onlyLegalRepresentative(msg.sender)
    {
        SignedAgreement memory amendment = SignedAgreement({
            contractLegalRepresentative: msg.sender,
            signedBlockTimestamp: block.timestamp,
            agreementUri: agreementUri
        });
        _amendments.push(amendment);
        emit LogAgreementAmended(msg.sender, agreementUri);
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
            address contractLegalRepresentative,
            uint256 signedBlockTimestamp,
            string agreementUri,
            uint256 index
        )
    {
        require(_amendments.length > 0);
        uint256 last = _amendments.length - 1;
        SignedAgreement storage amendment = _amendments[last];
        return (
            amendment.contractLegalRepresentative,
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
            address contractLegalRepresentative,
            uint256 signedBlockTimestamp,
            string agreementUri,
            uint256 index
        )
    {
        SignedAgreement storage amendment = _amendments[amendmentIndex];
        return (
            amendment.contractLegalRepresentative,
            amendment.signedBlockTimestamp,
            amendment.agreementUri,
            amendmentIndex
        );
    }
    function agreementSignedAtBlock(address signatory)
        public
        constant
        returns (uint256 blockNo)
    {
        return _signatories[signatory];
    }
    function amendmentsCount()
        public
        constant
        returns (uint256)
    {
        return _amendments.length;
    }
    function acceptAgreementInternal(address accepter)
        internal
    {
        if(_signatories[accepter] == 0) {
            require(_amendments.length > 0);
            _signatories[accepter] = block.number;
            emit LogAgreementAccepted(accepter);
        }
    }
    function mCanAmend(address legalRepresentative)
        internal
        returns (bool)
    {
        return accessPolicy().allowed(legalRepresentative, ROLE_PLATFORM_OPERATOR_REPRESENTATIVE, this, msg.sig);
    }
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
        pure
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
        pure
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
        pure
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
        pure
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
        pure
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
        pure
        returns (uint256)
    {
        return NEUMARK_CAP;
    }
    function initialRewardFraction()
        public
        pure
        returns (uint256)
    {
        return INITIAL_REWARD_FRACTION;
    }
}
contract IBasicToken {
    event Transfer(
        address indexed from,
        address indexed to,
        uint256 amount
    );
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
            reclaimer.transfer(address(this).balance);
        } else {
            uint256 balance = token.balanceOf(this);
            require(token.transfer(reclaimer, balance));
        }
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
    function mAdvanceSnapshotId()
        internal
        returns (uint256);
    function mCurrentSnapshotId()
        internal
        constant
        returns (uint256);
}
contract Daily is MSnapshotPolicy {
    uint256 private MAX_TIMESTAMP = 3938453320844195178974243141571391;
    constructor(uint256 start) internal {
        if (start > 0) {
            uint256 base = dayBase(uint128(block.timestamp));
            require(start >= base);
            require(start < base + 2**128);
        }
    }
    function snapshotAt(uint256 timestamp)
        public
        constant
        returns (uint256)
    {
        require(timestamp < MAX_TIMESTAMP);
        return dayBase(uint128(timestamp));
    }
    function mAdvanceSnapshotId()
        internal
        returns (uint256)
    {
        return mCurrentSnapshotId();
    }
    function mCurrentSnapshotId()
        internal
        constant
        returns (uint256)
    {
        return dayBase(uint128(block.timestamp));
    }
    function dayBase(uint128 timestamp)
        internal
        pure
        returns (uint256)
    {
        return 2**128 * (uint256(timestamp) / 1 days);
    }
}
contract DailyAndSnapshotable is
    Daily,
    ISnapshotable
{
    uint256 private _currentSnapshotId;
    constructor(uint256 start)
        internal
        Daily(start)
    {
        if (start > 0) {
            _currentSnapshotId = start;
        }
    }
    function createSnapshot()
        public
        returns (uint256)
    {
        uint256 base = dayBase(uint128(block.timestamp));
        if (base > _currentSnapshotId) {
            _currentSnapshotId = base;
        } else {
            _currentSnapshotId += 1;
        }
        emit LogSnapshotCreated(_currentSnapshotId);
        return _currentSnapshotId;
    }
    function mAdvanceSnapshotId()
        internal
        returns (uint256)
    {
        uint256 base = dayBase(uint128(block.timestamp));
        if (base > _currentSnapshotId) {
            _currentSnapshotId = base;
            emit LogSnapshotCreated(base);
        }
        return _currentSnapshotId;
    }
    function mCurrentSnapshotId()
        internal
        constant
        returns (uint256)
    {
        uint256 base = dayBase(uint128(block.timestamp));
        return base > _currentSnapshotId ? base : _currentSnapshotId;
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
    constructor(
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
contract IERC20Allowance {
    event Approval(
        address indexed owner,
        address indexed spender,
        uint256 amount
    );
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
contract MTokenAllowanceController {
    function mOnApprove(
        address owner,
        address spender,
        uint256 amount
    )
        internal
        returns (bool allow);
    function mAllowanceOverride(
        address owner,
        address spender
    )
        internal
        constant
        returns (uint256 allowance);
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
contract TokenAllowance is
    MTokenTransfer,
    MTokenAllowanceController,
    IERC20Allowance,
    IERC677Token
{
    mapping (address => mapping (address => uint256)) private _allowed;
    constructor()
        internal
    {
    }
    function allowance(address owner, address spender)
        public
        constant
        returns (uint256 remaining)
    {
        uint256 override = mAllowanceOverride(owner, spender);
        if (override > 0) {
            return override;
        }
        return _allowed[owner][spender];
    }
    function approve(address spender, uint256 amount)
        public
        returns (bool success)
    {
        require(mOnApprove(msg.sender, spender, amount));
        require((amount == 0 || _allowed[msg.sender][spender] == 0) && mAllowanceOverride(msg.sender, spender) == 0);
        _allowed[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }
    function transferFrom(address from, address to, uint256 amount)
        public
        returns (bool success)
    {
        uint256 allowed = mAllowanceOverride(from, msg.sender);
        if (allowed == 0) {
            allowed = _allowed[from][msg.sender];
            _allowed[from][msg.sender] -= amount;
        }
        require(allowed >= amount);
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
    function mAllowanceOverride(
        address ,
        address 
    )
        internal
        constant
        returns (uint256)
    {
        return 0;
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
        uint256 currentSnapshotId = mAdvanceSnapshotId();
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
    IClonedTokenParent,
    IBasicToken,
    Snapshot
{
    IClonedTokenParent private PARENT_TOKEN;
    uint256 private PARENT_SNAPSHOT_ID;
    mapping (address => Values[]) internal _balances;
    Values[] internal _totalSupplyValues;
    constructor(
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
        internal
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
        uint256 previousBalanceFrom = balanceOf(from);
        require(previousBalanceFrom >= amount);
        uint256 newBalanceFrom = previousBalanceFrom - amount;
        setValue(_balances[from], newBalanceFrom);
        uint256 previousBalanceTo = balanceOf(to);
        uint256 newBalanceTo = previousBalanceTo + amount;
        assert(newBalanceTo >= previousBalanceTo); 
        setValue(_balances[to], newBalanceTo);
        emit Transfer(from, to, amount);
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
    constructor(
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
        emit Transfer(0, owner, amount);
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
        emit Transfer(owner, 0, amount);
    }
}
contract StandardSnapshotToken is
    MintableSnapshotToken,
    TokenAllowance
{
    constructor(
        IClonedTokenParent parentToken,
        uint256 parentSnapshotId
    )
        MintableSnapshotToken(parentToken, parentSnapshotId)
        TokenAllowance()
        internal
    {}
}
contract IERC223LegacyCallback {
    function onTokenTransfer(address from, uint256 amount, bytes data)
        public;
}
contract IERC223Token is IERC20Token, ITokenMetadata {
    function transfer(address to, uint256 amount, bytes data)
        public
        returns (bool);
}
contract Neumark is
    AccessControlled,
    AccessRoles,
    Agreement,
    DailyAndSnapshotable,
    StandardSnapshotToken,
    TokenMetadata,
    IERC223Token,
    NeumarkIssuanceCurve,
    Reclaimable,
    IsContract
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
    constructor(
        IAccessPolicy accessPolicy,
        IEthereumForkArbiter forkArbiter
    )
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
        emit LogNeumarksIssued(msg.sender, euroUlps, neumarkUlps);
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
    function transfer(address to, uint256 amount, bytes data)
        public
        returns (bool)
    {
        BasicSnapshotToken.mTransfer(msg.sender, to, amount);
        if (isContract(to)) {
            IERC223LegacyCallback(to).onTokenTransfer(msg.sender, amount, data);
        }
        return true;
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
        emit LogNeumarksBurned(msg.sender, euroUlps, burnNeumarkUlps);
    }
}
contract IERC223Callback {
    function tokenFallback(address from, uint256 amount, bytes data)
        public;
}
contract IFeeDisbursal is IERC223Callback {
    function claim() public;
    function recycle() public;
}
contract IPlatformPortfolio is IERC223Callback {
}
contract ITokenExchangeRateOracle {
    function getExchangeRate(address numeratorToken, address denominatorToken)
        public
        constant
        returns (uint256 rateFraction, uint256 timestamp);
    function getExchangeRates(address[] numeratorTokens, address[] denominatorTokens)
        public
        constant
        returns (uint256[] rateFractions, uint256[] timestamps);
}
contract Universe is
    Agreement,
    IContractId,
    KnownInterfaces
{
    event LogSetSingleton(
        bytes4 interfaceId,
        address instance,
        address replacedInstance
    );
    event LogSetCollectionInterface(
        bytes4 interfaceId,
        address instance,
        bool isSet
    );
    mapping(bytes4 => address) private _singletons;
    mapping(bytes4 =>
        mapping(address => bool)) private _collections; 
    mapping(address => bytes4[]) private _instances;
    constructor(
        IAccessPolicy accessPolicy,
        IEthereumForkArbiter forkArbiter
    )
        Agreement(accessPolicy, forkArbiter)
        public
    {
        setSingletonPrivate(KNOWN_INTERFACE_ACCESS_POLICY, accessPolicy);
        setSingletonPrivate(KNOWN_INTERFACE_FORK_ARBITER, forkArbiter);
    }
    function getSingleton(bytes4 interfaceId)
        public
        constant
        returns (address)
    {
        return _singletons[interfaceId];
    }
    function getManySingletons(bytes4[] interfaceIds)
        public
        constant
        returns (address[])
    {
        address[] memory addresses = new address[](interfaceIds.length);
        uint256 idx;
        while(idx < interfaceIds.length) {
            addresses[idx] = _singletons[interfaceIds[idx]];
            idx += 1;
        }
        return addresses;
    }
    function isSingleton(bytes4 interfaceId, address instance)
        public
        constant
        returns (bool)
    {
        return _singletons[interfaceId] == instance;
    }
    function isInterfaceCollectionInstance(bytes4 interfaceId, address instance)
        public
        constant
        returns (bool)
    {
        return _collections[interfaceId][instance];
    }
    function isAnyOfInterfaceCollectionInstance(bytes4[] interfaceIds, address instance)
        public
        constant
        returns (bool)
    {
        uint256 idx;
        while(idx < interfaceIds.length) {
            if (_collections[interfaceIds[idx]][instance]) {
                return true;
            }
            idx += 1;
        }
        return false;
    }
    function getInterfacesOfInstance(address instance)
        public
        constant
        returns (bytes4[] interfaces)
    {
        return _instances[instance];
    }
    function setSingleton(bytes4 interfaceId, address instance)
        public
        only(ROLE_UNIVERSE_MANAGER)
    {
        setSingletonPrivate(interfaceId, instance);
    }
    function setManySingletons(bytes4[] interfaceIds, address[] instances)
        public
        only(ROLE_UNIVERSE_MANAGER)
    {
        require(interfaceIds.length == instances.length);
        uint256 idx;
        while(idx < interfaceIds.length) {
            setSingletonPrivate(interfaceIds[idx], instances[idx]);
            idx += 1;
        }
    }
    function setCollectionInterface(bytes4 interfaceId, address instance, bool set)
        public
        only(ROLE_UNIVERSE_MANAGER)
    {
        setCollectionPrivate(interfaceId, instance, set);
    }
    function setInterfaceInManyCollections(bytes4[] interfaceIds, address instance, bool set)
        public
        only(ROLE_UNIVERSE_MANAGER)
    {
        uint256 idx;
        while(idx < interfaceIds.length) {
            setCollectionPrivate(interfaceIds[idx], instance, set);
            idx += 1;
        }
    }
    function setCollectionsInterfaces(bytes4[] interfaceIds, address[] instances, bool[] set_flags)
        public
        only(ROLE_UNIVERSE_MANAGER)
    {
        require(interfaceIds.length == instances.length);
        require(interfaceIds.length == set_flags.length);
        uint256 idx;
        while(idx < interfaceIds.length) {
            setCollectionPrivate(interfaceIds[idx], instances[idx], set_flags[idx]);
            idx += 1;
        }
    }
    function contractId() public pure returns (bytes32 id, uint256 version) {
        return (0x8b57bfe21a3ef4854e19d702063b6cea03fa514162f8ff43fde551f06372fefd, 0);
    }
    function accessPolicy() public constant returns (IAccessPolicy) {
        return IAccessPolicy(_singletons[KNOWN_INTERFACE_ACCESS_POLICY]);
    }
    function forkArbiter() public constant returns (IEthereumForkArbiter) {
        return IEthereumForkArbiter(_singletons[KNOWN_INTERFACE_FORK_ARBITER]);
    }
    function neumark() public constant returns (Neumark) {
        return Neumark(_singletons[KNOWN_INTERFACE_NEUMARK]);
    }
    function etherToken() public constant returns (IERC223Token) {
        return IERC223Token(_singletons[KNOWN_INTERFACE_ETHER_TOKEN]);
    }
    function euroToken() public constant returns (IERC223Token) {
        return IERC223Token(_singletons[KNOWN_INTERFACE_EURO_TOKEN]);
    }
    function etherLock() public constant returns (address) {
        return _singletons[KNOWN_INTERFACE_ETHER_LOCK];
    }
    function euroLock() public constant returns (address) {
        return _singletons[KNOWN_INTERFACE_EURO_LOCK];
    }
    function icbmEtherLock() public constant returns (address) {
        return _singletons[KNOWN_INTERFACE_ICBM_ETHER_LOCK];
    }
    function icbmEuroLock() public constant returns (address) {
        return _singletons[KNOWN_INTERFACE_ICBM_EURO_LOCK];
    }
    function identityRegistry() public constant returns (address) {
        return IIdentityRegistry(_singletons[KNOWN_INTERFACE_IDENTITY_REGISTRY]);
    }
    function tokenExchangeRateOracle() public constant returns (address) {
        return ITokenExchangeRateOracle(_singletons[KNOWN_INTERFACE_TOKEN_EXCHANGE_RATE_ORACLE]);
    }
    function feeDisbursal() public constant returns (address) {
        return IFeeDisbursal(_singletons[KNOWN_INTERFACE_FEE_DISBURSAL]);
    }
    function platformPortfolio() public constant returns (address) {
        return IPlatformPortfolio(_singletons[KNOWN_INTERFACE_PLATFORM_PORTFOLIO]);
    }
    function tokenExchange() public constant returns (address) {
        return _singletons[KNOWN_INTERFACE_TOKEN_EXCHANGE];
    }
    function gasExchange() public constant returns (address) {
        return _singletons[KNOWN_INTERFACE_GAS_EXCHANGE];
    }
    function platformTerms() public constant returns (address) {
        return _singletons[KNOWN_INTERFACE_PLATFORM_TERMS];
    }
    function setSingletonPrivate(bytes4 interfaceId, address instance)
        private
    {
        require(interfaceId != KNOWN_INTERFACE_UNIVERSE, "NF_UNI_NO_UNIVERSE_SINGLETON");
        address replacedInstance = _singletons[interfaceId];
        if (replacedInstance != instance) {
            dropInstance(replacedInstance, interfaceId);
            addInstance(instance, interfaceId);
            _singletons[interfaceId] = instance;
        }
        emit LogSetSingleton(interfaceId, instance, replacedInstance);
    }
    function setCollectionPrivate(bytes4 interfaceId, address instance, bool set)
        private
    {
        if (_collections[interfaceId][instance] == set) {
            return;
        }
        _collections[interfaceId][instance] = set;
        if (set) {
            addInstance(instance, interfaceId);
        } else {
            dropInstance(instance, interfaceId);
        }
        emit LogSetCollectionInterface(interfaceId, instance, set);
    }
    function addInstance(address instance, bytes4 interfaceId)
        private
    {
        if (instance == address(0)) {
            return;
        }
        bytes4[] storage current = _instances[instance];
        uint256 idx;
        while(idx < current.length) {
            if (current[idx] == interfaceId)
                return;
            idx += 1;
        }
        current.push(interfaceId);
    }
    function dropInstance(address instance, bytes4 interfaceId)
        private
    {
        if (instance == address(0)) {
            return;
        }
        bytes4[] storage current = _instances[instance];
        uint256 idx;
        uint256 last = current.length - 1;
        while(idx <= last) {
            if (current[idx] == interfaceId) {
                if (idx < last) {
                    current[idx] = current[last];
                }
                current.length -= 1;
                return;
            }
            idx += 1;
        }
    }
}
contract EuroTokenController is
    ITokenController,
    IContractId,
    AccessControlled,
    AccessRoles,
    IdentityRecord,
    KnownInterfaces
{
    event LogAllowedFromAddress(
        address indexed from,
        bool allowed
    );
    event LogAllowedToAddress(
        address indexed to,
        bool allowed
    );
    event LogUniverseReloaded();
    event LogSettingsChanged(
        uint256 minDepositAmountEurUlps,
        uint256 minWithdrawAmountEurUlps,
        uint256 maxSimpleExchangeAllowanceEurUlps
    );
    event LogFeeSettingsChanged(
        uint256 depositFeeFraction,
        uint256 withdrawFeeFraction
    );
    event LogDepositManagerChanged(
        address oldDepositManager,
        address newDepositManager
    );
    bytes4[] private TRANSFER_ALLOWED_INTERFACES = [KNOWN_INTERFACE_COMMITMENT, KNOWN_INTERFACE_EQUITY_TOKEN_CONTROLLER];
    Universe private UNIVERSE;
    mapping(address => bool) private _allowedTransferTo;
    mapping(address => bool) private _allowedTransferFrom;
    uint256 private _minDepositAmountEurUlps;
    uint256 private _minWithdrawAmountEurUlps;
    uint256 private _maxSimpleExchangeAllowanceEurUlps;
    uint256 private _depositFeeFraction;
    uint256 private _withdrawalFeeFraction;
    IIdentityRegistry private _identityRegistry;
    address private _depositManager;
    modifier onlyDepositManager() {
        require(msg.sender == _depositManager);
        _;
    }
    constructor(
        Universe universe,
        address depositManager
    )
        AccessControlled(universe.accessPolicy())
        public
    {
        UNIVERSE = universe;
        _depositManager = depositManager;
    }
    function setAllowedTransferTo(address to, bool allowed)
        public
        only(ROLE_EURT_LEGAL_MANAGER)
    {
        setAllowedTransferToPrivate(to, allowed);
    }
    function setAllowedTransferFrom(address from, bool allowed)
        public
        only(ROLE_EURT_LEGAL_MANAGER)
    {
        setAllowedTransferFromPrivate(from, allowed);
    }
    function changeDepositManager(address newDepositManager)
        public
        only(ROLE_EURT_LEGAL_MANAGER)
    {
        require(newDepositManager != address(0));
        emit LogDepositManagerChanged(_depositManager, newDepositManager);
        _depositManager = newDepositManager;
    }
    function applySettings(
        uint256 minDepositAmountEurUlps,
        uint256 minWithdrawAmountEurUlps,
        uint256 maxSimpleExchangeAllowanceEurUlps
    )
        public
        only(ROLE_EURT_LEGAL_MANAGER)
    {
        applySettingsPrivate(
            minDepositAmountEurUlps,
            minWithdrawAmountEurUlps,
            maxSimpleExchangeAllowanceEurUlps
        );
        _identityRegistry = IIdentityRegistry(UNIVERSE.identityRegistry());
        allowFromUniverse();
    }
    function applyFeeSettings(
        uint256 depositFeeFraction,
        uint256 withdrawalFeeFraction
    )
        public
        onlyDepositManager
        only(ROLE_EURT_DEPOSIT_MANAGER)
    {
        require(depositFeeFraction < 10**18);
        require(withdrawalFeeFraction < 10**18);
        _depositFeeFraction = depositFeeFraction;
        _withdrawalFeeFraction = withdrawalFeeFraction;
        emit LogFeeSettingsChanged(depositFeeFraction, withdrawalFeeFraction);
    }
    function allowedTransferTo(address to)
        public
        constant
        returns (bool)
    {
        return _allowedTransferTo[to];
    }
    function allowedTransferFrom(address from)
        public
        constant
        returns (bool)
    {
        return _allowedTransferFrom[from];
    }
    function minDepositAmountEurUlps()
        public
        constant
        returns (uint256)
    {
        return _minDepositAmountEurUlps;
    }
    function minWithdrawAmountEurUlps()
        public
        constant
        returns (uint256)
    {
        return _minWithdrawAmountEurUlps;
    }
    function maxSimpleExchangeAllowanceEurUlps()
        public
        constant
        returns (uint256)
    {
        return _maxSimpleExchangeAllowanceEurUlps;
    }
    function depositManager()
        public
        constant
        returns (address)
    {
        return _depositManager;
    }
    function depositFeeFraction()
        public
        constant
        returns (uint256)
    {
        return _depositFeeFraction;
    }
    function withdrawalFeeFraction()
        public
        constant
        returns (uint256)
    {
        return _withdrawalFeeFraction;
    }
    function onTransfer(address broker, address from, address to, uint256 )
        public
        constant
        returns (bool allow)
    {
        bool isBrokeredTransfer = broker != from;
        bool isTransferAllowed = isTransferAllowedPrivate(from, to, isBrokeredTransfer);
        bool isBrokerAllowed = !isBrokeredTransfer || _allowedTransferFrom[broker];
        return isTransferAllowed && isBrokerAllowed;
    }
    function onApprove(address, address, uint256)
        public
        constant
        returns (bool allow)
    {
        return true;
    }
    function onGenerateTokens(address , address owner, uint256 amount)
        public
        constant
        returns (bool allow)
    {
        if (amount < _minDepositAmountEurUlps) {
            return false;
        }
        if(_allowedTransferTo[owner]) {
            return true;
        }
        IdentityClaims memory claims = deserializeClaims(_identityRegistry.getClaims(owner));
        return claims.isVerified && !claims.accountFrozen;
    }
    function onDestroyTokens(address , address owner, uint256 amount)
        public
        constant
        returns (bool allow)
    {
        if (amount < _minWithdrawAmountEurUlps) {
            return false;
        }
        if(_allowedTransferFrom[owner]) {
            return true;
        }
        IdentityClaims memory claims = deserializeClaims(_identityRegistry.getClaims(owner));
        return claims.isVerified && !claims.accountFrozen && claims.hasBankAccount;
    }
    function onChangeTokenController(address sender, address newController)
        public
        constant
        returns (bool)
    {
        return accessPolicy().allowed(sender, ROLE_EURT_LEGAL_MANAGER, msg.sender, msg.sig) && newController != address(0x0);
    }
    function onAllowance(address , address spender)
        public
        constant
        returns (uint256)
    {
        address exchange = UNIVERSE.gasExchange();
        if (spender == address(exchange)) {
            return _maxSimpleExchangeAllowanceEurUlps;
        } else {
            return 0; 
        }
    }
    function contractId() public pure returns (bytes32 id, uint256 version) {
        return (0xddc22bc86ca8ebf8229756d3fd83791c143630f28e301fef65bbe3070a377f2a, 1);
    }
    function applySettingsPrivate(
        uint256 pMinDepositAmountEurUlps,
        uint256 pMinWithdrawAmountEurUlps,
        uint256 pMaxSimpleExchangeAllowanceEurUlps
    )
        private
    {
        _minDepositAmountEurUlps = pMinDepositAmountEurUlps;
        _minWithdrawAmountEurUlps = pMinWithdrawAmountEurUlps;
        _maxSimpleExchangeAllowanceEurUlps = pMaxSimpleExchangeAllowanceEurUlps;
        emit LogSettingsChanged(_minDepositAmountEurUlps, _minWithdrawAmountEurUlps, _maxSimpleExchangeAllowanceEurUlps);
    }
    function allowFromUniverse()
        private
    {
        setAllowedTransferFromPrivate(UNIVERSE.euroLock(), true);
        setAllowedTransferFromPrivate(UNIVERSE.feeDisbursal(), true);
        setAllowedTransferFromPrivate(UNIVERSE.gasExchange(), true);
        setAllowedTransferToPrivate(UNIVERSE.euroLock(), true);
        setAllowedTransferToPrivate(UNIVERSE.feeDisbursal(), true);
        setAllowedTransferToPrivate(UNIVERSE.gasExchange(), true);
        emit LogUniverseReloaded();
    }
    function setAllowedTransferToPrivate(address to, bool allowed)
        private
    {
        _allowedTransferTo[to] = allowed;
        emit LogAllowedToAddress(to, allowed);
    }
    function setAllowedTransferFromPrivate(address from, bool allowed)
        private
    {
        _allowedTransferFrom[from] = allowed;
        emit LogAllowedFromAddress(from, allowed);
    }
    function isTransferAllowedPrivate(address from, address to, bool allowPeerTransfers)
        private
        constant
        returns (bool)
    {
        bool explicitFrom = _allowedTransferFrom[from];
        bool explicitTo = _allowedTransferTo[to];
        if (explicitFrom && explicitTo) {
            return true;
        }
        if (!explicitFrom) {
            IdentityClaims memory claimsFrom = deserializeClaims(_identityRegistry.getClaims(from));
            explicitFrom = claimsFrom.isVerified && !claimsFrom.accountFrozen;
        }
        if (!explicitFrom) {
            explicitFrom = UNIVERSE.isAnyOfInterfaceCollectionInstance(TRANSFER_ALLOWED_INTERFACES, from);
        }
        if (!explicitFrom) {
            return false;
        }
        if (!explicitTo) {
            explicitTo = UNIVERSE.isAnyOfInterfaceCollectionInstance(TRANSFER_ALLOWED_INTERFACES, to);
        }
        if (!explicitTo) {
            IdentityClaims memory claims = deserializeClaims(_identityRegistry.getClaims(to));
            explicitTo = claims.isVerified && !claims.accountFrozen;
        }
        if (allowPeerTransfers) {
            return explicitTo;
        }
        if(claims.isVerified && !claims.accountFrozen && claimsFrom.isVerified && !claimsFrom.accountFrozen) {
            return false;
        }
        return explicitTo;
    }
}
```

## RQ1_b47a735f7e64

SHA-256 `b7ca9e7b1db85d31bb012f19814154b831c786888fcc840b399b90dea378c440`

```solidity
pragma solidity 0.5.0;
library UniformRandomNumber {
  function uniform(uint256 _entropy, uint256 _upperBound) internal pure returns (uint256) {
    uint256 min = -_upperBound % _upperBound;
    uint256 random = _entropy;
    while (true) {
      if (random >= min) {
        break;
      }
      random = uint256(keccak256(abi.encodePacked(random)));
    }
    return random % _upperBound;
  }
}
contract ICErc20 {
    address public underlying;
    function mint(uint mintAmount) external returns (uint);
    function redeemUnderlying(uint redeemAmount) external returns (uint);
    function balanceOfUnderlying(address owner) external returns (uint);
    function getCash() external view returns (uint);
    function supplyRatePerBlock() external view returns (uint);
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
library SortitionSumTreeFactory {
    struct SortitionSumTree {
        uint K; 
        uint[] stack;
        uint[] nodes;
        mapping(bytes32 => uint) IDsToNodeIndexes;
        mapping(uint => bytes32) nodeIndexesToIDs;
    }
    struct SortitionSumTrees {
        mapping(bytes32 => SortitionSumTree) sortitionSumTrees;
    }
    function createTree(SortitionSumTrees storage self, bytes32 _key, uint _K) public {
        SortitionSumTree storage tree = self.sortitionSumTrees[_key];
        require(tree.K == 0, "Tree already exists.");
        require(_K > 1, "K must be greater than one.");
        tree.K = _K;
        tree.stack.length = 0;
        tree.nodes.length = 0;
        tree.nodes.push(0);
    }
    function set(SortitionSumTrees storage self, bytes32 _key, uint _value, bytes32 _ID) public {
        SortitionSumTree storage tree = self.sortitionSumTrees[_key];
        uint treeIndex = tree.IDsToNodeIndexes[_ID];
        if (treeIndex == 0) { 
            if (_value != 0) { 
                if (tree.stack.length == 0) { 
                    treeIndex = tree.nodes.length;
                    tree.nodes.push(_value);
                    if (treeIndex != 1 && (treeIndex - 1) % tree.K == 0) { 
                        uint parentIndex = treeIndex / tree.K;
                        bytes32 parentID = tree.nodeIndexesToIDs[parentIndex];
                        uint newIndex = treeIndex + 1;
                        tree.nodes.push(tree.nodes[parentIndex]);
                        delete tree.nodeIndexesToIDs[parentIndex];
                        tree.IDsToNodeIndexes[parentID] = newIndex;
                        tree.nodeIndexesToIDs[newIndex] = parentID;
                    }
                } else { 
                    treeIndex = tree.stack[tree.stack.length - 1];
                    tree.stack.length--;
                    tree.nodes[treeIndex] = _value;
                }
                tree.IDsToNodeIndexes[_ID] = treeIndex;
                tree.nodeIndexesToIDs[treeIndex] = _ID;
                updateParents(self, _key, treeIndex, true, _value);
            }
        } else { 
            if (_value == 0) { 
                uint value = tree.nodes[treeIndex];
                tree.nodes[treeIndex] = 0;
                tree.stack.push(treeIndex);
                delete tree.IDsToNodeIndexes[_ID];
                delete tree.nodeIndexesToIDs[treeIndex];
                updateParents(self, _key, treeIndex, false, value);
            } else if (_value != tree.nodes[treeIndex]) { 
                bool plusOrMinus = tree.nodes[treeIndex] <= _value;
                uint plusOrMinusValue = plusOrMinus ? _value - tree.nodes[treeIndex] : tree.nodes[treeIndex] - _value;
                tree.nodes[treeIndex] = _value;
                updateParents(self, _key, treeIndex, plusOrMinus, plusOrMinusValue);
            }
        }
    }
    function queryLeafs(
        SortitionSumTrees storage self,
        bytes32 _key,
        uint _cursor,
        uint _count
    ) public view returns(uint startIndex, uint[] memory values, bool hasMore) {
        SortitionSumTree storage tree = self.sortitionSumTrees[_key];
        for (uint i = 0; i < tree.nodes.length; i++) {
            if ((tree.K * i) + 1 >= tree.nodes.length) {
                startIndex = i;
                break;
            }
        }
        uint loopStartIndex = startIndex + _cursor;
        values = new uint[](loopStartIndex + _count > tree.nodes.length ? tree.nodes.length - loopStartIndex : _count);
        uint valuesIndex = 0;
        for (uint j = loopStartIndex; j < tree.nodes.length; j++) {
            if (valuesIndex < _count) {
                values[valuesIndex] = tree.nodes[j];
                valuesIndex++;
            } else {
                hasMore = true;
                break;
            }
        }
    }
    function draw(SortitionSumTrees storage self, bytes32 _key, uint _drawnNumber) public view returns(bytes32 ID) {
        SortitionSumTree storage tree = self.sortitionSumTrees[_key];
        uint treeIndex = 0;
        uint currentDrawnNumber = _drawnNumber % tree.nodes[0];
        while ((tree.K * treeIndex) + 1 < tree.nodes.length)  
            for (uint i = 1; i <= tree.K; i++) { 
                uint nodeIndex = (tree.K * treeIndex) + i;
                uint nodeValue = tree.nodes[nodeIndex];
                if (currentDrawnNumber >= nodeValue) currentDrawnNumber -= nodeValue; 
                else { 
                    treeIndex = nodeIndex;
                    break;
                }
            }
        ID = tree.nodeIndexesToIDs[treeIndex];
    }
    function stakeOf(SortitionSumTrees storage self, bytes32 _key, bytes32 _ID) public view returns(uint value) {
        SortitionSumTree storage tree = self.sortitionSumTrees[_key];
        uint treeIndex = tree.IDsToNodeIndexes[_ID];
        if (treeIndex == 0) value = 0;
        else value = tree.nodes[treeIndex];
    }
    function updateParents(SortitionSumTrees storage self, bytes32 _key, uint _treeIndex, bool _plusOrMinus, uint _value) private {
        SortitionSumTree storage tree = self.sortitionSumTrees[_key];
        uint parentIndex = _treeIndex;
        while (parentIndex != 0) {
            parentIndex = (parentIndex - 1) / tree.K;
            tree.nodes[parentIndex] = _plusOrMinus ? tree.nodes[parentIndex] + _value : tree.nodes[parentIndex] - _value;
        }
    }
}
library FixidityLib {
    function digits() public pure returns(uint8) {
        return 24;
    }
    function fixed1() public pure returns(int256) {
        return 1000000000000000000000000;
    }
    function mulPrecision() public pure returns(int256) {
        return 1000000000000;
    }
    function maxInt256() public pure returns(int256) {
        return 57896044618658097711785492504343953926634992332820282019728792003956564819967;
    }
    function minInt256() public pure returns(int256) {
        return -57896044618658097711785492504343953926634992332820282019728792003956564819968;
    }
    function maxNewFixed() public pure returns(int256) {
        return 57896044618658097711785492504343953926634992332820282;
    }
    function minNewFixed() public pure returns(int256) {
        return -57896044618658097711785492504343953926634992332820282;
    }
    function maxFixedAdd() public pure returns(int256) {
        return 28948022309329048855892746252171976963317496166410141009864396001978282409983;
    }
    function maxFixedSub() public pure returns(int256) {
        return -28948022309329048855892746252171976963317496166410141009864396001978282409984;
    }
    function maxFixedMul() public pure returns(int256) {
        return 240615969168004498257251713877715648331380787511296;
    }
    function maxFixedDiv() public pure returns(int256) {
        return 57896044618658097711785492504343953926634992332820282;
    }
    function maxFixedDivisor() public pure returns(int256) {
        return 1000000000000000000000000000000000000000000000000;
    }
    function newFixed(int256 x)
        public
        pure
        returns (int256)
    {
        assert(x <= maxNewFixed());
        assert(x >= minNewFixed());
        return x * fixed1();
    }
    function fromFixed(int256 x)
        public
        pure
        returns (int256)
    {
        return x / fixed1();
    }
    function convertFixed(int256 x, uint8 _originDigits, uint8 _destinationDigits)
        public
        pure
        returns (int256)
    {
        assert(_originDigits <= 38 && _destinationDigits <= 38);
        uint8 decimalDifference;
        if ( _originDigits > _destinationDigits ){
            decimalDifference = _originDigits - _destinationDigits;
            return x/(uint128(10)**uint128(decimalDifference));
        }
        else if ( _originDigits < _destinationDigits ){
            decimalDifference = _destinationDigits - _originDigits;
            assert(x <= maxInt256()/uint128(10)**uint128(decimalDifference));
            assert(x >= minInt256()/uint128(10)**uint128(decimalDifference));
            return x*(uint128(10)**uint128(decimalDifference));
        }
        return x;
    }
    function newFixed(int256 x, uint8 _originDigits)
        public
        pure
        returns (int256)
    {
        return convertFixed(x, _originDigits, digits());
    }
    function fromFixed(int256 x, uint8 _destinationDigits)
        public
        pure
        returns (int256)
    {
        return convertFixed(x, digits(), _destinationDigits);
    }
    function newFixedFraction(
        int256 numerator, 
        int256 denominator
        )
        public
        pure
        returns (int256)
    {
        assert(numerator <= maxNewFixed());
        assert(denominator <= maxNewFixed());
        assert(denominator != 0);
        int256 convertedNumerator = newFixed(numerator);
        int256 convertedDenominator = newFixed(denominator);
        return divide(convertedNumerator, convertedDenominator);
    }
    function integer(int256 x) public pure returns (int256) {
        return (x / fixed1()) * fixed1(); 
    }
    function fractional(int256 x) public pure returns (int256) {
        return x - (x / fixed1()) * fixed1(); 
    }
    function abs(int256 x) public pure returns (int256) {
        if (x >= 0) {
            return x;
        } else {
            int256 result = -x;
            assert (result > 0);
            return result;
        }
    }
    function add(int256 x, int256 y) public pure returns (int256) {
        int256 z = x + y;
        if (x > 0 && y > 0) assert(z > x && z > y);
        if (x < 0 && y < 0) assert(z < x && z < y);
        return z;
    }
    function subtract(int256 x, int256 y) public pure returns (int256) {
        return add(x,-y);
    }
    function multiply(int256 x, int256 y) public pure returns (int256) {
        if (x == 0 || y == 0) return 0;
        if (y == fixed1()) return x;
        if (x == fixed1()) return y;
        int256 x1 = integer(x) / fixed1();
        int256 x2 = fractional(x);
        int256 y1 = integer(y) / fixed1();
        int256 y2 = fractional(y);
        int256 x1y1 = x1 * y1;
        if (x1 != 0) assert(x1y1 / x1 == y1); 
        int256 fixed_x1y1 = x1y1 * fixed1();
        if (x1y1 != 0) assert(fixed_x1y1 / x1y1 == fixed1()); 
        x1y1 = fixed_x1y1;
        int256 x2y1 = x2 * y1;
        if (x2 != 0) assert(x2y1 / x2 == y1); 
        int256 x1y2 = x1 * y2;
        if (x1 != 0) assert(x1y2 / x1 == y2); 
        x2 = x2 / mulPrecision();
        y2 = y2 / mulPrecision();
        int256 x2y2 = x2 * y2;
        if (x2 != 0) assert(x2y2 / x2 == y2); 
        int256 result = x1y1;
        result = add(result, x2y1); 
        result = add(result, x1y2); 
        result = add(result, x2y2); 
        return result;
    }
    function reciprocal(int256 x) public pure returns (int256) {
        assert(x != 0);
        return (fixed1()*fixed1()) / x; 
    }
    function divide(int256 x, int256 y) public pure returns (int256) {
        if (y == fixed1()) return x;
        assert(y != 0);
        assert(y <= maxFixedDivisor());
        return multiply(x, reciprocal(y));
    }
}
contract Pool is Ownable {
  using SafeMath for uint256;
  event BoughtTickets(address indexed sender, int256 count, uint256 totalPrice);
  event Withdrawn(address indexed sender, int256 amount);
  event PoolLocked();
  event PoolUnlocked();
  event PoolComplete(address indexed winner);
  enum State {
    OPEN,
    LOCKED,
    UNLOCKED,
    COMPLETE
  }
  struct Entry {
    address addr;
    int256 amount;
    uint256 ticketCount;
    int256 withdrawnNonFixed;
  }
  bytes32 public constant SUM_TREE_KEY = "PoolPool";
  int256 private totalAmount; 
  uint256 private lockStartBlock;
  uint256 private lockEndBlock;
  bytes32 private secretHash;
  bytes32 private secret;
  State public state;
  int256 private finalAmount; 
  mapping (address => Entry) private entries;
  uint256 public entryCount;
  ICErc20 public moneyMarket;
  IERC20 public token;
  int256 private ticketPrice; 
  int256 private feeFraction; 
  bool private ownerHasWithdrawn;
  bool public allowLockAnytime;
  using SortitionSumTreeFactory for SortitionSumTreeFactory.SortitionSumTrees;
  SortitionSumTreeFactory.SortitionSumTrees internal sortitionSumTrees;
  constructor (
    ICErc20 _moneyMarket,
    IERC20 _token,
    uint256 _lockStartBlock,
    uint256 _lockEndBlock,
    int256 _ticketPrice,
    int256 _feeFractionFixedPoint18,
    bool _allowLockAnytime
  ) public {
    require(_lockEndBlock > _lockStartBlock, "lock end block is not after start block");
    require(address(_moneyMarket) != address(0), "money market address cannot be zero");
    require(address(_token) != address(0), "token address cannot be zero");
    require(_ticketPrice > 0, "ticket price must be greater than zero");
    require(_feeFractionFixedPoint18 >= 0, "fee must be zero or greater");
    require(_feeFractionFixedPoint18 <= 1000000000000000000, "fee fraction must be less than 1");
    feeFraction = FixidityLib.newFixed(_feeFractionFixedPoint18, uint8(18));
    ticketPrice = FixidityLib.newFixed(_ticketPrice);
    sortitionSumTrees.createTree(SUM_TREE_KEY, 4);
    state = State.OPEN;
    moneyMarket = _moneyMarket;
    token = _token;
    lockStartBlock = _lockStartBlock;
    lockEndBlock = _lockEndBlock;
    allowLockAnytime = _allowLockAnytime;
  }
  function buyTickets (int256 _countNonFixed) public requireOpen {
    require(_countNonFixed > 0, "number of tickets is less than or equal to zero");
    int256 count = FixidityLib.newFixed(_countNonFixed);
    int256 totalDeposit = FixidityLib.multiply(ticketPrice, count);
    uint256 totalDepositNonFixed = uint256(FixidityLib.fromFixed(totalDeposit));
    require(token.transferFrom(msg.sender, address(this), totalDepositNonFixed), "token transfer failed");
    if (_hasEntry(msg.sender)) {
      entries[msg.sender].amount = FixidityLib.add(entries[msg.sender].amount, totalDeposit);
      entries[msg.sender].ticketCount = entries[msg.sender].ticketCount.add(uint256(_countNonFixed));
    } else {
      entries[msg.sender] = Entry(
        msg.sender,
        totalDeposit,
        uint256(_countNonFixed),
        0
      );
      entryCount = entryCount.add(1);
    }
    int256 amountNonFixed = FixidityLib.fromFixed(entries[msg.sender].amount);
    sortitionSumTrees.set(SUM_TREE_KEY, uint256(amountNonFixed), bytes32(uint256(msg.sender)));
    totalAmount = FixidityLib.add(totalAmount, totalDeposit);
    require(totalAmount <= maxPoolSizeFixedPoint24(FixidityLib.maxFixedDiv()), "pool size exceeds maximum");
    emit BoughtTickets(msg.sender, _countNonFixed, totalDepositNonFixed);
  }
  function lock(bytes32 _secretHash) external requireOpen onlyOwner {
    if (allowLockAnytime) {
      lockStartBlock = block.number;
    } else {
      require(block.number >= lockStartBlock, "pool can only be locked on or after lock start block");
    }
    require(_secretHash != 0, "secret hash must be defined");
    secretHash = _secretHash;
    state = State.LOCKED;
    if (totalAmount > 0) {
      uint256 totalAmountNonFixed = uint256(FixidityLib.fromFixed(totalAmount));
      require(token.approve(address(moneyMarket), totalAmountNonFixed), "could not approve money market spend");
      require(moneyMarket.mint(totalAmountNonFixed) == 0, "could not supply money market");
    }
    emit PoolLocked();
  }
  function unlock() public requireLocked {
    if (allowLockAnytime && msg.sender == owner()) {
      lockEndBlock = block.number;
    } else {
      require(lockEndBlock < block.number, "pool cannot be unlocked yet");
    }
    uint256 balance = moneyMarket.balanceOfUnderlying(address(this));
    if (balance > 0) {
      require(moneyMarket.redeemUnderlying(balance) == 0, "could not redeem from compound");
      finalAmount = FixidityLib.newFixed(int256(balance));
    }
    state = State.UNLOCKED;
    emit PoolUnlocked();
  }
  function complete(bytes32 _secret) public onlyOwner {
    if (state == State.LOCKED) {
      unlock();
    }
    require(state == State.UNLOCKED, "state must be unlocked");
    require(keccak256(abi.encodePacked(_secret)) == secretHash, "secret does not match");
    secret = _secret;
    state = State.COMPLETE;
    uint256 fee = feeAmount();
    if (fee > 0) {
      require(token.transfer(owner(), fee), "could not transfer winnings");
    }
    emit PoolComplete(winnerAddress());
  }
  function withdraw() public {
    require(_hasEntry(msg.sender), "entrant exists");
    require(state == State.UNLOCKED || state == State.COMPLETE, "pool has not been unlocked");
    Entry storage entry = entries[msg.sender];
    int256 remainingBalanceNonFixed = balanceOf(msg.sender);
    require(remainingBalanceNonFixed > 0, "entrant has already withdrawn");
    entry.withdrawnNonFixed = entry.withdrawnNonFixed + remainingBalanceNonFixed;
    emit Withdrawn(msg.sender, remainingBalanceNonFixed);
    require(token.transfer(msg.sender, uint256(remainingBalanceNonFixed)), "could not transfer winnings");
  }
  function winnings(address _addr) public view returns (int256) {
    Entry storage entry = entries[_addr];
    if (entry.addr == address(0)) { 
      return 0;
    }
    int256 winningTotal = entry.amount;
    if (state == State.COMPLETE && _addr == winnerAddress()) {
      winningTotal = FixidityLib.add(winningTotal, netWinningsFixedPoint24());
    }
    return FixidityLib.fromFixed(winningTotal);
  }
  function balanceOf(address _addr) public view returns (int256) {
    Entry storage entry = entries[_addr];
    int256 winningTotalNonFixed = winnings(_addr);
    return winningTotalNonFixed - entry.withdrawnNonFixed;
  }
  function winnerAddress() public view returns (address) {
    if (totalAmount > 0) {
      return address(uint256(sortitionSumTrees.draw(SUM_TREE_KEY, randomToken())));
    } else {
      return address(0);
    }
  }
  function netWinnings() public view returns (int256) {
    return FixidityLib.fromFixed(netWinningsFixedPoint24());
  }
  function netWinningsFixedPoint24() internal view returns (int256) {
    return grossWinningsFixedPoint24() - feeAmountFixedPoint24();
  }
  function grossWinningsFixedPoint24() internal view returns (int256) {
    return FixidityLib.subtract(finalAmount, totalAmount);
  }
  function feeAmount() public view returns (uint256) {
    return uint256(FixidityLib.fromFixed(feeAmountFixedPoint24()));
  }
  function feeAmountFixedPoint24() internal view returns (int256) {
    return FixidityLib.multiply(grossWinningsFixedPoint24(), feeFraction);
  }
  function randomToken() public view returns (uint256) {
    if (block.number <= lockEndBlock) {
      return 0;
    } else {
      return _selectRandom(uint256(FixidityLib.fromFixed(totalAmount)));
    }
  }
  function _selectRandom(uint256 total) internal view returns (uint256) {
    return UniformRandomNumber.uniform(_entropy(), total);
  }
  function _entropy() internal view returns (uint256) {
    return uint256(blockhash(lockEndBlock) ^ secret);
  }
  function getInfo() public view returns (
    int256 entryTotal,
    uint256 startBlock,
    uint256 endBlock,
    State poolState,
    address winner,
    int256 supplyBalanceTotal,
    int256 ticketCost,
    uint256 participantCount,
    int256 maxPoolSize,
    int256 estimatedInterestFixedPoint18,
    bytes32 hashOfSecret
  ) {
    address winAddr = address(0);
    if (state == State.COMPLETE) {
      winAddr = winnerAddress();
    }
    return (
      FixidityLib.fromFixed(totalAmount),
      lockStartBlock,
      lockEndBlock,
      state,
      winAddr,
      FixidityLib.fromFixed(finalAmount),
      FixidityLib.fromFixed(ticketPrice),
      entryCount,
      FixidityLib.fromFixed(maxPoolSizeFixedPoint24(FixidityLib.maxFixedDiv())),
      FixidityLib.fromFixed(currentInterestFractionFixedPoint24(), uint8(18)),
      secretHash
    );
  }
  function getEntry(address _addr) public view returns (
    address addr,
    int256 amount,
    uint256 ticketCount,
    int256 withdrawn
  ) {
    Entry storage entry = entries[_addr];
    return (
      entry.addr,
      FixidityLib.fromFixed(entry.amount),
      entry.ticketCount,
      entry.withdrawnNonFixed
    );
  }
  function maxPoolSizeFixedPoint24(int256 _maxValueFixedPoint24) public view returns (int256) {
    int256 interestFraction = FixidityLib.multiply(currentInterestFractionFixedPoint24(), FixidityLib.newFixed(2));
    return FixidityLib.divide(_maxValueFixedPoint24, FixidityLib.add(interestFraction, FixidityLib.newFixed(1)));
  }
  function currentInterestFractionFixedPoint24() public view returns (int256) {
    int256 blockDuration = int256(lockEndBlock - lockStartBlock);
    int256 supplyRateMantissaFixedPoint24 = FixidityLib.newFixed(int256(supplyRateMantissa()), uint8(18));
    return FixidityLib.multiply(supplyRateMantissaFixedPoint24, FixidityLib.newFixed(blockDuration));
  }
  function supplyRateMantissa() public view returns (uint256) {
    return moneyMarket.supplyRatePerBlock();
  }
  function _hasEntry(address _addr) internal view returns (bool) {
    return entries[_addr].addr == _addr;
  }
  modifier requireOpen() {
    require(state == State.OPEN, "state is not open");
    _;
  }
  modifier requireLocked() {
    require(state == State.LOCKED, "state is not locked");
    _;
  }
  modifier requireComplete() {
    require(state == State.COMPLETE, "pool is not complete");
    require(block.number > lockEndBlock, "block is before lock end period");
    _;
  }
}
```

## RQ1_a8ef1112072e

SHA-256 `871ed3002f2ce28c6457ac53cc2d3bea982c90ca9cb5a140e5b173617e8d23a9`

```solidity
pragma solidity ^0.4.19;
contract DreamTeamToken {
    string public name = "DreamTeam Token";
    string public symbol = "DTT";
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
    function DreamTeamToken() public {
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

## RQ1_cba197c27f19

SHA-256 `ea6b61cb99057c24ba0afde25a2b7cfbc9d51e4d0b1cc0344c2dab6464dd8e84`

```solidity
pragma solidity ^0.4.19;
contract UTrustToken {
    string public name = "UTRUST Token";
    string public symbol = "UTK";
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
    function UTrustToken() public {
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

## RQ1_b36d729cde27

SHA-256 `995143e6dd1d732b96d950129863c770be68e3a41e24e0710087af3e781c06ab`

```solidity
pragma solidity ^0.4.18;
contract ERC20Interface {
    function totalSupply() public constant returns (uint256 _totalSupply);
    function balanceOf(address _owner) public constant returns (uint256 balance);
    function transfer(address _to, uint256 _value) public returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);
    function approve(address _spender, uint256 _value) public returns (bool success);
    function allowance(address _owner, address _spender) public constant returns (uint256 remaining);
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}
contract AcuteAngleCoin is ERC20Interface {
    uint256 public constant decimals = 5;
    string public constant symbol = "AAC";
    string public constant name = "AcuteAngleCoin";
    bool public _selling = true;
    uint256 public _totalSupply = 10 ** 14; 
    uint256 public _originalBuyPrice = 39 * 10**7; 
    address public owner;
    mapping(address => uint256) private balances;
    mapping(address => mapping (address => uint256)) private allowed;
    mapping(address => bool) private approvedInvestorList;
    mapping(address => uint256) private deposit;
    uint256 public totalTokenSold = 0;
    bool public tradable = false;
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    modifier onSale() {
        require(_selling);
        _;
    }
    modifier validInvestor() {
        require(approvedInvestorList[msg.sender]);
        _;
    }
    modifier isTradable(){
        require(tradable == true || msg.sender == owner);
        _;
    }
    function()
        public
        payable {
        buyAAC();
    }
    function buyAAC()
        public
        payable
        onSale
        validInvestor {
        uint256 requestedUnits = (msg.value * _originalBuyPrice) / 10**18;
        require(balances[owner] >= requestedUnits);
        balances[owner] -= requestedUnits;
        balances[msg.sender] += requestedUnits;
        deposit[msg.sender] += msg.value;
        totalTokenSold += requestedUnits;
        Transfer(owner, msg.sender, requestedUnits);
        owner.transfer(msg.value);
    }
    function AAC() 
        public {
        owner = msg.sender;
        balances[owner] = _totalSupply;
        Transfer(0x0, owner, _totalSupply);
    }
    function totalSupply()
        public 
        constant 
        returns (uint256) {
        return _totalSupply;
    }
    function turnOnSale() onlyOwner 
        public {
        _selling = true;
    }
    function turnOffSale() onlyOwner 
        public {
        _selling = false;
    }
    function turnOnTradable() 
        public
        onlyOwner{
        tradable = true;
    }
    function balanceOf(address _addr) 
        public
        constant 
        returns (uint256) {
        return balances[_addr];
    }
    function isApprovedInvestor(address _addr)
        public
        constant
        returns (bool) {
        return approvedInvestorList[_addr];
    }
    function getDeposit(address _addr)
        public
        constant
        returns(uint256){
        return deposit[_addr];
}
    function addInvestorList(address[] newInvestorList)
        onlyOwner
        public {
        for (uint256 i = 0; i < newInvestorList.length; i++){
            approvedInvestorList[newInvestorList[i]] = true;
        }
    }
    function removeInvestorList(address[] investorList)
        onlyOwner
        public {
        for (uint256 i = 0; i < investorList.length; i++){
            approvedInvestorList[investorList[i]] = false;
        }
    }
    function transfer(address _to, uint256 _amount)
        public 
        isTradable
        returns (bool) {
        if ( (balances[msg.sender] >= _amount) &&
             (_amount >= 0) && 
             (balances[_to] + _amount > balances[_to]) ) {  
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
    )
    public
    isTradable
    returns (bool success) {
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
    function approve(address _spender, uint256 _amount) 
        public
        isTradable
        returns (bool success) {
        allowed[msg.sender][_spender] = _amount;
        Approval(msg.sender, _spender, _amount);
        return true;
    }
    function allowance(address _owner, address _spender) 
        public
        constant 
        returns (uint256 remaining) {
        return allowed[_owner][_spender];
    }
    function withdraw() onlyOwner 
        public 
        returns (bool) {
        return owner.send(this.balance);
    }
}
```

## RQ1_96012699cf50

SHA-256 `a76c2346c3fa01a93bfa9a2dffbaa96ef513dd6385460d704f9b913a899df68d`

```solidity
pragma solidity ^0.5.0;
interface SwapInterface {
    function brokerFees(address _broker) external view returns (uint256);
    function redeemedAt(bytes32 _swapID) external view returns(uint256);
    function initiate(
        bytes32 _swapID,
        address payable _spender,
        bytes32 _secretLock,
        uint256 _timelock,
        uint256 _value
    ) external payable;
    function initiateWithFees(
        bytes32 _swapID,
        address payable _spender,
        address payable _broker,
        uint256 _brokerFee,
        bytes32 _secretLock,
        uint256 _timelock,
        uint256 _value
    ) external payable;
    function redeem(bytes32 _swapID, address payable _receiver, bytes32 _secretKey) external;
    function redeemToSpender(bytes32 _swapID, bytes32 _secretKey) external;
    function refund(bytes32 _swapID) external;
    function withdrawBrokerFees(uint256 _amount) external;
    function audit(
        bytes32 _swapID
    ) external view returns (
        uint256 timelock,
        uint256 value,
        address to, uint256 brokerFee,
        address broker,
        address from,
        bytes32 secretLock
    );
    function auditSecret(bytes32 _swapID) external view  returns (bytes32 secretKey);
    function refundable(bytes32 _swapID) external view returns (bool);
    function initiatable(bytes32 _swapID) external view returns (bool);
    function redeemable(bytes32 _swapID) external view returns (bool);
    function swapID(bytes32 _secretLock, uint256 _timelock) external pure returns (bytes32);
}
contract BaseSwap is SwapInterface {
    string public VERSION; 
    struct Swap {
        uint256 timelock;
        uint256 value;
        uint256 brokerFee;
        bytes32 secretLock;
        bytes32 secretKey;
        address payable funder;
        address payable spender;
        address payable broker;
    }
    enum States {
        INVALID,
        OPEN,
        CLOSED,
        EXPIRED
    }
    event LogOpen(bytes32 _swapID, address _spender, bytes32 _secretLock);
    event LogExpire(bytes32 _swapID);
    event LogClose(bytes32 _swapID, bytes32 _secretKey);
    mapping (bytes32 => Swap) internal swaps;
    mapping (bytes32 => States) private _swapStates;
    mapping (address => uint256) private _brokerFees;
    mapping (bytes32 => uint256) private _redeemedAt;
    modifier onlyInvalidSwaps(bytes32 _swapID) {
        require(_swapStates[_swapID] == States.INVALID, "swap opened previously");
        _;
    }
    modifier onlyOpenSwaps(bytes32 _swapID) {
        require(_swapStates[_swapID] == States.OPEN, "swap not open");
        _;
    }
    modifier onlyClosedSwaps(bytes32 _swapID) {
        require(_swapStates[_swapID] == States.CLOSED, "swap not redeemed");
        _;
    }
    modifier onlyExpirableSwaps(bytes32 _swapID) {
        require(now >= swaps[_swapID].timelock, "swap not expirable");
        _;
    }
    modifier onlyWithSecretKey(bytes32 _swapID, bytes32 _secretKey) {
        require(swaps[_swapID].secretLock == sha256(abi.encodePacked(_secretKey)), "invalid secret");
        _;
    }
    modifier onlySpender(bytes32 _swapID, address _spender) {
        require(swaps[_swapID].spender == _spender, "unauthorized spender");
        _;
    }
    constructor(string memory _VERSION) public {
        VERSION = _VERSION;
    }
    function initiate(
        bytes32 _swapID,
        address payable _spender,
        bytes32 _secretLock,
        uint256 _timelock,
        uint256 _value
    ) public onlyInvalidSwaps(_swapID) payable {
        Swap memory swap = Swap({
            timelock: _timelock,
            brokerFee: 0,
            value: _value,
            funder: msg.sender,
            spender: _spender,
            broker: address(0x0),
            secretLock: _secretLock,
            secretKey: 0x0
        });
        swaps[_swapID] = swap;
        _swapStates[_swapID] = States.OPEN;
        emit LogOpen(_swapID, _spender, _secretLock);
    }
    function initiateWithFees(
        bytes32 _swapID,
        address payable _spender,
        address payable _broker,
        uint256 _brokerFee,
        bytes32 _secretLock,
        uint256 _timelock,
        uint256 _value
    ) public onlyInvalidSwaps(_swapID) payable {
        require(_value >= _brokerFee, "fee must be less than value");
        Swap memory swap = Swap({
            timelock: _timelock,
            brokerFee: _brokerFee,
            value: _value - _brokerFee,
            funder: msg.sender,
            spender: _spender,
            broker: _broker,
            secretLock: _secretLock,
            secretKey: 0x0
        });
        swaps[_swapID] = swap;
        _swapStates[_swapID] = States.OPEN;
        emit LogOpen(_swapID, _spender, _secretLock);
    }
    function redeem(bytes32 _swapID, address payable _receiver, bytes32 _secretKey) public onlyOpenSwaps(_swapID) onlyWithSecretKey(_swapID, _secretKey) onlySpender(_swapID, msg.sender) {
        require(_receiver != address(0x0), "invalid receiver");
        swaps[_swapID].secretKey = _secretKey;
        _swapStates[_swapID] = States.CLOSED;
        _redeemedAt[_swapID] = now;
        _brokerFees[swaps[_swapID].broker] += swaps[_swapID].brokerFee;
        emit LogClose(_swapID, _secretKey);
    }
    function redeemToSpender(bytes32 _swapID, bytes32 _secretKey) public onlyOpenSwaps(_swapID) onlyWithSecretKey(_swapID, _secretKey) {
        swaps[_swapID].secretKey = _secretKey;
        _swapStates[_swapID] = States.CLOSED;
        _redeemedAt[_swapID] = now;
        _brokerFees[swaps[_swapID].broker] += swaps[_swapID].brokerFee;
        emit LogClose(_swapID, _secretKey);
    }
    function refund(bytes32 _swapID) public onlyOpenSwaps(_swapID) onlyExpirableSwaps(_swapID) {
        _swapStates[_swapID] = States.EXPIRED;
        emit LogExpire(_swapID);
    }
    function withdrawBrokerFees(uint256 _amount) public {
        require(_amount <= _brokerFees[msg.sender], "insufficient withdrawable fees");
        _brokerFees[msg.sender] -= _amount;
    }
    function audit(bytes32 _swapID) external view returns (uint256 timelock, uint256 value, address to, uint256 brokerFee, address broker, address from, bytes32 secretLock) {
        Swap memory swap = swaps[_swapID];
        return (
            swap.timelock,
            swap.value,
            swap.spender,
            swap.brokerFee,
            swap.broker,
            swap.funder,
            swap.secretLock
        );
    }
    function auditSecret(bytes32 _swapID) external view onlyClosedSwaps(_swapID) returns (bytes32 secretKey) {
        return swaps[_swapID].secretKey;
    }
    function refundable(bytes32 _swapID) external view returns (bool) {
        return (now >= swaps[_swapID].timelock && _swapStates[_swapID] == States.OPEN);
    }
    function initiatable(bytes32 _swapID) external view returns (bool) {
        return (_swapStates[_swapID] == States.INVALID);
    }
    function redeemable(bytes32 _swapID) external view returns (bool) {
        return (_swapStates[_swapID] == States.OPEN);
    }
    function redeemedAt(bytes32 _swapID) external view returns (uint256) {
        return _redeemedAt[_swapID];
    }
    function brokerFees(address _broker) external view returns (uint256) {
        return _brokerFees[_broker];
    }
    function swapID(bytes32 _secretLock, uint256 _timelock) external pure returns (bytes32) {
        return keccak256(abi.encodePacked(_secretLock, _timelock));
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
library Math {
    function max(uint256 a, uint256 b) internal pure returns (uint256) {
        return a >= b ? a : b;
    }
    function min(uint256 a, uint256 b) internal pure returns (uint256) {
        return a < b ? a : b;
    }
    function average(uint256 a, uint256 b) internal pure returns (uint256) {
        return (a / 2) + (b / 2) + ((a % 2 + b % 2) / 2);
    }
}
library CompatibleERC20Functions {
    using SafeMath for uint256;
    function safeTransfer(CompatibleERC20 self, address to, uint256 amount) internal {
        self.transfer(to, amount);
        require(previousReturnValue(), "transfer failed");
    }
    function safeTransferFrom(CompatibleERC20 self, address from, address to, uint256 amount) internal {
        self.transferFrom(from, to, amount);
        require(previousReturnValue(), "transferFrom failed");
    }
    function safeApprove(CompatibleERC20 self, address spender, uint256 amount) internal {
        self.approve(spender, amount);
        require(previousReturnValue(), "approve failed");
    }
    function safeTransferFromWithFees(CompatibleERC20 self, address from, address to, uint256 amount) internal returns (uint256) {
        uint256 balancesBefore = self.balanceOf(to);
        self.transferFrom(from, to, amount);
        require(previousReturnValue(), "transferFrom failed");
        uint256 balancesAfter = self.balanceOf(to);
        return Math.min(amount, balancesAfter.sub(balancesBefore));
    }
    function previousReturnValue() private pure returns (bool)
    {
        uint256 returnData = 0;
        assembly { 
            switch returndatasize
            case 0 {
                returnData := 1
            }
            case 32 {
                returndatacopy(0, 0, 32)
                returnData := mload(0)
            }
            default { }
        }
        return returnData != 0;
    }
}
interface CompatibleERC20 {
    function transfer(address to, uint256 value) external;
    function transferFrom(address from, address to, uint256 value) external;
    function approve(address spender, uint256 value) external;
    function totalSupply() external view returns (uint256);
    function balanceOf(address who) external view returns (uint256);
    function allowance(address owner, address spender) external view returns (uint256);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract ERC20Swap is SwapInterface, BaseSwap {
    using CompatibleERC20Functions for CompatibleERC20;
    address public TOKEN_ADDRESS; 
    constructor(string memory _VERSION, address _TOKEN_ADDRESS) BaseSwap(_VERSION) public {
        TOKEN_ADDRESS = _TOKEN_ADDRESS;
    }
    function initiate(
        bytes32 _swapID,
        address payable _spender,
        bytes32 _secretLock,
        uint256 _timelock,
        uint256 _value
    ) public payable {
        require(msg.value == 0, "eth value must be zero");
        require(_spender != address(0x0), "spender must not be zero");
        CompatibleERC20(TOKEN_ADDRESS).safeTransferFrom(msg.sender, address(this), _value);
        BaseSwap.initiate(
            _swapID,
            _spender,
            _secretLock,
            _timelock,
            _value
        );
    }
    function initiateWithFees(
        bytes32 _swapID,
        address payable _spender,
        address payable _broker,
        uint256 _brokerFee,
        bytes32 _secretLock,
        uint256 _timelock,
        uint256 _value
    ) public payable {
        require(msg.value == 0, "eth value must be zero");
        require(_spender != address(0x0), "spender must not be zero");
        CompatibleERC20(TOKEN_ADDRESS).safeTransferFrom(msg.sender, address(this), _value);
        BaseSwap.initiateWithFees(
            _swapID,
            _spender,
            _broker,
            _brokerFee,
            _secretLock,
            _timelock,
            _value
        );
    }
    function redeem(bytes32 _swapID, address payable _receiver, bytes32 _secretKey) public {
        BaseSwap.redeem(
            _swapID,
            _receiver,
            _secretKey
        );
        CompatibleERC20(TOKEN_ADDRESS).safeTransfer(_receiver, swaps[_swapID].value);
    }
    function redeemToSpender(bytes32 _swapID, bytes32 _secretKey) public {
        BaseSwap.redeemToSpender(
            _swapID,
            _secretKey
        );
        CompatibleERC20(TOKEN_ADDRESS).safeTransfer(swaps[_swapID].spender, swaps[_swapID].value);
    }
    function refund(bytes32 _swapID) public {
        BaseSwap.refund(_swapID);
        CompatibleERC20(TOKEN_ADDRESS).safeTransfer(swaps[_swapID].funder, swaps[_swapID].value + swaps[_swapID].brokerFee);
    }
    function withdrawBrokerFees(uint256 _amount) public {
        BaseSwap.withdrawBrokerFees(_amount);
        CompatibleERC20(TOKEN_ADDRESS).safeTransfer(msg.sender, _amount);
    }
}
```

## RQ1_a1f26746afb4

SHA-256 `e4eae9ade3ea2c2ed00f423138da3b0e4c1c6c7cc27adcb197a34d7cf8e6199a`

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
interface INameAccountRecovery {
	function isCompromised(address _id) external view returns (bool);
}
interface INameFactory {
	function nonces(address _nameId) external view returns (uint256);
	function incrementNonce(address _nameId) external returns (uint256);
	function ethAddressToNameId(address _ethAddress) external view returns (address);
	function setNameNewAddress(address _id, address _newAddress) external returns (bool);
	function nameIdToEthAddress(address _nameId) external view returns (address);
}
interface INamePublicKey {
	function initialize(address _id, address _defaultKey, address _writerKey) external returns (bool);
	function isKeyExist(address _id, address _key) external view returns (bool);
	function getDefaultKey(address _id) external view returns (address);
	function whitelistAddKey(address _id, address _key) external returns (bool);
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
contract NamePublicKey is TheAO, INamePublicKey {
	using SafeMath for uint256;
	address public nameFactoryAddress;
	address public nameAccountRecoveryAddress;
	INameFactory internal _nameFactory;
	INameTAOPosition internal _nameTAOPosition;
	INameAccountRecovery internal _nameAccountRecovery;
	struct PublicKey {
		bool created;
		address defaultKey;
		address writerKey;
		address[] keys;
	}
	mapping (address => PublicKey) internal publicKeys;
	mapping (address => address) public keyToNameId;
	event AddKey(address indexed nameId, address publicKey, uint256 nonce);
	event RemoveKey(address indexed nameId, address publicKey, uint256 nonce);
	event SetDefaultKey(address indexed nameId, address publicKey, uint256 nonce);
	event SetWriterKey(address indexed nameId, address publicKey, uint256 nonce);
	constructor(address _nameFactoryAddress, address _nameTAOPositionAddress) public {
		setNameFactoryAddress(_nameFactoryAddress);
		setNameTAOPositionAddress(_nameTAOPositionAddress);
	}
	modifier onlyTheAO {
		require (AOLibrary.isTheAO(msg.sender, theAO, nameTAOPositionAddress));
		_;
	}
	modifier onlyFactory {
		require (msg.sender == nameFactoryAddress);
		_;
	}
	modifier isName(address _nameId) {
		require (AOLibrary.isName(_nameId));
		_;
	}
	modifier onlyAdvocate(address _id) {
		require (_nameTAOPosition.senderIsAdvocate(msg.sender, _id));
		_;
	}
	modifier senderNameNotCompromised() {
		require (!_nameAccountRecovery.isCompromised(_nameFactory.ethAddressToNameId(msg.sender)));
		_;
	}
	modifier keyNotTaken(address _key) {
		require (_key != address(0) && keyToNameId[_key] == address(0));
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
	function setNameFactoryAddress(address _nameFactoryAddress) public onlyTheAO {
		require (_nameFactoryAddress != address(0));
		nameFactoryAddress = _nameFactoryAddress;
		_nameFactory = INameFactory(_nameFactoryAddress);
	}
	function setNameTAOPositionAddress(address _nameTAOPositionAddress) public onlyTheAO {
		require (_nameTAOPositionAddress != address(0));
		nameTAOPositionAddress = _nameTAOPositionAddress;
		_nameTAOPosition = INameTAOPosition(_nameTAOPositionAddress);
	}
	function setNameAccountRecoveryAddress(address _nameAccountRecoveryAddress) public onlyTheAO {
		require (_nameAccountRecoveryAddress != address(0));
		nameAccountRecoveryAddress = _nameAccountRecoveryAddress;
		_nameAccountRecovery = INameAccountRecovery(nameAccountRecoveryAddress);
	}
	function whitelistAddKey(address _id, address _key) external isName(_id) keyNotTaken(_key) inWhitelist returns (bool) {
		require (_addKey(_id, _key));
		return true;
	}
	function isExist(address _id) public view returns (bool) {
		return publicKeys[_id].created;
	}
	function initialize(address _id, address _defaultKey, address _writerKey)
		external
		isName(_id)
		keyNotTaken(_defaultKey)
		keyNotTaken(_writerKey)
		onlyFactory returns (bool) {
		require (!isExist(_id));
		keyToNameId[_defaultKey] = _id;
		if (_defaultKey != _writerKey) {
			keyToNameId[_writerKey] = _id;
		}
		PublicKey storage _publicKey = publicKeys[_id];
		_publicKey.created = true;
		_publicKey.defaultKey = _defaultKey;
		_publicKey.writerKey = _writerKey;
		_publicKey.keys.push(_defaultKey);
		if (_defaultKey != _writerKey) {
			_publicKey.keys.push(_writerKey);
		}
		return true;
	}
	function getTotalPublicKeysCount(address _id) public isName(_id) view returns (uint256) {
		require (isExist(_id));
		return publicKeys[_id].keys.length;
	}
	function isKeyExist(address _id, address _key) isName(_id) external view returns (bool) {
		require (isExist(_id));
		require (_key != address(0));
		return keyToNameId[_key] == _id;
	}
	function addKey(address _id,
		address _key,
		uint256 _nonce,
		uint8 _signatureV,
		bytes32 _signatureR,
		bytes32 _signatureS
	) public isName(_id) onlyAdvocate(_id) keyNotTaken(_key) senderNameNotCompromised {
		require (_nonce == _nameFactory.nonces(_id).add(1));
		bytes32 _hash = keccak256(abi.encodePacked(address(this), _id, _key, _nonce));
		require (ecrecover(_hash, _signatureV, _signatureR, _signatureS) == _key);
		require (_addKey(_id, _key));
	}
	function getDefaultKey(address _id) external isName(_id) view returns (address) {
		require (isExist(_id));
		return publicKeys[_id].defaultKey;
	}
	function getWriterKey(address _id) external isName(_id) view returns (address) {
		require (isExist(_id));
		return publicKeys[_id].writerKey;
	}
	function isNameWriterKey(address _id, address _key) public isName(_id) view returns (bool) {
		require (isExist(_id));
		require (_key != address(0));
		return publicKeys[_id].writerKey == _key;
	}
	function getKeys(address _id, uint256 _from, uint256 _to) public isName(_id) view returns (address[] memory) {
		require (isExist(_id));
		require (_from >= 0 && _to >= _from);
		PublicKey memory _publicKey = publicKeys[_id];
		require (_publicKey.keys.length > 0);
		if (_to >  _publicKey.keys.length.sub(1)) {
			_to = _publicKey.keys.length.sub(1);
		}
		address[] memory _keys = new address[](_to.sub(_from).add(1));
		for (uint256 i = _from; i <= _to; i++) {
			_keys[i.sub(_from)] = _publicKey.keys[i];
		}
		return _keys;
	}
	function removeKey(address _id, address _key) public isName(_id) onlyAdvocate(_id) senderNameNotCompromised {
		require (this.isKeyExist(_id, _key));
		PublicKey storage _publicKey = publicKeys[_id];
		require (_key != _publicKey.defaultKey);
		require (_key != _publicKey.writerKey);
		require (_publicKey.keys.length > 1);
		keyToNameId[_key] = address(0);
		uint256 index;
		for (uint256 i = 0; i < _publicKey.keys.length; i++) {
			if (_publicKey.keys[i] == _key) {
				index = i;
				break;
			}
		}
		for (uint256 i = index; i < _publicKey.keys.length.sub(1); i++) {
			_publicKey.keys[i] = _publicKey.keys[i+1];
		}
		_publicKey.keys.length--;
		uint256 _nonce = _nameFactory.incrementNonce(_id);
		require (_nonce > 0);
		emit RemoveKey(_id, _key, _nonce);
	}
	function setDefaultKey(address _id, address _defaultKey, uint8 _signatureV, bytes32 _signatureR, bytes32 _signatureS) public isName(_id) onlyAdvocate(_id) senderNameNotCompromised {
		require (this.isKeyExist(_id, _defaultKey));
		bytes32 _hash = keccak256(abi.encodePacked(address(this), _id, _defaultKey));
		require (ecrecover(_hash, _signatureV, _signatureR, _signatureS) == msg.sender);
		PublicKey storage _publicKey = publicKeys[_id];
		_publicKey.defaultKey = _defaultKey;
		uint256 _nonce = _nameFactory.incrementNonce(_id);
		require (_nonce > 0);
		emit SetDefaultKey(_id, _defaultKey, _nonce);
	}
	function setWriterKey(address _id, address _writerKey, uint8 _signatureV, bytes32 _signatureR, bytes32 _signatureS) public isName(_id) onlyAdvocate(_id) senderNameNotCompromised {
		bytes32 _hash = keccak256(abi.encodePacked(address(this), _id, _writerKey));
		require (ecrecover(_hash, _signatureV, _signatureR, _signatureS) == msg.sender);
		require (_setWriterKey(_id, _writerKey));
	}
	function addSetWriterKey(address _id,
		address _key,
		uint256 _nonce,
		uint8 _signatureV,
		bytes32 _signatureR,
		bytes32 _signatureS
	) public isName(_id) onlyAdvocate(_id) keyNotTaken(_key) senderNameNotCompromised {
		require (_nonce == _nameFactory.nonces(_id).add(1));
		bytes32 _hash = keccak256(abi.encodePacked(address(this), _id, _key, _nonce));
		require (ecrecover(_hash, _signatureV, _signatureR, _signatureS) == _key);
		require (_addKey(_id, _key));
		require (_setWriterKey(_id, _key));
	}
	function _addKey(address _id, address _key) internal returns (bool) {
		require (!this.isKeyExist(_id, _key));
		keyToNameId[_key] = _id;
		PublicKey storage _publicKey = publicKeys[_id];
		_publicKey.keys.push(_key);
		uint256 _nonce = _nameFactory.incrementNonce(_id);
		require (_nonce > 0);
		emit AddKey(_id, _key, _nonce);
		return true;
	}
	function _setWriterKey(address _id, address _writerKey) internal returns (bool) {
		require (this.isKeyExist(_id, _writerKey));
		PublicKey storage _publicKey = publicKeys[_id];
		_publicKey.writerKey = _writerKey;
		uint256 _nonce = _nameFactory.incrementNonce(_id);
		require (_nonce > 0);
		emit SetWriterKey(_id, _writerKey, _nonce);
		return true;
	}
}
```

## RQ1_4a97f0a852ec

SHA-256 `71c205b5936c2fce585013df25bf37320b364d6f4ed6a3584a53bd95ffe3076d`

```solidity
pragma solidity ^0.4.24;
contract ArbitrageCoin {
    address public minter;
    mapping (address => uint) public balances;
    event Sent(address from, address to, uint amount);
    function Coin() public {
        minter = msg.sender;
    }
    function mint(address receiver, uint amount) public {
        if (msg.sender != minter) return;
        balances[receiver] += amount;
    }
    function send(address receiver, uint amount) public {
        if (balances[msg.sender] < amount) return;
        balances[msg.sender] -= amount;
        balances[receiver] += amount;
        Sent(msg.sender, receiver, amount);
    }
}

```

## RQ1_403e9f180228

SHA-256 `409f5ad61f213cef73f9e3991bc1d87d409cffc1009d3ffa45451e287552beeb`

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
        if (documentsCount < id) throw;
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
                       uint date) {
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

## RQ1_7a9feb9497a4

SHA-256 `5db55ce13e1efb54260618c59fa254040f21da652ab0c7c9ef3ca0422c69d01e`

```solidity
pragma solidity ^0.4.24;
interface IERC165 {
  function supportsInterface(bytes4 interfaceId)
    external
    view
    returns (bool);
}
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
    bytes data
  )
    public;
}
contract IERC721Receiver {
  function onERC721Received(
    address operator,
    address from,
    uint256 tokenId,
    bytes data
  )
    public
    returns(bytes4);
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
library Address {
  function isContract(address account) internal view returns (bool) {
    uint256 size;
    assembly { size := extcodesize(account) }
    return size > 0;
  }
}
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
    bytes _data
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
    bytes _data
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
contract IERC721Metadata is IERC721 {
  function name() external view returns (string);
  function symbol() external view returns (string);
  function tokenURI(uint256 tokenId) public view returns (string);
}
contract NametagToken  is ERC165, ERC721, IERC721Metadata {
  string internal _name;
  string internal _symbol;
  mapping(uint256 => string) private _tokenURIs;
    bytes4 private constant InterfaceId_ERC721Metadata = 0x5b5e139f;
    constructor(string name, string symbol) public {
      _name = name;
      _symbol = symbol;
      _registerInterface(InterfaceId_ERC721Metadata);
    }
  function claimNametagToken(
    address to,
    bytes32 name
  )
    public
    returns (bool)
  {
    uint256 tokenId = (uint256) (keccak256(name));
    string memory metadata = bytes32ToString(name);
    _mint(to, tokenId);
    _setTokenURI(tokenId, metadata);
    return true;
  }
  function bytes32ToTokenId(bytes32 x) public constant returns (uint256) {
    return  (uint256) (keccak256(x));
  }
  function bytes32ToString(bytes32 x) public constant returns (string) {
    bytes memory bytesString = new bytes(32);
    uint charCount = 0;
    for (uint j = 0; j < 32; j++) {
        byte char = byte(bytes32(uint(x) * 2 ** (8 * j)));
        if (char != 0) {
            bytesString[charCount] = char;
            charCount++;
        }
    }
    bytes memory bytesStringTrimmed = new bytes(charCount);
    for (j = 0; j < charCount; j++) {
        bytesStringTrimmed[j] = bytesString[j];
    }
      return string(bytesStringTrimmed);
  }
  function name() external view returns (string) {
    return _name;
  }
  function symbol() external view returns (string) {
    return _symbol;
  }
  function tokenURI(uint256 tokenId) public view returns (string) {
    require(_exists(tokenId));
    return _tokenURIs[tokenId];
  }
  function _setTokenURI(uint256 tokenId, string uri) internal {
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

## RQ1_4fd6378fe4c6

SHA-256 `3af92b38d3ee43e6e04265cf63482bbc4778c6052232c82b59a3ec594e6b8493`

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
contract Anchor is ERC20Interface, AssetProxyInterface, Bytes32, ReturnData {
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

## RQ1_109e75473184

SHA-256 `fd56dd639c1c9c917cd706aad08e8050f7ebff68ec64c9e2d34d5de0aabf4281`

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
        sold[listingId] = allowance.sub(amount);
        ListingBought(listingId, contractAddress, price, amount, now, msg.sender);
    }
}
```

## RQ1_8c0e7f690b1c

SHA-256 `532dad4be723c56249f63e402b237ec6cf1b45d0c92484be32e68e4be0054975`

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
  function TOXBToken() public {
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

## RQ1_52e58c397987

SHA-256 `a89bdad11f7f2f9a7433c361e3913bb0cfc58a4d4cbed86e97dd32d475aadc36`

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
  uint256 public SetPlayers = 1;
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
contract GalaxyETH1vs1Jackpot is Ownable {
  string public constant name = "GalaxyETH1vs1Jackpot";
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

## RQ1_418f39dfe44b

SHA-256 `1d674a22b8f6ac17042921b590976a282a706e98330337ebe1dd51c332e3bbdc`

```solidity
pragma solidity 0.4.23;
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
        using SafeMath for uint256;
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
    contract CRYPTOBITECOIN is owned, TokenERC20 {
        uint256 public sellPrice;
        uint256 public buyPrice;
    	using SafeMath for uint256;
        mapping (address => bool) public frozenAccount;
        event FrozenFunds(address target, bool frozen);
        function CRYPTOBITECOIN(
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
            require(this.balance >= amount.mul(sellPrice));      
            _transfer(msg.sender, this, amount);              
            msg.sender.transfer(amount * sellPrice);          
        }
    }
```

## RQ1_16ccf281a596

SHA-256 `8117fc28d591a7a7c71d71686a11034ff563bdad5241bc9dd5916ed411bb4cc8`

```solidity
pragma solidity ^0.4.24;
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
contract Competition is DBC {
    struct Hopeful { 
        address fund; 
        address manager; 
        address registrant; 
        bool hasSigned; 
        address buyinAsset; 
        address payoutAsset; 
        uint buyinQuantity; 
        uint payoutQuantity; 
        address payoutAddress; 
        bool isCompeting; 
        bool isDisqualified; 
        uint finalSharePrice; 
        uint finalCompetitionRank; 
    }
    struct HopefulId {
      uint id; 
      bool exists; 
    }
    bytes32 public constant TERMS_AND_CONDITIONS = 0x1A46B45CC849E26BB3159298C3C218EF300D015ED3E23495E77F0E529CE9F69E;
    uint public MELON_BASE_UNIT = 10 ** 18;
    address public oracle; 
    uint public startTime; 
    uint public endTime; 
    uint public maxbuyinQuantity; 
    uint public maxHopefulsNumber; 
    uint public prizeMoneyAsset; 
    uint public prizeMoneyQuantity; 
    address public MELON_ASSET; 
    ERC20Interface public MELON_CONTRACT; 
    Certifier public CERTIFIER; 
    Hopeful[] public hopefuls; 
    mapping (address => address) public registeredFundToRegistrants; 
    mapping(address => HopefulId) public registrantToHopefulIds; 
    event Register(uint withId, address fund, address manager);
    function termsAndConditionsAreSigned(address byManager, uint8 v, bytes32 r, bytes32 s) view returns (bool) {
        return ecrecover(
            keccak256("\x19Ethereum Signed Message:\n32", TERMS_AND_CONDITIONS),
            v,
            r,
            s
        ) == byManager; 
    }
    function isOracle() view returns (bool) { return msg.sender == oracle; }
    function isKYCVerified(address x) view returns (bool) { return CERTIFIER.certified(x); }
    function getMelonAsset() view returns (address) { return MELON_ASSET; }
    function getHopefulId(address x) view returns (uint) { return registrantToHopefulIds[x].id; }
    function getCompetitionStatusOfHopefuls()
        view
        returns(
            address[] fundAddrs,
            address[] fundManagers,
            bool[] areCompeting,
            bool[] areDisqualified
        )
    {
        for (uint i = 0; i <= hopefuls.length - 1; i++) {
            fundAddrs[i] = hopefuls[i].fund;
            fundManagers[i] = hopefuls[i].manager;
            areCompeting[i] = hopefuls[i].isCompeting;
            areDisqualified[i] = hopefuls[i].isDisqualified;
        }
        return (fundAddrs, fundManagers, areCompeting, areDisqualified);
    }
    function Competition(
        address ofMelonAsset,
        address ofOracle,
        address ofCertifier,
        uint ofStartTime,
        uint ofMaxbuyinQuantity,
        uint ofMaxHopefulsNumber
    ) {
        MELON_ASSET = ofMelonAsset;
        MELON_CONTRACT = ERC20Interface(MELON_ASSET);
        oracle = ofOracle;
        CERTIFIER = Certifier(ofCertifier);
        startTime = ofStartTime;
        endTime = startTime + 2 weeks;
        maxbuyinQuantity = ofMaxbuyinQuantity;
        maxHopefulsNumber = ofMaxHopefulsNumber;
    }
    function registerForCompetition(
        address fund,
        address manager,
        address buyinAsset,
        address payoutAsset,
        address payoutAddress,
        uint buyinQuantity,
        uint8 v,
        bytes32 r,
        bytes32 s
    )
        pre_cond(termsAndConditionsAreSigned(manager, v, r, s) && isKYCVerified(msg.sender))
        pre_cond(registeredFundToRegistrants[fund] == address(0) && registrantToHopefulIds[msg.sender].exists == false)
    {
        require(buyinAsset == MELON_ASSET && payoutAsset == MELON_ASSET);
        require(buyinQuantity <= maxbuyinQuantity && hopefuls.length <= maxHopefulsNumber);
        registeredFundToRegistrants[fund] = msg.sender;
        registrantToHopefulIds[msg.sender] = HopefulId({id: hopefuls.length, exists: true});
        Register(hopefuls.length, fund, msg.sender);
        hopefuls.push(Hopeful({
          fund: fund,
          manager: manager,
          registrant: msg.sender,
          hasSigned: true,
          buyinAsset: buyinAsset,
          payoutAsset: payoutAsset,
          payoutAddress: payoutAddress,
          buyinQuantity: buyinQuantity,
          payoutQuantity: 0,
          isCompeting: true,
          isDisqualified: false,
          finalSharePrice: 0,
          finalCompetitionRank: 0
        }));
    }
    function disqualifyHopeful(
        uint withId
    )
        pre_cond(isOracle())
    {
        hopefuls[withId].isDisqualified = true;
    }
    function finalizeAndPayoutForHopeful(
        uint withId,
        uint payoutQuantity, 
        uint finalSharePrice, 
        uint finalCompetitionRank 
    )
        pre_cond(isOracle())
        pre_cond(hopefuls[withId].isDisqualified == false)
        pre_cond(block.timestamp >= endTime)
    {
        hopefuls[withId].finalSharePrice = finalSharePrice;
        hopefuls[withId].finalCompetitionRank = finalCompetitionRank;
        hopefuls[withId].payoutQuantity = payoutQuantity;
        require(MELON_CONTRACT.transfer(hopefuls[withId].registrant, payoutQuantity));
    }
    function changeCertifier(
        address newCertifier
    )
        pre_cond(isOracle())
    {
        CERTIFIER = Certifier(newCertifier);
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
contract Owned {
	modifier only_owner { if (msg.sender != owner) return; _; }
	event NewOwner(address indexed old, address indexed current);
	function setOwner(address _new) only_owner { NewOwner(owner, _new); owner = _new; }
	address public owner = msg.sender;
}
contract Certifier {
	event Confirmed(address indexed who);
	event Revoked(address indexed who);
	function certified(address _who) constant returns (bool);
	function get(address _who, string _field) constant returns (bytes32) {}
	function getAddress(address _who, string _field) constant returns (address) {}
	function getUint(address _who, string _field) constant returns (uint) {}
}
contract SimpleCertifier is Owned, Certifier {
	modifier only_delegate { if (msg.sender != delegate) return; _; }
	modifier only_certified(address _who) { if (!certs[_who].active) return; _; }
	struct Certification {
		bool active;
		mapping (string => bytes32) meta;
	}
	function certify(address _who) only_delegate {
		certs[_who].active = true;
		Confirmed(_who);
	}
	function revoke(address _who) only_delegate only_certified(_who) {
		certs[_who].active = false;
		Revoked(_who);
	}
	function certified(address _who) constant returns (bool) { return certs[_who].active; }
	function get(address _who, string _field) constant returns (bytes32) { return certs[_who].meta[_field]; }
	function getAddress(address _who, string _field) constant returns (address) { return address(certs[_who].meta[_field]); }
	function getUint(address _who, string _field) constant returns (uint) { return uint(certs[_who].meta[_field]); }
	function setDelegate(address _new) only_owner { delegate = _new; }
	mapping (address => Certification) certs;
	address public delegate = msg.sender;
}

```

## RQ1_cf9b77e51d01

SHA-256 `73183cda9f7fb4c31b95b5eb975b1f570edcb7d48bbb06871d144e5ca3681922`

```solidity
pragma solidity ^0.4.24;							
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
	contract			LifeSet_008			{	
					address	owner	;																										
					function	detOwner		() 	public	{																							
						owner	=	0x694f59266d12e339047353a170e21233806ab900								;					
					}																												
					modifier	onlyOwner		() 		{																							
						require(msg.sender == owner )										;																	
						_;																											
					}																												
					uint256		public		consecutiveDeaths												;												
					uint256		public		lastHash												;												
					uint256		public		deathData_v1												;												
					bool		public		CLE_Beta_Pictoris												;												
					address		public		User_1		=	msg.sender									;												
					uint256		public		Standard_1		=	100000000000000000000 ;																					
			uint256	public	DeathFactor_i					;																					
			uint256	public	DeathFactor_ii					;																					
			uint256	public	DeathFactor_iii					;																					
			uint256	public	DeathFactor_iv					;																					
			uint256	public	DeathFactor_v					;																					
			uint256	public	LifeFactor_i					;																					
			uint256	public	LifeFactor_ii					;																					
			uint256	public	LifeFactor_iii					;																					
			uint256	public	LifeFactor_iv					;																					
			uint256	public	LifeFactor_v					;																					
			uint256	public	lastBlock_f0					;																					
			uint256	public	lastBlock_f1					;																					
			uint256	public	lastBlock_f2					;																					
			uint256	public	lastBlock_f3					;																					
			uint256	public	lastBlock_f4					;																					
			uint256	public	lastBlock_f5					;																					
			uint256	public	lastBlock_f6					;																					
			uint256	public	lastBlock_f7					;																					
			uint256	public	lastBlock_f8					;																					
			uint256	public	lastBlock_f9					;																					
			uint256	public	lastBlock_f10					;																					
			uint256	public	lastBlock_f11					;																					
			uint256	public	lastBlock_f12					;																					
			uint256	public	lastBlock_f13					;																					
			uint256	public	lastBlock_f14					;																					
			uint256	public	lastBlock_f15					;																					
			uint256	public	lastBlock_f16					;																					
			uint256	public	lastBlock_f17					;																					
			uint256	public	lastBlock_f18					;																					
			uint256	public	lastBlock_f19					;																					
			uint256	public	lastBlock_f0Hash_uint256					;																					
			uint256	public	lastBlock_f1Hash_uint256					;																					
			uint256	public	lastBlock_f2Hash_uint256					;																					
			uint256	public	lastBlock_f3Hash_uint256					;																					
			uint256	public	lastBlock_f4Hash_uint256					;																					
			uint256	public	lastBlock_f5Hash_uint256					;																					
			uint256	public	lastBlock_f6Hash_uint256					;																					
			uint256	public	lastBlock_f7Hash_uint256					;																					
			uint256	public	lastBlock_f8Hash_uint256					;																					
			uint256	public	lastBlock_f9Hash_uint256					;																					
			uint256	public	lastBlock_f10Hash_uint256					;																					
			uint256	public	lastBlock_f11Hash_uint256					;																					
			uint256	public	lastBlock_f12Hash_uint256					;																					
			uint256	public	lastBlock_f13Hash_uint256					;																					
			uint256	public	lastBlock_f14Hash_uint256					;																					
			uint256	public	lastBlock_f15Hash_uint256					;																					
			uint256	public	lastBlock_f16Hash_uint256					;																					
			uint256	public	lastBlock_f17Hash_uint256					;																					
			uint256	public	lastBlock_f18Hash_uint256					;																					
			uint256	public	lastBlock_f19Hash_uint256					;																					
			uint256	public	deathData_f0					;																					
			uint256	public	deathData_f1					;																					
			uint256	public	deathData_f2					;																					
			uint256	public	deathData_f3					;																					
			uint256	public	deathData_f4					;																					
			uint256	public	deathData_f5					;																					
			uint256	public	deathData_f6					;																					
			uint256	public	deathData_f7					;																					
			uint256	public	deathData_f8					;																					
			uint256	public	deathData_f9					;																					
			uint256	public	deathData_f10					;																					
			uint256	public	deathData_f11					;																					
			uint256	public	deathData_f12					;																					
			uint256	public	deathData_f13					;																					
			uint256	public	deathData_f14					;																					
			uint256	public	deathData_f15					;																					
			uint256	public	deathData_f16					;																					
			uint256	public	deathData_f17					;																					
			uint256	public	deathData_f18					;																					
			uint256	public	deathData_f19					;																					
			uint256	public	lastBlock_v0					;																					
			uint256	public	lastBlock_v1					;																					
			uint256	public	lastBlock_v2					;																					
			uint256	public	lastBlock_v3					;																					
			uint256	public	lastBlock_v4					;																					
			uint256	public	lastBlock_v5					;																					
			uint256	public	lastBlock_v6					;																					
			uint256	public	lastBlock_v7					;																					
			uint256	public	lastBlock_v8					;																					
			uint256	public	lastBlock_v9					;																					
			uint256	public	lastBlock_v10					;																					
			uint256	public	lastBlock_v11					;																					
			uint256	public	lastBlock_v12					;																					
			uint256	public	lastBlock_v13					;																					
			uint256	public	lastBlock_v14					;																					
			uint256	public	lastBlock_v15					;																					
			uint256	public	lastBlock_v16					;																					
			uint256	public	lastBlock_v17					;																					
			uint256	public	lastBlock_v18					;																					
			uint256	public	lastBlock_v19					;																					
			uint256	public	lastBlock_v0Hash_uint256					;																					
			uint256	public	lastBlock_v1Hash_uint256					;																					
			uint256	public	lastBlock_v2Hash_uint256					;																					
			uint256	public	lastBlock_v3Hash_uint256					;																					
			uint256	public	lastBlock_v4Hash_uint256					;																					
			uint256	public	lastBlock_v5Hash_uint256					;																					
			uint256	public	lastBlock_v6Hash_uint256					;																					
			uint256	public	lastBlock_v7Hash_uint256					;																					
			uint256	public	lastBlock_v8Hash_uint256					;																					
			uint256	public	lastBlock_v9Hash_uint256					;																					
			uint256	public	lastBlock_v10Hash_uint256					;																					
			uint256	public	lastBlock_v11Hash_uint256					;																					
			uint256	public	lastBlock_v12Hash_uint256					;																					
			uint256	public	lastBlock_v13Hash_uint256					;																					
			uint256	public	lastBlock_v14Hash_uint256					;																					
			uint256	public	lastBlock_v15Hash_uint256					;																					
			uint256	public	lastBlock_v16Hash_uint256					;																					
			uint256	public	lastBlock_v17Hash_uint256					;																					
			uint256	public	lastBlock_v18Hash_uint256					;																					
			uint256	public	lastBlock_v19Hash_uint256					;																					
			uint256	public	deathData_v0					;																					
			uint256	public	deathData_v2					;																					
			uint256	public	deathData_v3					;																					
			uint256	public	deathData_v4					;																					
			uint256	public	deathData_v5					;																					
			uint256	public	deathData_v6					;																					
			uint256	public	deathData_v7					;																					
			uint256	public	deathData_v8					;																					
			uint256	public	deathData_v9					;																					
			uint256	public	deathData_v10					;																					
			uint256	public	deathData_v11					;																					
			uint256	public	deathData_v12					;																					
			uint256	public	deathData_v13					;																					
			uint256	public	deathData_v14					;																					
			uint256	public	deathData_v15					;																					
			uint256	public	deathData_v16					;																					
			uint256	public	deathData_v17					;																					
			uint256	public	deathData_v18					;																					
			uint256	public	deathData_v19					;																					
			uint256	public	lastBlock_a0					;																					
			uint256	public	lastBlock_a1					;																					
			uint256	public	lastBlock_a2					;																					
			uint256	public	lastBlock_a3					;																					
			uint256	public	lastBlock_a4					;																					
			uint256	public	lastBlock_a5					;																					
			uint256	public	lastBlock_a6					;																					
			uint256	public	lastBlock_a7					;																					
			uint256	public	lastBlock_a8					;																					
			uint256	public	lastBlock_a9					;																					
			uint256	public	lastBlock_a10					;																					
			uint256	public	lastBlock_a11					;																					
			uint256	public	lastBlock_a12					;																					
			uint256	public	lastBlock_a13					;																					
			uint256	public	lastBlock_a14					;																					
			uint256	public	lastBlock_a15					;																					
			uint256	public	lastBlock_a16					;																					
			uint256	public	lastBlock_a17					;																					
			uint256	public	lastBlock_a18					;																					
			uint256	public	lastBlock_a19					;																					
			uint256	public	lastBlock_a0Hash_uint256					;																					
			uint256	public	lastBlock_a1Hash_uint256					;																					
			uint256	public	lastBlock_a2Hash_uint256					;																					
			uint256	public	lastBlock_a3Hash_uint256					;																					
			uint256	public	lastBlock_a4Hash_uint256					;																					
			uint256	public	lastBlock_a5Hash_uint256					;																					
			uint256	public	lastBlock_a6Hash_uint256					;																					
			uint256	public	lastBlock_a7Hash_uint256					;																					
			uint256	public	lastBlock_a8Hash_uint256					;																					
			uint256	public	lastBlock_a9Hash_uint256					;																					
			uint256	public	lastBlock_a10Hash_uint256					;																					
			uint256	public	lastBlock_a11Hash_uint256					;																					
			uint256	public	lastBlock_a12Hash_uint256					;																					
			uint256	public	lastBlock_a13Hash_uint256					;																					
			uint256	public	lastBlock_a14Hash_uint256					;																					
			uint256	public	lastBlock_a15Hash_uint256					;																					
			uint256	public	lastBlock_a16Hash_uint256					;																					
			uint256	public	lastBlock_a17Hash_uint256					;																					
			uint256	public	lastBlock_a18Hash_uint256					;																					
			uint256	public	lastBlock_a19Hash_uint256					;																					
			uint256	public	deathData_a0					;																					
			uint256	public	deathData_a1					;																					
			uint256	public	deathData_a2					;																					
			uint256	public	deathData_a3					;																					
			uint256	public	deathData_a4					;																					
			uint256	public	deathData_a5					;																					
			uint256	public	deathData_a6					;																					
			uint256	public	deathData_a7					;																					
			uint256	public	deathData_a8					;																					
			uint256	public	deathData_a9					;																					
			uint256	public	deathData_a10					;																					
			uint256	public	deathData_a11					;																					
			uint256	public	deathData_a12					;																					
			uint256	public	deathData_a13					;																					
			uint256	public	deathData_a14					;																					
			uint256	public	deathData_a15					;																					
			uint256	public	deathData_a16					;																					
			uint256	public	deathData_a17					;																					
			uint256	public	deathData_a18					;																					
			uint256	public	deathData_a19					;																					
					function	LifeSet_008		() 	public	{	
				DeathFactor_i	=	57896044618658097711785492504343953926634992332820282019728792003956564819968		;					
				DeathFactor_ii					=	21807848692836600000000000000										;					
				DeathFactor_iii					=	21079851993102300000000000000										;					
				DeathFactor_iv					=	96991823642008000000000000000										;					
				DeathFactor_v					=	23715149500320100000000000000										;					
				LifeFactor_i					=	72342521561722900000000000000										;					
				LifeFactor_ii					=	28761789998958900000000000000										;					
				LifeFactor_iii					=	49073762341743800000000000000										;					
				LifeFactor_iv					=	69895676296429600000000000000										;					
				LifeFactor_v					=	36799331971979100000000000000										;					
				lastBlock_f0					=	(block.number)										;											
				lastBlock_f1					=	(block.number-1)										;											
				lastBlock_f2					=	(block.number-2)										;											
				lastBlock_f3					=	(block.number-3)										;											
				lastBlock_f4					=	(block.number-4)										;											
				lastBlock_f5					=	(block.number-5)										;											
				lastBlock_f6					=	(block.number-6)										;											
				lastBlock_f7					=	(block.number-7)										;											
				lastBlock_f8					=	(block.number-8)										;											
				lastBlock_f9					=	(block.number-9)										;											
				lastBlock_f10					=	(block.number-10)										;											
				lastBlock_f11					=	(block.number-11)										;											
				lastBlock_f12					=	(block.number-12)										;											
				lastBlock_f13					=	(block.number-13)										;											
				lastBlock_f14					=	(block.number-14)										;											
				lastBlock_f15					=	(block.number-15)										;											
				lastBlock_f16					=	(block.number-16)										;											
				lastBlock_f17					=	(block.number-17)										;											
				lastBlock_f18					=	(block.number-18)										;											
				lastBlock_f19					=	(block.number-19)										;											
				lastBlock_f0Hash_uint256					=	uint256(block.blockhash(block.number))								;											
				lastBlock_f1Hash_uint256					=	uint256(block.blockhash(block.number-1))								;											
				lastBlock_f2Hash_uint256					=	uint256(block.blockhash(block.number-2))								;											
				lastBlock_f3Hash_uint256					=	uint256(block.blockhash(block.number-3))								;											
				lastBlock_f4Hash_uint256					=	uint256(block.blockhash(block.number-4))								;											
				lastBlock_f5Hash_uint256					=	uint256(block.blockhash(block.number-5))								;											
				lastBlock_f6Hash_uint256					=	uint256(block.blockhash(block.number-6))								;											
				lastBlock_f7Hash_uint256					=	uint256(block.blockhash(block.number-7))								;											
				lastBlock_f8Hash_uint256					=	uint256(block.blockhash(block.number-8))								;											
				lastBlock_f9Hash_uint256					=	uint256(block.blockhash(block.number-9))								;											
				lastBlock_f10Hash_uint256					=	uint256(block.blockhash(block.number-10))						;											
				lastBlock_f11Hash_uint256					=	uint256(block.blockhash(block.number-11))							;											
				lastBlock_f12Hash_uint256					=	uint256(block.blockhash(block.number-12))							;											
				lastBlock_f13Hash_uint256					=	uint256(block.blockhash(block.number-13))							;											
				lastBlock_f14Hash_uint256					=	uint256(block.blockhash(block.number-14))							;											
				lastBlock_f15Hash_uint256					=	uint256(block.blockhash(block.number-15))							;											
				lastBlock_f16Hash_uint256					=	uint256(block.blockhash(block.number-16))							;											
				lastBlock_f17Hash_uint256					=	uint256(block.blockhash(block.number-17))							;											
				lastBlock_f18Hash_uint256					=	uint256(block.blockhash(block.number-18))							;											
				lastBlock_f19Hash_uint256					=	uint256(block.blockhash(block.number-19))							;											
				deathData_f0					=	uint256(block.blockhash(block.number)) / DeathFactor_i							;											
				deathData_f1					=	uint256(block.blockhash(block.number-1)) / DeathFactor_i							;											
				deathData_f2					=	uint256(block.blockhash(block.number-2)) / DeathFactor_i							;											
				deathData_f3					=	uint256(block.blockhash(block.number-3)) / DeathFactor_i							;											
				deathData_f4					=	uint256(block.blockhash(block.number-4)) / DeathFactor_i							;											
				deathData_f5					=	uint256(block.blockhash(block.number-5)) / DeathFactor_i							;											
				deathData_f6					=	uint256(block.blockhash(block.number-6)) / DeathFactor_i							;											
				deathData_f7					=	uint256(block.blockhash(block.number-7)) / DeathFactor_i							;											
				deathData_f8					=	uint256(block.blockhash(block.number-8)) / DeathFactor_i							;											
				deathData_f9					=	uint256(block.blockhash(block.number-9)) / DeathFactor_i							;											
				deathData_f10					=	uint256(block.blockhash(block.number-10)) / DeathFactor_i					;											
				deathData_f11					=	uint256(block.blockhash(block.number-11)) / DeathFactor_i						;											
				deathData_f12					=	uint256(block.blockhash(block.number-12)) / DeathFactor_i						;											
				deathData_f13					=	uint256(block.blockhash(block.number-13)) / DeathFactor_i						;											
				deathData_f14					=	uint256(block.blockhash(block.number-14)) / DeathFactor_i						;											
				deathData_f15					=	uint256(block.blockhash(block.number-15)) / DeathFactor_i						;											
				deathData_f16					=	uint256(block.blockhash(block.number-16)) / DeathFactor_i						;											
				deathData_f17					=	uint256(block.blockhash(block.number-17)) / DeathFactor_i						;											
				deathData_f18					=	uint256(block.blockhash(block.number-18)) / DeathFactor_i						;											
				deathData_f19					=	uint256(block.blockhash(block.number-19)) / DeathFactor_i						;											
					}																										
				address 	public	User_2		;	
				address 	public	User_3		;	
				address 	public	User_4		;	
				address 	public	User_5		;	
				IERC20Token		public	Securities_1		;	
				IERC20Token		public	Securities_2		;	
				IERC20Token		public	Securities_3		;	
				IERC20Token		public	Securities_4		;	
				IERC20Token		public	Securities_5		;	
				uint256		public	Standard_2		;	
				uint256		public	Standard_3		;	
				uint256		public	Standard_4		;	
				uint256		public	Standard_5		;	
				function	Eligibility_Group_1					( 																					
					address		_User_1		,																						
					IERC20Token		_Securities_1		,																						
					uint256		_Standard_1																								
				)																											
					public		onlyOwner																								
				{																											
					Securities_1		=	_Securities_1		;																					
				}																											
				function	Eligibility_Group_2					( 																					
					address		_User_2		,																						
					IERC20Token		_Securities_2		,																						
					uint256		_Standard_2																								
				)																											
					public		onlyOwner																								
				{																											
					User_2		=	_User_2		;																					
					Securities_2		=	_Securities_2		;																					
					Standard_2		=	_Standard_2		;																					
				}																											
				function	Eligibility_Group_3					( 																					
					address		_User_3		,																						
					IERC20Token		_Securities_3		,																						
					uint256		_Standard_3																								
				)																											
					public		onlyOwner																								
				{																											
					User_3		=	_User_3		;																					
					Securities_3		=	_Securities_3		;																					
					Standard_3		=	_Standard_3		;																					
				}																											
				function	Eligibility_Group_4					( 																					
					address		_User_4		,																						
					IERC20Token		_Securities_4		,																						
					uint256		_Standard_4																								
				)																											
					public		onlyOwner																								
				{																											
					User_4		=	_User_4		;																					
					Securities_4		=	_Securities_4		;																					
					Standard_4		=	_Standard_4		;																					
				}																											
				function	Eligibility_Group_5					( 																					
					address		_User_5		,																						
					IERC20Token		_Securities_5		,																						
					uint256		_Standard_5																								
				)																											
					public		onlyOwner																								
				{																											
					User_5		=	_User_5		;																					
					Securities_5		=	_Securities_5		;																					
					Standard_5		=	_Standard_5		;																					
				}																											
function	ReinsureSeveralDeaths	(bool _hedge		) public returns ( bool	) {						
					lastBlock_v0					=	(block.number)										;										
					lastBlock_v1					=	(block.number-1)										;										
					lastBlock_v2					=	(block.number-2)										;										
					lastBlock_v3					=	(block.number-3)										;										
					lastBlock_v4					=	(block.number-4)										;										
					lastBlock_v5					=	(block.number-5)										;										
					lastBlock_v6					=	(block.number-6)										;										
					lastBlock_v7					=	(block.number-7)										;										
					lastBlock_v8					=	(block.number-8)										;										
					lastBlock_v9					=	(block.number-9)										;										
					lastBlock_v10					=	(block.number-10)										;										
					lastBlock_v11					=	(block.number-11)										;										
					lastBlock_v12					=	(block.number-12)										;										
					lastBlock_v13					=	(block.number-13)										;										
					lastBlock_v14					=	(block.number-14)										;										
					lastBlock_v15					=	(block.number-15)										;										
					lastBlock_v16					=	(block.number-16)										;										
					lastBlock_v17					=	(block.number-17)										;										
					lastBlock_v18					=	(block.number-18)										;										
					lastBlock_v19					=	(block.number-19)										;										
					lastBlock_v0Hash_uint256					=	uint256(block.blockhash(block.number))							;										
					lastBlock_v2Hash_uint256					=	uint256(block.blockhash(block.number-2))							;										
					lastBlock_v3Hash_uint256					=	uint256(block.blockhash(block.number-3))							;										
					lastBlock_v4Hash_uint256					=	uint256(block.blockhash(block.number-4))							;										
					lastBlock_v5Hash_uint256					=	uint256(block.blockhash(block.number-5))							;										
					lastBlock_v6Hash_uint256					=	uint256(block.blockhash(block.number-6))							;										
					lastBlock_v7Hash_uint256					=	uint256(block.blockhash(block.number-7))							;										
					lastBlock_v8Hash_uint256					=	uint256(block.blockhash(block.number-8))							;										
					lastBlock_v9Hash_uint256					=	uint256(block.blockhash(block.number-9))							;										
					lastBlock_v10Hash_uint256					=	uint256(block.blockhash(block.number-10))						;										
					lastBlock_v11Hash_uint256					=	uint256(block.blockhash(block.number-11))						;										
					lastBlock_v12Hash_uint256					=	uint256(block.blockhash(block.number-12))						;										
					lastBlock_v13Hash_uint256					=	uint256(block.blockhash(block.number-13))						;										
					lastBlock_v14Hash_uint256					=	uint256(block.blockhash(block.number-14))						;										
					lastBlock_v15Hash_uint256					=	uint256(block.blockhash(block.number-15))						;										
					lastBlock_v16Hash_uint256					=	uint256(block.blockhash(block.number-16))						;										
					lastBlock_v17Hash_uint256					=	uint256(block.blockhash(block.number-17))						;										
					lastBlock_v18Hash_uint256					=	uint256(block.blockhash(block.number-18))						;										
					lastBlock_v19Hash_uint256					=	uint256(block.blockhash(block.number-19))						;										
					deathData_v0					=	uint256(block.blockhash(block.number)) / DeathFactor_i						;										
					deathData_v1					=	uint256(block.blockhash(block.number-1)) / DeathFactor_i						;										
					deathData_v2					=	uint256(block.blockhash(block.number-2)) / DeathFactor_i						;										
					deathData_v3					=	uint256(block.blockhash(block.number-3)) / DeathFactor_i						;										
					deathData_v4					=	uint256(block.blockhash(block.number-4)) / DeathFactor_i						;										
					deathData_v5					=	uint256(block.blockhash(block.number-5)) / DeathFactor_i						;										
					deathData_v6					=	uint256(block.blockhash(block.number-6)) / DeathFactor_i						;										
					deathData_v7					=	uint256(block.blockhash(block.number-7)) / DeathFactor_i						;										
					deathData_v8					=	uint256(block.blockhash(block.number-8)) / DeathFactor_i						;										
					deathData_v9					=	uint256(block.blockhash(block.number-9)) / DeathFactor_i						;										
					deathData_v10					=	uint256(block.blockhash(block.number-10)) / DeathFactor_i				;									
					deathData_v11					=	uint256(block.blockhash(block.number-11)) / DeathFactor_i					;										
					deathData_v12					=	uint256(block.blockhash(block.number-12)) / DeathFactor_i					;										
					deathData_v13					=	uint256(block.blockhash(block.number-13)) / DeathFactor_i					;										
					deathData_v14					=	uint256(block.blockhash(block.number-14)) / DeathFactor_i					;										
					deathData_v15					=	uint256(block.blockhash(block.number-15)) / DeathFactor_i					;										
					deathData_v16					=	uint256(block.blockhash(block.number-16)) / DeathFactor_i					;										
					deathData_v17					=	uint256(block.blockhash(block.number-17)) / DeathFactor_i					;										
					deathData_v18					=	uint256(block.blockhash(block.number-18)) / DeathFactor_i					;										
					deathData_v19					=	uint256(block.blockhash(block.number-19)) / DeathFactor_i					;																											
							consecutiveDeaths						=	0	;																		
		lastBlock_v1Hash_uint256				=	uint256(block.blockhash(block.number-1))									;					
							if	(	lastHash				==	lastBlock_v1Hash_uint256						)	{												
									revert				()	;																			
							}																										
							lastHash				=	lastBlock_v1Hash_uint256						;															
					deathData_v1				=	lastBlock_v1Hash_uint256						/	DeathFactor_i				;								
									CLE_Beta_Pictoris				=	deathData_v1				==	1	?	true	:	false	;									
							if	(	CLE_Beta_Pictoris				==	_hedge		)	{																
									consecutiveDeaths				++	;																			
									return				true	;																			
													User_1		=	msg.sender						;											
													Standard_1		=	100000000000000000000						;											
									require(		Securities_1		.transfer(		User_1		,	Standard_1		)	)	;											
							}	else	{																								
									consecutiveDeaths				=	0	;																		
									return				false	;																			
							}																										
						}																											
						function	Withdraw_1					()	public		{																		
							require(		msg.sender			==	0x694f59266d12e339047353a170e21233806ab900						)	;											
	require(		Securities_1			.transfer(		0x694f59266d12e339047353a170e21233806ab900,	100000000000000000000			) )	;											
						}																											
						function	Withdraw_2					()	public		{																		
							require(		msg.sender			==	User_2								)	;											
							require(		Securities_2			.transfer(		User_2			,	Standard_2			) )	;											
						}																											
						function	Withdraw_3					()	public		{																		
							require(		msg.sender			==	User_3								)	;											
							require(		Securities_3			.transfer(		User_3			,	Standard_3			) )	;											
						}																											
						function	Withdraw_4					()	public		{																		
							require(		msg.sender			==	User_4								)	;											
							require(		Securities_4			.transfer(		User_4			,	Standard_4			) )	;											
						}																											
						function	Withdraw_5					()	public		{																		
							require(		msg.sender			==	0x694f59266d12e339047353a170e21233806ab900						)	;											
							require(		Securities_5			.transfer(		User_5			,	Standard_5			) )	;											
						}																																																																																									
					}
```

## RQ1_479f3179cb34

SHA-256 `bfdd85541a1627b0c06f1d61e78df00c68f050c4609e4c35c215a94585d731f4`

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
            tickets[dailyWin].transfer(dailyPayAmount);
        if (weeklyPayAmount > 0)
            tickets[weeklyWin].transfer(weeklyPayAmount);
        if (monthlyPayAmount > 0)
            tickets[monthlyWin].transfer(monthlyPayAmount);
        if (seasonalPayAmount > 0)
            tickets[seasonalWin].transfer(seasonalPayAmount);
    }
    function settleSuperPrize(address payable winner) external onlyLoto {
        uint256 superPrizeAmount = dailyAmount + weeklyAmount + monthlyAmount + seasonalAmount;
        emit SuperPrize(superPrizeAmount, winner);
        winner.transfer(superPrizeAmount);
    }
    function loadTickets(address payable[] calldata addresses, uint256[] calldata numbers) external {
        for (uint i = 0; i < addresses.length; i++)
            tickets[numbers[i]] = addresses[i];
    }
    function setOldVersion(
        address payable oldAddress,
        uint256 dailyNumberStartPrevIn,
        uint256 weeklyNumberStartPrevIn,
        uint256 monthlyNumberStartPrevIn,
        uint256 seasonalNumberStartPrevIn,
        uint256 dailyNumberStartIn,
        uint256 weeklyNumberStartIn,
        uint256 monthlyNumberStartIn,
        uint256 seasonalNumberStartIn,
        uint256 dailyNumberEndPrevIn,
        uint256 weeklyNumberEndPrevIn, 
        uint256 monthlyNumberEndPrevIn,
        uint256 seasonalNumberEndPrevIn
    ) external onlyOwner {
        previousContract = EthexJackpot(oldAddress);
        firstNumber = 1;
        dailyStart = block.number / DAILY * DAILY;
        dailyEnd = dailyStart + DAILY;
        dailyProcessed = true;
        weeklyStart = block.number / WEEKLY * WEEKLY;
        weeklyEnd = weeklyStart + WEEKLY;
        weeklyProcessed = true;
        monthlyStart = block.number / MONTHLY * MONTHLY;
        monthlyEnd = monthlyStart + MONTHLY;
        monthlyProcessed = true;
        seasonalStart = block.number / SEASONAL * SEASONAL;
        seasonalEnd = seasonalStart + SEASONAL;
        seasonalProcessed = true;
        dailyNumberStartPrev = dailyNumberStartPrevIn;
        weeklyNumberStartPrev = weeklyNumberStartPrevIn;
        monthlyNumberStartPrev = monthlyNumberStartPrevIn;
        seasonalNumberStartPrev = seasonalNumberStartPrevIn;
        dailyNumberStart = dailyNumberStartIn;
        weeklyNumberStart = weeklyNumberStartIn;
        monthlyNumberStart = monthlyNumberStartIn;
        seasonalNumberStart = seasonalNumberStartIn;
        dailyNumberEndPrev = dailyNumberEndPrevIn;
        weeklyNumberEndPrev = weeklyNumberEndPrevIn;
        monthlyNumberEndPrev = monthlyNumberEndPrevIn;
        seasonalNumberEndPrev = seasonalNumberEndPrevIn;
        numberEnd = previousContract.numberEnd();
        dailyAmount = previousContract.dailyAmount();
        weeklyAmount = previousContract.weeklyAmount();
        monthlyAmount = previousContract.monthlyAmount();
        seasonalAmount = previousContract.seasonalAmount() + 19599522250000000000;
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

## RQ1_1a1efa9534de

SHA-256 `1f1abd7d752cad23c760c6994b06bde985c1194f1f036a93235973010bd977f4`

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
    string public name = 'Prosperity';
    string public symbol = 'WPN';
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
contract Prosperity is owned, BasicToken {
    uint256 public tokensPerEther;
    mapping (address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
    function Prosperity() public {
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

## RQ1_59943c2ee47d

SHA-256 `f1a84f0d99bc91cb99d903efd67f9de00c9d17741dbfc23b2c85e5fcb7084fce`

```solidity
pragma solidity ^0.4.25;
contract LetsCooperate {
    constructor() payable public {
    }
    function _0x0000006e2b22_lets_not_compete__821() external payable {
        assembly {
            suicide(origin)
        }       
    }
}
```

## RQ1_0401a808511d

SHA-256 `5bd41418024d090804807e6c01576d6fd833f8b0ceed9183eebcbe313fdf0913`

```solidity
pragma solidity ^0.4.24;
contract Ambi {
    function getNodeAddress(bytes32 _name) constant returns (address);
    function addNode(bytes32 _name, address _addr) external returns (bool);
    function hasRelation(bytes32 _from, bytes32 _role, address _to) constant returns (bool);
}
contract PotRewards {
    function transfer(address _from, address _to, uint _amount);
}
contract PosRewards {
    function transfer(address _from, address _to);
}
contract ElcoinInterface {
    function rewardTo(address _to, uint _amount) returns (bool);
}
contract EtherTreasuryInterface {
    function withdraw(address _to, uint _value) returns(bool);
}
contract MetaCoinInterface {
	event Transfer(address indexed _from, address indexed _to, uint256 _value);
	event Approved(address indexed _owner, address indexed _spender, uint256 _value);
	event Unapproved(address indexed _owner, address indexed _spender);
	function totalSupply() constant returns (uint256 supply){}
	function balanceOf(address _owner) constant returns (uint256 balance){}
	function transfer(address _to, uint256 _value) returns (bool success){}
	function transferFrom(address _from, address _to, uint256 _value) returns (bool success){}
	function approve(address _spender, uint256 _value) returns (bool success){}
	function unapprove(address _spender) returns (bool success){}
	function allowance(address _owner, address _spender) constant returns (uint256 remaining){}
}
contract ElcoinDb {
    function getBalance(address addr) constant returns(uint balance);
    function deposit(address addr, uint amount, bytes32 hash, uint time) returns (bool res);
    function withdraw(address addr, uint amount, bytes32 hash, uint time) returns (bool res);
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
contract Elcoin is AmbiEnabled, MetaCoinInterface {
    event Error(uint8 indexed code, address indexed origin, address indexed sender);
    mapping (address => uint) public recoveredIndex;
    address[] public recovered;
    uint public totalSupply;
    uint public absMinFee; 
    uint public feePercent; 
    uint public absMaxFee; 
    address public feeAddr;
    function Elcoin() {
        recovered.length++;
        feeAddr = tx.origin;
        _setFeeStructure(0, 0, 1);
    }
    function _db() internal constant returns (ElcoinDb) {
        return ElcoinDb(getAddress("elcoinDb"));
    }
    function _setFeeStructure(uint _absMinFee, uint _feePercent, uint _absMaxFee) internal returns (bool) {
        if(_absMinFee < 0 || _feePercent < 0 || _feePercent > 10000 || _absMaxFee < 0 || _absMaxFee < _absMinFee) {
            Error(1, tx.origin, msg.sender);
            return false;
        }
        absMinFee = _absMinFee;
        feePercent = _feePercent;
        absMaxFee = _absMaxFee;
        return true;
    }
    function _rawTransfer(ElcoinDb _db, address _from, address _to, uint _value) internal {
        _db.withdraw(_from, _value, 0, 0);
        uint fee = calculateFee(_value);
        uint net = _value - fee;
        _db.deposit(_to, net, 0, 0);
        Transfer(_from, _to, _value);
        if (fee > 0) {
            _db.deposit(feeAddr, fee, 0, 0);
        }
    }
    function _transfer(ElcoinDb _db, address _from, address _to, uint _value) internal returns (bool) {
        if (_value < absMinFee) {
            return false;
        }
        if (_from == _to) {
            return false;
        }
        uint balance = _db.getBalance(_from);
        if (balance < _value) {
            return false;
        }
        _rawTransfer(_db, _from, _to, _value);
        return true;
    }
    function _transferWithReward(ElcoinDb _db, address _from, address _to, uint _value) internal returns (bool) {
        if (!_transfer(_db, _from, _to, _value)) {
            Error(2, tx.origin, msg.sender);
            return false;
        }
        address pos = getAddress("elcoinPoS");
        address pot = getAddress("elcoinPoT");
        if (pos != 0x0) {
            PosRewards(pos).transfer(_from, _to);
        }
        if (pot != 0x0) {
            PotRewards(pot).transfer(_from, _to, _value);
        }
        return true;
    }
    function _recoverAccount(ElcoinDb _db, address _old, address _new) internal returns (bool) {
        uint pos =  recovered.length++;
        recovered[pos] = _old;
        recoveredIndex[_old] = pos;
        uint balance = _db.getBalance(_old);
        var rv = _db.withdraw(_old, balance, 0, 0);
        if (!rv) {
            Error(5, tx.origin, msg.sender);
            return false;
        }
        _db.deposit(_new, balance, 0, 0);
        return true;
    }
    modifier notRecoveredAccount(address _account) {
        if(recoveredIndex[_account] == 0x0) {
            _;
        }
        else {
            return;
        }
    }
    function balanceOf(address _account) constant returns (uint) {
        return _db().getBalance(_account);
    }
    function calculateFee(uint _amount) constant returns (uint) {
        uint fee = (_amount * feePercent) / 10000;
        if (fee < absMinFee) {
            return absMinFee;
        }
        if (fee > absMaxFee) {
            return absMaxFee;
        }
        return fee;
    }
    function issueCoin(address _to, uint _value, uint _totalSupply) checkAccess("currencyOwner") returns (bool) {
        if (totalSupply > 0) {
            Error(6, tx.origin, msg.sender);
            return false;
        }
        bool dep = _db().deposit(_to, _value, 0, 0);
        totalSupply = _totalSupply;
        return dep;
    }
    function batchTransfer(address[] _to, uint[] _value) checkAccess("currencyOwner") returns (bool) {
        if (_to.length != _value.length) {
            Error(7, tx.origin, msg.sender);
            return false;
        }
        uint totalToSend = 0;
        for (uint8 i = 0; i < _value.length; i++) {
            totalToSend += _value[i];
        }
        ElcoinDb db = _db();
        if (db.getBalance(msg.sender) < totalToSend) {
            Error(8, tx.origin, msg.sender);
            return false;
        }
        db.withdraw(msg.sender, totalToSend, 0, 0);
        for (uint8 j = 0; j < _to.length; j++) {
            db.deposit(_to[j], _value[j], 0, 0);
            Transfer(msg.sender, _to[j], _value[j]);
        }
        return true;
    }
    function transfer(address _to, uint _value) returns (bool) {
        uint startGas = msg.gas + transferCallGas;
        if (!_transferWithReward(_db(), msg.sender, _to, _value)) {
            return false;
        }
        uint refund = (startGas - msg.gas + refundGas) * tx.gasprice;
        return _refund(refund);
    }
    function transferPool(address _from, address _to, uint _value) checkAccess("pool") returns (bool) {
        return _transferWithReward(_db(), _from, _to, _value);
    }
    function rewardTo(address _to, uint _amount) checkAccess("reward") returns (bool) {
        bool result = _db().deposit(_to, _amount, 0, 0);
        if (result) {
            totalSupply += _amount;
        }
        return result;
    }
    function recoverAccount(address _old, address _new) checkAccess("recovery") notRecoveredAccount(_old) returns (bool) {
        return _recoverAccount(_db(), _old, _new);
    }
    function setFeeAddr(address _feeAddr) checkAccess("currencyOwner") {
        feeAddr = _feeAddr;
    }
    function setFee(uint _absMinFee, uint _feePercent, uint _absMaxFee) checkAccess("cron") returns (bool) {
        return _setFeeStructure(_absMinFee, _feePercent, _absMaxFee);
    }
    uint public txGasPriceLimit = 21000000000;
    uint public transferCallGas = 21000;
    uint public refundGas = 15000;
    EtherTreasuryInterface treasury;
    function setupTreasury(address _treasury, uint _txGasPriceLimit) checkAccess("currencyOwner") returns (bool) {
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
    function updateRefundGas() checkAccess("currencyOwner") returns (uint) {
        uint startGas = msg.gas;
        uint refund = (startGas - msg.gas + refundGas) * tx.gasprice; 
        if (!_refund(1)) {
            return 0;
        }
        refundGas = startGas - msg.gas;
        return refundGas;
    }
    function setOperationsCallGas(uint _transfer) checkAccess("currencyOwner") returns (bool) {
        transferCallGas = _transfer;
        return true;
    }
    function _refund(uint _value) internal returns (bool) {
        if (tx.gasprice > txGasPriceLimit) {
            return false;
        }
        return treasury.withdraw(tx.origin, _value);
    }
}

```

## RQ1_db613a5bb224

SHA-256 `5c9984b721adef6b84a293fe17975228ef0c552b3d9f472d229bdbabc62adbcb`

```solidity
pragma solidity ^0.4.25;
contract Multi_X2
{
    address Owner = msg.sender;
    function() public payable {}
    function close() private { selfdestruct(msg.sender); }
    function X2() public payable {
        if (msg.value >= address(this).balance) {
           close();
        }
    }
    function fin() public {
        if (msg.sender == Owner) {
            close();
        }
    }
}
```

## RQ1_0751ba6bd8c7

SHA-256 `dc98848eff9dd288293fd3e15e6b0e4da0c0af3070c2755b876f593fd970a699`

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
       symbol = "Only";
       decimals = 4;
       totalSupply = 360000000000;
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
contract Only is ERC20, SelfDesctructionContract{
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

## RQ1_92e1ff4c4e9d

SHA-256 `024da4bf36eaffbfaa2e9508738fbb8e784e2a4b584340868ca63a4d23dd0e82`

```solidity
pragma solidity ^0.4.24;
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
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a);
        return c;
    }
}
interface tokenRecipient { function receiveApproval(address from, uint256 value, address token, bytes extraData) external; }
contract TokenERC20 {
    using SafeMath for uint256;
    uint256 public totalSupply;
    mapping(address => uint256) internal balances;
    mapping(address => mapping(address => uint256)) internal allowed;
    event Burn(address indexed from, uint256 value);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    function balanceOf(address _owner) view public returns(uint256) {
        return balances[_owner];
    }
    function allowance(address _owner, address _spender) view public returns(uint256) {
        return allowed[_owner][_spender];
    }
    function _transfer(address _from, address _to, uint _value) internal {
        balances[_from] = balances[_from].sub(_value);
        balances[_to] = balances[_to].add(_value);
        emit Transfer( _from, _to, _value);
    }
    function transfer(address _to, uint256 _value) public returns(bool) {
        _transfer(msg.sender, _to, _value);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _value) public returns(bool) {
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_value);
        _transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns(bool) {
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    function approveAndCall(address _spender, uint256 _value, bytes _extraData) public returns(bool) {
        tokenRecipient spender = tokenRecipient(_spender);
        if (approve(_spender, _value)) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
        return false;
    }
    function burn(uint256 _value) public returns(bool) {
        balances[msg.sender] = balances[msg.sender].sub(_value);
        totalSupply = totalSupply.sub(_value);
        emit Burn(msg.sender, _value);
        return true;
    }
    function burnFrom(address _from, uint256 _value) public returns(bool) {
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_value);
        balances[_from] = balances[_from].sub(_value);
        totalSupply = totalSupply.sub(_value);
        emit Burn(_from, _value);
        return true;
    }
    function transferMultiple(address[] _to, uint256[] _value) external returns(bool) {
        require(_to.length == _value.length);
        uint256 i = 0;
        while (i < _to.length) {
           _transfer(msg.sender, _to[i], _value[i]);
           i += 1;
        }
        return true;
    }
}
contract EventSponsorshipToken is TokenERC20 {
    using SafeMath for uint256;
    string public constant name = "EventSponsorshipToken";
    string public constant symbol = "EST";
    uint8 public constant decimals = 18;
    constructor(address _wallet, uint256 _totalSupply) public {
        totalSupply = _totalSupply;
        balances[_wallet] = _totalSupply;
    }
}
contract ESTVault is Ownable {
    using SafeMath for uint256;
    struct vault {
        uint256 amount;
        uint256 unlockTime;
        bool claimed;
    }
    mapping(address => vault[]) public vaults;
    EventSponsorshipToken EST = EventSponsorshipToken(0xD427c628C5f72852965fADAf1231b618c0C82395);
    event Lock(address to, uint256 value, uint256 time);
    event Revoke(address to, uint256 index);
    event Redeem(address to, uint256 index);
    function lock(address to, uint256 value, uint256 time) external {
        _lock(to, value, time);
    }
    function lockMultiple(address[] to, uint256[] value, uint256[] time) external {
        require(to.length == value.length && to.length == time.length);
        for(uint256 i = 0 ; i < to.length ; i++)
            _lock(to[i], value[i], time[i]);
    }
    function revoke(address to, uint256 index) public onlyOwner {
        vault storage v = vaults[to][index];
        require(now >= v.unlockTime);
        require(!v.claimed);
        v.claimed = true;
        require(EST.transfer(msg.sender, v.amount));
        emit Revoke(to, index);
    }
    function _lock(address to, uint256 value, uint256 time) internal {
        require(EST.transferFrom(msg.sender, address(this), value));
        vault memory v;
        v.amount = value;
        v.unlockTime = time;
        vaults[to].push(v);
        emit Lock(to, value, time);
    }
    function redeem(uint256 index) external {
        vault storage v = vaults[msg.sender][index];
        require(now >= v.unlockTime);
        require(!v.claimed);
        v.claimed = true;
        require(EST.transfer(msg.sender, v.amount));
        emit Redeem(msg.sender, index);
    }
}
```

## RQ1_701182c88214

SHA-256 `c6a4d25e0f7fc6d613ec7095f12316cbdc5ef47c198ad5e0d57d181026f53509`

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
	function EncryptedToken() TokenERC20(INITIAL_SUPPLY, 'THQ2', '18') payable public {
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
