(define (pt row)

(define (printSpace count)
  (cond
    ((= count 0) (print " "))
    (else (printSpace (- count 1))
          (print " ")))
    )

(define (printT l)
  (cond
    ((null? l) 1)
    (else (print (car l) " ")
          (printT (cdr l))
          )
    ) 
  )


(define (printList l count)
  (cond
    ((null? l) 1)
    (else (printSpace count) (printT (car l))
          (println)
          (printList (cdr l) (- count 1))
      )
    )
  )

  


(define (helper row tempList)
  (define (iter colCount l)
    (define (pascal row col)
      (cond
        ((or (= row col) (= 1 col)) 
      1)
      (else (+ (pascal (- row 1) (- col 1)) (pascal (- row 1) col)) )
      )
    )
  (if (= colCount 0) 
      l
      (iter (- colCount 1) (cons (pascal (+ row 1) colCount) l))
      ))
  (cond
  ((= row -1)
   tempList
   )
   (else (helper (- row 1) (cons (iter (+ row 1) ()) tempList)))
    )
)
(printList (helper row ()) row)
)

(pt 7)
