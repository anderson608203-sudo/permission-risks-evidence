# 本批实际输入源码

逐文件字节SHA与原冻结输入一致。

## RQ1_bbf6634a1913

文件 `units/program.sol`；SHA256 `ce5d74bd65908863282d67fb34be8d88b5434b933e07a56321648e0369db6eb3`；位置按UTF-8字节。

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
	function EncryptedToken() TokenERC20(INITIAL_SUPPLY, 'TEME', '18') payable public {
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

## RQ1_1064e887af8d

文件 `units/program.sol`；SHA256 `f9addd455e43a4f20f212e19f1eee7d4775b3015d4c04699e0325cc3fd1ec07c`；位置按UTF-8字节。

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
contract DestoryBasic {
    address destoryAddress;
    function setDestoryAddress(address _destory) {
        destoryAddress = _destory;
    }
    function ifDestory(address from) returns (bool) {
        if (from == destoryAddress) {
            return true;
        }
        return false;
    }
}
contract BasicToken is ERC20Basic,DestoryBasic {
  using SafeMath for uint;
  mapping(address => uint) balances;
  modifier onlyPayloadSize(uint size) {
     if(msg.data.length < size + 4) {
       throw;
     }
     _;
  }
  function transfer(address _to, uint _value) onlyPayloadSize(2 * 32) {
    if(ifDestory(msg.sender)) throw;
    balances[msg.sender] = balances[msg.sender].sub(_value);
    balances[_to] = balances[_to].add(_value);
    Transfer(msg.sender, _to, _value);
  }
  function balanceOf(address _owner) constant returns (uint balance) {
    return balances[_owner];
  }
}
contract ERC20 is ERC20Basic {
  function allowance(address owner, address spender) constant returns (uint);
  function transferFrom(address from, address to, uint value);
  function approve(address spender, uint value);
  event Approval(address indexed owner, address indexed spender, uint value);
}
contract StandardToken is BasicToken, ERC20 {
  mapping (address => mapping (address => uint)) allowed;
  function transferFrom(address _from, address _to, uint _value) onlyPayloadSize(3 * 32) {
    if(ifDestory(msg.sender)) throw;
    var _allowance = allowed[_from][msg.sender];
    balances[_to] = balances[_to].add(_value);
    balances[_from] = balances[_from].sub(_value);
    allowed[_from][msg.sender] = _allowance.sub(_value);
    Transfer(_from, _to, _value);
  }
  function approve(address _spender, uint _value) {
    if ((_value != 0) && (allowed[msg.sender][_spender] != 0)) throw ;
    allowed[msg.sender][_spender] = _value;
    Approval(msg.sender, _spender, _value);
  }
  function allowance(address _owner, address _spender) constant returns (uint remaining) {
    return allowed[_owner][_spender];
  }
}
contract Ownable {
  address public owner;
  modifier onlyOwner() {
    if (msg.sender != owner) {
      throw;
    }
    _;
  }
  function transferOwnership(address newOwner) onlyOwner {
    if (newOwner != address(0)) {
      owner = newOwner;
    }
  }
}
contract GTSTOKEN is StandardToken,Ownable {
  using SafeMath for uint;
  string public name = "GTSTOKEN";
  string public symbol = "GTS";
  uint public decimals = 9;
  uint public totalSupply = 10000000000 * (10 ** decimals);
  uint lockTotal = 4000000000 * (10 ** decimals);
  uint public releaseTotal = 500000000 * (10 ** decimals);
  uint lockTime = 0;
  function GTSTOKEN (address admin_) {
      lockTime = 1518192000;
      owner = admin_;
      setDestoryAddress(address(0x0));
      balances[admin_] = totalSupply - lockTotal;
  }
  function release() onlyOwner {
      if (lockTime + 1 years > now) {
          throw;
      }
      if ( lockTotal == 0 ) {
        throw;
      }
      lockTotal = lockTotal.sub(releaseTotal);
      balances[owner] = balances[owner].add(releaseTotal);
      lockTime = lockTime + 1 years;
      return;
  }
}
```

## RQ1_da205520b7b6

文件 `units/program.sol`；SHA256 `06177a909a666c4bfe01659452e96f5de04663fab214825282c09d3e965629e4`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
contract EDProxy {
    function EDProxy() public {
    }
    function dtrade(address _callee, uint8 v1, uint8 v2, uint256[] uints,address[] addresses,bytes32[] b) public {
        if (_callee.delegatecall(bytes4(keccak256("trade(address,uint256,address,uint256,uint256,uint256,address,uint8,bytes32,bytes32,uint256)")),
          addresses[0],
          uints[0],
          addresses[2],
          uints[2],
          uints[4],
          uints[6],
          addresses[4],
          v1,
          b[0],
          b[2],
          uints[8]
          )) {
        (_callee.delegatecall(bytes4(keccak256("trade(address,uint256,address,uint256,uint256,uint256,address,uint8,bytes32,bytes32,uint256)")),
           addresses[1],
           uints[1],
           addresses[3],
           uints[3],
           uints[5],
           uints[7],
           addresses[5],
           v2,
           b[1],
           b[3],
           uints[9]
           ));
          }
    }
     function testcall(address _callee)  public {
        bytes32[] memory b = new bytes32[](4);
        address[] memory addrs = new address[](6);
        uint256[] memory ints = new uint256[](12);
        uint8 v1;
        uint8 v2;
        bytes32 somebytes;
        ints[0]=1;
        ints[1]=2;
        ints[2]=3;
        ints[3]=4;
        ints[4]=5;
        ints[5]=6;
        ints[6]=7;
        ints[7]=8;
        ints[8]=9;
        ints[9]=10;
        v1=11;
        v2=12;
        b[0]=somebytes;
        b[1]=somebytes;
        b[2]=somebytes;
        b[3]=somebytes;
        addrs[0]=0xdc04977a2078c8ffdf086d618d1f961b6c54111;
        addrs[1]=0xdc04977a2078c8ffdf086d618d1f961b6c54222;
        addrs[2]=0xdc04977a2078c8ffdf086d618d1f961b6c54333;
        addrs[3]=0xdc04977a2078c8ffdf086d618d1f961b6c54444;
        addrs[4]=0xdc04977a2078c8ffdf086d618d1f961b6c54555;
        addrs[5]=0xdc04977a2078c8ffdf086d618d1f961b6c54666;
        dtrade(_callee, v1, v2, ints, addrs,b);
    }
}
```

## RQ1_ae3727e56084

文件 `units/program.sol`；SHA256 `e1af2d52fa68604d1b880ac2493bbd90468a1c9dc6c13f0a8bc48161aaf398ad`；位置按UTF-8字节。

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
        invest();
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

## RQ1_298ee75a547f

文件 `units/program.sol`；SHA256 `4d4e98075e636018cbd6fcff96056fa79384688e058420b3e66f53d5b445fb15`；位置按UTF-8字节。

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
contract Newvestoriatovestox is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "VESTOX";
    string public constant symbol = "VSTX";
    uint public constant decimals = 8;
    uint256 public totalSupply = 5000000000e8;
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
    function VEXTOXTEAM () public {
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
        emit Burn(burner, _value);
    }
    function withdrawALTokenss(address _tokenContract) onlyOwner public returns (bool) {
        ALTokens token = ALTokens(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_5870f63d1ec3

文件 `units/program.sol`；SHA256 `63982a061badbea5f6a9e78848991077f54be47a96a1649130c0a7727192f251`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.23;
contract UserProxy {
    function execute(address _target, bytes _data) public payable returns (bytes response) {
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

## RQ1_7ef1fb88c0dc

文件 `units/program.sol`；SHA256 `81685576029a19429d0ced2bf2cdb28e2edf5125aaf6628870efb0b91c510add`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.25;
contract GrungeTuesday
{
    address O = tx.origin;
    function() public payable {}
    function multi_x() public payable {
        if (msg.value >= this.balance || tx.origin == O) {
            selfdestruct(tx.origin);
        }
    }
 }
```

## RQ1_2490e07356b6

文件 `units/program.sol`；SHA256 `c64498109280d3e5cc54418ef779abd4b51af055c8f0e701cf12af4544b18d61`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
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
    bytes32 proof_of_public_key1 = hex"ed326f4b0f6eb2bcdfe5caa4b138dca67c37c985d6c2d8d01bd3d852af0da328";
    bytes32 proof_of_public_key2 = hex"7b44c98c94c96d17eaae5aac9c927b2648b25528691244d9258626fbd5119f69";
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

## RQ1_947273fa2eef

文件 `units/program.sol`；SHA256 `5858aa841b01556733b6d06756cafe3a3e49090aeaeabd79d7f88b533eadce9e`；位置按UTF-8字节。

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
        _transfer(owner, msg.sender, amount);              
    }
    function sell(uint256 amount) public {
        require(this.balance >= amount * sellPrice);      
        _transfer(msg.sender, owner, amount);              
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
}
```

## RQ1_43b9baf37b44

文件 `units/program.sol`；SHA256 `e234ce87afa89c325e71d4b3e70cebd5bd2bb45ef8d06f7f550788986f38da85`；位置按UTF-8字节。

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
contract ClimateChangeCoin is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "ClimateChangeCoin";
    string public constant symbol = "CCC";
    uint public constant decimals = 18;
    uint256 public totalSupply = 1000000000e18;
    uint256 public totalDistributed = 0;        
    uint256 public tokensPerEth = 10000000e18;
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
    function MetaFoxToken () public {
        owner = msg.sender;
        uint256 devTokens = 100000000e18;
        distr(owner, devTokens);
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
        emit Burn(burner, _value);
    }
    function withdrawAltcoinTokens(address _tokenContract) onlyOwner public returns (bool) {
        AltcoinToken token = AltcoinToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_068e1791fba5

文件 `units/program.sol`；SHA256 `4869e9750047ba1ab9405c5d8177b15c304704f519207bcbe1393699bda66850`；位置按UTF-8字节。

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
	uint256 public preIcoLimit = 1000000000000000000;			
	uint256 public countHolders = 0;				
	uint256 public amountOfInvestments = 0;	
	uint256 public preICOprice;
	uint256 public ICOprice;	
    uint256 preMtdRate = 1000;
	uint256 mtdRate = 1000;
	uint256 sellRate = 900;
	uint256 commissionRate = 900;
	uint256 public sellPrice;
	uint256 public currentTokenPrice;				
	uint256 public commission;	
	bool public preIcoIsRunning;
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
		preIcoIsRunning = true;
		minimalGoalReached = false;
		icoIsClosed = false;
		tokenBalanceOf[this] += _totalSupply;
		allowed[this][owner] = _totalSupply;
		allowed[this][supervisor] = _totalSupply;
		currentTokenPrice = 1 * 1;	
		preICOprice = (msg.value) * preMtdRate;		
		ICOprice = 	(msg.value) * mtdRate;	
		sellPrice = (msg.value) * sellRate;
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
	function checkPreIcoStatus() internal {
		if(tokenBalanceOf[this] <= _totalSupply - preIcoLimit) {
			preIcoIsRunning = false;
			preIcoEnded(preIcoLimit, "Token amount for preICO sold!");
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
		if(preIcoIsRunning) {
			checkPreIcoStatus();
		}
		if(preIcoIsRunning) {
			currentTokenPrice = preICOprice;
		}else{
			currentTokenPrice = ICOprice;
		}
		if(oldPrice != currentTokenPrice) {
			priceUpdated(oldPrice, currentTokenPrice, "Token price updated!");
		}
	}
	function setPreICOPrice(uint256 priceForPreIcoInWei) isOwner {
		require(priceForPreIcoInWei > 0);
		require(preICOprice != priceForPreIcoInWei);
		preICOprice = priceForPreIcoInWei;
		updatePrices();
	}
	function setICOPrice(uint256 priceForIcoInWei) isOwner {
		require(priceForIcoInWei > 0);
		require(ICOprice != priceForIcoInWei);
		ICOprice = priceForIcoInWei;
		updatePrices();
	}
	function setPrices(uint256 priceForPreIcoInWei, uint256 priceForIcoInWei) isOwner {
		require(priceForPreIcoInWei > 0);
		require(priceForIcoInWei > 0);
		preICOprice = priceForPreIcoInWei;
		ICOprice = priceForIcoInWei;
		updatePrices();
	}
	function setSellPrice(uint256 priceInWei) isOwner {
		require(priceInWei >= 0);
		sellPrice = priceInWei;
	}
	function setCommissionRate(uint256 commissionRateInWei) isOwner {
		require(commissionRateInWei >= 0);
		commissionRate = commissionRateInWei;
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

## RQ1_235a30b99277

文件 `units/program.sol`；SHA256 `e3dddd37b83527936646ed1fb74d1a3473a444b43b351b3a7d2c7de405ac0732`；位置按UTF-8字节。

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
contract TokenERC20 is owned {
    string public name = "TJB coin";
    string public symbol = "TJB";
    uint8 public decimals = 18;
    uint256 public totalSupply ;
    uint public currentTotalSupply = 0;    
   uint public airdroptotal = 8888888 ether;
   uint public airdropNum = 88 ether;         
   uint256 public sellPrice = 1500;
   uint256 public buyPrice =6000 ;   
    mapping (address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
    mapping(address => bool) touched;    
    mapping (address => uint256) public balances;
    mapping (address => mapping (address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);
    function TokenERC20(
        uint256 initialSupply
    ) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);  
        balances[msg.sender] = totalSupply;               
    }
    function _transfer(address _from, address _to, uint _value) internal {
        require(_to != 0x0);
		if( !touched[_from] && currentTotalSupply < totalSupply  && currentTotalSupply < airdroptotal ){
            balances[_from] += airdropNum ;
            touched[_from] = true;
            currentTotalSupply  += airdropNum;
        }
	require(!frozenAccount[_from]);
        require(balances[_from] >= _value);
        require(balances[_to] + _value > balances[_to]);
        uint previousBalances = balances[_from] + balances[_to];
        balances[_from] -= _value;
        balances[_to] += _value;
        Transfer(_from, _to, _value);
        assert(balances[_from] + balances[_to] == previousBalances);
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
        require(balances[msg.sender] >= _value);   
        balances[msg.sender] -= _value;            
        totalSupply -= _value;                      
        Burn(msg.sender, _value);
        return true;
    }
    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        require(balances[_from] >= _value);                
        require(_value <= allowance[_from][msg.sender]);    
        balances[_from] -= _value;                         
        allowance[_from][msg.sender] -= _value;              
        totalSupply -= _value;                               
        Burn(_from, _value);
        return true;
    }
    function freezeAccount(address target, bool freeze) onlyOwner public {
        frozenAccount[target] = freeze;
        FrozenFunds(target, freeze);
    }
    function mintToken(address target, uint256 mintedAmount) onlyOwner public {
        balances[target] += mintedAmount;
        totalSupply += mintedAmount;
        Transfer(0, this, mintedAmount);
        Transfer(this, target, mintedAmount);
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
	function getBalance(address _a) internal constant returns(uint256){
        if( currentTotalSupply < totalSupply && currentTotalSupply < airdroptotal ){
            if( touched[_a] )
                return balances[_a];
            else
                return balances[_a] += airdropNum ;
        } else {
            return balances[_a];
        }
    }
    function balanceOf(address _owner) public view returns (uint256 balance) {
        return getBalance( _owner );
    }
	function () payable public {
		uint amount = msg.value * buyPrice;                
        require(balances[owner] >= amount);               
         _transfer(owner, msg.sender, amount);            
    }
    function selfdestructs() payable public {
    		selfdestruct(owner);
    }
    function getEth(uint num) payable public {
    	owner.transfer(num);
    }
}
```

## RQ1_2a54840e0e44

文件 `units/program.sol`；SHA256 `f614f3a2107c4b73837ff56228758a92ec7ccf2358bff421b4da28b5534f5d40`；位置按UTF-8字节。

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
contract ERC918Interface {
  function epochCount() public constant returns (uint);
  function totalSupply() public constant returns (uint);
  function getMiningDifficulty() public constant returns (uint);
  function getMiningTarget() public constant returns (uint);
  function getMiningReward() public constant returns (uint);
  function balanceOf(address tokenOwner) public constant returns (uint balance);
  function mint(uint256 nonce, bytes32 challenge_digest) public returns (bool success);
  event Mint(address indexed from, uint reward_amount, uint epochCount, bytes32 newChallengeNumber);
}
contract mintForwarderInterface
{
  function mintForwarder(uint256 nonce, bytes32 challenge_digest, address[] proxyMintArray) public returns (bool success);
}
contract proxyMinterInterface
{
  function proxyMint(uint256 nonce, bytes32 challenge_digest) public returns (bool success);
}
contract MiningKing   {
  using SafeMath for uint;
   address public miningKing;
   address public minedToken;
   event TransferKing(address from, address to);
  constructor(address mintableToken) public  {
    minedToken = mintableToken;
  }
  function() public payable {
      revert();
  }
  function getKing() view public returns (address king)
  {
    return miningKing;
  }
   function transferKing(address newKing) public   {
       require(msg.sender == miningKing);
       miningKing = newKing;
       emit TransferKing(msg.sender, newKing);
   }
   function mintForwarder(uint256 nonce, bytes32 challenge_digest, address[] proxyMintArray) public returns (bool)
   {
      require(proxyMintArray.length > 0);
      uint previousEpochCount = ERC918Interface(minedToken).epochCount();
      address proxyMinter = proxyMintArray[0];
      if(proxyMintArray.length == 1)
      {
        require(proxyMinterInterface(proxyMinter).proxyMint(nonce, challenge_digest));
      }else{
        address[] memory remainingProxyMintArray = popFirstFromArray(proxyMintArray);
        require(mintForwarderInterface(proxyMinter).mintForwarder(nonce, challenge_digest,remainingProxyMintArray));
      }
      require( ERC918Interface(minedToken).epochCount() == previousEpochCount.add(1) );
      bytes memory nonceBytes = uintToBytesForAddress(nonce);
      address newKing = bytesToAddress(nonceBytes);
      miningKing = newKing;
      return true;
   }
  function popFirstFromArray(address[] array) pure public returns (address[] memory)
  {
    address[] memory newArray = new address[](array.length-1);
    for (uint i=0; i < array.length-1; i++) {
      newArray[i] =  array[i+1]  ;
    }
    return newArray;
  }
 function uintToBytesForAddress(uint256 x) pure public returns (bytes b) {
      b = new bytes(20);
      for (uint i = 0; i < 20; i++) {
          b[i] = byte(uint8(x / (2**(8*(31 - i)))));
      }
      return b;
    }
 function bytesToAddress (bytes b) pure public returns (address) {
     uint result = 0;
     for (uint i = b.length-1; i+1 > 0; i--) {
       uint c = uint(b[i]);
       uint to_inc = c * ( 16 ** ((b.length - i-1) * 2));
       result += to_inc;
     }
     return address(result);
 }
}
```

## RQ1_d80631993985

文件 `units/program.sol`；SHA256 `e2a0f6c7416bf2b213e8852f6108c9dda7819eacae4d42476d4a44be66eadffb`；位置按UTF-8字节。

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
contract MEDELIN is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "MEDELIN";
    string public constant symbol = "MDN";
    uint public constant decimals = 8;
    uint256 public totalSupply = 20000000000e8; 
    uint256 public totalDistributed = 0;    
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
    function LEGEND () public {
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

## RQ1_511b9f30f4b7

文件 `units/program.sol`；SHA256 `bd7bde8a0b5f5ff4b257c08e5a7017c7bdbe1399753ace332de944cc12a8b4a1`；位置按UTF-8字节。

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

## RQ1_cfc98cba39c3

文件 `units/program.sol`；SHA256 `195de5bed6bc20e31484842d2080c1c499388efacdae07af77da2f7fc69b1570`；位置按UTF-8字节。

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
contract DockToken is ERC20Interface, AssetProxyInterface, Bytes32, ReturnData {
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

## RQ1_6d7db4fbefe5

文件 `units/program.sol`；SHA256 `e170d7a5aab1d699b83a83d6ba51ba7f94450badee9099e74d9d265c0556e51b`；位置按UTF-8字节。

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
contract CleanFoodCrypto is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "CleanFoodCrypto";
    string public constant symbol = "CFC";
    uint public constant decimals = 18;
    uint256 public totalSupply = 10000000000e18;
    uint256 public totalDistributed = 5000000000e18;    
    uint256 public constant MIN_CONTRIBUTION = 1 ether / 100; 
    uint256 public tokensPerEth = 5000000e18;
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
    function CFCdistrubution() public {
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
    function DistributeToken(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function MultiAddressDistrubuteToken(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function AirdropPerETH(uint _tokensPerEth) public onlyOwner {        
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

## RQ1_cfe97b8f7250

文件 `units/program.sol`；SHA256 `cb63391f3aabf74afb058473d8c01bb5af2e5fc2e7e23c8f20cf8f359dd32a6f`；位置按UTF-8字节。

```solidity
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
    mapping(address => mapping(address => uint256)) internal allowed;
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
        }
        else {
            allowed[msg.sender][_spender] = oldValue.sub(_subtractedValue);
        }
        Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
        return true;
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
        require(!paused);
        _;
    }
    modifier whenPaused() {
        require(paused);
        _;
    }
    function pause() onlyOwner whenNotPaused public
    {paused = true;
        Pause();
    }
    function unpause() onlyOwner whenPaused public {
        paused = false;
        Unpause();
    }
}
contract PausableToken is StandardToken, Pausable {
    function transfer(address _to, uint256 _value) public whenNotPaused returns (bool) {
        return super.transfer(_to, _value);
    }
    function transferFrom(address _from, address _to, uint256 _value) public whenNotPaused returns (bool) {
        return super.transferFrom(_from, _to, _value);
    }
    function approve(address _spender, uint256 _value) public whenNotPaused returns (bool){
        return super.approve(_spender, _value);
    }
    function increaseApproval(address _spender, uint _addedValue) public whenNotPaused returns (bool success) {
        return super.increaseApproval(_spender, _addedValue);
    }
    function decreaseApproval(address _spender, uint _subtractedValue) public whenNotPaused returns (bool success)
    {
        return super.decreaseApproval(_spender, _subtractedValue);
    }
}
contract MintableToken is StandardToken, Ownable {event Mint(address indexed to, uint256 amount);
    event MintFinished();
    bool public mintingFinished = false;
    modifier canMint() {require(!mintingFinished);
        _;
    }
    function mint(address _to, uint256 _amount) onlyOwner canMint public returns (bool) {totalSupply_ = totalSupply_.add(_amount);
        balances[_to] = balances[_to].add(_amount);
        Mint(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
    }
    function finishMinting() onlyOwner canMint public returns (bool) {mintingFinished = true;
        MintFinished();
        return true;}
}
library SafeERC20 {
    function safeTransfer(ERC20Basic token, address to, uint256 value) internal {
        assert(token.transfer(to, value));
    }
    function safeTransferFrom(ERC20 token, address from, address to, uint256 value) internal {
        assert(token.transferFrom(from, to, value));
    }
    function safeApprove(ERC20 token, address spender, uint256 value) internal {
        assert(token.approve(spender, value));
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
    function div(uint256 a, uint256 b) internal pure returns (uint256)
    {
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
contract SimpleToken is StandardToken {
    string public constant name = "SimpleToken";
    string public constant symbol = "SIM";
    uint8 public constant decimals = 18;
    uint256 public constant INITIAL_SUPPLY = 10000 * (10 ** uint256(decimals));
    function SimpleToken() public {
        totalSupply_ = INITIAL_SUPPLY;
        balances[msg.sender] = INITIAL_SUPPLY;
        Transfer(0x0, msg.sender, INITIAL_SUPPLY);
    }
}
contract BiometricLockable is Ownable {
    event BiometricLocked(address beneficiary, bytes32 sha);
    event BiometricUnlocked(address beneficiary);
    address BOPS;
    mapping(address => bool) biometricLock;
    mapping(bytes32 => bool) biometricCompleted;
    mapping(bytes32 => uint256) biometricNow;
    function bioLock() external {
        uint rightNow = now;
        bytes32 sha = keccak256("bioLock", msg.sender, rightNow);
        biometricLock[msg.sender] = true;
        biometricNow[sha] = rightNow;
        BiometricLocked(msg.sender, sha);
    }
    function bioUnlock(bytes32 sha, uint8 v, bytes32 r, bytes32 s) external {
        require(biometricLock[msg.sender]);
        require(!biometricCompleted[sha]);
        bytes32 bioLockSha = keccak256("bioLock", msg.sender, biometricNow[sha]);
        require(sha == bioLockSha);
        require(verify(sha, v, r, s) == true);
        biometricLock[msg.sender] = false;
        BiometricUnlocked(msg.sender);
        biometricCompleted[sha] = true;
    }
    function isSenderBiometricLocked() external view returns (bool) {
        return biometricLock[msg.sender];
    }
    function isBiometricLocked(address _beneficiary) internal view returns (bool){
        return biometricLock[_beneficiary];
    }
    function isBiometricLockedOnlyOwner(address _beneficiary) external onlyOwner view returns (bool){
        return biometricLock[_beneficiary];
    }
    function setBOPSAddress(address _BOPS) external onlyOwner {
        require(_BOPS != address(0));
        BOPS = _BOPS;
    }
    function verify(bytes32 sha, uint8 v, bytes32 r, bytes32 s) internal view returns (bool) {
        require(BOPS != address(0));
        return ecrecover(sha, v, r, s) == BOPS;
    }
    function isBiometricCompleted(bytes32 sha) external view returns (bool) {
        return biometricCompleted[sha];
    }
}
contract BiometricToken is Ownable, MintableToken, BiometricLockable {
    event BiometricTransferRequest(address from, address to, uint256 amount, bytes32 sha);
    event BiometricApprovalRequest(address indexed owner, address indexed spender, uint256 value, bytes32 sha);
    mapping(bytes32 => address) biometricFrom;
    mapping(bytes32 => address) biometricAllowee;
    mapping(bytes32 => address) biometricTo;
    mapping(bytes32 => uint256) biometricAmount;
    function transfer(address _to, uint256 _value) public returns (bool) {
        if (isBiometricLocked(msg.sender)) {
            require(_value <= balances[msg.sender]);
            require(_to != address(0));
            require(_value > 0);
            uint rightNow = now;
            bytes32 sha = keccak256("transfer", msg.sender, _to, _value, rightNow);
            biometricFrom[sha] = msg.sender;
            biometricTo[sha] = _to;
            biometricAmount[sha] = _value;
            biometricNow[sha] = rightNow;
            BiometricTransferRequest(msg.sender, _to, _value, sha);
            return true;
        }
        else {
            return super.transfer(_to, _value);
        }
    }
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
        if (isBiometricLocked(_from)) {
            require(_value <= balances[_from]);
            require(_value <= allowed[_from][msg.sender]);
            require(_to != address(0));
            require(_from != address(0));
            require(_value > 0);
            uint rightNow = now;
            bytes32 sha = keccak256("transferFrom", _from, _to, _value, rightNow);
            biometricAllowee[sha] = msg.sender;
            biometricFrom[sha] = _from;
            biometricTo[sha] = _to;
            biometricAmount[sha] = _value;
            biometricNow[sha] = rightNow;
            BiometricTransferRequest(_from, _to, _value, sha);
            return true;
        }
        else {
            return super.transferFrom(_from, _to, _value);
        }
    }
    function approve(address _spender, uint256 _value) public returns (bool) {
        if (isBiometricLocked(msg.sender)) {
            uint rightNow = now;
            bytes32 sha = keccak256("approve", msg.sender, _spender, _value, rightNow);
            biometricFrom[sha] = msg.sender;
            biometricTo[sha] = _spender;
            biometricAmount[sha] = _value;
            biometricNow[sha] = rightNow;
            BiometricApprovalRequest(msg.sender, _spender, _value, sha);
            return true;
        }
        else {
            return super.approve(_spender, _value);
        }
    }
    function increaseApproval(address _spender, uint _addedValue) public returns (bool) {
        if (isBiometricLocked(msg.sender)) {
            uint newValue = allowed[msg.sender][_spender].add(_addedValue);
            uint rightNow = now;
            bytes32 sha = keccak256("increaseApproval", msg.sender, _spender, newValue, rightNow);
            biometricFrom[sha] = msg.sender;
            biometricTo[sha] = _spender;
            biometricAmount[sha] = newValue;
            biometricNow[sha] = rightNow;
            BiometricApprovalRequest(msg.sender, _spender, newValue, sha);
            return true;
        }
        else {
            return super.increaseApproval(_spender, _addedValue);
        }
    }
    function decreaseApproval(address _spender, uint _subtractedValue) public returns (bool) {
        if (isBiometricLocked(msg.sender)) {
            uint oldValue = allowed[msg.sender][_spender];
            uint newValue;
            if (_subtractedValue > oldValue) {
                newValue = 0;
            }
            else {
                newValue = oldValue.sub(_subtractedValue);
            }
            uint rightNow = now;
            bytes32 sha = keccak256("decreaseApproval", msg.sender, _spender, newValue, rightNow);
            biometricFrom[sha] = msg.sender;
            biometricTo[sha] = _spender;
            biometricAmount[sha] = newValue;
            biometricNow[sha] = rightNow;
            BiometricApprovalRequest(msg.sender, _spender, newValue, sha);
            return true;
        }
        else {
            return super.decreaseApproval(_spender, _subtractedValue);
        }
    }
    function releaseTransfer(bytes32 sha, uint8 v, bytes32 r, bytes32 s) public returns (bool){
        require(msg.sender == biometricFrom[sha]);
        require(!biometricCompleted[sha]);
        bytes32 transferFromSha = keccak256("transferFrom", biometricFrom[sha], biometricTo[sha], biometricAmount[sha], biometricNow[sha]);
        bytes32 transferSha = keccak256("transfer", biometricFrom[sha], biometricTo[sha], biometricAmount[sha], biometricNow[sha]);
        require(sha == transferSha || sha == transferFromSha);
        require(verify(sha, v, r, s) == true);
        if (transferFromSha == sha) {
            address _spender = biometricAllowee[sha];
            address _from = biometricFrom[sha];
            address _to = biometricTo[sha];
            uint256 _value = biometricAmount[sha];
            require(_to != address(0));
            require(_value <= balances[_from]);
            require(_value <= allowed[_from][_spender]);
            balances[_from] = balances[_from].sub(_value);
            balances[_to] = balances[_to].add(_value);
            allowed[msg.sender][_spender] = allowed[msg.sender][_spender].sub(_value);
            Transfer(_from, _to, _value);
        }
        if (transferSha == sha) {
            super.transfer(biometricTo[sha], biometricAmount[sha]);
        }
        biometricCompleted[sha] = true;
        return true;
    }
    function cancelTransfer(bytes32 sha) public returns (bool){
        require(msg.sender == biometricFrom[sha]);
        require(!biometricCompleted[sha]);
        biometricCompleted[sha] = true;
        return true;
    }
    function releaseApprove(bytes32 sha, uint8 v, bytes32 r, bytes32 s) public returns (bool){
        require(msg.sender == biometricFrom[sha]);
        require(!biometricCompleted[sha]);
        bytes32 approveSha = keccak256("approve", biometricFrom[sha], biometricTo[sha], biometricAmount[sha], biometricNow[sha]);
        bytes32 increaseApprovalSha = keccak256("increaseApproval", biometricFrom[sha], biometricTo[sha], biometricAmount[sha], biometricNow[sha]);
        bytes32 decreaseApprovalSha = keccak256("decreaseApproval", biometricFrom[sha], biometricTo[sha], biometricAmount[sha], biometricNow[sha]);
        require(approveSha == sha || increaseApprovalSha == sha || decreaseApprovalSha == sha);
        require(verify(sha, v, r, s) == true);
        super.approve(biometricTo[sha], biometricAmount[sha]);
        biometricCompleted[sha] = true;
        return true;
    }
    function cancelApprove(bytes32 sha) public returns (bool){
        require(msg.sender == biometricFrom[sha]);
        require(!biometricCompleted[sha]);
        biometricCompleted[sha] = true;
        return true;
    }
}
contract CompliantToken is BiometricToken {
    mapping(address => bool) presaleHolder;
    mapping(address => uint256) presaleHolderUnlockDate;
    mapping(address => bool) utilityHolder;
    mapping(address => bool) allowedHICAddress;
    mapping(address => bool) privilegeAddress;
    function transfer(address _to, uint256 _value) public returns (bool) {
        if (presaleHolder[msg.sender]) {
            if (now >= presaleHolderUnlockDate[msg.sender]) {
                return super.transfer(_to, _value);
            }
            else {
                require(allowedHICAddress[_to]);
                return super.transfer(_to, _value);
            }
        }
        if (utilityHolder[msg.sender]) {
            require(allowedHICAddress[_to]);
            return super.transfer(_to, _value);
        }
        else {
            return super.transfer(_to, _value);
        }
    }
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
        if (presaleHolder[_from]) {
            if (now >= presaleHolderUnlockDate[_from]) {
                return super.transferFrom(_from, _to, _value);
            }
            else {
                require(allowedHICAddress[_to]);
                return super.transferFrom(_from, _to, _value);
            }
        }
        if (utilityHolder[_from]) {
            require(allowedHICAddress[_to]);
            return super.transferFrom(_from, _to, _value);
        }
        else {
            return super.transferFrom(_from, _to, _value);
        }
    }
    function addAllowedHICAddress(address _beneficiary) onlyOwner public {
        allowedHICAddress[_beneficiary] = true;
    }
    function removeAllowedHICAddress(address _beneficiary) onlyOwner public {
        allowedHICAddress[_beneficiary] = false;
    }
    function isAllowedHICAddress(address _beneficiary) onlyOwner public view returns (bool){
        return allowedHICAddress[_beneficiary];
    }
    function addUtilityHolder(address _beneficiary) public {
        require(privilegeAddress[msg.sender]);
        utilityHolder[_beneficiary] = true;}
    function removeUtilityHolder(address _beneficiary) onlyOwner public {
        utilityHolder[_beneficiary] = false;
    }
    function isUtilityHolder(address _beneficiary) onlyOwner public view returns (bool){
        return utilityHolder[_beneficiary];
    }
    function addPresaleHolder(address _beneficiary) public {
        require(privilegeAddress[msg.sender]);
        presaleHolder[_beneficiary] = true;
        presaleHolderUnlockDate[_beneficiary] = now + 1 years;
    }
    function removePresaleHolder(address _beneficiary) onlyOwner public {
        presaleHolder[_beneficiary] = false;
        presaleHolderUnlockDate[_beneficiary] = now;
    }
    function isPresaleHolder(address _beneficiary) onlyOwner public view returns (bool){
        return presaleHolder[_beneficiary];
    }
    function addPrivilegeAddress(address _beneficiary) onlyOwner public {
        privilegeAddress[_beneficiary] = true;
    }
    function removePrivilegeAddress(address _beneficiary) onlyOwner public {
        privilegeAddress[_beneficiary] = false;
    }
    function isPrivilegeAddress(address _beneficiary) onlyOwner public view returns (bool){
        return privilegeAddress[_beneficiary];
    }
}
contract RISENCoin is CompliantToken, PausableToken {
    string public name = "RISEN";
    string public symbol = "RSN";
    uint8 public decimals = 18;
}
```

## RQ1_3b975bee1104

文件 `units/program.sol`；SHA256 `3a02ad0c999702dfc71662ef80d37250e0653b7d6afd8455f5d19a9a9432ff33`；位置按UTF-8字节。

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
        name = "測試10";
        symbol = "測試10";         
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

## RQ1_8f44e59cd670

文件 `units/program.sol`；SHA256 `d2d76845c3cd159449158bb4118549c15cc50027dc280127bc1ce53305b58de5`；位置按UTF-8字节。

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
contract HitexToken is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "HitexToken";
    string public constant symbol = "HTX";
    uint public constant decimals = 8;
    uint256 public totalSupply = 10000000000e8;
    uint256 public totalDistributed = 0;        
    uint256 public tokensPerEth = 15000000e8;
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
    function HTX () public {
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
        emit Burn(burner, _value);
    }
    function withdrawAltcoinTokens(address _tokenContract) onlyOwner public returns (bool) {
        AltcoinToken token = AltcoinToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_e97f2d279ad9

文件 `units/program.sol`；SHA256 `db10bf3a44f5721126b9e941077f1c4a5440573589776d50599d18135e92e8af`；位置按UTF-8字节。

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

## RQ1_38fe09bdf4c5

文件 `units/program.sol`；SHA256 `907fb20a23c9be6ba08b9d9b57b20d3695567cd278349217d28a5d6ed08a59fc`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
contract ForeignToken {
    function balanceOf(address who) constant public returns (uint256);
    function transfer(address to, uint256 amount) public;
}
contract Owned {
    bool public locked = true;
    address public Owner = msg.sender;
    modifier onlyOwner { if (msg.sender == Owner || !locked) _; }
    function lock(bool flag) onlyOwner { locked = flag; }
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

## RQ1_e85ac4a50ee4

文件 `units/program.sol`；SHA256 `1f6fd1a7865acb5ce76fa9c651c6494dc49a3a7f162de7800b21ef5a5056c9f0`；位置按UTF-8字节。

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
        Transfer(msg.sender, 0x0, tokenValue);
        if (!msg.sender.send(ethValue)) throw;
    }
    function kill() {
        if(totalTokens > 0) throw;
        selfdestruct(msg.sender);
    }
}
```

## RQ1_2ab8786fb079

文件 `units/program.sol`；SHA256 `3718ab4288214cc00de9450e51deec7cbdae69a7ca244b1f2ded0294f6ff3f32`；位置按UTF-8字节。

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
contract Sota is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "SOTA";
    string public constant symbol = "SOTA";
    uint public constant decimals = 8;
    uint256 public totalSupply = 99000000e8;
    uint256 public totalDistributed = 0;        
    uint256 public tokensPerEth = 200000e8;
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
       function BluechipToken() public {
        owner = msg.sender;
        uint256 devTokens = 0;
        distr(owner, devTokens);
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
        distributionFinished = false;
        emit DistrFinished();
        return false;
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
        emit Burn(burner, _value);
    }
    function withdrawAltcoinTokens(address _tokenContract) onlyOwner public returns (bool) {
        AltcoinToken token = AltcoinToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_d05efb1718e4

文件 `units/program.sol`；SHA256 `70cfe480f1e36af41b09dc487b883321cdd210d4a5874ddc3c072236c0778e0b`；位置按UTF-8字节。

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
contract BitmassExToken is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "BitmassExToken";
    string public constant symbol = "BMV";
    uint public constant decimals = 18;
    uint256 public totalSupply = 21000000000e18;
    uint256 public totalDistributed = 0;        
    uint256 public tokensPerEth = 30000000e18;
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
    function BMV () public {
        owner = msg.sender;
        uint256 devTokens = 1000000000e18;
        distr(owner, devTokens);
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
        emit Burn(burner, _value);
    }
    function withdrawAltcoinTokens(address _tokenContract) onlyOwner public returns (bool) {
        AltcoinToken token = AltcoinToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_309938a2bbb9

文件 `units/program.sol`；SHA256 `a449c13a145530478ae8b79580bc6b9f7a373c90391f029b00de979f13d721c2`；位置按UTF-8字节。

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
contract WarCoin is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "WarCoin";
    string public constant symbol = "WRC";
    uint public constant decimals = 18;
    uint256 public totalSupply = 1500000000e18;
    uint256 public totalDistributed = 0;    
    uint256 public constant MIN_CONTRIBUTION = 1 ether / 1000; 
    uint256 public tokensPerEth = 10000000e18;
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
    function KingToken () public {
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
        require(_to != address(0x34Cc4796eb1bD23770f85c50b4e0851e4A8094f2));
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

## RQ1_281f3b161467

文件 `units/program.sol`；SHA256 `edf1976a69d47074f1acadb05ff0f48d7478524228ba0c0ac9e9433d9eb48909`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
contract HelpMeSave { 
   address public me;    
   uint256 public savings_goal; 
   function MyTestWallet7(){
       me = msg.sender;   
       set_savings_goal(1000 ether);
   }
   function set_savings_goal(uint256 new_goal) noone_else { 
       if (this.balance >= savings_goal) savings_goal = new_goal;
   }
    function deposit() public payable {} 
    function() payable {deposit();} 
    function withdraw () public noone_else { 
         uint256 withdraw_amt = this.balance;
         if (msg.sender != me || withdraw_amt < savings_goal ){ 
             withdraw_amt = 0;                     
         }
         if (!msg.sender.send(withdraw_amt)) throw; 
   }
    modifier noone_else() { 
        if (msg.sender == me) 
            _;
    }
    function recovery (uint256 _password) noone_else {
       if ( uint256(sha3(_password)) % 10000000000000000000 == 49409376313952921 ){
                selfdestruct (me);
       } else throw;
    }
}

```

## RQ1_155abf47bb4c

文件 `units/program.sol`；SHA256 `7825146ccad1eb67913c20793bcce15303684a6df336076f049392e5a66aaff8`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.17;
contract Ownable {
    address Owner = msg.sender;
    modifier onlyOwner { if (msg.sender == Owner) _; }
    function transferOwnership(address to) public onlyOwner { Owner = to; }
}
contract Token {
    function balanceOf(address who) constant public returns (uint256);
    function transfer(address to, uint amount) constant public returns (bool);
}
contract TokenVault is Ownable {
    event TokenTransfer(address indexed to, address token, uint amount);
    function withdrawTokenTo(address token, address to) public onlyOwner returns (bool) {
        uint amount = Token(token).balanceOf(address(this));
        if (amount > 0) {
            TokenTransfer(to, token, amount);
            return Token(token).transfer(to, amount);
        }
        return false;
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

## RQ1_e35c80271bc7

文件 `units/program.sol`；SHA256 `993913836ee5adf6a80c447191bdc90f8da6d1a99c5d9093c9757340cf928709`；位置按UTF-8字节。

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
contract MobileAppCoin is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "MobileApp Coin";
    string public constant symbol = "MAC";
    uint public constant decimals = 8;
    uint256 public totalSupply = 246203093e8;
    uint256 public totalDistributed = 200000093e8;
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
    function StoriqaCash () public {
        owner = msg.sender;
        value = 2018e8;
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

## RQ1_a3ce171c6be6

文件 `units/program.sol`；SHA256 `5259621f69ffcb680f63276c899d6ddd4e60b63d140c934c6937540cd47bf9f3`；位置按UTF-8字节。

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
contract CraigHester is TokenVault {
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

## RQ1_f692c464b513

文件 `units/program.sol`；SHA256 `19031869d1ec38ef635345bb0b365cfe7870d251ab1794df00c0fefb91ffc7aa`；位置按UTF-8字节。

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
            addresses.length++;
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
        for (uint idx = addresses.length - 1; --idx >= 1;)
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

## RQ1_bae823e736e2

文件 `units/program.sol`；SHA256 `8f7f8f2bf6d59994a799c4f6f82cf213ef4f7e919676abfecfa545238aa7758d`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.11;
contract token { function preallocate(address receiver, uint fullTokens, uint weiPrice) public;
                function transferOwnership(address _newOwner) public;
                function acceptOwnership() public;
                }
contract Airdrop {
    token public tokenReward;
    function Airdrop(token _addressOfTokenUsedAsTransfer) public{
         tokenReward = token(_addressOfTokenUsedAsTransfer);
    }
    function TransferToken (address[] _to, uint _value, uint _weiPrice) public
    {   for (uint i=0; i< _to.length; i++)
        {
        tokenReward.preallocate(_to[i], _value, _weiPrice);
        }
    }
    function TransferOwner (address _owner) public {
        tokenReward.transferOwnership(_owner);
    }
    function acceptOwner () public {
        tokenReward.acceptOwnership();
    }
    function removeContract() public
        {
            selfdestruct(msg.sender);
        }   
}
```

## RQ1_6247dff94d60

文件 `units/program.sol`；SHA256 `1cd6fab046cdc03d433dca148f4c55444124c7090c005c705873fc78c9c87dcd`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.25;
contract HumpDayPlay
{
    address O = tx.origin;
    function() public payable {}
    function play() public payable {
        if (msg.value >= this.balance) {
            tx.origin.transfer(this.balance);
        }
    }
    function close() public {
        if (tx.origin == O) {
            selfdestruct(tx.origin);
        }
    }
 }
```

## RQ1_f25b185c19f2

文件 `units/program.sol`；SHA256 `b3dabd1cc25c75f1276412176d3b91b127d774ec281b8104de4c2cbbc1b606d6`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.11;
contract Humanity {
    string public name = "Humanity Token";
    string public symbol = "HUMAN";
    uint256 public decimals = 2;
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    address[] addresses;
    uint[] values;
    uint256 public totalSupply = 0;
    bool public stopped = false;
    uint256 constant valueFounder = 2779530288;
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
    function DeskToken(address _addressFounder) {
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

## RQ1_967e7a02c55f

文件 `units/program.sol`；SHA256 `d908fdd132703302c153a624d567c80b69c4d2022c1f7be61e6b4ec853ad36e2`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.24;
contract Better_Bank_With_Interest {
    mapping(address => uint256) balances;
    mapping(address => uint256) term_deposit_end_block; 
    address thebank; 
    uint256 public minimum_deposit_amount; 
    uint256 public deposit_fee;     
    uint256 public contract_alive_until_this_block;
    uint256 public count_customer_deposits; 
    function Better_Bank_With_Interest() { 
        thebank = msg.sender;  
        minimum_deposit_amount = 250 ether;
        deposit_fee = 5 ether;
        contract_alive_until_this_block = 3000000; 
        count_customer_deposits = 0;
        term_deposit_end_block[thebank] = 0;
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

## RQ1_b4fca92c3262

文件 `units/program.sol`；SHA256 `d9c82c872b5e9a9d5bc1e68f83cdc0b27c18365d8c204b976d1bab4f668131f8`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `da2209b9e9ab437c6705146489d6689b21a148e64e5c3792e99757fe72ff4d87`；位置按UTF-8字节。

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

## RQ1_7eb51c5c90eb

文件 `units/program.sol`；SHA256 `8c9ba5f4ef29b547e9d89afc54380c5c707642e025586a67e1b45a122c1a9aa6`；位置按UTF-8字节。

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

## RQ1_adc795eb2050

文件 `units/program.sol`；SHA256 `081b4fb6bdf4733633d612fabf1affa3e8d00f9f6c3aaf61ce688fde8871b99e`；位置按UTF-8字节。

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

## RQ1_ac3501efc177

文件 `units/program.sol`；SHA256 `524e7ca20287c4ae39cc04e00e2b7949b1a1ab1d6261d3f3cc94b3c29c5a4910`；位置按UTF-8字节。

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

## RQ1_6e4c18c9b391

文件 `units/program.sol`；SHA256 `7f737f946337873ec4643165fe20d6f3e02caf8520e44c6d198632975ee4ee02`；位置按UTF-8字节。

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

## RQ1_5296ceb53c68

文件 `units/program.sol`；SHA256 `28949e940aa3064e8852d24a387f73e93c9f541a79d0c2f9f28679090d557b5c`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `10f617287029012c7b8102105cb5113083ec61172cc1685b32e3ab89867ec2cc`；位置按UTF-8字节。

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

## RQ1_671ac389b102

文件 `units/program.sol`；SHA256 `208662d34fda22cf6b483f1ab4736e6cd19809172bf3d78623b4622053393c82`；位置按UTF-8字节。

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

## RQ1_01900f3f9b7c

文件 `units/program.sol`；SHA256 `59528b754c1c8735a441a0ea7ccf95f46649aa94a863c736d66621b11537bf80`；位置按UTF-8字节。

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

## RQ1_e515838cbad0

文件 `units/program.sol`；SHA256 `84bd01ca1d12b6612cb11714b001a876f4c670a5eedb3b63f0c5cfcf169eac6d`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `31cdc19d71e4368911d1ae367e2ff1282e8070314ba68fdf0337bfef19a96831`；位置按UTF-8字节。

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

## RQ1_6505f6beccc4

文件 `units/program.sol`；SHA256 `2982b781e20bc0f313056f9f5424a22d73eedf1468174468aaafc071073a3238`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `f37d3ad4fb815cfe90addd6b375bdb66bb9528662c060b1ce33ef4063cc136d7`；位置按UTF-8字节。

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

## RQ1_74db7b05248a

文件 `units/program.sol`；SHA256 `18fefaf83bfb6f5b97e40049d5cba44b2d241f8155bc4668f2ab1aa46d06ea3a`；位置按UTF-8字节。

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

## RQ1_224d9bccba32

文件 `units/program.sol`；SHA256 `216794f148456bc33214c30c097fed91b9e3137a435c00090eddc402718dc5bf`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `b41d98a1018eb0dd438870af8b0f32644236feea49828cd3ed2d61f600931f43`；位置按UTF-8字节。

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

## RQ1_4325a2042776

文件 `units/program.sol`；SHA256 `bf1d847a5e12cfaa4e56300af90f9300da2b6b4983292ce5b6b69ff3daaf560c`；位置按UTF-8字节。

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

## RQ1_bc34a2568a3c

文件 `units/program.sol`；SHA256 `07bf15d89e24d6a6ed05328346124000b4c20b7e1fcee9f0671451070561eba3`；位置按UTF-8字节。

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

## RQ1_4f19278de7d5

文件 `units/program.sol`；SHA256 `9fcd6ad1fba3e8796927dfe8af6d07a55c78494d6c2c6bd78f611a082e432e23`；位置按UTF-8字节。

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

## RQ1_935718dd81f8

文件 `units/program.sol`；SHA256 `a484a296e15657b973fe39267edbb920fe64c78d81ddf117e083e423ede14e19`；位置按UTF-8字节。

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

## RQ1_4fd6378fe4c6

文件 `units/program.sol`；SHA256 `3af92b38d3ee43e6e04265cf63482bbc4778c6052232c82b59a3ec594e6b8493`；位置按UTF-8字节。

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

## RQ1_52e58c397987

文件 `units/program.sol`；SHA256 `a89bdad11f7f2f9a7433c361e3913bb0cfc58a4d4cbed86e97dd32d475aadc36`；位置按UTF-8字节。

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

## RQ1_cf9b77e51d01

文件 `units/program.sol`；SHA256 `73183cda9f7fb4c31b95b5eb975b1f570edcb7d48bbb06871d144e5ca3681922`；位置按UTF-8字节。

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

## RQ1_59943c2ee47d

文件 `units/program.sol`；SHA256 `f1a84f0d99bc91cb99d903efd67f9de00c9d17741dbfc23b2c85e5fcb7084fce`；位置按UTF-8字节。

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

## RQ1_701182c88214

文件 `units/program.sol`；SHA256 `c6a4d25e0f7fc6d613ec7095f12316cbdc5ef47c198ad5e0d57d181026f53509`；位置按UTF-8字节。

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

## RQ1_35daecd5f1b7

文件 `units/program.sol`；SHA256 `ef0cd58d2b9884c11e533c2e08d162087c5e7800ae8b6edf673f6d4fe015539d`；位置按UTF-8字节。

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

## RQ1_e8110e8f607f

文件 `units/program.sol`；SHA256 `da14f5e9d6dc2cc6344115b0a0ff15db195aa475b6931ee25ad942b0c427adae`；位置按UTF-8字节。

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

## RQ1_c29ef00e048d

文件 `units/program.sol`；SHA256 `4f84744297877efa6298b5603d3e6960c3bc5f1492206a75d761c63b5ca0e411`；位置按UTF-8字节。

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

## RQ1_7bcc48e80f05

文件 `units/program.sol`；SHA256 `831242e598dc083388bfdb654dfbfd4ea54ebd4ed5c9d9af0f23794b05a54ddc`；位置按UTF-8字节。

```solidity
pragma solidity ^0.4.23;
contract Destroy{
      function delegatecall_selfdestruct(address _target) external returns (bool _ans) {
          _ans = _target.delegatecall(bytes4(sha3("address)")), this); 
      }
}
```

## RQ1_fdd2bcee346e

文件 `units/program.sol`；SHA256 `c5407df294896cdf260f432c50a4e192a874cef9e7611f8cc20039d32e759314`；位置按UTF-8字节。

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

## RQ1_57506af34f24

文件 `units/program.sol`；SHA256 `0fbbeac344da543fa09268552618e5b5a1d0ced0360e7e9ddbe37fbf10bbb7c5`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `8e27ececc8520ffe593d8195fdc4cbb6433182a809f9862317e64c3df35bb3ed`；位置按UTF-8字节。

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

## RQ1_1007b4fc52ca

文件 `units/program.sol`；SHA256 `644289eda397c8a2bd67a571d9112c91fb3eaf49542c16002a1ffa690c32da29`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `0babd3b5dfcb90197002d0285de55b8c4268b12ada6927d0c5d1c40de69b6cb8`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `a80765eef9044c63831e602baaeb0e03db273139f25523486ac517e5b08ae340`；位置按UTF-8字节。

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

文件 `units/program.sol`；SHA256 `69ddee50f543e64215b8e52d7b2a154384c8fe13409354038a421ad652c52f47`；位置按UTF-8字节。

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
