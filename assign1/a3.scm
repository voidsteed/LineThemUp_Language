(define (min8 a b c d e f g h)
  (define (compare x y) 
    (if (<= x y) 
        x
        y
    )
  )
  (compare h (compare g (compare f (compare e (compare d (compare c (compare b a)))))))
)  

(define (run3)
  (println "minimum is " (min8 10 4 3 9 5 6 7 8))
  (println ["It compared 7 times"])
  (println "minimum is " (min8 1 4 3 19 5 16 7 8))
  (println ["It compared 7 times"])
  (println "minimum is " (min8 10 4 31 9 51 6 74 8))
  (println ["It compared 7 times"])
  )

(run3)

