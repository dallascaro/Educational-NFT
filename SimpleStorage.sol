// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract DegreeDevelopment {
    //variables
    string StudentID; //00481235
    string StudentName; //John Doe
    string DegreeType; // Example: Masters of Science, Bachelors of Science
    string ProgramType; //Comp science
    string SchoolName; // UTPB
    string DateToday; //08/11/2021
    string Location; //location of NFT URI
    uint256 favoriteNumber; //test variable
    //Diplomna Structure
    struct diploma {
        string StudentID;
        string StudentName;
        string DegreeType;
        string ProgramType;
        string SchoolName;
        string DateToday;
        string Location;
    }
    //array build
    diploma[] public Diploma;

    //mapping structure for contract look up
    //mapping(string => int256) public StudentNameLookUp;
    //mapping(uint256 => int256) public StudentIDLookUp;

    //testing function
    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    //adding contracts to public block chain
    function addGraduate(
        string memory _StudentID,
        string memory _StudentName,
        string memory _DegreeType,
        string memory _ProgramType,
        string memory _SchoolName,
        string memory _DateToday,
        string memory _Location
    ) public {
        Diploma.push(
            diploma(
                _StudentID,
                _StudentName,
                _DegreeType,
                _ProgramType,
                _SchoolName,
                _DateToday,
                _Location
            )
        );

        //Mapping values to index number to look up data in array
        //StudentNameLookUp[_StudentName] = int256(Diploma.length) - 1;
        //StudentIDLookUp[_StudentID] = int256(Diploma.length) - 1;
    }
}
