// BankCommands.js - Componente para mostrar comandos relacionados con el sistema bancario

import React from 'react';

const BankCommands = () => {
  const bankCommands = [
    {
      name: '$balance',
      description: 'Consulta tu saldo actual en el banco'
    },
    {
      name: '$trabajar',
      description: 'Trabaja para ganar dinero (cooldown de 3 minutos)'
    },
    {
      name: '$robar <@usuario>',
      description: 'Intenta robar dinero a otro usuario (riesgo de multa)'
    },
    {
      name: '$donar <@usuario> <cantidad>',
      description: 'Donar una cantidad específica de dinero a otro usuario'
    },
    {
      name: '$ranking',
      description: 'Ver el ranking de los 5 usuarios con más dinero'
    },
    {
      name: '$perfil [@usuario]',
      description: 'Ver tu perfil o el de otro usuario con información bancaria'
    }
  ];

  return (
    <div className="bank-commands-section">
      <h3>Comandos Bancarios</h3>
      <div className="commands-grid">
        {bankCommands.map((command, index) => (
          <div key={index} className="command-card">
            <h4>{command.name}</h4>
            <p>{command.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BankCommands;