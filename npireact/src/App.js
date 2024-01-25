import "./styles.css"

function App() {
  return (
    <div className="Calculator-grid">
      <div className="output">
        <div className="previous-operand"></div>
        <div className="current-operand"></div>
      </div>

    <button onclick="appendToExpression('1')">1</button>
    <button onclick="appendToExpression('2')">2</button>
    <button onclick="appendToExpression('3')">3</button>

    <button onclick="appendToExpression('4')">4</button>
    <button onclick="appendToExpression('5')">5</button>
    <button onclick="appendToExpression('6')">6</button>

    <button onclick="appendToExpression('7')">7</button>
    <button onclick="appendToExpression('8')">8</button>
    <button onclick="appendToExpression('9')">9</button>

    <button onclick="appendToExpression('+')">+</button>
    <button onclick="appendToExpression('-')">-</button>
    <button onclick="appendToExpression('*')">*</button>
    <button onclick="appendToExpression('/')">/</button>

    <button onclick="clearExpression()">Effacer</button>
    <button onclick="calculate()">Calculer</button>

    <p id="result">Résultat : </p>

    </div>
  );
}

export default App;
