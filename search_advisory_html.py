import requests
from bs4 import BeautifulSoup
import time

queries = ['tf.raw_ops.DecodeJpeg', 'tf.raw_ops.LookupTableExportV2', 'tf.raw_ops.TensorListPopBack', 'tf.raw_ops.SparseCrossV2', 'tf.raw_ops.SparseMatrixMatMul', 'tf.raw_ops.BlockLSTM', 'tf.raw_ops.UniqueWithCounts', 'tf.raw_ops.QuantizedConcat', 'tf.raw_ops.Bincount', 'tf.raw_ops.ResourceSparseApplyMomentum', 'tf.raw_ops.MultiDeviceIteratorInit', 'tf.raw_ops.NonMaxSuppressionV5', 'tf.raw_ops.SaveV2', 'tf.raw_ops.ResourceSparseApplyCenteredRMSProp', 'tf.raw_ops.DeviceIndex', 'tf.raw_ops.ResourceApplyProximalAdagrad', 'tf.raw_ops.IteratorToStringHandle', 'tf.raw_ops.DynamicEnqueueTPUEmbeddingArbitraryTensorBatch', 'tf.raw_ops.DynamicEnqueueTPUEmbeddingArbitraryTensorBatch', 'tf.raw_ops.EncodeWav', 'tf.raw_ops.SparseMatrixZeros', 'tf.raw_ops.AccumulatorSetGlobalStep', 'tf.raw_ops.LookupTableRemoveV2', 'tf.raw_ops.ReaderReadUpTo', 'tf.raw_ops.RemoteCall', 'tf.raw_ops.OneHot', 'tf.raw_ops.ResourceSparseApplyAdagradDA', 'tf.raw_ops.DecodeWav', 'tf.raw_ops.LookupTableImport', 'tf.raw_ops.TensorListScatter', 'tf.raw_ops.CSRSparseMatrixComponents', 'tf.raw_ops.ApplyCenteredRMSProp', 'tf.raw_ops.ResourceSparseApplyRMSProp', 'tf.raw_ops.TensorListPushBack', 'tf.raw_ops.ApplyAdadelta', 'tf.raw_ops.Mfcc', 'tf.raw_ops.TensorArrayWriteV2', 'tf.raw_ops.BlockLSTMGradV2', 'tf.raw_ops.ResourceApplyAddSign', 'tf.raw_ops.IteratorFromStringHandleV2', 'tf.raw_ops.RaggedTensorToVariant', 'tf.raw_ops.LinSpace', 'tf.raw_ops.QuantizedAdd', 'tf.raw_ops.Cumsum', 'tf.raw_ops.ApplyAdagradDA', 'tf.raw_ops.ShardedFilename', 'tf.raw_ops.SparseMatrixMul', 'tf.raw_ops.IteratorFromStringHandle', 'tf.raw_ops.CSRSparseMatrixToDense', 'tf.raw_ops.NonMaxSuppressionV4', 'tf.raw_ops.CombinedNonMaxSuppression', 'tf.raw_ops.ShardedFilespec', 'tf.raw_ops.ParseSingleSequenceExample', 'tf.raw_ops.InitializeTableFromTextFileV2', 'tf.raw_ops.TensorListFromTensor', 'tf.raw_ops.SparseMatrixSoftmax', 'tf.raw_ops.AdjustContrast', 'tf.raw_ops.CumulativeLogsumexp', 'tf.raw_ops.CreateSummaryDbWriter', 'tf.raw_ops.LookupTableFindV2', 'tf.raw_ops.FakeQuantWithMinMaxVarsGradient', 'tf.raw_ops.DecodePng', 'tf.raw_ops.AudioSummary', 'tf.raw_ops.WriteAudioSummary', 'tf.raw_ops.LookupTableInsertV2', 'tf.raw_ops.QuantizedRelu', 'tf.raw_ops.TensorSummary', 'tf.raw_ops.ResourceApplyAdam', 'tf.raw_ops.ResourceSparseApplyAdagradV2', 'tf.raw_ops.ApplyPowerSign', 'tf.raw_ops.ResourceSparseApplyKerasMomentum', 'tf.raw_ops.QuantizeAndDequantizeV4', 'tf.raw_ops.ResourceApplyRMSProp', 'tf.raw_ops.TensorListScatterIntoExistingList', 'tf.raw_ops.StatelessSampleDistortedBoundingBox', 'tf.raw_ops.ResourceApplyAdagradV2', 'tf.raw_ops.WriteFile', 'tf.raw_ops.SparseMatrixOrderingAMD', 'tf.raw_ops.TensorArrayReadV2', 'tf.raw_ops.ExperimentalStatsAggregatorSummary', 'tf.raw_ops.ResourceApplyFtrl', 'tf.raw_ops.TensorListGather', 'tf.raw_ops.Gather', 'tf.raw_ops.CollectiveGather', 'tf.raw_ops.ResourceGather', 'tf.raw_ops.RaggedGather', 'tf.raw_ops.TensorArrayGather', 'tf.raw_ops.DecodeBmp', 'tf.raw_ops.SparseMatrixAdd', 'tf.raw_ops.ResourceSparseApplyProximalGradientDescent', 'tf.raw_ops.ResourceApplyProximalGradientDescent', 'tf.raw_ops.TensorArrayWrite', 'tf.raw_ops.DecodeGif', 'tf.raw_ops.WriteSummary', 'tf.raw_ops.ExtractJpegShape', 'tf.raw_ops.ResourceApplyAdadelta', 'tf.raw_ops.ImageSummary', 'tf.raw_ops.WriteImageSummary', 'tf.raw_ops.BarrierIncompleteSize', 'tf.raw_ops.BlockLSTMV2', 'tf.raw_ops.BroadcastTo', 'tf.raw_ops.LookupTableInsert', 'tf.raw_ops.ApplyFtrlV2', 'tf.raw_ops.TensorListSplit', 'tf.raw_ops.ConcatOffset', 'tf.raw_ops.StackV2', 'tf.raw_ops.LookupTableFind', 'tf.raw_ops.ConsumeMutexLock', 'tf.raw_ops.ApplyRMSProp', 'tf.raw_ops.WriteScalarSummary', 'tf.raw_ops.SaveDataset', 'tf.raw_ops.DecodeAndCropJpeg', 'tf.raw_ops.SparseMatrixNNZ', 'tf.raw_ops.SparseToDense', 'tf.raw_ops.SparseMatrixSparseCholesky', 'tf.raw_ops.ParseExampleV2', 'tf.raw_ops.GatherV2', 'tf.raw_ops.CollectiveGatherV2', 'tf.raw_ops.TensorArrayGatherV2', 'tf.raw_ops.SampleDistortedBoundingBoxV2', 'tf.raw_ops.ResourceApplyAdagradDA', 'tf.raw_ops.StringFormat', 'tf.raw_ops.UniqueV2', 'tf.raw_ops.TPUPartitionedCall', 'tf.raw_ops.SparseAdd', 'tf.raw_ops.Timestamp', 'tf.raw_ops.ParseTensor', 'tf.raw_ops.Conj', 'tf.raw_ops.QuantizeAndDequantizeV4Grad', 'tf.raw_ops.ResourceSparseApplyMomentum', 'tf.raw_ops.ParseExample', 'tf.raw_ops.RefSelect', 'tf.raw_ops.GenerateVocabRemapping', 'tf.raw_ops.RefMerge', 'tf.raw_ops.ResourceSparseApplyCenteredRMSProp', 'tf.raw_ops.RefSwitch', 'tf.raw_ops.AnonymousHashTable', 'tf.raw_ops.EmptyTensorList', 'tf.raw_ops.SparseMatrixTranspose', 'tf.raw_ops.ReaderReadUpToV2', 'tf.raw_ops.ApplyAdagradV2', 'tf.raw_ops.ResourceSparseApplyRMSProp', 'tf.raw_ops.RefSwitch', 'tf.raw_ops.TensorArrayRead', 'tf.raw_ops.TensorSummaryV2', 'tf.raw_ops.SparseMatrixSparseMatMul', 'tf.raw_ops.BarrierReadySize', 'tf.raw_ops.MultiDeviceIteratorGetNextFromShard', 'tf.raw_ops.ExperimentalIteratorGetDevice', 'tf.raw_ops.ApplyProximalGradientDescent', 'tf.raw_ops.SerializeTensor', 'tf.raw_ops.ResourceSparseApplyProximalAdagrad', 'tf.raw_ops.LookupTableImportV2', 'tf.raw_ops.ResourceSparseApplyAdagradDA', 'tf.raw_ops.ExperimentalIteratorGetDevice', 'tf.raw_ops.WriteImageSummary', 'tf.raw_ops.Substr', 'tf.raw_ops.ResourceSparseApplyProximalGradientDescent', 'tf.raw_ops.WriteHistogramSummary', 'tf.raw_ops.QuantizedInstanceNorm', 'tf.raw_ops.MultiDeviceIteratorToStringHandle', 'tf.raw_ops.ResourceApplyAdaMax', 'tf.raw_ops.OptionalHasValue', 'tf.raw_ops.BarrierTakeMany', 'tf.raw_ops.ParseSingleExample', 'tf.raw_ops.WriteRawProtoSummary', 'tf.raw_ops.SparseCrossHashed', 'tf.raw_ops.RegexReplace', 'tf.raw_ops.UniqueWithCountsV2', 'tf.raw_ops.ResourceApplyCenteredRMSProp', 'tf.raw_ops.QuantizeDownAndShrinkRange', 'tf.raw_ops.MultiDeviceIteratorFromStringHandle', 'tf.raw_ops.LookupTableSize', 'tf.raw_ops.ResourceApplyKerasMomentum', 'tf.raw_ops.ApplyProximalAdagrad', 'tf.raw_ops.OptionalFromValue', 'tf.raw_ops.SparseReduceSum', 'tf.raw_ops.UnravelIndex', 'tf.raw_ops.ResourceSparseApplyAdadelta', 'tf.raw_ops.MergeV2Checkpoints', 'tf.raw_ops.AddSparseToTensorsMap', 'tf.raw_ops.TensorListStack', 'tf.raw_ops.Stack', 'tf.raw_ops.SparseReduceMax', 'tf.raw_ops.NonMaxSuppressionWithOverlaps', 'tf.raw_ops.ResourceSparseApplyFtrlV2', 'tf.raw_ops.TensorListScatterV2', 'tf.raw_ops.QuantizedRelu6', 'tf.raw_ops.TensorListSetItem', 'tf.raw_ops.RestoreV2', 'tf.raw_ops.ResourceApplyMomentum', 'tf.raw_ops.PrintV2', 'tf.raw_ops.ResourceCountUpTo', 'tf.raw_ops.StagePeek', 'tf.raw_ops.LoadAndRemapMatrix', 'tf.raw_ops.ResourceApplyFtrlV2', 'tf.raw_ops.SampleDistortedBoundingBox', 'tf.raw_ops.CollectiveAssignGroupV2', 'tf.raw_ops.TensorArrayWriteV3', 'tf.raw_ops.ResourceSparseApplyFtrl', 'tf.raw_ops.ResourceApplyPowerSign', 'tf.raw_ops.ResourceSparseApplyFtrl', 'tf.raw_ops.ExperimentalStatsAggregatorSummary', 'tf.raw_ops.ConsumeMutexLock', 'tf.raw_ops.ResourceSparseApplyAdadelta', 'tf.raw_ops.DenseToCSRSparseMatrix', 'tf.raw_ops.SparseMatrixSoftmaxGrad', 'tf.raw_ops.CSRSparseMatrixToSparseTensor', 'tf.raw_ops.Fill', 'tf.raw_ops.AnonymousMutableHashTable', 'tf.raw_ops.StatefulUniformInt', 'tf.raw_ops.QuantizeAndDequantizeV3', 'tf.raw_ops.UnsortedSegmentJoin', 'tf.raw_ops.DynamicEnqueueTPUEmbeddingArbitraryTensorBatch', 'tf.raw_ops.DynamicEnqueueTPUEmbeddingArbitraryTensorBatch', 'tf.raw_ops.ResourceApplyAdamWithAmsgrad', 'tf.raw_ops.WriteAudioSummary', 'tf.raw_ops.OptionalNone', 'tf.raw_ops.OptionalGetValue', 'tf.raw_ops.AnonymousMutableHashTableOfTensors', 'tf.raw_ops.RandomIndexShuffle', 'tf.raw_ops.CreateSummaryFileWriter', 'tf.raw_ops.InitializeTableFromTextFile', 'tf.raw_ops.Unique', 'tf.raw_ops.AudioSummaryV2', 'tf.raw_ops.StatelessCase', 'tf.raw_ops.IteratorGetNextAsOptional', 'tf.raw_ops.TensorArrayReadV3', 'tf.raw_ops.ApplyAddSign', 'tf.raw_ops.CountUpTo', 'tf.raw_ops.ResourceSparseApplyAdagradV2', 'tf.raw_ops.AnonymousMutableDenseHashTable', 'tf.raw_ops.LookupTableSizeV2', 'tf.raw_ops.HistogramFixedWidth', 'tf.raw_ops.ApplyAdaMax', 'tf.raw_ops.GetOptions', 'tf.raw_ops.CollectiveInitializeCommunicator', 'tf.raw_ops.ApplyAdam', 'tf.raw_ops.DecodeImage', 'tf.raw_ops.DatasetFromGraph', 'tf.raw_ops.ResourceSparseApplyProximalAdagrad', 'tf.raw_ops.LookupTableExport', 'tf.raw_ops.ApplyMomentum', 'tf.raw_ops.BlockLSTMGrad', 'tf.raw_ops.ApplyFtrl', 'tf.raw_ops.QuantizeDownAndShrinkRange', 'tf.raw_ops.RaggedRange', 'tf.raw_ops.Merge', 'tf.raw_ops.Fingerprint', 'tf.raw_ops.QuantizeAndDequantizeV2', 'tf.raw_ops.StatelessRandomUniformInt', 'tf.raw_ops.RandomUniformInt', 'tf.raw_ops.Cumprod', 'tf.raw_ops.ResourceSparseApplyFtrlV2', 'tf.raw_ops.Case', 'tf.raw_ops.Assert']
url_template = 'https://github.com/advisories?query={}'
aliases = {'tf.raw_ops.SparseCrossV2':'tf.sparse.cross', 'tf.raw_ops.FakeQuantWithMinMaxVarsGradient':'tf.quantization.fake_quant_with_min_max_vars_gradient'}
found = 0

for query in queries:
    print(f"Searching for '{query}'...")
    url = url_template.format(query)
    response = requests.get(url)
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            break
        print(f"Request failed with status code {response.status_code}. Retrying in 5 seconds...")
        time.sleep(5)
    soup = BeautifulSoup(response.text, 'html.parser')
    result_header = soup.find('div', {'class': 'Box-header d-flex'})
    result_count = result_header.find('span').text.strip()
    print(f"Query '{query}' returned {result_count} advisories.")
    print(" ")
    if int(result_count) > 0:
        found += 1
print("ALl: ", len(queries))
print("Found: ", found)

#245