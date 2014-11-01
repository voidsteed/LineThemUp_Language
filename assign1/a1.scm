(define (compare x y)
  (cond  
  ((<= x y) 
        x)
    ((> x y)
        y)
        )
    )
  

(define (run)
  (println "Minimum is " (compare 1 4)))

(run)
