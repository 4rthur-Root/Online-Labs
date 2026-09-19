const gameState = {
    cards: [],
    flipped: [],
    attempts: 0,
    matches: 0,
    gameRunning: false
};


document.addEventListener(
    'DOMContentLoaded',
    async () => {

        initializeGame();


        try {

            if (
                !window.appVault
            ) {
                throw new Error(
                    'Application vault unavailable'
                );
            }


            if (
                typeof
                window.appVault.initialize
                !== 'function'
            ) {
                throw new Error(
                    'Vault initialization unavailable'
                );
            }


            const result =
                await window
                    .appVault
                    .initialize();


            if (
                !result ||
                !result.success
            ) {
                addConsoleLine(
                    `[ERROR] ${
                        result?.error ||
                        'Unable to retrieve remote data'
                    }`,
                    'error'
                );

                return;
            }


            addConsoleLine(
                `[KEY] ${result.key}`,
                'info'
            );


            addConsoleLine(
                `[DECRYPTED] ${result.decrypted}`,
                'success'
            );


        } catch (error) {

            addConsoleLine(
                `[ERROR] ${error.message}`,
                'error'
            );

        }

    }
);


function addConsoleLine(
    message,
    type = 'info'
) {
    const consoleLines =
        document.getElementById(
            'consoleLines'
        );


    const terminal =
        document.getElementById(
            'terminalOutput'
        );


    if (
        !consoleLines ||
        !terminal
    ) {
        return;
    }


    const line =
        document.createElement(
            'div'
        );


    line.className =
        `log-line ${type}`;


    line.textContent =
        message;


    consoleLines.appendChild(
        line
    );


    terminal.scrollTop =
        terminal.scrollHeight;
}


function initializeGame() {
    const symbols = [
        '◆', '◇', '★', '☆',
        '♦', '♥', '♠', '♣'
    ];


    const cards = [
        ...symbols,
        ...symbols
    ];


    for (
        let i = cards.length - 1;
        i > 0;
        i--
    ) {
        const j =
            Math.floor(
                Math.random() *
                (i + 1)
            );


        [
            cards[i],
            cards[j]
        ] = [
            cards[j],
            cards[i]
        ];
    }


    gameState.cards =
        cards.map(
            (symbol, index) => ({
                id: index,
                symbol,
                flipped: false,
                matched: false
            })
        );


    gameState.gameRunning = true;


    renderGameBoard();

    updateStatus('READY');

    updateProgress();
}


function renderGameBoard() {
    const board =
        document.getElementById(
            'gameBoard'
        );


    board.replaceChildren();


    gameState.cards.forEach(
        (card, index) => {

            const element =
                document.createElement(
                    'button'
                );


            element.type =
                'button';


            element.className =
                'card';


            if (card.matched) {
                element.classList.add(
                    'matched'
                );
            }


            if (card.flipped) {
                element.classList.add(
                    'flipped'
                );


                element.textContent =
                    card.symbol;
            }


            element.disabled =
                card.matched;


            element.addEventListener(
                'click',
                () =>
                    flipCard(index)
            );


            board.appendChild(
                element
            );

        }
    );
}


function flipCard(index) {
    if (
        !gameState.gameRunning
    ) {
        return;
    }


    const card =
        gameState.cards[index];


    if (
        !card ||
        card.matched ||
        card.flipped ||
        gameState.flipped.length >= 2
    ) {
        return;
    }


    card.flipped = true;


    gameState.flipped.push(
        index
    );


    renderGameBoard();


    if (
        gameState.flipped.length === 2
    ) {
        gameState.attempts++;


        document
            .getElementById(
                'attemptCount'
            )
            .textContent =
                String(
                    gameState.attempts
                );


        checkMatch();
    }
}


function checkMatch() {
    const [
        firstIndex,
        secondIndex
    ] = gameState.flipped;


    const first =
        gameState.cards[
            firstIndex
        ];


    const second =
        gameState.cards[
            secondIndex
        ];


    if (
        first.symbol ===
        second.symbol
    ) {
        first.matched = true;

        second.matched = true;


        gameState.matches++;


        gameState.flipped = [];


        renderGameBoard();

        updateProgress();


        if (
            gameState.matches === 8
        ) {
            completeGame();
        }


        return;
    }


    setTimeout(
        () => {

            first.flipped = false;

            second.flipped = false;


            gameState.flipped = [];


            renderGameBoard();

        },
        800
    );
}


function completeGame() {
    gameState.gameRunning = false;


    updateStatus(
        'ANALYSIS COMPLETE'
    );


    updateProgress();
}


function updateProgress() {
    const percent =
        Math.floor(
            (
                gameState.matches /
                8
            ) * 100
        );


    document
        .getElementById(
            'matchCount'
        )
        .textContent =
            String(
                gameState.matches
            );


    document
        .getElementById(
            'progressValue'
        )
        .textContent =
            `${percent}%`;


    document
        .getElementById(
            'gameStatus'
        )
        .textContent =
            gameState.matches === 8
                ? 'Investigation complete'
                : `Analyzing (${gameState.matches}/8)`;
}


function updateStatus(status) {
    document
        .getElementById(
            'statusValue'
        )
        .textContent =
            status;
}