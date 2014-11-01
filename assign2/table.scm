(define (assoc x y)
    (cond
        ((null? y) #f)
        ((equal? x (caar y)) (car y))
        (else (assoc x (cdr y)))
        )
    )
(define table nil)
(define (put tag function)
    (assign table (cons (list tag function) table))
    )
(define (get tag) (cadr (assoc tag table)))
(define (remove tag)
    (define (iter prev items)
        (inspect items)
        (cond
            ((null? items) #f)
            ((equal? tag (caar items))
                (if (null? prev)
                    (assign table (cdr items))
                    (set-cdr! prev (cdr items))
                    )
                #t
                )
            (else
                (iter items (cdr items))
                )
            )
        )
    (iter nil table)
    )

;{
(put 'x 'y)
(put '(a 1) 3)
(put 3 '(z z))

(inspect (get 'x))
(inspect (get '(a 1)))

(remove '(a 1))
(inspect table)
;}
