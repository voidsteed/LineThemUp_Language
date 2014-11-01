(define (root3 n)
  (define (iter max min guess)
    (cond
      ((< (* guess guess guess) n)
       (iter max guess (/ (real (+ guess max)) 2))
       )
      ((> (* guess guess guess) n)
       (iter guess min (/ (real (+ guess min)) 2))
       )
      (else 
        guess)
    )
    )
    (iter (+ n 1) 0 1)
  )

(define (run4)
  (println "n = 27, The root is " (root3 27) " The answer should 3.")
  (println "n = 64, The root is " (root3 64) " The answer should 4.")
  (println "n = 8, The root is " (root3 8) " The answer should 2.")
  (println "n = 100, The root is " (root3 100) " The answer should 4.64.")

  )

(run4)
