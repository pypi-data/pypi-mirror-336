#!/usr/bin/env python

import argparse
import dotenv
dotenv.load_dotenv()

from .confident_solver import ConfidentSolver, LlmModelEnum, ConfidenceModelEnum, OutputSchemaTypeEnum

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, default="Jen enters a lottery by picking $4$ distinct numbers from $S=\\{1,2,3,\\cdots,9,10\\}.$ $4$ numbers are randomly chosen from $S.$ She wins a prize if at least two of her numbers were $2$ of the randomly chosen numbers, and wins the grand prize if all four of her numbers were the randomly chosen numbers. The probability of her winning the grand prize given that she won a prize is $\\tfrac{m}{n}$ where $m$ and $n$ are relatively prime positive integers. Find $m+n$.")
    parser.add_argument("--llm_model", default=LlmModelEnum.GPT_4O_MINI, choices=[_.value for _ in LlmModelEnum])
    parser.add_argument("--confidence_model", default=ConfidenceModelEnum.MSPRT, choices=[_.value for _ in ConfidenceModelEnum])
    parser.add_argument("--output_type", default=OutputSchemaTypeEnum.FLOAT, choices=[_.value for _ in OutputSchemaTypeEnum])
    parser.add_argument("--debug", action="store_true")

    args = parser.parse_args()

    consol = ConfidentSolver(
        llm_model=args.llm_model,
        confidence_model=args.confidence_model,
        output_schema=args.output_type,
    )
    res = consol.invoke(args.prompt, debug=args.debug)
    if args.debug:
        print(res.to_csv())
    else:
        print(res)


if __name__ == "__main__":
    main()
