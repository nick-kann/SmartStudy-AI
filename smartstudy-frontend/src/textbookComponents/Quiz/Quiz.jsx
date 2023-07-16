import React, {useState} from 'react';
const Quiz = () => {
  const [activeQuestion, setActiveQuestion] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState('')

  const onClickNext = () => {
    setActiveQuestion((prev) => prev + 1)
  }

  const { questions } = quiz
  const { question, choices } = questions[activeQuestion]

  return (
    <div>
      <h1>Quiz</h1>
      <h2>{question}</h2>
      <ul>
        {choices.map((item) => (
          <li>{item}</li>
        ))}
      </ul>
      <button onClick={onClickNext}>Next</button>
    </div>
  )
}
