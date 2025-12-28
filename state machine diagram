stateDiagram-v2
    [*] --> Idle

    Idle --> UI_Ready : Server Start
    UI_Ready --> WaitingInput : Load index.html

    WaitingInput --> Reset : New Chat
    Reset --> WaitingInput

    WaitingInput --> ChatProcessing : Send Message
    ChatProcessing --> ChatResponse : LLM Reply
    ChatResponse --> WaitingInput

    WaitingInput --> PDFUploaded : Upload PDF
    PDFUploaded --> PDFValidation

    PDFValidation --> Error : Invalid PDF
    PDFValidation --> PDFProcessing : Valid PDF

    PDFProcessing --> PDFLLM
    PDFLLM --> PDFResponse
    PDFResponse --> WaitingInput

    Error --> WaitingInput
