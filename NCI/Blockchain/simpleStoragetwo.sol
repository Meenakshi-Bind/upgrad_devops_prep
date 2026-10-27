pragma solidity ^0.5.17;

contract Favorites {
    string Music;
    string Movie;
    string Food;
    string State;

    // Setters
    function setMusic(string memory music) public {
        Music = music;
    }
    function setFood(string memory food) public {
        Food = food;
    }
    function setState(string memory state) public {
        State = state;
    }
    function setMovie(string memory movie) public {
        Movie = movie;
    }

    

    // Getters
    function getMusic() public view returns (string memory) {
        return Music;
    }
    function getFood() public view returns (string memory) {
        return Food;
    }
    function getState() public view returns (string memory) {
        return State;
    }
    function getMovie() public view returns (string memory) {
        return Movie;
    }

   
}