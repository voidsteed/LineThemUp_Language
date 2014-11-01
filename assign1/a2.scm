(define (zeno_cost d c f)
  (cond
  ((<= c (/ (real 1) 12))
    0)
  ((<= d (/ (real 1) 9600))
      5)
  (else 
    (+ (zeno_cost (/ (real d) 2) (* c f) f) c)
        )
      )
  )

(define (run2)
  (println "The answer is " (zeno_cost (/ 2.5 9600) 10 10)
  ) )
  


(run2)
