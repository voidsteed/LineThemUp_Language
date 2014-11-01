(define (zorp i f)
  (define (iter x y z count)
    ;got this iterative idea from Kaleb and Dr.j
    ;it has 3 base cases and shift to right with box like fib's doing
        (cond
            ((= count 0)
                x)
            ((= count 1)
                y)
            ((= count 2)
                z)
            (else
                (iter y z (/ (+ z (* (- z x) (- z x))) (+ (- x (* 2 x)) z)) (- count 1))
                )
            )
        )
    (iter (f 0) (f 1) (f 2) i)
    )
(println "iter: " (zorp 6 (lambda (x) (* x x))) "It should be 36")

