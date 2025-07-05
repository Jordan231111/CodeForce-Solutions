const board = document.getElementById("board");
const ctx = board.getContext("2d");
const square = 20;

const snake = [
  { x: 100, y: 100 },
  { x: 80, y: 100 },
  { x: 60, y: 100 }
];

window.move = { x: square, y: 0 };

let food = {
  x: Math.floor(Math.random() * (board.width / square)) * square,
  y: Math.floor(Math.random() * (board.height / square)) * square
};

let score = 0;

function draw_rect(part) {
// Write your code here(Implemented previously)
}

function draw_snake() {
// Write your code here(Implemented previously)
}

function draw_food() {
  ctx.fillStyle = "red";
  ctx.fillRect(food.x, food.y, square, square);
}

function draw_score() {
  document.getElementById("score").textContent = score;
}

function clear_canvas() {
  ctx.fillStyle = "white";
  ctx.strokeStyle = "black";
  ctx.fillRect(0, 0, board.width, board.height);
  ctx.strokeRect(0, 0, board.width, board.height);
}

function moveSnake() {
  const head = { x: snake[0].x + window.move.x, y: snake[0].y + window.move.y };
  snake.unshift(head);

  if (head.x === food.x && head.y === food.y) {
    score += 1;
    draw_score();
    food = {
      x: Math.floor(Math.random() * (board.width / square)) * square,
      y: Math.floor(Math.random() * (board.height / square)) * square
    };
  } else {
    snake.pop();
  }
}

function checkCollision() {
  const head = window.snake[0];

  // Fix wall collision detection to check all four boundaries
  if (
    head.x < 0 ||
    head.x >= board.width || 
    head.y < 0 ||
    head.y >= board.height
  ) {
    window.gameOver = true;
    showGameOver();
    return;
  }

  // Fix self-collision logic to check both x and y coordinates
  for (let i = 1; i < window.snake.length; i++) {
    if (window.snake[i].x === head.x && window.snake[i].y === head.y) {
      window.gameOver = true;
      showGameOver();
      return;
    }
  }
}

// Show Game Over Text
function showGameOver() {
  if (!ctx) return;
  ctx.fillStyle = "black";
  ctx.font = "40px Arial";
  ctx.textAlign = "center";
  ctx.fillText("Game Over", board.width / 2, board.height / 2);
}
document.addEventListener("keydown", registerMove);

function registerMove(e) {
  const curr = window.move;
  if (e.key === "ArrowUp" && curr.y === 0) window.move = { x: 0, y: -square };
  if (e.key === "ArrowDown" && curr.y === 0) window.move = { x: 0, y: square };
  if (e.key === "ArrowLeft" && curr.x === 0) window.move = { x: -square, y: 0 };
  if (e.key === "ArrowRight" && curr.x === 0) window.move = { x: square, y: 0 };
}

window.gameOver = false;

function main() {
  if (window.gameOver) return;

  setTimeout(() => {
    clear_canvas();
    moveSnake();
    checkCollision(); 
    draw_snake();
    draw_food();
    main();
  }, 150);
}

// Expose for testing
window.snake = snake;
window.moveSnake = moveSnake;
window.clear_canvas = clear_canvas;
window.registerMove = registerMove;
window.checkCollision = checkCollision;
window.board = board;
window.ctx = ctx;
window.main = main;
window.move = window.move;
window.food = food;
window.score = score;

draw_score();
main();