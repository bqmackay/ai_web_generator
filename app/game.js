// Function to move cursor to the next box when a letter is entered
function moveToNext(input, event) {
  if (event.keyCode >= 65 && event.keyCode <= 90) {
    var nextInput = input.nextElementSibling;
    if (nextInput) {
      nextInput.focus();
    }
  }
}

// Function to move cursor to the previous box and remove character when delete key is pressed
function moveToPrevious(input, event) {
  if (event.keyCode === 8 && input.value === '') {
    var prevInput = input.previousElementSibling;
    if (prevInput) {
      prevInput.focus();
      prevInput.value = '';
    }
  }
}

secret_word = "apple"
let tryCount = 0;

function checkGuess() {
  tryCount++;
  let combinedWord = '';
  const inputs = document.querySelectorAll('.row:last-child input');
  inputs.forEach((input, index) => {
    const letter = input.value.toLowerCase();
    if (letter === secret_word[index]) {
      input.style.border = '2px solid green';
    } else if (secret_word.includes(letter)) {
      input.style.border = '2px solid orange';
    } else {
      input.style.border = '2px solid red';
    }
    combinedWord += letter;
  });

  const messageElement = document.getElementById('message');
  if (combinedWord === secret_word) {
    messageElement.innerText = 'Congratulations! 🎉 You guessed the secret word!';
    document.getElementById('new-row').style.display = 'block';
    // Disable previous row
    document.querySelectorAll('.row:last-child input').forEach(input => {
      input.disabled = true;
    });
  } else {
    if (tryCount === 5) {
      revealSecretWord();
    } else {
      messageElement.innerText = 'Try again! The word is not complete.';
      createNewRow(); // Call function to create a new row
    }
  }
}

function revealSecretWord() {
  const messageElement = document.getElementById('message');
  messageElement.innerText = 'You have exhausted all your tries. The secret word was: ' + secret_word;
}

document.addEventListener('DOMContentLoaded', function() {
  // Event listener for keyup to move cursor to the next box and check completed word on submit
  const submitButton = document.getElementById('submit-button');
  if (submitButton) {
    submitButton.addEventListener('click', checkGuess);
  }
  createNewRow()
});

// Event listener for keydown to automatically capitalize the input value if it is a letter
document.addEventListener('keydown', function(event) {
  const input = document.activeElement;
  if (event.keyCode >= 65 && event.keyCode <= 90) {
    input.value = input.value + String.fromCharCode(event.keyCode).toUpperCase();
    event.preventDefault();
  }
});

// Function to create a new row of input boxes
function createNewRow() {
  const row = document.createElement('div');
  row.classList.add('row');
  for (let i = 0; i < secret_word.length; i++) {
    const input = document.createElement('input');
    input.setAttribute('type', 'text');
    input.setAttribute('maxlength', '1');
    input.addEventListener('keyup', function(event) {
      moveToNext(this, event);
    });
    input.addEventListener('keydown', function(event) {
      moveToPrevious(this, event);
    });
    row.appendChild(input);
  }
  document.getElementById('input-container').appendChild(row);
}
