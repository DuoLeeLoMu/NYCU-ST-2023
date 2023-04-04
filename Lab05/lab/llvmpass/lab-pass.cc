/*
  Ref:
  * https://llvm.org/doxygen/
  * https://llvm.org/docs/GettingStarted.html
  * https://llvm.org/docs/WritingAnLLVMPass.html
  * https://llvm.org/docs/ProgrammersManual.html
 */
#include "lab-pass.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Constants.h"

using namespace llvm;

char LabPass::ID = 0;

bool LabPass::doInitialization(Module &M) {
  return true;
}

static Constant *getI8StrVal(Module &M, char const *str, Twine const &name) {
  LLVMContext &ctx = M.getContext();

  Constant *strConstant = ConstantDataArray::getString(ctx, str);

  GlobalVariable *gvStr = new GlobalVariable(M, strConstant->getType(), true,
                                             GlobalValue::InternalLinkage, strConstant, name);

  Constant *zero = Constant::getNullValue(IntegerType::getInt32Ty(ctx));
  Constant *indices[] = {zero, zero};
  Constant *strVal = ConstantExpr::getGetElementPtr(Type::getInt8PtrTy(ctx),
                                                    gvStr, indices, true);

  return strVal;
}

static FunctionCallee printfPrototype(Module &M) {
  LLVMContext &ctx = M.getContext();

  FunctionType *printfType = FunctionType::get(
      Type::getInt32Ty(ctx),
      {Type::getInt8PtrTy(ctx)},
      true);

  FunctionCallee printfCallee = M.getOrInsertFunction("printf", printfType);

  return printfCallee;
}

static FunctionCallee printfPrototype_Space(Module &M) {
  LLVMContext &ctx = M.getContext();

  FunctionType *printfType = FunctionType::get(
      Type::getInt32Ty(ctx),
      {Type::getInt8PtrTy(ctx), Type::getInt32Ty(ctx), Type::getInt8PtrTy(ctx)},
      true);

  FunctionCallee printfCallee = M.getOrInsertFunction("printf", printfType);

  return printfCallee;
}

static FunctionCallee printfPrototype_Address(Module &M) {
  LLVMContext &ctx = M.getContext();

  FunctionType *printfType = FunctionType::get(
      Type::getInt32Ty(ctx),
      {Type::getInt8PtrTy(ctx), Type::getInt8PtrTy(ctx)},
      true);

  FunctionCallee printfCallee = M.getOrInsertFunction("printf", printfType);

  return printfCallee;
}

bool LabPass::runOnModule(Module &M) {
  errs() << "runOnModule\n";

  LLVMContext &ctx = M.getContext();

  Constant *zero = Constant::getNullValue(IntegerType::getInt32Ty(ctx));
  Constant *one = Constant::getIntegerValue(Type::getInt32Ty(ctx), APInt(32, 1));

  GlobalVariable *globalVar = new GlobalVariable(M, Type::getInt32Ty(ctx), false, GlobalValue::ExternalLinkage, zero, "globalVar");

  FunctionCallee printfCallee = printfPrototype(M);
  FunctionCallee printfSpace = printfPrototype_Space(M);
  FunctionCallee printfAddress = printfPrototype_Address(M);

  for (auto &F : M) {
    if ( F.empty() ) {
      continue;
    }
    errs() << F.getName() << "\n";

    BasicBlock &Bstart = F.front();
    BasicBlock &Bend = F.back();

    // Insert code at prologue
    Instruction &Istart = Bstart.front();
    IRBuilder<> BuilderStart(&Istart);

    Value *current_depth = BuilderStart.CreateLoad(Type::getInt32Ty(ctx), globalVar, "globalVar");

    // print depth ( main depth = 0 )
    if ( F.getName() != "main" ) {
      Constant *space = getI8StrVal(M, " ", "space");
      Constant *format = getI8StrVal(M, "%*s", "format");
      BuilderStart.CreateCall(printfSpace, {format, current_depth, space});
    }

    // print function name
    Constant *functionName = getI8StrVal(M, F.getName().data(), "functionName");
    BuilderStart.CreateCall(printfCallee, {functionName});

    // print ": "
    Constant *colon = getI8StrVal(M, ": ", "colon");
    BuilderStart.CreateCall(printfCallee, {colon});

    // print address
    Value *functionPtr = ConstantExpr::getBitCast(&F, Type::getInt32PtrTy(ctx));
    Constant *format = getI8StrVal(M, "%p", "format");
    BuilderStart.CreateCall(printfAddress, {format, functionPtr});

    // print "\n"
    Constant *enter = getI8StrVal(M, "\n", "enter");
    BuilderStart.CreateCall(printfCallee, {enter});

    // add depth
    Value *new_depth = BuilderStart.CreateAdd(current_depth, one);

    // store depth
    BuilderStart.CreateStore(new_depth, globalVar);

    // middle

    // Insert code at epilogue
    Instruction &Iend = Bend.back();
    IRBuilder<> BuilderEnd(&Iend);

    // sub depth
    current_depth = BuilderEnd.CreateLoad(Type::getInt32Ty(ctx), globalVar, "globalVar");
    new_depth = BuilderEnd.CreateSub(current_depth, one);

    // store depth
    BuilderEnd.CreateStore(new_depth, globalVar);

  }

  return true;
}

static RegisterPass<LabPass> X("labpass", "Lab Pass", false, false);