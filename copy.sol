pragma solidity ^0.5.1;

contract MedicalQueue {

    address public owner;
    enum Role {OTHER,RECEPTIONIST,DOCTOR,ADMIN}
    mapping(address => Role) roles;

    modifier onlyByAddress(address _account) {
        require(
            msg.sender == _account,
            "Sender not authorized."
        );
        _;
    }

    modifier onlyByRole(Role _role) {
        require(
            roles[msg.sender] == _role || roles[msg.sender] == Role.ADMIN,
            "Sender not authorized."
        );
        _;
    }

    constructor() public {
        owner = msg.sender;
        roles[owner] = Role.ADMIN;
    }

    function add_doctor(address _account, string memory _name) public onlyByAddress(owner) returns(bool success) {
        roles[_account] = Role.DOCTOR;
        doctorListStruct[_account].nameDoctor = _name;
        doctorListStruct[_account].listPointer = numberDoctors;
        numberDoctors += 1;
        return true;
    }

    function add_receptionist(address _account) public onlyByAddress(owner) returns(bool success) {
        roles[_account] = Role.RECEPTIONIST;
        return true;
    }


    function getDoctor(address _account) public returns(string memory name_) {
        name_ = doctorListStruct[_account].nameDoctor;
    }

    function greet() public returns (string memory greet) {
        greet = "Hello World!";
    }

    struct EntityStruct {
        uint entityData;
        uint queueDoctor;
        uint listPointer;
   }

    struct PatientStruct {
        string namePatient;
        address addressDoctor;
        uint listPointer;
    }

    mapping(uint => PatientStruct) public patientStructs;

    struct DoctorStruct {
        string nameDoctor;
        uint[] patients;
        uint listPointer;
   }

    function newPatient(uint idPatient, address addressDoctor, string memory namePatient) public returns(bool success) {
        patientStructs[idPatient].namePatient = namePatient;
        patientStructs[idPatient].addressDoctor = addressDoctor;
        patientStructs[idPatient].listPointer = doctorListStruct[addressDoctor].patients.push(idPatient) - 1;
        return true;
   }

    function deletePatient(uint idPatient) public returns(bool success) {
        address doctorListToDelete = patientStructs[idPatient].addressDoctor;
        uint patientToDelete = patientStructs[idPatient].listPointer;

        uint last = doctorListStruct[doctorListToDelete].patients.length - 1;
        uint current = patientToDelete;

        while( current < last) {
            doctorListStruct[doctorListToDelete].patients[current] = doctorListStruct[doctorListToDelete].patients[current+1];
            patientStructs[doctorListStruct[doctorListToDelete].patients[current]].listPointer = current;
            current++;
        }
        doctorListStruct[doctorListToDelete].patients.length--;

        delete patientStructs[idPatient];
        return true;
  }

  function deleteFirstPatient(address addressDoctor) public returns(bool success) {
      uint idPatient = doctorListStruct[addressDoctor].patients[0];
      deletePatient(idPatient);
      return true;
  }

    function getPatients(address addressDoctor) public view returns(uint[] memory) {
         return doctorListStruct[addressDoctor].patients;
  }



   mapping(uint => EntityStruct) public entityStructs;
   mapping(address => DoctorStruct) public doctorListStruct;
   uint[][] public entityList;

   uint numberDoctors = 0;

   function isEntity(uint entityAddress) public returns(bool isIndeed) {
        if(entityList.length == 0) return false;
        return (entityList[0][entityStructs[entityAddress].listPointer] == entityAddress);
   }

   function getEntityCount(uint queueDoctor) public returns(uint entityCount) {
        return entityList[queueDoctor].length;
   }

  function newEntity(uint entityAddress, uint queueDoctor, uint entityData) public returns(bool success) {
    // require(isEntity(entityAddress));
    entityStructs[entityAddress].entityData = entityData;
    entityStructs[entityAddress].queueDoctor = queueDoctor;
    entityStructs[entityAddress].listPointer = entityList[queueDoctor].push(entityAddress) - 1;
    return true;
  }

  function updateEntity(uint entityAddress, uint entityData) public returns(bool success) {
    //require(isEntity(entityAddress));
    entityStructs[entityAddress].entityData = entityData;
    return true;
  }

  function deleteEntity(uint entityAddress) public returns(bool success) {
    //require(isEntity(entityAddress));
    uint kolumnToDelete = entityStructs[entityAddress].queueDoctor;
    uint rowToDelete = entityStructs[entityAddress].listPointer;

    uint last = entityList[kolumnToDelete].length;
    uint current = rowToDelete;

    while( current < last) {
        entityList[kolumnToDelete][current] = entityList[kolumnToDelete][current+1];
        entityStructs[entityList[kolumnToDelete][current]].listPointer = current;
    }

    entityList.length--;
    return true;
  }



}