(define (ramanujan depth)
  (define (iter count result)
    (cond
      ((= count 0)
       result)
      (else
        (iter (- count 1) (sqrt (+ 1 (* (+ count 1) result))))
      )
    )
    )
  (cond
    ((= 0 depth)
     1)
    ((= 1 depth)
     (sqrt 3))
    (else 
      (iter (- depth 1) (sqrt (+ 1 (+ depth 1)))))
    )
  )
  


(define (run8)
  (println "pass depth = 0 it should be 0 " (ramanujan 0) )
  (println "Pass depth = 1 Answer should be 1.73....  " (ramanujan 1) )
  (println "pass depth = 2 it should be 2.23.... " (ramanujan 2) )
  (println "pass depth = 3 it should be 2.55.... " (ramanujan 3) )
  (println "pass depth = 4 it should be 2.755.... " (ramanujan 4) )
  )

(run8)
