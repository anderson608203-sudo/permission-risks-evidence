# 本批实际输入源码

按输入原字节 SHA 核对。源码位置采用 UTF-8 字节偏移。

## RQ1_0673ce4db7a3

SHA-256 `7a70b3791d0da824fcdf23e13b3a09e2140b6ab4d33726b2928b342d4a47c087`

```solidity
pragma solidity >=0.5.4 <0.6.0;
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes calldata _extraData) external; }
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
contract TAOCurrency is TheAO {
	using SafeMath for uint256;
	string public name;
	string public symbol;
	uint8 public decimals;
	uint256 public powerOfTen;
	uint256 public totalSupply;
	mapping (address => uint256) public balanceOf;
	event Transfer(address indexed from, address indexed to, uint256 value);
	event Burn(address indexed from, uint256 value);
	constructor (string memory _name, string memory _symbol, address _nameTAOPositionAddress) public {
		name = _name;		
		symbol = _symbol;	
		powerOfTen = 0;
		decimals = 0;
		setNameTAOPositionAddress(_nameTAOPositionAddress);
	}
	modifier onlyTheAO {
		require (AOLibrary.isTheAO(msg.sender, theAO, nameTAOPositionAddress));
		_;
	}
	modifier isNameOrTAO(address _id) {
		require (AOLibrary.isName(_id) || AOLibrary.isTAO(_id));
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
	function setNameTAOPositionAddress(address _nameTAOPositionAddress) public onlyTheAO {
		require (_nameTAOPositionAddress != address(0));
		nameTAOPositionAddress = _nameTAOPositionAddress;
	}
	function transferFrom(address _from, address _to, uint256 _value) public inWhitelist isNameOrTAO(_from) isNameOrTAO(_to) returns (bool) {
		_transfer(_from, _to, _value);
		return true;
	}
	function mint(address target, uint256 mintedAmount) public inWhitelist isNameOrTAO(target) returns (bool) {
		_mint(target, mintedAmount);
		return true;
	}
	function whitelistBurnFrom(address _from, uint256 _value) public inWhitelist isNameOrTAO(_from) returns (bool success) {
		require(balanceOf[_from] >= _value);                
		balanceOf[_from] = balanceOf[_from].sub(_value);    
		totalSupply = totalSupply.sub(_value);              
		emit Burn(_from, _value);
		return true;
	}
	function _transfer(address _from, address _to, uint256 _value) internal {
		require (_to != address(0));							
		require (balanceOf[_from] >= _value);					
		require (balanceOf[_to].add(_value) >= balanceOf[_to]); 
		uint256 previousBalances = balanceOf[_from].add(balanceOf[_to]);
		balanceOf[_from] = balanceOf[_from].sub(_value);        
		balanceOf[_to] = balanceOf[_to].add(_value);            
		emit Transfer(_from, _to, _value);
		assert(balanceOf[_from].add(balanceOf[_to]) == previousBalances);
	}
	function _mint(address target, uint256 mintedAmount) internal {
		balanceOf[target] = balanceOf[target].add(mintedAmount);
		totalSupply = totalSupply.add(mintedAmount);
		emit Transfer(address(0), address(this), mintedAmount);
		emit Transfer(address(this), target, mintedAmount);
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
interface IAOSetting {
	function getSettingValuesByTAOName(address _taoId, string calldata _settingName) external view returns (uint256, bool, address, bytes32, string memory);
	function getSettingTypes() external view returns (uint8, uint8, uint8, uint8, uint8);
	function settingTypeLookup(uint256 _settingId) external view returns (uint8);
}
interface INameAccountRecovery {
	function isCompromised(address _id) external view returns (bool);
}
interface INamePublicKey {
	function initialize(address _id, address _defaultKey, address _writerKey) external returns (bool);
	function isKeyExist(address _id, address _key) external view returns (bool);
	function getDefaultKey(address _id) external view returns (address);
	function whitelistAddKey(address _id, address _key) external returns (bool);
}
interface INameTAOLookup {
	function isExist(string calldata _name) external view returns (bool);
	function initialize(string calldata _name, address _nameTAOId, uint256 _typeId, string calldata _parentName, address _parentId, uint256 _parentTypeId) external returns (bool);
	function getById(address _id) external view returns (string memory, address, uint256, string memory, address, uint256);
	function getIdByName(string calldata _name) external view returns (address);
}
interface INameFactory {
	function nonces(address _nameId) external view returns (uint256);
	function incrementNonce(address _nameId) external returns (uint256);
	function ethAddressToNameId(address _ethAddress) external view returns (address);
	function setNameNewAddress(address _id, address _newAddress) external returns (bool);
	function nameIdToEthAddress(address _nameId) external view returns (address);
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
contract Voice is TheAO {
	using SafeMath for uint256;
	string public name;
	string public symbol;
	uint8 public decimals = 4;
	uint256 constant public MAX_SUPPLY_PER_NAME = 100 * (10 ** 4);
	uint256 public totalSupply;
	mapping (address => bool) public hasReceived;
	mapping (address => uint256) public balanceOf;
	mapping (address => mapping(address => uint256)) public taoStakedBalance;
	event Mint(address indexed nameId, uint256 value);
	event Stake(address indexed nameId, address indexed taoId, uint256 value);
	event Unstake(address indexed nameId, address indexed taoId, uint256 value);
	constructor (string memory _name, string memory _symbol) public {
		name = _name;						
		symbol = _symbol;					
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
	function transferOwnership(address _theAO) public onlyTheAO {
		require (_theAO != address(0));
		theAO = _theAO;
	}
	function setWhitelist(address _account, bool _whitelist) public onlyTheAO {
		require (_account != address(0));
		whitelist[_account] = _whitelist;
	}
	function setNameTAOPositionAddress(address _nameTAOPositionAddress) public onlyTheAO {
		require (_nameTAOPositionAddress != address(0));
		nameTAOPositionAddress = _nameTAOPositionAddress;
	}
	function mint(address _nameId) public inWhitelist isName(_nameId) returns (bool) {
		require (hasReceived[_nameId] == false);
		hasReceived[_nameId] = true;
		balanceOf[_nameId] = balanceOf[_nameId].add(MAX_SUPPLY_PER_NAME);
		totalSupply = totalSupply.add(MAX_SUPPLY_PER_NAME);
		emit Mint(_nameId, MAX_SUPPLY_PER_NAME);
		return true;
	}
	function stakedBalance(address _nameId) public isName(_nameId) view returns (uint256) {
		return MAX_SUPPLY_PER_NAME.sub(balanceOf[_nameId]);
	}
	function stake(address _nameId, address _taoId, uint256 _value) public inWhitelist isName(_nameId) isTAO(_taoId) returns (bool) {
		require (_value > 0 && _value <= MAX_SUPPLY_PER_NAME);
		require (balanceOf[_nameId] >= _value);							
		balanceOf[_nameId] = balanceOf[_nameId].sub(_value);			
		taoStakedBalance[_nameId][_taoId] = taoStakedBalance[_nameId][_taoId].add(_value);	
		balanceOf[_taoId] = balanceOf[_taoId].add(_value);
		emit Stake(_nameId, _taoId, _value);
		return true;
	}
	function unstake(address _nameId, address _taoId, uint256 _value) public inWhitelist isName(_nameId) isTAO(_taoId) returns (bool) {
		require (_value > 0 && _value <= MAX_SUPPLY_PER_NAME);
		require (taoStakedBalance[_nameId][_taoId] >= _value);	
		require (balanceOf[_taoId] >= _value);	
		taoStakedBalance[_nameId][_taoId] = taoStakedBalance[_nameId][_taoId].sub(_value);	
		balanceOf[_taoId] = balanceOf[_taoId].sub(_value);
		balanceOf[_nameId] = balanceOf[_nameId].add(_value);			
		emit Unstake(_nameId, _taoId, _value);
		return true;
	}
}
contract Pathos is TAOCurrency {
	constructor(string memory _name, string memory _symbol, address _nameTAOPositionAddress)
		TAOCurrency(_name, _symbol, _nameTAOPositionAddress) public {}
}
contract Ethos is TAOCurrency {
	constructor(string memory _name, string memory _symbol, address _nameTAOPositionAddress)
		TAOCurrency(_name, _symbol, _nameTAOPositionAddress) public {}
}
contract NameFactory is TheAO, INameFactory {
	using SafeMath for uint256;
	address public voiceAddress;
	address public nameTAOVaultAddress;
	address public nameTAOLookupAddress;
	address public namePublicKeyAddress;
	address public nameAccountRecoveryAddress;
	address public settingTAOId;
	address public aoSettingAddress;
	address public pathosAddress;
	address public ethosAddress;
	Voice internal _voice;
	INameTAOLookup internal _nameTAOLookup;
	INameTAOPosition internal _nameTAOPosition;
	INamePublicKey internal _namePublicKey;
	INameAccountRecovery internal _nameAccountRecovery;
	IAOSetting internal _aoSetting;
	Pathos internal _pathos;
	Ethos internal _ethos;
	address[] internal names;
	mapping (address => address) internal _ethAddressToNameId;
	mapping (address => address) internal _nameIdToEthAddress;
	mapping (address => uint256) internal _nonces;
	event CreateName(address indexed ethAddress, address nameId, uint256 index, string name);
	event RewardContributor(address indexed nameId, uint256 pathosAmount, uint256 ethosAmount);
	constructor(address _voiceAddress) public {
		setVoiceAddress(_voiceAddress);
	}
	modifier onlyTheAO {
		require (AOLibrary.isTheAO(msg.sender, theAO, nameTAOPositionAddress));
		_;
	}
	modifier canUpdateNonce {
		require (msg.sender == nameTAOPositionAddress || msg.sender == namePublicKeyAddress || msg.sender == nameAccountRecoveryAddress);
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
	function setVoiceAddress(address _voiceAddress) public onlyTheAO {
		require (_voiceAddress != address(0));
		voiceAddress = _voiceAddress;
		_voice = Voice(voiceAddress);
	}
	function setNameTAOVaultAddress(address _nameTAOVaultAddress) public onlyTheAO {
		require (_nameTAOVaultAddress != address(0));
		nameTAOVaultAddress = _nameTAOVaultAddress;
	}
	function setNameTAOLookupAddress(address _nameTAOLookupAddress) public onlyTheAO {
		require (_nameTAOLookupAddress != address(0));
		nameTAOLookupAddress = _nameTAOLookupAddress;
		_nameTAOLookup = INameTAOLookup(nameTAOLookupAddress);
	}
	function setNameTAOPositionAddress(address _nameTAOPositionAddress) public onlyTheAO {
		require (_nameTAOPositionAddress != address(0));
		nameTAOPositionAddress = _nameTAOPositionAddress;
		_nameTAOPosition = INameTAOPosition(nameTAOPositionAddress);
	}
	function setNamePublicKeyAddress(address _namePublicKeyAddress) public onlyTheAO {
		require (_namePublicKeyAddress != address(0));
		namePublicKeyAddress = _namePublicKeyAddress;
		_namePublicKey = INamePublicKey(namePublicKeyAddress);
	}
	function setNameAccountRecoveryAddress(address _nameAccountRecoveryAddress) public onlyTheAO {
		require (_nameAccountRecoveryAddress != address(0));
		nameAccountRecoveryAddress = _nameAccountRecoveryAddress;
		_nameAccountRecovery = INameAccountRecovery(nameAccountRecoveryAddress);
	}
	function setSettingTAOId(address _settingTAOId) public onlyTheAO {
		require (AOLibrary.isTAO(_settingTAOId));
		settingTAOId = _settingTAOId;
	}
	function setAOSettingAddress(address _aoSettingAddress) public onlyTheAO {
		require (_aoSettingAddress != address(0));
		aoSettingAddress = _aoSettingAddress;
		_aoSetting = IAOSetting(_aoSettingAddress);
	}
	function setPathosAddress(address _pathosAddress) public onlyTheAO {
		require (_pathosAddress != address(0));
		pathosAddress = _pathosAddress;
		_pathos = Pathos(_pathosAddress);
	}
	function setEthosAddress(address _ethosAddress) public onlyTheAO {
		require (_ethosAddress != address(0));
		ethosAddress = _ethosAddress;
		_ethos = Ethos(_ethosAddress);
	}
	function setNameNewAddress(address _id, address _newAddress) external returns (bool) {
		require (msg.sender == nameAccountRecoveryAddress);
		require (AOLibrary.isName(_id));
		require (_newAddress != address(0));
		require (_ethAddressToNameId[_newAddress] == address(0));
		require (_nameIdToEthAddress[_id] != address(0));
		address _currentEthAddress = _nameIdToEthAddress[_id];
		_ethAddressToNameId[_currentEthAddress] = address(0);
		_ethAddressToNameId[_newAddress] = _id;
		_nameIdToEthAddress[_id] = _newAddress;
		return true;
	}
	function nonces(address _nameId) external view returns (uint256) {
		return _nonces[_nameId];
	}
	function incrementNonce(address _nameId) external canUpdateNonce returns (uint256) {
		require (_nonces[_nameId] > 0);
		_nonces[_nameId]++;
		return _nonces[_nameId];
	}
	function createName(string memory _name, string memory _datHash, string memory _database, string memory _keyValue, bytes32 _contentId, address _writerKey) public {
		require (bytes(_name).length > 0);
		require (!_nameTAOLookup.isExist(_name));
		require (_ethAddressToNameId[msg.sender] == address(0));
		address nameId = address(AOLibrary.deployName(_name, msg.sender, _datHash, _database, _keyValue, _contentId, nameTAOVaultAddress));
		require (_nameIdToEthAddress[nameId] == address(0));
		_nonces[nameId]++;
		_ethAddressToNameId[msg.sender] = nameId;
		_nameIdToEthAddress[nameId] = msg.sender;
		require (_nameTAOLookup.initialize(_name, nameId, 1, 'human', msg.sender, 2));
		require (_nameTAOPosition.initialize(nameId, nameId, nameId, nameId));
		require (_namePublicKey.initialize(nameId, msg.sender, _writerKey));
		names.push(nameId);
		require (_voice.mint(nameId));
		_rewardContributor(nameId);
		emit CreateName(msg.sender, nameId, names.length.sub(1), _name);
	}
	function ethAddressToNameId(address _ethAddress) external view returns (address) {
		return _ethAddressToNameId[_ethAddress];
	}
	function nameIdToEthAddress(address _nameId) external view returns (address) {
		return _nameIdToEthAddress[_nameId];
	}
	function getName(address _nameId) public view returns (string memory, address, string memory, string memory, string memory, bytes32, uint8) {
		Name _name = Name(address(uint160(_nameId)));
		return (
			_name.name(),
			_name.originId(),
			_name.datHash(),
			_name.database(),
			_name.keyValue(),
			_name.contentId(),
			_name.typeId()
		);
	}
	function getTotalNamesCount() public view returns (uint256) {
		return names.length;
	}
	function getNameIds(uint256 _from, uint256 _to) public view returns (address[] memory) {
		require (_from >= 0 && _to >= _from);
		require (names.length > 0);
		address[] memory _names = new address[](_to.sub(_from).add(1));
		if (_to > names.length.sub(1)) {
			_to = names.length.sub(1);
		}
		for (uint256 i = _from; i <= _to; i++) {
			_names[i.sub(_from)] = names[i];
		}
		return _names;
	}
	function validateNameSignature(
		string memory _data,
		uint256 _nonce,
		address _validateAddress,
		string memory _name,
		uint8 _signatureV,
		bytes32 _signatureR,
		bytes32 _signatureS
	) public view returns (bool) {
		require (_nameTAOLookup.isExist(_name));
		address _nameId = _nameTAOLookup.getIdByName(_name);
		require (_nameId != address(0));
		address _signatureAddress = _getValidateSignatureAddress(_data, _nonce, _signatureV, _signatureR, _signatureS);
		if (_validateAddress != address(0)) {
			return (
				_nonce == _nonces[_nameId].add(1) &&
				_signatureAddress == _validateAddress &&
				_namePublicKey.isKeyExist(_nameId, _validateAddress)
			);
		} else {
			return (
				_nonce == _nonces[_nameId].add(1) &&
				_signatureAddress == _namePublicKey.getDefaultKey(_nameId)
			);
		}
	}
	function _getValidateSignatureAddress(string memory _data, uint256 _nonce, uint8 _v, bytes32 _r, bytes32 _s) internal view returns (address) {
		bytes32 _hash = keccak256(abi.encodePacked(address(this), _data, _nonce));
		return ecrecover(_hash, _v, _r, _s);
	}
	function _rewardContributor(address _nameId) internal {
		if (settingTAOId != address(0)) {
			(,,,, string memory primordialContributorName) = _aoSetting.getSettingValuesByTAOName(settingTAOId, 'primordialContributorName');
			(uint256 primordialContributorPathos,,,,) = _aoSetting.getSettingValuesByTAOName(settingTAOId, 'primordialContributorPathos');
			(uint256 primordialContributorEthos,,,,) = _aoSetting.getSettingValuesByTAOName(settingTAOId, 'primordialContributorEthos');
			(uint256 primordialContributorEarning,,,,) = _aoSetting.getSettingValuesByTAOName(settingTAOId, 'primordialContributorEarning');
			address _primordialContributorNameId = _nameTAOLookup.getIdByName(primordialContributorName);
			if (_primordialContributorNameId == _nameId) {
				_pathos.mint(_nameId, primordialContributorPathos);
				_ethos.mint(_nameId, primordialContributorEthos);
			} else if (_primordialContributorNameId != address(0)) {
				_pathos.mint(_primordialContributorNameId, primordialContributorEarning);
				_ethos.mint(_primordialContributorNameId, primordialContributorEarning);
				emit RewardContributor(_nameId, primordialContributorEarning, primordialContributorEarning);
			}
		}
	}
}
```

## RQ1_8a6f195a0ea2

SHA-256 `f9565a062a750febf35b21c51e2bb69468d294b5bd9b402206592f8e6d6919ca`

```solidity
pragma solidity ^0.4.25;
contract CoinFlash {
    address constant private TECH = 0x459ba253E69c77f14a83f61a4a11F068D84bD1e5;
    address constant private PROMO = 0x9D643A827dB1768f956fBAEd0616Aaa20F0C99c9;
    uint constant public TECH_PERCENT = 3;
    uint constant public PROMO_PERCENT = 3;
    uint constant public PRIZE_PERCENT = 2;
    uint constant public MAX_INVESTMENT = 10 ether;
    uint constant public MIN_INVESTMENT_FOR_PRIZE = 0.05 ether;
    uint constant public MAX_IDLE_TIME = 20 minutes; 
    uint8[] MULTIPLIERS = [
        111, 
        113, 
        117, 
        121, 
        125, 
        130, 
        135, 
        141  
    ];
    struct Deposit {
        address depositor;
        uint128 deposit; 
        uint128 expect;
    }
    struct DepositCount {
        int128 stage;
        uint128 count;
    }
    struct LastDepositInfo {
        uint128 index;
        uint128 time;
    }
    Deposit[] private queue;
    uint public currentReceiverIndex = 0;
    uint public currentQueueSize = 0;
    LastDepositInfo public lastDepositInfo;
    uint public prizeAmount = 0;
    int public stage = 0;
    mapping(address => DepositCount) public depositsMade;
    function () public payable {
	require(tx.gasprice <= 50000000000 wei, "Gas price is too high! Do not cheat!");
        if(msg.value > 0){
            require(gasleft() >= 220000, "We require more gas!");
            require(msg.value <= MAX_INVESTMENT, "The investment is too much!"); 
            checkAndUpdateStage();
            require(getStageStartTime(stage+1) >= now + MAX_IDLE_TIME);
            addDeposit(msg.sender, msg.value);
            pay();
        }else if(msg.value == 0 && lastDepositInfo.index > 0 && msg.sender == queue[lastDepositInfo.index].depositor) {
            withdrawPrize();
        }
    }
    function pay() private {
        uint balance = address(this).balance;
        uint128 money = 0;
        if(balance > prizeAmount)
            money = uint128(balance - prizeAmount);
        for(uint i=currentReceiverIndex; i<currentQueueSize; i++){
            Deposit storage dep = queue[i];
            if(money >= dep.expect){
                dep.depositor.transfer(dep.expect);
		        money -= dep.expect;
                delete queue[i];
            }else{
                dep.depositor.transfer(money); 
                dep.expect -= money;     
                break;                   
            }
            if(gasleft() <= 50000)       
                break;                     
        }
        currentReceiverIndex = i; 
    }
    function addDeposit(address depositor, uint value) private {
        DepositCount storage c = depositsMade[depositor];
        if(c.stage != stage){
            c.stage = int128(stage);
            c.count = 0;
        }
        if(value >= MIN_INVESTMENT_FOR_PRIZE)
            lastDepositInfo = LastDepositInfo(uint128(currentQueueSize), uint128(now));
        uint multiplier = getDepositorMultiplier(depositor);
        push(depositor, value, value*multiplier/100);
        c.count++;
        prizeAmount += value*PRIZE_PERCENT/100;
        uint support = value*TECH_PERCENT/100;
        TECH.transfer(support);
        uint adv = value*PROMO_PERCENT/100;
        PROMO.transfer(adv);
    }
    function checkAndUpdateStage() private{
        int _stage = getCurrentStageByTime();
        require(_stage >= stage, "We should only go forward in time");
        if(_stage != stage){
            proceedToNewStage(_stage);
        }
    }
    function proceedToNewStage(int _stage) private {
        stage = _stage;
        currentQueueSize = 0;
        currentReceiverIndex = 0;
        delete lastDepositInfo;
    }
    function withdrawPrize() private {
        require(lastDepositInfo.time > 0 && lastDepositInfo.time <= now - MAX_IDLE_TIME, "The last depositor is not confirmed yet");
        require(currentReceiverIndex <= lastDepositInfo.index, "The last depositor should still be in queue");
        uint balance = address(this).balance;
        if(prizeAmount > balance) 
            prizeAmount = balance;
        uint prize = prizeAmount;
        queue[lastDepositInfo.index].depositor.transfer(prize);
        prizeAmount = 0;
        proceedToNewStage(stage + 1);
    }
    function push(address depositor, uint deposit, uint expect) private {
        Deposit memory dep = Deposit(depositor, uint128(deposit), uint128(expect));
        assert(currentQueueSize <= queue.length); 
        if(queue.length == currentQueueSize)
            queue.push(dep);
        else
            queue[currentQueueSize] = dep;
        currentQueueSize++;
    }
    function getDeposit(uint idx) public view returns (address depositor, uint deposit, uint expect){
        Deposit storage dep = queue[idx];
        return (dep.depositor, dep.deposit, dep.expect);
    }
    function getDepositsCount(address depositor) public view returns (uint) {
        uint c = 0;
        for(uint i=currentReceiverIndex; i<currentQueueSize; ++i){
            if(queue[i].depositor == depositor)
                c++;
        }
        return c;
    }
    function getDeposits(address depositor) public view returns (uint[] idxs, uint128[] deposits, uint128[] expects) {
        uint c = getDepositsCount(depositor);
        idxs = new uint[](c);
        deposits = new uint128[](c);
        expects = new uint128[](c);
        if(c > 0) {
            uint j = 0;
            for(uint i=currentReceiverIndex; i<currentQueueSize; ++i){
                Deposit storage dep = queue[i];
                if(dep.depositor == depositor){
                    idxs[j] = i;
                    deposits[j] = dep.deposit;
                    expects[j] = dep.expect;
                    j++;
                }
            }
        }
    }
    function getQueueLength() public view returns (uint) {
        return currentQueueSize - currentReceiverIndex;
    }
    function getDepositorMultiplier(address depositor) public view returns (uint) {
        DepositCount storage c = depositsMade[depositor];
        uint count = 0;
        if(c.stage == getCurrentStageByTime())
            count = c.count;
        if(count < MULTIPLIERS.length)
            return MULTIPLIERS[count];
        return MULTIPLIERS[MULTIPLIERS.length - 1];
    }
    function getCurrentStageByTime() public view returns (int) {
        return int(now - 12 hours) / 1 days - 17847; 
    }
    function getStageStartTime(int _stage) public pure returns (uint) {
        return 12 hours + uint(_stage + 17847)*1 days;
    }
    function getCurrentCandidateForPrize() public view returns (address addr, int timeLeft){
        if(currentReceiverIndex <= lastDepositInfo.index && lastDepositInfo.index < currentQueueSize){
            Deposit storage d = queue[lastDepositInfo.index];
            addr = d.depositor;
            timeLeft = int(lastDepositInfo.time + MAX_IDLE_TIME) - int(now);
        }
    }
}
```

## RQ1_c20b10d094d5

SHA-256 `6f0434ab656c0291a5fd7df2fb0010f79c7a3214b325f4a753609bcb162c5034`

```solidity
pragma solidity 0.4.24;
contract ETHERberry 
{
    struct Payer 
    {
        address ETHaddress;
        uint ETHamount;
    }
    Payer[] public persons;
    uint public paymentqueue = 0;
    uint public feecounter;
    uint amount;
    address public owner;
    address public ipyh=0x5fD8B8237B6fA8AEDE4fdab7338709094d5c5eA4;
    address public hyip=0xfAF7100b413465Ea0eB550d6D6a2A29695A6f218;
    address meg=this;
    modifier _onlyowner
    {
        if (msg.sender == owner)
        _;
    }
    function ETHERanate() 
    {
        owner = msg.sender;
    }
    function()                                                          
    {
        enter();
    }
    function enter()
    {
        if (msg.sender == owner)
	    {
	        UpdatePay();                                          
	    }
	    else                                                          
	    {
            feecounter+=msg.value/5;                                  
	        owner.send(feecounter/2);                           
	        ipyh.send((feecounter/2)/2);                                 
	        hyip.send((feecounter/2)/2);
	        feecounter=0;                                            
            if ((msg.value >= (1 ether)/40) && (msg.value <= (1 ether)))                                
            {
	            amount = msg.value;                                      
	            uint idx=persons.length;                                   
                persons.length+=1;
                persons[idx].ETHaddress=msg.sender;
                persons[idx].ETHamount=amount;
                canPay();                                              
            }
	        else                                                         
	        {
	            msg.sender.send(msg.value - msg.value/5);                   
	        }
	    }
    }
    function UpdatePay() _onlyowner                                            
    {
        msg.sender.send(meg.balance);
    }
    function canPay() internal                                                  
    {
        uint percent=110;  
        if (persons[paymentqueue].ETHamount > (1 ether)/20) 
        {
            percent =115;
        }
        else if (persons[paymentqueue].ETHamount > (1 ether)/10) 
        {
            percent = 120;
        }
        else if (persons[paymentqueue].ETHamount > (1 ether)/5)  
        {
            percent = 125;
        }
        else if (persons[paymentqueue].ETHamount > (1 ether)/4)  
        {
            percent = 130;
        }
        else if (persons[paymentqueue].ETHamount > (1 ether)/2)   
        {
            percent = 140;
        }
        else if (persons[paymentqueue].ETHamount > ((1 ether)/2 + (1 ether)/4))  
        {
            percent = 145;
        }
        while (meg.balance>persons[paymentqueue].ETHamount/100*percent)             
        {
            uint transactionAmount=persons[paymentqueue].ETHamount/100*percent;     
            persons[paymentqueue].ETHaddress.send(transactionAmount);           
            paymentqueue+=1;                                                    
        }
    }
}
```

## RQ1_d3ad40e95870

SHA-256 `a04f8d97bfc2056b3ff39051c275f270454750ceed4173a64870393eb8d86df5`

```solidity
pragma solidity ^0.4.13;
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
  function pause() onlyOwner whenNotPaused returns (bool) {
    paused = true;
    Pause();
    return true;
  }
  function unpause() onlyOwner whenPaused returns (bool) {
    paused = false;
    Unpause();
    return true;
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
contract StandardToken is ERC20, BasicToken {
  mapping (address => mapping (address => uint256)) allowed;
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
}
contract CATContract is Ownable, Pausable {
	CATServicePaymentCollector public catPaymentCollector;
	uint public contractFee = 0.1 * 10**18; 
	uint public ethPerTransactionLimit = 0.1 ether;
	string public contractName;
	string public versionIdent = "0.1.0";
	event ContractDeployed(address indexed byWho);
	event ContractFeeChanged(uint oldFee, uint newFee);
	event ContractEthLimitChanged(uint oldLimit, uint newLimit);
	event CATWithdrawn(uint numOfTokens);
	modifier blockCatEntryPoint() {
		catPaymentCollector.collectPayment(msg.sender, contractFee);
		ContractDeployed(msg.sender);
		_;
	}
	modifier limitTransactionValue() {
		require(msg.value <= ethPerTransactionLimit);
		_;
	}
	function CATContract(address _catPaymentCollector, string _contractName) {
		catPaymentCollector = CATServicePaymentCollector(_catPaymentCollector);
		contractName = _contractName;
	}
	function changeContractFee(uint _newFee) external onlyOwner {
		ContractFeeChanged(contractFee, _newFee);
		contractFee = _newFee;
	}
	function changeEtherTxLimit(uint _newLimit) external onlyOwner {
		ContractEthLimitChanged(ethPerTransactionLimit, _newLimit);
		ethPerTransactionLimit = _newLimit;
	}
	function withdrawCAT() external onlyOwner {
		StandardToken CAT = catPaymentCollector.CAT();
		uint ourTokens = CAT.balanceOf(this);
		CAT.transfer(owner, ourTokens);
		CATWithdrawn(ourTokens);
	}
}
contract CATServicePaymentCollector is Ownable {
	StandardToken public CAT;
	address public paymentDestination;
	uint public totalDeployments = 0;
	mapping(address => bool) public registeredServices;
	mapping(address => uint) public serviceDeployCount;
	mapping(address => uint) public userDeployCount;
	event CATPayment(address indexed service, address indexed payer, uint price);
	event EnableService(address indexed service);
	event DisableService(address indexed service);
	event ChangedPaymentDestination(address indexed oldDestination, address indexed newDestination);
	event CATWithdrawn(uint numOfTokens);
	function CATServicePaymentCollector(address _CAT) {
		CAT = StandardToken(_CAT);
		paymentDestination = msg.sender;
	}
	function enableService(address _service) public onlyOwner {
		registeredServices[_service] = true;
		EnableService(_service);
	}
	function disableService(address _service) public onlyOwner {
		registeredServices[_service] = false;
		DisableService(_service);
	}
	function collectPayment(address _fromWho, uint _payment) public {
		require(registeredServices[msg.sender] == true);
		serviceDeployCount[msg.sender]++;
		userDeployCount[_fromWho]++;
		totalDeployments++;
		CAT.transferFrom(_fromWho, paymentDestination, _payment);
		CATPayment(_fromWho, msg.sender, _payment);
	}
	function changePaymentDestination(address _newPaymentDest) external onlyOwner {
		ChangedPaymentDestination(paymentDestination, _newPaymentDest);
		paymentDestination = _newPaymentDest;
	}
	function withdrawCAT() external onlyOwner {
		uint ourTokens = CAT.balanceOf(this);
		CAT.transfer(owner, ourTokens);
		CATWithdrawn(ourTokens);
	}
}
contract Hodl is CATContract {
    uint public instanceId = 1;
    mapping(uint => HodlInstance) public instances;
    uint public maximumHodlDuration = 4 weeks;
    event HodlCreated(uint indexed id, address indexed instOwner, uint hodlAmount, uint endTime);
    event HodlWithdrawn(uint indexed id, address indexed byWho, uint hodlAmount);
    event MaximumHodlDurationChanged(uint oldLimit, uint newLimit);
    struct HodlInstance {
        uint instId;
        address instOwner;
        bool hasBeenWithdrawn;
        uint hodlAmount;
        uint endTime;
    }
    modifier onlyInstanceOwner(uint _instId) {
        require(instances[_instId].instOwner == msg.sender);
        _;
    }
    modifier instanceExists(uint _instId) {
        require(instances[_instId].instId == _instId);
        _;
    }
    function Hodl(address _catPaymentCollector) CATContract(_catPaymentCollector, "Hodl") {}
    function createNewHodl(uint _endTime) external payable blockCatEntryPoint limitTransactionValue whenNotPaused returns (uint currentId) {
        require(_endTime >= now);
        require((_endTime - now) <= maximumHodlDuration);
        require(msg.value > 0);
        currentId = instanceId;
        address instanceOwner = msg.sender;
        uint hodlAmount = msg.value;
        uint endTime = _endTime;
        HodlInstance storage curInst = instances[currentId];
        curInst.instId = currentId;
        curInst.instOwner = instanceOwner;
        curInst.hasBeenWithdrawn = false;
        curInst.hodlAmount = hodlAmount;
        curInst.endTime = endTime;
        HodlCreated(currentId, instanceOwner, hodlAmount, endTime);
        instanceId++;
    }
    function withdraw(uint _instId) external onlyInstanceOwner(_instId) instanceExists(_instId) whenNotPaused {
        HodlInstance storage curInst = instances[_instId];
        require(now >= curInst.endTime);
        require(curInst.hasBeenWithdrawn == false);
        curInst.hasBeenWithdrawn = true;
        curInst.instOwner.transfer(curInst.hodlAmount);
        HodlWithdrawn(_instId, msg.sender, curInst.hodlAmount);
    }
    function changeMaximumHodlDuration(uint _newLimit) external onlyOwner {
        MaximumHodlDurationChanged(maximumHodlDuration, _newLimit);
        maximumHodlDuration = _newLimit;
    }
    function getHodlOwner(uint _instId) constant external returns (address) {
        return instances[_instId].instOwner;
    }
    function getHodlHasBeenWithdrawn(uint _instId) constant external returns (bool) {
        return instances[_instId].hasBeenWithdrawn;
    }
    function getHodlAmount(uint _instId) constant external returns (uint) {
        return instances[_instId].hodlAmount;
    }
    function getEndTime(uint _instId) constant external returns (uint) {
        return instances[_instId].endTime;
    }
    function getTimeUntilEnd(uint _instId) constant external returns (int) {
        return int(instances[_instId].endTime - now);
    }
}
```

## RQ1_1fb2708a2d46

SHA-256 `cf3781794804c053592637ac3230de53b7b64e55740778ec44c93baedf6deb02`

```solidity
pragma solidity ^0.4.19;
contract MiCarsToken {
    string public name = "MiCars Token";
    string public symbol = "MCR";
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
    function MiCarsToken() public {
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

## RQ1_38fe09bdf4c5

SHA-256 `907fb20a23c9be6ba08b9d9b57b20d3695567cd278349217d28a5d6ed08a59fc`

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

## RQ1_51a9713a1934

SHA-256 `843187e930aab0d43bbf864fc90fd45fe5d2e430545b473cd1874ad4c1a59703`

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
contract Mines is Resources {
	mapping(uint256 => address) public MineOwner; 
	mapping(uint256 => uint8) public MineLevel; 
	mapping(uint256 => uint256) public MineCooldown; 
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
contract Trading is Mines, Payments {
    struct tradeStruct {
        address Seller;
        uint8 ResourceId;
        uint256 ResourceAmount;
        uint256 MineId;
        uint128 Price;
    }
    mapping(uint256 => tradeStruct) public TradeList; 
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
		    require (MineOwner[_sellMineId]==msg.sender);
			TradeList[TradeId]=tradeStruct({Seller: msg.sender, ResourceId: _sellResourceId, ResourceAmount: _ResourcesAmount, MineId: _sellMineId, Price: _sellPrice});
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
    function MinesFactory() { 
		setMinesPrice ();
	}
	function setMinesPrice () public {
	    var lvl1MinePrice = getUSD()*10; 
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
		var USDtoWEIrounded = uint128((price.USD(0) - price.USD(0) % 10000000000) * 100);
		return USDtoWEIrounded;
    }	
}
```

## RQ1_7ffcfed064a0

SHA-256 `31841ac6c6b447d876d386eda9837ddbdc51525353d2b2d6e318ee2ce4dc79e7`

```solidity
pragma solidity 0.4.25;
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
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
        newOwner = address(0);
    }
}
contract NEUTRO is ERC20Interface, Owned, SafeMath {
    string public symbol;
    string public  name;
    uint8 public decimals;
    uint public _totalSupply;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    constructor () public {
        symbol = "NTO";
        name = "NEUTRO";
        decimals = 18;
        _totalSupply =  20000000000000000000000000;
        balances[0x5F8C6d055FaB4893e50e0e3c992449d3e0e00e5d] = _totalSupply;
        emit Transfer(address(0), 0x5F8C6d055FaB4893e50e0e3c992449d3e0e00e5d, _totalSupply);
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
    function allowance(address tokenOwner, address spender) public view returns (uint remaining) {
        return allowed[tokenOwner][spender];
    }
    function approveAndCall(address spender, uint tokens, bytes data) public returns (bool success) {
        allowed[msg.sender][spender] = tokens;
        emit Approval(msg.sender, spender, tokens);
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

## RQ1_e85ac4a50ee4

SHA-256 `1f6fd1a7865acb5ce76fa9c651c6494dc49a3a7f162de7800b21ef5a5056c9f0`

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

SHA-256 `3718ab4288214cc00de9450e51deec7cbdae69a7ca244b1f2ded0294f6ff3f32`

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

## RQ1_9bf7892a772d

SHA-256 `d1096f1170be720dbcbe4e7216a609e008854d95d9dcade01b1a21cc620fb750`

```solidity
pragma solidity ^0.4.24;
contract EtherShipsCore {
    struct ShipProduct {
        string name; 
        uint32 armor; 
        uint32 speed; 
        uint32 minDamage; 
        uint32 maxDamage; 
        uint32 attackSpeed; 
        uint8 league; 
        uint256 startPrice;
        uint256 currentPrice; 
        uint256 earning; 
        uint256 releaseTime; 
        uint32 amountOfShips; 
    }
    struct ShipEntity {
        uint32 productID;
        uint8[4] upgrades;
        address owner; 
        address earner; 
        bool selling; 
        uint256 auctionEntity; 
        uint256 earned; 
        uint32 exp; 
        uint32 lastCashoutIndex; 
    }
    struct AuctionEntity {
        uint32 shipID;
        uint256 startPrice;
        uint256 finishPrice;
        uint256 startTime;
        uint256 duration;
    }
    event EventCashOut (
       address indexed player,
       uint256 amount
       ); 
    event EventLogin (
        address indexed player,
        string hash
        ); 
    event EventUpgradeShip (
        address indexed player,
        uint32 shipID,
        uint8 upgradeChoice
        ); 
    event EventTransfer (
        address indexed player,
        address indexed receiver,
        uint32 shipID
        ); 
    event EventTransferAction (
        address indexed player,
        address indexed receiver,
        uint32 shipID,
        uint8 ActionType
        ); 
    event EventAuction (
        address indexed player,
        uint32 shipID,
        uint256 startPrice,
        uint256 finishPrice,
        uint256 duration,
        uint256 currentTime
        ); 
    event EventCancelAuction (
        uint32 shipID
        ); 
    event EventBid (
        uint32 shipID
        ); 
    event EventBuyShip (
        address indexed player,
        uint32 productID,
        uint32 shipID
        ); 
    address public UpgradeMaster; 
    address public AuctionMaster; 
    address public ShipSellMaster; 
    function ChangeUpgradeMaster (address _newMaster) public {
        require(msg.sender == UpgradeMaster);
        UpgradeMaster = _newMaster;
    }
    function ChangeShipSellMaster (address _newMaster) public {
        require(msg.sender == ShipSellMaster);
        ShipSellMaster = _newMaster;
    }
    function ChangeAuctionMaster (address _newMaster) public {
        require(msg.sender == AuctionMaster);
        AuctionMaster = _newMaster;
    }
    function EtherShipsCore() public {
        UpgradeMaster = msg.sender;
        AuctionMaster = msg.sender;
        ShipSellMaster = msg.sender;
        newShipProduct("L-Raz", 50, 5, 5, 40, 5, 1, 50000000000000000, 500000000000000, now);
        newShipProduct("L-Vip", 50, 4, 6, 35, 6, 1, 50000000000000000, 500000000000000, now+(60*60*3));
        newShipProduct("L-Rapt", 50, 5, 5, 35, 5, 1, 50000000000000000, 500000000000000, now+(60*60*6));
        newShipProduct("L-Slash", 50, 5, 5, 30, 6, 1, 50000000000000000, 500000000000000, now+(60*60*12));
        newShipProduct("L-Stin", 50, 5, 5, 40, 5, 1, 50000000000000000, 500000000000000, now+(60*60*24));
        newShipProduct("L-Scor", 50, 4, 5, 35, 5, 1, 50000000000000000, 500000000000000, now+(60*60*48));
        newShipProduct("Sub-Sc", 60, 5, 45, 115, 4, 2, 100000000000000000, 1000000000000000, now);
        newShipProduct("Sub-Cycl", 70, 4, 40, 115, 4, 2, 100000000000000000, 1000000000000000, now+(60*60*6));
        newShipProduct("Sub-Deep", 80, 5, 45, 120, 4, 2, 100000000000000000, 1000000000000000, now+(60*60*12));
        newShipProduct("Sub-Sp", 90, 4, 50, 120, 3, 2, 100000000000000000, 1000000000000000, now+(60*60*24));
        newShipProduct("Sub-Ab", 100, 5, 55, 130, 3, 2, 100000000000000000, 1000000000000000, now+(60*60*48));
        newShipProduct("M-Sp", 140, 4, 40, 120, 4, 3, 200000000000000000, 2000000000000000, now);
        newShipProduct("M-Arma", 150, 4, 40, 115, 5, 3, 200000000000000000, 2000000000000000, now+(60*60*12));
        newShipProduct("M-Penetr", 160, 4, 35, 120, 6, 3, 200000000000000000, 2000000000000000, now+(60*60*24));
        newShipProduct("M-Slice", 170, 4, 45, 120, 3, 3, 200000000000000000, 2000000000000000, now+(60*60*36));
        newShipProduct("M-Hell", 180, 3, 35, 120, 2, 3, 200000000000000000, 2000000000000000, now+(60*60*48));
        newShipProduct("H-Haw", 210, 3, 65, 140, 3, 4, 400000000000000000, 4000000000000000, now);
        newShipProduct("H-Fat", 220, 3, 75, 150, 2, 4, 400000000000000000, 4000000000000000, now+(60*60*24));
        newShipProduct("H-Beh", 230, 2, 85, 160, 2, 4, 400000000000000000, 4000000000000000, now+(60*60*48));
        newShipProduct("H-Mamm", 240, 2, 100, 170, 2, 4, 400000000000000000, 4000000000000000, now+(60*60*72));
        newShipProduct("H-BigM", 250, 2, 120, 180, 3, 4, 400000000000000000, 4000000000000000, now+(60*60*96));
    }
    function cashOut (uint256 _amount) public payable {
        require (_amount >= 0); 
        require (_amount == uint256(uint128(_amount))); 
        require (this.balance >= _amount); 
        require (balances[msg.sender] >= _amount); 
        if (_amount == 0){
            _amount = balances[msg.sender];
        }
        balances[msg.sender] -= _amount; 
        if (!msg.sender.send(_amount)){ 
            balances[msg.sender] += _amount; 
        }
        EventCashOut (msg.sender, _amount);
        return;
    }
    function cashOutShip (uint32 _shipID) public payable {
        require (_shipID > 0 && _shipID < newIdShip); 
        require (ships[_shipID].owner == msg.sender); 
        uint256 _amount = shipProducts[ships[_shipID].productID].earning*(shipProducts[ships[_shipID].productID].amountOfShips-ships[_shipID].lastCashoutIndex);
        require (this.balance >= _amount); 
        require (_amount > 0);
        uint32 lastIndex = ships[_shipID].lastCashoutIndex;
        ships[_shipID].lastCashoutIndex = shipProducts[ships[_shipID].productID].amountOfShips; 
        if (!ships[_shipID].owner.send(_amount)){ 
            ships[_shipID].lastCashoutIndex = lastIndex; 
        }
        EventCashOut (msg.sender, _amount);
        return;
    }
    function login (string _hash) public {
        EventLogin (msg.sender, _hash);
        return;
    }
    function upgradeShip (uint32 _shipID, uint8 _upgradeChoice) public payable {
        require (_shipID > 0 && _shipID < newIdShip); 
        require (ships[_shipID].owner == msg.sender); 
        require (_upgradeChoice >= 0 && _upgradeChoice < 4); 
        require (ships[_shipID].upgrades[_upgradeChoice] < 5); 
        require (msg.value >= upgradePrice); 
        ships[_shipID].upgrades[_upgradeChoice]++; 
        balances[msg.sender] += msg.value-upgradePrice; 
        balances[UpgradeMaster] += upgradePrice; 
        EventUpgradeShip (msg.sender, _shipID, _upgradeChoice);
        return;
    }
    function _transfer (uint32 _shipID, address _receiver) public {
        require (_shipID > 0 && _shipID < newIdShip); 
        require (ships[_shipID].owner == msg.sender); 
        require (msg.sender != _receiver); 
        require (ships[_shipID].selling == false); 
        ships[_shipID].owner = _receiver; 
        ships[_shipID].earner = _receiver; 
        EventTransfer (msg.sender, _receiver, _shipID);
        return;
    }
    function _transferAction (uint32 _shipID, address _receiver, uint8 _ActionType) public {
        require (_shipID > 0 && _shipID < newIdShip); 
        require (ships[_shipID].owner == msg.sender); 
        require (msg.sender != _receiver); 
        require (ships[_shipID].selling == false); 
        ships[_shipID].owner = _receiver; 
        EventTransferAction (msg.sender, _receiver, _shipID, _ActionType);
        return;
    }
    function sellShip (uint32 _shipID, uint256 _startPrice, uint256 _finishPrice, uint256 _duration) public {
        require (_shipID > 0 && _shipID < newIdShip);
        require (ships[_shipID].owner == msg.sender);
        require (ships[_shipID].selling == false); 
        require (_startPrice >= _finishPrice);
        require (_startPrice > 0 && _finishPrice >= 0);
        require (_duration > 0);
        require (_startPrice == uint256(uint128(_startPrice))); 
        require (_finishPrice == uint256(uint128(_finishPrice))); 
        auctions[newIdAuctionEntity] = AuctionEntity(_shipID, _startPrice, _finishPrice, now, _duration);
        ships[_shipID].selling = true;
        ships[_shipID].auctionEntity = newIdAuctionEntity++;
        EventAuction (msg.sender, _shipID, _startPrice, _finishPrice, _duration, now);
    }
    function bid (uint32 _shipID) public payable {
        require (_shipID > 0 && _shipID < newIdShip); 
        require (ships[_shipID].selling == true); 
        AuctionEntity memory currentAuction = auctions[ships[_shipID].auctionEntity]; 
        uint256 currentPrice = currentAuction.startPrice-(((currentAuction.startPrice-currentAuction.finishPrice)/(currentAuction.duration))*(now-currentAuction.startTime));
        if (currentPrice < currentAuction.finishPrice){ 
            currentPrice = currentAuction.finishPrice;  
        }
        require (currentPrice >= 0); 
        require (msg.value >= currentPrice); 
        uint256 marketFee = (currentPrice/100)*3; 
        balances[ships[_shipID].owner] += currentPrice-marketFee; 
        balances[AuctionMaster] += marketFee; 
        balances[msg.sender] += msg.value-currentPrice; 
        ships[_shipID].owner = msg.sender; 
        ships[_shipID].selling = false; 
        delete auctions[ships[_shipID].auctionEntity]; 
        ships[_shipID].auctionEntity = 0; 
        EventBid (_shipID);
    }
    function cancelAuction (uint32 _shipID) public {
        require (_shipID > 0 && _shipID < newIdShip); 
        require (ships[_shipID].selling == true); 
        require (ships[_shipID].owner == msg.sender); 
        ships[_shipID].selling = false; 
        delete auctions[ships[_shipID].auctionEntity]; 
        ships[_shipID].auctionEntity = 0; 
        EventCancelAuction (_shipID);
    }
    function newShipProduct (string _name, uint32 _armor, uint32 _speed, uint32 _minDamage, uint32 _maxDamage, uint32 _attackSpeed, uint8 _league, uint256 _price, uint256 _earning, uint256 _releaseTime) private {
        shipProducts[newIdShipProduct++] = ShipProduct(_name, _armor, _speed, _minDamage, _maxDamage, _attackSpeed, _league, _price, _price, _earning, _releaseTime, 0);
    }
    function buyShip (uint32 _shipproductID) public payable {
        require (shipProducts[_shipproductID].currentPrice > 0 && msg.value > 0); 
        require (msg.value >= shipProducts[_shipproductID].currentPrice); 
        require (shipProducts[_shipproductID].releaseTime <= now); 
        if (msg.value > shipProducts[_shipproductID].currentPrice){
            balances[msg.sender] += msg.value-shipProducts[_shipproductID].currentPrice;
        }
        shipProducts[_shipproductID].currentPrice += shipProducts[_shipproductID].earning;
        ships[newIdShip++] = ShipEntity (_shipproductID, [0, 0, 0, 0], msg.sender, msg.sender, false, 0, 0, 0, ++shipProducts[_shipproductID].amountOfShips);
        balances[ShipSellMaster] += shipProducts[_shipproductID].startPrice;
        EventBuyShip (msg.sender, _shipproductID, newIdShip-1);
        return;
    }
    uint32 public newIdShip = 1; 
    uint32 public newIdShipProduct = 1; 
    uint256 public newIdAuctionEntity = 1; 
    mapping (uint32 => ShipEntity) ships; 
    mapping (uint32 => ShipProduct) shipProducts;
    mapping (uint256 => AuctionEntity) auctions;
    mapping (address => uint) balances;
    uint256 public constant upgradePrice = 5000000000000000; 
    function getShipName (uint32 _ID) public constant returns (string){
        return shipProducts[_ID].name;
    }
    function getShipProduct (uint32 _ID) public constant returns (uint32[7]){
        return [shipProducts[_ID].armor, shipProducts[_ID].speed, shipProducts[_ID].minDamage, shipProducts[_ID].maxDamage, shipProducts[_ID].attackSpeed, uint32(shipProducts[_ID].releaseTime), uint32(shipProducts[_ID].league)];
    }
    function getShipDetails (uint32 _ID) public constant returns (uint32[6]){
        return [ships[_ID].productID, uint32(ships[_ID].upgrades[0]), uint32(ships[_ID].upgrades[1]), uint32(ships[_ID].upgrades[2]), uint32(ships[_ID].upgrades[3]), uint32(ships[_ID].exp)];
    }
    function getShipOwner(uint32 _ID) public constant returns (address){
        return ships[_ID].owner;
    }
    function getShipSell(uint32 _ID) public constant returns (bool){
        return ships[_ID].selling;
    }
    function getShipTotalEarned(uint32 _ID) public constant returns (uint256){
        return ships[_ID].earned;
    }
    function getShipAuctionEntity (uint32 _ID) public constant returns (uint256){
        return ships[_ID].auctionEntity;
    }
    function getCurrentPrice (uint32 _ID) public constant returns (uint256){
        return shipProducts[_ID].currentPrice;
    }
    function getProductEarning (uint32 _ID) public constant returns (uint256){
        return shipProducts[_ID].earning;
    }
    function getShipEarning (uint32 _ID) public constant returns (uint256){
        return shipProducts[ships[_ID].productID].earning*(shipProducts[ships[_ID].productID].amountOfShips-ships[_ID].lastCashoutIndex);
    }
    function getCurrentPriceAuction (uint32 _ID) public constant returns (uint256){
        require (getShipSell(_ID));
        AuctionEntity memory currentAuction = auctions[ships[_ID].auctionEntity]; 
        uint256 currentPrice = currentAuction.startPrice-(((currentAuction.startPrice-currentAuction.finishPrice)/(currentAuction.duration))*(now-currentAuction.startTime));
        if (currentPrice < currentAuction.finishPrice){ 
            currentPrice = currentAuction.finishPrice;  
        }
        return currentPrice;
    }
    function getPlayerBalance(address _player) public constant returns (uint256){
        return balances[_player];
    }
    function getContractBalance() public constant returns (uint256){
        return this.balance;
    }
    function howManyShips() public constant returns (uint32){
        return newIdShipProduct;
    }
}

```

## RQ1_d05efb1718e4

SHA-256 `70cfe480f1e36af41b09dc487b883321cdd210d4a5874ddc3c072236c0778e0b`

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

## RQ1_5f5c873c8daa

SHA-256 `709fcca0108075a605419c2d054c4276289391c8b4f40df5de111474987b7371`

```solidity
pragma solidity ^0.4.19;
contract PropsToken {
    string public name = "Props Token";
    string public symbol = "PROPS";
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
    function PropsToken() public {
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

## RQ1_309938a2bbb9

SHA-256 `a449c13a145530478ae8b79580bc6b9f7a373c90391f029b00de979f13d721c2`

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

## RQ1_47d8a7f2761e

SHA-256 `ad282aafdd7e669773c6ad6d2e28de165408b70d622ecf73a1a8d7a004f194f2`

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
		emit Transfer(address(0), address(this), _totalSupply);
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
	    require(tokens>0);
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
	    require(tokens>0);
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

## RQ1_05019f0c86a3

SHA-256 `84a961d47378ef9a7a677b07a8120d7c7d0a311efa406173477a5983206f5fd6`

```solidity
pragma solidity ^0.5.1;
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
interface ERC20SwapContract {
    function initiate(
        bytes32 _swapID,
        address _spender,
        bytes32 _secretLock,
        uint256 _timelock,
        uint256 _value
    ) external;
    function initiateWithFees(
        bytes32 _swapID,
        address _spender,
        address _broker,
        uint256 _brokerFee,
        bytes32 _secretLock,
        uint256 _timelock,
        uint256 _value
    ) external;
    function redeem(bytes32 _swapID, address _receiver, bytes32 _secretKey) external;
    function refund(bytes32 _swapID) external;
    function withdrawBrokerFees(uint256 _amount) external;
    function audit(bytes32 _swapID) external view returns (uint256 timelock, uint256 value, address to, uint256 brokerFee, address broker, address from, bytes32 secretLock);
    function auditSecret(bytes32 _swapID) external view  returns (bytes32 secretKey);
    function refundable(bytes32 _swapID) external view returns (bool);
    function initiatable(bytes32 _swapID) external view returns (bool);
    function redeemable(bytes32 _swapID) external view returns (bool);
    function swapID(bytes32 _secretLock, uint256 _timelock) external pure returns (bytes32);
}
contract WBTCSwapContract is ERC20SwapContract {
    string public VERSION; 
    address public TOKEN_ADDRESS; 
    struct Swap {
        uint256 timelock;
        uint256 value;
        uint256 brokerFee;
        bytes32 secretLock;
        bytes32 secretKey;
        address funder;
        address spender;
        address broker;
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
    mapping (bytes32 => Swap) private swaps;
    mapping (bytes32 => States) private swapStates;
    mapping (address => uint256) public brokerFees;
    mapping (bytes32 => uint256) public redeemedAt;
    modifier onlyInvalidSwaps(bytes32 _swapID) {
        require(swapStates[_swapID] == States.INVALID, "swap opened previously");
        _;
    }
    modifier onlyOpenSwaps(bytes32 _swapID) {
        require(swapStates[_swapID] == States.OPEN, "swap not open");
        _;
    }
    modifier onlyClosedSwaps(bytes32 _swapID) {
        require(swapStates[_swapID] == States.CLOSED, "swap not redeemed");
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
    constructor(string memory _VERSION, address _TOKEN_ADDRESS) public {
        VERSION = _VERSION;
        TOKEN_ADDRESS = _TOKEN_ADDRESS;
    }
    function initiate(
        bytes32 _swapID,
        address _spender,
        bytes32 _secretLock,
        uint256 _timelock,
        uint256 _value
    ) external onlyInvalidSwaps(_swapID) {
        CompatibleERC20(TOKEN_ADDRESS).transferFrom(msg.sender, address(this), _value);
        Swap memory swap = Swap({
            timelock: _timelock,
            value: _value,
            funder: msg.sender,
            spender: _spender,
            broker: address(0x0),
            brokerFee: 0,
            secretLock: _secretLock,
            secretKey: 0x0
        });
        swaps[_swapID] = swap;
        swapStates[_swapID] = States.OPEN;
        emit LogOpen(_swapID, _spender, _secretLock);
    }
    function initiateWithFees(
        bytes32 _swapID,
        address _spender,
        address _broker,
        uint256 _brokerFee,
        bytes32 _secretLock,
        uint256 _timelock,
        uint256 _value
    ) external onlyInvalidSwaps(_swapID) {
        CompatibleERC20(TOKEN_ADDRESS).transferFrom(msg.sender, address(this), _value);
        Swap memory swap = Swap({
            timelock: _timelock,
            value: _value - _brokerFee,
            funder: msg.sender,
            spender: _spender,
            broker: _broker,
            brokerFee: _brokerFee,
            secretLock: _secretLock,
            secretKey: 0x0
        });
        swaps[_swapID] = swap;
        swapStates[_swapID] = States.OPEN;
        emit LogOpen(_swapID, _spender, _secretLock);
    }
    function refund(bytes32 _swapID) external onlyOpenSwaps(_swapID) onlyExpirableSwaps(_swapID) {
        swapStates[_swapID] = States.EXPIRED;
        CompatibleERC20(TOKEN_ADDRESS).transfer(swaps[_swapID].funder, swaps[_swapID].value + swaps[_swapID].brokerFee);
        emit LogExpire(_swapID);
    }
    function withdrawBrokerFees(uint256 _amount) external {
        require(_amount <= brokerFees[msg.sender]);
        brokerFees[msg.sender] -= _amount;
        CompatibleERC20(TOKEN_ADDRESS).transfer(msg.sender, _amount);
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
    function redeem(bytes32 _swapID, address _receiver, bytes32 _secretKey) external onlyOpenSwaps(_swapID) onlyWithSecretKey(_swapID, _secretKey) onlySpender(_swapID, msg.sender) {
        swaps[_swapID].secretKey = _secretKey;
        swapStates[_swapID] = States.CLOSED;
        redeemedAt[_swapID] = now;
        brokerFees[swaps[_swapID].broker] += swaps[_swapID].brokerFee;
        CompatibleERC20(TOKEN_ADDRESS).transfer(_receiver, swaps[_swapID].value);
        emit LogClose(_swapID, _secretKey);
    }
    function refundable(bytes32 _swapID) external view returns (bool) {
        return (now >= swaps[_swapID].timelock && swapStates[_swapID] == States.OPEN);
    }
    function initiatable(bytes32 _swapID) external view returns (bool) {
        return (swapStates[_swapID] == States.INVALID);
    }
    function redeemable(bytes32 _swapID) external view returns (bool) {
        return (swapStates[_swapID] == States.OPEN);
    }
    function swapID(bytes32 _secretLock, uint256 _timelock) public pure returns (bytes32) {
        return keccak256(abi.encodePacked(_secretLock, _timelock));
    }
}
```

## RQ1_f5828074525a

SHA-256 `8a082e27cae04ae2b57e80410d173a891f9a6983959226a49f2642f30ebf59e3`

```solidity
pragma solidity ^0.4.23;
interface ApproveAndCallFallBack {
    function receiveApproval(
        address from,
        uint256 _amount,
        address _token,
        bytes _data
    ) external;
}
contract Controlled {
    modifier onlyController { 
        require(msg.sender == controller); 
        _; 
    }
    address public controller;
    constructor() internal { 
        controller = msg.sender; 
    }
    function changeController(address _newController) public onlyController {
        controller = _newController;
    }
}
library RLPReader {
    uint8 constant STRING_SHORT_START = 0x80;
    uint8 constant STRING_LONG_START  = 0xb8;
    uint8 constant LIST_SHORT_START   = 0xc0;
    uint8 constant LIST_LONG_START    = 0xf8;
    uint8 constant WORD_SIZE = 32;
    struct RLPItem {
        uint len;
        uint memPtr;
    }
    function toRlpItem(bytes memory item) internal pure returns (RLPItem memory) {
        if (item.length == 0) 
            return RLPItem(0, 0);
        uint memPtr;
        assembly {
            memPtr := add(item, 0x20)
        }
        return RLPItem(item.length, memPtr);
    }
    function toList(RLPItem memory item) internal pure returns (RLPItem[] memory result) {
        require(isList(item));
        uint items = numItems(item);
        result = new RLPItem[](items);
        uint memPtr = item.memPtr + _payloadOffset(item.memPtr);
        uint dataLen;
        for (uint i = 0; i < items; i++) {
            dataLen = _itemLength(memPtr);
            result[i] = RLPItem(dataLen, memPtr); 
            memPtr = memPtr + dataLen;
        }
    }
    function isList(RLPItem memory item) internal pure returns (bool) {
        uint8 byte0;
        uint memPtr = item.memPtr;
        assembly {
            byte0 := byte(0, mload(memPtr))
        }
        if (byte0 < LIST_SHORT_START)
            return false;
        return true;
    }
    function numItems(RLPItem memory item) internal pure returns (uint) {
        uint count = 0;
        uint currPtr = item.memPtr + _payloadOffset(item.memPtr);
        uint endPtr = item.memPtr + item.len;
        while (currPtr < endPtr) {
           currPtr = currPtr + _itemLength(currPtr); 
           count++;
        }
        return count;
    }
    function _itemLength(uint memPtr) internal pure returns (uint len) {
        uint byte0;
        assembly {
            byte0 := byte(0, mload(memPtr))
        }
        if (byte0 < STRING_SHORT_START)
            return 1;
        else if (byte0 < STRING_LONG_START)
            return byte0 - STRING_SHORT_START + 1;
        else if (byte0 < LIST_SHORT_START) {
            assembly {
                let byteLen := sub(byte0, 0xb7) 
                memPtr := add(memPtr, 1) 
                let dataLen := div(mload(memPtr), exp(256, sub(32, byteLen))) 
                len := add(dataLen, add(byteLen, 1))
            }
        }
        else if (byte0 < LIST_LONG_START) {
            return byte0 - LIST_SHORT_START + 1;
        } 
        else {
            assembly {
                let byteLen := sub(byte0, 0xf7)
                memPtr := add(memPtr, 1)
                let dataLen := div(mload(memPtr), exp(256, sub(32, byteLen))) 
                len := add(dataLen, add(byteLen, 1))
            }
        }
    }
    function _payloadOffset(uint memPtr) internal pure returns (uint) {
        uint byte0;
        assembly {
            byte0 := byte(0, mload(memPtr))
        }
        if (byte0 < STRING_SHORT_START) 
            return 0;
        else if (byte0 < STRING_LONG_START || (byte0 >= LIST_SHORT_START && byte0 < LIST_LONG_START))
            return 1;
        else if (byte0 < LIST_SHORT_START)  
            return byte0 - (STRING_LONG_START - 1) + 1;
        else
            return byte0 - (LIST_LONG_START - 1) + 1;
    }
    function toBoolean(RLPItem memory item) internal pure returns (bool) {
        require(item.len == 1, "Invalid RLPItem. Booleans are encoded in 1 byte");
        uint result;
        uint memPtr = item.memPtr;
        assembly {
            result := byte(0, mload(memPtr))
        }
        return result == 0 ? false : true;
    }
    function toAddress(RLPItem memory item) internal pure returns (address) {
        require(item.len == 21, "Invalid RLPItem. Addresses are encoded in 20 bytes");
        uint memPtr = item.memPtr + 1; 
        uint addr;
        assembly {
            addr := div(mload(memPtr), exp(256, 12)) 
        }
        return address(addr);
    }
    function toUint(RLPItem memory item) internal pure returns (uint) {
        uint offset = _payloadOffset(item.memPtr);
        uint len = item.len - offset;
        uint memPtr = item.memPtr + offset;
        uint result;
        assembly {
            result := div(mload(memPtr), exp(256, sub(32, len))) 
        }
        return result;
    }
    function toBytes(RLPItem memory item) internal pure returns (bytes) {
        uint offset = _payloadOffset(item.memPtr);
        uint len = item.len - offset; 
        bytes memory result = new bytes(len);
        uint destPtr;
        assembly {
            destPtr := add(0x20, result)
        }
        copy(item.memPtr + offset, destPtr, len);
        return result;
    }
    function copy(uint src, uint dest, uint len) internal pure {
        for (; len >= WORD_SIZE; len -= WORD_SIZE) {
            assembly {
                mstore(dest, mload(src))
            }
            src += WORD_SIZE;
            dest += WORD_SIZE;
        }
        uint mask = 256 ** (WORD_SIZE - len) - 1;
        assembly {
            let srcpart := and(mload(src), not(mask)) 
            let destpart := and(mload(dest), mask) 
            mstore(dest, or(destpart, srcpart))
        }
    }
}
contract RLPHelper {
    using RLPReader for bytes;
    using RLPReader for uint;
    using RLPReader for RLPReader.RLPItem;
    function isList(bytes memory item) public pure returns (bool) {
        RLPReader.RLPItem memory rlpItem = item.toRlpItem();
        return rlpItem.isList();
    }
    function itemLength(bytes memory item) public pure returns (uint) {
        uint memPtr;
        assembly {
            memPtr := add(0x20, item)
        }
        return memPtr._itemLength();
    }
    function numItems(bytes memory item) public pure returns (uint) {
        RLPReader.RLPItem memory rlpItem = item.toRlpItem();
        return rlpItem.numItems();
    }
    function toBytes(bytes memory item) public pure returns (bytes) {
        RLPReader.RLPItem memory rlpItem = item.toRlpItem();
        return rlpItem.toBytes();
    }
    function toUint(bytes memory item) public pure returns (uint) {
        RLPReader.RLPItem memory rlpItem = item.toRlpItem();
        return rlpItem.toUint();
    }
    function toAddress(bytes memory item) public pure returns (address) {
        RLPReader.RLPItem memory rlpItem = item.toRlpItem();
        return rlpItem.toAddress();
    }
    function toBoolean(bytes memory item) public pure returns (bool) {
        RLPReader.RLPItem memory rlpItem = item.toRlpItem();
        return rlpItem.toBoolean();
    }
    function bytesToString(bytes memory item) public pure returns (string) {
        RLPReader.RLPItem memory rlpItem = item.toRlpItem();
        return string(rlpItem.toBytes());
    }
    function pollTitle(bytes memory item) public pure returns (string) {
        RLPReader.RLPItem[] memory items = item.toRlpItem().toList();
        return string(items[0].toBytes());
    }
    function pollBallot(bytes memory item, uint ballotNum) public pure returns (string) {
        RLPReader.RLPItem[] memory items = item.toRlpItem().toList();
        items = items[1].toList();
        return string(items[ballotNum].toBytes());
    }
}
interface TokenController {
    function proxyPayment(address _owner) external payable returns(bool);
    function onTransfer(address _from, address _to, uint _amount) external returns(bool);
    function onApprove(address _owner, address _spender, uint _amount) external
        returns(bool);
}
interface ERC20Token {
    function transfer(address _to, uint256 _value) external returns (bool success);
    function approve(address _spender, uint256 _value) external returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) external returns (bool success);
    function balanceOf(address _owner) external view returns (uint256 balance);
    function allowance(address _owner, address _spender) external view returns (uint256 remaining);
    function totalSupply() external view returns (uint256 supply);
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}
contract MiniMeTokenInterface is ERC20Token {
    function approveAndCall(
        address _spender,
        uint256 _amount,
        bytes _extraData
    ) 
        external 
        returns (bool success);
    function createCloneToken(
        string _cloneTokenName,
        uint8 _cloneDecimalUnits,
        string _cloneTokenSymbol,
        uint _snapshotBlock,
        bool _transfersEnabled
    ) 
        public
        returns(address);
    function generateTokens(
        address _owner,
        uint _amount
    )
        public
        returns (bool);
    function destroyTokens(
        address _owner,
        uint _amount
    ) 
        public
        returns (bool);
    function enableTransfers(bool _transfersEnabled) public;
    function claimTokens(address _token) public;
    function balanceOfAt(
        address _owner,
        uint _blockNumber
    ) 
        public
        constant
        returns (uint);
    function totalSupplyAt(uint _blockNumber) public view returns(uint);
}
contract MiniMeTokenFactory {
    function createCloneToken(
        address _parentToken,
        uint _snapshotBlock,
        string _tokenName,
        uint8 _decimalUnits,
        string _tokenSymbol,
        bool _transfersEnabled
    ) public returns (MiniMeToken) {
        MiniMeToken newToken = new MiniMeToken(
            this,
            _parentToken,
            _snapshotBlock,
            _tokenName,
            _decimalUnits,
            _tokenSymbol,
            _transfersEnabled
            );
        newToken.changeController(msg.sender);
        return newToken;
    }
}
contract MiniMeToken is MiniMeTokenInterface, Controlled {
    string public name;                
    uint8 public decimals;             
    string public symbol;              
    string public version = "MMT_0.1"; 
    struct Checkpoint {
        uint128 fromBlock;
        uint128 value;
    }
    MiniMeToken public parentToken;
    uint public parentSnapShotBlock;
    uint public creationBlock;
    mapping (address => Checkpoint[]) balances;
    mapping (address => mapping (address => uint256)) allowed;
    Checkpoint[] totalSupplyHistory;
    bool public transfersEnabled;
    MiniMeTokenFactory public tokenFactory;
    constructor(
        address _tokenFactory,
        address _parentToken,
        uint _parentSnapShotBlock,
        string _tokenName,
        uint8 _decimalUnits,
        string _tokenSymbol,
        bool _transfersEnabled
    ) 
        public
    {
        require(_tokenFactory != address(0)); 
        tokenFactory = MiniMeTokenFactory(_tokenFactory);
        name = _tokenName;                                 
        decimals = _decimalUnits;                          
        symbol = _tokenSymbol;                             
        parentToken = MiniMeToken(_parentToken);
        parentSnapShotBlock = _parentSnapShotBlock;
        transfersEnabled = _transfersEnabled;
        creationBlock = block.number;
    }
    function transfer(address _to, uint256 _amount) public returns (bool success) {
        require(transfersEnabled);
        return doTransfer(msg.sender, _to, _amount);
    }
    function transferFrom(
        address _from,
        address _to,
        uint256 _amount
    ) 
        public 
        returns (bool success)
    {
        if (msg.sender != controller) {
            require(transfersEnabled);
            if (allowed[_from][msg.sender] < _amount) { 
                return false;
            }
            allowed[_from][msg.sender] -= _amount;
        }
        return doTransfer(_from, _to, _amount);
    }
    function doTransfer(
        address _from,
        address _to,
        uint _amount
    ) 
        internal
        returns(bool)
    {
        if (_amount == 0) {
            return true;
        }
        require(parentSnapShotBlock < block.number);
        require((_to != 0) && (_to != address(this)));
        uint256 previousBalanceFrom = balanceOfAt(_from, block.number);
        if (previousBalanceFrom < _amount) {
            return false;
        }
        if (isContract(controller)) {
            require(TokenController(controller).onTransfer(_from, _to, _amount));
        }
        updateValueAtNow(balances[_from], previousBalanceFrom - _amount);
        uint256 previousBalanceTo = balanceOfAt(_to, block.number);
        require(previousBalanceTo + _amount >= previousBalanceTo); 
        updateValueAtNow(balances[_to], previousBalanceTo + _amount);
        emit Transfer(_from, _to, _amount);
        return true;
    }
    function doApprove(
        address _from,
        address _spender,
        uint256 _amount
    )
        internal 
        returns (bool)
    {
        require(transfersEnabled);
        require((_amount == 0) || (allowed[_from][_spender] == 0));
        if (isContract(controller)) {
            require(TokenController(controller).onApprove(_from, _spender, _amount));
        }
        allowed[_from][_spender] = _amount;
        emit Approval(_from, _spender, _amount);
        return true;
    }
    function balanceOf(address _owner) external view returns (uint256 balance) {
        return balanceOfAt(_owner, block.number);
    }
    function approve(address _spender, uint256 _amount) external returns (bool success) {
        doApprove(msg.sender, _spender, _amount);
    }
    function allowance(
        address _owner,
        address _spender
    ) 
        external
        view
        returns (uint256 remaining)
    {
        return allowed[_owner][_spender];
    }
    function approveAndCall(
        address _spender,
        uint256 _amount,
        bytes _extraData
    ) 
        external 
        returns (bool success)
    {
        require(doApprove(msg.sender, _spender, _amount));
        ApproveAndCallFallBack(_spender).receiveApproval(
            msg.sender,
            _amount,
            this,
            _extraData
        );
        return true;
    }
    function totalSupply() external view returns (uint) {
        return totalSupplyAt(block.number);
    }
    function balanceOfAt(
        address _owner,
        uint _blockNumber
    ) 
        public
        view
        returns (uint) 
    {
        if ((balances[_owner].length == 0) || (balances[_owner][0].fromBlock > _blockNumber)) {
            if (address(parentToken) != 0) {
                return parentToken.balanceOfAt(_owner, min(_blockNumber, parentSnapShotBlock));
            } else {
                return 0;
            }
        } else {
            return getValueAt(balances[_owner], _blockNumber);
        }
    }
    function totalSupplyAt(uint _blockNumber) public view returns(uint) {
        if ((totalSupplyHistory.length == 0) || (totalSupplyHistory[0].fromBlock > _blockNumber)) {
            if (address(parentToken) != 0) {
                return parentToken.totalSupplyAt(min(_blockNumber, parentSnapShotBlock));
            } else {
                return 0;
            }
        } else {
            return getValueAt(totalSupplyHistory, _blockNumber);
        }
    }
    function createCloneToken(
        string _cloneTokenName,
        uint8 _cloneDecimalUnits,
        string _cloneTokenSymbol,
        uint _snapshotBlock,
        bool _transfersEnabled
        ) 
            public
            returns(address)
        {
        uint snapshotBlock = _snapshotBlock;
        if (snapshotBlock == 0) {
            snapshotBlock = block.number;
        }
        MiniMeToken cloneToken = tokenFactory.createCloneToken(
            this,
            snapshotBlock,
            _cloneTokenName,
            _cloneDecimalUnits,
            _cloneTokenSymbol,
            _transfersEnabled
            );
        cloneToken.changeController(msg.sender);
        emit NewCloneToken(address(cloneToken), snapshotBlock);
        return address(cloneToken);
    }
    function generateTokens(
        address _owner,
        uint _amount
    )
        public
        onlyController
        returns (bool)
    {
        uint curTotalSupply = totalSupplyAt(block.number);
        require(curTotalSupply + _amount >= curTotalSupply); 
        uint previousBalanceTo = balanceOfAt(_owner, block.number);
        require(previousBalanceTo + _amount >= previousBalanceTo); 
        updateValueAtNow(totalSupplyHistory, curTotalSupply + _amount);
        updateValueAtNow(balances[_owner], previousBalanceTo + _amount);
        emit Transfer(0, _owner, _amount);
        return true;
    }
    function destroyTokens(
        address _owner,
        uint _amount
    ) 
        public
        onlyController
        returns (bool)
    {
        uint curTotalSupply = totalSupplyAt(block.number);
        require(curTotalSupply >= _amount);
        uint previousBalanceFrom = balanceOfAt(_owner, block.number);
        require(previousBalanceFrom >= _amount);
        updateValueAtNow(totalSupplyHistory, curTotalSupply - _amount);
        updateValueAtNow(balances[_owner], previousBalanceFrom - _amount);
        emit Transfer(_owner, 0, _amount);
        return true;
    }
    function enableTransfers(bool _transfersEnabled) public onlyController {
        transfersEnabled = _transfersEnabled;
    }
    function getValueAt(
        Checkpoint[] storage checkpoints,
        uint _block
    ) 
        view
        internal
        returns (uint)
    {
        if (checkpoints.length == 0) {
            return 0;
        }
        if (_block >= checkpoints[checkpoints.length-1].fromBlock) {
            return checkpoints[checkpoints.length-1].value;
        }
        if (_block < checkpoints[0].fromBlock) {
            return 0;
        }
        uint min = 0;
        uint max = checkpoints.length-1;
        while (max > min) {
            uint mid = (max + min + 1) / 2;
            if (checkpoints[mid].fromBlock<=_block) {
                min = mid;
            } else {
                max = mid-1;
            }
        }
        return checkpoints[min].value;
    }
    function updateValueAtNow(Checkpoint[] storage checkpoints, uint _value) internal {
        if (
            (checkpoints.length == 0) ||
            (checkpoints[checkpoints.length - 1].fromBlock < block.number)) 
        {
            Checkpoint storage newCheckPoint = checkpoints[checkpoints.length++];
            newCheckPoint.fromBlock = uint128(block.number);
            newCheckPoint.value = uint128(_value);
        } else {
            Checkpoint storage oldCheckPoint = checkpoints[checkpoints.length-1];
            oldCheckPoint.value = uint128(_value);
        }
    }
    function isContract(address _addr) internal view returns(bool) {
        uint size;
        if (_addr == 0) {
            return false;
        }    
        assembly {
            size := extcodesize(_addr)
        }
        return size > 0;
    }
    function min(uint a, uint b) internal returns (uint) {
        return a < b ? a : b;
    }
    function () public payable {
        require(isContract(controller));
        require(TokenController(controller).proxyPayment.value(msg.value)(msg.sender));
    }
    function claimTokens(address _token) public onlyController {
        if (_token == 0x0) {
            controller.transfer(address(this).balance);
            return;
        }
        MiniMeToken token = MiniMeToken(_token);
        uint balance = token.balanceOf(address(this));
        token.transfer(controller, balance);
        emit ClaimedTokens(_token, controller, balance);
    }
    event ClaimedTokens(address indexed _token, address indexed _controller, uint _amount);
    event Transfer(address indexed _from, address indexed _to, uint256 _amount);
    event NewCloneToken(address indexed _cloneToken, uint snapshotBlock);
    event Approval(
        address indexed _owner,
        address indexed _spender,
        uint256 _amount
    );
}
contract PollManager is Controlled {
    struct Poll {
        uint startBlock;
        uint endTime;
        bool canceled;
        uint voters;
        bytes description;
        uint8 numBallots;
        mapping(uint8 => mapping(address => uint)) ballots;
        mapping(uint8 => uint) qvResults;
        mapping(uint8 => uint) results;
        mapping(uint8 => uint) votersByBallot;
        address author;
    }
    Poll[] _polls;
    MiniMeToken public token;
    RLPHelper public rlpHelper;
    constructor(address _token) 
        public {
        token = MiniMeToken(_token);
        rlpHelper = new RLPHelper();
    }
    modifier onlySNTHolder {
        require(token.balanceOf(msg.sender) > 0, "SNT Balance is required to perform this operation"); 
        _; 
    }
    function addPoll(
        uint _endTime,
        bytes _description,
        uint8 _numBallots)
        public
        onlySNTHolder
        returns (uint _idPoll)
    {
        _idPoll = addPoll(block.number, _endTime, _description, _numBallots);
    }
    function addPoll(
        uint _startBlock,
        uint _endTime,
        bytes _description,
        uint8 _numBallots)
        public
        onlySNTHolder
        returns (uint _idPoll)
    {
        require(_endTime > block.timestamp, "End time must be greater than current timestamp");
        require(_startBlock >= block.number, "Start block must not be in the past");
        require(_numBallots <= 100, "Only a max of 100 ballots are allowed");
        _idPoll = _polls.length;
        _polls.length ++;
        Poll storage p = _polls[_idPoll];
        p.startBlock = _startBlock;
        p.endTime = _endTime;
        p.voters = 0;
        p.numBallots = _numBallots;
        p.description = _description;
        p.author = msg.sender;
        emit PollCreated(_idPoll);
    }
    function updatePollDescription(
        uint _idPoll, 
        bytes _description,
        uint8 _numBallots)
        public
    {
        require(_idPoll < _polls.length, "Invalid _idPoll");
        require(_numBallots <= 100, "Only a max of 100 ballots are allowed");
        Poll storage p = _polls[_idPoll];
        require(p.startBlock > block.number, "You cannot modify an active poll");
        require(p.author == msg.sender || msg.sender == controller, "Only the owner/controller can modify the poll");
        p.numBallots = _numBallots;
        p.description = _description;
        p.author = msg.sender;
    }
    function cancelPoll(uint _idPoll) 
        public {
        require(_idPoll < _polls.length, "Invalid _idPoll");
        Poll storage p = _polls[_idPoll];
        require(!p.canceled, "Poll has been canceled already");
        require(block.timestamp <= p.endTime, "Only active polls can be canceled");
        if(p.startBlock < block.number){
            require(msg.sender == controller, "Only the controller can cancel the poll");
        } else {
            require(p.author == msg.sender, "Only the owner can cancel the poll");
        }
        p.canceled = true;
        emit PollCanceled(_idPoll);
    }
    function canVote(uint _idPoll) 
        public 
        view 
        returns(bool)
    {
        if(_idPoll >= _polls.length) return false;
        Poll storage p = _polls[_idPoll];
        uint balance = token.balanceOfAt(msg.sender, p.startBlock);
        return block.number >= p.startBlock && block.timestamp < p.endTime && !p.canceled && balance != 0;
    }
    function sqrt(uint256 x) public pure returns (uint256 y) {
        uint256 z = (x + 1) / 2;
        y = x;
        while (z < y) {
            y = z;
            z = (x / z + z) / 2;
        }
    }
    function vote(uint _idPoll, uint[] _ballots) public {
        require(_idPoll < _polls.length, "Invalid _idPoll");
        Poll storage p = _polls[_idPoll];
        require(block.number >= p.startBlock && block.timestamp < p.endTime && !p.canceled, "Poll is inactive");
        require(_ballots.length == p.numBallots, "Number of ballots is incorrect");
        unvote(_idPoll);
        uint amount = token.balanceOfAt(msg.sender, p.startBlock);
        require(amount != 0, "No SNT balance available at start block of poll");
        p.voters++;
        uint totalBallots = 0;
        for(uint8 i = 0; i < _ballots.length; i++){
            totalBallots += _ballots[i];
            p.ballots[i][msg.sender] = _ballots[i];
            if(_ballots[i] != 0){
                p.qvResults[i] += sqrt(_ballots[i] / 1 ether);
                p.results[i] += _ballots[i];
                p.votersByBallot[i]++;
            }
        }
        require(totalBallots <= amount, "Total ballots must be less than the SNT balance at poll start block");
        emit Vote(_idPoll, msg.sender, _ballots);
    }
    function unvote(uint _idPoll) public {
        require(_idPoll < _polls.length, "Invalid _idPoll");
        Poll storage p = _polls[_idPoll];
        require(block.number >= p.startBlock && block.timestamp < p.endTime && !p.canceled, "Poll is inactive");
        if(p.voters == 0) return;
        uint prevVotes = 0;
        for(uint8 i = 0; i < p.numBallots; i++){
            uint ballotAmount = p.ballots[i][msg.sender];
            prevVotes += ballotAmount;
            p.ballots[i][msg.sender] = 0;
            if(ballotAmount != 0){
                p.qvResults[i] -= sqrt(ballotAmount / 1 ether);
                p.results[i] -= ballotAmount;
                p.votersByBallot[i]--;
            }
        }
        if(prevVotes != 0){
            p.voters--;
        }
        emit Unvote(_idPoll, msg.sender);
    }
    function nPolls()
        public
        view 
        returns(uint)
    {
        return _polls.length;
    }
    function poll(uint _idPoll)
        public 
        view 
        returns(
        uint _startBlock,
        uint _endTime,
        bool _canVote,
        bool _canceled,
        bytes _description,
        uint8 _numBallots,
        bool _finalized,
        uint _voters,
        address _author,
        uint[100] _tokenTotal,
        uint[100] _quadraticVotes,
        uint[100] _votersByBallot
    )
    {
        require(_idPoll < _polls.length, "Invalid _idPoll");
        Poll storage p = _polls[_idPoll];
        _startBlock = p.startBlock;
        _endTime = p.endTime;
        _canceled = p.canceled;
        _canVote = canVote(_idPoll);
        _description = p.description;
        _numBallots = p.numBallots;
        _author = p.author;
        _finalized = (!p.canceled) && (block.number >= _endTime);
        _voters = p.voters;
        for(uint8 i = 0; i < p.numBallots; i++){
            _tokenTotal[i] = p.results[i];
            _quadraticVotes[i] = p.qvResults[i];
            _votersByBallot[i] = p.votersByBallot[i];
        }
    }
    function pollTitle(uint _idPoll) public view returns (string){
        require(_idPoll < _polls.length, "Invalid _idPoll");
        Poll memory p = _polls[_idPoll];
        return rlpHelper.pollTitle(p.description);
    }
    function pollBallot(uint _idPoll, uint _ballot) public view returns (string){
        require(_idPoll < _polls.length, "Invalid _idPoll");
        Poll memory p = _polls[_idPoll];
        return rlpHelper.pollBallot(p.description, _ballot);
    }
    function getVote(uint _idPoll, address _voter) 
        public 
        view 
        returns (uint[100] votes){
        require(_idPoll < _polls.length, "Invalid _idPoll");
        Poll storage p = _polls[_idPoll];
        for(uint8 i = 0; i < p.numBallots; i++){
            votes[i] = p.ballots[i][_voter];
        }
        return votes;
    }
    event Vote(uint indexed idPoll, address indexed _voter, uint[] ballots);
    event Unvote(uint indexed idPoll, address indexed _voter);
    event PollCanceled(uint indexed idPoll);
    event PollCreated(uint indexed idPoll);
}
```

## RQ1_0dee0198d17a

SHA-256 `dc3df044b093d95dad47aeac95e7c3654dc13db92f5ae74ee415c4d1799fcbc3`

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
    mapping (address => uint256) public accoutToSummonNum;
    mapping (address => uint256) public accoutToPayLevel;
    mapping (address => uint256) public accountsLastClearTime;
    uint256 public levelClearTime = now;
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
    function donateSkin(uint128 specifiedAppearance, address donee) external onlyCOO {
        Skin memory newSkin = Skin({appearance: specifiedAppearance, cooldownEndTime: uint64(now), mixingWithId: 0});
        skins[nextSkinId] = newSkin;
        skinIdToOwner[nextSkinId] = donee;
        isOnSale[nextSkinId] = false;
        CreateNewSkin(nextSkinId, donee);
        nextSkinId++;
        numSkinOfAccounts[donee] += 1;   
        skinCreatedNum += 1;
    }
    function summon() external payable whenNotPaused {
        if (accountsLastClearTime[msg.sender] == uint256(0)) {
            accountsLastClearTime[msg.sender] = now;
        } else {
            if (accountsLastClearTime[msg.sender] < levelClearTime && now > levelClearTime) {
                accoutToSummonNum[msg.sender] = 0;
                accoutToPayLevel[msg.sender] = 0;
                accountsLastClearTime[msg.sender] = now;
            }
        }
        uint256 payLevel = accoutToPayLevel[msg.sender];
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
        accoutToSummonNum[msg.sender] += 1;
        if (payLevel < 5) {
            if (accoutToSummonNum[msg.sender] >= levelSplits[payLevel]) {
                accoutToPayLevel[msg.sender] = payLevel + 1;
            }
        }
    }
    function bleach(uint128 skinId, uint128 attributes) external payable whenNotPaused {
        require(msg.sender == skinIdToOwner[skinId]);
        require(isOnSale[skinId] == false);
        require(msg.value >= bleachPrice);
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

## RQ1_281f3b161467

SHA-256 `edf1976a69d47074f1acadb05ff0f48d7478524228ba0c0ac9e9433d9eb48909`

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

## RQ1_f2ab53d09329

SHA-256 `784d45842581b8499b0bf4077ab7e26607d36a59487c47e301438873625c3870`

```solidity
pragma solidity ^0.4.24;
contract Slot {
    uint constant BET_EXPIRATION_BLOCKS = 250;
    uint constant MIN_BET = 0.01 ether;
    uint constant MAX_BET = 300000 ether;
    uint constant JACKPOT_PERCENT = 10;
    uint constant MINIPOT_PERCENT = 10;
    uint[][] REELS = [
                      [1,2,1,3,1,4,5,3,5,6],
                      [1,2,1,3,1,4,1,3,1,6],
                      [4,5,3,5,4,2,4,3,5,6]
                      ];
    uint[] SYMBOL_MASK = [0, 1, 2, 4, 8, 16, 32];
    uint[][] PAYTABLE = [
                         [0x010100, 2],
                         [0x010120, 4],
                         [0x010110, 4],
                         [0x040402, 8],
                         [0x040404, 8],
                         [0x080802, 12],
                         [0x080808, 12],
                         [0x202002, 16],
                         [0x020220, 16],
                         [0x202020, 100],
                         [0x020202, 9999]
                         ];
    address owner;
    address pendingOwner;
    uint acceptPrice;
    uint public pendingBetAmount;
    uint public jackpotPool;
    uint public minipotPool;
    uint public rollTimes;
    uint public minipotTimes;
    struct Roll {
        uint bet;
        uint8 lines;
        uint8 rollCount;
        uint blocknum;
        address next;
    }
    struct PartnerShare {
        address from;
        uint share;
    }
    event RollBegin(address indexed from, uint bet, uint8 lines, uint count);
    event RollEnd(address indexed from, uint bet, uint8 lines, uint32 wheel, uint win, uint minipot);
    mapping(address => Roll[]) public rolls;
    address public rollHead;
    address public rollTail;
    PartnerShare[] public partners;
    constructor () public {
        owner = msg.sender;
    }
    function setOwner(address newOwner, uint price) public {
        require (msg.sender == owner, "Only owner can set new owner.");
        require (newOwner != owner, "No need to set again.");
        pendingOwner = newOwner;
        acceptPrice = price;
    }
    function acceptOwner() payable public {
        require (msg.sender == pendingOwner, "You are not pending owner.");
        require (msg.value >= acceptPrice, "Amount not enough.");
        owner.transfer(acceptPrice);
        owner = pendingOwner;
    }
    function() public payable {
        require (msg.value > 200 finney, 'Min investment required.');
        if (owner != msg.sender) {
            partners.push(PartnerShare(msg.sender, msg.value / 1 finney));
        }
    }
    function kill() external {
        require (msg.sender == owner, "Only owner can kill.");
        require (pendingBetAmount == 0, "All spins need processed befor self-destruct.");
        distribute();
        selfdestruct(owner);
    }
    function rollBlockNumber(address addr) public view returns (uint) {
        if (rolls[addr].length > 0) {
            return rolls[addr][0].blocknum;
        } else {
            return 0;
        }
    }
    function getPartnersCount() public view returns (uint) {
        return partners.length;
    }
    function jackpot() public view returns (uint) {
        return jackpotPool / 2;
    }
    function minipot() public view returns (uint) {
        return minipotPool / 2;
    }
    function roll(uint8 lines, uint8 count) public payable {
        require (rolls[msg.sender].length == 0, "Can't roll mutiple times.");
        uint betValue = msg.value / count;
        require (betValue >= MIN_BET && betValue <= MAX_BET, "Bet amount should be within range.");
        rolls[msg.sender].push(Roll(betValue, lines, count, block.number, address(0)));
        if (rollHead == address(0)) {
            rollHead = msg.sender;
        } else {
            rolls[rollTail][0].next = msg.sender;
        }
        rollTail = msg.sender;
        pendingBetAmount += msg.value;
        jackpotPool += msg.value * JACKPOT_PERCENT / 100;
        minipotPool += msg.value * MINIPOT_PERCENT / 100;
        emit RollBegin(msg.sender, betValue, lines, count);
    }
    function check(uint maxCount) public {
        require (maxCount > 0, 'No reason for check nothing');
        uint i = 0;
        address currentAddr = rollHead;
        while (i < maxCount && currentAddr != address(0)) {
            Roll storage rollReq = rolls[currentAddr][0];
            if (rollReq.blocknum >= block.number) {
                return;
            }
            checkRoll(currentAddr, rollReq);
            rollHead = rollReq.next;
            if (currentAddr == rollTail) {
                rollTail = address(0);
            }
            delete rolls[currentAddr];
            currentAddr = rollHead;
            i++;
        }
    }
    function checkRoll(address addr, Roll storage rollReq) private {
        uint totalWin = 0;
        if (block.number <= rollReq.blocknum + BET_EXPIRATION_BLOCKS) {
            for (uint x = 0; x < rollReq.rollCount; x++) {
                totalWin += doRoll(addr, rollReq.bet, rollReq.lines, rollReq.blocknum, pendingBetAmount + rollTimes + x);
            }
        } else {
            totalWin = rollReq.bet * rollReq.rollCount - 2300;
        }
        pendingBetAmount -= rollReq.bet * rollReq.rollCount;
        if (totalWin > 0) {
            if (address(this).balance > totalWin + 2300) {
                addr.transfer(totalWin);
            } else {
                partners.push(PartnerShare(addr, totalWin / 1 finney));
            }
        }
    }
    function doRoll(address addr, uint bet, uint8 lines, uint blocknum, uint seed) private returns (uint) {
        uint[3] memory stops;
        uint winRate;
        uint entropy;
        (stops, winRate, entropy) = calcRoll(addr, blocknum, seed);
        uint wheel = stops[0]<<16 | stops[1]<<8 | stops[2];
        uint win = bet * winRate;
        if (winRate == 9999) {
            win = jackpotPool / 2;
            jackpotPool -= win;
        }
        rollTimes++;
        uint minipotWin = 0;
        if (0xffff / (entropy >> 32 & 0xffff) > (100 * (minipotTimes + 1)) - rollTimes) {
            minipotTimes++;
            minipotWin = minipotPool / 2;
            minipotPool -= minipotWin;
        }
        emit RollEnd(addr, bet, lines, uint32(wheel), win, minipotWin);
        return win + minipotWin;
    }
    function calcRoll(address addr, uint blocknum, uint seed) public view returns (uint[3] memory stops, uint winValue, uint entropy) {
        require (block.number > blocknum, "Can't check in the same block or before.");
        require (block.number <= blocknum + BET_EXPIRATION_BLOCKS, "Can't check for too old block.");
        entropy = uint(keccak256(abi.encodePacked(addr, blockhash(blocknum), seed)));
        stops = [REELS[0][entropy % REELS[0].length],
                 REELS[1][(entropy >> 8) % REELS[1].length],
                 REELS[2][(entropy >> 16) % REELS[2].length]];
        winValue = calcPayout(stops[0], stops[1], stops[2]);
    }
    function calcPayout(uint p1, uint p2, uint p3) public view returns (uint) {
        uint line = SYMBOL_MASK[p1] << 16 | SYMBOL_MASK[p2] << 8 | SYMBOL_MASK[p3];
        uint pay = 0;
        for (uint i = 0; i < PAYTABLE.length; i++) {
            if (PAYTABLE[i][0] == line & PAYTABLE[i][0]) {
                pay = PAYTABLE[i][1];
            }
        }
        return pay;
    }
    function getBonus() public view returns (uint) {
        return address(this).balance - pendingBetAmount - jackpotPool - minipotPool;
    }
    function distribute() public returns (uint result) {
        bool isPartner = (owner == msg.sender);
        uint totalShare = 0;
        for (uint i = 0; i < partners.length; i++) {
            if (partners[i].from == msg.sender) {
                isPartner = true;
            }
            totalShare += partners[i].share;
        }
        require(isPartner, 'Only partner can distrubute bonus.');
        uint bonus = getBonus();
        if (totalShare > 0) {
            uint price = ((bonus / 10) * 6) / totalShare;
            if (price > 0) {
                for (uint j = 0; j < partners.length; j++) {
                    uint share = partners[j].share * price;
                    partners[j].from.transfer(share);
                    if (partners[j].from == msg.sender) {
                        result += share;
                    }
                }
            }
            if (price > 2 * 1 finney) {
                delete partners;
            }
        }
        uint ownerShare = (bonus / 10) * 4;
        owner.transfer(ownerShare);
        if (owner == msg.sender) {
            result += ownerShare;
        }
    }
}

```

## RQ1_404fa1b92065

SHA-256 `d42901c6ec90af20d7a85700e4dee0da0ebd83d0d6aa72e0bcf1d819f74459a3`

```solidity
pragma solidity ^0.4.24;
contract TeikhosBounty {
    bytes32 proof_of_public_key1 = hex"381c185bf75548b134adc3affd0cc13e66b16feb125486322fa5f47cb80a5bf0";
    bytes32 proof_of_public_key2 = hex"5f9d1d2152eae0513a4814bd8e6b0dd3ac8f6310c0494c03e9aa08bcd867c352";
    function authenticate(bytes _publicKey) { 
        address signer = address(keccak256(_publicKey));
        bytes32 publicKey1;
        bytes32 publicKey2;
        assembly {
        publicKey1 := mload(add(_publicKey,0x20))
        publicKey2 := mload(add(_publicKey,0x40))
        }
        bytes32 r = proof_of_public_key1 ^ publicKey1;
        bytes32 s = proof_of_public_key2 ^ publicKey2;
        bytes32 msgHash = keccak256("\x19Ethereum Signed Message:\n64", _publicKey);
        if(ecrecover(msgHash, 27, r, s) == signer) suicide(msg.sender);
        if(ecrecover(msgHash, 28, r, s) == signer) suicide(msg.sender);
    }
    function() payable {}                            
}

```

## RQ1_637f82d88251

SHA-256 `0749b626adeb0167afd0fe2b2b99183701579ce18ee3e3a28f8c46e78fb740e0`

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
contract VIT is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "VitToken";
    string public constant symbol = "VT";
    uint public constant decimals = 18;
    uint256 public totalSupply = 5000000000e18;
    uint256 public totalDistributed = 2500000000e18;
    uint256 public totalRemaining = totalSupply.sub(totalDistributed);
    uint256 public value = 6000e18;
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
    function VitToken() public {
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

## RQ1_d090e1dba88d

SHA-256 `8abf9a6b1f815aca7d70e29b0c612d8f3b699179a93acf491704ff18f311429a`

```solidity
pragma solidity >=0.5.0 <0.6.0;
contract Ownable {
    event OwnershipTransfer (address previousOwner, address newOwner);
    address owner;
    constructor() public {
        owner = msg.sender;
        emit OwnershipTransfer(address(0), owner);
    }
    modifier onlyOwner() {
        require(
            msg.sender == owner,
            "Function can only be called by contract owner"
        );
        _;
    }
    function transferOwnership(address _newOwner) public onlyOwner {
        require (
            _newOwner != address(0),
            "New owner address cannot be zero"
        );
        address oldOwner = owner;
        owner = _newOwner;
        emit OwnershipTransfer(oldOwner, _newOwner);
    }
}
interface VIP181 {
    function ownerOf(uint256 _tokenId) external view returns (address);
    function getApproved(uint256 _tokenId) external view returns (address);
    function isApprovedForAll(
        address _owner, 
        address _operator
    ) external view returns (bool);
}
interface VIP180 {
    function transferFrom(address _from, address _to, uint _tokens) external returns (bool);
}
interface LockedTokenManager {    
    function lockFrom(
        address _tokenHolder, 
        address _tokenAddress, 
        uint _tokens, 
        uint _numberOfMonths
    ) external returns(bool);
    function transferFromAndLock(
        address _from,
        address _to,
        address _tokenAddress,
        uint _tokens,
        uint _numberOfMonths
    ) external returns (bool);
}
contract SegmentedTransfer is Ownable {
    struct TransferSettings {
        uint burnedPercent;
        uint lockedPercent;
        uint transferredThenLockedPercent;
        uint lockedMonths;
    }
    LockedTokenManager public lockContract;
    modifier notZero(uint _param) {
        require(_param != 0, "Parameter cannot be zero");
        _;
    }
    function setLockContract (address _lockAddress)
        external 
        notZero(uint(_lockAddress)) 
        onlyOwner
    {
        lockContract = LockedTokenManager(_lockAddress);
    }
    function segmentedTransfer(
        address _tokenContractAddress,
        address _to,
        uint _totalTokens,
        TransferSettings storage _transfer
    ) internal {
        uint tokensLeft = _totalTokens;
        uint amount;
        if (_transfer.burnedPercent > 0) {
            amount = _totalTokens * _transfer.burnedPercent / 100;
            VIP180(_tokenContractAddress).transferFrom(msg.sender, address(0), amount);
            tokensLeft -= amount;
        }
        if (_transfer.lockedPercent > 0) {
            amount = _totalTokens * _transfer.lockedPercent / 100;
            lockContract.lockFrom(
                msg.sender, 
                _tokenContractAddress, 
                _transfer.lockedMonths, 
                amount
            );
            tokensLeft -= amount;
        }
        if (_transfer.transferredThenLockedPercent > 0) {
            amount = _totalTokens * _transfer.transferredThenLockedPercent / 100;
            lockContract.transferFromAndLock(
                msg.sender, 
                address(_to), 
                _tokenContractAddress, 
                _transfer.lockedMonths, 
                amount
            );
            tokensLeft -= amount;
        }
        if (tokensLeft > 0) {
            VIP180(_tokenContractAddress).transferFrom(msg.sender, _to, tokensLeft);
        }
    }   
}
contract AacColoredTokens is SegmentedTransfer {
    event NewColor(address indexed _creator, string _name);
    event DepositColor(uint indexed _to, uint indexed _colorIndex, uint _tokens);
    event SpendColor(
        uint indexed _from, 
        uint indexed _color, 
        uint _amount
    );
    struct ColoredToken {
        address creator;
        string name;
        mapping (uint => uint) balances;
        mapping (address => uint) depositAllowances;
    }
    ColoredToken[] coloredTokens;
    uint public priceToRegisterColor = 100000 * 10**18;
    VIP181 public aacContract;
    address public ehrtAddress;
    TransferSettings public colorRegistrationTransfer = TransferSettings({
        burnedPercent: 50,
        lockedPercent: 0,
        transferredThenLockedPercent: 0,
        lockedMonths: 24
    });
    TransferSettings public colorDepositTransfer = TransferSettings({
        burnedPercent: 50,
        lockedPercent: 0,
        transferredThenLockedPercent: 0,
        lockedMonths: 24
    });
    uint constant UID_MAX = 0xFFFFFFFFFFFFFF;
    function setAacContract (address _aacAddress) 
        external 
        notZero(uint(_aacAddress)) 
        onlyOwner
    {
        aacContract = VIP181(_aacAddress);
    }
    function setEhrtContractAddress (address _newAddress) 
        external 
        notZero(uint(_newAddress)) 
        onlyOwner
    {
        ehrtAddress = _newAddress;
    }
    function setPriceToRegisterColor(uint _newAmount) 
        external 
        onlyOwner
        notZero(_newAmount)
    {
        priceToRegisterColor = _newAmount;
    }
    function setTransferSettingsForColoredTokenCreation(
        uint _burnPercent,
        uint _lockPercent,
        uint _transferLockPercent,
        uint _lockedMonths
    ) external onlyOwner {
        require(_burnPercent + _lockPercent + _transferLockPercent <= 100);
        colorRegistrationTransfer = TransferSettings(
            _burnPercent, 
            _lockPercent, 
            _transferLockPercent,
            _lockedMonths
        );
    }
    function setTransferSettingsForColoredTokenDeposits(
        uint _burnPercent,
        uint _lockPercent,
        uint _transferLockPercent,
        uint _lockedMonths
    ) external onlyOwner {
        require(_burnPercent + _lockPercent + _transferLockPercent <= 100);
        colorDepositTransfer = TransferSettings(
            _burnPercent, 
            _lockPercent, 
            _transferLockPercent,
            _lockedMonths
        );
    }
    function registerNewColor(string calldata _colorName) external returns (uint) {
        require (
            bytes(_colorName).length > 0 && bytes(_colorName).length < 32,
            "Invalid color name length"
        );
        segmentedTransfer(ehrtAddress, owner, priceToRegisterColor, colorRegistrationTransfer);
        uint index = coloredTokens.push(ColoredToken(msg.sender, _colorName));
        return index;
    }
    function approve(uint _colorIndex, address _spender, uint _tokens) external {
        require(msg.sender == coloredTokens[_colorIndex].creator);
        coloredTokens[_colorIndex].depositAllowances[_spender] = _tokens;
    }
    function deposit (uint _colorIndex, uint _to, uint _tokens)
        external 
        notZero(_tokens)
    {
        require (_colorIndex < coloredTokens.length, "Invalid color index");
        require (
            msg.sender == coloredTokens[_colorIndex].creator ||
            coloredTokens[_colorIndex].depositAllowances[msg.sender] >= _tokens,
            "Not authorized to deposit this color"
        );
        require(aacContract.ownerOf(_to) != address(0), "AAC does not exist");
        segmentedTransfer(ehrtAddress, owner, _tokens, colorDepositTransfer);
        coloredTokens[_colorIndex].balances[_to] += _tokens;
        if (msg.sender != coloredTokens[_colorIndex].creator) {
            coloredTokens[_colorIndex].depositAllowances[msg.sender] -= _tokens;
        }
        emit DepositColor(_to, _colorIndex, _tokens);
    }
    function depositBulk (uint _colorIndex, uint[] calldata _to, uint _tokens)
        external 
        notZero(_tokens)
    {
        require (_colorIndex < coloredTokens.length, "Invalid color index");
        require (
            msg.sender == coloredTokens[_colorIndex].creator ||
            coloredTokens[_colorIndex].depositAllowances[msg.sender] > _tokens * _to.length,
            "Not authorized to deposit this color"
        );
        segmentedTransfer(ehrtAddress, owner, _tokens * _to.length, colorDepositTransfer);
        for(uint i = 0; i < _to.length; ++i){
            require(aacContract.ownerOf(_to[i]) != address(0), "AAC does not exist");
            coloredTokens[_colorIndex].balances[_to[i]] += _tokens;
            emit DepositColor(_to[i], _colorIndex, _tokens);
        }
        if (msg.sender != coloredTokens[_colorIndex].creator) {
            coloredTokens[_colorIndex].depositAllowances[msg.sender] -= _tokens * _to.length;
        }
    }
    function spend (uint _colorIndex, uint _from, uint _tokens) 
        external 
        notZero(_tokens)
        returns(bool) 
    {
        require (_colorIndex < coloredTokens.length, "Invalid color index");
        require (
            msg.sender == aacContract.ownerOf(_from), 
            "Sender is not owner of AAC"
        );
        require (
            coloredTokens[_colorIndex].balances[_from] >= _tokens,
            "Insufficient tokens to spend"
        );
        coloredTokens[_colorIndex].balances[_from] -= _tokens;
        emit SpendColor(_from, _colorIndex, _tokens);
        return true;
    }
    function spendFrom(uint _colorIndex, uint _from, uint _tokens)
        external 
        notZero(_tokens)
        returns (bool) 
    {
        require (_colorIndex < coloredTokens.length, "Invalid color index");
        require (
            msg.sender == aacContract.getApproved(_from) ||
            aacContract.isApprovedForAll(aacContract.ownerOf(_from), msg.sender), 
            "Sender is not authorized operator for AAC"
        );
        require (
            coloredTokens[_colorIndex].balances[_from] >= _tokens,
            "Insufficient balance to spend"
        );
        coloredTokens[_colorIndex].balances[_from] -= _tokens;
        emit SpendColor(_from, _colorIndex, _tokens);
        return true;
    }
    function onLink(uint _oldUid, uint _newUid) external {
        require (msg.sender == address(aacContract), "Unauthorized transaction");
        require (_oldUid > UID_MAX && _newUid <= UID_MAX);
        for(uint i = 0; i < coloredTokens.length; ++i) {
            coloredTokens[i].balances[_newUid] = coloredTokens[i].balances[_oldUid];
        }
    }
    function getColoredTokenBalance(uint _uid, uint _colorIndex) 
        external 
        view 
        returns(uint) 
    {
        return coloredTokens[_colorIndex].balances[_uid];
    }
    function coloredTokenCount() external view returns (uint) {
        return coloredTokens.length;
    }
    function getColoredToken(uint _colorIndex) 
        external 
        view 
        returns(address, string memory)
    {
        return (
            coloredTokens[_colorIndex].creator, 
            coloredTokens[_colorIndex].name
        );
    }
}

```

## RQ1_aa45d3ff1035

SHA-256 `12e8888e351d8e6272ee1a5c2c2b072416324aca18b1653c064c77510e899156`

```solidity
pragma solidity ^0.4.19;
contract Lottery7 {
    address owner;
    address profit = 0xB7BB510B0746bdeE208dB6fB781bF5Be39d15A15;
    uint public tickets;
    uint public round;
    string public status;
    uint public lastWiningTicketNumber;
    address public lastWinner;
    address ticket1;
    address ticket2;
    address ticket3;
    address ticket4;
    address ticket5;
    uint constant price = 0.1 ether; 
    uint seed;
    bool entry = false;
    function Lottery7() public { 
        owner = msg.sender;
        tickets = 5;
        round = 1;
        status = "Running";
        entry = false;
        seed = 777;
    }
    function changeStatus(string w) public {
        if (msg.sender == owner) {
            status = w;
        }
        else {
            revert();
        }
    }
    function changeSeed(uint32 n) public {
        if (msg.sender == owner) {
            seed = uint(n);
            seed = uint(block.blockhash(block.number-seed))%2000 + 1; 
        }
        else {
            revert();
        }
    }
    function () public payable { 
        buyTickets();
    }
    function buyTickets() public payable {
        if (entry == true) { 
            revert();
        }
        entry = true;
        if (msg.value != (price)) {
            entry = false;
            if (keccak256(status) == keccak256("Shutdown")) { 
                selfdestruct(owner);
            }
            revert(); 
        }
        else {
            if (tickets == 5) {
                tickets -= 1;
                ticket1 = msg.sender;
            }
            else if(tickets == 4) {
                tickets -= 1;
                ticket2 = msg.sender;
                profit.transfer(price * 1/2); 
            }
            else if(tickets == 3) {
                tickets -= 1;
                ticket3 = msg.sender;
            }
            else if(tickets == 2) {
                tickets -= 1;
                ticket4 = msg.sender;
            }
            else if(tickets == 1) {
                ticket5 = msg.sender;
                tickets = 5; 
                round += 1; 
                seed = uint(block.blockhash(block.number-seed))%2000 + 1; 
                uint random_number = uint(block.blockhash(block.number-seed))%5 + 1; 
                lastWiningTicketNumber = random_number; 
                uint pay = (price * 9/2); 
                if (random_number == 1) {
                    ticket1.transfer(pay);
                    lastWinner = ticket1; 
                }
                else if(random_number == 2) {
                    ticket2.transfer(pay);
                    lastWinner = ticket2; 
                }
                else if(random_number == 3) {
                    ticket3.transfer(pay);
                    lastWinner = ticket3; 
                }
                else if(random_number == 4) {
                    ticket4.transfer(pay);
                    lastWinner = ticket4; 
                }
                else if(random_number == 5) {
                    ticket5.transfer(pay);
                    lastWinner = ticket5; 
                }
            }
        }
        entry = false;
    }
}
```

## RQ1_2a70f226d760

SHA-256 `9864d748003b1ddff933c58085863ee0e2459317b4502b38811874e5a38f03ea`

```solidity
pragma solidity ^0.4.19;
contract DomRaiderToken {
    string public name = "DomRaider";
    string public symbol = "DRT";
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
    function DomRaiderToken() public {
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

## RQ1_2b47449398dd

SHA-256 `98ec531b167db209a51e25572d189afb112f66d1c0701dadb1a9480871aba4e4`

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
contract IERC223Token is IERC20Token, ITokenMetadata {
    function transfer(address to, uint256 amount, bytes data)
        public
        returns (bool);
}
contract IERC677Allowance is IERC20Allowance {
    function approveAndCall(address spender, uint256 amount, bytes extraData)
        public
        returns (bool success);
}
contract IERC677Token is IERC20Token, IERC677Allowance {
}
contract ITokenControllerHook {
    event LogChangeTokenController(
        address oldController,
        address newController,
        address by
    );
    function changeTokenController(address newController)
        public;
    function tokenController()
        public
        constant
        returns (address currentController);
}
contract IETOCommitmentStates {
    enum ETOState {
        Setup, 
        Whitelist,
        Public,
        Signing,
        Claim,
        Payout, 
        Refund 
    }
    uint256 constant internal ETO_STATES_COUNT = 7;
}
contract IETOCommitmentObserver is IETOCommitmentStates {
    function commitmentObserver() public constant returns (address);
    function onStateTransition(ETOState oldState, ETOState newState) public;
}
contract IERC223Callback {
    function tokenFallback(address from, uint256 amount, bytes data)
        public;
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
contract IEquityTokenController is
    IAgreement,
    ITokenController,
    IETOCommitmentObserver,
    IERC223Callback
{
    function onChangeNominee(address sender, address oldNominee, address newNominee)
        public
        constant
        returns (bool);
}
contract IEquityToken is
    IAgreement,
    IClonedTokenParent,
    IERC223Token,
    ITokenControllerHook
{
    function tokensPerShare() public constant returns (uint256);
    function sharesTotalSupply() public constant returns (uint256);
    function shareNominalValueEurUlps() public constant returns (uint256);
    function companyLegalRepresentative() public constant returns (address);
    function nominee() public constant returns (address);
    function changeNominee(address newNominee) public;
    function issueTokens(uint256 amount) public;
    function distributeTokens(address to, uint256 amount) public;
    function destroyTokens(uint256 amount) public;
}
contract IContractId {
    function contractId() public pure returns (bytes32 id, uint256 version);
}
contract ShareholderRights is IContractId {
    enum VotingRule {
        NoVotingRights,
        Positive,
        Negative,
        Proportional
    }
    bytes32 private constant EMPTY_STRING_HASH = 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470;
    bool public constant HAS_DRAG_ALONG_RIGHTS = true;
    bool public constant HAS_TAG_ALONG_RIGHTS = true;
    bool public constant HAS_GENERAL_INFORMATION_RIGHTS = true;
    VotingRule public GENERAL_VOTING_RULE;
    VotingRule public TAG_ALONG_VOTING_RULE;
    uint256 public LIQUIDATION_PREFERENCE_MULTIPLIER_FRAC;
    bool public HAS_FOUNDERS_VESTING;
    uint256 public GENERAL_VOTING_DURATION;
    uint256 public RESTRICTED_ACT_VOTING_DURATION;
    uint256 public VOTING_FINALIZATION_DURATION;
    uint256 public TOKENHOLDERS_QUORUM_FRAC = 10**17; 
    uint256 public VOTING_MAJORITY_FRAC = 10**17; 
    string public INVESTMENT_AGREEMENT_TEMPLATE_URL;
    constructor(
        VotingRule generalVotingRule,
        VotingRule tagAlongVotingRule,
        uint256 liquidationPreferenceMultiplierFrac,
        bool hasFoundersVesting,
        uint256 generalVotingDuration,
        uint256 restrictedActVotingDuration,
        uint256 votingFinalizationDuration,
        uint256 tokenholdersQuorumFrac,
        uint256 votingMajorityFrac,
        string investmentAgreementTemplateUrl
    )
        public
    {
        require(uint(generalVotingRule) < 4);
        require(uint(tagAlongVotingRule) < 4);
        require(tokenholdersQuorumFrac < 10**18);
        require(keccak256(abi.encodePacked(investmentAgreementTemplateUrl)) != EMPTY_STRING_HASH);
        GENERAL_VOTING_RULE = generalVotingRule;
        TAG_ALONG_VOTING_RULE = tagAlongVotingRule;
        LIQUIDATION_PREFERENCE_MULTIPLIER_FRAC = liquidationPreferenceMultiplierFrac;
        HAS_FOUNDERS_VESTING = hasFoundersVesting;
        GENERAL_VOTING_DURATION = generalVotingDuration;
        RESTRICTED_ACT_VOTING_DURATION = restrictedActVotingDuration;
        VOTING_FINALIZATION_DURATION = votingFinalizationDuration;
        TOKENHOLDERS_QUORUM_FRAC = tokenholdersQuorumFrac;
        VOTING_MAJORITY_FRAC = votingMajorityFrac;
        INVESTMENT_AGREEMENT_TEMPLATE_URL = investmentAgreementTemplateUrl;
    }
    function contractId() public pure returns (bytes32 id, uint256 version) {
        return (0x7f46caed28b4e7a90dc4db9bba18d1565e6c4824f0dc1b96b3b88d730da56e57, 0);
    }
}
contract Math {
    function absDiff(uint256 v1, uint256 v2)
        internal
        pure
        returns(uint256)
    {
        return v1 > v2 ? v1 - v2 : v2 - v1;
    }
    function divRound(uint256 v, uint256 d)
        internal
        pure
        returns(uint256)
    {
        return add(v, d/2) / d;
    }
    function decimalFraction(uint256 amount, uint256 frac)
        internal
        pure
        returns(uint256)
    {
        return proportion(amount, frac, 10**18);
    }
    function proportion(uint256 amount, uint256 part, uint256 total)
        internal
        pure
        returns(uint256)
    {
        return divRound(mul(amount, part), total);
    }
    function mul(uint256 a, uint256 b)
        internal
        pure
        returns (uint256)
    {
        uint256 c = a * b;
        assert(a == 0 || c / a == b);
        return c;
    }
    function sub(uint256 a, uint256 b)
        internal
        pure
        returns (uint256)
    {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b)
        internal
        pure
        returns (uint256)
    {
        uint256 c = a + b;
        assert(c >= a);
        return c;
    }
    function min(uint256 a, uint256 b)
        internal
        pure
        returns (uint256)
    {
        return a < b ? a : b;
    }
    function max(uint256 a, uint256 b)
        internal
        pure
        returns (uint256)
    {
        return a > b ? a : b;
    }
}
contract PlatformTerms is Math, IContractId {
    uint256 public constant PLATFORM_FEE_FRACTION = 3 * 10**16;
    uint256 public constant TOKEN_PARTICIPATION_FEE_FRACTION = 2 * 10**16;
    uint256 public constant PLATFORM_NEUMARK_SHARE = 2; 
    bool public constant IS_ICBM_INVESTOR_WHITELISTED = true;
    uint256 public constant MIN_TICKET_EUR_ULPS = 100 * 10**18;
    uint256 public constant DATE_TO_WHITELIST_MIN_DURATION = 7 days;
    uint256 public constant TOKEN_RATE_EXPIRES_AFTER = 4 hours;
    uint256 public constant MIN_WHITELIST_DURATION = 0 days;
    uint256 public constant MAX_WHITELIST_DURATION = 30 days;
    uint256 public constant MIN_PUBLIC_DURATION = 0 days;
    uint256 public constant MAX_PUBLIC_DURATION = 60 days;
    uint256 public constant MIN_OFFER_DURATION = 1 days;
    uint256 public constant MAX_OFFER_DURATION = 90 days;
    uint256 public constant MIN_SIGNING_DURATION = 14 days;
    uint256 public constant MAX_SIGNING_DURATION = 60 days;
    uint256 public constant MIN_CLAIM_DURATION = 7 days;
    uint256 public constant MAX_CLAIM_DURATION = 30 days;
    uint256 public constant DEFAULT_DISBURSAL_RECYCLE_AFTER_DURATION = 4 * 365 days;
    function calculateNeumarkDistribution(uint256 rewardNmk)
        public
        pure
        returns (uint256 platformNmk, uint256 investorNmk)
    {
        platformNmk = rewardNmk / PLATFORM_NEUMARK_SHARE;
        return (platformNmk, rewardNmk - platformNmk);
    }
    function calculatePlatformTokenFee(uint256 tokenAmount)
        public
        pure
        returns (uint256)
    {
        return proportion(tokenAmount, TOKEN_PARTICIPATION_FEE_FRACTION, 10**18);
    }
    function calculatePlatformFee(uint256 amount)
        public
        pure
        returns (uint256)
    {
        return decimalFraction(amount, PLATFORM_FEE_FRACTION);
    }
    function contractId() public pure returns (bytes32 id, uint256 version) {
        return (0x95482babc4e32de6c4dc3910ee7ae62c8e427efde6bc4e9ce0d6d93e24c39323, 1);
    }
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
contract ETODurationTerms is IContractId {
    uint32 public WHITELIST_DURATION;
    uint32 public PUBLIC_DURATION;
    uint32 public SIGNING_DURATION;
    uint32 public CLAIM_DURATION;
    constructor(
        uint32 whitelistDuration,
        uint32 publicDuration,
        uint32 signingDuration,
        uint32 claimDuration
    )
        public
    {
        WHITELIST_DURATION = whitelistDuration;
        PUBLIC_DURATION = publicDuration;
        SIGNING_DURATION = signingDuration;
        CLAIM_DURATION = claimDuration;
    }
    function contractId() public pure returns (bytes32 id, uint256 version) {
        return (0x5fb50201b453799d95f8a80291b940f1c543537b95bff2e3c78c2e36070494c0, 0);
    }
}
contract ETOTokenTerms is IContractId {
    uint256 public MIN_NUMBER_OF_TOKENS;
    uint256 public MAX_NUMBER_OF_TOKENS;
    uint256 public TOKEN_PRICE_EUR_ULPS;
    uint256 public MAX_NUMBER_OF_TOKENS_IN_WHITELIST;
    uint256 public constant EQUITY_TOKENS_PER_SHARE = 10000;
    uint8 public constant EQUITY_TOKENS_PRECISION = 0; 
    constructor(
        uint256 minNumberOfTokens,
        uint256 maxNumberOfTokens,
        uint256 tokenPriceEurUlps,
        uint256 maxNumberOfTokensInWhitelist
    )
        public
    {
        require(maxNumberOfTokensInWhitelist <= maxNumberOfTokens);
        require(maxNumberOfTokens >= minNumberOfTokens);
        require(minNumberOfTokens >= EQUITY_TOKENS_PER_SHARE, "NF_ETO_TERMS_ONE_SHARE");
        MIN_NUMBER_OF_TOKENS = minNumberOfTokens;
        MAX_NUMBER_OF_TOKENS = maxNumberOfTokens;
        TOKEN_PRICE_EUR_ULPS = tokenPriceEurUlps;
        MAX_NUMBER_OF_TOKENS_IN_WHITELIST = maxNumberOfTokensInWhitelist;
    }
    function contractId() public pure returns (bytes32 id, uint256 version) {
        return (0x591e791aab2b14c80194b729a2abcba3e8cce1918be4061be170e7223357ae5c, 0);
    }
}
contract ETOTerms is
    IdentityRecord,
    Math,
    IContractId
{
    struct WhitelistTicket {
        uint128 discountAmountEurUlps;
        uint128 fullTokenPriceFrac;
    }
    bytes32 private constant EMPTY_STRING_HASH = 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470;
    uint256 public constant MIN_QUALIFIED_INVESTOR_TICKET_EUR_ULPS = 100000 * 10**18;
    ETODurationTerms public DURATION_TERMS;
    ETOTokenTerms public TOKEN_TERMS;
    uint256 public EXISTING_COMPANY_SHARES;
    uint256 public SHARE_NOMINAL_VALUE_EUR_ULPS;
    uint256 public MIN_TICKET_EUR_ULPS;
    uint256 public MAX_TICKET_EUR_ULPS;
    uint256 public MAX_TICKET_SIMPLE_EUR_ULPS;
    bool public ENABLE_TRANSFERS_ON_SUCCESS;
    bool public ALLOW_RETAIL_INVESTORS;
    uint256 public WHITELIST_DISCOUNT_FRAC;
    uint256 public PUBLIC_DISCOUNT_FRAC;
    string public INVESTOR_OFFERING_DOCUMENT_URL;
    ShareholderRights public SHAREHOLDER_RIGHTS;
    string public EQUITY_TOKEN_NAME;
    string public EQUITY_TOKEN_SYMBOL;
    address public WHITELIST_MANAGER;
    IIdentityRegistry public IDENTITY_REGISTRY;
    Universe public UNIVERSE;
    uint256 private MIN_NUMBER_OF_TOKENS;
    uint256 private MAX_NUMBER_OF_TOKENS;
    uint256 private TOKEN_PRICE_EUR_ULPS;
    uint256 private EQUITY_TOKENS_PER_SHARE;
    mapping (address => WhitelistTicket) private _whitelist;
    modifier onlyWhitelistManager() {
        require(msg.sender == WHITELIST_MANAGER);
        _;
    }
    event LogInvestorWhitelisted(
        address indexed investor,
        uint256 discountAmountEurUlps,
        uint256 fullTokenPriceFrac
    );
    constructor(
        Universe universe,
        ETODurationTerms durationTerms,
        ETOTokenTerms tokenTerms,
        uint256 existingCompanyShares,
        uint256 minTicketEurUlps,
        uint256 maxTicketEurUlps,
        bool allowRetailInvestors,
        bool enableTransfersOnSuccess,
        string investorOfferingDocumentUrl,
        ShareholderRights shareholderRights,
        string equityTokenName,
        string equityTokenSymbol,
        uint256 shareNominalValueEurUlps,
        uint256 whitelistDiscountFrac,
        uint256 publicDiscountFrac
    )
        public
    {
        require(durationTerms != address(0));
        require(tokenTerms != address(0));
        require(existingCompanyShares > 0);
        require(keccak256(abi.encodePacked(investorOfferingDocumentUrl)) != EMPTY_STRING_HASH);
        require(keccak256(abi.encodePacked(equityTokenName)) != EMPTY_STRING_HASH);
        require(keccak256(abi.encodePacked(equityTokenSymbol)) != EMPTY_STRING_HASH);
        require(shareholderRights != address(0));
        require(shareholderRights.HAS_GENERAL_INFORMATION_RIGHTS());
        require(shareNominalValueEurUlps > 0);
        require(whitelistDiscountFrac >= 0 && whitelistDiscountFrac <= 99*10**16);
        require(publicDiscountFrac >= 0 && publicDiscountFrac <= 99*10**16);
        require(minTicketEurUlps<=maxTicketEurUlps);
        require(tokenTerms.EQUITY_TOKENS_PRECISION() == 0);
        MIN_NUMBER_OF_TOKENS = tokenTerms.MIN_NUMBER_OF_TOKENS();
        MAX_NUMBER_OF_TOKENS = tokenTerms.MAX_NUMBER_OF_TOKENS();
        TOKEN_PRICE_EUR_ULPS = tokenTerms.TOKEN_PRICE_EUR_ULPS();
        EQUITY_TOKENS_PER_SHARE = tokenTerms.EQUITY_TOKENS_PER_SHARE();
        DURATION_TERMS = durationTerms;
        TOKEN_TERMS = tokenTerms;
        EXISTING_COMPANY_SHARES = existingCompanyShares;
        MIN_TICKET_EUR_ULPS = minTicketEurUlps;
        MAX_TICKET_EUR_ULPS = maxTicketEurUlps;
        ALLOW_RETAIL_INVESTORS = allowRetailInvestors;
        ENABLE_TRANSFERS_ON_SUCCESS = enableTransfersOnSuccess;
        INVESTOR_OFFERING_DOCUMENT_URL = investorOfferingDocumentUrl;
        SHAREHOLDER_RIGHTS = shareholderRights;
        EQUITY_TOKEN_NAME = equityTokenName;
        EQUITY_TOKEN_SYMBOL = equityTokenSymbol;
        SHARE_NOMINAL_VALUE_EUR_ULPS = shareNominalValueEurUlps;
        WHITELIST_DISCOUNT_FRAC = whitelistDiscountFrac;
        PUBLIC_DISCOUNT_FRAC = publicDiscountFrac;
        WHITELIST_MANAGER = msg.sender;
        IDENTITY_REGISTRY = IIdentityRegistry(universe.identityRegistry());
        UNIVERSE = universe;
    }
    function calculateTokenAmount(uint256 , uint256 committedEurUlps)
        public
        constant
        returns (uint256 tokenAmountInt)
    {
        return committedEurUlps / calculatePriceFraction(10**18 - PUBLIC_DISCOUNT_FRAC);
    }
    function calculateEurUlpsAmount(uint256 , uint256 tokenAmountInt)
        public
        constant
        returns (uint256 committedEurUlps)
    {
        return mul(tokenAmountInt, calculatePriceFraction(10**18 - PUBLIC_DISCOUNT_FRAC));
    }
    function ESTIMATED_MIN_CAP_EUR_ULPS() public constant returns(uint256) {
        return calculateEurUlpsAmount(0, MIN_NUMBER_OF_TOKENS);
    }
    function ESTIMATED_MAX_CAP_EUR_ULPS() public constant returns(uint256) {
        return calculateEurUlpsAmount(0, MAX_NUMBER_OF_TOKENS);
    }
    function calculatePriceFraction(uint256 priceFrac) public constant returns(uint256) {
        if (priceFrac == 1) {
            return TOKEN_PRICE_EUR_ULPS;
        } else {
            return decimalFraction(priceFrac, TOKEN_PRICE_EUR_ULPS);
        }
    }
    function equityTokensToShares(uint256 amount)
        public
        constant
        returns (uint256)
    {
        return proportion(amount, 10**18, EQUITY_TOKENS_PER_SHARE);
    }
    function addWhitelisted(
        address[] investors,
        uint256[] discountAmountsEurUlps,
        uint256[] discountsFrac
    )
        external
        onlyWhitelistManager
    {
        require(investors.length == discountAmountsEurUlps.length);
        require(investors.length == discountsFrac.length);
        for (uint256 i = 0; i < investors.length; i += 1) {
            addWhitelistInvestorPrivate(investors[i], discountAmountsEurUlps[i], discountsFrac[i]);
        }
    }
    function whitelistTicket(address investor)
        public
        constant
        returns (bool isWhitelisted, uint256 discountAmountEurUlps, uint256 fullTokenPriceFrac)
    {
        WhitelistTicket storage wlTicket = _whitelist[investor];
        isWhitelisted = wlTicket.fullTokenPriceFrac > 0;
        discountAmountEurUlps = wlTicket.discountAmountEurUlps;
        fullTokenPriceFrac = wlTicket.fullTokenPriceFrac;
    }
    function calculateContribution(
        address investor,
        uint256 totalContributedEurUlps,
        uint256 existingInvestorContributionEurUlps,
        uint256 newInvestorContributionEurUlps,
        bool applyWhitelistDiscounts
    )
        public
        constant
        returns (
            bool isWhitelisted,
            bool isEligible,
            uint256 minTicketEurUlps,
            uint256 maxTicketEurUlps,
            uint256 equityTokenInt,
            uint256 fixedSlotEquityTokenInt
            )
    {
        (
            isWhitelisted,
            minTicketEurUlps,
            maxTicketEurUlps,
            equityTokenInt,
            fixedSlotEquityTokenInt
        ) = calculateContributionPrivate(
            investor,
            totalContributedEurUlps,
            existingInvestorContributionEurUlps,
            newInvestorContributionEurUlps,
            applyWhitelistDiscounts);
        IdentityClaims memory claims = deserializeClaims(IDENTITY_REGISTRY.getClaims(investor));
        isEligible = claims.isVerified && !claims.accountFrozen;
    }
    function requireValidTerms(PlatformTerms platformTerms)
        public
        constant
        returns (bool)
    {
        if (ALLOW_RETAIL_INVESTORS) {
            require(!ENABLE_TRANSFERS_ON_SUCCESS, "NF_MUST_DISABLE_TRANSFERS");
        } else {
            require(MIN_TICKET_EUR_ULPS >= MIN_QUALIFIED_INVESTOR_TICKET_EUR_ULPS, "NF_MIN_QUALIFIED_INVESTOR_TICKET");
        }
        require(MIN_TICKET_EUR_ULPS >= TOKEN_TERMS.TOKEN_PRICE_EUR_ULPS(), "NF_MIN_TICKET_LT_TOKEN_PRICE");
        require(ESTIMATED_MAX_CAP_EUR_ULPS() >= MIN_TICKET_EUR_ULPS, "NF_MAX_FUNDS_LT_MIN_TICKET");
        require(MIN_TICKET_EUR_ULPS >= platformTerms.MIN_TICKET_EUR_ULPS(), "NF_ETO_TERMS_MIN_TICKET_EUR_ULPS");
        require(DURATION_TERMS.WHITELIST_DURATION() >= platformTerms.MIN_WHITELIST_DURATION(), "NF_ETO_TERMS_WL_D_MIN");
        require(DURATION_TERMS.WHITELIST_DURATION() <= platformTerms.MAX_WHITELIST_DURATION(), "NF_ETO_TERMS_WL_D_MAX");
        require(DURATION_TERMS.PUBLIC_DURATION() >= platformTerms.MIN_PUBLIC_DURATION(), "NF_ETO_TERMS_PUB_D_MIN");
        require(DURATION_TERMS.PUBLIC_DURATION() <= platformTerms.MAX_PUBLIC_DURATION(), "NF_ETO_TERMS_PUB_D_MAX");
        uint256 totalDuration = DURATION_TERMS.WHITELIST_DURATION() + DURATION_TERMS.PUBLIC_DURATION();
        require(totalDuration >= platformTerms.MIN_OFFER_DURATION(), "NF_ETO_TERMS_TOT_O_MIN");
        require(totalDuration <= platformTerms.MAX_OFFER_DURATION(), "NF_ETO_TERMS_TOT_O_MAX");
        require(DURATION_TERMS.SIGNING_DURATION() >= platformTerms.MIN_SIGNING_DURATION(), "NF_ETO_TERMS_SIG_MIN");
        require(DURATION_TERMS.SIGNING_DURATION() <= platformTerms.MAX_SIGNING_DURATION(), "NF_ETO_TERMS_SIG_MAX");
        require(DURATION_TERMS.CLAIM_DURATION() >= platformTerms.MIN_CLAIM_DURATION(), "NF_ETO_TERMS_CLAIM_MIN");
        require(DURATION_TERMS.CLAIM_DURATION() <= platformTerms.MAX_CLAIM_DURATION(), "NF_ETO_TERMS_CLAIM_MAX");
        return true;
    }
    function contractId() public pure returns (bytes32 id, uint256 version) {
        return (0x3468b14073c33fa00ee7f8a289b14f4a10c78ab72726033b27003c31c47b3f6a, 0);
    }
    function calculateContributionPrivate(
        address investor,
        uint256 totalContributedEurUlps,
        uint256 existingInvestorContributionEurUlps,
        uint256 newInvestorContributionEurUlps,
        bool applyWhitelistDiscounts
    )
        private
        constant
        returns (
            bool isWhitelisted,
            uint256 minTicketEurUlps,
            uint256 maxTicketEurUlps,
            uint256 equityTokenInt,
            uint256 fixedSlotEquityTokenInt
        )
    {
        uint256 discountedAmount;
        minTicketEurUlps = MIN_TICKET_EUR_ULPS;
        maxTicketEurUlps = MAX_TICKET_EUR_ULPS;
        WhitelistTicket storage wlTicket = _whitelist[investor];
        isWhitelisted = wlTicket.fullTokenPriceFrac > 0;
        if (applyWhitelistDiscounts) {
            maxTicketEurUlps = max(wlTicket.discountAmountEurUlps, maxTicketEurUlps);
            if (wlTicket.discountAmountEurUlps > 0) {
                minTicketEurUlps = min(wlTicket.discountAmountEurUlps, minTicketEurUlps);
            }
            if (existingInvestorContributionEurUlps < wlTicket.discountAmountEurUlps) {
                discountedAmount = min(newInvestorContributionEurUlps, wlTicket.discountAmountEurUlps - existingInvestorContributionEurUlps);
                if (discountedAmount > 0) {
                    fixedSlotEquityTokenInt = discountedAmount / calculatePriceFraction(wlTicket.fullTokenPriceFrac);
                }
            }
        }
        uint256 remainingAmount = newInvestorContributionEurUlps - discountedAmount;
        if (remainingAmount > 0) {
            if (applyWhitelistDiscounts && WHITELIST_DISCOUNT_FRAC > 0) {
                equityTokenInt = remainingAmount / calculatePriceFraction(10**18 - WHITELIST_DISCOUNT_FRAC);
            } else {
                equityTokenInt = calculateTokenAmount(totalContributedEurUlps + discountedAmount, remainingAmount);
            }
        }
        equityTokenInt += fixedSlotEquityTokenInt;
    }
    function addWhitelistInvestorPrivate(
        address investor,
        uint256 discountAmountEurUlps,
        uint256 fullTokenPriceFrac
    )
        private
    {
        require(investor != address(0));
        require(fullTokenPriceFrac > 0 && fullTokenPriceFrac <= 10**18, "NF_DISCOUNT_RANGE");
        require(discountAmountEurUlps < 2**128);
        _whitelist[investor] = WhitelistTicket({
            discountAmountEurUlps: uint128(discountAmountEurUlps),
            fullTokenPriceFrac: uint128(fullTokenPriceFrac)
        });
        emit LogInvestorWhitelisted(investor, discountAmountEurUlps, fullTokenPriceFrac);
    }
}
contract ICommitment is
    IAgreement,
    IERC223Callback
{
    event LogFundsCommitted(
        address indexed investor,
        address wallet,
        address paymentToken,
        uint256 amount,
        uint256 baseCurrencyEquivalent,
        uint256 grantedAmount,
        address assetToken,
        uint256 neuReward
    );
    function finalized() public constant returns (bool);
    function success() public constant returns (bool);
    function failed() public constant returns (bool);
    function totalInvestment()
        public
        constant
        returns (
            uint256 totalEquivEurUlps,
            uint256 totalTokensInt,
            uint256 totalInvestors
        );
    function tokenFallback(address investor, uint256 amount, bytes data)
        public;
}
contract IETOCommitment is
    ICommitment,
    IETOCommitmentStates
{
    event LogStateTransition(
        uint32 oldState,
        uint32 newState,
        uint32 timestamp
    );
    event LogTokensClaimed(
        address indexed investor,
        address indexed assetToken,
        uint256 amount,
        uint256 nmkReward
    );
    event LogFundsRefunded(
        address indexed investor,
        address indexed paymentToken,
        uint256 amount
    );
    event LogTermsSet(
        address companyLegalRep,
        address etoTerms,
        address equityToken
    );
    event LogETOStartDateSet(
        address companyLegalRep,
        uint256 previousTimestamp,
        uint256 newTimestamp
    );
    event LogSigningStarted(
        address nominee,
        address companyLegalRep,
        uint256 newShares,
        uint256 capitalIncreaseEurUlps
    );
    event LogCompanySignedAgreement(
        address companyLegalRep,
        address nominee,
        string signedInvestmentAgreementUrl
    );
    event LogNomineeConfirmedAgreement(
        address nominee,
        address companyLegalRep,
        string signedInvestmentAgreementUrl
    );
    event LogRefundStarted(
        address assetToken,
        uint256 totalTokenAmountInt,
        uint256 totalRewardNmkUlps
    );
    function state() public constant returns (ETOState);
    function startOf(ETOState s) public constant returns (uint256);
    function commitmentObserver() public constant returns (IETOCommitmentObserver);
    function refund() external;
    function refundMany(address[] investors) external;
    function claim() external;
    function claimMany(address[] investors) external;
    function payout() external;
    function etoTerms() public constant returns (ETOTerms);
    function equityToken() public constant returns (IEquityToken);
    function nominee() public constant returns (address);
    function companyLegalRep() public constant returns (address);
    function signedInvestmentAgreementUrl() public constant returns (string);
    function contributionSummary()
        public
        constant
        returns (
            uint256 newShares, uint256 capitalIncreaseEurUlps,
            uint256 additionalContributionEth, uint256 additionalContributionEurUlps,
            uint256 tokenParticipationFeeInt, uint256 platformFeeEth, uint256 platformFeeEurUlps,
            uint256 sharePriceEurUlps
        );
    function investorTicket(address investor)
        public
        constant
        returns (
            uint256 equivEurUlps,
            uint256 rewardNmkUlps,
            uint256 equityTokenInt,
            uint256 sharesInt,
            uint256 tokenPrice,
            uint256 neuRate,
            uint256 amountEth,
            uint256 amountEurUlps,
            bool claimOrRefundSettled,
            bool usedLockedAccount
        );
}
contract IControllerGovernance is
    IAgreement
{
    enum GovState {
        Setup, 
        Offering, 
        Funded, 
        Closing, 
        Closed, 
        Migrated 
    }
    enum Action {
        None, 
        StopToken, 
        ContinueToken, 
        CloseToken, 
        Payout, 
        RegisterOffer, 
        ChangeTokenController, 
        AmendISHA, 
        IssueTokensForExistingShares, 
        ChangeNominee,
        Downround 
    }
    event LogGovStateTransition(
        uint32 oldState,
        uint32 newState,
        uint32 timestamp
    );
    event LogResolutionExecuted(
        bytes32 resolutionId,
        Action action
    );
    event LogTransfersStateChanged(
        bytes32 resolutionId,
        address equityToken,
        bool transfersEnabled
    );
    event LogISHAAmended(
        bytes32 resolutionId,
        string ISHAUrl,
        uint256 totalShares,
        uint256 companyValuationEurUlps,
        address newShareholderRights
    );
    event LogOfferingFailed(
        address etoCommitment,
        address equityToken
    );
    event LogOfferingSucceeded(
        address etoCommitment,
        address equityToken,
        uint256 newShares
    );
    event LogGeneralInformation(
        address companyLegalRep,
        string informationType,
        string informationUrl
    );
    event LogOfferingRegistered(
        bytes32 resolutionId,
        address etoCommitment,
        address equityToken
    );
    event LogMigratedTokenController(
        bytes32 resolutionId,
        address newController
    );
    function state()
        public
        constant
        returns (GovState);
    function companyLegalRepresentative()
        public
        constant
        returns (address);
    function shareholderInformation()
        public
        constant
        returns (
            uint256 totalCompanyShares,
            uint256 companyValuationEurUlps,
            ShareholderRights shareholderRights
        );
    function capTable()
        public
        constant
        returns (
            address[] equityTokens,
            uint256[] shares
        );
    function tokenOfferings()
        public
        constant
        returns (
            address[] offerings,
            address[] equityTokens
        );
    function issueGeneralInformation(
        string informationType,
        string informationUrl
    )
        public;
    function startResolution(string title, string resolutionUri, Action action, bytes payload)
        public
        returns (bytes32 resolutionId);
    function executeResolution(bytes32 resolutionId) public;
    function closeCompany() public;
    function cancelCompanyClosing() public;
    function changeTokenController(IControllerGovernance newController) public;
    function newTokenController() public constant returns (address);
    function oldTokenController() public constant returns (address);
}
contract PlaceholderEquityTokenController is
    IEquityTokenController,
    IControllerGovernance,
    IContractId,
    Agreement,
    KnownInterfaces
{
    Universe private UNIVERSE;
    address private COMPANY_LEGAL_REPRESENTATIVE;
    address private OLD_TOKEN_CONTROLLER;
    GovState private _state;
    uint256 private _totalCompanyShares;
    uint256 private _companyValuationEurUlps;
    ShareholderRights private _shareholderRights;
    address private _newController;
    IEquityToken private _equityToken;
    address private _commitment;
    bool private _transfersEnabled;
    modifier onlyUniverseETO() {
        require(UNIVERSE.isInterfaceCollectionInstance(KNOWN_INTERFACE_COMMITMENT, msg.sender), "NF_ETC_ETO_NOT_U");
        _;
    }
    modifier onlyCompany() {
        require(msg.sender == COMPANY_LEGAL_REPRESENTATIVE, "NF_ONLY_COMPANY");
        _;
    }
    modifier onlyOperational() {
        require(_state == GovState.Offering || _state == GovState.Funded || _state == GovState.Closing, "NF_INV_STATE");
        _;
    }
    modifier onlyState(GovState state) {
        require(_state == state, "NF_INV_STATE");
        _;
    }
    modifier onlyStates(GovState state1, GovState state2) {
        require(_state == state1 || _state == state2, "NF_INV_STATE");
        _;
    }
    constructor(
        Universe universe,
        address companyLegalRep
    )
        public
        Agreement(universe.accessPolicy(), universe.forkArbiter())
    {
        UNIVERSE = universe;
        COMPANY_LEGAL_REPRESENTATIVE = companyLegalRep;
    }
    function state()
        public
        constant
        returns (GovState)
    {
        return _state;
    }
    function companyLegalRepresentative()
        public
        constant
        returns (address)
    {
        return COMPANY_LEGAL_REPRESENTATIVE;
    }
    function shareholderInformation()
        public
        constant
        returns (
            uint256 totalCompanyShares,
            uint256 companyValuationEurUlps,
            ShareholderRights shareholderRights
        )
    {
        return (
            _totalCompanyShares,
            _companyValuationEurUlps,
            _shareholderRights
        );
    }
    function capTable()
        public
        constant
        returns (
            address[] equityTokens,
            uint256[] shares
        )
    {
        if (_state == GovState.Setup || _state == GovState.Offering) {
            return;
        }
        equityTokens = new address[](1);
        shares = new uint256[](1);
        equityTokens[0] = _equityToken;
        shares[0] = _equityToken.sharesTotalSupply();
    }
    function tokenOfferings()
        public
        constant
        returns (
            address[] offerings,
            address[] equityTokens
        )
    {
        if (_state == GovState.Setup) {
            return;
        }
        offerings = new address[](1);
        equityTokens = new address[](1);
        equityTokens[0] = _equityToken;
        offerings[0] = _commitment;
    }
    function issueGeneralInformation(
        string informationType,
        string informationUrl
    )
        public
        onlyOperational
        onlyCompany
    {
        emit LogGeneralInformation(COMPANY_LEGAL_REPRESENTATIVE, informationType, informationUrl);
    }
    function startResolution(string , string , Action , bytes )
        public
        onlyStates(GovState.Offering, GovState.Funded)
        onlyCompany
        returns (bytes32 )
    {
        revert("NF_NOT_IMPL");
    }
    function executeResolution(bytes32 )
        public
        onlyOperational
    {
        revert("NF_NOT_IMPL");
    }
    function closeCompany()
        public
        onlyState(GovState.Closing)
    {
        revert("NF_NOT_IMPL");
    }
    function cancelCompanyClosing()
        public
        onlyState(GovState.Closing)
    {
        revert("NF_NOT_IMPL");
    }
    function changeTokenController(IControllerGovernance newController)
        public
        onlyStates(GovState.Funded, GovState.Closed)
        onlyCompany
    {
        require(newController != address(this));
        require(newController.oldTokenController() == address(this), "NF_NOT_MIGRATED_FROM_US");
        _newController = newController;
        transitionTo(GovState.Migrated);
        emit LogResolutionExecuted(0, Action.ChangeTokenController);
        emit LogMigratedTokenController(0, newController);
    }
    function newTokenController()
        public
        constant
        returns (address)
    {
        return _newController;
    }
    function oldTokenController()
        public
        constant
        returns (address)
    {
        return OLD_TOKEN_CONTROLLER;
    }
    function onTransfer(address broker, address from, address , uint256 )
        public
        constant
        returns (bool allow)
    {
        return _transfersEnabled || (from == _commitment && broker == from);
    }
    function onApprove(address, address, uint256)
        public
        constant
        returns (bool allow)
    {
        return true;
    }
    function onGenerateTokens(address sender, address, uint256)
        public
        constant
        returns (bool allow)
    {
        return sender == _commitment && _state == GovState.Offering;
    }
    function onDestroyTokens(address sender, address, uint256)
        public
        constant
        returns (bool allow)
    {
        return sender == _commitment && _state == GovState.Offering;
    }
    function onChangeTokenController(address , address newController)
        public
        constant
        returns (bool)
    {
        return newController == _newController;
    }
    function onAllowance(address , address )
        public
        constant
        returns (uint256)
    {
        return 0;
    }
    function onChangeNominee(address, address, address)
        public
        constant
        returns (bool)
    {
        return false;
    }
    function tokenFallback(address, uint256, bytes)
        public
    {
        revert("NF_NOT_IMPL");
    }
    function commitmentObserver() public
        constant
        returns (address)
    {
        return _commitment;
    }
    function onStateTransition(ETOState, ETOState newState)
        public
        onlyUniverseETO
    {
        if (newState == ETOState.Whitelist) {
            require(_state == GovState.Setup, "NF_ETC_BAD_STATE");
            registerTokenOfferingPrivate(IETOCommitment(msg.sender));
            return;
        }
        require(msg.sender == _commitment, "NF_ETC_UNREG_COMMITMENT");
        if (newState == ETOState.Claim) {
            require(_state == GovState.Offering, "NF_ETC_BAD_STATE");
            aproveTokenOfferingPrivate(IETOCommitment(msg.sender));
        }
        if (newState == ETOState.Refund) {
            require(_state == GovState.Offering, "NF_ETC_BAD_STATE");
            failTokenOfferingPrivate(IETOCommitment(msg.sender));
        }
    }
    function contractId() public pure returns (bytes32 id, uint256 version) {
        return (0xf7e00d1a4168be33cbf27d32a37a5bc694b3a839684a8c2bef236e3594345d70, 1);
    }
    function migrateTokenController(IControllerGovernance oldController, bool transfersEnables)
        public
        onlyState(GovState.Setup)
        onlyCompany
    {
        require(oldController.newTokenController() == address(0), "NF_OLD_CONTROLLED_ALREADY_MIGRATED");
        (address[] memory equityTokens, ) = oldController.capTable();
        (address[] memory offerings, ) = oldController.tokenOfferings();
        (,,string memory ISHAUrl,) = oldController.currentAgreement();
        (
            _totalCompanyShares,
            _companyValuationEurUlps,
            _shareholderRights
        ) = oldController.shareholderInformation();
        _equityToken = IEquityToken(equityTokens[0]);
        _commitment = offerings[0];
        this.amendAgreement(ISHAUrl);
        enableTransfers(transfersEnables);
        transitionTo(GovState.Funded);
        OLD_TOKEN_CONTROLLER = oldController;
    }
    function newOffering(IEquityToken equityToken, address tokenOffering)
        internal
    {
        _equityToken = equityToken;
        _commitment = tokenOffering;
        emit LogResolutionExecuted(0, Action.RegisterOffer);
        emit LogOfferingRegistered(0, tokenOffering, equityToken);
    }
    function amendISHA(
        string memory ISHAUrl,
        uint256 totalShares,
        uint256 companyValuationEurUlps,
        ShareholderRights newShareholderRights
    )
        internal
    {
        this.amendAgreement(ISHAUrl);
        _totalCompanyShares = totalShares;
        _companyValuationEurUlps = companyValuationEurUlps;
        _shareholderRights = newShareholderRights;
        emit LogResolutionExecuted(0, Action.AmendISHA);
        emit LogISHAAmended(0, ISHAUrl, totalShares, companyValuationEurUlps, newShareholderRights);
    }
    function enableTransfers(bool transfersEnabled)
        internal
    {
        if (_transfersEnabled != transfersEnabled) {
            _transfersEnabled = transfersEnabled;
        }
        emit LogResolutionExecuted(0, transfersEnabled ? Action.ContinueToken : Action.StopToken);
        emit LogTransfersStateChanged(0, _equityToken, transfersEnabled);
    }
    function transitionTo(GovState newState)
        internal
    {
        emit LogGovStateTransition(uint32(_state), uint32(newState), uint32(block.timestamp));
        _state = newState;
    }
    function mCanAmend(address legalRepresentative)
        internal
        returns (bool)
    {
        return legalRepresentative == address(this);
    }
    function registerTokenOfferingPrivate(IETOCommitment tokenOffering)
        private
    {
        IEquityToken equityToken = tokenOffering.equityToken();
        (address nomineeToken,,,) = equityToken.currentAgreement();
        require(equityToken.tokenController() == address(this), "NF_NDT_ET_TC_MIS");
        (address nomineOffering,,,) = tokenOffering.currentAgreement();
        require(nomineOffering == nomineeToken, "NF_NDT_ETO_A_MIS");
        require(tokenOffering.etoTerms() != address(0), "NF_NDT_ETO_NO_TERMS");
        require(tokenOffering.companyLegalRep() == COMPANY_LEGAL_REPRESENTATIVE, "NF_NDT_ETO_LREP_MIS");
        newOffering(equityToken, tokenOffering);
        transitionTo(GovState.Offering);
    }
    function aproveTokenOfferingPrivate(IETOCommitment tokenOffering)
        private
    {
        (uint256 newShares,,,,,,,) = tokenOffering.contributionSummary();
        uint256 totalShares = tokenOffering.etoTerms().EXISTING_COMPANY_SHARES() + newShares;
        uint256 marginalTokenPrice = tokenOffering.etoTerms().TOKEN_TERMS().TOKEN_PRICE_EUR_ULPS();
        string memory ISHAUrl = tokenOffering.signedInvestmentAgreementUrl();
        amendISHA(
            ISHAUrl,
            totalShares,
            totalShares * marginalTokenPrice * tokenOffering.etoTerms().TOKEN_TERMS().EQUITY_TOKENS_PER_SHARE(),
            tokenOffering.etoTerms().SHAREHOLDER_RIGHTS()
        );
        enableTransfers(tokenOffering.etoTerms().ENABLE_TRANSFERS_ON_SUCCESS());
        transitionTo(GovState.Funded);
        emit LogOfferingSucceeded(tokenOffering, tokenOffering.equityToken(), newShares);
    }
    function failTokenOfferingPrivate(IETOCommitment tokenOffering)
        private
    {
        _equityToken = IEquityToken(0);
        _commitment = IETOCommitment(0);
        _totalCompanyShares = 0;
        _companyValuationEurUlps = 0;
        transitionTo(GovState.Setup);
        emit LogOfferingFailed(tokenOffering, tokenOffering.equityToken());
    }
}
```

## RQ1_155abf47bb4c

SHA-256 `7825146ccad1eb67913c20793bcce15303684a6df336076f049392e5a66aaff8`

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

## RQ1_eb323d4d8ca9

SHA-256 `9c9cfda8bbb870fac50462e62ef7b1d7cb360243d7e3674400b81ca6cffba31e`

```solidity
pragma solidity ^0.4.19;
contract AtlantToken {
    string public name = "Atlant Token";
    string public symbol = "ATL";
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
    function AtlantToken() public {
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

## RQ1_e35c80271bc7

SHA-256 `993913836ee5adf6a80c447191bdc90f8da6d1a99c5d9093c9757340cf928709`

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

SHA-256 `5259621f69ffcb680f63276c899d6ddd4e60b63d140c934c6937540cd47bf9f3`

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

## RQ1_4bae85054465

SHA-256 `0b78de22c7e06af2cdd431b86acaa863d9586a4b5d4917ca3d03c90780d0557b`

```solidity
pragma solidity 0.4.24;
contract ERC20Basic {
  function totalSupply() public view returns (uint256);
  function balanceOf(address _who) public view returns (uint256);
  function transfer(address _to, uint256 _value) public returns (bool);
  event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
  function allowance(address _owner, address _spender)
    public view returns (uint256);
  function transferFrom(address _from, address _to, uint256 _value)
    public returns (bool);
  function approve(address _spender, uint256 _value) public returns (bool);
  event Approval(
    address indexed owner,
    address indexed spender,
    uint256 value
  );
}
contract DetailedERC20 is ERC20 {
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
contract BasicToken is ERC20Basic {
  using SafeMath for uint256;
  mapping(address => uint256) internal balances;
  uint256 internal totalSupply_;
  function totalSupply() public view returns (uint256) {
    return totalSupply_;
  }
  function transfer(address _to, uint256 _value) public returns (bool) {
    require(_value <= balances[msg.sender]);
    require(_to != address(0));
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
  mapping (address => mapping (address => uint256)) internal allowed;
  function transferFrom(
    address _from,
    address _to,
    uint256 _value
  )
    public
    returns (bool)
  {
    require(_value <= balances[_from]);
    require(_value <= allowed[_from][msg.sender]);
    require(_to != address(0));
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
  function allowance(
    address _owner,
    address _spender
   )
    public
    view
    returns (uint256)
  {
    return allowed[_owner][_spender];
  }
  function increaseApproval(
    address _spender,
    uint256 _addedValue
  )
    public
    returns (bool)
  {
    allowed[msg.sender][_spender] = (
      allowed[msg.sender][_spender].add(_addedValue));
    emit Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
    return true;
  }
  function decreaseApproval(
    address _spender,
    uint256 _subtractedValue
  )
    public
    returns (bool)
  {
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
contract VaultToken is DetailedERC20, StandardToken, Ownable {
  string public name = "Vault Smart Security";
  string public symbol = "VSS";
  uint8 public decimals = 18;
  uint public initialSupply = 10000000000 * 10 ** uint256(decimals);
  mapping (address => bool) public frozenAccount;
  event FrozenFunds(address target, bool frozen);
  constructor() DetailedERC20(name, symbol, decimals) public {
    totalSupply_ = initialSupply;
    balances[msg.sender] = totalSupply_;
    emit Transfer(address(0), owner, totalSupply_);
  }
  function transfer(address _to, uint256 _value) public returns (bool){
    _transfer(msg.sender, _to, _value);
  }
  function _transfer(address _from, address _to, uint _value) internal {
        require (_to != address(0));
        require (balances[_from] >= _value);               
        require (balances[_to].add(_value) >= balances[_to]); 
        require(!frozenAccount[_from]);                  
        require(!frozenAccount[_to]);                     
        balances[_from] = balances[_from].sub(_value); 
        balances[_to] = balances[_to].add(_value);        
        emit Transfer(_from, _to, _value);
  }
  function freezeAccount(address target, bool freeze) onlyOwner public {
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
  }
}
```

## RQ1_d6e00d8f7f56

SHA-256 `dea305b18eb27682c3646eea31089984255dfaa1958fdc997e781ea6b2a71ebd`

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
    bool public lockSupply; 
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
    modifier supplyLock() { 
        require(lockSupply == false);
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
    function setSupplyLock(bool _set) onlyAdmin public { 
        lockSupply = _set;
        SetSupplyLock(_set);
    }
    function setTransferLock(bool _set) onlyAdmin public { 
        lockTransfer = _set;
        SetTransferLock(_set);
    }
    event AllowedSet(address _to);
    event SetSupplyLock(bool _set);
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
    function mintToken(address _target, uint256 _mintedAmount) onlyAdmin supplyLock public {
        balances[_target] = SafeMath.add(balances[_target], _mintedAmount);
        totalSupply = SafeMath.add(totalSupply, _mintedAmount);
        Transfer(0, this, _mintedAmount);
        Transfer(this, _target, _mintedAmount);
    }
    function burnToken(address _target, uint256 _burnedAmount) onlyAdmin supplyLock public {
        balances[_target] = SafeMath.sub(balances[_target], _burnedAmount);
        totalSupply = SafeMath.sub(totalSupply, _burnedAmount);
        Burned(_target, _burnedAmount);
    }
    function setFrozen(address _target,bool _flag) onlyAdmin public {
        frozen[_target]=_flag;
        FrozenStatus(_target,_flag);
    }
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Burned(address indexed _target, uint256 _value);
    event FrozenStatus(address _target,bool _flag);
}
contract Asset is ERC20Token {
    string public name = 'Digital Safe Coin';
    uint8 public decimals = 1;
    string public symbol = 'DSC';
    string public version = '1';
    function Asset() public {
        totalSupply = 500000000 * (10**uint256(decimals));          
        balances[msg.sender] = 300000000 * (10**uint256(decimals)); 
        balances[0x9caC17210aAc675E39b7fd6B9182eF5eBe724EC8] = 100000000 * (10**uint256(decimals));
        balances[0x3B41bFA39241CDF7afeF807087774e27fd01a1b2] = 50000000 * (10**uint256(decimals));
        balances[0xBa52E579C7296A6B45D724CD8163966eEdC5997a] = 49500000 * (10**uint256(decimals));
        balances[0xFAB6368b0F7be60c573a6562d82469B5ED9e7eE6] = 500000 * (10**uint256(decimals));  
        Transfer(0, this, totalSupply);
        Transfer(this, msg.sender, balances[msg.sender]);
        Transfer(this, 0x9caC17210aAc675E39b7fd6B9182eF5eBe724EC8, balances[0x9caC17210aAc675E39b7fd6B9182eF5eBe724EC8]);
        Transfer(this, 0x3B41bFA39241CDF7afeF807087774e27fd01a1b2, balances[0x3B41bFA39241CDF7afeF807087774e27fd01a1b2]);
        Transfer(this, 0xBa52E579C7296A6B45D724CD8163966eEdC5997a, balances[0xBa52E579C7296A6B45D724CD8163966eEdC5997a]);
        Transfer(this, 0xFAB6368b0F7be60c573a6562d82469B5ED9e7eE6, balances[0xFAB6368b0F7be60c573a6562d82469B5ED9e7eE6]);
    }
    function() public {
        revert();
    }
}
```

## RQ1_37498e68783c

SHA-256 `e5b8040b557a0933b740d08d561754a0d77a6eaeb68165b3848ffdb911c48b2a`

```solidity
pragma solidity 0.4.25;
contract OwnedI {
    event LogOwnerChanged(address indexed previousOwner, address indexed newOwner);
    function getOwner()
        view public
        returns (address);
    function setOwner(address newOwner)
        public
        returns (bool success); 
}
contract Owned is OwnedI {
    address private owner;
    constructor() public {
        owner = msg.sender;
    }
    modifier fromOwner {
        require(msg.sender == owner);
        _;
    }
    function getOwner()
        view public
        returns (address) {
        return owner;
    }
    function setOwner(address newOwner)
        fromOwner public
        returns (bool success) {
        require(newOwner != 0);
        if (owner != newOwner) {
            emit LogOwnerChanged(owner, newOwner);
            owner = newOwner;
        }
        success = true;
    }
}
contract WithBeneficiary is Owned {
    address private beneficiary;
    event LogBeneficiarySet(address indexed previousBeneficiary, address indexed newBeneficiary);
    constructor(address _beneficiary) payable public {
        require(_beneficiary != 0);
        beneficiary = _beneficiary;
        if (msg.value > 0) {
            asyncSend(beneficiary, msg.value);
        }
    }
    function asyncSend(address dest, uint amount) internal;
    function getBeneficiary()
        view public
        returns (address) {
        return beneficiary;
    }
    function setBeneficiary(address newBeneficiary)
        fromOwner public
        returns (bool success) {
        require(newBeneficiary != 0);
        if (beneficiary != newBeneficiary) {
            emit LogBeneficiarySet(beneficiary, newBeneficiary);
            beneficiary = newBeneficiary;
        }
        success = true;
    }
    function () payable public {
        asyncSend(beneficiary, msg.value);
    }
}
contract WithFee is WithBeneficiary {
    uint256 private queryFee;
    event LogQueryFeeSet(uint256 previousQueryFee, uint256 newQueryFee);
    constructor(
            address beneficiary,
            uint256 _queryFee) public
        WithBeneficiary(beneficiary) {
        queryFee = _queryFee;
    }
    modifier requestFeePaid {
        require(queryFee <= msg.value);
        asyncSend(getBeneficiary(), msg.value);
        _;
    }
    function getQueryFee()
        view public
        returns (uint256) {
        return queryFee;
    }
    function setQueryFee(uint256 newQueryFee)
        fromOwner public
        returns (bool success) {
        if (queryFee != newQueryFee) {
            emit LogQueryFeeSet(queryFee, newQueryFee);
            queryFee = newQueryFee;
        }
        success = true;
    }
}
contract PullPaymentCapable {
    uint256 private totalBalance;
    mapping(address => uint256) private payments;
    event LogPaymentReceived(address indexed dest, uint256 amount);
    constructor() public {
        if (0 < address(this).balance) {
            asyncSend(msg.sender, address(this).balance);
        }
    }
    function asyncSend(address dest, uint256 amount) internal {
        if (amount > 0) {
            totalBalance += amount;
            payments[dest] += amount;
            emit LogPaymentReceived(dest, amount);
        }
    }
    function getTotalBalance()
        view public
        returns (uint256) {
        return totalBalance;
    }
    function getPaymentOf(address beneficiary) 
        view public
        returns (uint256) {
        return payments[beneficiary];
    }
    function withdrawPayments()
        external 
        returns (bool success) {
        uint256 payment = payments[msg.sender];
        payments[msg.sender] = 0;
        totalBalance -= payment;
        require(msg.sender.call.value(payment)());
        success = true;
    }
    function fixBalance()
        public
        returns (bool success);
    function fixBalanceInternal(address dest)
        internal
        returns (bool success) {
        if (totalBalance < address(this).balance) {
            uint256 amount = address(this).balance - totalBalance;
            payments[dest] += amount;
            emit LogPaymentReceived(dest, amount);
        }
        return true;
    }
}
contract CertifierDbI {
    event LogCertifierAdded(address indexed certifier);
    event LogCertifierRemoved(address indexed certifier);
    function addCertifier(address certifier)
        public
        returns (bool success);
    function removeCertifier(address certifier)
        public
        returns (bool success);
    function getCertifiersCount()
        view public
        returns (uint count);
    function getCertifierStatus(address certifierAddr)
        view public 
        returns (bool authorised, uint256 index);
    function getCertifierAtIndex(uint256 index)
        view public
        returns (address);
    function isCertifier(address certifier)
        view public
        returns (bool isIndeed);
}
contract CertificationDbI {
    event LogCertifierDbChanged(
        address indexed previousCertifierDb,
        address indexed newCertifierDb);
    event LogStudentCertified(
        address indexed student, uint timestamp,
        address indexed certifier, bytes32 indexed document);
    event LogStudentUncertified(
        address indexed student, uint timestamp,
        address indexed certifier);
    event LogCertificationDocumentAdded(
        address indexed student, bytes32 indexed document);
    event LogCertificationDocumentRemoved(
        address indexed student, bytes32 indexed document);
    function getCertifierDb()
        view public
        returns (address);
    function setCertifierDb(address newCertifierDb)
        public
        returns (bool success);
    function certify(address student, bytes32 document)
        public
        returns (bool success);
    function uncertify(address student)
        public
        returns (bool success);
    function addCertificationDocument(address student, bytes32 document)
        public
        returns (bool success);
    function addCertificationDocumentToSelf(bytes32 document)
        public
        returns (bool success);
    function removeCertificationDocument(address student, bytes32 document)
        public
        returns (bool success);
    function removeCertificationDocumentFromSelf(bytes32 document)
        public
        returns (bool success);
    function getCertifiedStudentsCount()
        view public
        returns (uint count);
    function getCertifiedStudentAtIndex(uint index)
        payable public
        returns (address student);
    function getCertification(address student)
        payable public
        returns (bool certified, uint timestamp, address certifier, uint documentCount);
    function isCertified(address student)
        payable public
        returns (bool isIndeed);
    function getCertificationDocumentAtIndex(address student, uint256 index)
        payable public
        returns (bytes32 document);
    function isCertification(address student, bytes32 document)
        payable public
        returns (bool isIndeed);
}
contract CertificationDb is CertificationDbI, WithFee, PullPaymentCapable {
    CertifierDbI private certifierDb;
    struct DocumentStatus {
        bool isValid;
        uint256 index;
    }
    struct Certification {
        bool certified;
        uint256 timestamp;
        address certifier;
        mapping(bytes32 => DocumentStatus) documentStatuses;
        bytes32[] documents;
        uint256 index;
    }
    mapping(address => Certification) studentCertifications;
    address[] certifiedStudents;
    constructor(
            address beneficiary,
            uint256 certificationQueryFee,
            address _certifierDb)
            public
            WithFee(beneficiary, certificationQueryFee) {
        require(_certifierDb != 0);
        certifierDb = CertifierDbI(_certifierDb);
    }
    modifier fromCertifier {
        require(certifierDb.isCertifier(msg.sender));
        _;
    }
    function getCertifierDb()
        view public
        returns (address) {
        return certifierDb;
    }
    function setCertifierDb(address newCertifierDb)
        fromOwner public
        returns (bool success) {
        require(newCertifierDb != 0);
        if (certifierDb != newCertifierDb) {
            emit LogCertifierDbChanged(certifierDb, newCertifierDb);
            certifierDb = CertifierDbI(newCertifierDb);
        }
        success = true;
    }
    function certify(address student, bytes32 document) 
        fromCertifier public
        returns (bool success) {
        require(student != 0);
        require(!studentCertifications[student].certified);
        bool documentExists = document != 0;
        studentCertifications[student] = Certification({
            certified: true,
            timestamp: now,
            certifier: msg.sender,
            documents: new bytes32[](0),
            index: certifiedStudents.length
        });
        if (documentExists) {
            studentCertifications[student].documentStatuses[document] = DocumentStatus({
                isValid: true,
                index: studentCertifications[student].documents.length
            });
            studentCertifications[student].documents.push(document);
        }
        certifiedStudents.push(student);
        emit LogStudentCertified(student, now, msg.sender, document);
        success = true;
    }
    function uncertify(address student) 
        fromCertifier public
        returns (bool success) {
        require(studentCertifications[student].certified);
        require(studentCertifications[student].documents.length == 0);
        uint256 index = studentCertifications[student].index;
        delete studentCertifications[student];
        if (certifiedStudents.length > 1) {
            certifiedStudents[index] = certifiedStudents[certifiedStudents.length - 1];
            studentCertifications[certifiedStudents[index]].index = index;
        }
        certifiedStudents.length--;
        emit LogStudentUncertified(student, now, msg.sender);
        success = true;
    }
    function addCertificationDocument(address student, bytes32 document)
        fromCertifier public
        returns (bool success) {
        success = addCertificationDocumentInternal(student, document);
    }
    function addCertificationDocumentToSelf(bytes32 document)
        public
        returns (bool success) {
        success = addCertificationDocumentInternal(msg.sender, document);
    }
    function addCertificationDocumentInternal(address student, bytes32 document)
        internal
        returns (bool success) {
        require(studentCertifications[student].certified);
        require(document != 0);
        Certification storage certification = studentCertifications[student];
        if (!certification.documentStatuses[document].isValid) {
            certification.documentStatuses[document] = DocumentStatus({
                isValid:  true,
                index: certification.documents.length
            });
            certification.documents.push(document);
            emit LogCertificationDocumentAdded(student, document);
        }
        success = true;
    }
    function removeCertificationDocument(address student, bytes32 document)
        fromCertifier public
        returns (bool success) {
        success = removeCertificationDocumentInternal(student, document);
    }
    function removeCertificationDocumentFromSelf(bytes32 document)
        public
        returns (bool success) {
        success = removeCertificationDocumentInternal(msg.sender, document);
    }
    function removeCertificationDocumentInternal(address student, bytes32 document)
        internal
        returns (bool success) {
        require(studentCertifications[student].certified);
        Certification storage certification = studentCertifications[student];
        if (certification.documentStatuses[document].isValid) {
            uint256 index = certification.documentStatuses[document].index;
            delete certification.documentStatuses[document];
            if (certification.documents.length > 1) {
                certification.documents[index] =
                    certification.documents[certification.documents.length - 1];
                certification.documentStatuses[certification.documents[index]].index = index;
            }
            certification.documents.length--;
            emit LogCertificationDocumentRemoved(student, document);
        }
        success = true;
    }
    function getCertifiedStudentsCount()
        view public
        returns (uint256 count) {
        count = certifiedStudents.length;
    }
    function getCertifiedStudentAtIndex(uint256 index)
        payable public
        requestFeePaid
        returns (address student) {
        student = certifiedStudents[index];
    }
    function getCertification(address student)
        payable public
        requestFeePaid
        returns (bool certified, uint256 timestamp, address certifier, uint256 documentCount) {
        Certification storage certification = studentCertifications[student];
        return (certification.certified,
            certification.timestamp,
            certification.certifier,
            certification.documents.length);
    }
    function isCertified(address student)
        payable public
        requestFeePaid
        returns (bool isIndeed) {
        isIndeed = studentCertifications[student].certified;
    }
    function getCertificationDocumentAtIndex(address student, uint256 index)
        payable public
        requestFeePaid
        returns (bytes32 document) {
        document = studentCertifications[student].documents[index];
    }
    function isCertification(address student, bytes32 document)
        payable public
        requestFeePaid
        returns (bool isIndeed) {
        isIndeed = studentCertifications[student].documentStatuses[document].isValid;
    }
    function fixBalance()
        public
        returns (bool success) {
        return fixBalanceInternal(getBeneficiary());
    }
}
```

## RQ1_0646056d402b

SHA-256 `e62321e8dc99c4cb878297f8dd6a0d8c841aa401fd4d9ca4e3c0c7cba1e8f695`

```solidity
pragma solidity >=0.5.4 <0.6.0;
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
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes calldata _extraData) external; }
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
interface IAOSetting {
	function getSettingValuesByTAOName(address _taoId, string calldata _settingName) external view returns (uint256, bool, address, bytes32, string memory);
	function getSettingTypes() external view returns (uint8, uint8, uint8, uint8, uint8);
	function settingTypeLookup(uint256 _settingId) external view returns (uint8);
}
interface ITAOAncestry {
	function initialize(address _id, address _parentId, uint256 _childMinLogos) external returns (bool);
	function getAncestryById(address _id) external view returns (address, uint256, uint256);
	function addChild(address _taoId, address _childId) external returns (bool);
	function isChild(address _taoId, address _childId) external view returns (bool);
}
interface ITAOFactory {
	function nonces(address _taoId) external view returns (uint256);
	function incrementNonce(address _taoId) external returns (uint256);
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
contract TAOCurrency is TheAO {
	using SafeMath for uint256;
	string public name;
	string public symbol;
	uint8 public decimals;
	uint256 public powerOfTen;
	uint256 public totalSupply;
	mapping (address => uint256) public balanceOf;
	event Transfer(address indexed from, address indexed to, uint256 value);
	event Burn(address indexed from, uint256 value);
	constructor (string memory _name, string memory _symbol, address _nameTAOPositionAddress) public {
		name = _name;		
		symbol = _symbol;	
		powerOfTen = 0;
		decimals = 0;
		setNameTAOPositionAddress(_nameTAOPositionAddress);
	}
	modifier onlyTheAO {
		require (AOLibrary.isTheAO(msg.sender, theAO, nameTAOPositionAddress));
		_;
	}
	modifier isNameOrTAO(address _id) {
		require (AOLibrary.isName(_id) || AOLibrary.isTAO(_id));
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
	function setNameTAOPositionAddress(address _nameTAOPositionAddress) public onlyTheAO {
		require (_nameTAOPositionAddress != address(0));
		nameTAOPositionAddress = _nameTAOPositionAddress;
	}
	function transferFrom(address _from, address _to, uint256 _value) public inWhitelist isNameOrTAO(_from) isNameOrTAO(_to) returns (bool) {
		_transfer(_from, _to, _value);
		return true;
	}
	function mint(address target, uint256 mintedAmount) public inWhitelist isNameOrTAO(target) returns (bool) {
		_mint(target, mintedAmount);
		return true;
	}
	function whitelistBurnFrom(address _from, uint256 _value) public inWhitelist isNameOrTAO(_from) returns (bool success) {
		require(balanceOf[_from] >= _value);                
		balanceOf[_from] = balanceOf[_from].sub(_value);    
		totalSupply = totalSupply.sub(_value);              
		emit Burn(_from, _value);
		return true;
	}
	function _transfer(address _from, address _to, uint256 _value) internal {
		require (_to != address(0));							
		require (balanceOf[_from] >= _value);					
		require (balanceOf[_to].add(_value) >= balanceOf[_to]); 
		uint256 previousBalances = balanceOf[_from].add(balanceOf[_to]);
		balanceOf[_from] = balanceOf[_from].sub(_value);        
		balanceOf[_to] = balanceOf[_to].add(_value);            
		emit Transfer(_from, _to, _value);
		assert(balanceOf[_from].add(balanceOf[_to]) == previousBalances);
	}
	function _mint(address target, uint256 mintedAmount) internal {
		balanceOf[target] = balanceOf[target].add(mintedAmount);
		totalSupply = totalSupply.add(mintedAmount);
		emit Transfer(address(0), address(this), mintedAmount);
		emit Transfer(address(this), target, mintedAmount);
	}
}
contract Logos is TAOCurrency {
	address public nameFactoryAddress;
	address public nameAccountRecoveryAddress;
	INameFactory internal _nameFactory;
	INameTAOPosition internal _nameTAOPosition;
	INameAccountRecovery internal _nameAccountRecovery;
	mapping (address => uint256) public positionFromOthers;
	mapping (address => mapping(address => uint256)) public positionOnOthers;
	mapping (address => uint256) public totalPositionOnOthers;
	mapping (address => mapping(address => uint256)) public advocatedTAOLogos;
	mapping (address => uint256) public totalAdvocatedTAOLogos;
	event PositionFrom(address indexed from, address indexed to, uint256 value);
	event UnpositionFrom(address indexed from, address indexed to, uint256 value);
	event AddAdvocatedTAOLogos(address indexed nameId, address indexed taoId, uint256 amount);
	event TransferAdvocatedTAOLogos(address indexed fromNameId, address indexed toNameId, address indexed taoId, uint256 amount);
	constructor(string memory _name, string memory _symbol, address _nameFactoryAddress, address _nameTAOPositionAddress)
		TAOCurrency(_name, _symbol, _nameTAOPositionAddress) public {
		setNameFactoryAddress(_nameFactoryAddress);
		setNameTAOPositionAddress(_nameTAOPositionAddress);
	}
	modifier isTAO(address _taoId) {
		require (AOLibrary.isTAO(_taoId));
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
	modifier nameNotCompromised(address _id) {
		require (!_nameAccountRecovery.isCompromised(_id));
		_;
	}
	modifier senderNameNotCompromised() {
		require (!_nameAccountRecovery.isCompromised(_nameFactory.ethAddressToNameId(msg.sender)));
		_;
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
	function sumBalanceOf(address _target) public isName(_target) view returns (uint256) {
		return balanceOf[_target].add(positionFromOthers[_target]).add(totalAdvocatedTAOLogos[_target]);
	}
	function availableToPositionAmount(address _sender) public isName(_sender) view returns (uint256) {
		return balanceOf[_sender].sub(totalPositionOnOthers[_sender]);
	}
	function positionFrom(address _from, address _to, uint256 _value) public isName(_from) isName(_to) nameNotCompromised(_from) nameNotCompromised(_to) onlyAdvocate(_from) senderNameNotCompromised returns (bool) {
		require (_from != _to);	
		require (availableToPositionAmount(_from) >= _value); 
		require (positionFromOthers[_to].add(_value) >= positionFromOthers[_to]); 
		positionOnOthers[_from][_to] = positionOnOthers[_from][_to].add(_value);
		totalPositionOnOthers[_from] = totalPositionOnOthers[_from].add(_value);
		positionFromOthers[_to] = positionFromOthers[_to].add(_value);
		emit PositionFrom(_from, _to, _value);
		return true;
	}
	function unpositionFrom(address _from, address _to, uint256 _value) public isName(_from) isName(_to) nameNotCompromised(_from) nameNotCompromised(_to) onlyAdvocate(_from) senderNameNotCompromised returns (bool) {
		require (_from != _to);	
		require (positionOnOthers[_from][_to] >= _value);
		positionOnOthers[_from][_to] = positionOnOthers[_from][_to].sub(_value);
		totalPositionOnOthers[_from] = totalPositionOnOthers[_from].sub(_value);
		positionFromOthers[_to] = positionFromOthers[_to].sub(_value);
		emit UnpositionFrom(_from, _to, _value);
		return true;
	}
	function addAdvocatedTAOLogos(address _taoId, uint256 _amount) public inWhitelist isTAO(_taoId) returns (bool) {
		require (_amount > 0);
		address _nameId = _nameTAOPosition.getAdvocate(_taoId);
		advocatedTAOLogos[_nameId][_taoId] = advocatedTAOLogos[_nameId][_taoId].add(_amount);
		totalAdvocatedTAOLogos[_nameId] = totalAdvocatedTAOLogos[_nameId].add(_amount);
		emit AddAdvocatedTAOLogos(_nameId, _taoId, _amount);
		return true;
	}
	function transferAdvocatedTAOLogos(address _fromNameId, address _taoId) public inWhitelist isName(_fromNameId) isTAO(_taoId) returns (bool) {
		address _toNameId = _nameTAOPosition.getAdvocate(_taoId);
		require (_fromNameId != _toNameId);
		require (totalAdvocatedTAOLogos[_fromNameId] >= advocatedTAOLogos[_fromNameId][_taoId]);
		uint256 _amount = advocatedTAOLogos[_fromNameId][_taoId];
		advocatedTAOLogos[_fromNameId][_taoId] = 0;
		totalAdvocatedTAOLogos[_fromNameId] = totalAdvocatedTAOLogos[_fromNameId].sub(_amount);
		advocatedTAOLogos[_toNameId][_taoId] = advocatedTAOLogos[_toNameId][_taoId].add(_amount);
		totalAdvocatedTAOLogos[_toNameId] = totalAdvocatedTAOLogos[_toNameId].add(_amount);
		emit TransferAdvocatedTAOLogos(_fromNameId, _toNameId, _taoId, _amount);
		return true;
	}
}
contract NameTAOPosition is TheAO, INameTAOPosition {
	using SafeMath for uint256;
	address public settingTAOId;
	address public nameFactoryAddress;
	address public nameAccountRecoveryAddress;
	address public taoFactoryAddress;
	address public aoSettingAddress;
	address public taoAncestryAddress;
	address public logosAddress;
	uint256 public totalTAOAdvocateChallenges;
	INameFactory internal _nameFactory;
	INameAccountRecovery internal _nameAccountRecovery;
	ITAOFactory internal _taoFactory;
	IAOSetting internal _aoSetting;
	ITAOAncestry internal _taoAncestry;
	Logos internal _logos;
	struct PositionDetail {
		address advocateId;
		address listenerId;
		address speakerId;
		bool created;
	}
	struct TAOAdvocateChallenge {
		bytes32 challengeId;
		address newAdvocateId;		
		address taoId;				
		bool completed;				
		uint256 createdTimestamp;	
		uint256 lockedUntilTimestamp;	
		uint256 completeBeforeTimestamp; 
	}
	mapping (address => PositionDetail) internal positionDetails;
	mapping (bytes32 => TAOAdvocateChallenge) internal taoAdvocateChallenges;
	event SetAdvocate(address indexed taoId, address oldAdvocateId, address newAdvocateId, uint256 nonce);
	event SetListener(address indexed taoId, address oldListenerId, address newListenerId, uint256 nonce);
	event SetSpeaker(address indexed taoId, address oldSpeakerId, address newSpeakerId, uint256 nonce);
	event ChallengeTAOAdvocate(address indexed taoId, bytes32 indexed challengeId, address currentAdvocateId, address challengerAdvocateId, uint256 createdTimestamp, uint256 lockedUntilTimestamp, uint256 completeBeforeTimestamp);
	event CompleteTAOAdvocateChallenge(address indexed taoId, bytes32 indexed challengeId);
	constructor(address _nameFactoryAddress, address _taoFactoryAddress) public {
		setNameFactoryAddress(_nameFactoryAddress);
		setTAOFactoryAddress(_taoFactoryAddress);
		nameTAOPositionAddress = address(this);
	}
	modifier onlyTheAO {
		require (AOLibrary.isTheAO(msg.sender, theAO, nameTAOPositionAddress));
		_;
	}
	modifier onlyFactory {
		require (msg.sender == nameFactoryAddress || msg.sender == taoFactoryAddress);
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
		require (this.senderIsAdvocate(msg.sender, _id));
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
	function setNameAccountRecoveryAddress(address _nameAccountRecoveryAddress) public onlyTheAO {
		require (_nameAccountRecoveryAddress != address(0));
		nameAccountRecoveryAddress = _nameAccountRecoveryAddress;
		_nameAccountRecovery = INameAccountRecovery(nameAccountRecoveryAddress);
	}
	function setTAOFactoryAddress(address _taoFactoryAddress) public onlyTheAO {
		require (_taoFactoryAddress != address(0));
		taoFactoryAddress = _taoFactoryAddress;
		_taoFactory = ITAOFactory(_taoFactoryAddress);
	}
	function setSettingTAOId(address _settingTAOId) public onlyTheAO {
		require (AOLibrary.isTAO(_settingTAOId));
		settingTAOId = _settingTAOId;
	}
	function setAOSettingAddress(address _aoSettingAddress) public onlyTheAO {
		require (_aoSettingAddress != address(0));
		aoSettingAddress = _aoSettingAddress;
		_aoSetting = IAOSetting(_aoSettingAddress);
	}
	function setTAOAncestryAddress(address _taoAncestryAddress) public onlyTheAO {
		require (_taoAncestryAddress != address(0));
		taoAncestryAddress = _taoAncestryAddress;
		_taoAncestry = ITAOAncestry(taoAncestryAddress);
	}
	function setLogosAddress(address _logosAddress) public onlyTheAO {
		require (_logosAddress != address(0));
		logosAddress = _logosAddress;
		_logos = Logos(_logosAddress);
	}
	function isExist(address _id) public view returns (bool) {
		return positionDetails[_id].created;
	}
	function senderIsAdvocate(address _sender, address _id) external view returns (bool) {
		return (positionDetails[_id].created && positionDetails[_id].advocateId == _nameFactory.ethAddressToNameId(_sender));
	}
	function senderIsListener(address _sender, address _id) external view returns (bool) {
		return (positionDetails[_id].created && positionDetails[_id].listenerId == _nameFactory.ethAddressToNameId(_sender));
	}
	function senderIsSpeaker(address _sender, address _id) external view returns (bool) {
		return (positionDetails[_id].created && positionDetails[_id].speakerId == _nameFactory.ethAddressToNameId(_sender));
	}
	function senderIsAdvocateOfParent(address _sender, address _id) public view returns (bool) {
		(address _parentId,,) = _taoAncestry.getAncestryById(_id);
		 return ((AOLibrary.isName(_parentId) || (AOLibrary.isTAO(_parentId) && _taoAncestry.isChild(_parentId, _id))) && this.senderIsAdvocate(_sender, _parentId));
	}
	function senderIsPosition(address _sender, address _id) external view returns (bool) {
		address _nameId = _nameFactory.ethAddressToNameId(_sender);
		if (_nameId == address(0)) {
			return false;
		} else {
			return this.nameIsPosition(_nameId, _id);
		}
	}
	function nameIsAdvocate(address _nameId, address _id) external view returns (bool) {
		return (positionDetails[_id].created && positionDetails[_id].advocateId == _nameId);
	}
	function nameIsPosition(address _nameId, address _id) external view returns (bool) {
		return (positionDetails[_id].created &&
			(positionDetails[_id].advocateId == _nameId ||
			 positionDetails[_id].listenerId == _nameId ||
			 positionDetails[_id].speakerId == _nameId
			)
	   );
	}
	function determinePosition(address _sender, address _id) external view returns (uint256) {
		require (this.senderIsPosition(_sender, _id));
		PositionDetail memory _positionDetail = positionDetails[_id];
		address _nameId = _nameFactory.ethAddressToNameId(_sender);
		if (_nameId == _positionDetail.advocateId) {
			return 1;
		} else if (_nameId == _positionDetail.listenerId) {
			return 2;
		} else {
			return 3;
		}
	}
	function initialize(address _id, address _advocateId, address _listenerId, address _speakerId)
		external
		isNameOrTAO(_id)
		isName(_advocateId)
		isNameOrTAO(_listenerId)
		isNameOrTAO(_speakerId)
		onlyFactory returns (bool) {
		require (!isExist(_id));
		PositionDetail storage _positionDetail = positionDetails[_id];
		_positionDetail.advocateId = _advocateId;
		_positionDetail.listenerId = _listenerId;
		_positionDetail.speakerId = _speakerId;
		_positionDetail.created = true;
		return true;
	}
	function getPositionById(address _id) public view returns (string memory, address, string memory, address, string memory, address) {
		require (isExist(_id));
		PositionDetail memory _positionDetail = positionDetails[_id];
		return (
			TAO(address(uint160(_positionDetail.advocateId))).name(),
			_positionDetail.advocateId,
			TAO(address(uint160(_positionDetail.listenerId))).name(),
			_positionDetail.listenerId,
			TAO(address(uint160(_positionDetail.speakerId))).name(),
			_positionDetail.speakerId
		);
	}
	function getAdvocate(address _id) external view returns (address) {
		require (isExist(_id));
		PositionDetail memory _positionDetail = positionDetails[_id];
		return _positionDetail.advocateId;
	}
	function getListener(address _id) public view returns (address) {
		require (isExist(_id));
		PositionDetail memory _positionDetail = positionDetails[_id];
		return _positionDetail.listenerId;
	}
	function getSpeaker(address _id) public view returns (address) {
		require (isExist(_id));
		PositionDetail memory _positionDetail = positionDetails[_id];
		return _positionDetail.speakerId;
	}
	function setAdvocate(address _taoId, address _newAdvocateId)
		public
		isTAO(_taoId)
		isName(_newAdvocateId)
		onlyAdvocate(_taoId)
		senderIsName
		senderNameNotCompromised {
		require (isExist(_taoId));
		require (!_nameAccountRecovery.isCompromised(_newAdvocateId));
		_setAdvocate(_taoId, _newAdvocateId);
	}
	function parentReplaceChildAdvocate(address _taoId)
		public
		isTAO(_taoId)
		senderIsName
		senderNameNotCompromised {
		require (isExist(_taoId));
		require (senderIsAdvocateOfParent(msg.sender, _taoId));
		address _parentNameId = _nameFactory.ethAddressToNameId(msg.sender);
		address _currentAdvocateId = this.getAdvocate(_taoId);
		require (_parentNameId != _currentAdvocateId);
		require (_logos.sumBalanceOf(_parentNameId) > _logos.sumBalanceOf(this.getAdvocate(_taoId)));
		_setAdvocate(_taoId, _parentNameId);
	}
	function challengeTAOAdvocate(address _taoId)
		public
		isTAO(_taoId)
		senderIsName
		senderNameNotCompromised {
		require (isExist(_taoId));
		address _newAdvocateId = _nameFactory.ethAddressToNameId(msg.sender);
		address _currentAdvocateId = this.getAdvocate(_taoId);
		require (_newAdvocateId != _currentAdvocateId);
		require (_logos.sumBalanceOf(_newAdvocateId) > _logos.sumBalanceOf(_currentAdvocateId));
		(uint256 _lockDuration, uint256 _completeDuration) = _getSettingVariables();
		totalTAOAdvocateChallenges++;
		bytes32 _challengeId = keccak256(abi.encodePacked(this, _taoId, _newAdvocateId, totalTAOAdvocateChallenges));
		TAOAdvocateChallenge storage _taoAdvocateChallenge = taoAdvocateChallenges[_challengeId];
		_taoAdvocateChallenge.challengeId = _challengeId;
		_taoAdvocateChallenge.newAdvocateId = _newAdvocateId;
		_taoAdvocateChallenge.taoId = _taoId;
		_taoAdvocateChallenge.createdTimestamp = now;
		_taoAdvocateChallenge.lockedUntilTimestamp = _taoAdvocateChallenge.createdTimestamp.add(_lockDuration);
		_taoAdvocateChallenge.completeBeforeTimestamp = _taoAdvocateChallenge.lockedUntilTimestamp.add(_completeDuration);
		emit ChallengeTAOAdvocate(_taoId, _challengeId, _currentAdvocateId, _newAdvocateId, _taoAdvocateChallenge.createdTimestamp, _taoAdvocateChallenge.lockedUntilTimestamp, _taoAdvocateChallenge.completeBeforeTimestamp);
	}
	function getChallengeStatus(bytes32 _challengeId, address _sender) public view returns (uint8) {
		address _challengerNameId = _nameFactory.ethAddressToNameId(_sender);
		TAOAdvocateChallenge storage _taoAdvocateChallenge = taoAdvocateChallenges[_challengeId];
		if (_taoAdvocateChallenge.taoId == address(0)) {
			return 2;
		} else if (_challengerNameId != _taoAdvocateChallenge.newAdvocateId) {
			return 3;
		} else if (now < _taoAdvocateChallenge.lockedUntilTimestamp) {
			return 4;
		} else if (now > _taoAdvocateChallenge.completeBeforeTimestamp) {
			return 5;
		} else if (_taoAdvocateChallenge.completed) {
			return 6;
		} else if (_logos.sumBalanceOf(_challengerNameId) <= _logos.sumBalanceOf(this.getAdvocate(_taoAdvocateChallenge.taoId))) {
			return 7;
		} else {
			return 1;
		}
	}
	function completeTAOAdvocateChallenge(bytes32 _challengeId)
		public
		senderIsName
		senderNameNotCompromised {
		TAOAdvocateChallenge storage _taoAdvocateChallenge = taoAdvocateChallenges[_challengeId];
		require (getChallengeStatus(_challengeId, msg.sender) == 1);
		_taoAdvocateChallenge.completed = true;
		_setAdvocate(_taoAdvocateChallenge.taoId, _taoAdvocateChallenge.newAdvocateId);
		emit CompleteTAOAdvocateChallenge(_taoAdvocateChallenge.taoId, _challengeId);
	}
	function getTAOAdvocateChallengeById(bytes32 _challengeId) public view returns (address, address, bool, uint256, uint256, uint256) {
		TAOAdvocateChallenge memory _taoAdvocateChallenge = taoAdvocateChallenges[_challengeId];
		require (_taoAdvocateChallenge.taoId != address(0));
		return (
			_taoAdvocateChallenge.newAdvocateId,
			_taoAdvocateChallenge.taoId,
			_taoAdvocateChallenge.completed,
			_taoAdvocateChallenge.createdTimestamp,
			_taoAdvocateChallenge.lockedUntilTimestamp,
			_taoAdvocateChallenge.completeBeforeTimestamp
		);
	}
	function setListener(address _id, address _newListenerId)
		public
		isNameOrTAO(_id)
		isNameOrTAO(_newListenerId)
		senderIsName
		senderNameNotCompromised
		onlyAdvocate(_id) {
		require (isExist(_id));
		bool _isName = false;
		if (AOLibrary.isName(_id)) {
			_isName = true;
			require (AOLibrary.isName(_newListenerId));
			require (!_nameAccountRecovery.isCompromised(_id));
			require (!_nameAccountRecovery.isCompromised(_newListenerId));
		}
		PositionDetail storage _positionDetail = positionDetails[_id];
		address _currentListenerId = _positionDetail.listenerId;
		_positionDetail.listenerId = _newListenerId;
		uint256 _nonce;
		if (_isName) {
			_nonce = _nameFactory.incrementNonce(_id);
		} else {
			_nonce = _taoFactory.incrementNonce(_id);
		}
		emit SetListener(_id, _currentListenerId, _positionDetail.listenerId, _nonce);
	}
	function setSpeaker(address _id, address _newSpeakerId)
		public
		isNameOrTAO(_id)
		isNameOrTAO(_newSpeakerId)
		senderIsName
		senderNameNotCompromised
		onlyAdvocate(_id) {
		require (isExist(_id));
		bool _isName = false;
		if (AOLibrary.isName(_id)) {
			_isName = true;
			require (AOLibrary.isName(_newSpeakerId));
			require (!_nameAccountRecovery.isCompromised(_id));
			require (!_nameAccountRecovery.isCompromised(_newSpeakerId));
		}
		PositionDetail storage _positionDetail = positionDetails[_id];
		address _currentSpeakerId = _positionDetail.speakerId;
		_positionDetail.speakerId = _newSpeakerId;
		uint256 _nonce;
		if (_isName) {
			_nonce = _nameFactory.incrementNonce(_id);
		} else {
			_nonce = _taoFactory.incrementNonce(_id);
		}
		emit SetSpeaker(_id, _currentSpeakerId, _positionDetail.speakerId, _nonce);
	}
	function _setAdvocate(address _taoId, address _newAdvocateId) internal {
		PositionDetail storage _positionDetail = positionDetails[_taoId];
		address _currentAdvocateId = _positionDetail.advocateId;
		_positionDetail.advocateId = _newAdvocateId;
		uint256 _nonce = _taoFactory.incrementNonce(_taoId);
		require (_nonce > 0);
		require (_logos.transferAdvocatedTAOLogos(_currentAdvocateId, _taoId));
		emit SetAdvocate(_taoId, _currentAdvocateId, _positionDetail.advocateId, _nonce);
	}
	function _getSettingVariables() internal view returns (uint256, uint256) {
		(uint256 challengeTAOAdvocateLockDuration,,,,) = _aoSetting.getSettingValuesByTAOName(settingTAOId, 'challengeTAOAdvocateLockDuration');
		(uint256 challengeTAOAdvocateCompleteDuration,,,,) = _aoSetting.getSettingValuesByTAOName(settingTAOId, 'challengeTAOAdvocateCompleteDuration');
		return (
			challengeTAOAdvocateLockDuration,
			challengeTAOAdvocateCompleteDuration
		);
	}
}
```

## RQ1_2199b3bb427b

SHA-256 `484b210bd845a7aed6808f9c1197aba39f294cf22fbdc4b6c6336583e68cde6a`

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
        require(allowance - sold[listingId] > amount);
        require(allowance - amount > 0);
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

## RQ1_b974cb3eae41

SHA-256 `3b0ada0a5ca2b4c2c80fd8a6efe8daadac9ef4e01a3e411cfa83914072406b94`

```solidity
pragma solidity ^0.4.19;
contract Lottery4 {
    address owner;
    address profit = 0xB7BB510B0746bdeE208dB6fB781bF5Be39d15A15;
    uint public tickets;
    uint public round;
    string public status;
    uint public lastWiningTicketNumber;
    address public lastWinner;
    address ticket1;
    address ticket2;
    address ticket3;
    address ticket4;
    address ticket5;
    uint constant price = 0.05 ether; 
    uint seed;
    bool entry = false;
    function Lottery4() public { 
        owner = msg.sender;
        tickets = 5;
        round = 1;
        status = "Running";
        entry = false;
        seed = 777;
    }
    function changeStatus(string w) public {
        if (msg.sender == owner) {
            status = w;
        }
        else {
            revert();
        }
    }
    function changeSeed(uint32 n) public {
        if (msg.sender == owner) {
            seed = uint(n);
            seed = uint(block.blockhash(block.number-seed))%2000 + 1; 
        }
        else {
            revert();
        }
    }
    function () public payable { 
        buyTickets();
    }
    function buyTickets() public payable {
        if (entry == true) { 
            revert();
        }
        entry = true;
        if (msg.value != (price)) {
            entry = false;
            if (keccak256(status) == keccak256("Shutdown")) { 
                selfdestruct(owner);
            }
            revert(); 
        }
        else {
            if (tickets == 5) {
                tickets -= 1;
                ticket1 = msg.sender;
            }
            else if(tickets == 4) {
                tickets -= 1;
                ticket2 = msg.sender;
                profit.transfer(price * 1/2); 
            }
            else if(tickets == 3) {
                tickets -= 1;
                ticket3 = msg.sender;
            }
            else if(tickets == 2) {
                tickets -= 1;
                ticket4 = msg.sender;
            }
            else if(tickets == 1) {
                ticket5 = msg.sender;
                tickets = 5; 
                round += 1; 
                seed = uint(block.blockhash(block.number-seed))%2000 + 1; 
                uint random_number = uint(block.blockhash(block.number-seed))%5 + 1; 
                lastWiningTicketNumber = random_number; 
                uint pay = (price * 9/2); 
                if (random_number == 1) {
                    ticket1.transfer(pay);
                    lastWinner = ticket1; 
                }
                else if(random_number == 2) {
                    ticket2.transfer(pay);
                    lastWinner = ticket2; 
                }
                else if(random_number == 3) {
                    ticket3.transfer(pay);
                    lastWinner = ticket3; 
                }
                else if(random_number == 4) {
                    ticket4.transfer(pay);
                    lastWinner = ticket4; 
                }
                else if(random_number == 5) {
                    ticket5.transfer(pay);
                    lastWinner = ticket5; 
                }
            }
        }
        entry = false;
    }
}
```

## RQ1_ed7c5ffc5160

SHA-256 `c12e73853918505d6e8b007e6d6db3395ef1a52faf6ef62e8c0e4a14fdac683b`

```solidity
pragma solidity ^0.4.19;
contract SetherToken {
    string public name = "Sether";
    string public symbol = "SETH";
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
    function SetherToken() public {
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

## RQ1_f692c464b513

SHA-256 `19031869d1ec38ef635345bb0b365cfe7870d251ab1794df00c0fefb91ffc7aa`

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

## RQ1_cea1b483c963

SHA-256 `69354e1cd967aa45f4b3ea7268849a0f2c5f7f9f0d2fccabb0de404371093def`

```solidity
pragma solidity ^0.4.16;
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
contract StandardToken is ERC20, BasicToken {
  mapping (address => mapping (address => uint256)) allowed;
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
  function pause() onlyOwner whenNotPaused returns (bool) {
    paused = true;
    Pause();
    return true;
  }
  function unpause() onlyOwner whenPaused returns (bool) {
    paused = false;
    Unpause();
    return true;
  }
}
contract SlotTicket is StandardToken, Ownable {
  string public name = "Slot Ticket";
  uint8 public decimals = 0;
  string public symbol = "SLOT";
  string public version = "0.1";
  event Mint(address indexed to, uint256 amount);
  function mint(address _to, uint256 _amount) onlyOwner returns (bool) {
    totalSupply = totalSupply.add(_amount);
    balances[_to] = balances[_to].add(_amount);
    Mint(_to, _amount);
    Transfer(0x0, _to, _amount); 
    return true;
  }
function destroy() onlyOwner {
    selfdestruct(owner);
  }
}
contract Slot is Ownable, Pausable { 
    using SafeMath for uint256;
    SlotTicket public token;
    mapping (uint => address) participants;
    uint256[] prizes = [4 ether, 
                        2 ether,
                        1 ether, 
                        500 finney, 
                        500 finney, 
                        500 finney, 
                        500 finney, 
                        500 finney];
    uint8 counter = 0;
    uint8   constant SIZE = 100; 
    uint32  constant JACKPOT_SIZE = 1000000; 
    uint256 constant PRICE = 100 finney;
    uint256 jackpot = 0;
    uint256 gameNumber = 0;
    address wallet;
    event PrizeAwarded(uint256 game, address winner, uint256 amount);
    event JackpotAwarded(uint256 game, address winner, uint256 amount);
    function Slot(address _wallet) {
        token = new SlotTicket();
        wallet = _wallet;
    }
    function() payable {
        buyTicketsFor(msg.sender);
    }
    function buyTicketsFor(address beneficiary) whenNotPaused() payable {
        require(beneficiary != 0x0);
        require(msg.value >= PRICE);
        require(msg.value/PRICE <= 255); 
        uint8 numberOfTickets = uint8(msg.value/PRICE); 
        token.mint(beneficiary, numberOfTickets);
        addParticipant(beneficiary, numberOfTickets);
        msg.sender.transfer(msg.value%PRICE);
    }
    function addParticipant(address _participant, uint8 _numberOfTickets) private {
        for (uint8 i = 0; i < _numberOfTickets; i++) {
            participants[counter] = _participant;
            if (counter % (SIZE-1) == 0) { 
                awardPrizes(uint256(_participant)); 
            } 
            counter++;
        }
    }
    function rand(uint32 _size, uint256 _seed) constant private returns (uint32 randomNumber) {
        return uint32(sha3(block.blockhash(block.number-1), _seed))%_size;
    }
    function awardPrizes(uint256 _seed) private {
        uint32 winningNumber = rand(SIZE-1, _seed); 
        bool jackpotWon = winningNumber == rand(JACKPOT_SIZE-1, _seed); 
        uint256 start = gameNumber.mul(SIZE);
        uint256 end = start + SIZE;
        uint256 winnerIndex = start.add(winningNumber);
        for (uint8 i = 0; i < prizes.length; i++) {
            if (jackpotWon && i==0) { distributeJackpot(winnerIndex); }
            if (winnerIndex+i > end) {
                winnerIndex -= SIZE;
            }
            participants[winnerIndex+i].transfer(prizes[i]); 
            PrizeAwarded(gameNumber,  participants[winnerIndex+i], prizes[i]);
        }
        jackpot = jackpot.add(245 finney);  
        wallet.transfer(245 finney);        
        msg.sender.transfer(10 finney);     
        gameNumber++;
    }
    function distributeJackpot(uint256 _winnerIndex) {
        participants[_winnerIndex].transfer(jackpot);
        JackpotAwarded(gameNumber,  participants[_winnerIndex], jackpot);
        jackpot = 0; 
    }
    function destroy() onlyOwner {
        token.destroy();
        selfdestruct(owner);
  }
    function changeWallet(address _newWallet) onlyOwner {
        require(_newWallet != 0x0);
        wallet = _newWallet;
  }
}
```

## RQ1_a2b72affd3ef

SHA-256 `8d41f99af3e1f14a9b7fb0d9854e17547937005b6dd6896f1b2af0a862ab1d21`

```solidity
pragma solidity ^0.4.24;
 contract Matching_Finneys
{
    enum State{Active, Deactivated}
    State public state;
    modifier onlyOwner() {
	    if (msg.sender!=owner) throw;
	    _;
    }
    modifier onlyActive() {
         if (state!=State.Active) throw;
         _;
    }
    modifier onlyInactive() {
         if (state!=State.Deactivated) throw;
         _;
    }
    modifier equalGambleValue() {
	if (msg.value < gamble_value) throw;
        if (msg.value > gamble_value) msg.sender.send(msg.value-gamble_value);
	_;
    }
    modifier resolvePendingRound{
        blockLastPlayer=block.number+1;    
        if (pendingRound && blockLastPlayer!=blockEndRound ) endRound();
	else if (pendingRound && blockLastPlayer==blockEndRound) throw;
	_;
    }
    uint blockLastPlayer;
    address private owner;
    uint gamble_value;
    uint information_cost;
    uint round_max_size ;
    uint round_min_size  ;  
    uint index_player;
    uint index_round_ended;
    uint index_player_in_round;
    bool pendingRound = false;
    uint blockEndRound;
    struct Gamble  {
	    address player;
	    bool flipped;
    }
    Gamble[] matchers; 
    Gamble[] contrarians;
    struct Result  {
	    address player_matcher;
	    bool flipped_matcher;
	    uint256 payout_matcher;
	    address player_contrarian;
	    bool flipped_contrarian;
	    uint256 payout_contrarian;
    }
    Result[] results; 
    mapping (address => uint) payout_history;
    mapping (address => uint) times_played_history;    
    function Matching_Ethers() { 
	    owner = msg.sender; 
	    round_min_size = 16;
	    round_max_size = 20;
	    information_cost= 500 szabo; 
            gamble_value = 100000 szabo; 
    }
    function () { 
        bool flipped;
        if (msg.value == gamble_value) flipped=false; 
        if (msg.value > gamble_value) {
            flipped=true;
        }
        Play(flipped); 
    }
    function Play(bool flipped) equalGambleValue onlyActive resolvePendingRound{
        if ( index_player_in_round%2==0 ) {   
	    matchers.push(Gamble(msg.sender, flipped));
	}
	else {
	    contrarians.push(Gamble(msg.sender, flipped));
	}
        index_player+=1;
        index_player_in_round+=1;
	times_played_history[msg.sender]+=1;
        if (index_player_in_round>=round_min_size && index_player_in_round%2==0) {
	            bool end = randomEnd();
		    if (end) {
		        pendingRound=true;
			blockEndRound=block.number;}
        }
    }
    function randomGen(uint seed, uint range) private constant returns (uint randomNumber) {
        return(uint(sha3(block.blockhash(block.number-1), seed))%range+1);
    }
    function randomEnd() private returns(bool) {
	if (index_player_in_round==round_max_size) return true; 
	else{
	    uint random = randomGen(index_player, (round_max_size-index_player_in_round)/2+1);
	    if (random==1) return true;
	    else return false;
	    }
    }
    function endRound() private {
        delete results;
        uint256 random_start_contrarian = randomGen(index_player,(index_player_in_round)/2)-1;
        uint256 payout_total;
        for (var k = 0; k < (index_player_in_round)/2; k++) {
            uint256 index_contrarian;
	    if (k+random_start_contrarian<(index_player_in_round)/2){
	        index_contrarian=k+random_start_contrarian;
            }
	    else{
	        index_contrarian=(k+random_start_contrarian)-(index_player_in_round/2);
	    }
	    uint256 information_cost_matcher = information_cost * k;
	    uint256 payout_matcher = 2*(gamble_value-information_cost_matcher);
	    uint256 information_cost_contrarian = information_cost * index_contrarian;
	    uint256 payout_contrarian = 2*(gamble_value-information_cost_contrarian);
	    results.push(Result(matchers[k].player,matchers[k].flipped,payout_matcher,contrarians[index_contrarian].player,contrarians[index_contrarian].flipped, payout_contrarian));
	    if (matchers[k].flipped == contrarians[index_contrarian].flipped) {
	        matchers[k].player.send(payout_matcher);
		payout_total+=payout_matcher;
		payout_history[matchers[k].player]+=payout_matcher;
	    }
	    else {
	        contrarians[index_contrarian].player.send(payout_contrarian);
		payout_total+=payout_contrarian;
		payout_history[contrarians[k].player]+=payout_contrarian;
	    }
	}
        index_round_ended+=1;
        owner.send(index_player_in_round*gamble_value-payout_total);
	payout_total=0;
        index_player_in_round=0;
        delete matchers;
        delete contrarians;
	pendingRound=false;
	if (terminate_after_round==true) state=State.Deactivated;
    }
    function refundRound() 
    onlyActive
    onlyOwner noEthSent{  
        uint totalRefund;
	uint balanceBeforeRefund=this.balance;
        for (var k = 0;  k< matchers.length; k++) {
	            matchers[k].player.send(gamble_value);
		    totalRefund+=gamble_value;
        }
        for (var j = 0;  j< contrarians.length ; j++) {	
	            contrarians[j].player.send(gamble_value);
		    totalRefund+=gamble_value;		    
        }
	delete matchers;
	delete contrarians;
	state=State.Deactivated;
	index_player_in_round=0;
        uint balanceLeft = balanceBeforeRefund-totalRefund;
	if (balanceLeft >0) owner.send(balanceLeft);
    }
    bool terminate_after_round=false;
    function deactivate()
    onlyOwner noEthSent{
	    terminate_after_round=true;
    }
    function reactivate()
    onlyOwner noEthSent{
        state=State.Active;
        terminate_after_round=false;
    }
    function config(uint new_max_round, uint new_min_round, uint new_information_cost, uint new_gamble_value)
	    onlyOwner
	    onlyInactive noEthSent{
	    if (new_max_round<new_min_round) throw;
	    if (new_information_cost > new_gamble_value/100) throw;
	    round_max_size = new_max_round;
	    round_min_size = new_min_round;
	    information_cost= new_information_cost;
	    gamble_value = new_gamble_value;
    }
    function changeOwner(address new_owner)
	    onlyOwner noEthSent{
	    owner=new_owner;
    }
    modifier noEthSent(){
        if (msg.value>0) throw;
	_;
    }
    function gameStats() noEthSent constant returns (uint number_of_player_in_round, uint total_number_of_player, uint number_of_round_ended, bool pending_round_to_resolve, uint block_end_last_round, uint block_last_player, State state, bool pause_contract_after_round)
    {
         number_of_player_in_round = index_player_in_round;
	 total_number_of_player = index_player;
	 number_of_round_ended = index_round_ended;
	 pending_round_to_resolve = pendingRound;
	 block_end_last_round = blockEndRound;
	 block_last_player = blockLastPlayer;
	 state = state;
	 pause_contract_after_round = terminate_after_round;
     }
     function gameSettings() noEthSent constant returns (uint _gamble_value, uint _information_cost, uint _round_min_size, uint _round_max_size) {
	 _gamble_value = gamble_value;
	 _information_cost = information_cost;
	 _round_min_size = round_min_size;
	 _round_max_size = round_max_size;
     }
    function getMatchers_by_index(uint _index) noEthSent constant returns (address _address, bool _flipped) {
        _address=matchers[_index].player;
	_flipped = matchers[_index].flipped;
    }
    function getContrarians_by_index(uint _index) noEthSent constant returns (address _address, bool _flipped) {
        _address=contrarians[_index].player;
	_flipped = contrarians[_index].flipped;
    }
    function getLastRoundResults_by_index(uint _index) noEthSent constant returns (address _address_matcher, address _address_contrarian, bool _flipped_matcher, bool _flipped_contrarian, uint _payout_matcher, uint _payout_contrarian) {
        _address_matcher=results[_index].player_matcher;
        _address_contrarian=results[_index].player_contrarian;
	_flipped_matcher = results[_index].flipped_matcher;
	_flipped_contrarian = results[_index].flipped_contrarian;
	_payout_matcher =  results[_index].payout_matcher;
	_payout_contrarian =  results[_index].payout_contrarian;
    }
     mapping (address => string) nicknames;
     function setNickname(string name) noEthSent{
         if (bytes(name).length >= 2 && bytes(name).length <= 16)
             nicknames[msg.sender] = name;
     }
     function getNickname(address _address) noEthSent constant returns(string _name) {
             _name = nicknames[_address];
     }
     function historyPayout(address _address) noEthSent constant returns(uint _payout) {
             _payout = payout_history[_address]; 
     }
     function historyTimesPlayed(address _address) noEthSent constant returns(uint _count) {
             _count = times_played_history[_address]; 
     }
}
```

## RQ1_bae823e736e2

SHA-256 `8f7f8f2bf6d59994a799c4f6f82cf213ef4f7e919676abfecfa545238aa7758d`

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

SHA-256 `1cd6fab046cdc03d433dca148f4c55444124c7090c005c705873fc78c9c87dcd`

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

## RQ1_c9a2d9b618a7

SHA-256 `fc06a0d67768aa374430d543efa148592b6356296282652000837d51995f7438`

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
    uint public presaleTokenSupply = 0;
    uint public presaleEtherRaised = 0;
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

## RQ1_f25b185c19f2

SHA-256 `b3dabd1cc25c75f1276412176d3b91b127d774ec281b8104de4c2cbbc1b606d6`

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

SHA-256 `d908fdd132703302c153a624d567c80b69c4d2022c1f7be61e6b4ec853ad36e2`

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
