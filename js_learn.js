class Actor {
  constructor(startX, startY) {
    this.x = startX;
    this.y = startY;
  }
  
  move(dx, dy) {
    this.x += dx;
    this.y += dy;
  }

  distanceTo(otherActor) {
    let dx = otherActor.x - this.x;
    let dy = otherActor.y - this.y;
    return Math.hypot(dx, dy);
  }
}




class Player extends Actor {
  constructor(startX, startY) {
    super(startX, startY);
    this.hp = 100;
  }
}




class Enemy extends Actor {
  attack(player) {
    if (this.distanceTo(player) < 4) {
      player.hp -= 10;
      return true;
    } else {
      return false;
    }
  }
}



function Cat(name) {
  this.name = name;
}
Cat.prototype.sayHello = function () {
  console.log(`Miaow! My name is ${this.name}.`);
};


class Dog {
  constructor(name) {
    this.name = name;
  }

  sayHello() {
    console.log(`Woof! My name is ${this.name}.`);
  }
}

kiki.__proto__;



let heading = document.getElementById("main-heading");
heading.innerText;

let strong = document.querySelectorAll("#main-heading strong");
document.querySelector
strong[0].textContent;



heading.addEventListener("click", () => {
  console.log("You clicked the heading!");
});