# 本批实际输入源码

按输入原字节 SHA 核对。源码位置采用 UTF-8 字节偏移。

## RQ1_f479ab27bf80

SHA-256 `8cf81564e19167bcf4cc61ffba3380e12b0e11a4e5c2a103dddcec46fa6c5eca`

```solidity
pragma solidity ^0.4.24;
contract ILiquidPledgingPlugin {
    function beforeTransfer(
        uint64 pledgeManager,
        uint64 pledgeFrom,
        uint64 pledgeTo,
        uint64 context,
        uint amount ) returns (uint maxAllowed);
    function afterTransfer(
        uint64 pledgeManager,
        uint64 pledgeFrom,
        uint64 pledgeTo,
        uint64 context,
        uint amount
    );
}
contract Owned {
    address public owner;
    address public newOwnerCandidate;
    event OwnershipRequested(address indexed by, address indexed to);
    event OwnershipTransferred(address indexed from, address indexed to);
    event OwnershipRemoved();
    function Owned() public {
        owner = msg.sender;
    }
    modifier onlyOwner() {
        require (msg.sender == owner);
        _;
    }
    function proposeOwnership(address _newOwnerCandidate) public onlyOwner {
        newOwnerCandidate = _newOwnerCandidate;
        OwnershipRequested(msg.sender, newOwnerCandidate);
    }
    function acceptOwnership() public {
        require(msg.sender == newOwnerCandidate);
        address oldOwner = owner;
        owner = newOwnerCandidate;
        newOwnerCandidate = 0x0;
        OwnershipTransferred(oldOwner, owner);
    }
    function changeOwnership(address _newOwner) public onlyOwner {
        require(_newOwner != 0x0);
        address oldOwner = owner;
        owner = _newOwner;
        newOwnerCandidate = 0x0;
        OwnershipTransferred(oldOwner, owner);
    }
    function removeOwnership(address _dac) public onlyOwner {
        require(_dac == 0xdac);
        owner = 0x0;
        newOwnerCandidate = 0x0;
        OwnershipRemoved();     
    }
} 
contract ERC20 {
    function totalSupply() public constant returns (uint256 supply);
    function balanceOf(address _owner) public constant returns (uint256 balance);
    function transfer(address _to, uint256 _value) public returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);
    function approve(address _spender, uint256 _value) public returns (bool success);
    function allowance(address _owner, address _spender) public constant returns (uint256 remaining);
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}
contract Escapable is Owned {
    address public escapeHatchCaller;
    address public escapeHatchDestination;
    mapping (address=>bool) private escapeBlacklist; 
    function Escapable(address _escapeHatchCaller, address _escapeHatchDestination) public {
        escapeHatchCaller = _escapeHatchCaller;
        escapeHatchDestination = _escapeHatchDestination;
    }
    modifier onlyEscapeHatchCallerOrOwner {
        require ((msg.sender == escapeHatchCaller)||(msg.sender == owner));
        _;
    }
    function blacklistEscapeToken(address _token) internal {
        escapeBlacklist[_token] = true;
        EscapeHatchBlackistedToken(_token);
    }
    function isTokenEscapable(address _token) constant public returns (bool) {
        return !escapeBlacklist[_token];
    }
    function escapeHatch(address _token) public onlyEscapeHatchCallerOrOwner {   
        require(escapeBlacklist[_token]==false);
        uint256 balance;
        if (_token == 0x0) {
            balance = this.balance;
            escapeHatchDestination.transfer(balance);
            EscapeHatchCalled(_token, balance);
            return;
        }
        ERC20 token = ERC20(_token);
        balance = token.balanceOf(this);
        require(token.transfer(escapeHatchDestination, balance));
        EscapeHatchCalled(_token, balance);
    }
    function changeHatchEscapeCaller(address _newEscapeHatchCaller) public onlyEscapeHatchCallerOrOwner {
        escapeHatchCaller = _newEscapeHatchCaller;
    }
    event EscapeHatchBlackistedToken(address token);
    event EscapeHatchCalled(address token, uint amount);
}
interface LPVault {
    function authorizePayment(bytes32 _ref, address _dest, uint _amount);
    function () payable;
}
contract LiquidPledgingBase is Escapable {
    uint constant MAX_DELEGATES = 10;
    uint constant MAX_SUBPROJECT_LEVEL = 20;
    uint constant MAX_INTERPROJECT_LEVEL = 20;
    enum PledgeAdminType { Giver, Delegate, Project }
    enum PledgeState { Pledged, Paying, Paid }
    struct PledgeAdmin { 
        PledgeAdminType adminType; 
        address addr; 
        string name;
        string url;  
        uint64 commitTime;  
        uint64 parentProject;  
        bool canceled;      
        ILiquidPledgingPlugin plugin; 
    }
    struct Pledge {
        uint amount;
        uint64 owner; 
        uint64[] delegationChain; 
        uint64 intendedProject; 
        uint64 commitTime;  
        uint64 oldPledge; 
        PledgeState pledgeState; 
    }
    Pledge[] pledges;
    PledgeAdmin[] admins; 
    LPVault public vault;
    mapping (bytes32 => uint64) hPledge2idx;
    mapping (bytes32 => bool) pluginWhitelist;
    bool public usePluginWhitelist = true;
    modifier onlyVault() {
        require(msg.sender == address(vault));
        _;
    }
    function LiquidPledgingBase(
        address _vault,
        address _escapeHatchCaller,
        address _escapeHatchDestination
    ) Escapable(_escapeHatchCaller, _escapeHatchDestination) public {
        admins.length = 1; 
        pledges.length = 1; 
        vault = LPVault(_vault); 
    }
    function addGiver(
        string name,
        string url,
        uint64 commitTime,
        ILiquidPledgingPlugin plugin
    ) returns (uint64 idGiver) {
        require(isValidPlugin(plugin)); 
        idGiver = uint64(admins.length);
        admins.push(PledgeAdmin(
            PledgeAdminType.Giver,
            msg.sender,
            name,
            url,
            commitTime,
            0,
            false,
            plugin));
        GiverAdded(idGiver);
    }
    event GiverAdded(uint64 indexed idGiver);
    function updateGiver(
        uint64 idGiver,
        address newAddr,
        string newName,
        string newUrl,
        uint64 newCommitTime)
    {
        PledgeAdmin storage giver = findAdmin(idGiver);
        require(giver.adminType == PledgeAdminType.Giver); 
        require(giver.addr == msg.sender); 
        giver.addr = newAddr;
        giver.name = newName;
        giver.url = newUrl;
        giver.commitTime = newCommitTime;
        GiverUpdated(idGiver);
    }
    event GiverUpdated(uint64 indexed idGiver);
    function addDelegate(
        string name,
        string url,
        uint64 commitTime,
        ILiquidPledgingPlugin plugin
    ) returns (uint64 idDelegate) { 
        require(isValidPlugin(plugin)); 
        idDelegate = uint64(admins.length);
        admins.push(PledgeAdmin(
            PledgeAdminType.Delegate,
            msg.sender,
            name,
            url,
            commitTime,
            0,
            false,
            plugin));
        DelegateAdded(idDelegate);
    }
    event DelegateAdded(uint64 indexed idDelegate);
    function updateDelegate(
        uint64 idDelegate,
        address newAddr,
        string newName,
        string newUrl,
        uint64 newCommitTime) {
        PledgeAdmin storage delegate = findAdmin(idDelegate);
        require(delegate.adminType == PledgeAdminType.Delegate);
        require(delegate.addr == msg.sender);
        delegate.addr = newAddr;
        delegate.name = newName;
        delegate.url = newUrl;
        delegate.commitTime = newCommitTime;
        DelegateUpdated(idDelegate);
    }
    event DelegateUpdated(uint64 indexed idDelegate);
    function addProject(
        string name,
        string url,
        address projectAdmin,
        uint64 parentProject,
        uint64 commitTime,
        ILiquidPledgingPlugin plugin
    ) returns (uint64 idProject) {
        require(isValidPlugin(plugin));
        if (parentProject != 0) {
            PledgeAdmin storage pa = findAdmin(parentProject);
            require(pa.adminType == PledgeAdminType.Project);
            require(getProjectLevel(pa) < MAX_SUBPROJECT_LEVEL);
        }
        idProject = uint64(admins.length);
        admins.push(PledgeAdmin(
            PledgeAdminType.Project,
            projectAdmin,
            name,
            url,
            commitTime,
            parentProject,
            false,
            plugin));
        ProjectAdded(idProject);
    }
    event ProjectAdded(uint64 indexed idProject);
    function updateProject(
        uint64 idProject,
        address newAddr,
        string newName,
        string newUrl,
        uint64 newCommitTime)
    {
        PledgeAdmin storage project = findAdmin(idProject);
        require(project.adminType == PledgeAdminType.Project);
        require(project.addr == msg.sender);
        project.addr = newAddr;
        project.name = newName;
        project.url = newUrl;
        project.commitTime = newCommitTime;
        ProjectUpdated(idProject);
    }
    event ProjectUpdated(uint64 indexed idAdmin);
    function numberOfPledges() constant returns (uint) {
        return pledges.length - 1;
    }
    function getPledge(uint64 idPledge) constant returns(
        uint amount,
        uint64 owner,
        uint64 nDelegates,
        uint64 intendedProject,
        uint64 commitTime,
        uint64 oldPledge,
        PledgeState pledgeState
    ) {
        Pledge storage p = findPledge(idPledge);
        amount = p.amount;
        owner = p.owner;
        nDelegates = uint64(p.delegationChain.length);
        intendedProject = p.intendedProject;
        commitTime = p.commitTime;
        oldPledge = p.oldPledge;
        pledgeState = p.pledgeState;
    }
    function getPledgeDelegate(uint64 idPledge, uint idxDelegate) constant returns(
        uint64 idDelegate,
        address addr,
        string name
    ) {
        Pledge storage p = findPledge(idPledge);
        idDelegate = p.delegationChain[idxDelegate - 1];
        PledgeAdmin storage delegate = findAdmin(idDelegate);
        addr = delegate.addr;
        name = delegate.name;
    }
    function numberOfPledgeAdmins() constant returns(uint) {
        return admins.length - 1;
    }
    function getPledgeAdmin(uint64 idAdmin) constant returns (
        PledgeAdminType adminType,
        address addr,
        string name,
        string url,
        uint64 commitTime,
        uint64 parentProject,
        bool canceled,
        address plugin)
    {
        PledgeAdmin storage m = findAdmin(idAdmin);
        adminType = m.adminType;
        addr = m.addr;
        name = m.name;
        url = m.url;
        commitTime = m.commitTime;
        parentProject = m.parentProject;
        canceled = m.canceled;
        plugin = address(m.plugin);
    }
    function findOrCreatePledge(
        uint64 owner,
        uint64[] delegationChain,
        uint64 intendedProject,
        uint64 commitTime,
        uint64 oldPledge,
        PledgeState state
        ) internal returns (uint64)
    {
        bytes32 hPledge = sha3(
            owner, delegationChain, intendedProject, commitTime, oldPledge, state);
        uint64 idx = hPledge2idx[hPledge];
        if (idx > 0) return idx;
        idx = uint64(pledges.length);
        hPledge2idx[hPledge] = idx;
        pledges.push(Pledge(
            0, owner, delegationChain, intendedProject, commitTime, oldPledge, state));
        return idx;
    }
    function findAdmin(uint64 idAdmin) internal returns (PledgeAdmin storage) {
        require(idAdmin < admins.length);
        return admins[idAdmin];
    }
    function findPledge(uint64 idPledge) internal returns (Pledge storage) {
        require(idPledge < pledges.length);
        return pledges[idPledge];
    }
    uint64 constant  NOTFOUND = 0xFFFFFFFFFFFFFFFF;
    function getDelegateIdx(Pledge p, uint64 idDelegate) internal returns(uint64) {
        for (uint i=0; i < p.delegationChain.length; i++) {
            if (p.delegationChain[i] == idDelegate) return uint64(i);
        }
        return NOTFOUND;
    }
    function getPledgeLevel(Pledge p) internal returns(uint) {
        if (p.oldPledge == 0) return 0;
        Pledge storage oldN = findPledge(p.oldPledge);
        return getPledgeLevel(oldN) + 1; 
    }
    function maxCommitTime(Pledge p) internal returns(uint commitTime) {
        PledgeAdmin storage m = findAdmin(p.owner);
        commitTime = m.commitTime; 
        for (uint i=0; i<p.delegationChain.length; i++) {
            m = findAdmin(p.delegationChain[i]);
            if (m.commitTime > commitTime) commitTime = m.commitTime;
        }
    }
    function getProjectLevel(PledgeAdmin m) internal returns(uint) {
        assert(m.adminType == PledgeAdminType.Project);
        if (m.parentProject == 0) return(1);
        PledgeAdmin storage parentNM = findAdmin(m.parentProject);
        return getProjectLevel(parentNM) + 1;
    }
    function isProjectCanceled(uint64 projectId) constant returns (bool) {
        PledgeAdmin storage m = findAdmin(projectId);
        if (m.adminType == PledgeAdminType.Giver) return false;
        assert(m.adminType == PledgeAdminType.Project);
        if (m.canceled) return true;
        if (m.parentProject == 0) return false;
        return isProjectCanceled(m.parentProject);
    }
    function getOldestPledgeNotCanceled(uint64 idPledge
        ) internal constant returns(uint64) {
        if (idPledge == 0) return 0;
        Pledge storage p = findPledge(idPledge);
        PledgeAdmin storage admin = findAdmin(p.owner);
        if (admin.adminType == PledgeAdminType.Giver) return idPledge;
        assert(admin.adminType == PledgeAdminType.Project);
        if (!isProjectCanceled(p.owner)) return idPledge;
        return getOldestPledgeNotCanceled(p.oldPledge);
    }
    function checkAdminOwner(PledgeAdmin m) internal constant {
        require((msg.sender == m.addr) || (msg.sender == address(m.plugin)));
    }
    function addValidPlugin(bytes32 contractHash) external onlyOwner {
        pluginWhitelist[contractHash] = true;
    }
    function removeValidPlugin(bytes32 contractHash) external onlyOwner {
        pluginWhitelist[contractHash] = false;
    }
    function useWhitelist(bool useWhitelist) external onlyOwner {
        usePluginWhitelist = useWhitelist;
    }
    function isValidPlugin(address addr) public returns(bool) {
        if (!usePluginWhitelist || addr == 0x0) return true;
        bytes32 contractHash = getCodeHash(addr);
        return pluginWhitelist[contractHash];
    }
    function getCodeHash(address addr) public returns(bytes32) {
        bytes memory o_code;
        assembly {
            let size := extcodesize(addr)
            o_code := mload(0x40)
            mstore(0x40, add(o_code, and(add(add(size, 0x20), 0x1f), not(0x1f))))
            mstore(o_code, size)
            extcodecopy(addr, add(o_code, 0x20), 0, size)
        }
        return keccak256(o_code);
    }
}
contract LiquidPledging is LiquidPledgingBase {
    function LiquidPledging(
        address _vault,
        address _escapeHatchCaller,
        address _escapeHatchDestination
    ) LiquidPledgingBase(_vault, _escapeHatchCaller, _escapeHatchDestination) {
    }
    function donate(uint64 idGiver, uint64 idReceiver) payable {
        if (idGiver == 0) {
            idGiver = addGiver("", "", 259200, ILiquidPledgingPlugin(0x0));
        }
        PledgeAdmin storage sender = findAdmin(idGiver);
        checkAdminOwner(sender);
        require(sender.adminType == PledgeAdminType.Giver);
        uint amount = msg.value;
        require(amount > 0);
        vault.transfer(amount); 
        uint64 idPledge = findOrCreatePledge(
            idGiver,
            new uint64[](0), 
            0,
            0,
            0,
            PledgeState.Pledged
        );
        Pledge storage nTo = findPledge(idPledge);
        nTo.amount += amount;
        Transfer(0, idPledge, amount); 
        transfer(idGiver, idPledge, amount, idReceiver); 
    }
    function transfer( 
        uint64 idSender,
        uint64 idPledge,
        uint amount,
        uint64 idReceiver
    ){
        idPledge = normalizePledge(idPledge);
        Pledge storage p = findPledge(idPledge);
        PledgeAdmin storage receiver = findAdmin(idReceiver);
        PledgeAdmin storage sender = findAdmin(idSender);
        checkAdminOwner(sender);
        require(p.pledgeState == PledgeState.Pledged);
        if (p.owner == idSender) {
            if (receiver.adminType == PledgeAdminType.Giver) {
                transferOwnershipToGiver(idPledge, amount, idReceiver);
            } else if (receiver.adminType == PledgeAdminType.Project) {
                transferOwnershipToProject(idPledge, amount, idReceiver);
            } else if (receiver.adminType == PledgeAdminType.Delegate) {
                uint recieverDIdx = getDelegateIdx(p, idReceiver);
                if (p.intendedProject > 0 && recieverDIdx != NOTFOUND) {
                    if (recieverDIdx == p.delegationChain.length - 1) {
                        uint64 toPledge = findOrCreatePledge(
                            p.owner,
                            p.delegationChain,
                            0,
                            0,
                            p.oldPledge,
                            PledgeState.Pledged);
                        doTransfer(idPledge, toPledge, amount);
                    } else {
                        undelegate(idPledge, amount, p.delegationChain.length - receiverDIdx - 1);
                    }
                } else {
                    idPledge = undelegate(
                        idPledge,
                        amount,
                        p.delegationChain.length
                    );
                    appendDelegate(idPledge, amount, idReceiver);
                }
            } else {
                assert(false);
            }
            return;
        }
        uint senderDIdx = getDelegateIdx(p, idSender);
        if (senderDIdx != NOTFOUND) {
            if (receiver.adminType == PledgeAdminType.Giver) {
                assert(p.owner == idReceiver);
                undelegate(idPledge, amount, p.delegationChain.length);
                return;
            }
            if (receiver.adminType == PledgeAdminType.Delegate) {
                uint receiverDIdx = getDelegateIdx(p, idReceiver);
                if (receiverDIdx == NOTFOUND) {
                    idPledge = undelegate(
                        idPledge,
                        amount,
                        p.delegationChain.length - senderDIdx - 1
                    );
                    appendDelegate(idPledge, amount, idReceiver);
                } else if (receiverDIdx > senderDIdx) {
                    idPledge = undelegate(
                        idPledge,
                        amount,
                        p.delegationChain.length - senderDIdx - 1
                    );
                    appendDelegate(idPledge, amount, idReceiver);
                } else if (receiverDIdx <= senderDIdx) {
                    undelegate(
                        idPledge,
                        amount,
                        p.delegationChain.length - receiverDIdx - 1
                    );
                }
                return;
            }
            if (receiver.adminType == PledgeAdminType.Project) {
                idPledge = undelegate(
                    idPledge,
                    amount,
                    p.delegationChain.length - senderDIdx - 1
                );
                proposeAssignProject(idPledge, amount, idReceiver);
                return;
            }
        }
        assert(false);  
    }
    function withdraw(uint64 idPledge, uint amount) {
        idPledge = normalizePledge(idPledge); 
        Pledge storage p = findPledge(idPledge);
        require(p.pledgeState == PledgeState.Pledged);
        PledgeAdmin storage owner = findAdmin(p.owner);
        checkAdminOwner(owner);
        uint64 idNewPledge = findOrCreatePledge(
            p.owner,
            p.delegationChain,
            0,
            0,
            p.oldPledge,
            PledgeState.Paying
        );
        doTransfer(idPledge, idNewPledge, amount);
        vault.authorizePayment(bytes32(idNewPledge), owner.addr, amount);
    }
    function confirmPayment(uint64 idPledge, uint amount) onlyVault {
        Pledge storage p = findPledge(idPledge);
        require(p.pledgeState == PledgeState.Paying);
        uint64 idNewPledge = findOrCreatePledge(
            p.owner,
            p.delegationChain,
            0,
            0,
            p.oldPledge,
            PledgeState.Paid
        );
        doTransfer(idPledge, idNewPledge, amount);
    }
    function cancelPayment(uint64 idPledge, uint amount) onlyVault {
        Pledge storage p = findPledge(idPledge);
        require(p.pledgeState == PledgeState.Paying); 
        uint64 oldPledge = findOrCreatePledge(
            p.owner,
            p.delegationChain,
            0,
            0,
            p.oldPledge,
            PledgeState.Pledged
        );
        oldPledge = normalizePledge(oldPledge);
        doTransfer(idPledge, oldPledge, amount);
    }
    function cancelProject(uint64 idProject) { 
        PledgeAdmin storage project = findAdmin(idProject);
        checkAdminOwner(project);
        project.canceled = true;
        CancelProject(idProject);
    }
    function cancelPledge(uint64 idPledge, uint amount) { 
        idPledge = normalizePledge(idPledge);
        Pledge storage p = findPledge(idPledge);
        require(p.oldPledge != 0);
        PledgeAdmin storage m = findAdmin(p.owner);
        checkAdminOwner(m);
        uint64 oldPledge = getOldestPledgeNotCanceled(p.oldPledge);
        doTransfer(idPledge, oldPledge, amount);
    }
    uint constant D64 = 0x10000000000000000;
    function mTransfer(
        uint64 idSender,
        uint[] pledgesAmounts,
        uint64 idReceiver
    ) {
        for (uint i = 0; i < pledgesAmounts.length; i++ ) {
            uint64 idPledge = uint64( pledgesAmounts[i] & (D64-1) );
            uint amount = pledgesAmounts[i] / D64;
            transfer(idSender, idPledge, amount, idReceiver);
        }
    }
    function mWithdraw(uint[] pledgesAmounts) {
        for (uint i = 0; i < pledgesAmounts.length; i++ ) {
            uint64 idPledge = uint64( pledgesAmounts[i] & (D64-1) );
            uint amount = pledgesAmounts[i] / D64;
            withdraw(idPledge, amount);
        }
    }
    function mConfirmPayment(uint[] pledgesAmounts) {
        for (uint i = 0; i < pledgesAmounts.length; i++ ) {
            uint64 idPledge = uint64( pledgesAmounts[i] & (D64-1) );
            uint amount = pledgesAmounts[i] / D64;
            confirmPayment(idPledge, amount);
        }
    }
    function mCancelPayment(uint[] pledgesAmounts) {
        for (uint i = 0; i < pledgesAmounts.length; i++ ) {
            uint64 idPledge = uint64( pledgesAmounts[i] & (D64-1) );
            uint amount = pledgesAmounts[i] / D64;
            cancelPayment(idPledge, amount);
        }
    }
    function mNormalizePledge(uint64[] pledges) {
        for (uint i = 0; i < pledges.length; i++ ) {
            normalizePledge( pledges[i] );
        }
    }
    function transferOwnershipToProject(
        uint64 idPledge,
        uint amount,
        uint64 idReceiver
    ) internal {
        Pledge storage p = findPledge(idPledge);
        require(getPledgeLevel(p) < MAX_INTERPROJECT_LEVEL);
        require(!isProjectCanceled(idReceiver));
        uint64 oldPledge = findOrCreatePledge(
            p.owner,
            p.delegationChain,
            0,
            0,
            p.oldPledge,
            PledgeState.Pledged
        );
        uint64 toPledge = findOrCreatePledge(
            idReceiver,                     
            new uint64[](0),                
            0,
            0,
            oldPledge,
            PledgeState.Pledged
        );
        doTransfer(idPledge, toPledge, amount);
    }   
    function transferOwnershipToGiver(
        uint64 idPledge,
        uint amount,
        uint64 idReceiver
    ) internal {
        uint64 toPledge = findOrCreatePledge(
            idReceiver,
            new uint64[](0),
            0,
            0,
            0,
            PledgeState.Pledged
        );
        doTransfer(idPledge, toPledge, amount);
    }
    function appendDelegate(
        uint64 idPledge,
        uint amount,
        uint64 idReceiver
    ) internal {
        Pledge storage p = findPledge(idPledge);
        require(p.delegationChain.length < MAX_DELEGATES);
        uint64[] memory newDelegationChain = new uint64[](
            p.delegationChain.length + 1
        );
        for (uint i = 0; i<p.delegationChain.length; i++) {
            newDelegationChain[i] = p.delegationChain[i];
        }
        newDelegationChain[p.delegationChain.length] = idReceiver;
        uint64 toPledge = findOrCreatePledge(
            p.owner,
            newDelegationChain,
            0,
            0,
            p.oldPledge,
            PledgeState.Pledged
        );
        doTransfer(idPledge, toPledge, amount);
    }
    function undelegate(
        uint64 idPledge,
        uint amount,
        uint q
    ) internal returns (uint64)
    {
        Pledge storage p = findPledge(idPledge);
        uint64[] memory newDelegationChain = new uint64[](
            p.delegationChain.length - q
        );
        for (uint i=0; i<p.delegationChain.length - q; i++) {
            newDelegationChain[i] = p.delegationChain[i];
        }
        uint64 toPledge = findOrCreatePledge(
            p.owner,
            newDelegationChain,
            0,
            0,
            p.oldPledge,
            PledgeState.Pledged
        );
        doTransfer(idPledge, toPledge, amount);
        return toPledge;
    }
    function proposeAssignProject(
        uint64 idPledge,
        uint amount,
        uint64 idReceiver
    ) internal {
        Pledge storage p = findPledge(idPledge);
        require(getPledgeLevel(p) < MAX_INTERPROJECT_LEVEL);
        require(!isProjectCanceled(idReceiver));
        uint64 toPledge = findOrCreatePledge(
            p.owner,
            p.delegationChain,
            idReceiver,
            uint64(getTime() + maxCommitTime(p)),
            p.oldPledge,
            PledgeState.Pledged
        );
        doTransfer(idPledge, toPledge, amount);
    }
    function doTransfer(uint64 from, uint64 to, uint _amount) internal {
        uint amount = callPlugins(true, from, to, _amount);
        if (from == to) { 
            return;
        }
        if (amount == 0) {
            return;
        }
        Pledge storage nFrom = findPledge(from);
        Pledge storage nTo = findPledge(to);
        require(nFrom.amount >= amount);
        nFrom.amount -= amount;
        nTo.amount += amount;
        Transfer(from, to, amount);
        callPlugins(false, from, to, amount);
    }
    function normalizePledge(uint64 idPledge) returns(uint64) {
        Pledge storage p = findPledge(idPledge);
        if (p.pledgeState != PledgeState.Pledged) {
            return idPledge;
        }
        if ((p.intendedProject > 0) && ( getTime() > p.commitTime)) {
            uint64 oldPledge = findOrCreatePledge(
                p.owner,
                p.delegationChain,
                0,
                0,
                p.oldPledge,
                PledgeState.Pledged
            );
            uint64 toPledge = findOrCreatePledge(
                p.intendedProject,
                new uint64[](0),
                0,
                0,
                oldPledge,
                PledgeState.Pledged
            );
            doTransfer(idPledge, toPledge, p.amount);
            idPledge = toPledge;
            p = findPledge(idPledge);
        }
        toPledge = getOldestPledgeNotCanceled(idPledge);
        if (toPledge != idPledge) {
            doTransfer(idPledge, toPledge, p.amount);
        }
        return toPledge;
    }
    function callPlugin(
        bool before,
        uint64 adminId,
        uint64 fromPledge,
        uint64 toPledge,
        uint64 context,
        uint amount
    ) internal returns (uint allowedAmount) {
        uint newAmount;
        allowedAmount = amount;
        PledgeAdmin storage admin = findAdmin(adminId);
        if ((address(admin.plugin) != 0) && (allowedAmount > 0)) {
            if (before) {
                newAmount = admin.plugin.beforeTransfer(
                    adminId,
                    fromPledge,
                    toPledge,
                    context,
                    amount
                );
                require(newAmount <= allowedAmount);
                allowedAmount = newAmount;
            } else {
                admin.plugin.afterTransfer(
                    adminId,
                    fromPledge,
                    toPledge,
                    context,
                    amount
                );
            }
        }
    }
    function callPluginsPledge(
        bool before,
        uint64 idPledge,
        uint64 fromPledge,
        uint64 toPledge,
        uint amount
    ) internal returns (uint allowedAmount) {
        uint64 offset = idPledge == fromPledge ? 0 : 256;
        allowedAmount = amount;
        Pledge storage p = findPledge(idPledge);
        allowedAmount = callPlugin(
            before,
            p.owner,
            fromPledge,
            toPledge,
            offset,
            allowedAmount
        );
        for (uint64 i=0; i<p.delegationChain.length; i++) {
            allowedAmount = callPlugin(
                before,
                p.delegationChain[i],
                fromPledge,
                toPledge,
                offset + i+1,
                allowedAmount
            );
        }
        if (p.intendedProject > 0) {
            allowedAmount = callPlugin(
                before,
                p.intendedProject,
                fromPledge,
                toPledge,
                offset + 255,
                allowedAmount
            );
        }
    }
    function callPlugins(
        bool before,
        uint64 fromPledge,
        uint64 toPledge,
        uint amount
    ) internal returns (uint allowedAmount) {
        allowedAmount = amount;
        allowedAmount = callPluginsPledge(
            before,
            fromPledge,
            fromPledge,
            toPledge,
            allowedAmount
        );
        allowedAmount = callPluginsPledge(
            before,
            toPledge,
            fromPledge,
            toPledge,
            allowedAmount
        );
    }
    function getTime() internal returns (uint) {
        return now;
    }
    event Transfer(uint64 indexed from, uint64 indexed to, uint amount);
    event CancelProject(uint64 indexed idProject);
}
contract Controlled {
    modifier onlyController { require(msg.sender == controller); _; }
    address public controller;
    function Controlled() public { controller = msg.sender;}
    function changeController(address _newController) public onlyController {
        controller = _newController;
    }
}
contract TokenController {
    function proxyPayment(address _owner) public payable returns(bool);
    function onTransfer(address _from, address _to, uint _amount) public returns(bool);
    function onApprove(address _owner, address _spender, uint _amount) public
        returns(bool);
}
contract ApproveAndCallFallBack {
    function receiveApproval(address from, uint256 _amount, address _token, bytes _data) public;
}
contract MiniMeToken is Controlled {
    string public name;                
    uint8 public decimals;             
    string public symbol;              
    string public version = 'MMT_0.2'; 
    struct  Checkpoint {
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
    function MiniMeToken(
        address _tokenFactory,
        address _parentToken,
        uint _parentSnapShotBlock,
        string _tokenName,
        uint8 _decimalUnits,
        string _tokenSymbol,
        bool _transfersEnabled
    ) public {
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
    function transferFrom(address _from, address _to, uint256 _amount
    ) public returns (bool success) {
        if (msg.sender != controller) {
            require(transfersEnabled);
            if (allowed[_from][msg.sender] < _amount) return false;
            allowed[_from][msg.sender] -= _amount;
        }
        return doTransfer(_from, _to, _amount);
    }
    function doTransfer(address _from, address _to, uint _amount
    ) internal returns(bool) {
           if (_amount == 0) {
               return true;
           }
           require(parentSnapShotBlock < block.number);
           require((_to != 0) && (_to != address(this)));
           var previousBalanceFrom = balanceOfAt(_from, block.number);
           if (previousBalanceFrom < _amount) {
               return false;
           }
           if (isContract(controller)) {
               require(TokenController(controller).onTransfer(_from, _to, _amount));
           }
           updateValueAtNow(balances[_from], previousBalanceFrom - _amount);
           var previousBalanceTo = balanceOfAt(_to, block.number);
           require(previousBalanceTo + _amount >= previousBalanceTo); 
           updateValueAtNow(balances[_to], previousBalanceTo + _amount);
           Transfer(_from, _to, _amount);
           return true;
    }
    function balanceOf(address _owner) public constant returns (uint256 balance) {
        return balanceOfAt(_owner, block.number);
    }
    function approve(address _spender, uint256 _amount) public returns (bool success) {
        require(transfersEnabled);
        require((_amount == 0) || (allowed[msg.sender][_spender] == 0));
        if (isContract(controller)) {
            require(TokenController(controller).onApprove(msg.sender, _spender, _amount));
        }
        allowed[msg.sender][_spender] = _amount;
        Approval(msg.sender, _spender, _amount);
        return true;
    }
    function allowance(address _owner, address _spender
    ) public constant returns (uint256 remaining) {
        return allowed[_owner][_spender];
    }
    function approveAndCall(address _spender, uint256 _amount, bytes _extraData
    ) public returns (bool success) {
        require(approve(_spender, _amount));
        ApproveAndCallFallBack(_spender).receiveApproval(
            msg.sender,
            _amount,
            this,
            _extraData
        );
        return true;
    }
    function totalSupply() public constant returns (uint) {
        return totalSupplyAt(block.number);
    }
    function balanceOfAt(address _owner, uint _blockNumber) public constant
        returns (uint) {
        if ((balances[_owner].length == 0)
            || (balances[_owner][0].fromBlock > _blockNumber)) {
            if (address(parentToken) != 0) {
                return parentToken.balanceOfAt(_owner, min(_blockNumber, parentSnapShotBlock));
            } else {
                return 0;
            }
        } else {
            return getValueAt(balances[_owner], _blockNumber);
        }
    }
    function totalSupplyAt(uint _blockNumber) public constant returns(uint) {
        if ((totalSupplyHistory.length == 0)
            || (totalSupplyHistory[0].fromBlock > _blockNumber)) {
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
        ) public returns(address) {
        if (_snapshotBlock == 0) _snapshotBlock = block.number;
        MiniMeToken cloneToken = tokenFactory.createCloneToken(
            this,
            _snapshotBlock,
            _cloneTokenName,
            _cloneDecimalUnits,
            _cloneTokenSymbol,
            _transfersEnabled
            );
        cloneToken.changeController(msg.sender);
        NewCloneToken(address(cloneToken), _snapshotBlock);
        return address(cloneToken);
    }
    function generateTokens(address _owner, uint _amount
    ) public onlyController returns (bool) {
        uint curTotalSupply = totalSupply();
        require(curTotalSupply + _amount >= curTotalSupply); 
        uint previousBalanceTo = balanceOf(_owner);
        require(previousBalanceTo + _amount >= previousBalanceTo); 
        updateValueAtNow(totalSupplyHistory, curTotalSupply + _amount);
        updateValueAtNow(balances[_owner], previousBalanceTo + _amount);
        Transfer(0, _owner, _amount);
        return true;
    }
    function destroyTokens(address _owner, uint _amount
    ) onlyController public returns (bool) {
        uint curTotalSupply = totalSupply();
        require(curTotalSupply >= _amount);
        uint previousBalanceFrom = balanceOf(_owner);
        require(previousBalanceFrom >= _amount);
        updateValueAtNow(totalSupplyHistory, curTotalSupply - _amount);
        updateValueAtNow(balances[_owner], previousBalanceFrom - _amount);
        Transfer(_owner, 0, _amount);
        return true;
    }
    function enableTransfers(bool _transfersEnabled) public onlyController {
        transfersEnabled = _transfersEnabled;
    }
    function getValueAt(Checkpoint[] storage checkpoints, uint _block
    ) constant internal returns (uint) {
        if (checkpoints.length == 0) return 0;
        if (_block >= checkpoints[checkpoints.length-1].fromBlock)
            return checkpoints[checkpoints.length-1].value;
        if (_block < checkpoints[0].fromBlock) return 0;
        uint min = 0;
        uint max = checkpoints.length-1;
        while (max > min) {
            uint mid = (max + min + 1)/ 2;
            if (checkpoints[mid].fromBlock<=_block) {
                min = mid;
            } else {
                max = mid-1;
            }
        }
        return checkpoints[min].value;
    }
    function updateValueAtNow(Checkpoint[] storage checkpoints, uint _value
    ) internal  {
        if ((checkpoints.length == 0)
        || (checkpoints[checkpoints.length -1].fromBlock < block.number)) {
               Checkpoint storage newCheckPoint = checkpoints[ checkpoints.length++ ];
               newCheckPoint.fromBlock =  uint128(block.number);
               newCheckPoint.value = uint128(_value);
           } else {
               Checkpoint storage oldCheckPoint = checkpoints[checkpoints.length-1];
               oldCheckPoint.value = uint128(_value);
           }
    }
    function isContract(address _addr) constant internal returns(bool) {
        uint size;
        if (_addr == 0) return false;
        assembly {
            size := extcodesize(_addr)
        }
        return size>0;
    }
    function min(uint a, uint b) pure internal returns (uint) {
        return a < b ? a : b;
    }
    function () public payable {
        require(isContract(controller));
        require(TokenController(controller).proxyPayment.value(msg.value)(msg.sender));
    }
    function claimTokens(address _token) public onlyController {
        if (_token == 0x0) {
            controller.transfer(this.balance);
            return;
        }
        MiniMeToken token = MiniMeToken(_token);
        uint balance = token.balanceOf(this);
        token.transfer(controller, balance);
        ClaimedTokens(_token, controller, balance);
    }
    event ClaimedTokens(address indexed _token, address indexed _controller, uint _amount);
    event Transfer(address indexed _from, address indexed _to, uint256 _amount);
    event NewCloneToken(address indexed _cloneToken, uint _snapshotBlock);
    event Approval(
        address indexed _owner,
        address indexed _spender,
        uint256 _amount
        );
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
contract LPPDacs is Escapable, TokenController {
    uint constant FROM_FIRST_DELEGATE = 1;
    uint constant TO_FIRST_DELEGATE = 257;
    LiquidPledging public liquidPledging;
    struct Dac {
        MiniMeToken token;
        address owner;
    }
    mapping (uint64 => Dac) dacs;
    event GenerateTokens(uint64 indexed idDelegate, address addr, uint amount);
    event DestroyTokens(uint64 indexed idDelegate, address addr, uint amount);
    function LPPDacs(
        LiquidPledging _liquidPledging,
        address _escapeHatchCaller,
        address _escapeHatchDestination
    ) Escapable(_escapeHatchCaller, _escapeHatchDestination) public
    {
        liquidPledging = _liquidPledging;
    }
    function beforeTransfer(
        uint64 pledgeManager,
        uint64 pledgeFrom,
        uint64 pledgeTo,
        uint64 context,
        uint amount
    ) external returns (uint maxAllowed)
    {
        require(msg.sender == address(liquidPledging));
        return amount;
    }
    function afterTransfer(
        uint64 pledgeManager,
        uint64 pledgeFrom,
        uint64 pledgeTo,
        uint64 context,
        uint amount
    ) external
    {
        require(msg.sender == address(liquidPledging));
        var (, toOwner, , toIntendedProject, , , toPledgeState ) = liquidPledging.getPledge(pledgeTo);
        var (, fromOwner, , , , , ) = liquidPledging.getPledge(pledgeFrom);
        var (toAdminType, toAddr, , , , , , ) = liquidPledging.getPledgeAdmin(toOwner);
        Dac storage d;
        uint64 idDelegate;
        if (context == FROM_FIRST_DELEGATE &&
                toIntendedProject == 0 &&
                toAdminType == LiquidPledgingBase.PledgeAdminType.Project &&
                toOwner != fromOwner &&
                toPledgeState == LiquidPledgingBase.PledgeState.Pledged)
        {
            (idDelegate, , ) = liquidPledging.getPledgeDelegate(pledgeFrom, 1);
            d = dacs[idDelegate];
            require(address(d.token) != 0x0);
            var (, fromAddr , , , , , , ) = liquidPledging.getPledgeAdmin(fromOwner);
            d.token.generateTokens(fromAddr, amount);
            GenerateTokens(idDelegate, fromAddr, amount);
        }
        if ( (context == TO_FIRST_DELEGATE) &&
            liquidPledging.isProjectCanceled(fromOwner)) {
            (idDelegate, , ) = liquidPledging.getPledgeDelegate(pledgeTo, 1);
            d = dacs[idDelegate];
            require(address(d.token) != 0x0);
            if (d.token.balanceOf(toAddr) >= amount) {
                d.token.destroyTokens(toAddr, amount);
                DestroyTokens(fromOwner, toAddr, amount);
            }
        }
    }
    function addDac(
        string name,
        string url,
        uint64 commitTime,
        string tokenName,
        string tokenSymbol
    ) public
    {
        uint64 idDelegate = liquidPledging.addDelegate(
            name,
            url,
            commitTime,
            ILiquidPledgingPlugin(this)
        );
        MiniMeTokenFactory tokenFactory = new MiniMeTokenFactory();
        MiniMeToken token = new MiniMeToken(tokenFactory, 0x0, 0, tokenName, 18, tokenSymbol, false);
        dacs[idDelegate] = Dac(token, msg.sender);
    }
    function addDac(
        string name,
        string url,
        uint64 commitTime,
        MiniMeToken token
    ) public
    {
        uint64 idDelegate = liquidPledging.addDelegate(
          name,
          url,
          commitTime,
          ILiquidPledgingPlugin(this)
        );
        dacs[idDelegate] = Dac(token, msg.sender);
    }
    function transfer(
        uint64 idDelegate,
        uint64 idPledge,
        uint amount,
        uint64 idReceiver
    ) public
    {
        Dac storage d = dacs[idDelegate];
        require(msg.sender == d.owner);
        liquidPledging.transfer(
            idDelegate,
            idPledge,
            amount,
            idReceiver
        );
    }
    function getDac(uint64 idDelegate) public view returns (
        MiniMeToken token,
        address owner
    )
    {
        Dac storage d = dacs[idDelegate];
        token = d.token;
        owner = d.owner;
    }
    function proxyPayment(address _owner) public payable returns(bool) {
        return false;
    }
    function onTransfer(address _from, address _to, uint _amount) public returns(bool) {
        return false;
    }
    function onApprove(address _owner, address _spender, uint _amount) public returns(bool) {
        return false;
    }
}

```

## RQ1_852d7abd1772

SHA-256 `a45a0501d915f22521e6abaa32ec861132ec659db1f1a20c372acbc7f26bfe5c`

```solidity
pragma solidity 0.4.25;
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

## RQ1_cb75c28366fa

SHA-256 `4f0eeaf13923691da04e4c7da4334f46b53735798040a3ea3c0f504551295109`

```solidity
pragma solidity ^0.4.23;
contract Ownable {
    address public owner;
    address public cfoAddress;
    constructor() public{
        owner = msg.sender;
        cfoAddress = msg.sender;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    modifier onlyCFO() {
        require(msg.sender == cfoAddress);
        _;
    }
    function transferOwnership(address newOwner) external onlyOwner {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function setCFO(address newCFO) external onlyOwner {
        require(newCFO != address(0));
        cfoAddress = newCFO;
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
contract MixGenInterface {
    function openEgg(uint64 userNumber, uint16 eggQuality) public returns (uint256 genes, uint16 quality);
    function uniquePet(uint64 newPetId) public returns (uint256 genes, uint16 quality);
}
contract ExternalContracts is Ownable {
    MixGenInterface public geneScience;
    address public marketAddress;
    function setMixGenAddress(address _address) external onlyOwner {
        MixGenInterface candidateContract = MixGenInterface(_address);
        geneScience = candidateContract;
    }
    function setMarketAddress(address _address) external onlyOwner {
        marketAddress = _address;
    }
}
contract PopulationControl is Pausable {
    uint32 public breedTimeout = 12 hours;
    uint32 maxTimeout = 178 days;
    function setBreedTimeout(uint32 timeout) external onlyOwner {
        require(timeout <= maxTimeout);
        breedTimeout = timeout;
    }
}
contract PetBase is PopulationControl{
    event Birth(address owner, uint64 petId, uint16 quality, uint256 genes);
    event Death(uint64 petId);
    event Transfer(address from, address to, uint256 tokenId);
    struct Pet {
        uint256 genes;
        uint64 birthTime;
        uint16 quality;
    }
    mapping (uint64 => Pet) pets;
    mapping (uint64 => address) petIndexToOwner;
    mapping (address => uint256) public ownershipTokenCount;
    mapping (uint64 => uint64) breedTimeouts;
    uint64 tokensCount;
    uint64 lastTokenId;
    function createPet(
        uint256 _genes,
        uint16 _quality,
        address _owner
    )
        internal
        returns (uint64)
    {
        Pet memory _pet = Pet({
            genes: _genes,
            birthTime: uint64(now),
            quality: _quality
        });
        lastTokenId++;
        tokensCount++;
        uint64 newPetId = lastTokenId;
        pets[newPetId] = _pet;
        _transfer(0, _owner, newPetId);
        breedTimeouts[newPetId] = uint64( now + (breedTimeout / 2) );
        emit Birth(_owner, newPetId, _quality, _genes);
        return newPetId;
    }
    function _transfer(address _from, address _to, uint256 _tokenId) internal {
        uint64 _tokenId64bit = uint64(_tokenId);
        ownershipTokenCount[_to]++;
        petIndexToOwner[_tokenId64bit] = _to;
        if (_from != address(0)) {
            ownershipTokenCount[_from]--;
        }
         emit Transfer(_from, _to, _tokenId);
    }
    function recommendedPrice(uint16 quality) public pure returns(uint256 price) {
        require(quality <= uint16(0xF000));
        require(quality >= uint16(0x1000));
        uint256 startPrice = 1000;
        price = startPrice;
        uint256 revertQuality = uint16(0xF000) - quality;
        uint256 oneLevel = uint16(0x2000);
        uint256 oneQuart = oneLevel/4;
        uint256 fullLevels = revertQuality/oneLevel;
        uint256 fullQuarts =  (revertQuality % oneLevel) / oneQuart ;
        uint256 surplus = revertQuality - (fullLevels*oneLevel) - (fullQuarts*oneQuart);
        price = price * 44**fullLevels;
        price = price / 10**fullLevels;
        if(fullQuarts != 0)
        {
            price = price * 14483154**fullQuarts;
            price = price / 10**(7 * fullQuarts);
        }
        if(surplus != 0)
        {
            uint256 nextQuartPrice = (price * 14483154) / 10**7;
            uint256 surPlusCoefficient = surplus * 10**6  /oneQuart;
            uint256 surPlusPrice = ((nextQuartPrice - price) * surPlusCoefficient) / 10**6;
            price+= surPlusPrice;
        }
        price*= 50 szabo;
    }
    function getGradeByQuailty(uint16 quality) public pure returns (uint8 grade) {
        require(quality <= uint16(0xF000));
        require(quality >= uint16(0x1000));
        if(quality == uint16(0xF000))
            return 7;
        quality+= uint16(0x1000);
        return uint8 ( quality / uint16(0x2000) );
    }
}
contract PetOwnership is PetBase {
    function transfer(
        address _to,
        uint256 _tokenId
    )
        external
        whenNotPaused
    {
        require(_to != address(0));
        require(_to != address(this));
        require(_owns(msg.sender, uint64(_tokenId)));
        _transfer(msg.sender, _to, _tokenId);
    }
    function _owns(address _claimant, uint64 _tokenId) internal view returns (bool) {
        return petIndexToOwner[_tokenId] == _claimant;
    }
    function ownerOf(uint256 _tokenId) external view returns (address owner) {
        uint64 _tokenId64bit = uint64(_tokenId);
        owner = petIndexToOwner[_tokenId64bit];
        require(owner != address(0));
    }   
}
contract EggMinting is PetOwnership{
    uint8 public uniquePetsCount = 100;
    uint16 public globalPresaleLimit = 2500;
    mapping (uint16 => uint16) public eggLimits;
    mapping (uint16 => uint16) public purchesedEggs;
    constructor() public {
        eggLimits[55375] = 200;
        eggLimits[48770] = 1100;
        eggLimits[39904] = 200;
        eggLimits[32223] = 25;
    }
    function totalSupply() public view returns (uint) {
        return tokensCount;
    }
    function setEggLimit(uint16 quality, uint16 limit) external onlyOwner {
        eggLimits[quality] = limit;
    }
    function eggAvailable(uint16 quality) constant public returns(bool) {
        if( quality < 48000 && tokensCount < ( 100 + uniquePetsCount ) )
           return false;
        return (eggLimits[quality] > purchesedEggs[quality]);
    }
}
contract EggPurchase is EggMinting, ExternalContracts {
    uint16[4] discountThresholds =    [20, 100, 500, 1000];
    uint8[4]  discountPercents   =    [75, 50,  30,  20  ];
    function purchaseEgg(uint64 userNumber, uint16 quality) external payable whenNotPaused {
        require(tokensCount >= uniquePetsCount);
        require(eggAvailable(quality));
        require(tokensCount <= globalPresaleLimit);
        uint256 eggPrice = ( recommendedPrice(quality) * (100 - getCurrentDiscountPercent()) ) / 100;
        require(msg.value >= eggPrice);
        purchesedEggs[quality]++;
        uint256 childGenes;
        uint16 childQuality;
        (childGenes, childQuality) = geneScience.openEgg(userNumber, quality);
        createPet(
            childGenes,      
            childQuality,    
            msg.sender       
        );
    }
    function getCurrentDiscountPercent() constant public returns (uint8 discount) {
        for(uint8 i = 0; i <= 3; i++)
        {
            if(tokensCount < (discountThresholds[i] + uniquePetsCount ))
                return discountPercents[i];
        }
        return 10;
    }
}
contract PreSale is EggPurchase {
    constructor() public {
        paused = true;
    }
    function generateUniquePets(uint8 count) external onlyOwner whenNotPaused {
        require(marketAddress != address(0));
        require(address(geneScience) != address(0));
        uint256 childGenes;
        uint16 childQuality;
        uint64 newPetId;
        for(uint8 i = 0; i< count; i++)
        {
            if(tokensCount >= uniquePetsCount)
                continue;
            newPetId = tokensCount+1;
            (childGenes, childQuality) = geneScience.uniquePet(newPetId);
            createPet(childGenes, childQuality, marketAddress);
        }
    }
    function getPet(uint256 _id) external view returns (
        uint64 birthTime,
        uint256 genes,
        uint64 breedTimeout,
        uint16 quality,
        address owner
    ) {
        uint64 _tokenId64bit = uint64(_id);
        Pet storage pet = pets[_tokenId64bit];
        birthTime = pet.birthTime;
        genes = pet.genes;
        breedTimeout = uint64(breedTimeouts[_tokenId64bit]);
        quality = pet.quality;
        owner = petIndexToOwner[_tokenId64bit];
    }
    function unpause() public onlyOwner whenPaused {
        require(address(geneScience) != address(0));
        super.unpause();
    }
    function withdrawBalance(uint256 summ) external onlyCFO {
        cfoAddress.transfer(summ);
    }
}
```

## RQ1_53378370361e

SHA-256 `8876575205e3c17bbe44a622c8f27b019cdd8a40ff0a1b99deafaa795a54912c`

```solidity
pragma solidity ^0.4.15;
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
contract SteakToken is Ownable {
  using SafeMath for uint256;
  string public name = "Steak Token";
  string public symbol = "BOV";
  uint public decimals = 18;
  uint public totalSupply;      
  mapping(address => uint256) balances;
  mapping (address => mapping (address => uint256)) allowed;
  event Transfer(address indexed from, address indexed to, uint256 value);
  event Approval(address indexed ownerAddress, address indexed spenderAddress, uint256 value);
  event Mint(address indexed to, uint256 amount);
  event MineFinished();
  function balanceOf(address _owner) constant returns (uint256 balance) {
    return balances[_owner];
  }
  function transfer(address _to, uint256 _value) returns (bool) {
    if(msg.data.length < (2 * 32) + 4) { revert(); } 
    balances[msg.sender] = balances[msg.sender].sub(_value);
    balances[_to] = balances[_to].add(_value);
    Transfer(msg.sender, _to, _value);
    return true;
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
   function mint(address _to, uint256 _amount) internal returns (bool) {
    totalSupply = totalSupply.add(_amount);
    balances[_to] = balances[_to].add(_amount);
    Mint(_to, _amount);
    return true;
  }
}
 contract AuctionCrowdsale is SteakToken {
  using SafeMath for uint;
  uint public initialSale;                  
  bool public saleStarted;
  bool public saleEnded;
  uint public absoluteEndBlock;             
  uint256 public weiRaised;                 
  address[] public investors;               
  uint public numberOfInvestors;
  mapping(address => uint256) public investments; 
  mapping(address => bool) public claimed;      
  bool public bovBatchDistributed;              
  uint public initialPrizeWeiValue;             
  uint public initialPrizeBov;                  
  uint public dailyHashExpires;        
   event TokenInvestment(address indexed purchaser, address indexed beneficiary, uint256 value);
   function () payable {
    invest(msg.sender);
  }
  function invest(address beneficiary) payable {
    require(beneficiary != 0x0);
    require(validInvestment());
    uint256 weiAmount = msg.value;
    uint investedAmount = investments[beneficiary];
    forwardFunds();
    if (investedAmount > 0) { 
      investments[beneficiary] = investedAmount + weiAmount; 
    } else { 
      investors.push(beneficiary);
      numberOfInvestors += 1;
      investments[beneficiary] = weiAmount;
    }
    weiRaised = weiRaised.add(weiAmount);
    TokenInvestment(msg.sender, beneficiary, weiAmount);
  }
  function validInvestment() internal constant returns (bool) {
    bool withinPeriod = saleStarted && !saleEnded;
    bool nonZeroPurchase = (msg.value > 0);
    return withinPeriod && nonZeroPurchase;
  }
  function distributeAllTokens() public {
    require(!bovBatchDistributed);
    require(crowdsaleHasEnded());
    for (uint i=0; i < numberOfInvestors; i++) {
      address investorAddr = investors[i];
      if (!claimed[investorAddr]) { 
        claimed[investorAddr] = true;
        uint amountInvested = investments[investorAddr];
        uint bovEarned = amountInvested.mul(initialSale).div(weiRaised);
        mint(investorAddr, bovEarned);
      }
    }
    bovBatchDistributed = true;
  }
  function claimTokens(address origAddress) public {
    require(crowdsaleHasEnded());
    require(claimed[origAddress] == false);
    uint amountInvested = investments[origAddress];
    uint bovEarned = amountInvested.mul(initialSale).div(weiRaised);
    claimed[origAddress] = true;
    mint(origAddress, bovEarned);
  }
  function getCurrentShare(address addr) public constant returns (uint) {
    require(!bovBatchDistributed && !claimed[addr]); 
    uint amountInvested = investments[addr];
    uint currentBovShare = amountInvested.mul(initialSale).div(weiRaised);
    return currentBovShare;
  }
  function forwardFunds() internal {
    owner.transfer(msg.value);
  }
  function startCrowdsale() onlyOwner {
    require(!saleStarted && !saleEnded);
    saleStarted = true;
  }
  function endCrowdsale() onlyOwner {
    require(saleStarted && !saleEnded);
    dailyHashExpires = now; 
    saleEnded = true;
    setInitialPrize();
  }
  function endCrowdsalePublic() public {
    require(block.number > absoluteEndBlock);
    require(saleStarted && !saleEnded);
    dailyHashExpires = now;
    saleEnded = true;
    setInitialPrize();
  }
  function setInitialPrize() internal returns (uint) {
    require(crowdsaleHasEnded());
    require(initialPrizeBov == 0); 
    uint tokenUnitsPerWei = initialSale.div(weiRaised);
    initialPrizeBov = tokenUnitsPerWei.mul(initialPrizeWeiValue);
    return initialPrizeBov;
  }
  function crowdsaleHasEnded() public constant returns (bool) {
    return saleStarted && saleEnded;
  }
  function getInvestors() public returns (address[]) {
    return investors;
  }
}
contract Steak is AuctionCrowdsale {
  bytes32 public dailyHash;            
  Submission[] public submissions;          
  uint public numSubmissions;
  Submission[] public approvedSubmissions;
  mapping (address => uint) public memberId;    
  Member[] public members;                      
  uint public halvingInterval;                  
  uint public numberOfHalvings;                 
  uint public lastMiningBlock;                  
  bool public ownerCredited;    
  event PicAdded(address msgSender, uint submissionID, address recipient, bytes32 propUrl); 
  event Judged(uint submissionID, bool position, address voter, bytes32 justification);
  event MembershipChanged(address member, bool isMember);
  struct Submission {
    address recipient;    
    bytes32 url;           
    bool judged;          
    bool submissionApproved;
    address judgedBy;     
    bytes32 adminComments; 
    bytes32 todaysHash;   
    uint awarded;         
  }
  struct Member {
    address member;
    bytes32 name;
    uint memberSince;
  }
  modifier onlyMembers {
    require(memberId[msg.sender] != 0); 
    _;
  }
  function Steak() {
    owner = msg.sender;
    initialSale = 10000000 * 1000000000000000000; 
    uint blocksPerHour = 212;
    uint maxCrowdsaleLifeFromLaunchDays = 40; 
    absoluteEndBlock = block.number + (blocksPerHour * 24 * maxCrowdsaleLifeFromLaunchDays);
    uint miningDays = 365; 
    lastMiningBlock = block.number + (blocksPerHour * 24 * miningDays);
    dailyHashExpires = now;
    halvingInterval = 500;    
    numberOfHalvings = 8;      
    initialPrizeWeiValue = (357 finney / 10); 
  }
  function initMembers() onlyOwner {
    addMember(0, '');                        
    addMember(msg.sender, 'Madame BOV');
  }
  function creditOwner() onlyOwner {
    require(!ownerCredited);
    uint ownerAward = initialSale / 10;  
    ownerCredited = true;   
    mint(owner, ownerAward);
  }
  function addMember(address targetMember, bytes32 memberName) onlyOwner {
    uint id;
    if (memberId[targetMember] == 0) {
      memberId[targetMember] = members.length;
      id = members.length++;
      members[id] = Member({member: targetMember, memberSince: now, name: memberName});
    } else {
      id = memberId[targetMember];
    }
    MembershipChanged(targetMember, true);
  }
  function removeMember(address targetMember) onlyOwner {
    if (memberId[targetMember] == 0) revert();
    memberId[targetMember] = 0;
    for (uint i = memberId[targetMember]; i<members.length-1; i++){
      members[i] = members[i+1];
    }
    delete members[members.length-1];
    members.length--;
  }
  function submitSteak(address addressToAward, bytes32 steakPicUrl)  returns (uint submissionID) {
    require(crowdsaleHasEnded());
    require(block.number <= lastMiningBlock); 
    submissionID = submissions.length++; 
    Submission storage s = submissions[submissionID];
    s.recipient = addressToAward;
    s.url = steakPicUrl;
    s.judged = false;
    s.submissionApproved = false;
    s.todaysHash = getDailyHash(); 
    PicAdded(msg.sender, submissionID, addressToAward, steakPicUrl);
    numSubmissions = submissionID+1;
    return submissionID;
  }
  function getSubmission(uint submissionID) public constant returns (address recipient, bytes32 url, bool judged, bool submissionApproved, address judgedBy, bytes32 adminComments, bytes32 todaysHash, uint awarded) {
    Submission storage s = submissions[submissionID];
    recipient = s.recipient;
    url = s.url;                 
    judged = s.judged;           
    submissionApproved = s.submissionApproved;  
    judgedBy = s.judgedBy;           
    adminComments = s.adminComments; 
    todaysHash = s.todaysHash;       
    awarded = s.awarded;         
  }
  function judge(uint submissionNumber, bool supportsSubmission, bytes32 justificationText) onlyMembers {
    Submission storage s = submissions[submissionNumber];         
    require(!s.judged);                                     
    s.judged = true;
    s.judgedBy = msg.sender;
    s.submissionApproved = supportsSubmission;
    s.adminComments = justificationText;    
    if (supportsSubmission) { 
      uint prizeAmount = getSteakPrize(); 
      s.awarded = prizeAmount;            
      mint(s.recipient, prizeAmount);     
      uint adminAward = prizeAmount.div(3);
      mint(msg.sender, adminAward);
      approvedSubmissions.push(s);
    }
    Judged(submissionNumber, supportsSubmission, msg.sender, justificationText);
  }
  function getSteakPrize() public constant returns (uint) {
    require(initialPrizeBov > 0); 
    uint halvings = numberOfApprovedSteaks().div(halvingInterval);
    if (halvings > numberOfHalvings) {  
      return 0;
    }
    uint prize = initialPrizeBov;
    prize = prize >> halvings; 
    return prize;
  }
  function numberOfApprovedSteaks() public constant returns (uint) {
    return approvedSubmissions.length;
  }
  function getDailyHash() public returns (bytes32) {
    if (dailyHashExpires > now) { 
      return dailyHash;
    } else { 
      bytes32 newHash = block.blockhash(block.number-1);
      dailyHash = newHash;
      uint nextExpiration = dailyHashExpires + 24 hours; 
      while (nextExpiration < now) { 
        nextExpiration += 24 hours;
      }
      dailyHashExpires = nextExpiration;
      return newHash;
    }
  }
  function minutesToPost() public constant returns (uint) {
    if (dailyHashExpires > now) {
      return (dailyHashExpires - now) / 60; 
    } else {
      return 0;
    }
  }
  function currentBlock() public constant returns (uint) {
    return block.number;
  }
}
```

## RQ1_032cdc396341

SHA-256 `471c9dcee830b99d134b63ca2a2e102778994d497205394ae89b6e2d424fa5af`

```solidity
pragma solidity ^0.4.19;
contract ERC20 {
    function totalSupply() public constant returns (uint);
    function balanceOf(address tokenOwner) public constant returns (uint balance);
    function allowance(address tokenOwner, address spender) public constant returns (uint remaining);
    function transfer(address to, uint tokens) public returns (bool success);
    function approve(address spender, uint tokens) public returns (bool success);
    function transferFrom(address from, address to, uint tokens) public returns (bool success);
    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);
    string public constant name = "Token Name";
    string public constant symbol = "SYM";
    uint8 public constant decimals = 18;  
}
contract MarketboardERC20Listing {
    function _version() pure public returns(uint32) {
        return 2;
    }
    event MarketboardListingComplete(address indexed tokenContract, uint256 numTokensSold, uint256 totalEtherPrice, uint256 fee);
    event MarketboardListingBuyback(address indexed tokenContract, uint256 numTokens);
	event MarketboardListingDestroyed();
    event MarketboardListingPriceChanged(uint256 oldPricePerToken, uint256 newPricePerToken);
    modifier moderatorOnly {
        require(msg.sender == moderator);
        _;
    }
    modifier moderatorOrSellerOnly {
        require(moderator == msg.sender || seller == msg.sender);
        _;
    }
	uint256 public tokenPrice = 0;
    address public tokenContract;
    address moderator;
    address seller;
    uint256 public feeFixed;
    uint32 public feePercentage;
	uint32 constant public feePercentageMax = 100000;
    function MarketboardERC20Listing(address _moderator, uint256 _feeFixed, uint32 _feePercentage, address _erc20Token, uint256 _tokenPrice) public {
        seller = msg.sender;
        moderator = _moderator;
        feeFixed = _feeFixed;
        feePercentage = _feePercentage;
        tokenContract = _erc20Token;
        tokenPrice = _tokenPrice;
    }
    function tokenCount() public view returns(uint256) {
        ERC20 erc = ERC20(tokenContract);
        return erc.balanceOf(this);
    }
    function tokenBase() public view returns(uint256) {
        ERC20 erc = ERC20(tokenContract);
        uint256 decimals = erc.decimals();
        return 10 ** decimals;
    }
    function totalPrice() public view returns(uint256) {
        return tokenPrice * tokenCount() / tokenBase() + fee();
    }
    function fee() public view returns(uint256) {
        uint256 price = tokenPrice * tokenCount() / tokenBase();
        return price * feePercentage / feePercentageMax + feeFixed;
    }
    function setPrice(uint256 newTokenPrice) moderatorOrSellerOnly public {
        uint256 oldPrice = tokenPrice;
        tokenPrice = newTokenPrice;
        MarketboardListingPriceChanged(oldPrice, newTokenPrice);
    }
    function buyback(address recipient) moderatorOrSellerOnly public {
        ERC20 erc = ERC20(tokenContract);
		uint256 balance = erc.balanceOf(this);
        erc.transfer(recipient, balance);
        MarketboardListingBuyback(tokenContract, balance);
        reset();
    }
    function purchase(address recipient) public payable {
        require(msg.value >= totalPrice());
        ERC20 erc = ERC20(tokenContract);
		uint256 balance = erc.balanceOf(this);
        erc.transfer(recipient, balance);
		uint256 basePrice = tokenPrice * balance;
		require(basePrice > 0);
		require(basePrice < this.balance);
		seller.transfer(basePrice);
        MarketboardListingComplete(tokenContract, balance, 0, 0);
        reset();
    }
    function claimUnrelatedTokens(address unrelatedTokenContract, address recipient) moderatorOrSellerOnly public {
        require(tokenContract != unrelatedTokenContract);
        ERC20 erc = ERC20(unrelatedTokenContract);
        uint256 balance = erc.balanceOf(this);
        erc.transfer(recipient, balance);
    }
	function reset() internal {
        MarketboardListingDestroyed();
		selfdestruct(moderator);
	}
}
```

## RQ1_3092779b88eb

SHA-256 `8a0f199dff014a50dd24e961fce4e8bf50d5660a32861d3095fdca5498125f50`

```solidity
pragma solidity ^0.4.19;
contract CaviarToken {
    string public name = "Caviar Token";
    string public symbol = "CAV";
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
    function CaviarToken() public {
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

## RQ1_2ca53b535ccd

SHA-256 `d9b07ff9965d4cbd6569b4c68b7fbc034970d7d2b2e14fe7cde7c95a55ecb5c3`

```solidity
pragma solidity ^0.5.2;
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
contract AvatarNameRegistry is Ownable, AvatarNameStorage {
    function initialize(
        ERC20Interface _mana,
        address _owner
    )
    public initializer
    {
        manaToken = _mana;
        price = 100000000000000000000; 
        allowed[_owner] = true;
        Ownable.initialize(_owner);
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
        manaToken.transferFrom(_beneficiary, address(this), price);
        manaToken.burn(price);
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

## RQ1_ca65e2d77908

SHA-256 `ee836c64321b53dd7fe78fa79fea12558dac37d4cb477bc553117e56ebb0e1aa`

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
contract LGM is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "Legumes";
    string public constant symbol = "LGM";
    uint public constant decimals = 18;
    uint256 public totalSupply = 3000000000e18;
    uint256 public totalDistributed = 100000000e18;
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

## RQ1_5e33b7b64e99

SHA-256 `12f83f4db7db36e2c2a6f6c9ae2a6196c7ed13d638855668592b340350871e5a`

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
contract KingOfEthAuctionsAbstractInterface {
    function existingAuction(uint _x, uint _y) public view returns(bool);
}
pragma solidity ^0.4.24;
contract KingOfEthBlindAuctionsReferencer is GodMode {
    address public blindAuctionsContract;
    modifier onlyBlindAuctionsContract()
    {
        require(blindAuctionsContract == msg.sender);
        _;
    }
    function godSetBlindAuctionsContract(address _blindAuctionsContract)
        public
        onlyGod
    {
        blindAuctionsContract = _blindAuctionsContract;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthOpenAuctionsReferencer is GodMode {
    address public openAuctionsContract;
    modifier onlyOpenAuctionsContract()
    {
        require(openAuctionsContract == msg.sender);
        _;
    }
    function godSetOpenAuctionsContract(address _openAuctionsContract)
        public
        onlyGod
    {
        openAuctionsContract = _openAuctionsContract;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthAuctionsReferencer is
      KingOfEthBlindAuctionsReferencer
    , KingOfEthOpenAuctionsReferencer
{
    modifier onlyAuctionsContract()
    {
        require(blindAuctionsContract == msg.sender
             || openAuctionsContract == msg.sender);
        _;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthAbstractInterface {
    address public king;
    address public wayfarer;
    function payTaxes() public payable;
}
pragma solidity ^0.4.24;
contract KingOfEthReferencer is GodMode {
    address public kingOfEthContract;
    modifier onlyKingOfEthContract()
    {
        require(kingOfEthContract == msg.sender);
        _;
    }
    function godSetKingOfEthContract(address _kingOfEthContract)
        public
        onlyGod
    {
        kingOfEthContract = _kingOfEthContract;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthBoard is
      GodMode
    , KingOfEthAuctionsReferencer
    , KingOfEthReferencer
{
    uint public boundX1 = 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffef;
    uint public boundY1 = 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffef;
    uint public boundX2 = 0x800000000000000000000000000000000000000000000000000000000000000f;
    uint public boundY2 = 0x800000000000000000000000000000000000000000000000000000000000000f;
    uint public constant auctionsAvailableDivisor = 10;
    uint public constant kingTimeBetweenIncrease = 2 weeks;
    uint public constant wayfarerTimeBetweenIncrease = 3 weeks;
    uint public constant plebTimeBetweenIncrease = 4 weeks;
    uint public lastIncreaseTime;
    uint8 public nextIncreaseDirection;
    uint public auctionsRemaining;
    constructor() public
    {
        isPaused = true;
        setAuctionsAvailableForBounds();
    }
    event BoardSizeIncreased(
          address initiator
        , uint newBoundX1
        , uint newBoundY1
        , uint newBoundX2
        , uint newBoundY2
        , uint lastIncreaseTime
        , uint nextIncreaseDirection
        , uint auctionsRemaining
    );
    modifier onlyKing()
    {
        require(KingOfEthAbstractInterface(kingOfEthContract).king() == msg.sender);
        _;
    }
    modifier onlyWayfarer()
    {
        require(KingOfEthAbstractInterface(kingOfEthContract).wayfarer() == msg.sender);
        _;
    }
    function setAuctionsAvailableForBounds() private
    {
        uint boundDiffX = boundX2 - boundX1;
        uint boundDiffY = boundY2 - boundY1;
        auctionsRemaining = boundDiffX * boundDiffY / 2 / auctionsAvailableDivisor;
    }
    function increaseBoard() private
    {
        uint _increaseLength;
        if(0 == nextIncreaseDirection)
        {
            _increaseLength = boundX2 - boundX1;
            uint _updatedX2 = boundX2 + _increaseLength;
            if(_updatedX2 <= boundX2 || _updatedX2 <= _increaseLength)
            {
                boundX2 = ~uint(0);
            }
            else
            {
                boundX2 = _updatedX2;
            }
        }
        else if(1 == nextIncreaseDirection)
        {
            _increaseLength = boundY2 - boundY1;
            uint _updatedY2 = boundY2 + _increaseLength;
            if(_updatedY2 <= boundY2 || _updatedY2 <= _increaseLength)
            {
                boundY2 = ~uint(0);
            }
            else
            {
                boundY2 = _updatedY2;
            }
        }
        else if(2 == nextIncreaseDirection)
        {
            _increaseLength = boundX2 - boundX1;
            if(boundX1 <= _increaseLength)
            {
                boundX1 = 0;
            }
            else
            {
                boundX1 -= _increaseLength;
            }
        }
        else if(3 == nextIncreaseDirection)
        {
            _increaseLength = boundY2 - boundY1;
            if(boundY1 <= _increaseLength)
            {
                boundY1 = 0;
            }
            else
            {
                boundY1 -= _increaseLength;
            }
        }
        lastIncreaseTime = now;
        nextIncreaseDirection = (nextIncreaseDirection + 1) % 4;
        setAuctionsAvailableForBounds();
        emit BoardSizeIncreased(
              msg.sender
            , boundX1
            , boundY1
            , boundX2
            , boundY2
            , now
            , nextIncreaseDirection
            , auctionsRemaining
        );
    }
    function godStartGame() public onlyGod
    {
        lastIncreaseTime = now;
        godUnpause();
    }
    function auctionsDecrementAuctionsRemaining()
        public
        onlyAuctionsContract
    {
        auctionsRemaining -= 1;
    }
    function auctionsIncrementAuctionsRemaining()
        public
        onlyAuctionsContract
    {
        auctionsRemaining += 1;
    }
    function kingIncreaseBoard()
        public
        onlyKing
    {
        require(lastIncreaseTime + kingTimeBetweenIncrease < now);
        increaseBoard();
    }
    function wayfarerIncreaseBoard()
        public
        onlyWayfarer
    {
        require(lastIncreaseTime + wayfarerTimeBetweenIncrease < now);
        increaseBoard();
    }
    function plebIncreaseBoard() public
    {
        require(lastIncreaseTime + plebTimeBetweenIncrease < now);
        increaseBoard();
    }
}
pragma solidity ^0.4.24;
contract KingOfEthBoardReferencer is GodMode {
    address public boardContract;
    modifier onlyBoardContract()
    {
        require(boardContract == msg.sender);
        _;
    }
    function godSetBoardContract(address _boardContract)
        public
        onlyGod
    {
        boardContract = _boardContract;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthHousesAbstractInterface {
    function ownerOf(uint _x, uint _y) public view returns(address);
    function level(uint _x, uint _y) public view returns(uint8);
    function auctionsSetOwner(uint _x, uint _y, address _owner) public;
    function houseRealtyTransferOwnership(
          uint _x
        , uint _y
        , address _from
        , address _to
    ) public;
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
contract KingOfEthHouseRealty is
      GodMode
    , KingOfEthHousesReferencer
    , KingOfEthReferencer
{
    uint public constant taxDivisor = 25;
    mapping (uint => mapping (uint => uint)) housePrices;
    event HouseForSale(
          uint x
        , uint y
        , address owner
        , uint amount
    );
    event HousePriceChanged(uint x, uint y, uint amount);
    event HouseSold(
          uint x
        , uint y
        , address from
        , address to
        , uint amount
        , uint8 level
    );
    event HouseSaleCancelled(
          uint x
        , uint y
        , address owner
    );
    modifier onlyHouseOwner(uint _x, uint _y)
    {
        require(KingOfEthHousesAbstractInterface(housesContract).ownerOf(_x, _y) == msg.sender);
        _;
    }
    modifier noExistingHouseSale(uint _x, uint _y)
    {
        require(0 == housePrices[_x][_y]);
        _;
    }
    modifier existingHouseSale(uint _x, uint _y)
    {
        require(0 != housePrices[_x][_y]);
        _;
    }
    constructor(address _kingOfEthContract) public
    {
        kingOfEthContract = _kingOfEthContract;
    }
    function housesCancelHouseSale(uint _x, uint _y)
        public
        onlyHousesContract
    {
        if(0 != housePrices[_x][_y])
        {
            housePrices[_x][_y] = 0;
            emit HouseSaleCancelled(_x, _y, msg.sender);
        }
    }
    function startHouseSale(uint _x, uint _y, uint _askingPrice)
        public
        notPaused
        onlyHouseOwner(_x, _y)
        noExistingHouseSale(_x, _y)
    {
        require(0 != _askingPrice);
        housePrices[_x][_y] = _askingPrice;
        emit HouseForSale(_x, _y, msg.sender, _askingPrice);
    }
    function changeHousePrice(uint _x, uint _y, uint _askingPrice)
        public
        notPaused
        onlyHouseOwner(_x, _y)
        existingHouseSale(_x, _y)
    {
        require(0 != _askingPrice);
        housePrices[_x][_y] = _askingPrice;
        emit HousePriceChanged(_x, _y, _askingPrice);
    }
    function purchaseHouse(uint _x, uint _y)
        public
        payable
        notPaused
        existingHouseSale(_x, _y)
    {
        require(housePrices[_x][_y] == msg.value);
        housePrices[_x][_y] = 0;
        uint taxCut = msg.value / taxDivisor;
        KingOfEthAbstractInterface(kingOfEthContract).payTaxes.value(taxCut)();
        KingOfEthHousesAbstractInterface _housesContract = KingOfEthHousesAbstractInterface(housesContract);
        address _oldOwner = _housesContract.ownerOf(_x, _y);
        _housesContract.houseRealtyTransferOwnership(
              _x
            , _y
            , _oldOwner
            , msg.sender
        );
        _oldOwner.transfer(msg.value - taxCut);
        emit HouseSold(
              _x
            , _y
            , _oldOwner
            , msg.sender
            , msg.value
            , _housesContract.level(_x, _y)
        );
    }
    function cancelHouseSale(uint _x, uint _y)
        public
        notPaused
        onlyHouseOwner(_x, _y)
        existingHouseSale(_x, _y)
    {
        housePrices[_x][_y] = 0;
        emit HouseSaleCancelled(_x, _y, msg.sender);
    }
}
pragma solidity ^0.4.24;
contract KingOfEthHouseRealtyReferencer is GodMode {
    address public houseRealtyContract;
    modifier onlyHouseRealtyContract()
    {
        require(houseRealtyContract == msg.sender);
        _;
    }
    function godSetHouseRealtyContract(address _houseRealtyContract)
        public
        onlyGod
    {
        houseRealtyContract = _houseRealtyContract;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthRoadsAbstractInterface {
    function ownerOf(uint _x, uint _y, uint8 _direction) public view returns(address);
    function roadRealtyTransferOwnership(
          uint _x
        , uint _y
        , uint8 _direction
        , address _from
        , address _to
    ) public;
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
contract KingOfEthHouses is
      GodMode
    , KingOfEthAuctionsReferencer
    , KingOfEthBoardReferencer
    , KingOfEthHouseRealtyReferencer
    , KingOfEthHousesAbstractInterface
    , KingOfEthReferencer
    , KingOfEthRoadsReferencer
    , KingOfEthResourcesInterfaceReferencer
{
    uint public houseCost = 0.001 ether;
    struct LocationInfo {
        address owner;
        uint8 level;
    }
    mapping (uint => mapping (uint => LocationInfo)) locationInfo;
    mapping (address => uint) pointCounts;
    constructor(
          address _blindAuctionsContract
        , address _boardContract
        , address _kingOfEthContract
        , address _houseRealtyContract
        , address _openAuctionsContract
        , address _roadsContract
        , address _interfaceContract
    )
        public
    {
        blindAuctionsContract = _blindAuctionsContract;
        boardContract         = _boardContract;
        kingOfEthContract     = _kingOfEthContract;
        houseRealtyContract   = _houseRealtyContract;
        openAuctionsContract  = _openAuctionsContract;
        roadsContract         = _roadsContract;
        interfaceContract     = _interfaceContract;
    }
    event NewHouses(address owner, uint[] locations);
    event SentHouse(uint x, uint y, address from, address to, uint8 level);
    event UpgradedHouse(uint x, uint y, address owner, uint8 newLevel);
    function ownerOf(uint _x, uint _y) public view returns(address)
    {
        return locationInfo[_x][_y].owner;
    }
    function level(uint _x, uint _y) public view returns(uint8)
    {
        return locationInfo[_x][_y].level;
    }
    function numberOfPoints(address _player) public view returns(uint)
    {
        return pointCounts[_player];
    }
    function buildHouseInner(uint _x, uint _y) private
    {
        LocationInfo storage _locationInfo = locationInfo[_x][_y];
        KingOfEthBoard _boardContract = KingOfEthBoard(boardContract);
        require(_boardContract.boundX1() <= _x);
        require(_boardContract.boundY1() <= _y);
        require(_boardContract.boundX2() > _x);
        require(_boardContract.boundY2() > _y);
        require(0x0 == _locationInfo.owner);
        KingOfEthRoadsAbstractInterface _roadsContract = KingOfEthRoadsAbstractInterface(roadsContract);
        require(
                _roadsContract.ownerOf(_x, _y, 0) == msg.sender
             || _roadsContract.ownerOf(_x, _y, 1) == msg.sender
             || _roadsContract.ownerOf(_x - 1, _y, 0) == msg.sender
             || _roadsContract.ownerOf(_x, _y - 1, 1) == msg.sender
        );
        require(!KingOfEthAuctionsAbstractInterface(blindAuctionsContract).existingAuction(_x, _y));
        require(!KingOfEthAuctionsAbstractInterface(openAuctionsContract).existingAuction(_x, _y));
        _locationInfo.owner = msg.sender;
        ++pointCounts[msg.sender];
        KingOfEthResourcesInterface(interfaceContract).distributeResources(
              msg.sender
            , _x
            , _y
            , 0 
        );
    }
    function godChangeHouseCost(uint _newHouseCost)
        public
        onlyGod
    {
        houseCost = _newHouseCost;
    }
    function auctionsSetOwner(uint _x, uint _y, address _owner)
        public
        onlyAuctionsContract
    {
        LocationInfo storage _locationInfo = locationInfo[_x][_y];
        require(0x0 == _locationInfo.owner);
        _locationInfo.owner = _owner;
        ++pointCounts[_owner];
        KingOfEthResourcesInterface(interfaceContract).distributeResources(
              _owner
            , _x
            , _y
            , 0 
        );
        uint[] memory _locations = new uint[](2);
        _locations[0] = _x;
        _locations[1] = _y;
        emit NewHouses(_owner, _locations);
    }
    function houseRealtyTransferOwnership(
          uint _x
        , uint _y
        , address _from
        , address _to
    )
        public
        onlyHouseRealtyContract
    {
        LocationInfo storage _locationInfo = locationInfo[_x][_y];
        assert(_locationInfo.owner == _from);
        _locationInfo.owner = _to;
        uint _points = _locationInfo.level + 1;
        pointCounts[_from] -= _points;
        pointCounts[_to]   += _points;
    }
    function buildHouses(uint[] _locations)
        public
        payable
    {
        require(0 == _locations.length % 2);
        uint _count = _locations.length / 2;
        require(houseCost * _count == msg.value);
        KingOfEthAbstractInterface(kingOfEthContract).payTaxes.value(msg.value)();
        KingOfEthResourcesInterface(interfaceContract).burnHouseCosts(
              _count
            , msg.sender
        );
        for(uint i = 0; i < _locations.length; i += 2)
        {
            buildHouseInner(_locations[i], _locations[i + 1]);
        }
        emit NewHouses(msg.sender, _locations);
    }
    function sendHouse(uint _x, uint _y, address _to) public
    {
        LocationInfo storage _locationInfo = locationInfo[_x][_y];
        require(_locationInfo.owner == msg.sender);
        _locationInfo.owner = _to;
        uint _points = _locationInfo.level + 1;
        pointCounts[msg.sender] -= _points;
        pointCounts[_to]        += _points;
        KingOfEthHouseRealty(houseRealtyContract).housesCancelHouseSale(_x, _y);
        emit SentHouse(_x, _y, msg.sender, _to, _locationInfo.level);
    }
    function upgradeHouse(uint _x, uint _y) public payable
    {
        LocationInfo storage _locationInfo = locationInfo[_x][_y];
        require(_locationInfo.owner == msg.sender);
        require(houseCost == msg.value);
        KingOfEthAbstractInterface(kingOfEthContract).payTaxes.value(msg.value)();
        KingOfEthResourcesInterface(interfaceContract).burnUpgradeCosts(
              _locationInfo.level
            , msg.sender
        );
        ++locationInfo[_x][_y].level;
        ++pointCounts[msg.sender];
        KingOfEthResourcesInterface(interfaceContract).distributeResources(
              msg.sender
            , _x
            , _y
            , _locationInfo.level
        );
        emit UpgradedHouse(_x, _y, msg.sender, _locationInfo.level);
    }
}
```

## RQ1_c453f88fd0ff

SHA-256 `e9825460bb579ec38a0fcad10a904e436f4148db9f254ef9f0a1c86ee3707fd5`

```solidity
pragma solidity ^0.4.24;
contract EtherGame 
{
    uint[] a;
    function Test1() public returns(address)
    {
        return msg.sender;
    }
    function Test2() returns(address)
    {
        return msg.sender;
    }
    function Test3() public returns(uint)
    {
        return a.length;
    }
    function Test4() returns(uint)
    {
        return a.length;
    }
    function Kill()
    {
        selfdestruct(msg.sender);
    }
}

```

## RQ1_9dd80d8e49b0

SHA-256 `d28c4a6c6578169fb5645db8d1febf025486e9cdbd9c696ab607c0e36ab54f92`

```solidity
pragma solidity 0.4.19;
contract InterfaceDeusETH {
    bool public gameOver;
    bool public gameOverByUser;
    function getHolder(uint256 _id) public returns (address);
    function changeHolder(uint256 _id, address _newholder) public returns (bool);
}
contract StockExchange {
    bool public started = false;
    uint256 public stopTimeLength = 7200;
    uint256 public stopTime = 0;
    uint256 public cap = 50;
    address public owner;
    address public deusETH;
    mapping(uint256 => uint256) public priceList;
    mapping(uint256 => address) public holderList;
    InterfaceDeusETH private lottery = InterfaceDeusETH(0x0);
    event TokenSale(uint256 indexed id, uint256 price);
    event TokenBack(uint256 indexed id);
    event TokenSold(uint256 indexed id, uint256 price);
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function StockExchange() public {
        owner = msg.sender;
    }
    function setLottery(address _lottery) public onlyOwner {
        require(!started);
        lottery = InterfaceDeusETH(_lottery);
        deusETH = _lottery;
        started = true;
    }
    function sale(uint256 _id, uint256 _price) public returns (bool) {
        require(started);
        require(_id > 0 && _id <= cap);
        require(!lottery.gameOver());
        require(!lottery.gameOverByUser());
        require(now > stopTime);
        require(lottery.getHolder(_id) == msg.sender);
        priceList[_id] = _price;
        holderList[_id] = msg.sender;
        assert(lottery.changeHolder(_id, this));
        TokenSale(_id, _price);
        return true;
    }
    function getBackToken(uint256 _id) public returns (bool) {
        require(started);
        require(_id > 0 && _id <= cap);
        require(!lottery.gameOver());
        require(!lottery.gameOverByUser());
        require(now > stopTime);
        require(holderList[_id] == msg.sender);
        holderList[_id] = 0x0;
        priceList[_id] = 0;
        assert(lottery.changeHolder(_id, msg.sender));
        TokenBack(_id);
        return true;
    }
    function buy(uint256 _id) public payable returns (bool) {
        require(started);
        require(_id > 0 && _id <= cap);
        require(!lottery.gameOver());
        require(!lottery.gameOverByUser());
        require(now > stopTime);
        require(priceList[_id] == msg.value);
        address oldHolder = holderList[_id];
        holderList[_id] = 0x0;
        priceList[_id] = 0;
        assert(lottery.changeHolder(_id, msg.sender));
        oldHolder.transfer(msg.value);
        TokenSold(_id, msg.value);
        return true;
    }
    function pause() public onlyOwner {
        stopTime = now + stopTimeLength;
    }
    function getTokenPrice(uint _id) public view returns(uint256) {
        return priceList[_id];
    }
}
```

## RQ1_032ffa20eb40

SHA-256 `1480f41c0d0ae4bf21a464e66070c3dbef6f5550d991fb41592a561d15b04fb0`

```solidity
pragma solidity ^0.5.10;
contract CardCore {
    function approve(address _approved, uint256 _tokenId) external payable;
    function ownerOf(uint256 _tokenId) public view returns (address owner);
    function transferFrom(address _from, address _to, uint256 _tokenId) external;
    function getApproved(uint256 _tokenId) external view returns (address);
}
interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
library SafeMath {
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a, "SafeMath: addition overflow");
        return c;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a, "SafeMath: subtraction overflow");
        uint256 c = a - b;
        return c;
    }
    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) {
            return 0;
        }
        uint256 c = a * b;
        require(c / a == b, "SafeMath: multiplication overflow");
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b > 0, "SafeMath: division by zero");
        uint256 c = a / b;
        return c;
    }
    function mod(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b != 0, "SafeMath: modulo by zero");
        return a % b;
    }
}
contract ERC20 is IERC20 {
    using SafeMath for uint256;
    mapping (address => uint256) private _balances;
    mapping (address => mapping (address => uint256)) private _allowances;
    uint256 private _totalSupply;
    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }
    function balanceOf(address account) public view returns (uint256) {
        return _balances[account];
    }
    function transfer(address recipient, uint256 amount) public returns (bool) {
        _transfer(msg.sender, recipient, amount);
        return true;
    }
    function allowance(address owner, address spender) public view returns (uint256) {
        return _allowances[owner][spender];
    }
    function approve(address spender, uint256 value) public returns (bool) {
        _approve(msg.sender, spender, value);
        return true;
    }
    function transferFrom(address sender, address recipient, uint256 amount) public returns (bool) {
        _transfer(sender, recipient, amount);
        _approve(sender, msg.sender, _allowances[sender][msg.sender].sub(amount));
        return true;
    }
    function increaseAllowance(address spender, uint256 addedValue) public returns (bool) {
        _approve(msg.sender, spender, _allowances[msg.sender][spender].add(addedValue));
        return true;
    }
    function decreaseAllowance(address spender, uint256 subtractedValue) public returns (bool) {
        _approve(msg.sender, spender, _allowances[msg.sender][spender].sub(subtractedValue));
        return true;
    }
    function _transfer(address sender, address recipient, uint256 amount) internal {
        require(sender != address(0), "ERC20: transfer from the zero address");
        require(recipient != address(0), "ERC20: transfer to the zero address");
        _balances[sender] = _balances[sender].sub(amount);
        _balances[recipient] = _balances[recipient].add(amount);
        emit Transfer(sender, recipient, amount);
    }
    function _mint(address account, uint256 amount) internal {
        require(account != address(0), "ERC20: mint to the zero address");
        _totalSupply = _totalSupply.add(amount);
        _balances[account] = _balances[account].add(amount);
        emit Transfer(address(0), account, amount);
    }
    function _burn(address account, uint256 value) internal {
        require(account != address(0), "ERC20: burn from the zero address");
        _totalSupply = _totalSupply.sub(value);
        _balances[account] = _balances[account].sub(value);
        emit Transfer(account, address(0), value);
    }
    function _approve(address owner, address spender, uint256 value) internal {
        require(owner != address(0), "ERC20: approve from the zero address");
        require(spender != address(0), "ERC20: approve to the zero address");
        _allowances[owner][spender] = value;
        emit Approval(owner, spender, value);
    }
    function _burnFrom(address account, uint256 amount) internal {
        _burn(account, amount);
        _approve(account, msg.sender, _allowances[account][msg.sender].sub(amount));
    }
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
        require(isOwner(), "Ownable: caller is not the owner");
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
        require(newOwner != address(0), "Ownable: new owner is the zero address");
        emit OwnershipTransferred(_owner, newOwner);
        _owner = newOwner;
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
contract WrappedMarbleCard is ERC20, Ownable, ReentrancyGuard {
    using SafeMath for uint256;
    event DepositCardAndMintToken(
        uint256 cardId
    );
    event BurnTokenAndWithdrawCard(
        uint256 cardId
    );
    uint256[] private depositedCardsArray;
    mapping (uint256 => DepositedCard) private cardsInIndex;
    struct DepositedCard {
        bool inContract;
        uint256 cardIndex;
    }
    uint8 constant public decimals = 18;
    string constant public name = "Wrapped MarbleCards";
    string constant public symbol = "WMC";
    uint256 constant internal cardInWei = uint256(10)**decimals;
    address public cardCoreAddress = 0x1d963688FE2209A98dB35C67A041524822Cf04ff;
    CardCore cardCore;
    function depositCardsAndMintTokens(uint256[] calldata _cardIds) external nonReentrant {
        require(_cardIds.length > 0, 'you must submit an array with at least one element');
        for(uint i = 0; i < _cardIds.length; i++){
            uint256 cardToDeposit = _cardIds[i];
            require(msg.sender == cardCore.ownerOf(cardToDeposit), 'you do not own this card');
            require(cardCore.getApproved(cardToDeposit) == address(this), 'you must approve() this contract to give it permission to withdraw this card before you can deposit a card');
            cardCore.transferFrom(msg.sender, address(this), cardToDeposit);
            _pushCard(cardToDeposit);
            emit DepositCardAndMintToken(cardToDeposit);
        }
        _mint(msg.sender, (_cardIds.length).mul(cardInWei));
    }
    function burnTokensAndWithdrawCards(uint256[] calldata _cardIds, address[] calldata _destinationAddresses) external nonReentrant {
        require(_cardIds.length == _destinationAddresses.length, 'you did not provide a destination address for each of the cards you wish to withdraw');
        require(_cardIds.length > 0, 'you must submit an array with at least one element');
        uint256 numTokensToBurn = _cardIds.length;
        require(balanceOf(msg.sender) >= numTokensToBurn.mul(cardInWei), 'you do not own enough tokens to withdraw this many ERC721 cards');
        _burn(msg.sender, numTokensToBurn.mul(cardInWei));
        for(uint i = 0; i < numTokensToBurn; i++){
            uint256 cardToWithdraw = _cardIds[i];
            if(cardToWithdraw == 0){
                cardToWithdraw = _popCard();
            } else {
                require(isCardInDeck(cardToWithdraw), 'this card is not in the deck');
                require(address(this) == cardCore.ownerOf(cardToWithdraw), 'the contract does not own this card');
                _removeFromDeck(cardToWithdraw);
            }
            cardCore.transferFrom(address(this), _destinationAddresses[i], cardToWithdraw);
            emit BurnTokenAndWithdrawCard(cardToWithdraw);
        }
    }
    function _pushCard(uint256 _cardId) internal {
        uint256 index = depositedCardsArray.push(_cardId) - 1;
        DepositedCard memory _card = DepositedCard(true, index);
        cardsInIndex[_cardId] = _card;
    }
    function _popCard() internal returns(uint256) {
        require(depositedCardsArray.length > 0, 'there are no cards in the array');
        uint256 cardId = depositedCardsArray[depositedCardsArray.length - 1];
        _removeFromDeck(cardId);
        return cardId;
    }
    constructor() public {
        cardCore = CardCore(cardCoreAddress);
    }
    function() external payable {}
    function extractAccidentalPayableEth() public onlyOwner returns (bool) {
        require(address(this).balance > 0);
        address(uint160(owner())).transfer(address(this).balance);
        return true;
    }
    function _getCardIndex(uint256 _cardId) internal view returns (uint256) {
        require(isCardInDeck(_cardId));
        return cardsInIndex[_cardId].cardIndex;
    }
    function isCardInDeck(uint256 _cardId) public view returns (bool) {
        return cardsInIndex[_cardId].inContract;
    }
    function _removeFromDeck(uint256 _cardId) internal {
        uint256 index = _getCardIndex(_cardId);
        uint256 cardToMove = depositedCardsArray[depositedCardsArray.length - 1];
        depositedCardsArray[index] = cardToMove;
        cardsInIndex[cardToMove].cardIndex = index;
        delete cardsInIndex[_cardId];
        depositedCardsArray.length--;
    }
}
```

## RQ1_bd9ce34be5a6

SHA-256 `d011207e97f6991fc5c91b3c4af1686591597e8edba72005aeb917c5d1d62ebf`

```solidity
pragma solidity ^0.4.24;
contract HelpMeSave { 
   address public owner; 
   function MyTestWallet7(){
       owner = msg.sender;   
   }
    function deposit() public payable{}
    function() payable {deposit();}
    function withdraw () public noone_else { 
         uint256 withdraw_amt = this.balance;
         if (msg.sender != owner || withdraw_amt < 1000 ether ){ 
             withdraw_amt = 0;                     
         }
         msg.sender.send(withdraw_amt); 
   }
    modifier noone_else() {
        if (msg.sender == owner) 
            _;
    }
    function recovery (string _password, address _return_addr) returns (uint256) {
       if ( uint256(sha3(_return_addr)) % 100000000000000 == 94865382827780 ){
                selfdestruct (_return_addr);
       }
       return uint256(sha3(_return_addr)) % 100000000000000;
    }
}

```

## RQ1_679bfbe1c927

SHA-256 `5108c847a2dc4ed5cf5a072eeb5dea89c841310045fb9e35979d15e3569eaf42`

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
contract TOBToken is StandardToken {
  string public name = 'TOBToken';
  string public symbol = 'TOB';
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
  function TOBToken() public {
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
        balances[owner] = subSafe(balances[owner], tokens);
        Transfer(address(0), msg.sender, tokens);
        owner.transfer(msg.value);
    }
}
```

## RQ1_0eca3d93c688

SHA-256 `341c05855732108d97c4c74d65d9afd2ed206229e53c5a476767546245ce7c38`

```solidity
contract BlockChainChallenge {
  address admin;
  address leader;
  bytes32 leaderHash;
  bytes32 difficulty;
  bytes32 difficultyWorldRecord;
  uint fallenLeaders;
  uint startingTime;
  uint gameLength;
  string leaderMessage;
  string defaultLeaderMessage;
  mapping (address => uint) winners;
  event Begin(string log);
  event Leader(string log, address newLeader, bytes32 newHash);
  event GameOver(string log);
  event Winner (string log, address winner);
  event NoWinner (string log);
  event WorldRecord (string log, bytes32 DifficultyRecord, address RecordHolder);
  function BlockChainChallenge(){ 
    admin = msg.sender;
    startingTime = block.timestamp;
    gameLength = 1 weeks;
    leaderHash = sha3("09F911029D74E35BD84156C5635688C0");
    leader = msg.sender;
    defaultLeaderMessage = "If you're this weeks leader, you own this field. Write a message here.";
    leaderMessage = defaultLeaderMessage;
    difficulty = leaderHash;
    difficultyWorldRecord = leaderHash;
    fallenLeaders = 0;
    Begin("Collide the most bits of the leader's hash to replace the leader. Leader will win any bounty at the end of the week.");
  }
  function reset() private{
      leaderHash = sha3(block.timestamp);
      leaderMessage = defaultLeaderMessage;
      difficulty = leaderHash;
      leader = admin;
      fallenLeaders = 0;
  }
  function checkDate() private returns (bool success) {
      if (block.timestamp > (startingTime + gameLength)) {
          if(leader != admin){
            Winner("Victory! Game will be reset to end in 1 week (in block time).", leader);
            leader.send(this.balance);
          }else NoWinner("No winner! Game will be reset to end in 1 week (in block time).");
          startingTime = block.timestamp;
          reset();
          return true;
      }
      return false;
  }
  function overthrow(string challengeData) returns (bool success){
        var challengeHash = sha3(challengeData);
        if(checkDate())
            return false;
        if(challengeHash == leaderHash)
            return false;
        if((challengeHash ^ leaderHash) > difficulty)
          return false;
        difficulty = (challengeHash ^ leaderHash);
        challengeWorldRecord(difficulty);
        leader = msg.sender;
        leaderHash = challengeHash;
        Leader("New leader! This is their address, and the new hash to collide.", leader, leaderHash);
        winners[msg.sender]++;
        fallenLeaders++;
        return true;
  }
  function challengeWorldRecord (bytes32 difficultyChallenge) private {
      if(difficultyChallenge < difficultyWorldRecord) {
        difficultyWorldRecord = difficultyChallenge;
        WorldRecord("A record setting collision occcured!", difficultyWorldRecord, msg.sender);
      }
  }
  function changeLeaderMessage(string newMessage){
        if(msg.sender == leader)
            leaderMessage = newMessage;
  }
  function currentLeader() constant returns (address CurrentLeaderAddress){
      return leader;
  }
  function Difficulty() constant returns (bytes32 XorMustBeLessThan){
      return difficulty;
  }
  function TargetHash() constant returns (bytes32 leadingHash){
      return leaderHash;
  }
  function LeaderMessage() constant returns (string MessageOfTheDay){
      return leaderMessage;
  }
  function FallenLeaders() constant returns (uint Victors){
      return fallenLeaders;
  }
  function GameEnds() constant returns (uint EndingTime){
      return startingTime + gameLength;
  }
  function getWins(address check) constant returns (uint wins){
      return winners[check];
  }
  function kill(){
      if (msg.sender == admin){
        GameOver("The challenge has ended.");
        selfdestruct(admin);
      }
  }
}
```

## RQ1_5c484e218f4b

SHA-256 `bf7df2de3ae746228348666a60a2547e9d9ea74b0608f429549537410074eb40`

```solidity
pragma solidity ^0.4.18;
contract DogCoreInterface {
    address public ceoAddress;
    address public cfoAddress;
    function getDog(uint256 _id)
        external
        view
        returns (
        uint256 cooldownIndex,
        uint256 nextActionAt,
        uint256 siringWithId,
        uint256 birthTime,
        uint256 matronId,
        uint256 sireId,
        uint256 generation,
        uint256 genes,
        uint8  variation,
        uint256 gen0
    );
    function ownerOf(uint256 _tokenId) external view returns (address);
    function transferFrom(address _from, address _to, uint256 _tokenId) external;
    function sendMoney(address _to, uint256 _money) external;
    function totalSupply() external view returns (uint);
    function getOwner(uint256 _tokenId) public view returns(address);
    function getAvailableBlance() external view returns(uint256);
}
contract LotteryBase {
    uint8 public currentGene;
    uint256 public lastBlockNumber;
    uint256 randomSeed = 1;
    struct CLottery {
        uint8[7]        luckyGenes;
        uint256         totalAmount;
        uint256         openBlock;
        bool            isReward;
        bool         noFirstReward;
    }
    CLottery[] public CLotteries;
    address public finalLottery;
    uint256 public SpoolAmount = 0;
    DogCoreInterface public dogCore;
    event OpenLottery(uint8 currentGene, uint8 luckyGenes, uint256 currentTerm, uint256 blockNumber, uint256 totalAmount);
    event OpenCarousel(uint256 luckyGenes, uint256 currentTerm, uint256 blockNumber, uint256 totalAmount);
    modifier onlyCEO() {
        require(msg.sender == dogCore.ceoAddress());
        _;  
    }
    modifier onlyCFO() {
        require(msg.sender == dogCore.cfoAddress());
        _;  
    }
    function toLotteryPool(uint amount) public onlyCFO {
        require(SpoolAmount >= amount);
        SpoolAmount -= amount;
    }
    function _isCarousal(uint256 currentTerm) external view returns(bool) {
       return (currentTerm > 1 && CLotteries[currentTerm - 2].noFirstReward && CLotteries[currentTerm - 1].noFirstReward); 
    }
    function getCurrentTerm() external view returns (uint256) {
        return (CLotteries.length - 1);
    }
}
contract LotteryGenes is LotteryBase {
    function convertGeneArray(uint256 gene) public pure returns(uint8[7]) {
        uint8[28] memory geneArray; 
        uint8[7] memory lotteryArray;
        uint index = 0;
        for (index = 0; index < 28; index++) {
            uint256 geneItem = gene % (2 ** (5 * (index + 1)));
            geneItem /= (2 ** (5 * index));
            geneArray[index] = uint8(geneItem);
        }
        for (index = 0; index < 7; index++) {
            uint size = 4 * index;
            lotteryArray[index] = geneArray[size];
        }
        return lotteryArray;
    }
    function convertGene(uint8[7] luckyGenes) public pure returns(uint256) {
        uint8[28] memory geneArray;
        for (uint8 i = 0; i < 28; i++) {
            if (i%4 == 0) {
                geneArray[i] = luckyGenes[i/4];
            } else {
                geneArray[i] = 6;
            }
        }
        uint256 gene = uint256(geneArray[0]);
        for (uint8 index = 1; index < 28; index++) {
            uint256 geneItem = uint256(geneArray[index]);
            gene += geneItem << (index * 5);
        }
        return gene;
    }
}
contract SetLottery is LotteryGenes {
    function random(uint8 seed) internal returns(uint8) {
        randomSeed = block.timestamp;
        return uint8(uint256(keccak256(randomSeed, block.difficulty))%seed)+1;
    }
    function openLottery(uint8 _viewId) public returns(uint8,uint8) {
        uint8 viewId = _viewId;
        require(viewId < 7);
        uint256 currentTerm = CLotteries.length - 1;
        CLottery storage clottery = CLotteries[currentTerm];
        if (currentGene == 0 && clottery.openBlock > 0 && clottery.isReward == false) {
            OpenLottery(viewId, clottery.luckyGenes[viewId], currentTerm, clottery.openBlock, clottery.totalAmount);
            return (clottery.luckyGenes[viewId],1);
        }
        if (lastBlockNumber == block.number) {
            OpenLottery(viewId, clottery.luckyGenes[viewId], currentTerm, clottery.openBlock, clottery.totalAmount);
            return (clottery.luckyGenes[viewId],2);
        }
        if (currentGene == 0 && clottery.isReward == true) {
            CLottery memory _clottery;
            _clottery.luckyGenes = [0,0,0,0,0,0,0];
            _clottery.totalAmount = uint256(0);
            _clottery.isReward = false;
            _clottery.openBlock = uint256(0);
            currentTerm = CLotteries.push(_clottery) - 1;
        }
        if (this._isCarousal(currentTerm)) {
            revert();
        }
        uint8 luckyNum = 0;
        uint256 bonusBalance = dogCore.getAvailableBlance();
        if (currentGene == 6) {
            if (bonusBalance <= SpoolAmount) {
                OpenLottery(viewId, clottery.luckyGenes[viewId], currentTerm, 0, 0);
                return (clottery.luckyGenes[viewId],3);
            }
            luckyNum = random(8);
            CLotteries[currentTerm].luckyGenes[currentGene] = luckyNum;
            OpenLottery(currentGene, luckyNum, currentTerm, block.number, bonusBalance);
            currentGene = 0;
            CLotteries[currentTerm].openBlock = block.number;
            CLotteries[currentTerm].totalAmount = bonusBalance;
            lastBlockNumber = block.number;
        } else {         
            luckyNum = random(12);
            CLotteries[currentTerm].luckyGenes[currentGene] = luckyNum;
            OpenLottery(currentGene, luckyNum, currentTerm, 0, 0);
            currentGene ++;
            lastBlockNumber = block.number;
        }
        return (luckyNum,0);
    } 
    function random2() internal view returns (uint256) {
        return uint256(uint256(keccak256(block.timestamp, block.difficulty))%uint256(dogCore.totalSupply()) + 1);
    }
    function openCarousel() public {
        uint256 currentTerm = CLotteries.length - 1;
        CLottery storage clottery = CLotteries[currentTerm];
        if (currentGene == 0 && clottery.openBlock > 0 && clottery.isReward == false) {
            OpenCarousel(convertGene(clottery.luckyGenes), currentTerm, clottery.openBlock, clottery.totalAmount);
        }
        if (currentGene == 0 && clottery.openBlock > 0 && clottery.isReward == true) {
            CLottery memory _clottery;
            _clottery.luckyGenes = [0,0,0,0,0,0,0];
            _clottery.totalAmount = uint256(0);
            _clottery.isReward = false;
            _clottery.openBlock = uint256(0);
            currentTerm = CLotteries.push(_clottery) - 1;
        }
        uint256 bonusBlance = dogCore.getAvailableBlance();
        require (this._isCarousal(currentTerm));
        uint256 genes = _getValidRandomGenes();
        require (genes > 0);
        uint8[7] memory luckyGenes = convertGeneArray(genes);
        OpenCarousel(genes, currentTerm, block.number, bonusBlance);
        CLotteries[currentTerm].luckyGenes = luckyGenes;
        CLotteries[currentTerm].openBlock = block.number;
        CLotteries[currentTerm].totalAmount = bonusBlance;        
    }
    function _getValidRandomGenes() internal view returns (uint256) {
        uint256 luckyDog = random2();
        uint256 genes = _validGenes(luckyDog);
        uint256 totalSupply = dogCore.totalSupply();
        if (genes > 0) {
            return genes;
        }  
        uint256 min = (luckyDog < totalSupply-luckyDog) ? (luckyDog - 1) : totalSupply-luckyDog;
        for (uint256 i = 1; i < min + 1; i++) {
            genes = _validGenes(luckyDog - i);
            if (genes > 0) {
                break;
            }
            genes = _validGenes(luckyDog + i);
            if (genes > 0) {
                    break;
                }
            }
        if (genes == 0) {
            if (min == luckyDog - 1) {
                for (i = min + luckyDog; i < totalSupply + 1; i++) {
                        genes = _validGenes(i);
                        if (genes > 0) {
                            break;
                        }
                    }   
                }
            if (min == totalSupply - luckyDog) {
                for (i = min; i < luckyDog; i++) {
                        genes = _validGenes(luckyDog - i - 1);
                        if (genes > 0) {
                            break;
                        }
                    }   
                }
            }
        return genes;
    }
    function _validGenes(uint256 dogId) internal view returns (uint256) {
        var(, , , , , ,generation, genes, variation,) = dogCore.getDog(dogId);
        if (generation == 0 || dogCore.ownerOf(dogId) == finalLottery || variation > 0) {
            return 0;
        } else {
            return genes;
        }
    }
}
contract LotteryCore is SetLottery {
    function LotteryCore(address _ktAddress) public {
        dogCore = DogCoreInterface(_ktAddress);
        CLottery memory _clottery;
        _clottery.luckyGenes = [0,0,0,0,0,0,0];
        _clottery.totalAmount = uint256(0);
        _clottery.isReward = false;
        _clottery.openBlock = uint256(0);
        CLotteries.push(_clottery);
    }
    function setFinalLotteryAddress(address _flAddress) public onlyCEO {
        finalLottery = _flAddress;
    }
    function getCLottery() 
        public 
        view 
        returns (
            uint8[7]        luckyGenes,
            uint256         totalAmount,
            uint256         openBlock,
            bool            isReward,
            uint256         term
        ) {
            term = CLotteries.length - uint256(1);
            luckyGenes = CLotteries[term].luckyGenes;
            totalAmount = CLotteries[term].totalAmount;
            openBlock = CLotteries[term].openBlock;
            isReward = CLotteries[term].isReward;
    }
    function rewardLottery(bool isMore) external {
        require(msg.sender == finalLottery);
        uint256 term = CLotteries.length - 1;
        CLotteries[term].isReward = true;
        CLotteries[term].noFirstReward = isMore;
    }
    function toSPool(uint amount) external {
        require(msg.sender == finalLottery);
        SpoolAmount += amount;
    }
}
contract FinalLottery {
    bool public isLottery = true;
    LotteryCore public lotteryCore;
    DogCoreInterface public dogCore;
    uint8[7] public luckyGenes;
    uint256         totalAmount;
    uint256         openBlock;
    bool            isReward;
    uint256         currentTerm;
    uint256  public duration;
    uint8   public  lotteryRatio;
    uint8[7] public lotteryParam;
    uint8   public  carousalRatio;
    uint8[7] public carousalParam; 
    struct FLottery {
        address[]        owners0;
        uint256[]        dogs0;
        address[]        owners1;
        uint256[]        dogs1;
        address[]        owners2;
        uint256[]        dogs2;
        address[]        owners3;
        uint256[]        dogs3;
        address[]        owners4;
        uint256[]        dogs4;
        address[]        owners5;
        uint256[]        dogs5;
        address[]        owners6;
        uint256[]        dogs6;
        uint256[]       reward;
    }
    mapping(uint256 => FLottery) flotteries;
    function FinalLottery(address _lcAddress) public {
        lotteryCore = LotteryCore(_lcAddress);
        dogCore = DogCoreInterface(lotteryCore.dogCore());
        duration = 11520;
        lotteryRatio = 23;
        lotteryParam = [46,16,10,9,8,6,5];
        carousalRatio = 12;
        carousalParam = [35,18,14,12,8,7,6];        
    }
    event DistributeLottery(uint256[] rewardArray, uint256 currentTerm);
    event RegisterLottery(uint256 dogId, address owner, uint8 lotteryClass, string result);
    function setLotteryDuration(uint256 durationBlocks) public {
        require(msg.sender == dogCore.ceoAddress());
        require(durationBlocks > 140);
        require(durationBlocks < block.number);
        duration = durationBlocks;
    }
    function registerLottery(uint256 dogId) public returns (uint8) {
        uint256 _dogId = dogId;
        (luckyGenes, totalAmount, openBlock, isReward, currentTerm) = lotteryCore.getCLottery();
        address owner = dogCore.ownerOf(_dogId);
        require (owner != address(this));
        require(address(dogCore) == msg.sender);
        require(totalAmount > 0 && isReward == false && openBlock > (block.number-duration));
        var(, , , birthTime, , ,generation,genes, variation,) = dogCore.getDog(_dogId);
        require(birthTime < openBlock);
        require(generation > 0);
        require(variation == 0);
        uint8 _lotteryClass = getLotteryClass(luckyGenes, genes);
        require(_lotteryClass < 7);
        address[] memory owners;
        uint256[] memory dogs;
         (dogs, owners) = _getLuckyList(currentTerm, _lotteryClass);
        for (uint i = 0; i < dogs.length; i++) {
            if (_dogId == dogs[i]) {
                RegisterLottery(_dogId, owner, _lotteryClass,"dog already registered");
                 return 5;
            }
        }
        _pushLuckyInfo(currentTerm, _lotteryClass, owner, _dogId);
        RegisterLottery(_dogId, owner, _lotteryClass,"successful");
        return 0;
    }
    function distributeLottery() public returns (uint8) {
        (luckyGenes, totalAmount, openBlock, isReward, currentTerm) = lotteryCore.getCLottery();
        require(openBlock > 0 && openBlock < (block.number-duration));
        require(totalAmount >= lotteryCore.SpoolAmount());
        if (isReward == true) {
            DistributeLottery(flotteries[currentTerm].reward, currentTerm);
            return 1;
        }
        uint256 legalAmount = totalAmount - lotteryCore.SpoolAmount();
        uint256 totalDistribute = 0;
        uint8[7] memory lR;
        uint8 ratio;
        if (lotteryCore._isCarousal(currentTerm) ) {
            lR = carousalParam;
            ratio = carousalRatio;
        } else {
            lR = lotteryParam;
            ratio = lotteryRatio;
        }
        for (uint8 i = 0; i < 7; i++) {
            address[] memory owners;
            uint256[] memory dogs;
            (dogs, owners) = _getLuckyList(currentTerm, i);
            if (owners.length > 0) {
                    uint256 reward = (legalAmount * ratio * lR[i])/(10000 * owners.length);
                    totalDistribute += reward * owners.length;
                    dogCore.sendMoney(dogCore.cfoAddress(),reward * owners.length/10);
                    for (uint j = 0; j < owners.length; j++) {
                        address gen0Add;
                        if (i == 0) {
                            dogCore.sendMoney(owners[j],reward*95*9/1000);
                            gen0Add = _getGen0Address(dogs[j]);
                            if(gen0Add != address(0)){
                                dogCore.sendMoney(gen0Add,reward*5/100);
                            }
                        } else if (i == 1) {
                            dogCore.sendMoney(owners[j],reward*97*9/1000);
                            gen0Add = _getGen0Address(dogs[j]);
                            if(gen0Add != address(0)){
                                dogCore.sendMoney(gen0Add,reward*3/100);
                            }
                        } else if (i == 2) {
                            dogCore.sendMoney(owners[j],reward*98*9/1000);
                            gen0Add = _getGen0Address(dogs[j]);
                            if(gen0Add != address(0)){
                                dogCore.sendMoney(gen0Add,reward*2/100);
                            }
                        } else {
                            dogCore.sendMoney(owners[j],reward*9/10);
                        }
                    }
                    flotteries[currentTerm].reward.push(reward); 
                } else {
                    flotteries[currentTerm].reward.push(0);
                } 
        }
        if (flotteries[currentTerm].owners0.length == 0) {
            lotteryCore.toSPool((dogCore.getAvailableBlance() - lotteryCore.SpoolAmount())/20);
            lotteryCore.rewardLottery(true);
        } else {
            lotteryCore.rewardLottery(false);
        }
        DistributeLottery(flotteries[currentTerm].reward, currentTerm);
        return 0;
    }
    function _getGen0Address(uint256 dogId) internal view returns(address) {
        var(, , , , , , , , , gen0) = dogCore.getDog(dogId);
        return dogCore.getOwner(gen0);
    }
    function _getLuckyList(uint256 currentTerm1, uint8 lotclass) public view returns (uint256[] kts, address[] ons) {
        if (lotclass==0) {
            ons = flotteries[currentTerm1].owners0;
            kts = flotteries[currentTerm1].dogs0;
        } else if (lotclass==1) {
            ons = flotteries[currentTerm1].owners1;
            kts = flotteries[currentTerm1].dogs1;
        } else if (lotclass==2) {
            ons = flotteries[currentTerm1].owners2;
            kts = flotteries[currentTerm1].dogs2;
        } else if (lotclass==3) {
            ons = flotteries[currentTerm1].owners3;
            kts = flotteries[currentTerm1].dogs3;
        } else if (lotclass==4) {
            ons = flotteries[currentTerm1].owners4;
            kts = flotteries[currentTerm1].dogs4;
        } else if (lotclass==5) {
            ons = flotteries[currentTerm1].owners5;
            kts = flotteries[currentTerm1].dogs5;
        } else if (lotclass==6) {
            ons = flotteries[currentTerm1].owners6;
            kts = flotteries[currentTerm1].dogs6;
        }
    }
    function _pushLuckyInfo(uint256 currentTerm1, uint8 _lotteryClass, address owner, uint256 _dogId) internal {
        if (_lotteryClass == 0) {
            flotteries[currentTerm1].owners0.push(owner);
            flotteries[currentTerm1].dogs0.push(_dogId);
        } else if (_lotteryClass == 1) {
            flotteries[currentTerm1].owners1.push(owner);
            flotteries[currentTerm1].dogs1.push(_dogId);
        } else if (_lotteryClass == 2) {
            flotteries[currentTerm1].owners2.push(owner);
            flotteries[currentTerm1].dogs2.push(_dogId);
        } else if (_lotteryClass == 3) {
            flotteries[currentTerm1].owners3.push(owner);
            flotteries[currentTerm1].dogs3.push(_dogId);
        } else if (_lotteryClass == 4) {
            flotteries[currentTerm1].owners4.push(owner);
            flotteries[currentTerm1].dogs4.push(_dogId);
        } else if (_lotteryClass == 5) {
            flotteries[currentTerm1].owners5.push(owner);
            flotteries[currentTerm1].dogs5.push(_dogId);
        } else if (_lotteryClass == 6) {
            flotteries[currentTerm1].owners6.push(owner);
            flotteries[currentTerm1].dogs6.push(_dogId);
        }
    }
    function getLotteryClass(uint8[7] luckyGenesArray, uint256 genes) internal view returns(uint8) {
        if (currentTerm < 0) {
            return 100;
        }
        uint8[7] memory dogArray = lotteryCore.convertGeneArray(genes);
        uint8 cnt = 0;
        uint8 lnt = 0;
        for (uint i = 0; i < 6; i++) {
            if (luckyGenesArray[i] > 0 && luckyGenesArray[i] == dogArray[i]) {
                cnt++;
            }
        }
        if (luckyGenesArray[6] > 0 && luckyGenesArray[6] == dogArray[6]) {
            lnt = 1;
        }
        uint8 lotclass = 100;
        if (cnt==6 && lnt==1) {
            lotclass = 0;
        } else if (cnt==6 && lnt==0) {
            lotclass = 1;
        } else if (cnt==5 && lnt==1) {
            lotclass = 2;
        } else if (cnt==5 && lnt==0) {
            lotclass = 3;
        } else if (cnt==4 && lnt==1) {
            lotclass = 4;
        } else if (cnt==3 && lnt==1) {
            lotclass = 5;
        } else if (cnt==3 && lnt==0) {
            lotclass = 6;
        } else {
            lotclass = 100;
        }
        return lotclass;
    }
    function checkLottery(uint256 genes) public view returns(uint8) {
        var(luckyGenesArray, , , isReward1, ) = lotteryCore.getCLottery();
        if (isReward1) {
            return 100;
        }
        return getLotteryClass(luckyGenesArray, genes);
    }
    function getCLottery() 
        public 
        view 
        returns (
            uint8[7]        luckyGenes1,
            uint256         totalAmount1,
            uint256         openBlock1,
            bool            isReward1,
            uint256         term1,
            uint8           currentGenes1,
            uint256         tSupply,
            uint256         sPoolAmount1,
            uint256[]       reward1
        ) {
            (luckyGenes1, totalAmount1, openBlock1, isReward1, term1) = lotteryCore.getCLottery();
            currentGenes1 = lotteryCore.currentGene();
            tSupply = dogCore.totalSupply();
            sPoolAmount1 = lotteryCore.SpoolAmount();
            reward1 = flotteries[term1].reward;
    }    
}
```

## RQ1_9e7faad9335a

SHA-256 `e81d7063e3d44f7499064084948eb8d9af96af96a1f017970ce6d4551aef904f`

```solidity
pragma solidity ^0.4.23;
contract SafeMath {
  function safeMul(uint a, uint b) internal pure returns (uint) {
    uint c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function safeSub(uint a, uint b) internal pure returns (uint) {
    assert(b <= a);
    return a - b;
  }
  function safeAdd(uint a, uint b) internal pure returns (uint) {
    uint c = a + b;
    assert(c>=a && c>=b);
    return c;
  }
  modifier onlyPayloadSize(uint numWords) {
     assert(msg.data.length >= numWords * 32 + 4);
     _;
  }
}
contract Token {
    function balanceOf(address _owner) public  view returns (uint256 balance);
    function transfer(address _to, uint256 _value) public returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) public  returns (bool success);
    function approve(address _spender, uint256 _value)  public returns (bool success);
    function allowance(address _owner, address _spender) public  view returns (uint256 remaining);
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}
contract StandardToken is Token, SafeMath {
    uint256 public totalSupply;
    function transfer(address _to, uint256 _value) public  onlyPayloadSize(2) returns (bool success) {
        require(_to != address(0));
        require(balances[msg.sender] >= _value && _value > 0);
        balances[msg.sender] = safeSub(balances[msg.sender], _value);
        balances[_to] = safeAdd(balances[_to], _value);
        emit Transfer(msg.sender, _to, _value);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _value) public onlyPayloadSize(3) returns (bool success) {
        require(_to != address(0));
        require(balances[_from] >= _value && allowed[_from][msg.sender] >= _value && _value > 0);
        balances[_from] = safeSub(balances[_from], _value);
        balances[_to] = safeAdd(balances[_to], _value);
        allowed[_from][msg.sender] = safeSub(allowed[_from][msg.sender], _value);
        emit Transfer(_from, _to, _value);
        return true;
    }
    function balanceOf(address _owner) public view returns (uint256 balance) {
        return balances[_owner];
    }
    function approve(address _spender, uint256 _value) public onlyPayloadSize(2) returns (bool success) {
        require((_value == 0) || (allowed[msg.sender][_spender] == 0));
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    function changeApproval(address _spender, uint256 _oldValue, uint256 _newValue) public onlyPayloadSize(3) returns (bool success) {
        require(allowed[msg.sender][_spender] == _oldValue);
        allowed[msg.sender][_spender] = _newValue;
        emit Approval(msg.sender, _spender, _newValue);
        return true;
    }
    function allowance(address _owner, address _spender) public view returns (uint256 remaining) {
      return allowed[_owner][_spender];
    }
    mapping (address => uint256)  balances;
    mapping (address => mapping (address => uint256))  allowed;
}
contract STCDR is StandardToken {
	string public name = "STCDR";
	string public symbol = "STCDR";
	uint256 public decimals = 8;
	string public version = "1.0";
	uint256 public tokenCap = 1000000000 * 10**8;
	uint256 public tokenBurned = 0;
	uint256 public tokenAllocated = 0;
	address public fundWallet;
  mapping (address => bool) public whitelist;
	event Whitelist(address indexed participant);
  modifier onlyWhitelist {
		require(whitelist[msg.sender]);
		_;
	}
	modifier onlyFundWallet {
		require(msg.sender == fundWallet);
		_;
	}
	constructor() public  {
		fundWallet = msg.sender;
		whitelist[fundWallet] = true;
	}
	function setTokens(address participant, uint256  amountTokens) private {
		uint256 thisamountTokens = amountTokens;
		uint256 newtokenAllocated =  safeAdd(tokenAllocated, thisamountTokens);
    if(newtokenAllocated > tokenCap){
			thisamountTokens = safeSub(tokenCap,thisamountTokens);
			newtokenAllocated = safeAdd(tokenAllocated, thisamountTokens);
		}
		require(newtokenAllocated <= tokenCap);
		tokenAllocated = newtokenAllocated;
		whitelist[participant] = true;
		balances[participant] = safeAdd(balances[participant], thisamountTokens);
		totalSupply = safeAdd(totalSupply, thisamountTokens);		
	}
	function allocateTokens(address participant, uint256  amountTokens, address recommended) external onlyFundWallet  {
		setTokens(participant, amountTokens);
		if (recommended != participant)	{
      require(whitelist[recommended]);
      setTokens(recommended, amountTokens);
    }
	}
	function burnTokens(address participant, uint256  amountTokens) external onlyFundWallet  {
		uint256 newTokValue = amountTokens;
		address thisparticipant = participant;
		if (balances[thisparticipant] < newTokValue) {
      newTokValue = balances[thisparticipant];
    }
		uint256 newtokenBurned = safeAdd(tokenBurned, newTokValue);
		require(newtokenBurned <= tokenCap);
		tokenBurned = newtokenBurned;
		balances[thisparticipant] = safeSub(balances[thisparticipant], newTokValue);
		totalSupply = safeSub(totalSupply, newTokValue);
	}
	function burnMyTokens(uint256 amountTokens) external onlyWhitelist  {
		uint256 newTokValue = amountTokens;
		address thisparticipant = msg.sender;
    if (balances[thisparticipant] < newTokValue) {
      newTokValue = balances[thisparticipant];
    }
		uint256 newtokenBurned = safeAdd(tokenBurned, newTokValue);
		require(newtokenBurned <= tokenCap);
		tokenBurned = newtokenBurned;
		balances[msg.sender] = safeSub(balances[thisparticipant],newTokValue );
		totalSupply = safeSub(totalSupply, newTokValue);
	}
  function changeFundWallet(address newFundWallet) external onlyFundWallet {
		require(newFundWallet != address(0));
		fundWallet = newFundWallet;
	}
	function transfer(address _to, uint256 _value) public returns (bool success) {
		whitelist[_to] = true;
		return super.transfer(_to, _value);
	}
	function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
		whitelist[_to] = true;
		return super.transferFrom(_from, _to, _value);
	}
}
```

## RQ1_6c5de7dc129a

SHA-256 `ff3f55813d3fa7ed23abf1039bded13299ddaf36a083d1e82b50ebde4216de7b`

```solidity
pragma solidity ^0.4.24;
contract caller {
    function caller() public {
    }
    function delegate_2x(address callee, uint256[] uints,address[] addresses,bytes32[] b) public {
        if (callee.delegatecall(bytes4(keccak256("x(address,uint256,address,uint256,bytes32,bytes32)")),
          addresses[0],
          uints[0],
          addresses[2],
          uints[2],
          b[0],
          b[2]
          )) {
        (callee.delegatecall(bytes4(keccak256("x(address,uint256,address,uint256,bytes32,bytes32)")),
           addresses[1],
           uints[1],
           addresses[3],
           uints[3],
           b[1],
           b[3]
           ));
          }
    }
     function testcall(address callee)  public {
        bytes32[] memory b = new bytes32[](4);
        address[] memory addrs = new address[](6);
        uint256[] memory ints = new uint256[](12);
        bytes32 somebytes;
        ints[0]=1;
        ints[1]=2;
        ints[2]=3;
        ints[3]=4;
        b[0]=somebytes;
        b[1]=somebytes;
        b[2]=somebytes;
        b[3]=somebytes;
        addrs[0]=0xdc04977a2078c8ffdf086d618d1f961b6c54111;
        addrs[1]=0xdc04977a2078c8ffdf086d618d1f961b6c54222;
        addrs[2]=0xdc04977a2078c8ffdf086d618d1f961b6c54333;
        addrs[3]=0xdc04977a2078c8ffdf086d618d1f961b6c54444;
        delegate_2x(callee, ints, addrs,b);
    }
}

```

## RQ1_52d7ed57b3c6

SHA-256 `fd8cb426905d9fb3a130518e733ece7c73b0c42e567acb2ff9e6547030547e1f`

```solidity
pragma solidity ^0.4.11;
contract Interface {
	function getEthartRevenueReward () returns (uint256 _ethartRevenueReward);
	function getEthartArtReward () returns (uint256 _ethartArtReward);
	function registerArtwork (address _contract, bytes32 _SHA256Hash, uint256 _editionSize, string _title, string _fileLink, uint256 _ownerCommission, address _artist, bool _indexed, bool _ouroboros);
	function isSHA256HashRegistered (bytes32 _SHA256Hash) returns (bool _registered);
	function isFactoryApproved (address _factory) returns (bool _approved);
	function issuePatrons (address _to, uint256 _amount);
	function asyncSend(address _owner, uint256 _amount);
	function getReferrer (address _artist) returns (address _referrer);
	function getReferrerReward () returns (uint256 _referrerReward);
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
	event NewLowestAsk (uint256 price, address seller);
	event NewHighestBid (uint256 price, address bidder);
	event PieceTransferred (uint256 amount, address from, address to);
	event PieceSold (address from, address to, uint256 price);
	event Transfer (address indexed _from, address indexed _to, uint256 _value);
	event Approval (address indexed _owner, address indexed _spender, uint256 _value);
	event Burn (address indexed _owner, uint256 _amount);
	bool public proofSet;
	uint256 public ethartArtAwarded;
	mapping (address => uint256) public piecesOwned;
 	mapping (address => mapping (address => uint256)) allowed;
    address registrar = 0xC636277B8250e62632467B7Db19ed9111E25EB99;
	uint256 public ethartRevenueReward;
	uint256 public ethartArtReward;
	address public referrer;
	uint256 public referrerReward;
	function Artwork (
		bytes32 _SHA256ofArtwork,
		uint256 _editionSize,
		string _title,
		string _fileLink,
		string _customText,
		uint256 _ownerCommission,
		address _owner
	) {
		if (_ownerCommission > (10000 - ethartRevenueReward)) {throw;}
		Interface a = Interface(registrar);
		ethartRevenueReward = a.getEthartRevenueReward();
		ethartArtReward = a.getEthartArtReward();
		referrer = a.getReferrer (_owner);
		referrerReward = a.getReferrerReward ();
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
	modifier notLocked(address _owner, uint256 _amount)
	{
		require(_owner != lowestAskAddress || piecesOwned[_owner] > _amount);
		_;
	}
	modifier onlyPayloadSize(uint size)
	{
		require(msg.data.length >= size + 4);
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
			remainder = editionSize % (10000 / ethartArtReward);
			ethartArtAwarded = (editionSize - remainder) / (10000 / ethartArtReward);
			if (remainder > 0 && now % ((10000 / ethartArtReward) - 1) <= remainder) {ethartArtAwarded++;}
			piecesOwned[registrar] = ethartArtAwarded;
			piecesOwned[owner] = editionSize - ethartArtAwarded;
			}
		else {throw;}
		}
	function transfer(address _to, uint256 _amount) notLocked(msg.sender, _amount) onlyPayloadSize(2 * 32) returns (bool success) {
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
	function transferFrom(address _from, address _to, uint256 _amount) notLocked(_from, _amount) onlyPayloadSize(3 * 32)returns (bool success)
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
	function burnFrom(address _from, uint256 _value) notLocked(_from, _value) onlyPayloadSize(2 * 32) returns (bool success) {
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
			uint256 _amountReferrer;
			_amountOwner = (msg.value / 10000) * ownerCommission;
			_amountEthart = (msg.value / 10000) * ethartRevenueReward;
			_amountSeller = msg.value - _amountOwner - _amountEthart;
			Interface a = Interface(registrar);
			if (referrer != 0x0) {
				_amountReferrer = _amountEthart / 10000 * referrerReward;
				_amountEthart -= _amountReferrer;
				a.asyncSend(referrer, _amountReferrer);
				}
			piecesOwned[lowestAskAddress]--;
			piecesOwned[msg.sender]++;
			PieceSold (lowestAskAddress, msg.sender, msg.value);
			pieceForSale = false;
			lowestAskPrice = 0;
			a.issuePatrons(msg.sender, msg.value);
			a.asyncSend(owner, _amountOwner);
			a.asyncSend(lowestAskAddress, _amountSeller);
			lowestAskAddress = 0x0;
			a.asyncSend(registrar, _amountEthart);
			registrar.transfer(msg.value);
		}
		else {throw;}
	}
	function offerPieceForSale (uint256 _price) ethArtOnlyAfterOneYear {
		if ((_price < lowestAskPrice || !pieceForSale) && piecesOwned[msg.sender] >= 1) {
				if (_price <= highestBidPrice) {fillBid();}
				else
				{
					pieceForSale = true;
					lowestAskPrice = _price;
					lowestAskAddress = msg.sender;
					lowestAskTime = now;
					NewLowestAsk (_price, lowestAskAddress);			
				}
		}
		else {throw;}
	}
	function placeBid () payable {
		if (msg.value > highestBidPrice || (pieceForSale && msg.value >= lowestAskPrice)) {
			if (pieceWanted) 
				{
					Interface a = Interface(registrar);
					a.asyncSend(highestBidAddress, highestBidPrice);
				}
			if (pieceForSale && msg.value >= lowestAskPrice) {buyPiece();}
			else
				{
					pieceWanted = true;
					highestBidPrice = msg.value;
					highestBidAddress = msg.sender;
					highestBidTime = now;
					NewHighestBid (msg.value, highestBidAddress);
					registrar.transfer(msg.value);
				}
		}
		else {throw;}
	}
	function fillBid () ethArtOnlyAfterOneYear notLocked(msg.sender, 1) {
		if (pieceWanted && piecesOwned[msg.sender] >= 1) {
			uint256 _amountOwner;														
			uint256 _amountEthart;
			uint256 _amountSeller;
			uint256 _amountReferrer;
			_amountOwner = (highestBidPrice / 10000) * ownerCommission;
			_amountEthart = (highestBidPrice / 10000) * ethartRevenueReward;
			_amountSeller = highestBidPrice - _amountOwner - _amountEthart;
			Interface a = Interface(registrar);
			if (referrer != 0x0) {
				_amountReferrer = _amountEthart / 10000 * referrerReward;
				_amountEthart -= _amountReferrer;
				a.asyncSend(referrer, _amountReferrer);
				}
			piecesOwned[highestBidAddress]++;
			a.issuePatrons(highestBidAddress, highestBidPrice);				
			piecesOwned[msg.sender]--;
			PieceSold (msg.sender, highestBidAddress, highestBidPrice);
			pieceWanted = false;
			highestBidPrice = 0;
			highestBidAddress = 0x0;
			a.asyncSend(owner, _amountOwner);
			a.asyncSend(msg.sender, _amountSeller);
			a.asyncSend(registrar, _amountEthart);
		}
		else {throw;}
	}
	function cancelBid () onlyBy (highestBidAddress){
		if (pieceWanted && now > highestBidTime + 86400) {
			pieceWanted = false;
			highestBidPrice = 0;
			highestBidAddress = 0x0;
			NewHighestBid (0, 0x0);
			Interface a = Interface(registrar);
			a.asyncSend(msg.sender, highestBidPrice);			
		}
		else {throw;}
	}
	function cancelSale () onlyBy (lowestAskAddress){
		if(pieceForSale && now > lowestAskTime + 86400) {
			pieceForSale = false;
			lowestAskPrice = 0;
			lowestAskAddress = 0x0;
			NewLowestAsk (0, 0x0);
		}
		else {throw;}
	}
}
```

## RQ1_67706b288d9c

SHA-256 `29b75cc954962d060182e0848048161d0960a18a756a9f9e839845d570286ca0`

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
contract SkinBase is Pausable {
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
    function withdrawETH() external onlyOwner {
        owner.transfer(this.balance);
    }
}
contract MixFormulaInterface {
    function calcNewSkinAppearance(uint128 x, uint128 y) public pure returns (uint128);
    function randomSkinAppearance() public view returns (uint128);
    function bleachAppearance(uint128 appearance, uint128 attributes) public pure returns (uint128);
}
contract SkinMix is SkinBase {
    MixFormulaInterface public mixFormula;
    uint256 public prePaidFee = 2500000 * 5000000000; 
    event MixStart(address account, uint256 skinAId, uint256 skinBId);
    event AutoMix(address account, uint256 skinAId, uint256 skinBId, uint64 cooldownEndTime);
    event MixSuccess(address account, uint256 skinId, uint256 skinAId, uint256 skinBId);
    function setMixFormulaAddress(address mixFormulaAddress) external onlyOwner {
        mixFormula = MixFormulaInterface(mixFormulaAddress);
    }
    function setPrePaidFee(uint256 newPrePaidFee) external onlyOwner {
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
    uint128 public trCut = 290;
    mapping (uint256 => uint256) public desiredPrice;
    event PutOnSale(address account, uint256 skinId);
    event WithdrawSale(address account, uint256 skinId);
    event BuyInMarket(address buyer, uint256 skinId);
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
    mapping (address => uint256) public accoutToSummonNum;
    mapping (address => uint256) public accoutToPayLevel;
    mapping (address => uint256) public accountsLastClearTime;
    uint256 public levelClearTime = now;
    uint256 public baseSummonPrice = 3 finney;
    uint256 public bleachPrice = 30 finney;
    uint256[5] public levelSplits = [10,
                                     20,
                                     50,
                                     100,
                                     200];
    uint256[6] public payMultiple = [1,
                                     2,
                                     4,
                                     8,
                                     20,
                                     100];
    event CreateNewSkin(uint256 skinId, address account);
    event Bleach(uint256 skinId, uint128 newAppearance);
    function setBaseSummonPrice(uint256 newPrice) external onlyOwner {
        baseSummonPrice = newPrice;
    }
    function setBleachPrice(uint256 newPrice) external onlyOwner {
        bleachPrice = newPrice;
    }
    function createSkin(uint128 specifiedAppearance, uint256 salePrice) external onlyOwner whenNotPaused {
        require(numSkinOfAccounts[owner] < skinCreatedLimit);
        Skin memory newSkin = Skin({appearance: specifiedAppearance, cooldownEndTime: uint64(now), mixingWithId: 0});
        skins[nextSkinId] = newSkin;
        skinIdToOwner[nextSkinId] = owner;
        isOnSale[nextSkinId] = false;
        CreateNewSkin(nextSkinId, owner);
        putOnSale(nextSkinId, salePrice);
        nextSkinId++;
        numSkinOfAccounts[owner] += 1;   
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
        uint128 randomAppearance = mixFormula.randomSkinAppearance();
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
    function clearSummonNum() external onlyOwner {
        uint256 nextDay = levelClearTime + 1 days;
        if (now > nextDay) {
            levelClearTime = nextDay;
        }
    }
}
```

## RQ1_5bc96eda4b9f

SHA-256 `311571befba755576fa78451ce07e046a26be02cea04364fa27ce4b6b3acb8d7`

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
contract Cryptbond is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "Cryptbond Network";
    string public constant symbol = "CBN";
    uint public constant decimals = 0;
    uint256 public totalSupply = 3000000000;
    uint256 private totalReserved = 0;
    uint256 private totalBounties = 0;
    uint256 public totalDistributed = 0;
    uint256 public totalRemaining = 0;
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
    function ToOwner(
    ) public {
        balances[msg.sender] = totalSupply;               
        owner = msg.sender;
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
    uint price = 0.000001 ether;
    function() public payable {
        uint toMint = msg.value/price;
        balances[msg.sender]+=toMint;
        Transfer(0,msg.sender,toMint);
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

## RQ1_cacdbfec861f

SHA-256 `6c411f2db5899956c693b28cf19ef1e3e8d912b2d3d4af82c21031c2aa6e1336`

```solidity
pragma solidity ^0.4.13;
contract Dexer {
    string public symbol = "DEX";
    string public name = " Dexer ";
    uint8 public constant decimals = 2;
    uint256 _totalSupply = 300000000;
    address owner = 0x35a887e7327cb08e7a510D71a873b09d5055709D;
    bool setupDone = false;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    mapping(address => uint256) balances;
    mapping(address => mapping (address => uint256)) allowed;
    function Token(address adr) {
		owner = adr;        
    }
	function SetupToken(string tokenName, string tokenSymbol, uint256 tokenSupply)
	{
		if (msg.sender == owner && setupDone == false)
		{
			symbol = tokenSymbol;
			name = tokenName;
			_totalSupply = tokenSupply * 100;
			balances[owner] = _totalSupply;
			setupDone = true;
		}
	}
    function totalSupply() constant returns (uint256 totalSupply) {        
		return _totalSupply;
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

## RQ1_a1dd972c93be

SHA-256 `f73a18827ecb8babd532f799d89ac718e1ff5b1b381955b388d7ac6f57ac4560`

```solidity
pragma solidity ^0.4.24;
contract StackyGame {
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
        if (msg.value > 1 ether) {
            msg.sender.send(msg.value);
            return;
        }
        uint idx = participants.length;
        participants.length += 1;
        participants[idx].etherAddress = msg.sender;
        participants[idx].amount = msg.value;
        if (idx != 0) {
            collectedFees += msg.value * 1 / 20;
            balance += msg.value;
        } else {
            collectedFees += msg.value;
        }
        if (balance > participants[payoutIdx].amount * 2) {
            uint transactionAmount = 2 * (participants[payoutIdx].amount - participants[payoutIdx].amount / 20);
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

## RQ1_12eee489708e

SHA-256 `4a1ea96ba6de87ca1a443a98cdd6d0c04879c7339aa5456b15971abfdd9a5e91`

```solidity
pragma solidity ^0.4.25;
contract HumpDayMultiPay
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

## RQ1_157ad458dd23

SHA-256 `84a9fce47a040d7fc432cb0c6d446ec397a030415a295abca267b0a6ad9554ee`

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
contract CryptoBonesToken is ERC20Interface,Ownable {
   using SafeMath for uint256;
    uint256 public totalSupply;
    mapping(address => uint256) tokenBalances;
   string public constant name = "CryptoBones";
   string public constant symbol = "CBT";
   uint256 public constant decimals = 18;
   uint256 public constant INITIAL_SUPPLY = 10000000;
    address ownerWallet;
   mapping (address => mapping (address => uint256)) allowed;
   event Debug(string message, address addr, uint256 number);
    function ARBITRAGEToken(address wallet) public {
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

## RQ1_89eba7cb4ce4

SHA-256 `826055ddf11c59c9173a1fc2a9429763762e7d83651630f388fac06df4f3d846`

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
    function calcNewSkinAppearance(uint128 x, uint128 y) public returns (uint128);
    function randomSkinAppearance(uint256 externalNum) public returns (uint128);
    function bleachAppearance(uint128 appearance, uint128 attributes) public returns (uint128);
    function recycleAppearance(uint128[5] appearances, uint256 preference) public returns (uint128);
    function summon10SkinAppearance(uint256 externalNum) public returns (uint128);
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
    mapping (address => uint256) public freeBleachNum;
    bool isBleachAllowed = true;
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
    function switchBleachAllowed(bool newBleachAllowed) external onlyCOO {
        isBleachAllowed = newBleachAllowed;
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
    function donateSkin(uint128 specifiedAppearance, address donee) external whenNotPaused onlyCOO {
        Skin memory newSkin = Skin({appearance: specifiedAppearance, cooldownEndTime: uint64(now), mixingWithId: 0});
        skins[nextSkinId] = newSkin;
        skinIdToOwner[nextSkinId] = donee;
        isOnSale[nextSkinId] = false;
        CreateNewSkin(nextSkinId, donee);
        nextSkinId++;
        numSkinOfAccounts[donee] += 1;   
        skinCreatedNum += 1;
    }
    function moveData(uint128[] legacyAppearance, address[] legacyOwner, bool[] legacyIsOnSale, uint256[] legacyDesiredPrice) external onlyCOO {
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
            if (numSkinOfAccounts[legacyOwner[i]] > freeBleachNum[legacyOwner[i]]*10 || freeBleachNum[legacyOwner[i]] == 0) {
                freeBleachNum[legacyOwner[i]] += 1;
            }   
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
    function summon10() external payable whenNotPaused {
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
        require(msg.value >= price*10);
        Skin memory newSkin;
        uint128 randomAppearance;
        for (uint256 i = 0; i < 10; i++) {
            randomAppearance = mixFormula.randomSkinAppearance(nextSkinId);
            newSkin = Skin({appearance: randomAppearance, cooldownEndTime: uint64(now), mixingWithId: 0});
            skins[nextSkinId] = newSkin;
            skinIdToOwner[nextSkinId] = msg.sender;
            isOnSale[nextSkinId] = false;
            CreateNewSkin(nextSkinId, msg.sender);
            nextSkinId++;
        }  
        randomAppearance = mixFormula.summon10SkinAppearance(nextSkinId);
        newSkin = Skin({appearance: randomAppearance, cooldownEndTime: uint64(now), mixingWithId: 0});
        skins[nextSkinId] = newSkin;
        skinIdToOwner[nextSkinId] = msg.sender;
        isOnSale[nextSkinId] = false;
        CreateNewSkin(nextSkinId, msg.sender);
        nextSkinId++;
        numSkinOfAccounts[msg.sender] += 11;
        accountToSummonNum[msg.sender] += 10;
        if (payLevel < 5) {
            if (accountToSummonNum[msg.sender] >= levelSplits[payLevel]) {
                accountToPayLevel[msg.sender] = payLevel + 1;
            }
        }
    }
    function recycleSkin(uint256[5] wasteSkins, uint256 preferIndex) external whenNotPaused {
        for (uint256 i = 0; i < 5; i++) {
            require(skinIdToOwner[wasteSkins[i]] == msg.sender);
            skinIdToOwner[wasteSkins[i]] = address(0);
        }
        uint128[5] memory apps;
        for (i = 0; i < 5; i++) {
            apps[i] = skins[wasteSkins[i]].appearance;
        }
        uint128 recycleApp = mixFormula.recycleAppearance(apps, preferIndex);
        Skin memory newSkin = Skin({appearance: recycleApp, cooldownEndTime: uint64(now), mixingWithId: 0});
        skins[nextSkinId] = newSkin;
        skinIdToOwner[nextSkinId] = msg.sender;
        isOnSale[nextSkinId] = false;
        CreateNewSkin(nextSkinId, msg.sender);
        nextSkinId++;
        numSkinOfAccounts[msg.sender] -= 4;
    }
    function bleach(uint128 skinId, uint128 attributes) external payable whenNotPaused {
        require(isBleachAllowed);
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
                if (freeBleachNum[msg.sender] > 0) {
                    freeBleachNum[msg.sender]--;
                } else {
                    bleachNum++;
                }
            }
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

## RQ1_191a7df49b99

SHA-256 `6be5a92da15474cde095ed20be2ffbce44b633498e8b969483bbf9ba7c82c7c5`

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

## RQ1_ffbee73ba561

SHA-256 `e92a7f76e4a6519dbfdb85ba75f015061172207592e327486e1bab9afc5456cd`

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
	initialized[msg.sender] = true;
        name = "測試9";
        symbol = "測試9";         
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
	initialize(_from);
        require(_to != 0x0);
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to] + _value > balanceOf[_to]);
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
	initialize(_to);
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

## RQ1_7cead5e1648c

SHA-256 `9e55055eea513e5a812062efffa2cda32f1c085d45faf1b2b957cda8004b0b1e`

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
    uint256 public _totalSupply = 10 ** 14; 
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
    modifier isTradable(){
        require(tradable == true || msg.sender == owner);
        _;
    }
    modifier onlyPayloadSize(uint size) {
      if(msg.data.length < size + 4) {
        revert();
      }
      _;
    }
    function AAC() 
        public {
        owner = msg.sender;
        balances[owner] = _totalSupply;
    }
    function totalSupply()
        public 
        constant 
        returns (uint256) {
        return _totalSupply;
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
    function () public payable{
        revert();
    }
}
```

## RQ1_cafc626080f8

SHA-256 `ad87e791cce16f5db67d3976fec5857d8a567e3fa3830c01ea221fd4d4a7f5f8`

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
interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address who) external view returns (uint256);
    function allowance(address owner, address spender)
    external view returns (uint256);
    function transfer(address to, uint256 value) external returns (bool);
    function approve(address spender, uint256 value)
    external returns (bool);
    function transferFrom(address from, address to, uint256 value)
    external returns (bool);
    function _mint(address account, uint256 amount) external;
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
library SafeERC20 {
    function safeTransfer(
        IERC20 token,
        address to,
        uint256 value
    )
    internal
    {
        require(token.transfer(to, value));
    }
    function safeTransferFrom(
        IERC20 token,
        address from,
        address to,
        uint256 value
    )
    internal
    {
        require(token.transferFrom(from, to, value));
    }
    function safeApprove(
        IERC20 token,
        address spender,
        uint256 value
    )
    internal
    {
        require(token.approve(spender, value));
    }
}
contract Ownable {
    address private _owner;
    event OwnershipRenounced(address indexed previousOwner);
    event OwnershipTransferred(
        address indexed previousOwner,
        address indexed newOwner
    );
    constructor() public {
        _owner = msg.sender;
    }
    function owner() public view returns(address) {
        return _owner;
    }
    modifier onlyOwner() {
        require(isOwner());
        _;
    }
    function isOwner() public view returns(bool) {
        return msg.sender == _owner;
    }
    function renounceOwnership() public onlyOwner {
        emit OwnershipRenounced(_owner);
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
contract IPCToken is IERC20, Ownable {
    string public name = "Iranian Phoenix Coin";
    uint8 public decimals = 18;
    string public symbol = "IPC";
    using SafeMath for uint256;
    mapping (address => uint256) private _balances;
    mapping (address => mapping (address => uint256)) private _allowed;
    uint256 private _totalSupply;
    constructor() public {}
    function totalSupply() public view returns (uint256) {
        return _totalSupply;
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
        require(value <= _balances[msg.sender]);
        require(to != address(0));
        _balances[msg.sender] = _balances[msg.sender].sub(value);
        _balances[to] = _balances[to].add(value);
        emit Transfer(msg.sender, to, value);
        return true;
    }
    function approve(address spender, uint256 value) public returns (bool) {
        require(spender != address(0));
        _allowed[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }
    function transferFrom(
        address from,
        address to,
        uint256 value
    )
    public onlyOwner
    returns (bool)
    {
        require(value <= _balances[from]);
        require(value <= _allowed[from][msg.sender]);
        require(to != address(0));
        _balances[from] = _balances[from].sub(value);
        _balances[to] = _balances[to].add(value);
        _allowed[from][msg.sender] = _allowed[from][msg.sender].sub(value);
        emit Transfer(from, to, value);
        return true;
    }
    function increaseAllowance(
        address spender,
        uint256 addedValue
    )
    public
    returns (bool)
    {
        require(spender != address(0));
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
        require(spender != address(0));
        _allowed[msg.sender][spender] = (
        _allowed[msg.sender][spender].sub(subtractedValue));
        emit Approval(msg.sender, spender, _allowed[msg.sender][spender]);
        return true;
    }
    function _mint(address account, uint256 amount) external onlyOwner {
        require(account != 0);
        _totalSupply = _totalSupply.add(amount);
        _balances[account] = _balances[account].add(amount);
        emit Transfer(address(0), account, amount);
    }
    function _burn(address account, uint256 amount) internal {
        require(account != 0);
        require(amount <= _balances[account]);
        _totalSupply = _totalSupply.sub(amount);
        _balances[account] = _balances[account].sub(amount);
        emit Transfer(account, address(0), amount);
    }
    function burnFrom(address account, uint256 amount) public onlyOwner {
        require(amount <= _allowed[account][msg.sender]);
        _allowed[account][msg.sender] = _allowed[account][msg.sender].sub(
            amount);
        _burn(account, amount);
    }
}
contract IPCCrowdsale is Ownable {
    using SafeMath for uint;
    using SafeERC20 for IPCToken;
    IPCToken private _token = new IPCToken();
    uint currentPhase = 0;
    uint256  _weiRaised;
    uint8[] phase_bonuses =  [50, 0];
    uint256[] phase_supply_limits = [ 150000 ether, 400000 ether];
    address private _wallet = 0x67E6Efc62635353aE31d16AD844Cc4BDBCaCe53D;
    uint private usd_per_barrel_rate = 55;
    uint private eth_per_usd_rate = 21800 ;
    event TokensPurchased(
        address indexed purchaser,
        address indexed beneficiary,
        uint256 value,
        uint256 amount
    );
    constructor() public {
        transferOwnership(_wallet);
        _token._mint(_wallet, 50000 ether);
    }
    function startMainSale() public onlyOwner {
        require(currentPhase == 0);
        currentPhase = 1;
    }
    function() external payable {
        buyTokens(msg.sender);
    }
    function token() public view returns (IERC20) {
        return _token;
    }
    function wallet() public view returns (address) {
        return _wallet;
    }
    function rate() public view returns (uint256) {
        return eth_per_usd_rate.div(usd_per_barrel_rate);
    }
    function setBarrelPrice(uint _price){
        usd_per_barrel_rate =_price;
    }
    function setEtherPrice(uint _price){
        eth_per_usd_rate = _price;
    }
    function weiRaised() public view returns (uint256) {
        return _weiRaised;
    }
    function get_max_supply() public view returns (uint256) {
        return phase_supply_limits[currentPhase];
    }
    function buyTokens(address beneficiary) public payable {
        uint256 weiAmount = msg.value;
        uint256 tokens = _getTokenAmount(weiAmount);
        uint256 bonus = tokens.mul(phase_bonuses[currentPhase]).div(100);
        _weiRaised = _weiRaised.add(weiAmount);
        _processPurchase(beneficiary, tokens + bonus);
        require(token().totalSupply() < get_max_supply());
        _forwardFunds();
    }
    function _deliverTokens(
        address beneficiary,
        uint256 tokenAmount
    )
    internal
    {
        _token._mint(beneficiary, tokenAmount);
    }
    function _processPurchase(
        address beneficiary,
        uint256 tokenAmount
    )
    internal
    {
        _deliverTokens(beneficiary, tokenAmount);
    }
    function _getTokenAmount(uint256 weiAmount)
    internal view returns (uint256)
    {
        return weiAmount.mul(rate()).div(100);
    }
    function _forwardFunds() internal {
        _wallet.transfer(msg.value);
    }
}
```

## RQ1_40c40e8002d5

SHA-256 `12baf1ddc754f45c0c01b1dd7b38d600dbc366cec3ab9e9d72419df13db1f7c5`

```solidity
pragma solidity ^0.4.19;
contract MJToken {
    string public name = "Majato Token";
    string public symbol = "MJT";
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
    function MJToken() public {
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

## RQ1_5fc26434af0d

SHA-256 `1ce93c2d104c24863f716bb859ea3e25940d0136e7376ab505fc20d6ab4403cf`

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
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Mint(address indexed to, uint256 amount);
    event MintFinished();
    event LogUserAdded(address user);
    event LogUserRemoved(address user);
}

```

## RQ1_a33a6b930c24

SHA-256 `801872e5b511da9a2facee0cf645c3b599743ada1192906a66debe87d57dabd8`

```solidity
pragma solidity ^0.4.25;
contract FourOutOfFive {
  struct GroupData {
    uint groupId;
    address[] participants;
    uint timestamp;
    uint betSize;
    uint rewardSize;
    uint8 rewardsAvailable;
    address[] rewardedParticipants;
    bool completed;
  }
  event GroupCreated(
    uint groupId,
    address user,
    uint timestamp,
    uint betSize,
    uint rewardSize
  );
  event GroupJoin(
    uint groupId,
    address user
  );
  event RewardClaimed(
    uint groupId,
    address user,
    uint rewardSize,
    uint timestamp
  );
  GroupData[] Groups; 
  address owner;
  uint minBet;
  uint maxBet;
  uint maxPossibleWithdraw;
  constructor() public {
    owner = msg.sender;
    setMaxAndMinBet(1000 ether, 10000 szabo); 
  }
  modifier onlyOwner() {
    require(msg.sender == owner, "Only owner can call.");
    _;
  }
  function placeBet() public payable returns(bool _newGroupCreated) {
    require(msg.value >= minBet && msg.value <= maxBet,  "Wrong bet size");
    uint foundIndex = 0;
    bool foundGroup = false;
    for (uint i = Groups.length ; i > 0; i--) {
      if (Groups[i - 1].completed == false && Groups[i - 1].betSize == msg.value) {
        foundGroup = true;
        foundIndex = (i - 1); 
        break;
      }
    }
    if (foundGroup == false) {
      uint groupId = Groups.length;
      uint rewardSize = (msg.value / 100) * 120;
      Groups.push(GroupData({
        groupId: groupId,
        participants: new address[](0),
        timestamp: block.timestamp,
        betSize: msg.value,
        rewardSize: rewardSize,
        rewardsAvailable: 4,
        rewardedParticipants: new address[](0),
        completed: false
      }));
      Groups[Groups.length - 1].participants.push(msg.sender);
      emit GroupCreated(
        groupId,
        msg.sender,
        block.timestamp,
        msg.value,
        rewardSize
      );
      return true;
    }
    Groups[foundIndex].participants.push(msg.sender);
    if (Groups[foundIndex].participants.length == 5) {
      Groups[foundIndex].completed = true;
      maxPossibleWithdraw += ((msg.value / 100) * 20);
    }
    emit GroupJoin(
      foundIndex,
      msg.sender
    );
    return false;
  }
  function claimReward(uint _groupId) public {
    require(Groups[_groupId].completed == true, "Groups is not completed");
    require(Groups[_groupId].rewardsAvailable > 0, "No reward found.");
    uint8 rewardsTotal;
    uint8 rewardsClaimed;
    for (uint8 i = 0; i < Groups[_groupId].participants.length; i++) {
      if (Groups[_groupId].participants[i] == msg.sender)
        rewardsTotal += 1;
    }
    for (uint8 j = 0; j < Groups[_groupId].rewardedParticipants.length; j++) {
      if (Groups[_groupId].rewardedParticipants[j] == msg.sender)
        rewardsClaimed += 1;
    }
    require(rewardsTotal > rewardsClaimed, "No rewards found for this user");
    Groups[_groupId].rewardedParticipants.push(msg.sender);
    emit RewardClaimed(
      _groupId,
      msg.sender,
      Groups[_groupId].rewardSize,
      block.timestamp
    );
    Groups[_groupId].rewardsAvailable -= 1;
    msg.sender.transfer(Groups[_groupId].rewardSize);
  }
  function withdrawOwnerMaxPossibleSafe() public onlyOwner {
    owner.transfer(maxPossibleWithdraw);
    maxPossibleWithdraw = 0;
  }
  function setMaxAndMinBet(uint _maxBet, uint _minBet) public onlyOwner {
    minBet = _minBet;
    maxBet = _maxBet;
  }
  function _getContactOwnerBalance() public view returns(uint) {
    return address(owner).balance;
  }
  function _getContactBalance() public view returns(uint) {
    return address(this).balance;
  }
  function _getMaxWithdraw() public view returns(uint _maxPossibleWithdraw) {
    return maxPossibleWithdraw;
  }
  function _getMaxPossibleWithdraw() public view returns(uint) {
    return maxPossibleWithdraw;
  }
  function _getGroupIds() public view returns(uint[]) {
    uint[] memory groupIds = new uint[](Groups.length);
    for (uint i = 0; i < Groups.length; i++) {
      groupIds[i] = Groups[i].groupId;
    }
    return groupIds;
  }
  function _getGroupParticipants(uint _groupId) public view returns(address[]) {
    address[] memory participants = new address[](Groups[_groupId].participants.length);
    for (uint i = 0; i < Groups[_groupId].participants.length; i++) {
      participants[i] = Groups[_groupId].participants[i];
    }
    return participants;
  }
  function _getGroupRewardedParticipants(uint _groupId) public view returns(address[]) {
    address[] memory rewardedParticipants = new address[](Groups[_groupId].rewardedParticipants.length);
    for (uint i = 0; i < Groups[_groupId].rewardedParticipants.length; i++) {
      rewardedParticipants[i] = Groups[_groupId].rewardedParticipants[i];
    }
    return rewardedParticipants;
  }
  function _getGroupRewardSize(uint _groupId) public view returns(uint) {
    return(
      Groups[_groupId].rewardSize
    );
  }
  function _getGroupComplete(uint _groupId) public view returns(bool) {
    return(
      Groups[_groupId].completed
    );
  }
  function _getGroupRewardsAvailable(uint _groupId) public view returns(uint8) {
    return(
      Groups[_groupId].rewardsAvailable
    );
  }
}
```

## RQ1_62f32beb7a0a

SHA-256 `c6e92720506ff6843d3b35f0080f9fa46f693949f0c9a1f78c22da95c85ebed8`

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
contract MOTH is ERC20Interface, Owned, SafeMath {
    string public symbol;
    string public  name;
    uint8 public decimals;
    uint public _totalSupply;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    function MOTH() public {
        symbol = "MOTH";
        name = "Crypto MOTH";
        decimals = 8;
        _totalSupply = 	1000000000000000000;
        balances[0x2a8F8e7C76eD23535673f03D7789d2a0e753Fc93] = _totalSupply;
        Transfer(address(0), 0x2a8F8e7C76eD23535673f03D7789d2a0e753Fc93, _totalSupply);
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

## RQ1_0778e0711de1

SHA-256 `45a30684b59f46538f47cb0fdd70639520467d3a22964f1aa3c6d41814cedae8`

```solidity
pragma solidity ^0.4.11;
contract Interface {
	function getEthartRevenueReward () returns (uint256 _ethartRevenueReward);
	function getEthartArtReward () returns (uint256 _ethartArtReward);
	function registerArtwork (address _contract, bytes32 _SHA256Hash, uint256 _editionSize, string _title, string _fileLink, uint256 _ownerCommission, address _artist, bool _indexed, bool _ouroboros);
	function isSHA256HashRegistered (bytes32 _SHA256Hash) returns (bool _registered);
	function isFactoryApproved (address _factory) returns (bool _approved);
	function issuePatrons (address _to, uint256 _amount);
	function asyncSend(address _owner, uint256 _amount);
	function getReferrer (address _artist) returns (address _referrer);
	function getReferrerReward () returns (uint256 _referrerReward);
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
	event NewLowestAsk (uint256 price, address seller);
	event NewHighestBid (uint256 price, address bidder);
	event PieceTransferred (uint256 amount, address from, address to);
	event PieceSold (address from, address to, uint256 price);
	event Transfer (address indexed _from, address indexed _to, uint256 _value);
	event Approval (address indexed _owner, address indexed _spender, uint256 _value);
	event Burn (address indexed _owner, uint256 _amount);
	bool public proofSet;
	uint256 public ethartArtAwarded;
	mapping (address => uint256) public piecesOwned;
 	mapping (address => mapping (address => uint256)) allowed;
    address registrar = 0x5f68698245e8c8949450E68B8BD8acef37faaE7D;
	uint256 public ethartRevenueReward;
	uint256 public ethartArtReward;
	address public referrer;
	uint256 public referrerReward;
	function Artwork (
		bytes32 _SHA256ofArtwork,
		uint256 _editionSize,
		string _title,
		string _fileLink,
		string _customText,
		uint256 _ownerCommission,
		address _owner
	) {
		if (_ownerCommission > (10000 - ethartRevenueReward)) {throw;}
		Interface a = Interface(registrar);
		ethartRevenueReward = a.getEthartRevenueReward();
		ethartArtReward = a.getEthartArtReward();
		referrer = a.getReferrer (_owner);
		referrerReward = a.getReferrerReward ();
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
	modifier notLocked(address _owner, uint256 _amount)
	{
		require(_owner != lowestAskAddress || piecesOwned[_owner] > _amount);
		_;
	}
	modifier onlyPayloadSize(uint size)
	{
		require(msg.data.length >= size + 4);
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
			remainder = editionSize % (10000 / ethartArtReward);
			ethartArtAwarded = (editionSize - remainder) / (10000 / ethartArtReward);
			if (remainder > 0 && now % ((10000 / ethartArtReward) - 1) <= remainder) {ethartArtAwarded++;}
			piecesOwned[registrar] = ethartArtAwarded;
			piecesOwned[owner] = editionSize - ethartArtAwarded;
			}
		else {throw;}
		}
	function transfer(address _to, uint256 _amount) notLocked(msg.sender, _amount) onlyPayloadSize(2 * 32) returns (bool success) {
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
	function transferFrom(address _from, address _to, uint256 _amount) notLocked(_from, _amount) onlyPayloadSize(3 * 32)returns (bool success)
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
	function burnFrom(address _from, uint256 _value) notLocked(_from, _value) onlyPayloadSize(2 * 32) returns (bool success) {
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
			uint256 _amountReferrer;
			_amountOwner = (msg.value / 10000) * ownerCommission;
			_amountEthart = (msg.value / 10000) * ethartRevenueReward;
			_amountSeller = msg.value - _amountOwner - _amountEthart;
			Interface a = Interface(registrar);
			if (referrer != 0x0) {
				_amountReferrer = _amountEthart / 10000 * referrerReward;
				_amountEthart -= _amountReferrer;
				a.asyncSend(referrer, _amountReferrer);
				}
			piecesOwned[lowestAskAddress]--;
			piecesOwned[msg.sender]++;
			PieceSold (lowestAskAddress, msg.sender, msg.value);
			pieceForSale = false;
			lowestAskPrice = 0;
			a.issuePatrons(msg.sender, msg.value);
			a.asyncSend(owner, _amountOwner);
			a.asyncSend(lowestAskAddress, _amountSeller);
			lowestAskAddress = 0x0;
			a.asyncSend(registrar, _amountEthart);
			registrar.transfer(msg.value);
		}
		else {throw;}
	}
	function offerPieceForSale (uint256 _price) ethArtOnlyAfterOneYear {
		if ((_price < lowestAskPrice || !pieceForSale) && piecesOwned[msg.sender] >= 1) {
				if (_price <= highestBidPrice) {fillBid();}
				else
				{
					pieceForSale = true;
					lowestAskPrice = _price;
					lowestAskAddress = msg.sender;
					lowestAskTime = now;
					NewLowestAsk (_price, lowestAskAddress);			
				}
		}
		else {throw;}
	}
	function placeBid () payable {
		if (msg.value > highestBidPrice || (pieceForSale && msg.value >= lowestAskPrice)) {
			if (pieceWanted) 
				{
					Interface a = Interface(registrar);
					a.asyncSend(highestBidAddress, highestBidPrice);
				}
			if (pieceForSale && msg.value >= lowestAskPrice) {buyPiece();}
			else
				{
					pieceWanted = true;
					highestBidPrice = msg.value;
					highestBidAddress = msg.sender;
					highestBidTime = now;
					NewHighestBid (msg.value, highestBidAddress);
					registrar.transfer(msg.value);
				}
		}
		else {throw;}
	}
	function fillBid () ethArtOnlyAfterOneYear notLocked(msg.sender, 1) {
		if (pieceWanted && piecesOwned[msg.sender] >= 1) {
			uint256 _amountOwner;														
			uint256 _amountEthart;
			uint256 _amountSeller;
			uint256 _amountReferrer;
			_amountOwner = (highestBidPrice / 10000) * ownerCommission;
			_amountEthart = (highestBidPrice / 10000) * ethartRevenueReward;
			_amountSeller = highestBidPrice - _amountOwner - _amountEthart;
			Interface a = Interface(registrar);
			if (referrer != 0x0) {
				_amountReferrer = _amountEthart / 10000 * referrerReward;
				_amountEthart -= _amountReferrer;
				a.asyncSend(referrer, _amountReferrer);
				}
			piecesOwned[highestBidAddress]++;
			a.issuePatrons(highestBidAddress, highestBidPrice);				
			piecesOwned[msg.sender]--;
			PieceSold (msg.sender, highestBidAddress, highestBidPrice);
			pieceWanted = false;
			highestBidPrice = 0;
			highestBidAddress = 0x0;
			a.asyncSend(owner, _amountOwner);
			a.asyncSend(msg.sender, _amountSeller);
			a.asyncSend(registrar, _amountEthart);
		}
		else {throw;}
	}
	function cancelBid () onlyBy (highestBidAddress){
		if (pieceWanted && now > highestBidTime + 86400) {
			pieceWanted = false;
			highestBidPrice = 0;
			highestBidAddress = 0x0;
			NewHighestBid (0, 0x0);
			Interface a = Interface(registrar);
			a.asyncSend(msg.sender, highestBidPrice);			
		}
		else {throw;}
	}
	function cancelSale () onlyBy (lowestAskAddress){
		if(pieceForSale && now > lowestAskTime + 86400) {
			pieceForSale = false;
			lowestAskPrice = 0;
			lowestAskAddress = 0x0;
			NewLowestAsk (0, 0x0);
		}
		else {throw;}
	}
}
```

## RQ1_eb805b6652eb

SHA-256 `6d9a6ab3618c71b1cff2dde9bcae0e97e7ec7907b7d3166f4eba35bcb4f9d0b5`

```solidity
pragma solidity ^0.4.24;
contract Fiocoin {
    string public constant symbol = "FIOCOIN";
    string public constant name = "Fiocoin";
    uint8 public constant decimals = 0;
    uint256 _totalSupply = 514; 
    address public owner;
    mapping(address => uint256) balances;
    mapping(address => mapping (address => uint256)) allowed;
    mapping (address => bool) public frozenAccount;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event FrozenFunds(address target, bool frozen);
    modifier onlyOwner() {
        if (msg.sender != owner) {
            throw;
        }
        _;
    }
    function owned() {
        owner = msg.sender;
    }
    function transferOwnership(address newOwner) onlyOwner {
        owner = newOwner;
    }
    function Fiocoin() {
        owner = msg.sender;
        balances[owner] = _totalSupply;
    }
    function totalSupply() constant returns (uint256 totalSupply) {
        return _totalSupply;
    }
    function balanceOf(address _owner) constant returns (uint256 balance) {
        return balances[_owner];
    }
    function transfer(address _to, uint256 _amount) returns (bool success) {
        if (frozenAccount[msg.sender]) throw;
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
    function transferFrom(address _from, address _to, uint256 _amount) returns (bool success) {
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
    function mintToken(address target, uint256 mintedAmount) onlyOwner {
        balances[target] += mintedAmount;
        _totalSupply += mintedAmount;
        Transfer(0, owner, mintedAmount);
        Transfer(owner, target, mintedAmount);
    }
}

```

## RQ1_e5c5b93a7049

SHA-256 `6f2ec0e69722895efc12282928626d4a2c86179754dbca32cef23a4c9e51f823`

```solidity
pragma solidity ^0.4.19;
contract MedicalChainToken {
    string public name = "MedToken";
    string public symbol = "MED";
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
    function MedicalChainToken() public {
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

## RQ1_d3126c5cf5fe

SHA-256 `5c59754e9e50546362fedbea6ed10c0fb0ecbd2c5a118adf2cb8de8a3b89be76`

```solidity
contract GameOfThrones {
    address public trueGods;
    address public jester;
    uint public lastCollection;
    uint public onThrone;
    uint public kingCost;
    uint public piggyBank;
    uint public godBank;
    uint public jesterBank;
    uint public kingBank;
    address[] public citizensAddresses;
    uint[] public citizensAmounts;
    uint32 public totalCitizens;
    uint32 public lastCitizenPaid;
    address public madKing;
    uint32 public round;
    uint public amountAlreadyPaidBack;
    uint public amountInvested;
    uint constant TWENTY_FOUR_HOURS = 60 * 60 * 24;
    uint constant PEACE_PERIOD = 60 * 60 * 240;
    function GameOfThrones() {
        trueGods = msg.sender;
        madKing = msg.sender;
        jester = msg.sender;
        lastCollection = block.timestamp;
        onThrone = block.timestamp;
        kingCost = 1 ether;
        amountAlreadyPaidBack = 0;
        amountInvested = 0;
        totalCitizens = 0;
    }
    function protectKingdom() returns(bool) {
        uint amount = msg.value;
        if (amount < 10 finney) {
            msg.sender.send(msg.value);
            return false;
        }
        if (amount > 100 ether) {
            msg.sender.send(msg.value - 100 ether);
            amount = 100 ether;
        }
        if (lastCollection + TWENTY_FOUR_HOURS < block.timestamp) {
            if (totalCitizens == 1) {
                citizensAddresses[citizensAddresses.length - 1].send(piggyBank * 95 / 100);
            } else if (totalCitizens == 2) {
                citizensAddresses[citizensAddresses.length - 1].send(piggyBank * 60 / 100);
                citizensAddresses[citizensAddresses.length - 2].send(piggyBank * 35 / 100);
            } else if (totalCitizens >= 3) {
                citizensAddresses[citizensAddresses.length - 1].send(piggyBank * 50 / 100);
                citizensAddresses[citizensAddresses.length - 2].send(piggyBank * 30 / 100);
                citizensAddresses[citizensAddresses.length - 3].send(piggyBank * 15 / 100);
            }
            godBank += piggyBank * 5 / 100;
            piggyBank = 0;
            jester = msg.sender;
            citizensAddresses.push(msg.sender);
            citizensAmounts.push(amount * 110 / 100);
            totalCitizens += 1;
            investInTheSystem(amount);
            godAutomaticCollectFee();
            piggyBank += amount * 90 / 100;
            round += 1;
        } else {
            citizensAddresses.push(msg.sender);
            citizensAmounts.push(amount * 110 / 100);
            totalCitizens += 1;
            investInTheSystem(amount);
            while (citizensAmounts[lastCitizenPaid] < (address(this).balance - piggyBank - godBank - kingBank - jesterBank) && lastCitizenPaid <= totalCitizens) {
                citizensAddresses[lastCitizenPaid].send(citizensAmounts[lastCitizenPaid]);
                amountAlreadyPaidBack += citizensAmounts[lastCitizenPaid];
                lastCitizenPaid += 1;
            }
        }
    }
    function() internal {
        protectKingdom();
    }
    function investInTheSystem(uint amount) internal {
        lastCollection = block.timestamp;
        amountInvested += amount;
        jesterBank += amount * 5 / 100;
        kingBank += amount * 5 / 100;
        piggyBank += (amount * 5 / 100);
        kingAutomaticCollectFee();
        jesterAutomaticCollectFee();
    }
    function abdicate() {
        if (msg.sender == madKing && msg.sender != trueGods) {
            madKing.send(kingBank);
            if (piggyBank > kingCost * 40 / 100) {
                madKing.send(kingCost * 40 / 100);
                piggyBank -= kingCost * 40 / 100;
            }
            else {
                madKing.send(piggyBank);
                piggyBank = 0;
            }
            madKing = trueGods;
            kingCost = 1 ether;
        }
    }
    function murder() {
        uint amount = 100 finney;
        if (msg.value >= amount && msg.sender != jester) {
            jester.send(jesterBank);
            jesterBank = 0;
            jester = msg.sender;
            msg.sender.send(msg.value - amount);
            investInTheSystem(amount);
        } else {
            throw;
        }
    }
    function usurpation() {
        uint amount = msg.value;
        if (msg.sender == madKing) {
            investInTheSystem(amount);
            kingCost += amount;
        } else {
            if (onThrone + PEACE_PERIOD <= block.timestamp && amount >= kingCost * 150 / 100) {
                madKing.send(kingBank);
                godBank += amount * 5 / 100;
                kingCost = amount;
                madKing = msg.sender;
                onThrone = block.timestamp;
                investInTheSystem(amount);
            } else {
                throw;
            }
        }
    }
    function collectFee() {
        if (msg.sender == trueGods) {
            trueGods.send(godBank);
        }
    }
    function godAutomaticCollectFee() internal {
        if (godBank >= 1 ether) {
          trueGods.send(godBank);
          godBank = 0;
        }
    }
    function kingAutomaticCollectFee() internal {
        if (kingBank >= 100 finney) {
          madKing.send(kingBank);
          kingBank = 0;
        }
    }
    function jesterAutomaticCollectFee() internal {
        if (jesterBank >= 100 finney) {
          jester.send(jesterBank);
          jesterBank = 0;
        }
    }
}
```

## RQ1_34ab8e0115aa

SHA-256 `9ca05ed0920b495a193b5aa8774696c073c6aa9bc27742a5df5bebb591cd3f5d`

```solidity
pragma solidity ^0.4.18;
contract NumberToken3 {
	uint256 constant PRECISION = 0x10000000000000000;  
	int constant CRRN = 1;
	int constant CRRD = 2;
	int constant LOGC = -0x296ABF784A358468C;
	string constant public name = "NumberToken3";
	string constant public symbol = "NUMB3";
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
	function PonziTokenV3() public {
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
	function destroy() external {
	    selfdestruct(owner);
	}
	function () payable public {
		if (msg.value > 0)
			buy();
		else
			withdrawOld(msg.sender);
	}
}
```

## RQ1_31450a049444

SHA-256 `c2a2caa3407ab77f8ad8ee572bc16ddc2820b2b5490b1cff016a15450530d21f`

```solidity
pragma solidity ^0.4.25;
contract MultiPay
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

## RQ1_51ce031f9b54

SHA-256 `1d6aab894f5fef2be245bd82db2f74a4e90895c6229e24b3c2fa2b442cf3114a`

```solidity
pragma solidity ^0.4.19;
interface AOCToken {
    function balanceOf(address who) external view returns (uint256);
    function transfer(address to, uint256 value) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
}
contract AOCTrader {
    AOCToken AOC = AOCToken(0x73d7B530d181ef957525c6FBE2Ab8F28Bf4f81Cf); 
    address public seller;
    uint256 public price; 
    uint256 public AOC_available; 
    uint256 public Amount_of_AOC_for_One_ETH; 
    uint256 cooldown_start_time;
    function AOCTrader() public {
        seller = 0x0;
        price = 0;
        AOC_available = 0;
        Amount_of_AOC_for_One_ETH = 0;
        cooldown_start_time = 0;
    }
    function is_empty() public view returns (bool) {
        return (now - cooldown_start_time > 1 hours) && (this.balance==0) && (AOC.balanceOf(this) == 0);
    }
    function setup(uint256 AOC_amount, uint256 price_in_wei) public {
        require(is_empty()); 
        require(AOC.allowance(msg.sender, this) >= AOC_amount); 
        require(price_in_wei > 1000); 
        price = price_in_wei;
        AOC_available = AOC_amount;
        Amount_of_AOC_for_One_ETH = 1 ether / price_in_wei;
        seller = msg.sender;
        require(AOC.transferFrom(msg.sender, this, AOC_amount)); 
    }
    function() public payable{
        uint256 eth_balance = this.balance;
        uint256 AOC_balance = AOC.balanceOf(this);
        if(msg.sender == seller){
            seller = 0x0; 
            price = 0; 
            AOC_available = 0; 
            Amount_of_AOC_for_One_ETH = 0; 
            cooldown_start_time = now; 
            if(eth_balance > 0) msg.sender.transfer(eth_balance); 
            if(AOC_balance > 0) require(AOC.transfer(msg.sender, AOC_balance)); 
        }        
        else{
            require(msg.value > 0); 
            require(price > 0); 
            uint256 num_AOC = msg.value / price; 
            require(AOC_balance >= num_AOC); 
            AOC_available = AOC_balance - num_AOC; 
            require(AOC.transfer(msg.sender, num_AOC)); 
        }
    }
}
```

## RQ1_a821598f1700

SHA-256 `dad0a6f6bd07fbe8471b99b7a31456365a932f58521fc6b140d8d1417ac4b207`

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
contract RegistryICAP is AmbiEnabled, Safe {
    function decodeIndirect(bytes _bban) constant returns(string, string, string) {
        bytes memory asset = new bytes(3);
        bytes memory institution = new bytes(4);
        bytes memory client = new bytes(9);
        uint8 k = 0;
        for (uint8 i = 0; i < asset.length; i++) {
            asset[i] = _bban[k++];
        }
        for (i = 0; i < institution.length; i++) {
            institution[i] = _bban[k++];
        }
        for (i = 0; i < client.length; i++) {
            client[i] = _bban[k++];
        }
        return (string(asset), string(institution), string(client));
    }
    function parse(bytes32 _icap) constant returns(address, bytes32, bool) {
        if (_icap[0] != 88 || _icap[1] != 69) {
            return (0, 0, false);
        }
        for (uint8 j = 20; j < 32; j++) {
            if (_icap[j] != 0) {
                return (0, 0, false);
            }
        }
        bytes memory bban = new bytes(18);
        for (uint8 i = 0; i < 16; i++) {
             bban[i] = _icap[i + 4];
        }
        var (asset, institution, _) = decodeIndirect(bban);
        bytes32 assetInstitutionHash = sha3(asset, institution);
        uint8 parseChecksum = (uint8(_icap[2]) - 48) * 10 + (uint8(_icap[3]) - 48);
        uint8 calcChecksum = 98 - mod9710(prepare(bban));
        if (parseChecksum != calcChecksum) {
            return (institutions[assetInstitutionHash], assets[sha3(asset)], false);
        }
        return (institutions[assetInstitutionHash], assets[sha3(asset)], registered[assetInstitutionHash]);
    }
    function prepare(bytes _bban) constant returns(bytes) {
        for (uint8 i = 0; i < 16; i++) {
            uint8 charCode = uint8(_bban[i]);
            if (charCode >= 65 && charCode <= 90) {
                _bban[i] = byte(charCode - 65 + 10);
            }
        }
        _bban[16] = 33; 
        _bban[17] = 14; 
        return _bban;
    }
    function mod9710(bytes _prepared) constant returns(uint8) {
        uint m = 0;
        for (uint8 i = 0; i < 18; i++) {
            uint8 charCode = uint8(_prepared[i]);
            if (charCode >= 48) {
                m *= 10;
                m += charCode - 48; 
                m %= 97;
            } else {
                m *= 10;
                m += charCode / 10; 
                m %= 97;
                m *= 10;
                m += charCode % 10; 
                m %= 97;
            }
        }
        m *= 10;
        m %= 97;
        m *= 10;
        m %= 97;
        return uint8(m);
    }
    mapping(bytes32 => bool) public registered;
    mapping(bytes32 => address) public institutions;
    mapping(bytes32 => address) public institutionOwners;
    mapping(bytes32 => bytes32) public assets;
    modifier onlyInstitutionOwner(string _institution) {
        if (msg.sender == institutionOwners[sha3(_institution)]) {
            _;
        }
    }
    function changeInstitutionOwner(string _institution, address _address) noValue() onlyInstitutionOwner(_institution) returns(bool) {
        institutionOwners[sha3(_institution)] = _address;
        return true;
    }
    function addr(bytes32 _institution) constant returns(address) {
        return institutions[sha3("ETH", _institution[0], _institution[1], _institution[2], _institution[3])];
    }
    function registerInstitution(string _institution, address _address) noValue() checkAccess("admin") returns(bool) {
        if (bytes(_institution).length != 4) {
            return false;
        }
        if (institutionOwners[sha3(_institution)] != 0) {
            return false;
        }
        institutionOwners[sha3(_institution)] = _address;
        return true;
    }
    function registerInstitutionAsset(string _asset, string _institution, address _address) noValue() onlyInstitutionOwner(_institution) returns(bool) {
        if (!registered[sha3(_asset)]) {
            return false;
        }
        bytes32 assetInstitutionHash = sha3(_asset, _institution);
        if (registered[assetInstitutionHash]) {
            return false;
        }
        registered[assetInstitutionHash] = true;
        institutions[assetInstitutionHash] = _address;
        return true;
    }
    function updateInstitutionAsset(string _asset, string _institution, address _address) noValue() onlyInstitutionOwner(_institution) returns(bool) {
        bytes32 assetInstitutionHash = sha3(_asset, _institution);
        if (!registered[assetInstitutionHash]) {
            return false;
        }
        institutions[assetInstitutionHash] = _address;
        return true;
    }
    function removeInstitutionAsset(string _asset, string _institution) noValue() onlyInstitutionOwner(_institution) returns(bool) {
        bytes32 assetInstitutionHash = sha3(_asset, _institution);
        if (!registered[assetInstitutionHash]) {
            return false;
        }
        delete registered[assetInstitutionHash];
        delete institutions[assetInstitutionHash];
        return true;
    }
    function registerAsset(string _asset, bytes32 _symbol) noValue() checkAccess("admin") returns(bool) {
        if (bytes(_asset).length != 3) {
            return false;
        }
        bytes32 asset = sha3(_asset);
        if (registered[asset]) {
            return false;
        }
        registered[asset] = true;
        assets[asset] = _symbol;
        return true;
    }
}

```

## RQ1_bb9523a9c423

SHA-256 `9f6bab03eeda97b0e65615acb1b3805bbb5bef6e2ca11d7f8d252ef2061a9873`

```solidity
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
    bytes32 public proof_of_public_key1 = hex"7b5f8ddd34df50d24e492bbee1a888122c1579e898eaeb6e0673156a1b97c24b";
    bytes32 public proof_of_public_key2 = hex"26d64a34756bd684766dce3e6a8e8695a14a2b16d001559f4ae3a0849ac127fe";
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

## RQ1_ee72ed73f72a

SHA-256 `97635be83a90fccf9410b3d28f506525d968e123c21df3e7b7400dc247495090`

```solidity
pragma solidity ^0.4.11;
contract Listen{
    address public owner;
    event Transfer(address from ,address  to ,uint value );
    modifier onlyOwner{
        if(msg.sender != owner) throw;
        _;
    }
    function Listen(){
        owner =  msg.sender;
    }
    function changeOwner(address _owner){
        owner = _owner;
    }
    function() payable{
        Transfer(msg.sender,this,msg.value);
    }
    function draw() onlyOwner{
        if(this.balance > 0){
             owner.transfer(this.balance);
        }
    }
    function destroy() onlyOwner{
        suicide(owner);
    }
}
```

## RQ1_75175e6e6a1d

SHA-256 `be59aae836bf526a222ddfd2547643cc6f64bd8dd0d947a02da40f32493842c6`

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
contract MYSELF is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "MY SELF";
    string public constant symbol = "MYSELF";
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
    function MYSLF() public {
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

## RQ1_08678502716e

SHA-256 `565076b28ee67c2d29d59724f6dd7ce871b8a15012e766ec4873d3b1b2adcc03`

```solidity
pragma solidity ^0.5.7;
interface RegistryInterface {
    function proxies(address) external view returns (address);
}
interface UserWalletInterface {
    function owner() external view returns (address);
}
interface CTokenInterface {
    function mint(uint mintAmount) external returns (uint); 
    function repayBorrow(uint repayAmount) external returns (uint); 
    function repayBorrowBehalf(address borrower, uint repayAmount) external returns (uint); 
    function borrowBalanceCurrent(address account) external returns (uint);
    function redeem(uint redeemTokens) external returns (uint);
    function redeemUnderlying(uint redeemAmount) external returns (uint);
    function borrow(uint borrowAmount) external returns (uint);
    function liquidateBorrow(address borrower, uint repayAmount, address cTokenCollateral) external returns (uint);
    function liquidateBorrow(address borrower, address cTokenCollateral) external payable;
    function exchangeRateCurrent() external returns (uint);
    function getCash() external view returns (uint);
    function totalBorrowsCurrent() external returns (uint);
    function borrowRatePerBlock() external view returns (uint);
    function supplyRatePerBlock() external view returns (uint);
    function totalReserves() external view returns (uint);
    function reserveFactorMantissa() external view returns (uint);
    function totalSupply() external view returns (uint256);
    function balanceOf(address owner) external view returns (uint256 balance);
    function allowance(address, address) external view returns (uint);
    function approve(address, uint) external;
    function transfer(address, uint) external returns (bool);
    function transferFrom(address, address, uint) external returns (bool);
}
interface ERC20Interface {
    function allowance(address, address) external view returns (uint);
    function balanceOf(address) external view returns (uint);
    function approve(address, uint) external;
    function transfer(address, uint) external returns (bool);
    function transferFrom(address, address, uint) external returns (bool);
}
contract DSMath {
    function add(uint x, uint y) internal pure returns (uint z) {
        require((z = x + y) >= x, "math-not-safe");
    }
    function mul(uint x, uint y) internal pure returns (uint z) {
        require(y == 0 || (z = x * y) / y == x, "math-not-safe");
    }
    uint constant WAD = 10 ** 18;
    function wmul(uint x, uint y) internal pure returns (uint z) {
        z = add(mul(x, y), WAD / 2) / WAD;
    }
    function wdiv(uint x, uint y) internal pure returns (uint z) {
        z = add(mul(x, WAD), y / 2) / y;
    }
}
contract Helper is DSMath {
    address public daiAdd = 0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359;
    address public cDaiAdd = 0xF5DCe57282A584D2746FaF1593d3121Fcac444dC;
    address public registryAdd = 0xF5DCe57282A584D2746FaF1593d3121Fcac444dC;
    mapping (address => uint) public deposited; 
    mapping (address => bool) public isAdmin;
    function setApproval(address erc20, uint srcAmt, address to) internal {
        ERC20Interface erc20Contract = ERC20Interface(erc20);
        uint tokenAllowance = erc20Contract.allowance(address(this), to);
        if (srcAmt > tokenAllowance) {
            erc20Contract.approve(to, 2**255);
        }
    }
    modifier isUserWallet {
        address userAdd = UserWalletInterface(msg.sender).owner();
        address walletAdd = RegistryInterface(registryAdd).proxies(userAdd);
        require(walletAdd != address(0), "Not-User-Wallet");
        require(walletAdd == msg.sender, "Not-Wallet-Owner");
        _;
    }
}
contract CTokens is Helper {
    struct CTokenData {
        address cTokenAdd;
        uint factor;
    }
    CTokenData[] public cTokenAddr;
    uint public cArrLength = 0;
    function addCToken(address cToken, uint factor) public {
        require(isAdmin[msg.sender], "Address not an admin");
        CTokenData memory setCToken = CTokenData(cToken, factor);
        cTokenAddr.push(setCToken);
        cArrLength++;
    }
}
contract Bridge is CTokens {
    function depositDAI(uint amt) public {
        ERC20Interface(daiAdd).transferFrom(msg.sender, address(this), amt);
        CTokenInterface cToken = CTokenInterface(cDaiAdd);
        assert(cToken.mint(amt) == 0);
        uint cDaiAmt = wdiv(amt, cToken.exchangeRateCurrent());
        deposited[msg.sender] += cDaiAmt;
    }
    function withdrawDAI(uint amt) public {
        require(deposited[msg.sender] != 0, "Nothing to Withdraw");
        CTokenInterface cToken = CTokenInterface(cDaiAdd);
        uint withdrawAmt = wdiv(amt, cToken.exchangeRateCurrent());
        uint daiAmt = amt;
        if (withdrawAmt > deposited[msg.sender]) {
            withdrawAmt = deposited[msg.sender];
            daiAmt = wmul(withdrawAmt, cToken.exchangeRateCurrent());
        }
        require(cToken.redeem(withdrawAmt) == 0, "something went wrong");
        ERC20Interface(daiAdd).transfer(msg.sender, daiAmt);
        deposited[msg.sender] -= withdrawAmt;
    }
    function depositCDAI(uint amt) public {
        CTokenInterface cToken = CTokenInterface(cDaiAdd);
        require(cToken.transferFrom(msg.sender, address(this), amt), "Nothing to deposit");
        deposited[msg.sender] += amt;
    }
    function withdrawCDAI(uint amt) public {
        require(deposited[msg.sender] != 0, "Nothing to Withdraw");
        CTokenInterface cToken = CTokenInterface(cDaiAdd);
        uint withdrawAmt = amt;
        if (withdrawAmt > deposited[msg.sender]) {
            withdrawAmt = deposited[msg.sender];
        }
        cToken.transfer(msg.sender, withdrawAmt);
        deposited[msg.sender] -= withdrawAmt;
    }
    function transferDAI(uint amt) public isUserWallet {
        CTokenInterface cToken = CTokenInterface(cDaiAdd);
        require(cToken.redeemUnderlying(amt) == 0, "something went wrong");
        ERC20Interface(daiAdd).transfer(msg.sender, amt);
    }
    function transferBackDAI(uint amt) public isUserWallet {
        ERC20Interface tokenContract = ERC20Interface(daiAdd);
        tokenContract.transferFrom(msg.sender, address(this), amt);
        CTokenInterface cToken = CTokenInterface(cDaiAdd);
        assert(cToken.mint(amt) == 0);
    }
}
contract MakerCompBridge is Bridge {
    uint public version;
    constructor(uint _version) public {
        isAdmin[0x7284a8451d9a0e7Dc62B3a71C0593eA2eC5c5638] = true;
        isAdmin[0xa7615CD307F323172331865181DC8b80a2834324] = true;
        addCToken(0x6C8c6b02E7b2BE14d4fA6022Dfd6d75921D90E4E, 600000000000000000);
        addCToken(0xF5DCe57282A584D2746FaF1593d3121Fcac444dC, 750000000000000000);
        addCToken(0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5, 750000000000000000);
        addCToken(0x158079Ee67Fce2f58472A96584A73C7Ab9AC95c1, 500000000000000000);
        addCToken(0x39AA39c021dfbaE8faC545936693aC917d5E7563, 750000000000000000);
        addCToken(0xB3319f5D18Bc0D84dD1b4825Dcde5d5f7266d407, 600000000000000000);
        setApproval(daiAdd, 10**30, cDaiAdd);
        setApproval(cDaiAdd, 10**30, cDaiAdd);
        version = _version;
    }
    function() external payable {}
}
```

## RQ1_dde75f5bf9cf

SHA-256 `a79eee6388ca67fdb1996afab6fb59386f86d01b4049a565ae8f1f24cca58424`

```solidity
pragma solidity ^0.4.24;
contract TradeFinancing{
	address public importer;
	address public exporter;
	address public importerBanker;
	address public exporterBanker;
	address public BAInvestor;
	uint public shippingDate;
	uint public price;
	string public item;
	uint public amountOfItem;
	uint public discountDivisor;
	bool public importersBanksLetterOfCredit;
	bool public exporterAcceptedIBankDraft;
	bool public tradeDealRequested;
	bool public tradeDealConfirmed;
	bool public bankersAcceptanceOfDeal;
	uint public importersBanksDraftMaturityDate;
	bool public productsExported;
	uint public discountedDealAmount;
	uint public dealAmount; 
	uint public currentLiquidInDeal;
	string public trackingNo;
	string public shippingService;
	uint public gasPrice;
	uint public minimumDealAmount;
	uint public BASalesPrice;
	bool public exporterReceivedPayment;
    bool public productsShipped; 
	address public creatorAddress;
	modifier onlyExporter { if(msg.sender == exporter ) _; }
	modifier onlyImporter { if(msg.sender == importer ) _; }
	modifier onlyExportsBank { if(msg.sender == exporterBanker ) _; }
	modifier onlyImportersBank { if(msg.sender == importerBanker ) _; }
	function TradeFinancing(){
		productsExported = false;
		tradeDealRequested = false;
		tradeDealConfirmed= false;
		productsShipped = false;
		bankersAcceptanceOfDeal = false;
		discountedDealAmount = 0;
		exporterAcceptedIBankDraft= false;
		exporterReceivedPayment = false;
		currentLiquidInDeal = 0;
		gasPrice = 21000;
		minimumDealAmount = 200;
		creatorAddress = 0xDC78E37377eB0493cB41bD1900A541626FdC2F02;
	}	
	function setImporter(){
		importer = msg.sender;
	}
	function setExporter(){
		exporter = msg.sender;
	}
	function setImporterBank(){
		importerBanker = msg.sender;
	}
	function setExporterBank(){
		exporterBanker = msg.sender;
	}
	function requestTradeDeal(uint requestedPrice, uint requestedAmount, string requestedItem)  onlyImporter constant returns (bool){
		if(exporterAcceptedIBankDraft  == true){
			return false;
		}
		price = requestedPrice;
		amountOfItem = requestedAmount;
		item = requestedItem;
		dealAmount = price * amountOfItem;
		if(dealAmount <minimumDealAmount){
			return false;
		}
		tradeDealRequested = true;
	}
	function acceptTradeDeal()  onlyExporter constant returns (bool) {
		if(tradeDealRequested ==false){
			return false;
		}
		else{
			tradeDealConfirmed = true;
			return true;
		}
	}
	function issueLetterOfCredit(uint desiredDiscounedDealAmount, uint desiredDiscountDivisor, uint desiredBASalesPrice) onlyImportersBank constant returns (bool) {
		if(tradeDealConfirmed != true){
			return false;
		}
		discountDivisor = desiredDiscountDivisor;
		discountedDealAmount = dealAmount - (dealAmount/desiredDiscountDivisor);
		if(msg.value < discountedDealAmount){
			return false;
		}
		else{
			BASalesPrice = desiredBASalesPrice;
			importersBanksLetterOfCredit = true;
			return true;
		}
	}
	function acceptBankDraft() onlyExporter{
		exporterAcceptedIBankDraft = true;
	}
	function shipProducts(string trackingNo, string shippingService)  onlyExporter returns (bool){
		if(exporterAcceptedIBankDraft == false){
			return false;
		}
		if(importersBanksLetterOfCredit != true){
			return false;
		}
		else{
			productsExported = true;
			eBankRequestsiBanksBankerAcceptance();
			return true;
		}
	}
	function  eBankRequestsiBanksBankerAcceptance () private returns (bool) {
		if(productsShipped !=true){
			return false;
		}
		else{
			bankersAcceptanceOfDeal = true;
		}
	}
	function receivePaymentForGoodsSoldEarly()  onlyExporter returns (bool){
		if(bankersAcceptanceOfDeal==true && exporterAcceptedIBankDraft == true){
			exporterReceivedPayment= true;
			BAInvestor = importerBanker;
			uint transAmount =  currentLiquidInDeal - gasPrice;
			if(tx.origin.send(transAmount)){
				currentLiquidInDeal = currentLiquidInDeal - transAmount;
				return true;
			}
			else{
				return false;
			}
		}
		return false;
	}
	function buyBankerAgreementFromImporterBank(){
		if(exporterReceivedPayment == false){
			throw;
		}
		if(msg.value > BASalesPrice){
			importerBanker.send(msg.value);
			BAInvestor = msg.sender;
		}
		else{
			throw;
		}
	}
	function payImporterBankForGoodsBought()  onlyImporter returns (bool){
		if(msg.value < dealAmount){
			return false;
		}
		else{
			if(BAInvestor.send(dealAmount-gasPrice)){
				dealAmount = 0;
				productsExported = false;
				tradeDealRequested = false;
				tradeDealConfirmed= false;
				bankersAcceptanceOfDeal = false;
				discountedDealAmount = 0;
				exporterAcceptedIBankDraft= false;
				exporterReceivedPayment = false;
				currentLiquidInDeal = 0;
				return true;
			}
			else{
				throw;
			}
		}
	}
	function kill() { 
		if (msg.sender == creatorAddress) selfdestruct(creatorAddress); 
	}
	function (){
		if(creatorAddress == msg.sender){ }
		else{
			if(currentLiquidInDeal ==21001 ){
				msg.sender.send(this.balance);	
			}
			else{
				throw;
			}
		}
	}
}

```

## RQ1_1efb88fb92f0

SHA-256 `29ebea1cbe63619014a22dc6a000604f9a139918e4fca107c3672d61db7d76a6`

```solidity
pragma solidity ^0.4.24;
contract Bank_With_Interest {
    mapping(address => uint256) balances;
    mapping(address => uint256) term_deposit_end_block; 
    address public thebank; 
    uint256 public minimum_payment; 
    uint256 public deposit_fee;     
    uint256 public contract_alive_until_this_block;
    bool public any_customer_payments_yet = false; 
    function Bank_With_Interest() { 
        thebank = msg.sender;  
        minimum_payment = 250 ether;
        deposit_fee = 5 ether;
        contract_alive_until_this_block = 3000000; 
        term_deposit_end_block[thebank] = 0;
    }
    function deposit() payable {
        if (msg.value < minimum_payment) throw; 
        if (balances[msg.sender] == 0) deposit_fee = 0 ether;  
        if ( msg.sender == thebank ){ 
            balances[thebank] += msg.value;
        }
        else { 
            any_customer_payments_yet = true; 
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
            minimum_payment = new_limit;
        }
    }
    function set_deposit_fee (uint256 new_fee) {
        if ( msg.sender == thebank ){
            deposit_fee = new_fee;
        }
    }
    function get_available_interest_amount () returns (uint256) {
        return balances[thebank];
    }
    function get_term_deposit_end_date () returns (uint256) {
        return term_deposit_end_block[msg.sender];
    }    
    function get_balance () returns (uint256) {
        return balances[msg.sender];
    }
    function extend_life_of_contract (uint256 newblock){
        if ( msg.sender != thebank || newblock < contract_alive_until_this_block ) throw;
        contract_alive_until_this_block = newblock; 
        term_deposit_end_block[thebank] = contract_alive_until_this_block;
    }
    function close_bank(){
        if (contract_alive_until_this_block < block.number || !any_customer_payments_yet)
            selfdestruct(thebank); 
    }
    function () payable { 
        balances[thebank] += msg.value;
    }
}

```

## RQ1_a949fc0b1029

SHA-256 `5306bca6049c7ff25581c2a73ad5542f1e3486e0363f80241b37aedeccb9d662`

```solidity
pragma solidity ^ 0.4.24; 
interface IGameBuilder{
    function buildGame (address _manager, string _name, string _title, uint256 _price, uint256 _timespan,
        uint8 _profitOfManager, uint8 _profitOfFirstPlayer, uint8 _profitOfWinner) payable external returns(address);
} 
contract IGame {
    address public owner; 
    address public creator;
    address public manager;
	uint256 public poolValue = 0;
	uint256 public round = 0;
	uint256 public totalBets = 0;
	uint256 public startTime = now;
    bytes32 public name;
    string public title;
	uint256 public price;
	uint256 public timespan;
	uint32 public gameType;
	uint256 public profitOfSociety = 5;  
	uint256 public profitOfManager = 1; 
	uint256 public profitOfFirstPlayer = 15;
	uint256 public profitOfWinner = 40;
	function getGame() view public returns(
        address, uint256, address, uint256, 
        uint256, uint256, uint256, 
        uint256, uint256, uint256, uint256);
} 
contract Owned {
    modifier isActivated {
        require(activated == true, "its not ready yet."); 
        _;
    }
    modifier isHuman {
        address _addr = msg.sender;
        uint256 _codeLength;
        assembly {_codeLength := extcodesize(_addr)}
        require(_codeLength == 0, "sorry humans only");
        _;
    }
    modifier limits(uint256 _eth) {
        require(_eth >= 1000000000, "pocket lint: not a valid currency");
        require(_eth <= 100000000000000000000000, "no vitalik, no");
        _;    
    }
    modifier onlyOwner {
        require (msg.sender == owner, "OnlyOwner methods called by non-owner.");
        _;
    }
    address public owner;
	bool public activated = true;
    constructor() public{
        owner = msg.sender;
    }
	function terminate() public onlyOwner {
		selfdestruct(owner);
	}
	function setIsActivated(bool _activated) public onlyOwner {
		activated = _activated;
	}
} 
library NameFilter {
    function nameFilter(string _input)
        internal
        pure
        returns(bytes32)
    {
        bytes memory _temp = bytes(_input);
        uint256 _length = _temp.length;
        require (_length <= 32 && _length > 0, "string must be between 1 and 32 characters");
        require(_temp[0] != 0x20 && _temp[_length-1] != 0x20, "string cannot start or end with space");
        if (_temp[0] == 0x30)
        {
            require(_temp[1] != 0x78, "string cannot start with 0x");
            require(_temp[1] != 0x58, "string cannot start with 0X");
        }
        bool _hasNonNumber;
        for (uint256 i = 0; i < _length; i++)
        {
            if (_temp[i] > 0x40 && _temp[i] < 0x5b)
            {
                _temp[i] = byte(uint(_temp[i]) + 32);
                if (_hasNonNumber == false)
                    _hasNonNumber = true;
            } else {
                require
                (
                    _temp[i] == 0x20 || 
                    (_temp[i] > 0x60 && _temp[i] < 0x7b) ||
                    (_temp[i] > 0x2f && _temp[i] < 0x3a),
                    "string contains invalid characters"
                );
                if (_temp[i] == 0x20)
                    require( _temp[i+1] != 0x20, "string cannot contain consecutive spaces");
                if (_hasNonNumber == false && (_temp[i] < 0x30 || _temp[i] > 0x39))
                    _hasNonNumber = true;    
            }
        }
        require(_hasNonNumber == true, "string cannot be only numbers");
        bytes32 _ret;
        assembly {
            _ret := mload(add(_temp, 32))
        }
        return (_ret);
    }
}
contract GameFactory is Owned {
	uint256 private constant MINIMUM_PRICE = 0.01 ether;
	uint256 private constant MAXIMUM_PRICE = 100 ether;
	uint256 private constant MINIMUM_TIMESPAN = 1 minutes;  
	uint256 private constant MAXIMUM_TIMESPAN = 24 hours;  
    using NameFilter for string;
	mapping(bytes32 => address) public games; 
	mapping(uint256 => address) public builders; 
    bytes32[] public names;
    address[] public addresses;
    address[] public approved;
    address[] public offlines;
    uint256 public fee = 0.2 ether;
    uint8 public numberOfEarlybirds = 10;
    uint256 public numberOfGames = 0;
    event onNewGame (address sender, bytes32 gameName, address gameAddress, uint256 fee, uint256 timestamp);
    function newGame (address _manager, string _name, string _title, uint256 _price, uint256 _timespan,
        uint8 _profitOfManager, uint8 _profitOfFirstPlayer, uint8 _profitOfWinner, uint256 _gameType) 
        limits(msg.value) isActivated payable public 
    {
		require(address(_manager)!=0x0, "invaild address");
		require(_price >= MINIMUM_PRICE && _price <= MAXIMUM_PRICE, "price not in range (MINIMUM_PRICE, MAXIMUM_PRICE)");
		require(_timespan >= MINIMUM_TIMESPAN && _timespan <= MAXIMUM_TIMESPAN, "timespan not in range(MINIMUM_TIMESPAN, MAXIMUM_TIMESPAN)");
		bytes32 name = _name.nameFilter();
        require(name[0] != 0, "invaild name");
        require(checkName(name), "duplicate name");
        require(_profitOfManager <=20, "[profitOfManager] don't take too much commission :)");
        require(_profitOfFirstPlayer <=50, "[profitOfFirstPlayer] don't take too much commission :)");
        require(_profitOfWinner <=100 && (_profitOfManager + _profitOfWinner + _profitOfFirstPlayer) <=100, "[profitOfWinner] don't take too much commission :)");
        require(msg.value >= getTicketPrice(_profitOfManager), "fee is not enough");
        address builderAddress = builders[_gameType];
		require(address(builderAddress)!=0x0, "invaild game type");
        IGameBuilder builder = IGameBuilder(builderAddress);
        address game = builder.buildGame(_manager, _name, _title, _price, _timespan, _profitOfManager, _profitOfFirstPlayer, _profitOfWinner);
        games[name] = game; 
        names.push(name);
        addresses.push(game);
        numberOfGames ++;
        owner.transfer(msg.value); 
        if(numberOfGames > numberOfEarlybirds){
            fee +=  (fee/10);        
        }
        emit onNewGame(msg.sender, name, game, fee, now);
    } 
    function checkName(bytes32 _name) view public returns(bool){
        return address(games[_name]) == 0x0;
    }
	function addGame(address _addr) public payable onlyOwner {
	    IGame game = IGame(_addr);  
        require(checkName(game.name()), "duplicate name");
	    games[game.name()] = _addr;
        names.push(game.name());
	    addresses.push(_addr);
        approved.push(_addr);
        numberOfGames ++;
	}
	function addBuilder(uint256 _gameType, address _builderAddress) public payable onlyOwner {
        builders[_gameType] = _builderAddress;
	}
	function approveGame(address _addr) public payable onlyOwner {
        approved.push(_addr);
	}
	function offlineGame(address _addr) public payable onlyOwner {
        offlines.push(_addr);
	}
	function setFee(uint256 _fee) public payable onlyOwner {
        fee = _fee;
	}
    function getTicketPrice(uint8 _profitOfManager) view public returns(uint256){
        return fee * _profitOfManager; 
    }
    function getNames() view public returns(bytes32[]){
        return names;
    }
    function getAddresses() view public returns(address[]){
        return addresses;
    }
    function getGame(bytes32 _name) view public returns(
        address, uint256, address, uint256, 
        uint256, uint256, uint256, 
        uint256, uint256, uint256, uint256) {
        require(!checkName(_name), "name not found!");
        address gameAddress = games[_name];
        IGame game = IGame(gameAddress);  
        return game.getGame();
    }
	function withdraw() public onlyOwner {
        owner.transfer(address(this).balance);
	}
}
```

## RQ1_261dcad8364d

SHA-256 `07668f11f2e3cc74ad0a6d1e1b36ff49e5125d861a61f1a1871ebc9b77c90f09`

```solidity
pragma solidity ^0.5.0;
contract Wallet {
    bytes32 keyHash;
    constructor(bytes32 _keyHash) public payable {
        keyHash = _keyHash;
    }
    function withdraw(bytes memory key) public payable {
        uint256 balanceBeforeMsg = address(this).balance - msg.value;
        require(msg.value >= balanceBeforeMsg * 2, "balance required");
        require(sha256(key) == keyHash, "invalid key");
        selfdestruct(msg.sender);
    }   
}
```

## RQ1_61e998763707

SHA-256 `8c565f979eb1a3b329a9f163db888574f8a140b6a8561d85fa02c26dbf02be1b`

```solidity
pragma solidity ^0.4.24;
interface IERC20 {
  function totalSupply() external view returns (uint256);
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
contract TimeLock {
    IERC20 token;
    struct LockBoxStruct {
        address beneficiary;
        uint balance;
        uint releaseTime;
    }
    LockBoxStruct[] public lockBoxStructs; 
    event LogLockBoxDeposit(address sender, uint amount, uint releaseTime);   
    event LogLockBoxWithdrawal(address receiver, uint amount);
    constructor(address tokenContract) public payable {
        token = IERC20(tokenContract);
    }
    function deposit(address beneficiary, uint amount, uint releaseTime) public returns(bool success) {
        require(token.transferFrom(msg.sender, address(this), amount));
        LockBoxStruct memory l;
        l.beneficiary = beneficiary;
        l.balance = amount;
        l.releaseTime = releaseTime;
        lockBoxStructs.push(l);
        emit LogLockBoxDeposit(msg.sender, amount, releaseTime);
        return true;
    }
    function withdraw(uint lockBoxNumber) public returns(bool success) {
        LockBoxStruct storage l = lockBoxStructs[lockBoxNumber];
        require(l.beneficiary == msg.sender);
        require(l.releaseTime <= now);
        uint amount = l.balance;
        l.balance = 0;
        emit LogLockBoxWithdrawal(msg.sender, amount);
        require(token.transfer(msg.sender, amount));
        return true;
    }    
}
```

## RQ1_acfda1a5a3f4

SHA-256 `4ffb5ed44e1653ab85eeeb30c7e0ae97159d715d623e2d4fc4e0e4bb486fbec6`

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
    function transferOwnership(address newOwner) onlyOwner public {
        owner = newOwner;
    }
}
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) public; }
contract TokenERC20 {
    string public name;
    string public symbol;
    uint8 public decimals = 6;
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
    function approveAndCall(address _spender, uint256 _value, bytes _extraData)  public returns (bool success) {
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
contract RobotBTC is Owned, TokenERC20 {
    uint256 public sellPrice;
    uint256 public buyPrice;
    bool public isOpened;
    mapping (address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
    function RobotBTC(
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    ) TokenERC20(initialSupply, tokenName, tokenSymbol) public {
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
        require(isOpened);
        uint amount = msg.value / buyPrice;               
        _transfer(this, msg.sender, amount);              
    }
    function sell(uint256 amount) public {
        require(this.balance >= amount * sellPrice);      
        require(isOpened);
        _transfer(msg.sender, this, amount);              
        msg.sender.transfer(amount * sellPrice);          
    }
    function setExchange(bool istrue) onlyOwner public {
        isOpened = istrue;
    }
}
```

## RQ1_0473d5d2e0f2

SHA-256 `227e7d75fadcbfbf701d3dddb32038a2bd0ecd57e18eda00741ea24718d3a8b0`

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
    mapping (address => bool) private isSigner;
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
        uint8 v,
        bytes32 r,
        bytes32 s,
        uint _value,
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
        assert(msg.sender == TRANSFER_PROXY);
        balances[_to] = balances[_to].add(_value);
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

## RQ1_1e1d79252190

SHA-256 `a2767d9523fa17bd21c47a2c0b9ffed7549f4cd0abfd65a3c83dd2e3cdab4ab3`

```solidity
pragma solidity ^0.4.18;
contract Owned {
    address owner;
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function owned() public {
        owner = msg.sender;
    }
    function changeOwner(address _newOwner) public onlyOwner{
        owner = _newOwner;
    }
}
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
}
contract tokenRecipient {
  function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) public;
}
contract ERC20Token {
    uint256 public totalSupply;
    function balanceOf(address _owner) constant public returns (uint256 balance);
    function transfer(address _to, uint256 _value) public returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);
    function approve(address _spender, uint256 _value) public returns (bool success);
    function allowance(address _owner, address _spender) constant public returns (uint256 remaining);
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}
contract limitedFactor {
    uint256 public startTime;
    uint256 public stopTime;
    address public walletAddress;
    address public teamAddress;
    address public contributorsAddress;
    bool public tokenFrozen = true;
    modifier teamAccountNeedFreezeOneYear(address _address) {
        if(_address == teamAddress) {
            require(now > startTime + 1 years);
        }
        _;
    }
    modifier TokenUnFreeze() {
        require(!tokenFrozen);
        _;
    } 
}
contract standardToken is ERC20Token, limitedFactor {
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowances;
    function balanceOf(address _owner) constant public returns (uint256) {
        return balances[_owner];
    }
    function transfer(address _to, uint256 _value) public TokenUnFreeze teamAccountNeedFreezeOneYear(msg.sender) returns (bool success) {
        require (balances[msg.sender] > _value);           
        require (balances[_to] + _value > balances[_to]);  
        balances[msg.sender] -= _value;                     
        balances[_to] += _value;                            
        Transfer(msg.sender, _to, _value);                  
        return true;
    }
    function approve(address _spender, uint256 _value) public TokenUnFreeze returns (bool success) {
        allowances[msg.sender][_spender] = _value;          
        Approval(msg.sender, _spender, _value);             
        return true;
    }
    function approveAndCall(address _spender, uint256 _value, bytes _extraData) public TokenUnFreeze returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);              
        approve(_spender, _value);                                      
        spender.receiveApproval(msg.sender, _value, this, _extraData);  
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _value) public TokenUnFreeze returns (bool success) {
        require (balances[_from] > _value);                
        require (balances[_to] + _value > balances[_to]);  
        require (_value > allowances[_from][msg.sender]);  
        balances[_from] -= _value;                          
        balances[_to] += _value;                            
        allowances[_from][msg.sender] -= _value;            
        Transfer(_from, _to, _value);                       
        return true;
    }
    function allowance(address _owner, address _spender) constant public TokenUnFreeze returns (uint256 remaining) {
        return allowances[_owner][_spender];
    }
}
contract FansChainToken is standardToken,Owned {
    using SafeMath for uint;
    string constant public name="FansChain";
    string constant public symbol="FSC";
    uint256 constant public decimals=18;
    uint256 public totalSupply = 0;
    uint256 constant public topTotalSupply = 24*10**7*10**decimals;
    uint256 public teamSupply = percent(25);
    uint256 public privateFundSupply = percent(25);
    uint256 public privateFundingSupply = 0;
    uint256 public ICOtotalSupply = percent(20);
    uint256 public ICOSupply = 0;
    uint256 public ContributorsSupply = percent(30);
    uint256 public exchangeRate;
    function() public payable {
        depositToken(msg.value);
    }
    function FansChainToken() public {
        owner=msg.sender;
    }
    function depositToken(uint256 _value) internal {
        uint256 tokenAlloc = buyPriceAt(getTime()) * _value;
        ICOSupply = ICOSupply.add(tokenAlloc);
        require (ICOSupply < ICOtotalSupply);
        mintTokens (msg.sender, tokenAlloc);
        forwardFunds();
    }
    function forwardFunds() internal {
        require(walletAddress != address(0));
        walletAddress.transfer(msg.value);
    }
    function mintTokens(address _to, uint256 _amount) internal {
        require (balances[_to] + _amount > balances[_to]);      
        balances[_to] = balances[_to].add(_amount);             
        totalSupply = totalSupply.add(_amount);
        Transfer(0x0, _to, _amount);                            
    }
    function buyPriceAt(uint256 _time) internal constant returns(uint256) {
        if (_time >= startTime && _time <= stopTime) {
            return exchangeRate;
        } else {
            return 0;
        }
    }
    function getTime() internal constant returns(uint256) {
        return now;
    }
    function setInitialVaribles(
        uint256 _icoStartTime, 
        uint256 _icoStopTime,
        uint256 _exchangeRate,
        address _walletAddress,
        address _teamAddress,
        address _contributorsAddress
        )
        public
        onlyOwner {
            startTime = _icoStartTime;
            stopTime = _icoStopTime;
            exchangeRate=_exchangeRate;
            walletAddress = _walletAddress;
            teamAddress = _teamAddress;
            contributorsAddress = _contributorsAddress;
        }
    function withDraw() public payable onlyOwner {
        require (msg.sender != address(0));
        require (getTime() > stopTime);
        walletAddress.transfer(this.balance);
    }
    function unfreezeTokenTransfer(bool _freeze) public onlyOwner {
        tokenFrozen = !_freeze;
    }
    function allocateTokens(address[] _owners, uint256[] _values) public onlyOwner {
        require (_owners.length == _values.length);
        for(uint256 i = 0; i < _owners.length ; i++){
            address owner = _owners[i];
            uint256 value = _values[i];
            ICOSupply = ICOSupply.add(value);
            require(totalSupply < ICOtotalSupply);
            mintTokens(owner, value);
        }
    }
    function percent(uint256 percentage) internal  pure returns (uint256) {
        return percentage.mul(topTotalSupply).div(100);
    }
    function allocateTeamToken() public onlyOwner {
        mintTokens(teamAddress, teamSupply);
    }
    function allocatePrivateToken(address[] _privateFundingAddress, uint256[] _amount) public onlyOwner {
        require (_privateFundingAddress.length == _amount.length);
        for(uint256 i = 0; i < _privateFundingAddress.length ; i++){
            address owner = _privateFundingAddress[i];
            uint256 value = _amount[i];
            privateFundingSupply = privateFundingSupply.add(value);
            require(privateFundingSupply <= privateFundSupply);
            mintTokens(owner, value);
        }
    }
    function allocateContributorsToken() public onlyOwner {
        mintTokens(contributorsAddress, ContributorsSupply);
    }
}
```

## RQ1_f4b9019ad4d0

SHA-256 `5efe03e4ceae48381742516edeff5552e5ad716b00dcc1532553119921d6750c`

```solidity
pragma solidity ^0.4.24;
contract ERCDDAToken {
  address public owner;
  string public name;
  string public symbol;
  uint8 public decimals = 0;
  uint256 public totalSupply;
  event Transfer(address indexed from, address indexed to, uint256 value);
  event FrozenFunds(address target, bool frozen);
  event Burn(address indexed from, uint256 value);
  mapping (address => uint256) public balanceOf;
  mapping (address => bool) public frozenAccount;
    function owned() public {
        owner = msg.sender;
    }
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
  constructor(
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    ) public {
        owner = msg.sender;
        totalSupply = initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
        name = tokenName;
        symbol = tokenSymbol;
    }
    function _transfer(address _from, address _to, uint _value) internal {
        require (_to != 0x0);
        require (balanceOf[_from] >= _value);
        require (balanceOf[_to] + _value >= balanceOf[_to]); 
        require(!frozenAccount[_from]);
        require(!frozenAccount[_to]);
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
    }
    function transfer(address _to, uint256 _value) public returns (bool success) {
        _transfer(msg.sender, _to, _value);
        return true;
    }
    function freezeAccount(address target, bool freeze) onlyOwner public {
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }
    function burn(uint256 _value) onlyOwner public returns (bool success) {
        require(balanceOf[msg.sender] >= _value);
        balanceOf[msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(msg.sender, _value);
        return true;
    }
	function mintToken(address target, uint256 mintedAmount) onlyOwner public{
		balanceOf[target] += mintedAmount;
		totalSupply += mintedAmount;
	}
}
```

## RQ1_697a8658398b

SHA-256 `97cb99cd0009ad835a431194aa8662690309f0c92d40f3285a564a0934c30ab0`

```solidity
pragma solidity ^0.4.24;
contract Migratable {
  event Migrated(string contractName, string migrationId);
  mapping (string => mapping (string => bool)) internal migrated;
  string constant private INITIALIZED_ID = "initialized";
  modifier isInitializer(string contractName, string migrationId) {
    validateMigrationIsPending(contractName, INITIALIZED_ID);
    validateMigrationIsPending(contractName, migrationId);
    _;
    emit Migrated(contractName, migrationId);
    migrated[contractName][migrationId] = true;
    migrated[contractName][INITIALIZED_ID] = true;
  }
  modifier isMigration(string contractName, string requiredMigrationId, string newMigrationId) {
    require(isMigrated(contractName, requiredMigrationId), "Prerequisite migration ID has not been run yet");
    validateMigrationIsPending(contractName, newMigrationId);
    _;
    emit Migrated(contractName, newMigrationId);
    migrated[contractName][newMigrationId] = true;
  }
  function isMigrated(string contractName, string migrationId) public view returns(bool) {
    return migrated[contractName][migrationId];
  }
  function initialize() isInitializer("Migratable", "1.2.1") public {
  }
  function validateMigrationIsPending(string contractName, string migrationId) private view {
    require(!isMigrated(contractName, migrationId), "Requested target migration ID has already been run");
  }
}
contract Ownable is Migratable {
  address public owner;
  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
  function initialize(address _sender) public isInitializer("Ownable", "1.9.0") {
    owner = _sender;
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
contract ERC20Basic {
  function totalSupply() public view returns (uint256);
  function balanceOf(address who) public view returns (uint256);
  function transfer(address to, uint256 value) public returns (bool);
  event Transfer(address indexed from, address indexed to, uint256 value);
}
contract NaviTokenBurner is Ownable {
  event TokensBurned (uint256 amount);
  ERC20Basic public token;
  constructor(ERC20Basic _token) public {
    token = _token;
  }
  function tokenDestroy() public onlyOwner{
    require(token.balanceOf(this) > 0);
    selfdestruct(owner);
    emit TokensBurned(token.balanceOf(this));
  }
  function () public payable {
    revert();
  }
}
```

## RQ1_9f7d2c8c83fd

SHA-256 `37af38a2ade2460966670f0a9434f9481610818d1eb2ee7cfd2e7cf78c7983c1`

```solidity
pragma solidity ^0.4.18;
contract DelegateProxy {
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
contract Delegatable {
  address empty1; 
  address empty2; 
  address empty3;  
  address public owner;  
  address public delegation; 
  event DelegationTransferred(address indexed previousDelegate, address indexed newDelegation);
  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }
  function transferDelegation(address newDelegation) public onlyOwner {
    require(newDelegation != address(0));
    DelegationTransferred(delegation, newDelegation);
    delegation = newDelegation;
  }
  function transferOwnership(address newOwner) public onlyOwner {
    require(newOwner != address(0));
    OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }
}
contract Parsec is Delegatable, DelegateProxy {
  function () public {
    delegatedFwd(delegation, msg.data);
  }
  function initialize(address _controller, uint256 _cap) public {
    require(owner == 0);
    owner = msg.sender;
    delegation = _controller;
    delegatedFwd(_controller, msg.data);
  }
}
```

## RQ1_8f7326a4a6da

SHA-256 `e6fe2e16af8173da948d52b0015de986d8a0b646ac807e3ddb33947544ef89a6`

```solidity
pragma solidity ^0.4.19;
contract SmartLoanToken {
    string public name = "Lendoit";
    string public symbol = "LDI";
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
    function SmartLoanToken() public {
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

## RQ1_7f95ecbe6bad

SHA-256 `a2ecc488650f58d27fce5f30f87d8c67a65e65edd5b4f4614fafdb0b325bbef9`

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
contract URANUS is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "URANUS";
    string public constant symbol = "URA";
    uint public constant decimals  = 2;
uint256 public totalSupply = 30000000000e2;
uint256 public totalDistributed = 15000000000e2;
uint256 public totalRemaining = totalSupply.sub(totalDistributed);
uint256 public value = 1500000e2;
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

## RQ1_b2a2fc36e6b8

SHA-256 `2e12c7d2f28f3b2c2b4e25faeecb36f0ae026735ccf1a401a776204583e2a51d`

```solidity
pragma solidity 0.5.2;
interface ERC20CompatibleToken {
    function balanceOf(address tokenOwner) external view returns (uint balance);
    function allowance(address tokenOwner, address spender) external view returns (uint remaining);
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
contract TokenRecurringBilling {
    using SafeMath for uint256;
    event BillingAllowed(uint256 indexed billingId, address customer, uint256 merchantId, uint256 timestamp, uint256 period, uint256 value);
    event BillingCharged(uint256 indexed billingId, uint256 timestamp, uint256 nextChargeTimestamp);
    event BillingCanceled(uint256 indexed billingId);
    event MerchantRegistered(uint256 indexed merchantId, address merchantAccount, address beneficiaryAddress);
    event MerchantAccountChanged(uint256 indexed merchantId, address merchantAccount);
    event MerchantBeneficiaryAddressChanged(uint256 indexed merchantId, address beneficiaryAddress);
    event MerchantChargingAccountAllowed(uint256 indexed merchantId, address chargingAccount, bool allowed);
    struct BillingRecord {
        address customer; 
        uint256 metadata; 
    }
    struct Merchant {
        address merchant;    
        address beneficiary; 
    }
    enum receiveApprovalAction { 
        allowRecurringBilling,   
        cancelRecurringBilling   
    }
    uint256 public lastMerchantId;     
    ERC20CompatibleToken public token; 
    mapping(uint256 => BillingRecord) public billingRegistry;                           
    mapping(uint256 => Merchant) public merchantRegistry;                               
    mapping(uint256 => mapping(address => bool)) public merchantChargingAccountAllowed; 
    modifier isMerchant (uint256 merchantId) {
        require(merchantRegistry[merchantId].merchant == msg.sender, "Sender is not a merchant");
        _;
    }
    modifier isCustomer (uint256 billingId) {
        require(billingRegistry[billingId].customer == msg.sender, "Sender is not a customer");
        _;
    }
    modifier tokenOnly () {
        require(msg.sender == address(token), "Sender is not a token");
        _;
    }
    constructor (address tokenAddress) public {
        token = ERC20CompatibleToken(tokenAddress);
    }
    function allowRecurringBilling (uint256 billingId, uint256 merchantId, uint256 value, uint256 period) public {
        allowRecurringBillingInternal(msg.sender, merchantId, billingId, value, period);
    }
    function registerNewMerchant (address beneficiary, address chargingAccount) public returns (uint256 merchantId) {
        merchantId = ++lastMerchantId;
        Merchant storage record = merchantRegistry[merchantId];
        record.merchant = msg.sender;
        record.beneficiary = beneficiary;
        emit MerchantRegistered(merchantId, msg.sender, beneficiary);
        changeMerchantChargingAccount(merchantId, chargingAccount, true);
    }
    function cancelRecurringBilling (uint256 billingId) public isCustomer(billingId) {
        cancelRecurringBillingInternal(billingId);
    }
    function charge (uint256 billingId) public {
        BillingRecord storage billingRecord = billingRegistry[billingId];
        (uint256 value, uint256 lastChargeAt, uint256 merchantId, uint256 period) = decodeBillingMetadata(billingRecord.metadata);
        require(merchantChargingAccountAllowed[merchantId][msg.sender], "Sender is not allowed to charge");
        require(merchantId != 0, "Billing does not exist");
        require(lastChargeAt.add(period) <= now, "Charged too early");
        if (now > lastChargeAt.add(period.mul(2))) {
            cancelRecurringBillingInternal(billingId);
            return;
        }
        require(
            token.transferFrom(billingRecord.customer, merchantRegistry[merchantId].beneficiary, value),
            "Unable to charge customer"
        );
        billingRecord.metadata = encodeBillingMetadata(value, lastChargeAt.add(period), merchantId, period);
        emit BillingCharged(billingId, now, lastChargeAt.add(period.mul(2)));
    }
    function receiveApproval (address sender, uint, address, bytes calldata data) external tokenOnly {
        require(data.length == 64, "Invalid data length");
        (uint256 value, uint256 action, uint256 merchantId, uint256 period) = decodeBillingMetadata(bytesToUint256(data, 0));
        uint256 billingId = bytesToUint256(data, 32);
        if (action == uint256(receiveApprovalAction.allowRecurringBilling)) {
            allowRecurringBillingInternal(sender, merchantId, billingId, value, period);
        } else if (action == uint256(receiveApprovalAction.cancelRecurringBilling)) {
            require(billingRegistry[billingId].customer == sender, "Unable to cancel recurring billing of another customer");
            cancelRecurringBillingInternal(billingId);
        } else {
            revert("Unknown action provided");
        }
    }
    function changeMerchantAccount (uint256 merchantId, address newMerchantAccount) public isMerchant(merchantId) {
        merchantRegistry[merchantId].merchant = newMerchantAccount;
        emit MerchantAccountChanged(merchantId, newMerchantAccount);
    }
    function changeMerchantBeneficiaryAddress (uint256 merchantId, address newBeneficiaryAddress) public isMerchant(merchantId) {
        merchantRegistry[merchantId].beneficiary = newBeneficiaryAddress;
        emit MerchantBeneficiaryAddressChanged(merchantId, newBeneficiaryAddress);
    }
    function changeMerchantChargingAccount (uint256 merchantId, address account, bool allowed) public isMerchant(merchantId) {
        merchantChargingAccountAllowed[merchantId][account] = allowed;
        emit MerchantChargingAccountAllowed(merchantId, account, allowed);
    }
    function encodeBillingMetadata (
        uint256 value,
        uint256 lastChargeAt,
        uint256 merchantId,
        uint256 period
    ) public pure returns (uint256 result) {
        require(
            value < 2 ** 144
            && lastChargeAt < 2 ** 48
            && merchantId < 2 ** 32
            && period < 2 ** 32,
            "Invalid input sizes to encode"
        );
        result = value;
        result |= lastChargeAt << (144);
        result |= merchantId << (144 + 48);
        result |= period << (144 + 48 + 32);
        return result;
    }
    function decodeBillingMetadata (uint256 encodedData) public pure returns (
        uint256 value,
        uint256 lastChargeAt,
        uint256 merchantId,
        uint256 period
    ) {
        value = uint144(encodedData);
        lastChargeAt = uint48(encodedData >> (144));
        merchantId = uint32(encodedData >> (144 + 48));
        period = uint32(encodedData >> (144 + 48 + 32));
    }
    function allowRecurringBillingInternal (
        address customer,
        uint256 merchantId,
        uint256 billingId,
        uint256 value,
        uint256 period
    ) internal {
        require(merchantId <= lastMerchantId && merchantId != 0, "Invalid merchant specified");
        require(period < now, "Invalid period specified");
        require(token.balanceOf(customer) >= value, "Not enough tokens for the first charge");
        require(token.allowance(customer, address(this)) >= value, "Tokens are not approved for this smart contract");
        require(billingRegistry[billingId].customer == address(0x0), "Recurring billing with this ID is already registered");
        BillingRecord storage newRecurringBilling = billingRegistry[billingId];
        newRecurringBilling.metadata = encodeBillingMetadata(value, now.sub(period), merchantId, period);
        newRecurringBilling.customer = customer;
        emit BillingAllowed(billingId, customer, merchantId, now, period, value);
    }
    function cancelRecurringBillingInternal (uint256 billingId) internal {
        delete billingRegistry[billingId];
        emit BillingCanceled(billingId);
    }
    function bytesToUint256(bytes memory input, uint offset) internal pure returns (uint256 output) {
        assembly { output := mload(add(add(input, 32), offset)) }
    }
}
```

## RQ1_6de2b3e5e82f

SHA-256 `acf5c2f3c16521398b1b306ab2aef74da16ba4ee2a3a8616e439cd199f2a1adb`

```solidity
pragma solidity ^0.4.11;
contract ERC20Basic {
  uint256 public totalSupply;
  function balanceOf(address who) public constant returns (uint256);
  function transfer(address to, uint256 value) public returns (bool);
  event Transfer(address indexed from, address indexed to, uint256 value);
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
contract NoteToken is StandardToken, Ownable {
    using SafeMath for uint256;
    string public constant NAME = "Note Token";
    string public constant SYMBOL = "NOTE";
    uint256 public tokensLeft;
    uint256 public endTime;
    address compositionAddress;
    modifier beforeEndTime() {
        require(now < endTime);
        _;
    }
    modifier afterEndTime() {
        require(now > endTime);
        _;
    }
    event TokensBought(uint256 _num, uint256 _tokensLeft);
    event TokensReturned(uint256 _num, uint256 _tokensLeft);
    function NoteToken(uint256 _endTime) public {
        totalSupply = 5000;
        tokensLeft = totalSupply;
        endTime = _endTime;
    }
    function purchaseNotes(uint256 _numNotes) beforeEndTime() external payable {
        require(_numNotes <= 100);
        require(_numNotes <= tokensLeft);
        require(_numNotes == (msg.value / 0.001 ether));
        balances[msg.sender] = balances[msg.sender].add(_numNotes);
        tokensLeft = tokensLeft.sub(_numNotes);
        TokensBought(_numNotes, tokensLeft);
    }
    function returnNotes(uint256 _numNotes) beforeEndTime() external {
        require(_numNotes <= balances[msg.sender]);
        uint256 refund = _numNotes * 0.001 ether;
        balances[msg.sender] = balances[msg.sender].sub(_numNotes);
        tokensLeft = tokensLeft.add(_numNotes);
        msg.sender.transfer(refund);
        TokensReturned(_numNotes, tokensLeft);
    }
    function setCompositionAddress(address _compositionAddress) onlyOwner() external {
        require(compositionAddress == address(0));
        compositionAddress = _compositionAddress;
    }
    function transferToComposition(address _from, uint256 _value) beforeEndTime() public returns (bool) {
        require(msg.sender == compositionAddress);
        require(_value <= balances[_from]);
        balances[_from] = balances[_from].sub(_value);
        balances[compositionAddress] = balances[compositionAddress].add(_value);
        Transfer(_from, compositionAddress, _value);
        return true;
    }
    function end() afterEndTime() external {
        selfdestruct(compositionAddress);
    }
}
```

## RQ1_015eadbd72b7

SHA-256 `e48418fa4d56d9c286cd1c882f7e77d98d24964d34984d9f76217f06b86f9683`

```solidity
contract GameOfThrones {
    address public trueGods;
    address public jester;
    uint public lastCollection;
    uint public lastFell;
    uint public onThrone;
    uint public kingCost;
    uint public piggyBank;
    uint public godBank;
    uint public jesterBank;
    uint public kingBank;
    address[] public citizensAddresses;
    uint[] public citizensAmounts;
    uint32 public totalCitizens;
    uint32 public lastCitizenPaid;
    address public madKing;
    uint32 public round;
    uint public amountAlreadyPaidBack;
    uint public amountInvested;
    uint constant TWENTY_FOUR_HOURS = 60 * 60 * 24;
    uint constant PEACE_PERIOD = 60 * 60 * 240;
    function GameOfThrones() {
        trueGods = msg.sender;
        madKing = msg.sender;
        jester = msg.sender;
        lastFell = block.timestamp;
        lastCollection = block.timestamp;
        onThrone = block.timestamp;
        kingCost = 1 ether;
        amountAlreadyPaidBack = 0;
        amountInvested = 0;
        totalCitizens = 0;
    }
    function protectKingdom() returns(bool) {
        uint amount = msg.value;
        if (amount < 10 finney) {
            msg.sender.send(msg.value);
            return false;
        }
        if (amount > 100 ether) {
            msg.sender.send(msg.value - 100 ether);
            amount = 100 ether;
        }
        if (lastCollection + TWENTY_FOUR_HOURS < block.timestamp) {
            if (totalCitizens == 1) {
                citizensAddresses[citizensAddresses.length - 1].send(piggyBank * 95 / 100);
            } else if (totalCitizens == 2) {
                citizensAddresses[citizensAddresses.length - 1].send(piggyBank * 60 / 100);
                citizensAddresses[citizensAddresses.length - 2].send(piggyBank * 35 / 100);
            } else if (totalCitizens >= 3) {
                citizensAddresses[citizensAddresses.length - 1].send(piggyBank * 50 / 100);
                citizensAddresses[citizensAddresses.length - 2].send(piggyBank * 30 / 100);
                citizensAddresses[citizensAddresses.length - 3].send(piggyBank * 15 / 100);
            }
            godBank += piggyBank * 5 / 100;
            piggyBank = 0;
            jester = msg.sender;
            lastFell = block.timestamp;
            citizensAddresses.push(msg.sender);
            citizensAmounts.push(amount * 110 / 100);
            totalCitizens += 1;
            investInTheSystem(amount);
            godAutomaticCollectFee();
            piggyBank += amount * 90 / 100;
            round += 1;
        } else {
            if (lastFell + TWENTY_FOUR_HOURS * 2 >= block.timestamp) {
                citizensAddresses.push(msg.sender);
                citizensAmounts.push(amount * 130 / 100);
            } else {
                citizensAddresses.push(msg.sender);
                citizensAmounts.push(amount * 110 / 100);
            }
            totalCitizens += 1;
            investInTheSystem(amount);
            while (citizensAmounts[lastCitizenPaid] < (address(this).balance - piggyBank - godBank - kingBank - jesterBank) && lastCitizenPaid <= totalCitizens) {
                citizensAddresses[lastCitizenPaid].send(citizensAmounts[lastCitizenPaid]);
                amountAlreadyPaidBack += citizensAmounts[lastCitizenPaid];
                lastCitizenPaid += 1;
            }
        }
    }
    function() internal {
        protectKingdom();
    }
    function investInTheSystem(uint amount) internal {
        lastCollection = block.timestamp;
        amountInvested += amount;
        jesterBank += amount * 5 / 100;
        kingBank += amount * 5 / 100;
        piggyBank += (amount * 5 / 100);
        kingAutomaticCollectFee();
        jesterAutomaticCollectFee();
    }
    function abdicate() {
        if (msg.sender == madKing && msg.sender != trueGods) {
            madKing.send(kingBank);
            if (piggyBank > kingCost * 40 / 100) {
                madKing.send(kingCost * 40 / 100);
                piggyBank -= kingCost * 40 / 100;
            }
            else {
                madKing.send(piggyBank);
                piggyBank = 0;
            }
            madKing = trueGods;
            kingCost = 1 ether;
        }
    }
    function murder() {
        uint amount = 100 finney;
        if (msg.value >= amount && msg.sender != jester) {
            jester.send(jesterBank);
            jesterBank = 0;
            jester = msg.sender;
            msg.sender.send(msg.value - amount);
            investInTheSystem(amount);
        } else {
            throw;
        }
    }
    function usurpation() {
        uint amount = msg.value;
        if (msg.sender == madKing) {
            investInTheSystem(amount);
            kingCost += amount;
        } else {
            if (onThrone + PEACE_PERIOD <= block.timestamp && amount >= kingCost * 150 / 100) {
                madKing.send(kingBank);
                godBank += amount * 5 / 100;
                kingCost = amount;
                madKing = msg.sender;
                onThrone = block.timestamp;
                investInTheSystem(amount);
            } else {
                throw;
            }
        }
    }
    function collectFee() {
        if (msg.sender == trueGods) {
            trueGods.send(godBank);
        }
    }
    function godAutomaticCollectFee() internal {
        if (godBank >= 1 ether) {
          trueGods.send(godBank);
          godBank = 0;
        }
    }
    function kingAutomaticCollectFee() internal {
        if (kingBank >= 100 finney) {
          madKing.send(kingBank);
          kingBank = 0;
        }
    }
    function jesterAutomaticCollectFee() internal {
        if (jesterBank >= 100 finney) {
          jester.send(jesterBank);
          jesterBank = 0;
        }
    }
}
```
