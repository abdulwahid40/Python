def compute_primes(bound):

    answer = list(range(2,bound))
    for divisor in range(2,bound):
        for item in answer:
                if item % divisor == 0:
                    answer.remove(item)
                    if divisor not in answer:
                        answer.append(divisor)
            
    return answer

print(len(compute_primes(200)))
print(len(compute_primes(2000)))